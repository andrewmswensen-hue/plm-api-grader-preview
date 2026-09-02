#!/usr/bin/env python3
"""
Builds the results table, the category jump pills, and the per-company detail
modals on index.html (the v1 "spreadsheet" layout).

WHY THIS EXISTS
    The scores appear in two places: the table cells and the pop-open modal.
    Hand-editing both is how they drift apart. This file is the single source of
    truth: edit DATA below, run `python3 build-report-card.py`, and both are
    rewritten from the same numbers.

TO ADD A NEW GRADED COMPANY
    Find it in CATEGORIES (the name must match exactly), then add an entry to
    RESULTS keyed by that same name. Re-run this script. That is the whole job.

    Each RESULTS entry needs:
      score / grade   the published 0-100 number and its letter
      cats            five (points, max, plain-English note) tuples, in order
      strengths       short bullets, the good news
      watch           short bullets, the things that cost you work
      bottom          one paragraph, the verdict a PM should read
      meta            run date, methodology version, model, evidence tier

HOUSE RULE
    No em dashes or en dashes anywhere in the copy. Commas, parens, hyphens,
    or split the sentence instead.
"""

import json, re, pathlib

HERE = pathlib.Path(__file__).parent
PAGE = HERE / "index.html"

# The five scoring categories, in table-column order, with their v1.1 maxima.
CAT_LABELS = [
    ("Functional Coverage",  15),
    ("Design &amp; Reliability", 10),
    ("Access Control",        5),
    ("Docs &amp; AI-Ready",       5),
    ("Access &amp; Cost",        15),
]

# ---------------------------------------------------------------------------
# THE LIST. Slug, display heading, and the companies in it.
# Source: Andrew's "PM Software List for API Grader" sheet.
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("pm-software",  "PM Software",
        ["AppFolio", "Buildium", "Rentvine", "Propertyware", "Rent Manager"]),
    ("listings",     "Listings, Applications &amp; Tenant Screening",
        ["Boom", "ShowMojo", "Tenant Turner", "RentEngine", "Rently"]),
    ("workflow",     "Workflow &amp; CRM",
        ["LeadSimple", "Aptly", "Process Street"]),
    ("maintenance",  "Maintenance",
        ["Property Meld", "Vendoroo", "Mason", "Latchel", "Lula"]),
    ("banks",        "Banks",
        ["Column", "Enterprise Bank"]),
    ("accounting",   "Corporate Accounting",
        ["Xero", "QuickBooks Online"]),
    ("phone",        "Phone",
        ["RingCentral", "SimpleVOIP", "Zoom Phone", "OpenPhone", "JustCall"]),
]

# Platforms with no API to grade at all. The row says so across the score columns
# rather than showing dashes, which would imply "not graded yet".
NO_API = {"Enterprise Bank"}

# Short labels for the pills (the headings above are too long for a pill row).
PILL_LABELS = {
    "pm-software": "PM Software", "listings": "Listings &amp; Screening",
    "workflow": "Workflow &amp; CRM", "maintenance": "Maintenance",
    "banks": "Banks", "accounting": "Corp Accounting", "phone": "Phone",
}

# ---------------------------------------------------------------------------
# THE RESULTS. Only companies that have actually been graded appear here.
# ---------------------------------------------------------------------------
RESULTS = {

"AppFolio": {
  "score": 48, "grade": "F",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Fable 5",
           "tier": "Baseline verified", "raw": "24.17 / 50"},
  # The first F, and the largest vendor on the list, so the note has to be
  # scrupulous about what the score does and does not say. The report is explicit
  # that the grade reflects access and control, not engineering quality.
  "note": "Graded three independent times against the same frozen evidence, with "
          "unreconciled totals of 50, 45 and 48. 21 of the 27 checks were "
          "unanimous, and the published 48 is recomputed from the reconciled marks "
          "rather than averaged. Across every defensible reading of the remaining "
          "ambiguities the score stays between 45 and 56, so the letter grade is F "
          "under all of them. Worth being precise about what that means: this is "
          "not a verdict on engineering quality. On design and reliability alone "
          "AppFolio scores 7.9 out of 10, tied for the highest of any platform graded "
          "so far. The F comes from the other half of the question, which is what "
          "an operator is actually allowed to build.",
  "cats": [
    (5.6, 15, "You can read everything and be notified about nearly everything, and "
              "you can automate maintenance, billing, and application decisions. "
              "But the leasing money cycle stays in the AppFolio interface. There "
              "is no lease creation, no move-out, no payment posting, no voiding or "
              "reversing a ledger transaction, and no reconciliation through the "
              "API. Leases can only be updated on three fields."),
    (7.9, 10, "The strongest part of the card, and a well engineered API by any "
              "measure. Typed schemas, real idempotency keys with replay headers, "
              "exact rate-limit semantics, cryptographically signed webhooks across "
              "20 topics, documented conflict behaviour, and a public status page. "
              "The gaps are minor: error codes mirror the HTTP status rather than "
              "naming the cause, there is no ordering guarantee on lists, the "
              "request id is undocumented, and there is no webhook retry contract."),
    (1.9, 5, "One all-or-nothing production key per database. You can rotate it "
             "yourself, but you cannot mint a read-only key for a reporting tool, a "
             "scoped key for an AI agent, or a second key you can revoke "
             "independently. Which endpoints and even which fields your key can see "
             "is negotiated with AppFolio rather than set by you. And there is no "
             "sandbox, so you test against production with that one key."),
    (1.3, 5, "A human developer with your login gets excellent documentation: 162 "
             "operations, typed schemas, worked examples, and a monthly changelog. "
             "Your AI tools get almost nothing. There is no OpenAPI spec published "
             "anywhere, no SDK, no MCP server, and the reference is a "
             "JavaScript-rendered page that returns an empty shell to anything "
             "without a browser. It is also login-gated, so it is not public."),
    (7.5, 15, "The API is a premium plan feature. There is no API at all on Core, "
              "read-only on Plus, and read-write only on the top Max plan. Even "
              "once you are entitled, generating the credential is self-serve but "
              "usable access is not: endpoint and field permissions are agreed with "
              "AppFolio case by case, and webhooks and batching need a "
              "representative."),
  ],
  "strengths": [
    "Second-highest Design and Reliability score of any platform graded so far",
    "Real idempotency keys, with replay headers and documented error codes",
    "Signed webhooks across 20 topics, with a public key set",
    "A Reports API exposing trust account, deposit, ledger and 1099 data",
    "Changelog with 104 dated entries and a monthly cadence",
  ],
  "watch": [
    "No lease creation, move-out, payment posting, voids or reconciliation via API",
    "One all-powerful key per database, with no read-only or scoped option",
    "No operator sandbox, so you test against production",
    "No OpenAPI spec, no SDK, and docs an AI tool cannot retrieve",
    "Endpoint and field access is negotiated with AppFolio, not self-serve",
  ],
  "bottom": "AppFolio's Database API is a well engineered read-and-notify platform "
            "with a genuinely strong operational core. Every object your business "
            "runs on is readable with typed schemas, incremental sync is the "
            "documented design, webhooks are cryptographically signed, and "
            "idempotency and rate limits are properly specified. The score is "
            "dragged down by what an operator is allowed to build. The API is "
            "locked to premium plans, endpoint and field access is negotiated with "
            "AppFolio rather than self-serve, there is one all-powerful key per "
            "database with no sandbox, AI tooling gets no spec or retrievable docs, "
            "and the leasing money cycle is absent entirely. The F reflects this "
            "rubric's heavy weighting of access, control and workflow completeness, "
            "not engineering quality. Practical read: on the Max plan this is an "
            "excellent system of record to sync from and to automate maintenance, "
            "billing and application decisions against, and the Reports API pulls "
            "trust account and 1099 data programmatically. It is not a platform you "
            "can run your whole business through, because managing trust accounts, "
            "posting payments and reconciliation stay in the interface.",
},

"Buildium": {
  "score": 78, "grade": "C+",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "38.75 / 50"},
  # Re-graded 2026-09-01 as a clean-room run plus a 3-grader reconciliation.
  # Every category landed on the identical points as the 2026-08-27 run, and the
  # two checks that diverged resolved to the same marks, so the per-category
  # prose below still holds. What is new is the provenance and one real caveat.
  "note": "Re-graded on 2026-09-01 as a clean-room run, then checked by three "
          "independent graders against the same frozen evidence. 25 of the 27 "
          "checks were unanimous, and the published 78 is recomputed from the "
          "reconciled marks rather than averaged. One honest caveat, and it is the "
          "whole spread between the runs: it rests on a single check, core "
          "operational actions. Graded strictly from the frozen evidence packet as "
          "written, the reproducible result is 74 (C). Graded against Buildium's "
          "full first-party reference, which lists create and update operations "
          "for every core object, it is 78 (C+). The difference is how complete "
          "the evidence packet was, not Buildium's actual capability. The 3-run "
          "process earned its keep here: it also forced a correction on bulk "
          "export, from yes down to partial.",
  "cats": [
    (15, 15, "Reads and writes nearly everything the business runs on: properties, "
             "units, leases, tenants, ledgers, bank accounts, bills, tasks, and work "
             "orders. Nothing critical is missing, and 91 webhook event types push "
             "changes to you in near real time."),
    (7.5, 10, "Modern, well typed, paginated, versioned, and openly monitored. Four "
              "gaps need code on your side: error responses carry no stable machine "
              "code, there are no idempotency keys (so a retried payment can double "
              "post), there is no lock stopping two writes from overwriting each "
              "other, and the only per-request trace id is an AWS header rather than "
              "a Buildium one."),
    (5, 5, "A perfect score, matched only by RingCentral and Column. Issue a "
           "read-only key for a reporting agent, scope a key to just the data an app "
           "needs, make one key per integration, and rotate or delete any of them "
           "yourself. A real sandbox exists and its keys cannot touch production."),
    (3.75, 5, "A developer or an AI tool can build against Buildium without "
              "reverse-engineering it. The reference is public and complete, the "
              "OpenAPI file drives code generation, and the changelog was current to "
              "nine days before the run. The gap is AI-native docs: no llms.txt, so "
              "an agent has to consume the OpenAPI file itself."),
    (7.5, 15, "One real barrier, and it is cost. Key creation is fully self-serve "
              "with no sales call, but the API is exclusive to the Premium plan at "
              "$400 a month. On Essential ($62) or Growth ($192) you cannot use it "
              "at all."),
  ],
  "strengths": [
    "The most complete object coverage of any API graded so far",
    "A real sandbox, with keys that cannot reach production data",
    "Read-only and per-resource scoped keys, self-serve",
    "91 webhook event types across 32 entities",
    "Changelog running monthly since 2020",
  ],
  "watch": [
    "Premium plan only, $400/month, so most operators are locked out",
    "No idempotency keys, so a retried payment can post twice",
    "Error responses never populate a machine-readable code",
    "No optimistic concurrency, so two writers can silently overwrite",
  ],
  "bottom": "Buildium's Open API is one of the most complete property management "
            "APIs you can build on today. It is a modern, well typed, versioned REST "
            "API with clear docs, a downloadable OpenAPI file, a sandbox, safe "
            "read-only keys, and a public status page. Its weak spots are all in "
            "money-safe automation: guard against double-posting a retried payment "
            "yourself, because the API will not. The biggest practical barrier is "
            "cost rather than capability, since the API is Premium-plan only. "
            "Buildium is not a bank, and moving money still depends on its ePay "
            "add-on and the underlying banks.",
},

"Column": {
  "score": 86, "grade": "B",
  "meta": {"run": "Sep 2, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Fully verified, sandbox", "raw": "43.13 / 50"},
  # Column sponsors this page, so this note leads with the audit trail rather
  # than the score. The decisive fact is that reconciliation went AGAINST the
  # sponsor: both blind graders would have published an A and the run held a B.
  "note": "Column sponsors this report, so the scoring deserves scrutiny. Here is "
          "exactly what the three runs did. The first scored 85. Two independent "
          "graders then worked blind from the frozen evidence, with no sight of "
          "the first run's marks, and scored 95 and 92. The published 86 is the "
          "reconciled result, and on the one check worth eight points, commercial "
          "gating, the reconciliation went against Column: both blind graders "
          "marked it a pass, which would have published 94 and an A, and the run "
          "held it at partial because Column publishes no pricing at all and "
          "several API capabilities require contacting them to enable. That "
          "disagreement is unresolved and recorded rather than averaged away. A "
          "reader who takes gated to mean strictly a purchasable plan ladder "
          "should read this as an A. Every write in this run happened inside "
          "Column's sandbox on a test key, which is why it is graded Fully "
          "verified.",
  "cats": [
    (15, 15, "The strongest part of the API. Everything a business runs on "
             "financially is reachable in code, and you can act on it rather than "
             "just look at it: open accounts, move money five different ways, put "
             "a transfer on hold and then release or kill it, claw back an ACH, "
             "stop a check, and be told about all of it automatically. In the "
             "sandbox the grader opened an account, updated it, sent money, held "
             "and released a payment, held and cancelled another, and closed the "
             "account, all through the API."),
    (7.5, 10, "The parts that stop you losing money are genuinely strong. "
              "Retrying a payment cannot double-send it, proven live. Webhooks "
              "are signed and retried for three days, you can page through and "
              "bulk-export everything, and errors name the exact field you got "
              "wrong. The weak spots are the ones you hit at 2am: Column will not "
              "tell you its rate limits or when to retry, not-found comes back as "
              "the wrong HTTP code so naive error handling misclassifies it, "
              "there is no protection against two processes overwriting each "
              "other, and the request id you would hand support is real but "
              "undocumented."),
    (5, 5, "Best in class, and the category that matters most if you ever point "
           "an AI agent at a bank account. You can mint a key that reads balances "
           "and nothing else, or one that pays vendors by ACH but is structurally "
           "incapable of sending a wire, scoped to a single account. You can "
           "require a human to approve transfers from a given key, issue one key "
           "per tool, and kill any of them instantly. With a sandbox that behaves "
           "like production, you can build something risky without it ever "
           "touching real money."),
    (4.4, 5, "If you hand Claude or ChatGPT the job of writing your Column "
             "integration, it has unusually good material to work from. Column "
             "publishes its entire documentation as one clean file built for AI "
             "tools, plus a full machine-readable spec you can point a code "
             "generator at. Two cautions: an older webhook guide still shows a "
             "URL that no longer works, so build from the API reference rather "
             "than the narrative guides, and the changelog has gone quiet, with a "
             "single entry in all of 2026."),
    (11.3, 15, "Getting in to experiment is free and takes minutes, and the "
               "sandbox is a real, complete copy of the bank, which is unusually "
               "generous. Production is another matter. Column publishes no price "
               "anywhere, you cannot flip yourself live, and pulling rent by ACH "
               "debit means parking locked cash equal to your rolling 60-day "
               "debit volume. That last one is the practical catch for a property "
               "manager, because pulling rent is exactly the use case and the "
               "collateral scales with your rent roll."),
  ],
  "strengths": [
    "Scoped keys down to a single rail on a single account, plus human approval",
    "Idempotency proven live: the same payment sent twice created one transfer",
    "Signed webhooks retried for three days, across 190 event types",
    "A free sandbox that is a complete copy of the bank, every route included",
    "The whole documentation published as one clean file built for AI tools",
  ],
  "watch": [
    "No published rate limits, no Retry-After, and no backoff guidance",
    "Not-found returns HTTP 400, contradicting Column's own documentation",
    "No protection against two processes overwriting the same record",
    "No published pricing anywhere, and no self-serve path to production",
    "Collecting rent by ACH debit requires locked collateral against 60-day volume",
  ],
  "bottom": "Column is a real, nationally chartered bank with one of the best "
            "banking APIs you can build on, and unlike almost every banking API "
            "you will be pitched, there is no sponsor bank in the middle: Column "
            "holds the money itself. You could build automated owner "
            "disbursements, vendor payments, rent collection by ACH debit, check "
            "issuance and deposit, and a reconciliation feed with running "
            "balances, and hand an AI agent a key that reads balances but is "
            "structurally incapable of moving a dollar. What you cannot do is "
            "treat it as a substitute for your PMS or your trust accounting. The "
            "API has no concept of a property, unit, lease or tenant, and despite "
            "a polished property-management page promising trust reconciliation "
            "and owner disbursements, there is not one property-management "
            "endpoint in the API itself. Two words in the marketing deserve care: "
            "the trust accounts in Column's changelog are legal estate-planning "
            "trusts, not client trust accounting, and the PM-specific promises "
            "are relationship features reached through a sales conversation, not "
            "documented API capabilities. Biggest strength is control and safety; "
            "biggest limitation is operational opacity; and the biggest business "
            "limitation is not technical at all.",
},

"LeadSimple": {
  "score": 87, "grade": "B+",
  "meta": {"run": "Aug 28, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "43.33 / 50"},
  # The first row that moved because the VENDOR changed the product, not because
  # the evidence or the rubric changed. Worth saying out loud: it is the clearest
  # evidence the report card is doing what it is for.
  "note": "This is the first platform here to move because the vendor changed the "
          "product, rather than because the evidence or the rubric changed. "
          "Between the 2026-08-27 run and this one, LeadSimple shipped five "
          "fixes, all of them in its two weakest categories: a public "
          "documentation site, multiple API keys, read-only keys, per-key revoke, "
          "and key labels. Access Control went from 1.3 out of 5 to 4.4, and "
          "Documentation from 2.5 to 3.1, taking the score from 78 (C+) to 87 "
          "(B+). Coverage and cost did not move, because the API surface and plan "
          "access did not change. Two independent graders then scored the same "
          "frozen evidence and agreed on 25 of the 27 checks, with the two splits "
          "resolved against the evidence rather than averaged. The three runs "
          "landed at 85, 86 and 87, so the result is robustly B or B+.",
  "cats": [
    (15, 15, "You can build real tools on this. Read and change your main "
             "records, contacts, deals, and processes, and receive change events "
             "by webhook. Two gaps: you cannot create or complete a task through "
             "the API, and you cannot delete records through it."),
    (5.8, 10, "The one category the improvements did not touch, and it shows. "
              "Good in places: live rate-limit counters on every response, a "
              "request id on each one, and page totals so you can plan a full "
              "sync. Weaker elsewhere, and unchanged from the last run. Money "
              "fields come back as text rather than numbers, errors give a "
              "message but no fixed code, webhooks have no signature and no "
              "stated retry rule, and there is no version in the path and no "
              "deprecation policy."),
    (4.4, 5, "This was the weakest area on the card at 1.3 out of 5, and it is "
             "now one of the stronger ones. LeadSimple shipped read-only keys, "
             "multiple named keys, and per-key revoke. You can hand a reporting "
             "agent a key that cannot change anything, give every integration its "
             "own key, and cut one off without breaking the rest. The gap left is "
             "fine-grained scoping: the create-key dialog offers only read-only or "
             "full read and write, so a key still cannot be limited to particular "
             "data."),
    (3.1, 5, "The reference is now public, which was the big fix. A complete "
             "no-login reference, a downloadable OpenAPI 3.0 file, and request "
             "samples in five languages, so a developer or an AI tool can build "
             "against it without an account. Two gaps remain: no llms.txt for AI "
             "retrieval, and no API-specific changelog, only a product-wide one."),
    (15, 15, "Full marks. You enable the API and create keys yourself with no "
             "sales call, and the REST surface you need is included in the plan "
             "rather than locked behind the top tier."),
  ],
  "strengths": [
    "Gained 9 points by shipping fixes to its two weakest categories",
    "Read-only keys, multiple named keys, and per-key revoke, all self-serve",
    "Public OpenAPI 3.0 spec and reference, no login required",
    "Full coverage of contacts, deals, and processes, with webhooks",
    "API access included in the plan, not gated to the top tier",
  ],
  "watch": [
    "Money fields come back as text, not numbers",
    "Webhooks have no signature and no documented retry policy",
    "Errors carry no stable machine-readable code",
    "Keys are read-only or full access; still no per-resource scoping",
    "No version in the path, and no deprecation policy",
  ],
  "bottom": "LeadSimple's REST API has improved markedly, from 78 (C+) to 87 (B+), "
            "because it fixed its two weakest areas. You can now create multiple "
            "labeled keys, make a key read-only, and revoke any key on its own, so "
            "you can hand a reporting agent something safe and cut off one "
            "integration without breaking the rest. The documentation is public "
            "now, with a downloadable OpenAPI 3.0 file and request samples in five "
            "languages, so a developer or an AI tool can build against it without "
            "a login. The remaining weaknesses are in reliability rather than "
            "access: money fields come back as text, errors carry no stable code, "
            "webhooks have no signature or retry policy, and there is no clear "
            "version policy. LeadSimple is not a bank and not your system of "
            "record. It sits on top of your PMS, so you still need that PMS for "
            "property, lease, ledger and money data.",
},


"Property Meld": {
  "score": 49, "grade": "F",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Fable 5.1",
           "tier": "Fully verified, controlled live", "raw": "24.38 / 50"},
  # The re-run that replaces the superseded v2.0 result. Keep the note's second
  # half: it is the record of why re-scoring an old run arithmetically was the
  # wrong call, and the page should carry that rather than only the commit log.
  "note": "This replaces the 2026-08-25 run, which was graded on a superseded "
          "scoring model and published 76 (C). This is a fresh clean-room run: no "
          "prior material was read or reused, and it is graded Fully verified, "
          "with real writes performed on labelled "
          "fixtures under recorded authorisation and cleanup confirmed "
          "afterwards. The re-run scores well below the old one because it found "
          "things the first run never looked for: no way to cancel a work order, "
          "an assignment field that is undocumented and untyped, field types that "
          "disagree with the published schema, and an idempotency guide naming a "
          "header the API does not honour.",
  "cats": [
    (5.6, 15, "You can read everything about your maintenance operation, and you "
              "can create work orders, complete them, and manage units, "
              "properties, residents, owners, vendors and tags. Creating, "
              "updating and deactivating a property and a unit worked exactly as "
              "documented under live test. What you cannot do is cancel a work "
              "order, and assigning a vendor or technician is possible only "
              "through a field that is undocumented and untyped. Scheduling, "
              "estimate approval and invoice approval all belong to the vendor's "
              "side of this API. There are no webhooks, so automations must poll."),
    (5.0, 10, "A clean, predictable REST design with a real status page, but your "
              "code has to defend itself. Field types do not always match the "
              "published schema, error bodies come in three shapes with no "
              "machine-readable code, posting a duplicate tag name crashes with a "
              "500 rather than a 400, page size is silently capped at 500, and "
              "there is no way to detect a concurrent edit. Idempotency keys do "
              "work, but only with the header spelling used in the recipe, not "
              "the one in the guide."),
    (2.5, 5, "You can make separate keys for separate tools and revoke any of "
             "them yourself, both self-serve. But every key carries full read and "
             "write power over the whole account. You cannot hand an AI agent a "
             "read-only or limited key, and there is no sandbox, which is why "
             "this run had to work on labelled fixtures inside the live account."),
    (3.8, 5, "A coding assistant can load this API well: a public OpenAPI file, "
             "an llms.txt index, and a Markdown version of every documentation "
             "page. What is missing is human explanation. 93 of the 94 operations "
             "carry no worked example, most have no description at all, one guide "
             "documents an idempotency header that does not work, and the "
             "changelog has two entries in five years."),
    (7.5, 15, "A split decision. If you are on the Ops plan you can create a key "
              "in seconds without talking to anyone. If you are on Core, the API "
              "is not included at all, and getting it means moving every unit up "
              "to the top tier."),
  ],
  "strengths": [
    "Verified with real live writes on labelled fixtures, cleaned up afterwards",
    "Public OpenAPI 3.0.3 schema plus an llms.txt index built for AI tools",
    "Working idempotency keys, proven live on repeated creates",
    "Multiple self-serve keys, each revocable on its own",
    "Public status page with per-component uptime and incident history",
  ],
  "watch": [
    "No way to cancel a work order through the API",
    "Vendor assignment works only through an undocumented, untyped field",
    "No webhooks at all, so everything has to poll",
    "Every key has full read and write over the account, and there is no sandbox",
    "The idempotency guide names a header the API does not honour",
  ],
  "bottom": "Property Meld is a maintenance-only tool and its API reflects that. "
            "You can build reporting, reminders, dashboards and intake automations "
            "on top of your work orders, units, residents and vendors today, you "
            "can create work orders and mark them complete, and live testing "
            "confirmed that creating, updating and deactivating properties, units "
            "and tags works cleanly. You cannot cancel a work order, you cannot "
            "reliably assign a vendor because the only field for it is "
            "undocumented, and scheduling, estimate and invoice approvals belong "
            "to the vendor's side of the API. The strengths are a public OpenAPI "
            "file, an llms.txt index AI tools can read, working idempotency keys, "
            "and self-serve keys you can revoke. The limitations are missing "
            "webhooks, full-access-only keys with no sandbox, loose typing, a "
            "guide documenting the wrong idempotency header, and an API sold only "
            "with the top plan. It holds no funds, so you still need your PMS for "
            "ledgers, owner statements and payments.",
},

"RentEngine": {
  "score": 78, "grade": "C+",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "38.83 / 50"},
  # Supersedes the 2026-08-27 run (74, C). Four of five categories moved, mostly
  # because the earlier run missed first-party evidence that exists: a status
  # page, a changelog, and a written compatibility policy. RentEngine also
  # shipped spec 1.3.0 in between.
  "note": "This replaces an earlier run from 2026-08-27 that scored 74 (C). Two "
          "things changed. The first run reported no status page and no changelog; "
          "both exist, along with a written compatibility policy promising 30 days "
          "notice before a breaking change, which is why Design and Reliability "
          "rose from 4.6 to 7.1. RentEngine also shipped a new API version in "
          "between. This run was graded three times against the same frozen "
          "evidence, with unreconciled totals of 75, 81 and 78, and the published "
          "78 is recomputed from the reconciled marks rather than averaged. "
          "Categories 2, 3 and 5 were unanimous. Two checks carry residual "
          "sensitivity, so the honest band is 74 to 82, centred on 78.",
  "cats": [
    (9.4, 15, "You can read essentially everything RentEngine knows: leads, units, "
              "showings, applications, screening results, calls, messages, and "
              "reports. That is the coverage that matters most for a leasing "
              "integration. You can also push new leads, schedule showings, manage "
              "unit inventory, and add notes and follow-ups. The limits are on "
              "changing state. You cannot update a prospect's fields at all, stage "
              "advancement is limited to two event types, there is no delete and no "
              "showing cancel, and the approve or reject decision lives in your PMS."),
    (7.1, 10, "Built to run in production, and confirmed live. Rate-limit headers, "
              "a real Retry-After, request ids you can quote to support, a clear "
              "versioning and deprecation contract, and a public status page are "
              "all present. The gaps are manageable: errors carry no stable machine "
              "code so you match on status and message text, there is no "
              "idempotency key, there is no protection against two writers "
              "overwriting each other, and webhook verification is an optional "
              "shared secret rather than a real signature."),
    (3.0, 5, "You can create several named keys and revoke them yourself, which is "
             "good for separating integrations and cutting off access fast. The "
             "weakness is blast radius. Every key carries the full permissions of "
             "the user who created it, and there is no read-only or "
             "resource-scoped option. To give an AI agent or a third party a narrow "
             "slice, your only lever is to create a limited RentEngine user and "
             "mint the token as that user. Treat every token like a password."),
    (4.4, 5, "A real strength. A developer or an AI coding tool can build straight "
             "from the public OpenAPI 3.1 spec without reverse-engineering, the "
             "guides for auth, pagination, rate limits and webhooks are clear, and "
             "the changelog was current to the day before this run. The one gap is "
             "a purpose-built AI retrieval corpus: the llms.txt file is an index "
             "only, so an AI tool leans on the spec instead."),
    (15, 15, "Full marks, and the opposite of the call-sales-to-unlock pattern "
             "common in this industry. If you are a customer you create your own "
             "key in the portal in minutes. API access is part of the standard "
             "platform on transaction pricing, with no premium tier gating it."),
  ],
  "strengths": [
    "API access included on standard pricing, with self-serve keys",
    "Public OpenAPI 3.1 spec, downloadable as JSON and YAML",
    "A written compatibility policy with 30 days notice before breaking changes",
    "Changelog current to the day before the run, and a public status page",
    "Request ids you can quote to support, echoed back if you supply your own",
  ],
  "watch": [
    "No endpoint updates a prospect's fields, and stage advance covers two events",
    "No delete anywhere, and no showing cancel",
    "Every key carries its creator's full permissions; no read-only option",
    "No idempotency key and no concurrency control, so retries and races need care",
    "Webhook verification is an optional shared secret, not a signature",
  ],
  "bottom": "RentEngine gives you a real, modern, well-documented leasing API you "
            "can get into today without a sales call, and it is genuinely strong at "
            "reading your leasing data and feeding it: leads in, showings "
            "scheduled, and change events out by webhook for the core objects. Its "
            "biggest strength is buildability and access, with a clean OpenAPI 3.1 "
            "spec, production-grade operability signals, and self-serve keys that "
            "are not paywalled. Its biggest limitation is write depth and safety. "
            "You cannot update a prospect or approve applications through the API, "
            "there is no delete, and there is no idempotency key, no concurrency "
            "control, and no read-only credential. It is a top-of-funnel leasing "
            "system, not a bank, PMS or trust-accounting platform, so you will "
            "still run accounting and the signed-lease lifecycle in your PMS.",
},

"Process Street": {
  "score": 73, "grade": "C",
  "meta": {"run": "Aug 31, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Fully verified, controlled live", "raw": "36.25 / 50"},
  # The only Fully verified run so far, and the only one graded three times.
  # The note below is not optional colour: the report leaves one disagreement
  # unresolved that moves the letter grade, so publishing 73 without it would
  # present a contested number as settled.
  "note": "Graded three independent times against the same frozen evidence. The "
          "three unreconciled totals were 75, 72 and 70, and the published 73 is "
          "not their average: it is recomputed from the check-level marks after "
          "each disagreement was resolved against the evidence. 21 of 26 "
          "applicable checks were unanimous. One disagreement is left unresolved "
          "and it moves the grade: on change notification, a strict reading of the "
          "scoring band gives 69 (D+) instead of 73 (C). This is also the only "
          "result here graded Fully verified on all eight live-test steps against a "
          "live account, including "
          "real writes and an observed webhook delivery, with nothing graded from "
          "documentation alone.",
  "cats": [
    (13.1, 15, "The strongest part of the API. Everything the product does, the "
               "API can do: start a checklist, tick tasks off, write form answers, "
               "assign people, build and publish templates, manage data sets. The "
               "writes were proven on a live account rather than taken from the "
               "docs. The weak spot is being told when things change. You get an "
               "event when a run starts, when a task is ticked, and when a run "
               "finishes, and nothing else. There is no changed-since filter "
               "anywhere, so anything outside those events means re-reading the "
               "whole list and comparing it yourself."),
    (5.0, 10, "The weakest half of the API, and the reason the grade sits where it "
              "does. The shape is fine: clean REST, sensible pagination with a "
              "documented sort order, and rate-limit headers that tell you exactly "
              "when to back off. Three things will cost you real engineering time. "
              "Retry safety is broken: the documentation promises that sending the "
              "same start-this-checklist request twice will not duplicate it, and "
              "in live testing it created two runs. The form-field data is loosely "
              "typed in both directions, and the docs describe the read format "
              "incorrectly. And there is no version check, so two systems writing "
              "the same run will silently overwrite each other."),
    (3.1, 5, "The category with real operational risk. Outside Enterprise, every "
             "API key is a full organization administrator. There is no read-only "
             "key and no way to limit a key to one workflow or folder, so any key "
             "you issue could delete every workflow in the account. You do get two "
             "real controls: you can hold several separate keys, and you can revoke "
             "any one of them instantly yourself. Treat every key as a master "
             "password and give each integration its own."),
    (3.8, 5, "A genuine strength. The full machine-readable spec is public and "
             "free, no login and no sales call, so an AI coding tool can consume "
             "the whole API in one file. Process Street also runs its own MCP "
             "server, which means Claude can drive the account directly without you "
             "writing an integration at all. That is unusual and genuinely "
             "valuable. Cautions: many write endpoints have no worked example, the "
             "AI-specific files are only link indexes, and the overview contains at "
             "least two statements that live testing disproved."),
    (11.3, 15, "Getting in the door is easy and free. You create keys yourself, and "
               "the whole API works on the entry plan. The catch is on paper rather "
               "than in practice: the Startup plan officially allows 50 API calls a "
               "month, which would be useless for real automation, though nothing "
               "enforced that limit during testing. Confirm your actual quota before "
               "building anything business critical, and note that scoped keys are "
               "Enterprise only."),
  ],
  "strengths": [
    "The only Fully verified result so far: all eight live-test steps run, writes included",
    "Graded three independent times, every disagreement resolved against the evidence",
    "Full OpenAPI 3.1 spec, public and free, no login required",
    "A first-party MCP server, so Claude can drive the account directly",
    "API access included on every plan, with self-serve keys",
  ],
  "watch": [
    "Documented duplicate prevention does not work: the same request created two runs",
    "Every API key is a full organization admin outside Enterprise",
    "Form-field data is loosely typed, and the docs describe the read format wrongly",
    "No changed-since filter anywhere, so no incremental sync",
    "Webhooks carry no payload signature of any kind",
  ],
  "bottom": "Process Street's API can do essentially everything the product can do, "
            "and the writes were proven on a live account rather than taken on "
            "trust. The documentation is a real strength: the complete "
            "machine-readable spec is public and free, and Process Street runs its "
            "own MCP server, so Claude can drive an account with very little custom "
            "code. Three things should shape how you use it. Retry safety is broken, "
            "so build your own duplicate guard. The documentation is wrong in places "
            "that matter, so build against observed behaviour and test each endpoint "
            "yourself. And outside Enterprise every key is a full organization "
            "administrator, so give each integration its own key and revoke "
            "precisely. It is not a PMS, a bank, or a trust accounting system. It is "
            "the procedure layer that runs on top of whatever holds your properties, "
            "leases and money, and it does have a genuine property management "
            "offering, though that comes from templates rather than any "
            "property-specific objects in the API.",
},

"RingCentral": {
  "score": 93, "grade": "A",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "46.67 / 50"},
  # No cross-category caveat here. The table groups by software type, so this is
  # read against the other phone systems, which is the whole reason the grouping
  # exists. A note explaining that would only undercut the score.
  "note": "The highest score graded so far, and the first A. Graded three "
          "independent times, and all three runs landed on 93. 25 of the 27 "
          "checks were unanimous, and the two that split sat in the same category "
          "and offset each other exactly, so the total is 93 under either "
          "resolution. Read paths were tested live on a production account with a "
          "read-only key; the write paths are graded from documentation, because "
          "the key supplied could not write. A sandbox key would lift those to "
          "fully verified.",
  "cats": [
    (15, 15, "A perfect score. You can pull essentially all of your "
             "communications data, calls, texts, voicemail and the directory, "
             "and act on it programmatically by sending texts and placing or "
             "controlling calls. Real-time events arrive by webhook, and there is "
             "dedicated incremental sync for call logs and messages. The write "
             "actions are well documented but were not exercised live here, "
             "because the key supplied was read-only."),
    (7.9, 10, "Predictable and production-grade: clean REST, structured errors "
              "carrying a stable machine code, clear rate-limit and request-id "
              "headers, real pagination, and proper incremental sync. Two gaps "
              "matter if you automate messaging. There are no idempotency keys, "
              "so guard your own retries or a text can send twice. And there is "
              "no optimistic concurrency: the API does return a conflict on "
              "competing writes, but nothing stops a lost update."),
    (5, 5, "A perfect score, and the safest platform here to hand to an app or an "
           "AI agent. You can issue a read-only, narrowly scoped key, which is "
           "exactly what this run used, run a separate key per integration, test "
           "against a real sandbox with its own isolated data, and revoke access "
           "instantly."),
    (3.8, 5, "Strong and build-ready, with a published OpenAPI spec and "
             "maintained SDKs in every common language. Two weak spots: there is "
             "no llms.txt for AI retrieval, so an AI tool consumes the spec "
             "instead, and the central changelog's newest entry is from April "
             "2022. Confirm current behaviour against the live reference rather "
             "than the changelog."),
    (15, 15, "Full marks. A free developer account, self-issued keys, a sandbox "
             "included, and API access bundled with a normal subscription. No "
             "premium tier to unlock and no sales call."),
  ],
  "strengths": [
    "The highest score graded so far, and the only A",
    "Read-only and finely scoped keys, proven on the key used for this run",
    "A real sandbox with its own accounts and isolated data",
    "OpenAPI spec plus maintained SDKs in eight languages",
    "Dedicated incremental sync for call logs and messages",
  ],
  "watch": [
    "No idempotency keys, so a retried text or call can send twice",
    "No optimistic concurrency, so two writers can overwrite each other",
    "The central changelog has not been updated since April 2022",
    "No llms.txt, so AI tools fall back to the OpenAPI spec",
    "High-volume SMS needs separate A2P registration and entitlement",
  ],
  "bottom": "RingCentral's API is excellent to build on: modern REST with an "
            "OpenAPI spec and SDKs in every common language, granular read-only "
            "and scoped keys, a real sandbox, structured errors, rate-limit and "
            "request-id headers, proper pagination and incremental sync, and "
            "self-serve free access. For a property manager this is the "
            "communications layer. You can log every tenant, owner and vendor "
            "call and text, send SMS reminders, build click-to-call and "
            "screen-pop, and get real-time webhooks. It is not a PMS, an "
            "accounting system, or a trust-accounting system, and it holds no "
            "funds. Property management is not a documented use case, only a "
            "general fit. The main engineering cautions are the missing "
            "idempotency keys and the lack of lost-update protection, so protect "
            "your own retries of anything that sends a message or moves money, "
            "and the stale changelog, so verify against the live reference.",
},

"Tenant Turner": {
  "score": 51, "grade": "F",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Baseline verified", "raw": "25.42 / 50"},
  # Sits directly under RentEngine in the same category, which is the comparison
  # that matters: 51 against 78 for two leasing tools graded on the same rubric.
  "note": "Graded three independent times. The runs scored 56, 50 and 51 before "
          "reconciliation and agreed on 23 of the 26 applicable checks; the three "
          "splits were each resolved against the evidence rather than averaged, "
          "landing on 51. The F held in all three runs and under every "
          "single-check alternative either independent grader considered. One "
          "detail worth knowing if you are grading a platform yourself: Tenant "
          "Turner's API reference and OpenAPI file sit behind a customer login, "
          "and the run only proceeded because the operator supplied authenticated "
          "access. Without it most of three categories would have been unverified "
          "and the run would have failed the coverage gate outright.",
  "cats": [
    (3.8, 15, "You can read almost everything Tenant Turner knows about your "
              "listings, leads and showings, and you can publish and activate a "
              "listing end to end. What you largely cannot do is change things. "
              "There is no cancelling or rescheduling a showing, no updating a "
              "lead, no writing back showing feedback, and no turning self-access "
              "viewing on or off. Event coverage is genuinely strong, with 21 "
              "signed triggers, but for anything beyond listings you will be "
              "reading Tenant Turner and acting somewhere else."),
    (4.2, 10, "The shape of the API is fine, and the pagination and incremental "
              "filters are well behaved. The problems are the ones that bite in "
              "production. Money-adjacent numbers arrive as strings even though "
              "you write them as numbers, so every rent and deposit needs parsing "
              "and your types will not round-trip. Retrying a failed showing "
              "creation can double-book a prospect, because nothing prevents "
              "duplicates. Nothing tells you what the rate limit is or when you "
              "hit it. And you cannot quote a request id to support."),
    (1.3, 5, "The area with real operational risk. There is one key, it can do "
             "everything your account can do, and you cannot give a contractor, a "
             "vendor or an AI agent a narrower slice. If you hand that key to an "
             "automation and it misbehaves, your only lever is to refresh the key, "
             "which instantly breaks every other integration using it. With no "
             "sandbox either, there is nowhere safe to develop."),
    (1.3, 5, "For the REST endpoints, a developer or coding agent handed the "
             "OpenAPI file can build quickly. Everything around it is thin. The "
             "docs sit behind a login, so a coding tool cannot reach them unaided. "
             "Webhooks, the most useful capability here, have no documentation at "
             "all, so payload shapes must be reverse-engineered. And there is no "
             "changelog, so the first sign something changed will be your "
             "integration breaking."),
    (15, 15, "Full marks, and the category Tenant Turner wins outright. Nothing "
             "stands between you and the API. If you are a customer on any plan "
             "the key is already sitting in your portal, it costs nothing extra, "
             "and you can start building this afternoon."),
  ],
  "strengths": [
    "Free on every plan, with the key already sitting in your portal",
    "21 signed webhook events, enough to keep a CRM current in near real time",
    "Cursor pagination and incremental filters that behave well under test",
    "Full write control over listings, including activate and deactivate",
    "Public status page showing 100% uptime over 90 days",
  ],
  "watch": [
    "One all-powerful key: no read-only option, no scoping, no second key",
    "A showing cannot be cancelled or rescheduled, and a lead cannot be updated",
    "Rent and deposit amounts write as numbers and read back as strings",
    "No documented rate limit, and no idempotency, so a retry can double-book",
    "Webhooks are undocumented, so payload shapes must be reverse-engineered",
  ],
  "bottom": "Tenant Turner has done the hard part of access exactly right: the API "
            "is free, on every plan, and the key is already in your portal. What "
            "you get for that is a solid read surface over your listings, leads "
            "and showings, full write control over listings themselves, and 21 "
            "signed webhook triggers. If your goal is getting your leasing data "
            "out and into something else, you can build that today, though you "
            "will be reverse-engineering the event payloads and correcting the "
            "generated client as you go. What you cannot build is write-back "
            "automation for the things that move fastest: any workflow ending in "
            "'and then change it in Tenant Turner' ends with a person in the "
            "portal instead. Read the score for what it measures. This rates API "
            "buildability, not the product, and Tenant Turner is a leasing tool "
            "that clearly does its job. Treat the API as a very good read-and-"
            "notify feed with a narrow write path for listings.",
},

"Xero": {
  "score": 80, "grade": "B-",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "39.92 / 50"},
  # C2.8 has now flipped twice on the same run. Both flips were about what the
  # grader could READ, never about Xero. Worth stating, because this is the second
  # report (after RentEngine) marked down for evidence that existed on a page the
  # fetch tool could not render.
  "note": "Three runs scored 80, 80 and 78 and agreed on 25 of the 27 checks. The "
          "check that split was webhook delivery, marked down because no retry "
          "policy could be cited from the frozen evidence. It turns out the policy "
          "is documented: it sits on a JavaScript-rendered page the discovery tool "
          "could not load. Rendering that page in a browser confirmed all three "
          "legs, HMAC signatures, a retry schedule of immediate then every 15 "
          "minutes for 24 hours, and consumer replay guidance. So the check is "
          "finalised yes and the score is 80 (B-). Nothing about Xero changed at "
          "any point; what changed was what the grader could read. One "
          "disagreement stays open, on AI-readable documentation, and it is now "
          "the only check that moves the letter: 80 (B-) if partial, 79 (C+) if "
          "no.",
  "cats": [
    (13.1, 15, "You can read and change the accounting data your business runs on, "
               "post invoices and payments, and update contacts and accounts. What "
               "you cannot do is import bank statements or reconcile through the "
               "API; a partner bank feed or another tool does that. Plan to poll "
               "with the modified-since filter, because webhooks only cover a few "
               "record types."),
    (6.7, 10, "Stable and predictable to run in production. Rate limits, "
              "pagination, request tracing, and idempotency are all solid, and you "
              "can trace any request with support. Watch three things: dates arrive "
              "in two different formats, error shapes are not uniform, and there is "
              "no lost-update protection, so two writers can overwrite each other."),
    (4.5, 5, "A strong point. You can safely give an app or an AI agent a limited, "
             "read-only key, and cut off access at any time. The one gap is testing: "
             "there is no true sandbox, you develop against a Demo Company, which is "
             "a separate data set but not a separate environment or key."),
    (4.4, 5, "Among the best documentation in this group. A developer or an AI "
             "coding tool can build against Xero without reverse-engineering. The "
             "reference is complete, the OpenAPI spec and six official SDKs are "
             "current, and Xero ships an official MCP server for AI agents. The only "
             "soft spot is no llms.txt-style bundle."),
    (11.3, 15, "You can get in the door today for free and connect your own "
               "organization at no cost beyond your Xero subscription. Costs appear "
               "only when you scale: higher call volumes, more connections, or the "
               "hands-off machine-to-machine key all move you to a paid tier."),
  ],
  "strengths": [
    "A changelog kept current, with a dated deprecation window out to Sept 2027",
    "Granular read/write scopes, verified enforced in live testing",
    "Six official SDKs plus an official MCP server for AI agents",
    "First-class idempotency keys on writes",
    "A correlation id on every response that support can actually use",
  ],
  "watch": [
    "Not property management software: no properties, units, leases, or work orders",
    "No bank statement import or reconciliation through the API",
    "Webhooks cover only four record types, so you poll for the rest",
    "Dates come back in two different formats",
    "No true sandbox, only a Demo Company",
  ],
  "bottom": "Xero has a strong, mature accounting API. You can build your own tools "
            "and AI agents on top of your general ledger, with good rate limits, "
            "pagination, tracing, and read-only keys you can revoke. The biggest API "
            "limits are no bank statement import or reconciliation, webhooks for "
            "only a few record types, and no lost-update protection. The biggest fit "
            "limit is that Xero is general accounting, not property management: no "
            "native properties, units, leases, or work orders, and no first-party "
            "trust or security deposit workflows. Treat Xero as an excellent "
            "accounting backend to connect to, not a replacement for a PMS, a bank, "
            "or a trust accounting system.",
},

}


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def tier(points, maximum):
    """Colour band for a category score, as a share of that category's maximum.

    40% and under is red, 41 to 74 is orange, 75 and up is blue.

    These are deliberately NOT the methodology's letter-grade boundaries. Tying
    them to the rubric would paint 75% orange, which reads as a warning about a
    score that is actually respectable, and it would spend red on so many cells
    that red stops meaning anything. Set here so red stays rare and genuinely
    signals a problem worth looking at.
    """
    pct = float(points) / maximum * 100
    return "lo" if pct <= 40 else ("mid" if pct < 75 else "hi")


def grade_class(g):
    return "grade-" + g[0].lower() if g else "grade-none"

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def fmt_pts(v):
    """15.0 -> 15, 7.5 -> 7.5. Keeps the table from reading like a spreadsheet."""
    return str(int(v)) if float(v) == int(v) else str(v)


def build_pills():
    out = ['<div class="pill-row" aria-label="Jump to a category">']
    for s, _, _ in CATEGORIES:
        out.append(f'<a class="jump-pill" href="#cat-{s}">{PILL_LABELS[s]}</a>')
    out.append("</div>")
    return "\n        ".join(out)


def build_rows():
    rows = []
    for s, heading, companies in CATEGORIES:
        rows.append(
            f'<tr class="grp" id="cat-{s}"><td colspan="8">{heading}'
            f'<span class="grp-n">{len(companies)} listed</span></td></tr>'
        )
        for co in companies:
            r = RESULTS.get(co)
            if co in NO_API:
                rows.append(
                    f'<tr class="no-api"><td class="plat">'
                    f'<span class="co-name">{co}</span></td>'
                    f'<td class="num" colspan="7">'
                    f'<span class="cat-legacy">No API available</span></td></tr>'
                )
                continue
            if not r:
                cells = '<td class="num"><span class="cat-none">&ndash;</span></td>' * 5
                rows.append(
                    f'<tr><td class="plat"><span class="co-name">{co}</span></td>'
                    f'{cells}'
                    f'<td class="num"><span class="cat-none">&ndash;</span></td>'
                    f'<td class="num"><span class="grade grade-none">&ndash;</span></td></tr>'
                )
                continue

            if r.get("legacy"):
                # Subscores are on a different scale, so showing them in these
                # columns would invite a false comparison. Flag instead.
                cells = ('<td class="num" colspan="5"><span class="cat-legacy">'
                         'graded on the older v2.0 scale, see details</span></td>')
            else:
                maxes = [m for _, m in CAT_LABELS]
                cells = "".join(
                    f'<td class="num"><span class="cat-score '
                    f'{tier(p, maxes[i])}">{fmt_pts(p)}</span></td>'
                    for i, (p, _, _) in enumerate(r["cats"])
                )
            flag = ' <span class="row-flag">v2.0</span>' if r.get("legacy") else ""
            rows.append(
                f'<tr class="has-detail" data-co="{slug(co)}">'
                f'<td class="plat"><button class="co-btn" type="button">'
                f'<span class="co-name">{co}</span>{flag}'
                f'<span class="co-hint">Click for details</span></button></td>'
                f'{cells}'
                f'<td class="num"><span class="cat-total">{r["score"]}</span></td>'
                f'<td class="num"><span class="grade {grade_class(r["grade"])}">'
                f'{r["grade"]}</span></td></tr>'
            )
    return "\n            ".join(rows)


def build_stats():
    graded = [r for r in RESULTS.values()]
    listed = sum(len(c) for _, _, c in CATEGORIES)
    # Round half up, matching the methodology's own rule for scores.
    # Python's round() is banker's rounding: it would turn 72.5 into 72.
    avg = (int(sum(r["score"] for r in graded) / len(graded) + 0.5)
           if graded else "&ndash;")
    best = max(graded, key=lambda r: r["score"]) if graded else None
    best_txt = f'{best["grade"]}' if best else "&ndash;"
    best_who = next((n for n, r in RESULTS.items() if r is best), "")
    return (
        '<div class="stats stats-color g4" aria-label="At a glance">'
        f'<div class="stat"><div class="v">{listed}</div><div class="k">Platforms listed</div></div>'
        f'<div class="stat"><div class="v">{len(graded)}</div><div class="k">Graded so far</div></div>'
        f'<div class="stat"><div class="v">{avg}</div><div class="k">Average score</div></div>'
        f'<div class="stat"><div class="v">{best_txt}</div><div class="k">Highest grade ({best_who})</div></div>'
        '</div>'
    )


def build_data():
    """The JSON the modal renders from. Same numbers as the table, by construction."""
    out = {}
    for name, r in RESULTS.items():
        maxima = r["legacy"]["maxima"] if r.get("legacy") else [m for _, m in CAT_LABELS]
        cat = next(h for _, h, cos in CATEGORIES if name in cos)
        out[slug(name)] = {
            "n": name, "cat": re.sub("&amp;", "&", cat),
            "s": r["score"], "g": r["grade"], "gc": grade_class(r["grade"]),
            "m": r["meta"],
            "c": [{"l": re.sub("&amp;", "&", CAT_LABELS[i][0]),
                   "p": fmt_pts(p), "x": maxima[i],
                   "pct": round(float(p) / maxima[i] * 100),
                   "tier": tier(p, maxima[i]),
                   "t": t}
                  for i, (p, _, t) in enumerate(r["cats"])],
            "st": r["strengths"], "w": r["watch"], "b": r["bottom"],
            "lg": r["legacy"]["note"] if r.get("legacy") else None,
            "rs": r.get("note") or r.get("rescored"),
        }
    return json.dumps(out, separators=(",", ":"), ensure_ascii=False)


BANDS = [(97,"A+"),(93,"A"),(90,"A-"),(87,"B+"),(83,"B"),(80,"B-"),
         (77,"C+"),(73,"C"),(70,"C-"),(67,"D+"),(63,"D"),(60,"D-"),(0,"F")]


def check_math():
    """Every row must add up, and its letter must match the published number.

    The category points, the headline score, and the grade are three separate
    fields that a careless edit can knock out of step. This recomputes the score
    from the parts and re-derives the letter from the v1.1 bands, and refuses to
    build if either disagrees. Rounding tolerance is one point, because the
    displayed category points are rounded to one decimal.
    """
    for name, r in RESULTS.items():
        maxima = r["legacy"]["maxima"] if r.get("legacy") else [m for _, m in CAT_LABELS]
        raw = sum(float(p) for p, _, _ in r["cats"])
        got = raw / sum(maxima) * 100
        if abs(got - r["score"]) > 1.0:
            raise SystemExit(
                f"{name}: categories sum to {raw:.2f}/{sum(maxima)} = {got:.1f}, "
                f"but the published score is {r['score']}")
        letter = next(g for lo, g in BANDS if r["score"] >= lo)
        if letter != r["grade"]:
            raise SystemExit(
                f"{name}: {r['score']}/100 is {letter} under the v1.1 bands, "
                f"but the grade is set to {r['grade']}")
        print(f"  ok  {name:15} {raw:5.2f}/{sum(maxima)} -> {r['score']} {r['grade']}")


def main():
    check_math()
    html = PAGE.read_text(encoding="utf-8")

    results_block = f"""      {build_stats()}
      <p class="sub" style="margin-top:16px;font-size:14px;">Scores are point-in-time and tied to the evidence access date. Methodology v1.1.</p>

      <h2 class="h-lead" style="margin-top:46px;">The results.</h2>
      <p class="sub" style="margin:10px 0 18px;">Scores are point-in-time, based on first-party documentation and, where available, live testing. Click any graded platform for the full breakdown.</p>

        {build_pills()}

      <p class="tbl-hint">Scroll the table sideways to see every category &rarr;</p>
      <div class="table-scroll">
        <table class="rank-table">
          <thead>
            <tr>
              <th>Platform</th>
{chr(10).join(f'              <th class="num col-cat">{l}<span class="th-max">/{m}</span></th>' for l, m in CAT_LABELS)}
              <th class="num">Score</th>
              <th class="num">Grade</th>
            </tr>
          </thead>
          <tbody>
            {build_rows()}
          </tbody>
        </table>
      </div>"""

    html = re.sub(
        r"(<!-- RESULTS:START -->\n).*?(\s*<!-- RESULTS:END -->)",
        lambda m: m.group(1) + results_block + m.group(2),
        html, flags=re.S,
    )

    html = re.sub(
        r"(<!-- DATA:START -->\n).*?(\s*<!-- DATA:END -->)",
        lambda m: (m.group(1)
                   + '<script type="application/json" id="coData">'
                   + build_data() + "</script>" + m.group(2)),
        html, flags=re.S,
    )

    PAGE.write_text(html, encoding="utf-8")
    print(f"Wrote {PAGE}")
    print(f"  {sum(len(c) for _,_,c in CATEGORIES)} companies in "
          f"{len(CATEGORIES)} categories, {len(RESULTS)} graded")


if __name__ == "__main__":
    main()
