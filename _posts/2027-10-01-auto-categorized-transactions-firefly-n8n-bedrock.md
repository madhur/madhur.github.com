---
layout: blog-post
title: "Auto-Categorized Transactions in Firefly III with n8n, Bedrock and ntfy"
excerpt: "Three feeds — email alerts, SMS backups and a realtime MacroDroid → n8n webhook — converge on the same Firefly III dashboard. A two-tier categorizer (regex + Claude on Bedrock) labels every row, cross-source dedup keeps the books clean, and the dashboard is fresh within seconds of every swipe."
disqus_id: /2027/10/01/auto-categorized-transactions-firefly-n8n-bedrock/
tags:
    - Firefly
    - n8n
    - Bedrock
    - Claude
    - ntfy
    - Python
    - Automation
    - Self-Hosted
---

*This article was written with the assistance of AI.*

---

I wanted one dashboard that answered "where did my money go this month?" without me having to import a CSV, tag anything, or remember which card was used at which merchant. The closest off-the-shelf product was Firefly III, but Firefly is a ledger — it does not know what an HDFC SMS looks like, it does not categorize on its own, and it certainly does not de-duplicate a row that arrived via SMS in the morning and showed up again on the credit-card statement four weeks later.

So I built the plumbing around it. Three feeds carry transactions into Firefly, a Python categorizer labels every row before insert, and a small dedup layer makes sure each real-world purchase shows up exactly once. The whole thing runs on my own box, talks to AWS Bedrock for the categorization fallback, and keeps the Firefly dashboard fresh within seconds of every swipe.

This is what the end result looks like — the Firefly dashboard after a few months of letting the pipeline run unattended (amounts blurred):

<img src="/images/Blog/firefly-dashboard.png" alt="Firefly III dashboard showing account history chart, top balance tiles, budgets and spending, and categories breakdown" style="max-width: 100%; height: auto;" />

This post walks through the design.

## The Three Feeds

I keep ending up with the same insight: no single feed is complete.

- **Email transaction alerts** are the most structured (the bank composes them) but they only cover instruments that send them. SBI does, ICICI does, HDFC mostly does. Some merchants and rails (FASTag tolls, NEFT credits) sometimes don't trigger an email at all.
- **The daily SMS backup** is the most complete — every SMS the banks send hits the phone — but it lags by up to a day, and SMS bodies are noisier than emails.
- **A realtime SMS webhook** keeps Firefly fresh within seconds, but it's fragile (relies on a third-party app on the device, the home network being up, the n8n container being up).

Together they form a belt-and-braces feed where the realtime webhook keeps the dashboard current throughout the day and the daily SMS batch is the eventually-consistent backstop. The email pipeline overlaps with both for the instruments that send alerts, which is useful because emails carry more context (merchant name spelt out, currency explicit, sometimes the UPI VPA).

The interesting engineering is what happens when all three see the same transaction.

### Feed 1: Gmail Transaction Alerts

Each bank's alert email follows a consistent template, so I have one regex parser per template. The config wires up which subject line and from-address goes to which parser, and how to route the resulting transaction by the card's last four digits:

```yaml
transaction_alerts:
  hdfc_credit_card:
    enabled: true
    parser: hdfc_credit
    subject_pattern: "A payment was made using your Credit Card"
    from_address: "alerts@hdfcbank.bank.in"
    account_routing:
      "1639": "<uuid-hdfc-diners>"
      "5877": "<uuid-hdfc-rupay>"
    sign: -1
    days_to_search: 7

  icici_credit_card:
    enabled: true
    parser: icici_credit
    subject_pattern: "Transaction alert for your ICICI Bank Credit Card"
    from_address: "credit_cards@icici.bank.in"
    account_routing:
      "2003": "<uuid-icici-amazon-pay>"
    sign: -1
    days_to_search: 7

  hdfc_savings_credit:
    enabled: true
    parser: hdfc_upi_credit
    subject_pattern: "View: Account update for your HDFC Bank A/c"
    from_address: "alerts@hdfcbank.bank.in"
    sign: 1                   # incoming money
    days_to_search: 7
```

The key idea is **account_routing by last-4**. HDFC sends the *same* subject line for every credit card I own; the parser yanks the last four digits out of the body, and the router picks the right Firefly account. That keeps the parser table flat — one entry per template, not per card.

A pickle-backed Gmail session walks the inbox since the last UID watermark, runs the parser, and stamps each match with a stable `imported_id` (which doubles as the Firefly `external_id` for dedup, more on that below). A systemd timer fires it every few hours.

### Feed 2: Daily SMS Backup via "SMS Backup & Restore"

The Android app [SMS Backup & Restore](https://www.synctech.com.au/sms-backup-restore/) emails me a single zipped XML attachment every night with the previous 24 hours of SMS plus call logs. The subject line is always literally "Sms backup".

My pipeline picks that up the next morning:

```yaml
sms_backup:
  enabled: true
  subject_pattern: "Sms backup"
  days_to_search: 7
  match_window_days: 1       # ±N days for cross-source dedup

  banks:
    hdfc:
      enabled: true
      parser: hdfc_sms
      sign: -1
      sender_substrings: ["HDFCBK", "HDFCBN"]
      account_routing:
        "9756": "<uuid-hdfc-savings>"
        "1639": "<uuid-hdfc-diners>"
        "5877": "<uuid-hdfc-rupay>"
      default_account_id: "<uuid-hdfc-savings>"

    icici:
      enabled: true
      parser: icici_sms
      sign: -1
      sender_substrings: ["ICICIT", "ICICIB"]
      account_routing:
        "2003": "<uuid-icici-amazon-pay>"
        "030":  "<uuid-icici-savings>"

    sbi:
      enabled: true
      parser: sbi_sms
      sign: -1
      sender_substrings: ["CBSSBI", "SBIUPI", "SBIPSG", "SBICRD"]
      account_routing:
        "0127": "<uuid-sbi-savings>"
        "5256": "<uuid-sbi-loan>"
```

The dispatcher is deliberately dumb: it looks at the sender header (e.g. `AD-HDFCBK-S`), picks a parser by substring, and runs it on the body. The parser itself is responsible for telling actual bank-transaction SMS apart from balance pings, OTPs and bill reminders — non-transactional SMS just return `None` and get dropped silently.

### Feed 3: Realtime SMS via MacroDroid → n8n → SSH

The third feed is where it gets fun. The daily SMS batch is a perfectly fine backstop, but it means the Firefly dashboard is up to a day stale at any given moment. If I open it in the evening to check whether we're tracking on the groceries budget, the morning's purchases aren't there yet. The realtime webhook closes that gap — a charge hits the phone, an SMS arrives, and Firefly has the row within a few seconds.

The flow:

```
MacroDroid (SMS received trigger)
   └─→ HTTPS POST to n8n webhook
         └─→ n8n "Respond" node returns 200 to MacroDroid
         └─→ n8n SSH node into the home box
               └─→ python sms_webhook_handler.py < stdin (JSON payload)
                     └─→ same parser / categorizer / Firefly writer
                         the daily batch uses
                     └─→ ntfy notification (incidental)
```

A couple of decisions worth flagging:

1. **MacroDroid forwards every SMS, the Python script decides what counts.** The realtime webhook does not pre-filter at the phone end. The same sender-substring → parser dispatch the daily batch uses runs here too; non-transactional SMS get dropped. That keeps the device-side macro tiny and the Python side authoritative.

2. **n8n is glue, not logic.** The n8n workflow has three nodes: webhook receiver, an immediate respond-200, and an SSH node that pipes the JSON payload into `sms_webhook_handler.py` over stdin. I deliberately don't do parsing in n8n. Everything that knows what an HDFC SMS looks like lives in the Python repo, where I can test it, version it, and reuse it from the daily batch.

3. **Fire-and-forget from MacroDroid's perspective.** n8n returns 200 before the SSH call completes. If the SSH call fails the daily batch will pick the SMS up next morning.

The Python handler itself is small because it reuses everything from the batch path:

```python
def main() -> int:
    payload = _read_payload()
    if payload is None:
        return 2

    address = (payload.get("address") or "").strip()
    body = payload.get("body") or ""
    epoch_ms = int(payload.get("date_ms") or
                   datetime.now(tz=timezone.utc).timestamp() * 1000)

    cfg = load_config("config.yaml")
    sms_cfg = cfg["sms_backup"]
    cat_cfg = cfg.get("categorization", {})

    # Same dispatch table the daily batch uses
    sender_map = _build_sender_map(sms_cfg["banks"])
    match = pick_bank(address, sender_map)
    if not match:
        return 0
    parser_name, bcfg = match

    parser_fn = SMS_PARSERS[parser_name]
    parsed = parser_fn(body, {"sms_date_iso": _epoch_ms_to_iso(epoch_ms),
                              "sign": bcfg.get("sign", -1)})
    if parsed is None:
        return 0   # OTP / balance ping / unknown format

    parsed.__dict__["_account_id"] = _resolve_account(bcfg, parsed.last4)
    parsed.imported_id = _stable_sms_id(parsed.__dict__["_account_id"],
                                        to_reconcile_payload(parsed))

    # Same categorizer the daily batch uses
    categorize([parsed], cat_cfg, no_llm=False)

    # Same Firefly writer the daily batch uses
    write_to_firefly([parsed], env=dict(os.environ), dry_run=False)

    # ntfy
    NtfyNotifier.for_channel(cfg, "transactions").send_success_notification(
        f"Spent Rs {abs(parsed.amount):,.2f} | {parsed.payee_name[:40]}",
        title="SMS realtime",
    )
    return 0
```

If I rename the daily batch's category map, the realtime handler picks the change up on the next SMS. No duplicated dispatch tables, no drifting parser logic.

## Categorization: Two Cheap Tiers, One Smart Tier

A transaction sitting in Firefly without a category is useless to me — the whole point is to slice the dashboard by category and see where the money is going. So the writer refuses to insert an uncategorized row at all; it errors instead. That forces every gap to surface as a log line rather than silently landing in a "Misc" bucket nobody looks at.

I run categorization in two tiers, in order. The first match wins.

### Tier 1: regex / substring map

99% of my transactions fit a small set of merchant patterns. They live in YAML and get compiled to regexes at startup:

```yaml
categorization:
  enabled: true
  use_llm_fallback: true
  bedrock_region: "ap-south-1"
  bedrock_model_id: "apac.anthropic.claude-3-7-sonnet-20250219-v1:0"

  category_map:
    # Transport
    "UBER|OLA\\b|RAPIDO": "<uuid-cabs>"
    "PETROL PUMP|HP PUMP|IOCL|BHARAT PETROL|INDIANOIL": "<uuid-fuel>"
    "FASTag|Toll Plaza|TOLLPLAZA|NHAI": "<uuid-fastag-tolls>"
    # Food
    "ZOMATO|SWIGGY|DOMINOS|SwiggyFood|SwiggyInstamart": "<uuid-food-delivery>"
    "STARBUCKS|BARBEQUE NATION|CCD|BURGER SINGH": "<uuid-dining>"
    # Groceries
    "MILKBASKET|BIGBASKET|BLINKIT|DUNZO|ZEPTO": "<uuid-groceries>"
    # Housing
    "BSES|TATA POWER|BESCOM|MSEB|TORRENT POWER": "<uuid-electricity>"
    "INDANE|HP GAS|BHARAT GAS": "<uuid-cooking-gas>"
    # Connectivity
    "ACT FIBER|JIO FIBER|JIOFIBER|AIRTEL FIBER": "<uuid-broadband>"
    "\\bAIRTEL\\b|\\bJIO\\b|\\bVI\\b|VODAFONE": "<uuid-mobile>"
    # Streaming / SaaS
    "NETFLIX|PRIME VIDEO|SPOTIFY|JioHotstar|SONYLIV": "<uuid-streaming>"
    "CURSOR|CLAUDE\\.AI|GITHUB|VERCEL|DIGITAL OCEAN": "<uuid-software-cloud>"
```

The implementation is the boring kind of code that's the same in every project that learns to like regex:

```python
def apply_keyword_map(txns, keyword_map):
    compiled = []
    for pattern, cat_id in keyword_map.items():
        if not cat_id:
            continue
        try:
            compiled.append((re.compile(pattern, re.IGNORECASE), pattern, cat_id))
        except re.error as e:
            logger.warning("Invalid regex %r in category_map: %s", pattern, e)

    n = 0
    for t in txns:
        if t.category:
            continue
        # Match only on merchant fields, NOT on `notes` — the notes field
        # carries the full bank-transmission string with UPI rail names and
        # holder names that produced false positives in earlier versions.
        haystack = f"{t.imported_payee} {t.payee_name}"
        for rx, pattern, cat_id in compiled:
            if rx.search(haystack):
                t.category = cat_id
                t.category_reason = f"tier1:{pattern}"
                n += 1
                break
    return n
```

The lesson encoded in that comment cost me an evening of head-scratching. Bank statement rows put a lot of junk in `notes` — UPI rail names, NEFT memo lines, and stray substrings from the payer's email memo that happened to contain words like "Amazon Prime" would match the `AMAZON` rule even though the actual payee was a person. Matching only on the merchant fields fixed it.

There's also a parallel `destination_routing` map that handles a special case: when the "merchant" is actually one of my own accounts (FASTag top-ups via PayZapp, credit-card bill payments). Those become Firefly `transfer` transactions between my own accounts rather than withdrawals to phantom expense accounts, which keeps the cashflow chart honest.

### Tier 2: Claude on Bedrock

Anything Tier 1 doesn't catch falls to the LLM. One batched Bedrock Converse call per script run, with the full list of valid categories included as a strict pick-from-this-list constraint.

```python
def classify_with_bedrock(uncategorized, grouped_categories,
                          model_id="apac.anthropic.claude-3-7-sonnet-20250219-v1:0",
                          region="ap-south-1",
                          batch_size=50,
                          sleep_between_batches=15.0):
    flat = _flatten_categories(grouped_categories)
    valid_ids = {c["id"] for c in flat if c.get("id")}

    client = boto3.client("bedrock-runtime", region_name=region)

    out = {}
    batches = [uncategorized[i:i + batch_size]
               for i in range(0, len(uncategorized), batch_size)]

    for idx, batch in enumerate(batches):
        prompt = _build_prompt(batch, flat)

        try:
            response = client.converse(
                modelId=model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": 4000, "temperature": 0.1},
            )
        except ClientError as e:
            if "ThrottlingException" in str(e):
                time.sleep(sleep_between_batches * 4)
                response = client.converse(...)   # one retry
            else:
                logger.error("Bedrock failed on batch %d/%d: %s",
                             idx + 1, len(batches), e)
                continue

        raw = response["output"]["message"]["content"][0]["text"]
        items = _parse_llm_response(raw)

        for item in items:
            cid = item.get("category_id")
            # Reject hallucinated UUIDs — the model picks from `flat` or nothing
            if cid and cid not in valid_ids:
                logger.warning("LLM returned unknown category_id %r — dropping", cid)
                cid = None
            out[item["id"]] = (cid, item.get("reason", "")[:160])

        if idx + 1 < len(batches):
            time.sleep(sleep_between_batches)

    return out
```

The prompt itself does three things that matter:

1. **Hands Claude the full list of valid category UUIDs**, generated from a snapshot file (`state/category_mapping_snapshot.yaml`) of the live taxonomy. The model picks an `id`, not a name — that closes the door on category-name typos creeping in.
2. **Tells Claude how to read the amount sign** — negative for expenses or outbound transfers, positive for income or inbound transfers — and gives it permission to use Transfer-group leaves in *both* directions even though `is_income=false` on those leaves.
3. **Rejects hallucinated UUIDs in code** even after the prompt instructions. If the model ever invents an `id`, the validator drops it and the row is logged as a Tier-2 failure rather than silently mis-categorized.

A single Bedrock call comfortably handles the ~50 unmapped transactions per month a healthy Tier-1 leaves over, with the batching loop sitting there as quota-headroom for the very occasional historical backfill.

## Firefly III as the Sink

Firefly is the persistence layer. The writer takes a list of categorized `ParsedTransaction`s and POSTs each one as a Firefly transaction. A few decisions are baked in:

- **Direction by amount sign.** Negative amount → `withdrawal` with the account as source and a `expense:<merchant>` account as destination. Positive → `deposit` from a `revenue:<merchant>` account. Both `ensure_expense` and `ensure_revenue` auto-create the counterparty account if it doesn't already exist, so merchants Firefly hasn't seen before just appear.
- **Transfers override the above.** If the categorizer stamped `_dest_firefly_account_id` (from `destination_routing`), the writer emits a `transfer` between two of my own accounts instead.
- **Owner tagging.** Each account belongs to a named person in the household; the writer stamps an `owner:<name>` tag on every transaction so Firefly's per-tag reports can split household spending across individuals.
- **No uncategorized rows.** As mentioned above, the writer hard-fails on a missing category. Bad fail-loud is better than silent fallback.

```python
if amount < 0:
    ttype = "withdrawal"
    src_id = ff_acct_id
    dst_id = ff.ensure_expense(payee_name)
else:
    ttype = "deposit"
    src_id = ff.ensure_revenue(payee_name)
    dst_id = ff_acct_id

dest_override = t.__dict__.get("_dest_firefly_account_id")
if dest_override:
    ttype = "transfer"
    if amount < 0:
        src_id = ff_acct_id
        dst_id = dest_override
    else:
        src_id = dest_override
        dst_id = ff_acct_id

group_id = ff.create_transaction(
    ttype=ttype,
    date=t.date,
    amount=abs(amount),
    source_id=src_id, destination_id=dst_id,
    description=getattr(t, "notes", None) or payee_name,
    category_id=cat_id,
    tags=[f"owner:{owner}"],
    notes=f"imported_id={imported_id}",
    external_id=imported_id,
)
```

The withdrawals list view in Firefly shows what these landed rows look like — a transaction per swipe, source account on the left, destination expense account in the middle, category on the right, and three pie charts up top breaking the period down by category, budget and counterparty:

<img src="/images/Blog/firefly-transactions.png" alt="Firefly III withdrawals page showing imported transactions with categories, source/destination accounts, and category/budget/destination pie charts" style="max-width: 100%; height: auto;" />

## Cross-Source Dedup: The Whole Point

This is the part the title hints at. A single coffee purchase produces three rows if I'm careless: an SMS hits the realtime webhook, the same SMS hits the daily batch the next morning, and the credit-card statement PDF four weeks later mentions it too.

Firefly has built-in `external_id` uniqueness, which gets me most of the way:

- The realtime webhook and the daily SMS batch produce **the same `imported_id`** for the same SMS, because the id is hashed off (account, date, amount, parsed payee, body) — a stable function of the SMS itself. Whichever feed wins the race POSTs first; the other one gets a 409 from Firefly and counts as `skipped`.

That handles SMS-vs-SMS. But the email alert for the same purchase produces a *different* `imported_id` (it hashes off the email UID + Gmail content), and the statement PDF produces another (it hashes the parsed PDF row). So `external_id` alone wouldn't catch SMS-vs-email or SMS-vs-statement collisions.

For those, the writer does a second-layer dedup: **same Firefly account, same signed amount, date within ±N days** (N = 1 by default). Before POSTing each row, it asks Firefly for that account's transactions in a window around the target date:

```python
# Pre-fetch one date-window slice per account so the per-txn match is in-memory
window_by_acct: dict[str, list[dict]] = {}
if not dry_run and match_window_days >= 0:
    dates_by_ff = defaultdict(list)
    for t in txns:
        ff_id = state["accounts"].get(t.__dict__.get("_account_id"))
        if ff_id and getattr(t, "date", None):
            dates_by_ff[ff_id].append(date.fromisoformat(t.date[:10]))
    for ff_id, dates in dates_by_ff.items():
        start = (min(dates) - timedelta(days=match_window_days)).isoformat()
        end   = (max(dates) + timedelta(days=match_window_days)).isoformat()
        window_by_acct[ff_id] = ff.list_account_transactions(ff_id, start, end)

# Then, per transaction:
consumed_groups = set()  # so two same-amount rows in one batch can't both
                         # match the same existing FF group

for t in txns:
    candidates = window_by_acct.get(ff_acct_id, [])
    target_d = date.fromisoformat(t.date[:10])
    target_amt = Decimal(str(t.amount)).quantize(Decimal("0.01"))

    best = None
    best_delta = None
    for c in candidates:
        if c["group_id"] in consumed_groups:
            continue
        cd = date.fromisoformat(c["date"][:10])
        if abs((cd - target_d).days) > match_window_days:
            continue
        if Decimal(str(c["amount"])).quantize(Decimal("0.01")) != target_amt:
            continue
        delta = abs((cd - target_d).days)
        if best_delta is None or delta < best_delta:
            best, best_delta = c, delta

    if best is not None:
        consumed_groups.add(best["group_id"])
        reconciled += 1
        logger.info("FF dedup: imported_id=%s matches existing group=%s — skipping POST",
                    imported_id, best["group_id"])
        continue
```

A few subtle things in that loop that matter:

- **`consumed_groups`** tracks the existing Firefly groups already claimed by an earlier row in the same batch. Without it, two distinct same-amount-same-day purchases would both match the same existing Firefly row and only one would land. Three identical Rs 200 cab rides on the same day would lose two.
- **Closest by date wins.** If multiple existing rows match the amount within the window, the one with the smallest date delta is chosen. Keeps the matches sensible when the window is wider than a day.
- **Comparison is quantized to two decimals.** Amount equality on `Decimal` without quantization fails on `200.00 != 200`.
- **`reconciled` is its own counter**, distinct from `added` and `skipped`. The script logs all three so I can tell at a glance whether a run filled in new history or just reconciled existing rows.

The match window is currently ±1 day, which is loose enough to catch settlement-date drift (an SMS arrives on the swipe date; the statement shows the *posted* date a day later) without being so wide that two distinct purchases collide.

## Statement PDF Reconciliation: Did We Catch Everything?

The three feeds get me near-complete coverage, but "near-complete" is the kind of statement that quietly accrues holes. An SMS doesn't arrive because the SIM was on roaming. The email alert silently changes its subject line and the parser stops matching. An ICICI FASTag toll uses a sender substring I never added. Whatever the cause, the result is the same: Firefly is missing transactions and I don't notice until the credit-card bill arrives.

So once a month, when each bank emails the statement PDF, I run a reconciliation pass that uses the statement as ground truth.

The script is **read-only** against Firefly. It does not write a single row. Its only job is to bucket every statement transaction into one of four outcomes and surface the interesting ones:

- **matched** — Firefly already has this transaction (no action)
- **statement_only** — on the PDF, missing from Firefly (= the SMS/email pipeline missed it)
- **firefly_only** — in Firefly for this period, not on the PDF (= a duplicate or a wrong-account row that needs deleting)
- **drift** — same payee, same date, but the amount disagrees by more than 1% (= parser bug)

### Step 1: extract rows from the PDF with Claude

Each statement template is wired to a `hint` that the PDF extractor passes through to Bedrock. The model is the same Claude 3.7 Sonnet I use for categorization, with a hint-specific prompt explaining the column layout of that particular bank's statement:

```yaml
statements:
  hdfc_diners:
    enabled: true
    hint: hdfc_diners                       # which prompt to use
    folder_pattern: "*HDFC Bank - Diners*"
    account_routing:
      "1639": "<uuid-hdfc-diners>"

  icici_amazon_pay:
    enabled: true
    hint: icici_amazon_pay
    folder_pattern: "*Amazon Pay ICICI*"
    account_routing:
      "2003": "<uuid-icici-amazon-pay>"

  sbi_e_account:
    enabled: true
    hint: sbi_e_account
    folder_pattern: "*E-account statement for your SBI*"

statements_root: "decrypted_statements"
```

`folder_pattern` is an `fnmatch` glob against the immediate parent folder name — which is just the email subject line, since the daily email-PDF extractor lands each statement in a per-subject directory. So the rule wiring is "if a PDF lives under a folder named like the statement email's subject, treat it with this hint."

Each hint maps to a bank-specific prompt with rules like:

```
- For HDFC Diners: `EMI` prefix means it is an EMI installment — still a debit.
- For SBI e-Account: one PDF holds multiple accounts (savings + loan); emit a
  separate section per `Savings Account` / `DL/TL ACCOUNT` block, each with
  its own last4.
- Credit column → +ve amount, Debit column → -ve.
```

The LLM returns a strict JSON array of `{date, amount, payee, last4}`. The last-4 routes the row to the correct Firefly account (same `account_routing` map style as the SMS pipeline).

### Step 2: bucket against Firefly

For each (account, period) pair, the auditor pulls every Firefly transaction in the statement window and runs a two-pass match.

**Pass 1 — exact-amount, same-sign, closest date within ±3 days.** Greedy 1:1: once a Firefly row is paired, it's removed from the candidate pool, so two same-amount-same-day statement rows can't both match the same existing Firefly row.

**Pass 2 — drift detection.** Anything left over from Pass 1 gets re-checked against the still-unmatched Firefly rows, this time using a token-overlap similarity on the payee names (with cities, country codes, legal suffixes and channel words like `UPI`, `NEFT`, `POS` stripped as noise). If the payees look similar and the dates are within ±1 day but the amounts differ by more than the drift threshold, that's a parser bug worth flagging:

```python
def classify(statement_rows, firefly_rows,
             *, match_window_days=3, drift_threshold_pct=1.0):

    # Firefly's synthetic types never correspond to real statement rows
    ff_relevant = [r for r in firefly_rows
                   if r.get("type") not in {"reconciliation", "opening balance",
                                            "liability credit"}]

    s_canon = [_coerce_statement(r) for r in statement_rows]
    f_canon = [_coerce_firefly(r) for r in ff_relevant]

    used_s, used_f = set(), set()
    matched, drift = [], []

    # Pass 1: exact-amount match within ±match_window_days, closest date wins
    for si, s in enumerate(s_canon):
        best_fi, best_dd = None, None
        for fi, f in enumerate(f_canon):
            if fi in used_f or (f.amount < 0) != (s.amount < 0):
                continue
            if abs(f.amount - s.amount) > Decimal("0.01"):
                continue
            dd = abs((f.date - s.date).days)
            if dd > match_window_days:
                continue
            if best_fi is None or dd < best_dd:
                best_fi, best_dd = fi, dd
        if best_fi is not None:
            used_s.add(si); used_f.add(best_fi)
            matched.append((s.raw, f_canon[best_fi].raw, best_dd))

    # Pass 2: drift — similar payee, ±1 day, amount differs > threshold
    for si, s in enumerate(s_canon):
        if si in used_s:
            continue
        best_fi, best_pct = None, None
        for fi, f in enumerate(f_canon):
            if fi in used_f or (f.amount < 0) != (s.amount < 0):
                continue
            if abs((f.date - s.date).days) > 1:
                continue
            if not _payee_similar(s.payee, f.payee):
                continue
            denom = max(abs(s.amount), abs(f.amount))
            diff_pct = float(abs(s.amount - f.amount) / denom * 100)
            if diff_pct < drift_threshold_pct:
                continue
            if best_fi is None or diff_pct < best_pct:
                best_fi, best_pct = fi, diff_pct
        if best_fi is not None:
            used_s.add(si); used_f.add(best_fi)
            drift.append((s.raw, f_canon[best_fi].raw, best_pct))

    return {
        "matched": matched,
        "drift": drift,
        "statement_only": [s_canon[si].raw for si in range(len(s_canon))
                           if si not in used_s],
        "firefly_only":   [f_canon[fi].raw for fi in range(len(f_canon))
                           if fi not in used_f],
    }
```

### What the output looks like

A typical month's audit log:

```
== HDFC Diners · …1639 · 2027-08-15 to 2027-09-14 ==
  matched=46  statement_only=2  firefly_only=0  drift=1

STATEMENT_ONLY (2):
  2027-08-22  -349.00  ICICI FASTAG TOLL HOSUR        # → add ICICI FASTag sender substring
  2027-09-03  -1299.0  AIRTEL DTH RECHARGE            # → add to category_map

DRIFT (1):
  stmt: 2027-08-30  -2189.00  STARBUCKS UB CITY
  ff:   2027-08-30  -2089.00  STARBUCKS UB CITY        # 4.6% off — investigate parser
```

The `statement_only` rows are the actionable ones. Each one is either:

- A sender substring I never added (action: add it to `sender_substrings` so future SMS get caught)
- A merchant the SMS parser silently dropped (action: read the SMS body, refine the regex)
- A transaction that genuinely arrived only via the statement (acceptable — but rare enough to be worth a manual insert)

`firefly_only` is the inverse signal: a Firefly row with no statement counterpart usually means I imported the same transaction under two different `imported_id`s and the dedup loop didn't catch it. Sometimes it's a refund the statement posted to a different period, in which case it'll match next month.

`drift` is almost always a parser bug — the SMS or email arrived with a "Rs. 100" foreign-exchange markup that the statement broke out separately, or a tip/cashback was charged later. Worth fixing at the parser level rather than re-categorizing.

The audit doesn't fix anything by itself. It tells me *where* the leaks are so I can patch the SMS/email pipeline rather than papering over the gaps with manual Firefly entries.

## ntfy Notifications

ntfy is the user-facing layer. Every script that touches money sends to it. I route by purpose, not by script, so the phone topics stay clean.

```yaml
ntfy_settings:
  enabled: true
  server_url: "https://ntfy.example.com"
  topic: "changes"               # default; channels below override
  app_name: "Email Reader"
  channels:
    transactions: "transactions" # Firefly transaction inserts
    backup: "backup"             # PDF landing, calendar uploads, etc.
```

Code-side, scripts ask for a channel by name and the notifier resolves it:

```python
notifier = NtfyNotifier.for_channel(cfg, "transactions")
notifier.send_success_notification(
    f"{verb} Rs {abs(amount):,.2f} | {payee[:40]} | {account_name}\n\n{table}",
    title="SMS realtime",
    markdown=True,
)
```

The table is a fenced markdown block (ntfy's web client only speaks CommonMark, no GFM tables), built from the Firefly write summary so I can see source / amount / account / category at a glance:

```text
| source  | amount      | account       | category          | description     |
| ------- | -----------:| ------------- | ----------------- | --------------- |
| sms-rt  |    -245.00  | HDFC Diners   | Transport: Cabs   | UBER INDIA      |
```

Subscribing the desktop to both topics gives me one notification stream for everything that runs, which is handy for spotting errors — but the realtime feed earns its keep by keeping Firefly current, not by the buzz it produces.

## What I Look At

The dashboard is just Firefly. With every transaction tagged with an `owner:` label, a real category, and an explicit source/destination account, Firefly's built-in reports do the rest: per-category spend over time, per-account cashflow, budget burndowns by category, year-over-year comparisons. I haven't had to write any reporting code.

The budgets page is the one I look at most. Per-category monthly budgets with bars that fill up as the month progresses — once the pipeline has been running for a few weeks, this becomes the answer to "are we tracking?" without me having to do anything:

<img src="/images/Blog/firefly-budgets.png" alt="Firefly III budgets page showing budgeted vs spent per category for the current month" style="max-width: 100%; height: auto;" />

The interesting numbers come from the categorizer logs. A healthy month looks like:

```
2027-09-30 — daily batch: parsed=187 tier1=174 tier2_llm=12 uncat=1
```

That one uncategorized row is the signal. It means there's either (a) a new merchant Tier-1 doesn't know yet, in which case I add a regex, or (b) a transaction the LLM legitimately couldn't pin down, in which case I either improve the prompt or accept that the LLM picked "low-confidence; closest match" and move on.

## Pieces

- **Firefly III** — `ghcr.io/firefly-iii/core`, behind Traefik and Authelia. The ledger, the dashboard, the source of truth.
- **n8n** — `n8nio/n8n`, also behind Authelia. Used as glue only: one webhook + one SSH node, no logic.
- **MacroDroid** on the phone — single macro: SMS-received trigger → HTTPS POST to the n8n webhook with `{address, body, date_ms}` JSON. Free version is fine for this.
- **SMS Backup & Restore** on the phone — scheduled daily email of the previous day's SMS + call logs as a zipped XML attachment.
- **AWS Bedrock** — Claude 3.7 Sonnet in `ap-south-1`, IAM user with the `bedrock:InvokeModel` policy and nothing else. No fine-tuning, no agents, just `Converse`.
- **ntfy** — `binwiederhier/ntfy`, behind Traefik. Reverse-proxied with a Cloudflare cert; the iOS app and a [systemd ntfy client]({% post_url 2027-03-01-ntfy-desktop-notifications-linux %}) on the laptop subscribe to the topics.
- **The Python repo** — three live entry-point scripts (`gmail_reader.py`, `sms_uploader_actual.py`, `sms_webhook_handler.py`) share a single `transaction_uploader_firefly.write_to_firefly`, a single `transaction_categorizer.categorize`, and a single set of SMS parsers. A fourth, `statement_uploader_actual.py`, is read-only and runs monthly to reconcile against the bank PDFs. Two systemd timers (one daily for the SMS batch, one hourly for the email alerts) and one always-on SSH listener on the home box.

A few things I'd do differently if I were starting over. I'd reach for `external_id` plus an amount-window dedup from day one — I tried to be clever with content hashes first, and it broke the moment an SMS spelled the same merchant slightly differently than the email did. I'd also start with the LLM tier in place from the first import; trying to land Tier-1 rules for every historical edge case was a worse use of time than just letting Claude pick the closest match and curating from there.

The whole pipeline ended up smaller than I expected — roughly 3000 lines of Python including the parsers, the Firefly client, the categorizer and the SMS uploader. The interesting code is in the dedup loop and the prompt; everything else is glue.

