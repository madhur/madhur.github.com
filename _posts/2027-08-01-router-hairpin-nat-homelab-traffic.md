---
layout: blog-post
title: "Hairpin NAT, Split-Horizon DNS, and Where I Landed Between Them"
excerpt: "Tracing 8 MB of unexplained traffic between my PC and my router led me through hairpin NAT, split-horizon DNS, and a hybrid homelab setup that avoids both."
disqus_id: /2027/08/01/router-hairpin-nat-homelab-traffic/
tags:
    - Homelab
    - Networking
    - NAT
    - DNS
    - Traefik
    - Prometheus
    - Jellyfin
    - Self-Hosted
---

*This article was written with the assistance of AI.*

---

It started as a casual question: *what is actually leaving my PC right now?* I have a homelab with around 50 containers, two reverse proxies, half a dozen monitoring agents, and torrents seeding in the background. I had no idea, in any precise sense, who my machine was talking to.

A 30-second packet capture answered the surface question quickly. qBittorrent dominated the bandwidth, Anthropic's API got a couple of hundred kilobytes from the Claude CLI I had open, and there was a steady trickle to my self-hosted ntfy and Prometheus services. Nothing surprising — except for one entry that didn't fit:

```
192.168.1.1 (my router) → 7.88 MB in 30 seconds
```

Eight megabytes between my PC and my router, in half a minute. The router isn't supposed to be a heavy traffic source. DNS queries don't add up to 8 MB.

This article walks through what it turned out to be and the small homelab change I made because of it.

## What I Saw on the Wire

The connection that accounted for almost all of that traffic was a single, long-lived TCP session:

```
192.168.1.1.37594 → 192.168.1.82.443  (3,649 packets, 30 seconds)
```

So the router had opened a connection *to my PC's port 443*. My PC was the server in this conversation, and Traefik holds port 443. The router was acting as a client of my own reverse proxy.

I used `tshark` to read the **Server Name Indication** (SNI) field — the unencrypted hostname inside the TLS ClientHello that tells the server which certificate to present. Over a 60-second capture, the SNI showed an exact 15-second cadence on one hostname:

```
22:15:46  cadvisor.desktop.madhur.co.in
22:16:01  cadvisor.desktop.madhur.co.in
22:16:16  cadvisor.desktop.madhur.co.in
22:16:31  cadvisor.desktop.madhur.co.in
```

A 15-second interval is the default Prometheus scrape interval. cAdvisor is Google's container metrics agent, normally scraped by Prometheus to track per-container CPU and memory.

The odd part: my Prometheus runs on this same machine. cAdvisor runs on this same machine. They're both on the host. Why was the scrape leaving my PC, going to the router, and coming back?

## What Is Hairpin NAT?

When a packet leaves your computer for a public IP address, it goes to your router (because the router is the only thing that can reach the public internet). Normally the router rewrites the packet to make it look like it came from the router's public IP, sends it out to the internet, and rewrites the response on the way back. That's plain old NAT.

**Hairpin NAT** (also called *NAT loopback* or *NAT reflection*) is what happens when the destination IP in your packet is *your own router's public IP*. The router realizes the packet wants to come right back to your home network. Instead of bouncing it out to the internet for nothing, it rewrites the destination to the matching internal IP and forwards the packet straight back.

To make the response work, most consumer routers also rewrite the *source* IP — replacing it with the router's own LAN IP. This is so the response goes back through the router (which holds the NAT state), instead of taking a shortcut directly between two LAN devices and breaking the connection.

The end result, from the perspective of the destination machine, is that all hairpinned traffic appears to come from `192.168.1.1` (your router's LAN IP), regardless of which device on the LAN actually sent it.

That fits what I was seeing. My Prometheus was scraping `https://cadvisor.desktop.madhur.co.in/metrics`. That hostname is a public DNS A record pointing at my home's public IP. The scrape went out, hit the router, the router did NAT loopback, and the packet came back to the same PC. From the PC's view, the traffic was "with the router" because the router had rewritten the source.

This was happening every 15 seconds. Each cAdvisor scrape returns a couple of hundred MB of metrics text uncompressed (or about 4 MB compressed over HTTP/2). Multiplied across the day, this is gigabytes of traffic going out of my NIC, into the router, and right back in — to talk to a container two hops away in the same machine.

## Why It's Worse Than It Looks

The pure bandwidth waste is the small problem. The bigger problems are:

1. **Router CPU**. Consumer routers have weak CPUs. Hairpinning every packet means every byte goes through the router's NAT engine twice (once outbound, once on the loopback). With 50 services and constant scrapes, that's a meaningful load.
2. **TLS termination overhead**. The traffic was HTTPS, so Traefik had to negotiate TLS, decrypt, route, re-fetch from cAdvisor over plain HTTP, encrypt the response. All for traffic that never actually leaves the machine.
3. **Authelia in the path**. My public services sit behind Authelia for authentication. The cAdvisor route bypassed it via a ClientIP rule, but the *check* still happened.
4. **It hides the real source**. When everything looks like "traffic with 192.168.1.1," I lose visibility into what's actually happening. I had no idea this was Prometheus until I read the SNI.

## The Same Pattern in Other Places

Once I understood the cause, I checked the other services.

### Jellyfin

I have Jellyfin behind Traefik at `jf.desktop.madhur.co.in`. When my Fire TV plays a movie, it resolves that hostname to my public IP, sends the stream request out, and the router hairpins it back. The entire Jellyfin stream — gigabytes per movie — goes from Fire TV to router to PC, when the LAN path is Fire TV directly to PC.

When I look at network monitoring on the PC, I see traffic flowing to `192.168.1.1`, not to the Fire TV — same source-rewrite effect.

### My Existing `*.local.*` Pattern

I already had Traefik routes for things like `grafana.local.madhur.co.in` and `proxmox.local.madhur.co.in`. They were defined in a file provider, served on plain HTTP (port 80, no TLS), with priority over a catch-all redirect. The DNS for `*.local.madhur.co.in` already pointed at `192.168.1.82` (my PC's LAN IP) instead of the public IP.

Crucially, when I send a packet from my PC to my own LAN IP, Linux is smart enough to route it via the loopback interface — it never touches the physical NIC, never reaches the router. I confirmed it:

```
$ ip route get 192.168.1.82
local 192.168.1.82 dev lo src 192.168.1.82
```

The `dev lo` confirms it: traffic to your own LAN IP is handled inside the kernel, with no router involved.

So I had two patterns living side-by-side:

- **`*.desktop.madhur.co.in`** → public IP → hairpin NAT through router → Traefik over HTTPS → Authelia
- **`*.local.madhur.co.in`** → my LAN IP → kernel loopback → Traefik over HTTP → no auth

The second pattern was strictly better for things accessed only from my LAN. cAdvisor and Jellyfin should have been on it. They weren't.

## The First Fix: New Routes, No Restart

The Traefik file provider has a `watch: true` flag. Drop a new YAML block in the dynamic directory, and Traefik picks it up without a restart. Two new entries in `local-services.yml`:

```yaml
http:
  routers:
    cadvisor-local:
      rule: "Host(`cadvisor.local.madhur.co.in`)"
      service: cadvisor-local
      entryPoints:
        - web
      priority: 100

    jellyfin-local-http:
      rule: "Host(`jf.local.madhur.co.in`)"
      service: jellyfin-local-http
      entryPoints:
        - web
      priority: 100

  services:
    cadvisor-local:
      loadBalancer:
        servers:
          - url: "http://cadvisor:8080"

    jellyfin-local-http:
      loadBalancer:
        servers:
          - url: "http://jellyfin:8096"
        passHostHeader: true
```

Two notes on this:

- The service URLs use the **container names** (`cadvisor`, `jellyfin`) instead of IPs. Traefik shares the `proxy-network` Docker network with those containers, so Docker's embedded DNS resolves the names. Container IPs change between restarts; names don't.
- `passHostHeader: true` matters for Jellyfin because it builds absolute URLs based on the incoming Host header. Without it the web UI would point at `cadvisor` or whatever and break.

Then I changed Prometheus's cAdvisor target from the public hostname to the local one and reloaded:

```diff
   - job_name: cadvisor
     static_configs:
     - targets:
-      - cadvisor.desktop.madhur.co.in
+      - cadvisor.local.madhur.co.in
```

```
$ curl -X POST http://localhost:9093/-/reload
```

Within 15 seconds the next scrape happened over the new route. I ran the SNI watch again, and the cAdvisor handshakes from `192.168.1.1` were gone. Eight megabytes per 30 seconds of router traffic gone.

For Jellyfin, I changed the server URL in the Fire TV's Jellyfin app to `http://jf.local.madhur.co.in`. Same effect: the stream now flows directly Fire TV ↔ PC over the LAN, with no router hairpin.

## Should Every Service Get Two URLs?

I have around 50 services, and many of them I also access from outside (Authelia gates the public side). The obvious next thought was: give every service two URLs — `bookstack.desktop.madhur.co.in` for outside, `bookstack.local.madhur.co.in` for home — and use the right one depending on where I am.

There are real downsides to that:

- **Mobile apps store one server URL**. Paperless mobile, NTFY, Immich, Bitwarden, Home Assistant. If I configure the LAN URL, the app breaks the moment I leave Wi-Fi. If I configure the public URL, I'm back to hairpin at home.
- **Authelia sessions don't carry across hostnames**. A login on `bookstack.desktop.*` is not a login on `bookstack.local.*`. Cookies are domain-scoped.
- **Bookmarks and shared links rot**. An old `desktop.*` bookmark used at home will hairpin. And if I'm sending someone a Bookstack link, I have to remember which URL to send.

The cleaner answer for services I bookmark or use across networks is **one URL that resolves to the right address depending on where I am**. That's split-horizon DNS.

## What Is Split-Horizon DNS?

Split-horizon DNS (sometimes called *split-brain DNS*) is when a single hostname resolves to *different IPs depending on who is asking*.

The way it usually works at home: you run a local DNS resolver inside your LAN. When devices on the LAN ask it to resolve `bookstack.desktop.madhur.co.in`, the resolver overrides the public answer and returns the LAN IP `192.168.1.82`. When devices outside your LAN ask public DNS for the same hostname, they get the public IP and reach you over the internet through the router.

The same hostname, the same bookmark, the same mobile app config — different network paths depending on context. The TLS cert keeps working in both directions because it's the same hostname. Authelia keeps working because it's the same hostname. Nothing on the client needs reconfiguring.

The standard implementations are AdGuard Home, Pi-hole, dnsmasq, or Unbound. All open source, and adding a wildcard rewrite is a one-liner in any of them.

## Why I Didn't Do Split-Horizon DNS

Split-horizon needs an always-on resolver, and nothing in my house is always on.

I have power cuts. I shut down my PC overnight to save electricity. My Proxmox node draws power that adds up over a month. I'm not running a Raspberry Pi 24/7 just to serve DNS, and I'm not running a VPS for it either — at that point I'd be paying real money to fix a problem the public internet already solves.

The "two DNS servers, primary local + fallback to Cloudflare" idea doesn't help much. DNS clients try the primary first and retry on failure with a multi-second timeout, often caching the failure. The secondary doesn't have the overrides anyway, so while the primary is down, lookups slow down and the overrides stop working.

Hosting the resolver on the router itself works if you run Asuswrt-Merlin (which exposes full dnsmasq), but on stock Asuswrt the local DNS feature isn't flexible enough for wildcard rewrites. I haven't flashed Merlin.

So split-horizon DNS is a good fit on paper but requires hardware I'm not going to keep powered.

## The Decision: A Hybrid

What I settled on:

**For services where hairpin overhead actually matters** — constant traffic or heavy streaming — use `*.local.*` on plain HTTP, file-provider routes, no auth (LAN is the trust boundary):

- cAdvisor (Prometheus scraping every 15s)
- Jellyfin (movie streaming to Fire TV)
- Anything else metrics-heavy or stream-heavy

**For everything else** — Bookstack, Paperless, NTFY, the dozens of light dashboards — keep the existing `*.desktop.*` URLs and accept the hairpin. The router handles it transparently. For a Bookstack page or a few notification pushes, the bandwidth and CPU cost is negligible. The benefit of one URL per service is worth more than the small amount of router work.

**For dev-tool services I never access from outside** — Grafana, Proxmox, Alertmanager, ActivityWatch, Watchyourlan — I keep the existing `*.local.*` routes I'd already set up. They're internal by design.

The split is by traffic profile, not by visibility. Heavy traffic gets the optimal path; light traffic gets the convenient path.

## A Tailscale Footnote

One option I considered and may come back to: **Tailscale**. It's a peer-to-peer mesh VPN with MagicDNS, free for personal use. With Tailscale on every device, traffic between two devices on the same LAN goes direct over the LAN (no relay overhead). When outside, traffic flows over the Tailscale tunnel. The hostname (`bookstack.your-tailnet.ts.net`) resolves the same way at home and away.

Tailscale does not require always-on home infrastructure — the coordination plane is hosted by Tailscale, my devices just need the client. The friction is the client-side install on every device, and it doesn't help when sharing a link with someone outside my tailnet.

For now the hybrid is enough. If hairpin starts becoming a real annoyance, Tailscale is the path I'd take before running a 24/7 DNS box.

## Takeaways

The simple lesson is: don't route traffic through the router when it's between two endpoints on the same machine. I'd built a consistent `*.desktop.*` reverse-proxy setup and used it everywhere, including for connections that didn't need to leave the kernel. When everything goes through the same path, it's worth occasionally checking whether the path is appropriate for what's flowing through it.

The deeper one is that homelab patterns have a cost. Putting every service behind a single reverse proxy with TLS and SSO is conceptually clean, but it forces traffic through layers that don't apply when both ends are localhost. The fix isn't to abandon the pattern — it's to keep a second pattern for cases where the first one produces strictly worse outcomes.

A couple of hours of investigation, four lines of YAML, and the unexplained 8 MB every 30 seconds is gone.
