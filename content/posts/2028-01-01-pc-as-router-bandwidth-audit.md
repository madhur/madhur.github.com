---
title: >-
  Turning My Homelab PC Into the House Router for a Day, Just to Find One
  Bandwidth Hog
date: '2028-01-01'
description: >-
  My ISP router has no per-device stats, and I don't want to root or replace it.
  So for one day I made my Arch homelab box the LAN's DHCP server and NAT
  gateway, hairpinning every device's traffic back out through the same router —
  no rewiring, fully scripted, fully reversible. Then I kept a piece of it: a
  journald-backed flow logger, a hairpin-aware dedupe, and a push-alerting
  big-flows report that outlived the audit.
tags:
  - Homelab
  - Networking
  - Linux
  - nftables
  - Shell
  - Python
  - Systemd
  - Self-Hosted
draft: false
params:
  disqus_id: /2028/01/01/pc-as-router-bandwidth-audit/
---

*This article was written with the assistance of AI.*

---

I'd been seeing high data usage on the household internet connection for a few days and had no way to find out why. My ISP router is a stock Asus RT-AC68U with an RT-AX53U as a mesh node — no Merlin firmware, no SSH, no per-client traffic breakdown. The admin UI shows one number: total bytes since last reboot. Not per device, not per site, nothing I could act on.

The honest options were: buy a managed switch with port mirroring, flash Merlin onto a router I wasn't sure would survive it, or drop a Pi with a traffic-shaping build in the middle of the LAN. All of that is either money or risk on a network my whole household depends on.

What I actually have is an always-on Arch Linux box already wired into the router — the homelab server running about 70 containers behind Traefik. It has a NIC, a kernel, and root access I already trust. For one day, could it just *become* the router?

## The Constraint That Shaped Everything

I didn't want to bypass the real router. It does the actual PPPoE/DHCP handoff to the ISP, and I wasn't going to re-wire the house or put my homelab box in the physical path between the modem and everything else. The PC stays exactly where it is today: one Ethernet cable into the same router port it's always used.

So the design isn't "replace the router." It's a **one-armed NAT hairpin**:

1. The PC becomes the LAN's DHCP + DNS server. Every device gets the PC's IP as its gateway instead of the router's.
2. Traffic from LAN devices arrives at the PC on `enp5s0`.
3. The PC re-writes the source IP (`MASQUERADE`) and sends it right back out — on the *same* `enp5s0`, to the *same* router, which still does the real NAT to the internet.
4. Return traffic retraces the same path back through the PC to the device.

Every packet enters and leaves on one interface. Nothing physically changes. The router never knows the PC isn't just another chatty LAN client with an unusually large MASQUERADE pool.

## The dnsmasq Side

`dnsmasq` replaces the router's DHCP server for the day and hands the PC out as gateway and DNS:

```conf
interface=enp5s0
bind-dynamic
listen-address=192.168.1.82

no-resolv
server=192.168.1.1

dhcp-range=192.168.1.100,192.168.1.250,12h
dhcp-authoritative
dhcp-option=option:router,192.168.1.82
dhcp-option=option:dns-server,192.168.1.82
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

log-queries
log-dhcp
log-facility=/var/log/dnsmasq-router-hairpin.log
```

Two lines here earned their comments the hard way:

- **`bind-dynamic` instead of `bind-interfaces`.** dnsmasq starting at boot races NetworkManager applying the PC's static IP. `bind-interfaces` demands the listen address exist immediately or dnsmasq dies; `bind-dynamic` lets it start on the wildcard address and pick up `192.168.1.82` once it lands, so it survives the boot-time ordering instead of burning through systemd's restart limit.
- **`dhcp-authoritative`.** Without it, a phone waking from sleep with a lease from the *old* router-issued DHCP pool sends a `DHCPREQUEST` for an address outside my new range, and stock dnsmasq just ignores it rather than NAK-ing it — the device silently keeps the router as its gateway and never shows up in the audit. This flag is only safe because, for the day, this PC really is the LAN's sole DHCP server.

`log-queries` and `log-dhcp` are what give me the per-device, per-site breakdown later — every hostname every device resolves, timestamped, in one log file.

## The nftables Side

A single isolated table does the forward-and-masquerade:

```nft
add table inet router_hairpin
flush table inet router_hairpin

table inet router_hairpin {
    chain forward {
        type filter hook forward priority filter; policy accept;
        iifname "enp5s0" oifname "enp5s0" ip saddr 192.168.1.0/24 counter accept comment "LAN hairpin forward"
    }

    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        iifname "enp5s0" oifname "enp5s0" ip saddr 192.168.1.0/24 counter masquerade comment "NAT hairpin back to router"
    }
}
```

`add table` + `flush table` as top-level statements (not nested inside the `table { }` block — I got that wrong on the first pass and `nft -c` caught it before it ever touched the kernel) makes the file idempotent: re-running it never duplicates rules, it just redeclares the same state. `counter` on both rules gives an objective yes/no during validation — `nft list table inet router_hairpin` either shows packets accumulating or it doesn't.

This table lives in its own namespace, deliberately separate from the `ip filter`/`ip nat` tables Docker and fail2ban already manage on this box. `flush table` only ever touches rules inside `inet router_hairpin` — it can't reach into Docker's tables even by accident.

## The Bug That Actually Cost Time: Docker's FORWARD Policy

The nftables table above looked complete and passed every syntax check. Deployed, it did nothing — devices got a DHCP lease, could resolve DNS, and then every actual connection just hung.

The cause: this box runs Docker, and Docker manages its own `iptables` `FORWARD` chain with `policy drop`, evaluated at the same netfilter forward hook as my `inet router_hairpin` table. Netfilter runs *every* base chain registered at a hook — my chain accepting a packet doesn't override Docker's chain, sitting right next to it, dropping the same packet. Two independent chains, same hook, and the drop wins.

Docker's own documented fix for exactly this is `DOCKER-USER` — a chain Docker creates, jumps to first from `FORWARD`, and never flushes on restart:

```bash
iptables -I DOCKER-USER -i enp5s0 -o enp5s0 -s 192.168.1.0/24 -j ACCEPT
```

That fixed outbound. Devices could reach the internet — for exactly one request. Replies never came back. I'd fixed the direction LAN clients send *to* the internet and missed the direction the internet replies *back*. The fix isn't the mirror image of the first rule with `-s` swapped for `-d` on all traffic — that would also accept unsolicited inbound connections into the LAN. It has to be scoped to established traffic only:

```bash
iptables -I DOCKER-USER -i enp5s0 -o enp5s0 -d 192.168.1.0/24 \
  -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```

Both rules are idempotent via `iptables -C` checks before inserting, and `rollback.sh` removes exactly these two and nothing else Docker owns. This was the only part of the whole setup that touched Docker-managed firewall state, and it's the part I was most careful to make surgical and reversible.

## Two Sysctl Gotchas

Same-interface hairpinning trips two kernel defaults that are normally fine and actively wrong here:

```conf
# ICMP redirects: kernel default sends one after routing decisions like this,
# telling the client "talk directly to the real gateway next time" — the
# client silently bypasses the PC after the first packet and drops out of
# the traffic accounting.
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.enp5s0.send_redirects = 0

# Strict reverse-path filtering drops hairpinned return traffic outright,
# since the packet's in-interface and out-interface are identical.
net.ipv4.conf.enp5s0.rp_filter = 2
```

The `send_redirects` one needed all three scopes because the kernel's effective value is `all OR interface` — zeroing only `enp5s0` while `conf.all` stays `1` still sends redirects. `rp_filter`'s effective value is the opposite shape, `max(all, interface)`, so setting the interface alone to `2` (loose) is sufficient regardless of what `conf.all` is.

## Reading the Numbers Correctly

Because every packet crosses `enp5s0` twice — once from the LAN device, once back out to the router — `vnstat` and ntopng's interface totals read roughly double actual household usage. That inflation is uniform across all traffic, so *rankings* (which device, which site) stay valid; only the absolute totals need halving. This PC's own Docker/Traefik traffic rides the same interface too, so it shows up as one of the top consumers by design, not as something to chase down.

For the dashboard I used `ntopng`, bound to the same interface:

```bash
systemctl enable --now ntopng@enp5s0.service
```

Arch's ntopng package ships a templated unit (`ntopng@.service`, `%I` for the interface) rather than a bare one — worth checking before assuming the unit name from another distro's docs.

## Making It Reversible

Every deploy step has an exact inverse in `rollback.sh`, run in reverse order, each one gated on a state file captured once per cycle so re-running never drifts from a stale baseline:

```bash
main() {
  deploy_static_ip
  deploy_dnsmasq
  deploy_nft
  deploy_docker_allow
  deploy_boot_persistence
  deploy_sysctl
  deploy_ntopng
}
```

```bash
main() {
  rollback_ntopng
  rollback_boot_persistence
  rollback_docker_allow
  rollback_nft
  rollback_sysctl
  rollback_dnsmasq
  rollback_static_ip
}
```

Rollback also guards against stranding my own network: since the PC is the LAN's only DHCP server for the day, reverting its own static IP back to DHCP *before* the router's DHCP server is back on would leave it with nothing to renew from. So rollback opens with a prompt:

```
Has the router's DHCP server been re-enabled? Rolling back before that
strands this box's own network. [y/N]
```

(`--yes` skips it for non-interactive runs.) `ip_forward` is the one setting deliberately *not* reverted — Docker needs it on permanently for its own bridge networking, and it was already `1` on this box before any of this existed. Everything else — the nft table, the two DOCKER-USER rules, the sysctl values, the static IP, dnsmasq's config — gets restored to exactly what it was.

Since the nft table and the DOCKER-USER rules both live only in kernel memory, a reboot mid-audit would silently drop them and strand the whole house with no obvious cause. A small oneshot systemd unit reapplies both on every boot by sourcing the same `deploy_nft`/`deploy_docker_allow` functions rather than duplicating the logic:

```ini
[Unit]
After=network-online.target docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash @REPO_ROOT@/scripts/reload-hairpin.sh
```

## What It Actually Gave Me

Once devices picked up the PC as gateway, ntopng's Hosts view gave exactly the breakdown the router never could: per-device totals, and per device, which application or protocol accounted for it. Cross-referencing that against the SNI hostnames in the dnsmasq query log turned "one aggregate byte counter for the whole house" into "this phone, this app, this many bytes, over this window" — the kind of drill-down the stock router's single admin-page number was never going to offer, no matter how long I stared at it.

## Extra Credit: bigflows, Live Alerts, and a Desktop Widget

ntopng's live dashboard answers "what's happening right now," but it isn't scriptable and it can't tap me on the shoulder. Once the hairpin proved itself on audit day, I kept it running and built a small toolkit on top of it — `bigflows` — for history I could query and alerts I didn't have to go looking for.

**Getting flow data out of ntopng without touching its UI.** ntopng can emit every completed flow — source/destination, byte counts, nDPI-detected app protocol, TLS SNI — as one JSON line per flow, over syslog. A systemd drop-in redirects that into its own journald namespace instead of the noisy system journal:

```ini
# /etc/systemd/system/ntopng@.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/ntopng -i %I -l 1 -F syslog
LogNamespace=ntopng-flows
```

`LogNamespace` matters here beyond tidiness: journald gives each namespace its own file with its own ACL, and the default on a namespaced journal directory is `group:wheel:r-x` — so anything in `wheel` reads it without `sudo`:

```bash
$ journalctl --namespace=ntopng-flows -n 1 -o cat
{"IPV4_SRC_ADDR": "192.168.1.129", "SRC_NAME": "phone-2",
 "IPV4_DST_ADDR": "49.207.249.29", "TLS_SERVER_NAME": "immich.desktop.madhur.co.in",
 "L7_PROTO_NAME": "TLS", "IN_BYTES": 231481, "OUT_BYTES": 5210, "FIRST_SWITCHED": 1786421...}
```

**The hairpin's second-order bug: every flow logged twice.** ntopng captures promiscuously on `enp5s0`, and this box's own hairpin sends every forwarded packet back out that same interface — so ntopng sees each LAN-to-internet conversation twice: once under the real device's IP, once again under the router's own IP after `MASQUERADE`. Same bytes, same timing, different source. Left alone, every report and every alert double-counts. `bigflows` collapses these by grouping on everything that should be identical between the two legs, and within a group that contains one of this box's own IPs, keeping the non-self entry:

```python
def dedupe_hairpin_flows(rows, self_ips):
    groups, order = {}, []
    for r in rows:
        key = (r.get("IPV4_DST_ADDR"), r.get("L4_DST_PORT"), r.get("L7_PROTO_NAME"),
               r.get("IN_BYTES"), r.get("OUT_BYTES"),
               r.get("FIRST_SWITCHED"), r.get("LAST_SWITCHED"))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(r)

    out = []
    for key in order:
        members = groups[key]
        non_self = [r for r in members if r.get("IPV4_SRC_ADDR") not in self_ips]
        if non_self and len(non_self) < len(members):
            out.append(non_self[0])   # real device gets the credit
        else:
            out.append(members[0])    # identical either way — keep one
    return out
```

I only trust this merge when a self-IP is actually present in the group — checked against a live sample where roughly 96% of same-content duplicate groups had exactly that shape. Groups of identical-content flows *without* a self IP (two devices broadcasting near-identical discovery packets in the same instant, say) are left alone rather than guessed at.

**Three small pieces sit on top of the same journal:**

- `bigflows` — a CLI that filters the journal by size, host, or SNI substring, and can render an HTML report: an inline-SVG hourly bar chart plus a sortable table, no external JS or CDN dependency.
- `ntopng-flow-report.timer` — a user-level systemd timer that regenerates that HTML every 5 minutes; a plain `python -m http.server` serves it on the LAN.
- `ntopng-flow-watch` — tails the journal live and pushes an `ntfy` push notification the moment a single flow crosses a byte threshold, with recurrence tracking: the same source→destination pair repeating inside a sliding window gets flagged explicitly ("4th time in 47 min, every ~15 min") and escalates to `urgent` priority — the signal that actually distinguishes a stuck retry loop from a one-off big download.

<img src="/images/Blog/bigflows-report.jpg" alt="bigflows HTML report: an hourly bar chart of big-flow traffic over the last 24 hours, plus a sortable table of individual large flows with source, destination, protocol, and duration" style="max-width: 100%; height: auto;" />

Device names in that screenshot are relabeled before publishing, for the same reason `asusrouter-exporter`'s git history got scrubbed of real MACs before it went public: real household device names are useful to me and not something to publish by accident.

Both the report pipeline and the alert watcher run as user-level systemd units (`Restart=always`, `WantedBy=default.target`) rather than system units — neither needs root, and both should come and go independently of anything else on the box.

## Where It Stands Now

The whole hairpin setup ran for a day, wired into the same router port it started on, and came back down to exactly the state it was in that morning via `rollback.sh`. `bigflows` and its two systemd units, though, outlived the audit — they didn't depend on the hairpin at all, only on ntopng already watching the interface, so I left them running as a permanent, queryable, alerting layer on top of a dashboard that used to only answer "what's happening right now."
