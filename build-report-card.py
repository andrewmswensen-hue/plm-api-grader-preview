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
    ("inspections",  "Inspections",
        ["zInspector", "ResidentInspect", "RentCheck", "HappyCo", "SnapInspect",
         "PropertyInspect"]),
    ("banks",        "Banks",
        ["Column", "Enterprise Bank"]),
    ("accounting",   "Corporate Accounting",
        ["Xero", "QuickBooks Online"]),
    ("deposits",     "Deposits",
        ["Obligo", "Lighthouse", "Rhino", "Jetty"]),
    ("phone",        "Phone",
        ["RingCentral", "LeadSimple Phone", "SimpleVOIP", "Zoom Phone", "OpenPhone"]),
]

# Short labels for the pills (the headings above are too long for a pill row).
PILL_LABELS = {
    "pm-software": "PM Software", "listings": "Listings &amp; Screening",
    "workflow": "Workflow &amp; CRM", "maintenance": "Maintenance",
    "inspections": "Inspections", "banks": "Banks",
    "accounting": "Corp Accounting", "deposits": "Deposits", "phone": "Phone",
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
          "AppFolio scores 7.9 out of 10, the second highest of any platform graded "
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
    (5, 5, "A perfect score, and the best access control graded so far. Issue a "
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

"LeadSimple": {
  "score": 78, "grade": "C+",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "39.17 / 50"},
  "cats": [
    (15, 15, "You can build real tools on this. Read and change your main records, "
             "contacts, deals, and processes, and receive change events by webhook. "
             "Two gaps: you cannot create or complete a task through the API, and "
             "you cannot delete records through it."),
    (5.4, 10, "Good in places: live rate-limit counters on every response, a request "
              "id on each one, and page totals so you can plan a full sync. Weaker "
              "elsewhere: money fields come back as text rather than numbers, errors "
              "give a message but no fixed code, webhooks have no signature and no "
              "stated retry rule, and there is no API version policy at all."),
    (1.3, 5, "The weakest single score on the board. LeadSimple gives one API key "
             "for the whole account, and that key can read and change everything. "
             "No read-only key, no way to limit a key to certain data, and no "
             "separate keys per tool. You can rotate it yourself, but a leaked key "
             "puts the entire account at risk."),
    (2.5, 5, "Workable for a developer, with limits. There is a full OpenAPI file "
             "for code tools, but the reference sits behind a login rather than "
             "being public, there are no AI-ready docs for the API, and no "
             "API-specific changelog."),
    (15, 15, "Full marks. You enable the API and copy the key yourself with no sales "
             "call, and the REST surface you need is included in the plan rather "
             "than locked behind the top tier."),
  ],
  "strengths": [
    "Full coverage of contacts, deals, and processes, with webhooks",
    "Included in the plan, not gated to the top tier",
    "Self-serve key with no sales call",
    "Live rate-limit counters and a request id on every response",
  ],
  "watch": [
    "One all-powerful account key, with no read-only or scoped option",
    "Webhooks have no signature and no documented retry policy",
    "Money fields return as text, not numbers",
    "No API version or deprecation policy",
    "Docs require a login",
  ],
  "bottom": "LeadSimple gives you a real, useful REST API. You can read and change "
            "your core CRM and operations data, contacts, deals, processes, "
            "communications, custom fields, and reports, and get change events by "
            "webhook. Its two clear weaknesses are safe automation and "
            "documentation. There is exactly one account key, it can do everything, "
            "and you cannot narrow it, so guard and rotate it carefully. Access "
            "itself is a genuine strength: self-serve and included on the plan. "
            "LeadSimple is not your system of record, it sits on top of your PMS, so "
            "you still need AppFolio, Buildium, or the like for property, lease, and "
            "money data.",
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
          "result so far graded Fully verified, meaning all eight live-test steps "
          "ran, including real writes and a webhook delivery, with nothing graded "
          "from documentation alone.",
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
    (3.8, 5, "The strongest category. The full machine-readable spec is public and "
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

"Xero": {
  "score": 80, "grade": "B-",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "39.92 / 50"},
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
    "Highest score graded so far, and the only B so far",
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
# AWAITING RE-RUN. Not rendered. Property Meld was graded on 2026-08-25 under
# methodology v2.0, which scored all five categories out of 10 rather than
# 15/10/5/5/15, and included two checks (C5.2 free sandbox, C5.4 onboarding
# friction) that no longer exist.
#
# Its numbers cannot be converted. The report states no category score out of 15
# or 5 anywhere, and Category 5 in particular earns "2 of 4" checks, two of which
# were retired, so there is nothing in the report to convert from. Any figure put
# in those columns would be one we calculated, not one a grading run produced.
#
# So the row is simply blank, like every other ungraded platform, until Peter
# re-runs Property Meld against the current methodology file. When that lands,
# move this entry back into RESULTS and replace score, grade, meta, and cats with
# the new run's numbers. The prose below (strengths, watch-outs, bottom line) is
# drawn from the v2.0 report and should be re-checked against the new one.
#
# Kept here rather than deleted so nothing from Peter's original run is lost.
# ---------------------------------------------------------------------------
AWAITING_RERUN = {

"Property Meld": {
  # DO NOT re-score this by hand. An earlier pass recomputed it to 72 (C-) under
  # the v1.1 weighting. The arithmetic was traceable, but every resulting number
  # was calculated rather than produced by a grading run, and the report states
  # no category score out of 15 or 5 anywhere. Category 5 is the clearest case:
  # the report earns "2 of 4" checks, two of which (C5.2 free sandbox, C5.4
  # onboarding friction) no longer exist, so its v1.1 score cannot be derived
  # from anything the report actually says. Only the published 76 (C) below is a
  # real result. Replace this whole entry when the v1.1 re-run lands.
  "score": 76, "grade": "C",
  "meta": {"run": "Aug 25, 2026", "method": "2.0", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "38.07 / 50"},
  "legacy": {
    "maxima": [10, 10, 10, 10, 10],
    "note": "This run was graded under methodology v2.0, which scored all five "
            "categories out of 10. Despite the higher number, v2.0 came before the "
            "current file: the line ran v2.0, then v1.1, then v1.2, which weights "
            "the categories 15 / 10 / 5 / 5 / 15. The numbers below are the ones "
            "this run actually published, on the older scale, so they are shown "
            "here rather than in the table, where they would invite a false "
            "comparison against the other rows. Property Meld is queued for a "
            "re-run against the current methodology, and this row will be replaced "
            "with that result.",
  },
  # Originally run and published under methodology v2.0 (76/100, C). Re-scored
  # here under v1.1 from the same frozen evidence packet. Not one check mark was
  # changed; only the category weighting differs, exactly as the LeadSimple run
  # was re-scored from v2.0 to v1.1. See "rescored" below for the reader-facing
  # version of this note.
  "cats": [
    (8.8, 10, "You can build the whole maintenance workflow: intake a work order, "
              "assign a vendor or technician, schedule it, complete it, and review "
              "it. The only coverage limit is change detection. There are no "
              "webhooks, so you poll for changes instead."),
    (6.8, 10, "Modern, well typed, idempotent, paginated, and transparent about "
              "uptime. The reliability gaps are real though: no protection against "
              "two writes overwriting each other, no bulk export, no Retry-After "
              "header, no documented request id for support, and error codes you "
              "cannot branch on."),
    (8.8, 10, "You can run several keys, revoke any of them yourself, and get a "
              "read-limited identity. Scoping is role-based rather than "
              "fine-grained, so you pick from set tiers rather than choosing "
              "exactly what a key can touch."),
    (8.8, 10, "Genuinely AI-friendly, and among the best documentation in this "
             "group. A public OpenAPI spec plus a real llms.txt corpus, with a "
              "Markdown twin of every page. The only weak signal is the changelog, "
              "which has two entries and has not been touched in about three years."),
    (5.0, 10, "Key creation is self-serve in the app, which is a real improvement, "
              "but there is still no free sandbox to test against and the API needs "
              "the higher Ops plan rather than the cheaper Core plan."),
  ],
  "strengths": [
    "Best-in-class AI-readable docs: llms.txt plus a Markdown twin per page",
    "Real idempotency keys on writes, with 24-hour retention",
    "Multiple keys, self-serve create and revoke",
    "Public status page showing 99.98% to 100% uptime",
  ],
  "watch": [
    "No webhooks at all, so you have to poll for every change",
    "No protection against two writes overwriting each other",
    "No free sandbox, so write testing happens against production",
    "Needs the higher Ops plan",
    "Changelog is about three years stale",
  ],
  "bottom": "Property Meld is a strong, genuinely AI-friendly build target for the "
            "full maintenance workflow, with idempotency keys, a public uptime page, "
            "and documentation as good as any here. The reliability gaps are "
            "real: no webhooks (you poll instead), no lost-update protection, no "
            "bulk export, and no support-usable request id. Access still costs the "
            "higher Ops plan with no free sandbox. Reads were live-tested, but write "
            "behavior is graded from documentation, because there is no sandbox to "
            "write against.",
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
