---
slug: "asusrouter-exporter"
title: >-
  asusrouter-exporter: Prometheus Metrics for an Asuswrt-Merlin Router, No Cloud
  API Required
date: '2027-12-01'
year: '2027'
month: '2027-12'
description: >-
  There's no official Prometheus exporter for Asuswrt-Merlin, so I SSH in and
  read /proc myself. TDD against real router fixtures, counter-reset handling
  for reboots, and — since the connected-client data is genuinely mine — a
  git-filter-repo pass to scrub household devices out of the history before
  open-sourcing it.
tags:
  - Prometheus
  - Grafana
  - Python
  - Networking
  - Self-Hosting
  - Open Source
draft: false
params:
  disqus_id: /2027/12/01/asusrouter-exporter/
---

*This article was written with the assistance of AI.*

---

My homelab dashboard tracks CPU, memory, and traffic for every box I run — except the one piece of hardware everything else's traffic passes through. My Asus router (Asuswrt-Merlin firmware) has no Prometheus exporter, no metrics endpoint, nothing. Just a web admin UI that's fine for a glance and useless for a graph.

There's no vendor API to poll here. Merlin doesn't ship one, and I didn't want to depend on a cloud service just to find out how loaded my own router's CPU is. So the exporter SSHes into the router and reads the same files the admin UI itself reads: `/proc/stat`, `/proc/meminfo`, `/proc/loadavg`, `/sys/class/net/*/statistics/*`, `nvram`, `ip neigh`, `wl assoclist`.

## Architecture

Nothing exotic — a single-process SSH-polling exporter, no new moving parts as it grew:

```
exporter/
├── parsers.py        # pure functions: raw command output -> Python values
├── router_client.py  # RouterClient: SSH commands -> parsers -> typed results
├── metrics.py         # prometheus_client Counter/Gauge definitions
└── poller.py          # Poller: RouterClient -> metrics, on a timer
```

`parsers.py` has no SSH or network code in it at all — every function takes a raw string and returns a Python value:

```python
def parse_cpu_line(raw):
    parts = raw.strip().splitlines()[0].split()
    values = [int(x) for x in parts[1:1 + len(_CPU_MODES)]]
    return dict(zip(_CPU_MODES, values))

def parse_loadavg(raw):
    parts = raw.strip().split()
    return float(parts[0]), float(parts[1]), float(parts[2])
```

`RouterClient` wires those parsers to actual commands over the SSH transport:

```python
def get_cpu_jiffies(self):
    return parse_cpu_line(self._run("head -1 /proc/stat"))

def get_interface_bytes(self, ifname):
    raw = self._run(
        f"cat /sys/class/net/{ifname}/statistics/rx_bytes "
        f"/sys/class/net/{ifname}/statistics/tx_bytes"
    )
    return parse_interface_bytes(raw)
```

`Poller` runs on a timer, calls `RouterClient`, and turns the results into Prometheus series. `asusrouter_up` has one job: if anything in a poll cycle throws, the whole cycle is marked down. No partial-success bookkeeping — a half-updated set of metrics is worse than an honest "the poll failed."

## Test-Driven Against Real Fixtures

Every parser was written test-first, against real output captured from the router — not guessed formats. Before writing a line of `parse_meminfo`, I SSHed in and saved the actual `/proc/meminfo` output to a fixture file, then wrote the test against that:

```python
def test_parse_cpu_line_extracts_jiffies_by_mode():
    result = parse_cpu_line(CPU_STAT_RAW)  # real /proc/stat capture
    assert result == {
        "user": 4347089, "nice": 0, "system": 17885235,
        "idle": 505191377, "iowait": 582662, "irq": 0, "softirq": 14279440,
    }
```

This caught a real gotcha early: the CPU-jiffies-to-seconds conversion factor is hardcoded to 100 (`USER_HZ`), because `getconf` isn't available on this router's BusyBox — there's no way to query the actual kernel tick rate at runtime. `/proc/stat` values are USER_HZ by long-standing kernel ABI convention regardless of the real timer frequency, so hardcoding 100 is the correct move here, not a shortcut.

## Counter Resets on Reboot

Byte counters and CPU jiffies both come from the kernel and both reset to zero on a router reboot. Prometheus counters must never go backwards, so every delta calculation treats a decrease as an implicit reset rather than a negative increment:

```python
@staticmethod
def _apply_counter_delta(counter, last_value, new_value):
    if last_value is None:
        delta = new_value
    else:
        delta = new_value - last_value
        if delta < 0:
            delta = new_value  # counter reset (reboot) -- treat as delta from zero
    counter.inc(delta)
    return new_value
```

Same function, reused for interface byte counters, aggregate CPU seconds, and per-core CPU seconds — one reset-safe primitive instead of three copies of the same bug waiting to happen.

## Identifying Connected Clients

The one part of this exporter that's genuinely fiddly: figuring out *who* is on the network well enough to label a metric with a human-readable name. No single router command has the full picture, so `get_connected_clients` merges four sources:

- `nvram get custom_clientlist` — names the user manually assigned in the admin UI (highest priority)
- `dnsmasq.leases` — DHCP hostnames and IPs
- `wl -i <iface> assoclist` per wifi band — which MACs are associated to 2.4GHz/5GHz/6GHz
- `ip neigh` — the ARP/NDP table, filtered to exclude `FAILED`/`INCOMPLETE` entries, used to catch wired clients that don't show up in any wireless assoclist

A MAC found in a wifi band's assoclist is labeled with that band; anything left over that has a live neighbor-table entry and a matching DHCP lease is labeled `wired`. Name resolution falls back in priority order: custom nvram name, then DHCP lease hostname, then the bare MAC if neither exists.

## Metrics

| Metric | Type | Labels | Description |
|---|---|---|---|
| `asusrouter_up` | gauge | | 1 if the last poll succeeded |
| `asusrouter_interface_rx_bytes_total` / `_tx_bytes_total` | counter | `interface` (`wan`/`lan`/`wifi_2g`/`wifi_5g`) | Bytes per interface |
| `asusrouter_cpu_seconds_total` | counter | `mode` | Aggregate CPU time |
| `asusrouter_cpu_core_seconds_total` | counter | `core`, `mode` | Per-core CPU time |
| `asusrouter_load1` / `_load5` / `_load15` | gauge | | Load average |
| `asusrouter_memory_bytes` | gauge | `type` (`total`/`free`/`buffers`/`cached`/`available`) | Memory usage |
| `asusrouter_client_connected` | gauge | `mac`, `name`, `ip`, `connection` | 1 per currently connected device |

Metric names deliberately mirror node_exporter's convention (`_cpu_seconds_total{mode}`, `load1`/`load5`/`load15`) — other tooling and dashboards already assume that shape, no reason to invent a new one.

One PromQL gotcha from wiring up the CPU-busy panel: `sum(rate(asusrouter_cpu_seconds_total[5m]))` looks right but silently drops the `instance`/`job` labels, which breaks the vector match against the `mode="idle"` side of the ratio. The fix is `sum without(mode) (...)` instead of a bare `sum(...)` — it collapses only the `mode` label and keeps everything else the match needs:

```
100 * (1 - (rate(asusrouter_cpu_seconds_total{mode="idle"}[5m])
  / ignoring(mode) sum without(mode) (rate(asusrouter_cpu_seconds_total[5m]))))
```

## Dashboard

The repo ships a ready-to-provision Grafana dashboard covering all of the above:

<img src="/images/Blog/asusrouter-dashboard-wan-overview.png" alt="WAN transfer rate and summary stats" style="max-width: 100%; height: auto;" />
<img src="/images/Blog/asusrouter-dashboard-cpu-load.png" alt="CPU usage and load average" style="max-width: 100%; height: auto;" />
<img src="/images/Blog/asusrouter-dashboard-memory-throughput.png" alt="Memory usage and per-interface throughput" style="max-width: 100%; height: auto;" />
<img src="/images/Blog/asusrouter-dashboard-cpu-percore.png" alt="Per-core CPU usage" style="max-width: 100%; height: auto;" />

It also has a connected-client-count panel, a connected-devices table, and a per-device connect/disconnect timeline — not pictured here, since those panels show my own devices' names, MACs, and IPs.

## Scrubbing the History Before Publishing

That last sentence is the reason this section exists. `asusrouter_client_connected` is, by design, exactly the kind of metric that's useful to *me* and radioactive to publish carelessly: real household device MACs and hostnames (phones, laptops, a couple of IoT devices) had ended up committed across test fixtures and docs from earlier development — the same real router data I'd used to TDD the parsers against, mentioned above.

Squashing the history to one commit would have hidden the leak but also thrown away the exact granular, commit-by-commit TDD story I wanted the public repo to show. So instead:

1. Cloned the repo into an isolated scratch location.
2. Built a longest-first, literal old→new replacement map — real MACs to fabricated locally-administered ones (`02:aa:aa:aa:aa:01`, …), real hostnames to generic stand-ins — and ran it through `git-filter-repo --replace-text` across the full history.
3. Dumped every blob in the rewritten history (`git rev-list --objects --all` piped through `git cat-file --batch`) and every commit message, and grepped both for every real value. Twice — once right after the rewrite, once again against a fresh clone of the pushed GitHub remote, since a filter that looks clean in the working clone but wasn't actually verified against everything that got pushed is not verified at all.
4. Kept the LAN IPs as-is — they're plain RFC1918 private addresses, not identifying on their own.

29 commits survived with their original messages and structure intact, and all 32 tests still pass post-scrub, because the fixture data and its test assertions were replaced by the same literal mapping.

## Source Code

The full source, including the Grafana dashboard JSON, is at [github.com/madhur/asusrouter-exporter](https://github.com/madhur/asusrouter-exporter). The project was built end-to-end using [Claude Code](https://claude.ai/claude-code).
