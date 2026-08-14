---
title: >-
  Instrumenting My Homelab: One Shared Client Library, Source-Attributed
  Prometheus Metrics
date: '2027-11-01'
description: >-
  Scattered API calls — Firefly, ntfy, Bedrock, Gmail, Google Drive — collapsed
  into one instrumented Python library that fires fire-and-forget statsd packets
  at a bridge Prometheus scrapes. The payoff is a dashboard that answers 'which
  script made this Bedrock call, and what is it costing me?' — plus the
  counter-birth gotcha that makes rate() lie about batch jobs.
tags:
  - Prometheus
  - Grafana
  - Observability
  - Bedrock
  - Python
  - statsd
  - Self-Hosted
  - Automation
draft: false
params:
  disqus_id: /2027/11/01/instrumenting-homelab-shared-client-prometheus/
---

*This article was written with the assistance of AI.*

---

A few months ago I [wired three feeds into Firefly III](/blog/2027/10/01/auto-categorized-transactions-firefly-n8n-bedrock.html) and let a two-tier categorizer label every transaction. It works. But it also quietly makes a steady trickle of AWS Bedrock calls, and one month the bill made me ask a question I couldn't answer: *which of my scripts is actually calling Bedrock, and for what?*

The categorizer calls it. The statement reconciler calls it. So does an unrelated script that vision-extracts a location from a photo, and another that captions images, and a RAG toy I built for my blog. Each one had its own inline `boto3.client("bedrock-runtime")`, its own retry loop, its own idea of which region and model to use. There was no single place that knew "a Bedrock call just happened." The same was true of ntfy — when my phone buzzed, I couldn't tell whether it was the torrents script, the transaction uploader, or an ICICI screenshot job that sent it.

I had API calls to maybe ten homelab services scattered across two directories (`~/Desktop/python` and `~/scripts`), as Python clients, inline `requests`/`boto3`, and raw `curl` in shell. No single instrumented path meant no observability. This post is about fixing that: one shared client library that every script imports, where every outbound call emits a Prometheus metric tagged with **which script made it**.

## The shape of the problem

I wanted to answer three kinds of question from one Grafana dashboard:

1. **Throughput and latency per service** — how many Firefly writes, how slow is a Bedrock call, how often does Gmail IMAP hang.
2. **Attribution by source** — *which script* drove that traffic. A Bedrock panel split by source should show `transaction_categorizer` vs `image_location` as separate lines. An ntfy panel should show torrents vs uploader vs icici.
3. **Sub-granularity** — within a service, the dimension that matters: ntfy *topic*, Bedrock *model*, Gmail *account*, n8n *workflow*, weather *city*.

The constraint that shaped everything: most of these scripts are **short-lived cron/batch jobs**. They wake up, do their work in a few seconds, and exit. A normal Prometheus pull model never sees them — by the time the 15-second scrape comes around, the process is long gone.

## Why statsd_exporter and not Pushgateway

The standard answer for "metrics from a job that exits" is the [Pushgateway](https://github.com/prometheus/pushgateway). I went with [statsd_exporter](https://github.com/prometheus/statsd_exporter) instead, for two reasons.

First, **delivery must never slow down or break the job**. The whole point is observability *of* the pipeline, and observability that can take the pipeline down is worse than none. Pushgateway is an HTTP `POST` — synchronous, blocking, fails loud if the gateway is down. statsd is a UDP datagram: fire-and-forget. If the exporter is down, absent, or busy, the packet drops silently into the void and the job carries on, never the wiser.

Second, **cumulative counters survive across runs**. Pushgateway holds the *last pushed value* per job and is really designed for "this job ran and here's its final state." statsd_exporter accumulates — every `homelab_api_requests_total` increment adds up across every run of every script, which is exactly the monotonic counter Prometheus wants to scrape.

So the architecture is a little relay:

```
short-lived python/shell job
   └─(UDP :9125, fire-and-forget)→ statsd_exporter
                                      └─(HTTP :9102/metrics)→ Prometheus (scrape)
                                                                └→ Grafana
```

statsd_exporter is a single Go binary. It listens for statsd packets on UDP `9125`, maps them to Prometheus series, and exposes them on `9102` for the host Prometheus to scrape on its normal interval. The job's only cost is one `sendto()` syscall.

## The metrics core: a 40-line UDP emitter

The whole metrics layer is dependency-free — statsd is just text over UDP, so there's nothing to `pip install`. The emitter lazily binds a non-blocking socket and never raises:

```python
class _StatsdEmitter:
    """Minimal dogstatsd UDP sender. Lazily binds a socket; never raises."""

    def __init__(self):
        self._sock = None
        self._addr = (config.STATSD_HOST, config.STATSD_PORT)  # 127.0.0.1:9125

    def _socket(self):
        if self._sock is None:
            try:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._sock.setblocking(False)
            except Exception:
                self._sock = None
        return self._sock

    def send(self, line):
        if not config.metrics_enabled():        # HOMELAB_METRICS_DISABLED kill switch
            return
        sock = self._socket()
        if sock is None:
            return
        try:
            sock.sendto(line.encode("utf-8"), self._addr)
        except Exception:
            pass   # buffer full, network down, exporter absent — drop silently
```

The wire format is **dogstatsd** — statsd with tags — `name:value|type|#k1:v1,k2:v2`. statsd_exporter parses those tags into Prometheus labels out of the box:

```python
def emit_count(name, value=1, tags=None):
    _emitter.send(f"homelab_{name}:{value}|c{_format_tags(tags)}")

def emit_timing_seconds(name, seconds, tags=None):
    # statsd_exporter reads a `|ms` timer value as MILLISECONDS and divides by
    # 1000 to observe seconds into the histogram. So we send milliseconds here;
    # the histogram buckets in the mapping config are therefore in seconds.
    _emitter.send(f"homelab_{name}:{seconds * 1000:.3f}|ms{_format_tags(tags)}")
```

That comment cost me a confused half hour. I sent a 20 ms duration, the histogram `_sum` read `0.00002`, and nothing lined up. statsd_exporter treats a timer value as milliseconds and divides by 1000 before observing it. So you send `seconds * 1000`, and you define your buckets in seconds. The mapping config makes timers into native histograms:

```yaml
defaults:
  timer_type: histogram
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30, 60, 120, 300, 600]
  match_type: glob
```

The buckets run all the way out to 600 s because some of these "API calls" are a Bedrock vision extraction on a bank screenshot, which can take 30 s, and the occasional Selenium login that takes minutes.

## Every client wraps its calls in `track()`

On top of the emitter sits one context manager that times a block and emits both a request counter and a duration histogram, tagged `ok`/`error`:

```python
@contextmanager
def track(service, operation, *, source=None, **extra_tags):
    labels = config.base_labels(source)                  # source, host, config
    labels.update({"service": service, "operation": operation})
    labels.update(extra_tags)
    start = time.perf_counter()
    status = "ok"
    try:
        yield
    except BaseException:
        status = "error"
        raise                                            # never swallow the real error
    finally:
        elapsed = time.perf_counter() - start
        labels["status"] = status
        emit_count("api_requests_total", 1, labels)
        emit_timing_seconds("api_request_duration_seconds", elapsed, labels)
```

Every client in the library is the same shape — keep the public API the existing call sites already use, wrap the outbound call. The Firefly client:

```python
def _request(self, method, path, **kwargs):
    with metrics.track("firefly", _op_name(method, path)):   # e.g. "post_transactions"
        r = self._client.request(method, path, **kwargs)
        ...
```

LLM clients additionally record token usage, because for Bedrock that's the line item on the bill:

```python
def record_llm_tokens(service, model, operation, *, input_tokens=0,
                      output_tokens=0, status="ok", source=None):
    base = config.base_labels(source)
    base.update({"service": service, "model": model, "operation": operation})
    emit_count("llm_requests_total", 1, {**base, "status": status})
    if input_tokens:
        emit_count("llm_tokens_total", input_tokens, {**base, "direction": "input"})
    if output_tokens:
        emit_count("llm_tokens_total", output_tokens, {**base, "direction": "output"})
```

The Bedrock client reads the `usage` block out of the Converse response and feeds it straight in, so `homelab_llm_tokens_total{model, operation, direction}` becomes a per-model, per-purpose token ledger I can multiply by the published price to estimate spend.

## Attribution: the ambient `source` label

The hard part of attribution is that the calls live in **shared client modules** invoked by many entrypoints. The Firefly client can't know whether it was the categorizer or the reconciler that called it — that knowledge lives at the top of the call stack, in the script that ran.

I didn't want to thread a `source=` argument through every method of every client. So `source` is an **ambient** value set once per entrypoint and inherited by everything downstream, via `contextvars`:

```python
_current_source = ContextVar("homelab_source", default=None)

def set_source(name):
    """Declare which entrypoint is running. Call once at startup."""
    _current_source.set(_sanitize_label(name))

def get_source(explicit=None):
    if explicit:
        return _sanitize_label(explicit)                 # per-call override
    ambient = _current_source.get()
    if ambient:
        return ambient                                   # set_source(...)
    env = os.environ.get("HOMELAB_SOURCE")
    if env:
        return _sanitize_label(env)                      # shell-set
    argv0 = Path(sys.argv[0]).stem                       # fallback: script name
    return argv0 or "unknown"
```

Each entrypoint declares itself in one line:

```python
def main():
    set_source("transaction_categorizer")
    ...
```

and from that point on, *every* client call it makes — Bedrock, Firefly, ntfy — carries `source="transaction_categorizer"` with no per-call plumbing. Run the categorizer and the image-location script separately, and the `service="bedrock"` series splits cleanly into two sources. That single fact — which script — is the thing the whole exercise was for.

A second ambient, `config`, carries the per-mailbox context (my wife's transactions vs mine run the same code with a different config file), so household spend stays separable too.

## The sub-granularity labels

With source nailed down, the per-service labels were easy to add at each client's `track()` call:

- **ntfy → `topic`**: `track("ntfy", "publish", topic=self.topic)`. Now an ntfy panel splits by topic *and* source — I can see that `private` is driven by the photos script while `transactions` is the uploader.
- **Bedrock / Ollama → `model`**: the exact model ID, so a Sonnet call and a Haiku call are distinct cost lines.
- **Gmail → `account`**: the nice one. My IMAP client is a drop-in subclass of `imaplib.IMAP4_SSL`, and the account is simply the login user — captured once and stamped on every command, with zero changes at the call sites:

  ```python
  class InstrumentedIMAP4_SSL(imaplib.IMAP4_SSL):
      def login(self, user, password):
          self._account = user or ""
          with metrics.track("gmail", "login", account=self._account):
              return super().login(user, password)

      def select(self, mailbox="INBOX", readonly=False):
          with metrics.track("gmail", "select", account=self._account):
              return super().select(mailbox, readonly)
      # ...same for search / fetch / uid / store / copy / logout
  ```

- **n8n → `workflow`**, **weather → `city`**: same pattern, each a config-supplied or call-supplied label.

The discipline here is **low cardinality**. A handful of topics, models, accounts, workflows, cities — all bounded. The thing you must never do is put an unbounded value (a message ID, a filename, a per-email subject) in a label; that's how you blow up Prometheus. None of these do.

## The counter-birth gotcha that makes rate() lie

This one deserves its own section because it had me convinced the whole thing was broken.

I built the dashboard, ran a Bedrock job, and the "tokens per second" panel showed a flat zero. Latency: flat zero. I'd verified the packets were arriving — `curl localhost:9102/metrics` plainly showed `homelab_llm_tokens_total{...} 5449`. The raw counter was right. But `rate()` and `increase()` over it returned **0**.

The reason is fundamental to how Prometheus counters work, and it bites sporadic batch jobs specifically. `rate()`/`increase()` need to observe a *change* between two scrapes. A one-shot job that fires once a day creates a series that is **born at its value** — the first time Prometheus ever scrapes it, the counter already reads 5449. Prometheus never witnessed the `0 → 5449` transition (the process that did it had already exited), so as far as `increase()` is concerned, nothing changed. The next day's run adds a bit more, but between runs the series is flat, and over any window that doesn't contain two runs, the rate is zero.

For high-frequency services `rate()` is fine. For "runs once a day" batch counters it's structurally the wrong tool. The fix is to stop trying to rate them and lean on what *is* always populated:

- **The cumulative counter itself**, drawn as a step line — a *staircase* that climbs by one tread every time the job runs:

  ```promql
  sum by (source) (homelab_api_requests_total{service=~"$service"})
  ```

  Rendered with `stepAfter` interpolation, each run is a visible step up. Flat between runs is correct and expected, not a bug.

- **Average latency from the histogram sum/count**, which needs no rate at all:

  ```promql
  sum by (service,operation) (homelab_api_request_duration_seconds_sum)
  /
  sum by (service,operation) (homelab_api_request_duration_seconds_count)
  ```

- **p95 from `histogram_quantile` over the raw buckets** (again, no `rate()` wrapper):

  ```promql
  histogram_quantile(0.95,
    sum by (service,operation,le) (homelab_api_request_duration_seconds_bucket))
  ```

The dashboard ended up with a RED-ish attribution table — one row per `(service, source, operation, model, topic, ...)` with calls, errors, avg and p95 — that is *always* populated because it never rates anything, plus the staircase panels for the time-series view. The lesson: for an event that happens a few times a day, `rate()` is a trap; cumulative counters and quantiles-over-raw-buckets are the honest views.

## Instrumenting the shell fleet from one choke point

Plenty of my homelab runs as shell. The cron scripts (`every_hour.sh`, `every_24_hours.sh`, …) wrap every task in a single reusable bash function, `run_with_notification "<cmd>" "<description>" "<topic>"`, that already times the command, captures its exit code, and knows its ntfy topic. That function is the perfect place to instrument the *entire* cron fleet at once — including pure-shell jobs that have no Python at all:

```bash
# Inside run_with_notification, after the command runs:
if [ -x "$HOMELAB_METRIC" ]; then
    local __jstatus=ok; [ $exit_code -ne 0 ] && __jstatus=error
    local __jsource="${HOMELAB_SOURCE:-$(basename "${0%.sh}")}"   # e.g. every_24_hours
    "$HOMELAB_METRIC" api --service cron --operation "$description" \
        --source "$__jsource" --topic "$topic" \
        --status "$__jstatus" --duration "$duration" >/dev/null 2>&1 || true
fi
```

(`homelab-metric` is a tiny CLI that emits one statsd packet the same way the Python clients do.)

The question this raises — and which I had to think through carefully — is *double counting*. If the weather job emits a `service=cron` metric here, and the Python weather client inside it also emits `service=weather` metrics, am I counting the same work twice?

No — because a Prometheus series is keyed by its full label set, and `service="cron"` is a different label value from `service="weather"`. They're not duplicates; they're two **granularities** of one run. The `cron` series answers "did the job run, how long end-to-end, did it exit 0." The `weather` series answers "how many API calls did it make, how slow was each." You want both, and you never add them together. The only way to get a misleading number is to `sum` across services without a `by (service)` — which the dashboard never does. For the pure-shell jobs (a `pacman -Syu`, a `trash-empty`), the `cron` metric is the *only* visibility there is, which is the whole point.

## Consolidation: how many ways should you send a notification?

Once the library existed, the duplication it was meant to kill became obvious. ntfy was the worst offender — I found *five* places that sent notifications:

1. The Python client (`NtfyNotifier`) — the real implementation, with auth, encoding, attachments, **metrics**.
2. A `homelab-ntfy` CLI — a thin shell→client bridge.
3. A `send_ntfy.py` — an *older* shell→client bridge doing exactly what #2 does.
4. A cron wrapper using raw `curl`.
5. A screenshot script using raw `curl`, instrumented by nothing.

The instinct is to collapse all five into one. The better answer is to collapse to **three layers**, each of which is genuinely needed:

- **One implementation** — the Python client. Every Python caller imports it directly.
- **One CLI bridge** (`homelab-ntfy`) — because a bash script can't `import` a Python class; it can only run a command. The CLI is a ~40-line adapter that parses args and calls the client, so shell callers get the same behaviour *and the same metrics*. `send_ntfy.py` was a duplicate of this idea written before the CLI existed — so it got deleted and its one caller repointed.
- **Orchestration scripts** that *call* the CLI rather than re-implementing `curl`.

The interesting case is the one place I **kept** raw `curl`: the cron failure-alert wrapper. Its job is to tell me when jobs fail — *including* when the Python venv or the library itself is broken. If it sent alerts through `homelab-ntfy` (same venv), a broken venv would silence the very alert telling me it's broken. So the harness keeps `curl` (no dependency on the thing it monitors) and emits its metric best-effort with `|| true`. Don't wire the smoke detector through the thing it's watching.

## The bridge runs as a user systemd service

The exporter itself is a long-running daemon, so it's a systemd unit, not a cron job — it has to be up continuously to catch the UDP packets jobs fire the instant they run.

```ini
[Service]
Restart=on-failure
ExecStart=/home/me/statsd_exporter/statsd_exporter \
    --statsd.listen-udp=127.0.0.1:9125 \
    --web.listen-address=127.0.0.1:9102 \
    --statsd.mapping-config=/home/me/ops/statsd_mapping.yml
NoNewPrivileges=true
ProtectSystem=strict
```

It binds only loopback (the jobs are all local), needs no privileged ports, and writes nothing — so it has no business running as root. It runs as my own user. There's a neat consistency argument for going one step further and making it a *user* unit (`systemctl --user`): Prometheus and the cron timers that feed it are already user units, so the bridge is the lone piece of the pipeline sitting in the system manager. With user-lingering already enabled, a user unit survives logout and starts at boot just the same. It's a tidiness win rather than a functional one — the UDP packet doesn't care which manager owns the listener — but co-locating the whole metrics pipeline under one manager is the kind of thing future-me will thank present-me for.

## What it answers now

The original question — *which script is calling Bedrock, and what's it costing* — is now a dashboard variable away. The attribution table shows, for the trailing window:

```
service   source                   operation       model            calls  errors  avg s  p95 s
bedrock   transaction_categorizer  categorize      claude-sonnet-4   31     0       2.3    3.1
bedrock   image_location           image_location  claude-sonnet-4   12     0       12.8   29.0
bedrock   statement_reconciler     extract_stmt    claude-sonnet-4    4     0        8.1   11.2
gmail     gmail_reader_config      select          —                 11     0        0.9    1.4
ntfy      desitorrents             publish         —                  1     0        0.3    0.3
cron      every_24_hours           Weather Fetch   —                  1     0        0.1    0.1
```

I can finally see that the image-location script, not the categorizer, is the expensive Bedrock tenant — it sends whole screenshots, so its calls are 12 s and 29 s at p95 against the categorizer's 2 s. That's the line item I'd optimise first, and I only know because the call is attributed to the script that made it.

## Pieces

- **The `homelab` library** — one installable Python package, `pip install -e`'d into the venvs that need it. Instrumented clients for Firefly, ntfy, Mailpit, CalDAV, Paperless, n8n, Bedrock, Ollama, Gmail, BookStack, plus newer Weather (OpenWeatherMap) and Google Drive clients. Two console scripts, `homelab-ntfy` and `homelab-metric`, bridge shell into the same instrumented path.
- **statsd_exporter** — single Go binary, host systemd unit, UDP `:9125` in, `:9102/metrics` out, timers mapped to native histograms.
- **Prometheus + Grafana** — already running for the rest of the homelab; one scrape job and one dashboard added. The dashboard variables (`source`, `service`, `model`, `topic`, `account`, `workflow`, `city`) are all scoped to `label_values(homelab_api_requests_total, …)` so they never bleed into the node-exporter and cAdvisor series that reuse generic label names like `service` and `model`.
- **The `track()` / `set_source()` pattern** — the two-line contract every entrypoint and every client follows. Everything else is glue.

A few things I'd tell myself at the start. Reach for statsd-over-UDP from day one if your workload is batch jobs — the fire-and-forget property isn't a nice-to-have, it's the thing that lets you instrument freely without ever worrying that a metrics outage takes a pipeline down. Understand the counter-birth problem *before* you build the dashboard, or you'll waste an evening convinced your packets aren't arriving when they're arriving fine and `rate()` is just the wrong question. And put the `source` label in from the first client — retrofitting attribution is annoying; designing for "which script did this" from the start costs one `contextvar` and one line per entrypoint.

The library ended up around 1500 lines, most of it the clients themselves; the metrics core that started this whole thing is barely 200. The dashboard is the part I actually look at, and for the first time the answer to "what is my homelab doing right now, and which script is doing it" is a glance rather than a guess.
