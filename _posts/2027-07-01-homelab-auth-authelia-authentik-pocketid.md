---
layout: blog-post
title: "Choosing an Auth Stack for My Homelab: Authentik, Authelia, PocketID, and TinyAuth"
excerpt: "How I decided between forward-auth and OIDC, why I moved my ~50-service homelab from Authentik to Authelia, and where PocketID and TinyAuth fit in."
disqus_id: /2027/07/01/homelab-auth-authelia-authentik-pocketid/
tags:
    - Homelab
    - Docker
    - Traefik
    - Authelia
    - Authentik
    - PocketID
    - Authentication
    - Passkeys
    - OIDC
    - Self-Hosted
---

*This article was written with the assistance of AI.*

---

My homelab has around 50 services behind Traefik — Immich, Jellyfin, Paperless, Dozzle, Termix, a dozen dev tools, and so on. I've been running Authentik as the gate for everything accessible from outside my LAN. It worked, but every time I wanted to tweak an access rule or add a new service, I had to click through the Authentik admin UI. That bothered me: everything else in my homelab lives in a git repo as YAML, but my auth configuration lived as mutable database state behind a web portal.

I also wanted passkey-first login. I'd been experimenting with PocketID and TinyAuth to scratch that itch, and I ended up with three different auth systems running in parallel. That's a smell.

This is how I untangled it.

## Forward-Auth vs OIDC

Before I could pick a tool, I needed to be honest about what I actually use. There are two very different auth patterns, and most homelabbers (including me, for a while) conflate them.

### Forward-Auth

In forward-auth, the reverse proxy intercepts every request and asks an auth service "is this person allowed?" before passing the request to the app. The app itself knows nothing about authentication — it just receives traffic and trusts that the proxy already vetted it.

In Traefik it looks like this:

```yaml
http:
  middlewares:
    authelia:
      forwardAuth:
        address: "http://authelia:9091/api/authz/forward-auth"
        trustForwardHeader: true
        authResponseHeaders:
          - Remote-User
          - Remote-Groups
          - Remote-Email
```

Every request to a service with this middleware triggers a subrequest to Authelia. Authelia returns `200 OK` if the user has a valid session, or `401` / `302` to redirect to the login page. The app only ever sees requests that have already passed the gate, with optional identity headers like `Remote-User` injected.

**What forward-auth is good for**: protecting apps that know nothing about authentication. Termix, Dozzle, qBittorrent, changedetection, most dashboard-style homelab tools. You get a single sign-on across all of them via one shared cookie.

**What it's not good for**: telling the app *who* the user is in a structured way. The headers are a convention, not a contract — and apps that care about real identity usually want OIDC.

### OIDC

In OIDC (OpenID Connect), the app itself speaks the protocol. When you visit it, it redirects you to the identity provider (Authelia, Authentik, Google, whoever), you authenticate there, and the IdP redirects you back with a signed ID token. The app reads your identity, groups, email, and creates its *own* user session using that data.

This is how I log into Immich or Nextcloud with "Login with Authentik" — the app knows it's me, maps my `admins` group to its `administrator` role, and shows me my own photos.

**What OIDC is good for**: apps that need to know who you are. Nextcloud, Immich, Outline, Grafana, Jellyfin (partially). First-class identity mapping, role syncing, per-user data.

**What it's not good for**: apps that don't speak OIDC. Running OIDC in front of Termix requires a second proxy like oauth2-proxy to translate OIDC tokens into a forward-auth-like gate.

### Which Do You Need?

The simplest way to think about it:

- If the app has a "Login with SSO" button → **OIDC**
- If the app has no login at all, or has its own standalone login you want to bypass → **forward-auth**

My homelab is mostly the second category. Almost everything I run is a utility dashboard or a niche tool that was never designed to support an external IdP. Forward-auth covers it. Only a handful of apps (Immich, Outline, Nextcloud) speak OIDC natively, and for those I was using Authentik as the issuer.

## The Contenders

With the terminology clear, here are the four systems I evaluated.

### Authentik

A full identity provider. Supports OIDC, OAuth 2.1, SAML 2.0, LDAP outpost, SCIM provisioning, federated IdPs (sign in with Google/GitHub as backend), device code flow, token exchange, dynamic client registration, property mappings, custom stages and flows.

It's enterprise-grade. It also runs four containers: server, worker, Postgres, Redis. Configuration lives in a web UI and a Postgres database. You can export policies, but the source of truth is the database, not a file.

For a company with hundreds of employees and dozens of SaaS integrations, Authentik is the right answer. For a homelab where I'm the only user, it's deeply overbuilt — and the web-UI-as-config model works against the GitOps philosophy I use everywhere else.

### Authelia

A lightweight auth server. Single Go binary, single container, configured through a YAML file. Does both forward-auth and OIDC. Passkey / WebAuthn support landed natively in v4.38 and got a proper "Sign in with Passkey" button in v4.39.

OIDC feature set is narrower than Authentik's — no SAML, no LDAP outpost, no SCIM, no dynamic client registration. Clients have to be declared in `configuration.yml`. For my setup that's a feature, not a bug: every OIDC app becomes one more YAML block that lives in git.

### PocketID

A minimal OIDC provider, passkey-first by design. Gorgeous login flow: click the button, touch your YubiKey or Face ID, you're in. No password stored anywhere.

The limitation is right there in the name: it's OIDC only. It doesn't do forward-auth. If I wanted to protect Termix or Dozzle with PocketID, I'd need to pair it with oauth2-proxy or traefik-forward-auth as a second component. That puts me back at two services to do what Authelia does alone.

### TinyAuth

A very small forward-auth service. Docker-labels-driven, minimal config, supports passkeys. Ideal if you want the simplest possible thing and you only have five services.

For a fifty-service setup I outgrew it quickly. No fine-grained access control rules, thinner session and rate-limiting story, smaller community.

## The Decision

Ranked by OIDC feature breadth: **Authentik > Authelia > PocketID**. Authentik wins on paper.

Ranked by fit for my homelab: **Authelia > PocketID > Authentik > TinyAuth**. The reasoning:

- **Authelia** covers both halves of my auth story (forward-auth and OIDC) in one container, with pure YAML config. It has native passkey login. Every Authentik feature it lacks (SAML, LDAP, SCIM, federation) is one I wasn't using.
- **PocketID** has the best passkey UX but only handles OIDC. Using it would force me to run a second forward-auth proxy, which defeats the simplification.
- **Authentik** is the most capable but the least ergonomic for a single-admin GitOps setup.
- **TinyAuth** is too thin for my service count.

So Authelia replaces all three — Authentik, PocketID, and TinyAuth — with one container.

## The Migration

My services fall into two groups based on how they integrated with Authentik:

1. **Forward-auth only** (the majority): Traefik middleware `authentik@file` gated the route. Migration is a one-line label swap.
2. **OIDC clients**: the app itself speaks OIDC to Authentik. Migration means registering the app as a client in Authelia's `configuration.yml` and updating the app's OIDC settings (issuer URL, client ID, secret).

It turned out I had zero active OIDC clients — I'd considered them for Immich and Nextcloud but never wired them up. Every service was pure forward-auth. That made the migration trivial.

### Setting Up Authelia

```yaml
# docker-compose.yml
services:
  authelia:
    image: authelia/authelia:latest
    container_name: authelia
    restart: unless-stopped
    environment:
      AUTHELIA_IDENTITY_VALIDATION_RESET_PASSWORD_JWT_SECRET_FILE: /secrets/jwt_secret
      AUTHELIA_SESSION_SECRET_FILE: /secrets/session_secret
      AUTHELIA_STORAGE_ENCRYPTION_KEY_FILE: /secrets/storage_encryption_key
    volumes:
      - ./config:/config
      - ./secrets:/secrets:ro
    networks:
      - proxy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.authelia.rule=Host(`auth.desktop.madhur.co.in`)"
      - "traefik.http.routers.authelia.entrypoints=websecure"
      - "traefik.http.routers.authelia.tls.certresolver=letencrypt"
      - "traefik.http.services.authelia.loadbalancer.server.port=9091"

networks:
  proxy-network:
    external: true
```

Secrets live in a gitignored `secrets/` directory, generated once with `openssl rand -hex 64`. The rest of the configuration sits in `config/configuration.yml`, committed to git.

A minimal `configuration.yml` for passkey-first login with `two_factor` policy:

```yaml
theme: dark

server:
  address: 'tcp://0.0.0.0:9091'

webauthn:
  disable: false
  enable_passkey_login: true
  display_name: 'Madhur Homelab'
  selection_criteria:
    discoverability: required
    user_verification: required

authentication_backend:
  password_reset:
    disable: true
  file:
    path: /config/users_database.yml
    watch: true
    password:
      algorithm: argon2

access_control:
  default_policy: deny
  rules:
    - domain: 'auth.desktop.madhur.co.in'
      policy: bypass
    - domain: '*.desktop.madhur.co.in'
      policy: two_factor

session:
  cookies:
    - domain: 'desktop.madhur.co.in'
      authelia_url: 'https://auth.desktop.madhur.co.in'
      default_redirection_url: 'https://desktop.madhur.co.in'
      name: authelia_session
      inactivity: '1 hour'
      expiration: '12 hours'
      remember_me: '1 month'

storage:
  local:
    path: /config/db.sqlite3

notifier:
  filesystem:
    filename: /config/notifications.txt
```

The key flag for PocketID-like UX is `enable_passkey_login: true` under `webauthn`. Combined with `discoverability: required` and `user_verification: required`, this adds a "Sign in with a passkey" button on the login page. A passkey with user verification counts as two factors (possession + biometric/PIN), so it satisfies the `two_factor` policy in one tap.

### The Forward-Auth Middleware

```yaml
# traefik/dynamic/authelia-middleware.yml
http:
  middlewares:
    authelia:
      forwardAuth:
        address: "http://authelia:9091/api/authz/forward-auth"
        trustForwardHeader: true
        authResponseHeaders:
          - Remote-User
          - Remote-Groups
          - Remote-Email
          - Remote-Name
```

Traefik's file provider picks this up automatically. Any router that references `authelia@file` as middleware is now gated by Authelia.

### Swapping the Labels

Across all my docker-compose files, I replaced `middlewares=authentik@file` with `middlewares=authelia@file`:

```bash
grep -rl 'middlewares=authentik@file' --include=docker-compose.yml \
  | xargs sed -i 's/middlewares=authentik@file/middlewares=authelia@file/g'
```

Then reloaded each service so Traefik saw the new labels:

```bash
for svc in n8n prefect code-server dozzle paperless jellyfin firefly \
           immich gatus it-tools bookstack glance homepage termix ...; do
  (cd "$svc" && docker compose up -d)
done
```

Twenty services, zero downtime, one commit.

## End State

One auth container, one YAML file, passkey login on everything. Authentik, PocketID, and TinyAuth are all gone. My git history shows auth policy changes per-service, per-commit — the GitOps hygiene I wanted from the start.

A few lessons that would have saved me time:

1. **Decide forward-auth vs OIDC before picking a tool.** They solve different problems. Most homelab apps need forward-auth; the tools that do both (Authelia, Authentik) are strictly more useful than OIDC-only tools (PocketID) for a generalist setup.
2. **Don't put secrets in `configuration.yml` if you're also using `*_FILE` env vars.** Authelia will fail to start with "already defined in other configuration sources" — it refuses to resolve the same key from two places. Use one or the other.
3. **Passkey-login requires discoverable credentials.** Set `webauthn.selection_criteria.discoverability: required` *before* registering your first passkey. Otherwise you'll register a regular (non-discoverable) WebAuthn credential that works as a second factor but can't be used for usernameless login.
4. **More features ≠ better fit.** Authentik is the most capable of the four by a wide margin. For a single-admin homelab, that capability is mostly dead weight, and the web-UI-as-config model actively gets in the way of reproducibility.

If you're running a similar setup and itching to consolidate, Authelia is where I'd start.
