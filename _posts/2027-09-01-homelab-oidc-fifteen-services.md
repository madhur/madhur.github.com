---
layout: blog-post
title: "Five Decisions for an OIDC-First Homelab"
excerpt: "After moving auth to Authelia, the easy questions were done and the interesting ones were left: native OIDC or forward-auth, local fallback or not, when to require a passkey, how long a session should live, and where secrets actually belong."
disqus_id: /2027/09/01/homelab-oidc-fifteen-services/
tags:
    - Homelab
    - Docker
    - Authelia
    - OIDC
    - SSO
    - Passkeys
    - Traefik
    - Self-Hosted
---

*This article was written with the assistance of AI.*

---

A couple of months ago I [consolidated my homelab auth stack on Authelia]({% post_url 2027-07-01-homelab-auth-authelia-authentik-pocketid %}). That migration answered the "which tool" question. It didn't answer the harder questions that come after: which apps should speak OIDC, which should stay on forward-auth, what happens when the IdP is down, and how aggressive 2FA and session expiration should be when the only user is me.

This post is about the five design decisions I ended up making, and why each one came out the way it did. The implementation details aren't interesting — Authelia is a YAML file, the apps are Docker containers — so I'm leaving them out. What matters is the shape of the policy.

## Decision 1: Native OIDC Where the App Has Its Own Identity Concept

Forward-auth is one cookie at the gate. The app behind it knows you got past Authelia. It does not know who you are.

That's fine for most homelab tools — Dozzle, Termix, qBittorrent, Olivetin. They don't care about identity. They want one logged-in operator and a working session. A forward-auth gate gives them that with zero per-app configuration.

It is *not* fine for apps that model users as first-class objects: Outline workspaces, Immich libraries, Bookstack pages, Linkwarden's per-user collections. Behind forward-auth those apps still ask you to register, still create their own user record, still want a password they manage themselves. You end up logging in twice — once at Authelia, once at the app — and the app's idea of "you" is unrelated to Authelia's.

So my rule for this round was simple: **if the app supports native OIDC in its open-source build and has a meaningful concept of "the user," wire it up. Otherwise leave it on forward-auth.**

That gave me a clear yes/no answer for every container:

- Native OIDC, enabled now: Outline, Immich, Paperless-ngx, BookStack, Memos, Linkwarden, Planka, OpenGist, Homebox, Vaultwarden, Dawarich, Journiv, Qui, Termix — plus Komodo, already done previously.
- Native OIDC but skipped this round: Nextcloud, Jellyfin, and Home Assistant all require manual plugin installs in the app's admin UI. Worth doing later, not worth batching.
- Native OIDC but with known issues: Karakeep has known interop problems with Authelia, AKHQ requires file-based YAML, Gatus needs an allowlist. Deferred.
- Paid only or no OIDC: Docmost, n8n enterprise, Firefly III, Glance, several utility apps. Stay on forward-auth.

That left fifteen apps for the OIDC batch, which is also where the title of this post comes from. The decision I want to flag is the rule, not the count: **OIDC for identity-aware apps, forward-auth for everything else.** Putting OIDC on top of an app that doesn't have a user concept gives you nothing forward-auth doesn't already.

## Decision 2: Local Login Stays as a Fallback

Most apps with OIDC support also let you choose whether the OIDC button replaces the password form or sits alongside it. The setting goes by different names — `OIDC_ONLY`, `AUTH_METHOD`, `AUTO_LAUNCH`, sometimes a checkbox in an admin UI — but it's always a binary: OIDC alongside the form, or OIDC instead of it.

The temptation is "instead of." It's cleaner. One login button, one identity source, no temptation to fall back to a separately-managed local password that drifts out of sync.

I went the other way: **wherever possible, keep the local login form available alongside the OIDC button.**

The reasoning is fragility. Authelia is one container. If it's down for any reason — a config error in a YAML push, the storage backing it gone, a stuck container after a host reboot — and every app is OIDC-only, every app is unreachable. That's a worse state than the world before SSO, where each app at least had its own login.

With a local fallback, the worst case is one extra password manager lookup. I lose some elegance; I gain a way back into every service even when the IdP is dark.

The exceptions: BookStack's `AUTH_METHOD=oidc` configuration hides the form field entirely (the workaround is `AUTH_AUTO_INITIATE=false`, which at least stops the auto-redirect so I can recover via the DB), and a couple of mobile apps don't fall back gracefully to local login once OIDC is configured. Both are tolerable; neither overrides the rule.

## Decision 3: Network-Aware Two-Factor

This is the part of the setup I'm most pleased with.

I want a passkey on my account. I do not want to touch the passkey every time I open a tab from the couch. Those two preferences are in tension only because most IdPs treat 2FA as a binary global setting: either everyone needs it always, or nobody needs it ever.

Authelia treats 2FA as a per-rule, per-network setting. A short definition of which IP ranges are "trusted":

```yaml
definitions:
  network:
    internal:
      - 192.168.1.0/24   # home LAN
      - 10.42.42.0/24    # wireguard
```

And then a policy that branches on whether the request came from one of them. For the forward-auth path:

```yaml
access_control:
  default_policy: deny
  rules:
    - domain: 'auth.desktop.madhur.co.in'
      policy: bypass
    - domain: '*.desktop.madhur.co.in'
      policy: one_factor
      networks: ['internal']
    - domain: '*.desktop.madhur.co.in'
      policy: two_factor
```

And the same idea for the OIDC clients, expressed as a named policy each client references:

```yaml
identity_providers:
  oidc:
    authorization_policies:
      internal_bypass:
        default_policy: 'two_factor'
        rules:
          - policy: 'one_factor'
            networks: ['internal']
```

The effect: when I open a service from the LAN or over WireGuard, I get a password prompt and nothing else. When I open it from a coffee shop, from mobile data, or from anywhere else, I get the password prompt and a "sign in with your passkey" button. Same login URL, same cookie, different requirements depending on where I am.

This works because Authelia trusts `X-Forwarded-For` from Traefik, which is the only thing that ever talks to it. The "real" client IP propagates correctly, and the network-match happens before any policy check.

The design lesson behind it: **2FA should follow risk, not be a constant tax.** A password on the LAN is roughly the same security as a password-plus-biometric on the LAN — the attacker who's already inside my house has bigger options than guessing my Bookstack password. A password on a public Wi-Fi network is much weaker than the same password backed by a hardware-bound passkey. Putting both factors behind the same policy treats those two situations as if they were equally risky. They aren't.

## Decision 4: Twenty-Four Hour Sessions, Everywhere

The natural next thought after the network-aware policy: can I tie session *expiration* to network too? A one-week session at home, a one-day session on the internet. Same shape as the 2FA rule, just for cookies.

Authelia doesn't support that. Session lifetime is per cookie-domain, and there's only one cookie domain. I poked at it for a while and concluded it's not worth the complexity — the workaround would be running every service on two hostnames with two different cookie scopes, which is a lot of plumbing for a marginal gain.

So the lifetime is global. The question becomes: which value should it have?

The tradeoff:

- Long session (one week, three-month remember-me): convenient on the LAN. If the cookie is ever stolen, the attacker has a week to use it.
- Short session (a day): re-auth daily everywhere. A stolen cookie is good for at most 24 hours.

I picked 24 hours. The reasoning: the network-aware 2FA rule already does the "make stolen-from-internet sessions hard to use" job — to create the cookie from outside the LAN you needed the password *and* a passkey. So a stolen LAN session would have to be exfiltrated from inside the LAN, where I'm not the threat model. And the LAN re-auth cost is "type your password once a day," which is well below my friction tolerance.

Configuration is three lines:

```yaml
session:
  cookies:
    - domain: 'desktop.madhur.co.in'
      inactivity: '4 hours'
      expiration: '24 hours'
      remember_me: '24 hours'
```

If I'd cared more about LAN convenience, the path forward would be two cookie domains (`*.desktop.madhur.co.in` and `*.ext.madhur.co.in` say) with different lifetimes, each app routed to both. That's a much bigger commitment for a small comfort gain. Not now.

## Decision 5: Secrets Live in `.env`, Not in Compose

Every OIDC client has a secret. I had a choice about where to put it.

**Option A: Inline in `docker-compose.yml`.**

```yaml
environment:
  - OIDC_CLIENT_SECRET=z5Ck8khuFF5kLGLTBrUvNHS7comZ8J7tALzvrQExwgEOxRcF
```

Simple. Self-contained. And committable straight to git, where anyone with read access to the repo (now or via future leaks) gets every client secret in plaintext.

**Option B: A separate `.env` file per service, referenced via substitution.**

```yaml
# docker-compose.yml (committed)
environment:
  - OIDC_CLIENT_SECRET=${OIDC_CLIENT_SECRET}
```

```bash
# .env (gitignored)
OIDC_CLIENT_SECRET=z5Ck8khuFF5kLGLTBrUvNHS7comZ8J7tALzvrQExwgEOxRcF
```

The compose file in git has no secret at all — just the *shape* of the configuration, with placeholders. The `.env` sits next to the compose file, holds the actual value, and is gitignored at the repo root. `docker compose` resolves the substitution at deploy time.

I went with option B for every new client secret. The argument isn't subtle: **secrets that don't need to be in version control shouldn't be.** Even on a private repo, you reduce the blast radius of every accident — a misplaced clone, a forwarded gist, a screen share — by keeping the secret material out of the file that's tracked.

A side benefit is that the diff for "I rotated the secret" is now a single-line edit to a gitignored file, with no commit at all. The compose shape stays stable, the runtime value floats.

The same pattern applies in reverse for Authelia: secrets live in `authelia/secrets/oidc_<name>_client_secret` (gitignored), and only the PBKDF2 hash of the secret is stored in `authelia/config/configuration.yml`. The hash is fine to commit — it's a one-way function. The plaintext shouldn't be anywhere git can see.

## Where This Leaves Things

Fifteen apps with native SSO, two factors of authentication that only show up when the request comes from outside my home, daily session lifetimes, and a tracked-vs-untracked split that keeps client secrets out of the repo.

The most surprising thing I noticed afterwards: none of this feels like extra work to use. The LAN experience is "type password, you're in everywhere." The internet experience is "type password, touch passkey, you're in everywhere." The mobile experience is the same as the internet experience because mobile is always over public networks. The auth is now the same shape as the rest of the stack — declarative, in git, versioned, recoverable.

A few rules of thumb I'd carry forward:

1. **Default to native OIDC for identity-aware apps; forward-auth for the rest.** Don't try to make every app speak OIDC if it doesn't natively care who's logged in.
2. **Always keep a local-login fallback** when the app lets you. Single-IdP setups are fragile; the fallback costs nothing until the day the IdP is dark.
3. **Make 2FA conditional on network, not global.** Constant taxes train users to ignore them; conditional ones get attention when they matter.
4. **Tighten session lifetimes before adding architectural complexity.** A 24-hour cookie is one line and solves most of the "session stolen" risk. Multi-domain cookies are weeks of work for a marginal gain.
5. **Secrets in `.env`, hashes in committed config.** The repo is the audit log of *what's deployed*, not *the credentials*. Keep those two things separate.

The next round of work is Nextcloud, Jellyfin, and Home Assistant — three plugin-based SSO integrations that I deferred. Different shape entirely; probably a different post.
