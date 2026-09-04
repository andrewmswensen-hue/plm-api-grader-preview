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
from pathlib import Path

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
          "AppFolio scores 7.9 out of 10, among the stronger marks here. The F comes from the other half of the question, which is what "
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
    "Strong Design and Reliability, 7.9 out of 10",
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

"Aptly": {
  "score": 58, "grade": "F",
  "meta": {"run": "Sep 3, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Fully verified, controlled live", "raw": "29.09 / 50"},
  # Second Fully verified run on the board. Perfect scores in Documentation and
  # Access Control sitting next to an F, because half of the heaviest category
  # is lost to a premium gate with no published price.
  "note": "Graded Fully verified, with writes exercised for real: a labelled fixture card was "
          "created, updated, moved through a stage transition and archived on a "
          "production board, with containment checked across every API-enabled "
          "board and the card count restored to its baseline afterward. Two "
          "checks could not be observed and both are disclosed rather than "
          "guessed. There is no idempotency mechanism to test, so that check was "
          "graded from documented absence. And webhooks could not be established "
          "either way: Aptly's developer portal contains no webhook content at "
          "all across a 250,000-byte corpus, while its customer help centre "
          "carries one row that reads like an outbound event. The report "
          "computed the score both ways and it is 58 either way, so the "
          "unresolved check changes nothing.",
  "cats": [
    (7.5, 15, "You can read everything on an Aptly board and create and change "
              "cards reliably, all of it verified live. What you cannot do is "
              "manage the automation layer through the API, and you cannot be "
              "notified when something changes. Every integration has to poll on "
              "a timer and ask what changed since last time. That works, and the "
              "updated-since filter is honest at hour granularity, but two things "
              "need care: send a malformed timestamp and Aptly quietly hands back "
              "every record instead of erroring, and the built-in text search did "
              "not reliably find cards that plainly existed. There is also no way "
              "to delete a card through the API, only archive, so a mistaken "
              "record has to be cleaned up by hand."),
    (4.1, 10, "The weakest part of the API, and weak in a specific way: the "
              "everyday experience is good, and the guarantees you would want "
              "before trusting it with unattended automation are missing. Errors "
              "come back clean and machine-readable, paging through cards is "
              "solid, and pulling a full dataset or just what changed is easy. "
              "What is missing matters. If a write times out and your code "
              "retries, you can get a duplicate card, because there is no way to "
              "say this is the same request. If two automations touch the same "
              "card at once, the second silently wins: the run proved it by "
              "sending a deliberately out-of-date update and watching Aptly "
              "accept it. There is no version number on the API and no published "
              "breaking-change policy, and no working status page. One practical "
              "quirk: after a write, reading the card back immediately can still "
              "show the old value for a minute or two."),
    (5, 5, "Full marks, and the part that matters most for handing access to an "
           "AI agent. You can issue a key that can only read, only on the boards "
           "you name, and nothing else, and you can kill it yourself in seconds "
           "without emailing anyone. Requests outside a key's boards or "
           "permissions come back as a 403. The one gap is that there is no "
           "practice environment, only your live account, which is why the write "
           "testing in this run was confined to a single labelled fixture that "
           "was created and then archived."),
    (5, 5, "Full marks, and not a close call. The documentation is complete, "
           "public, and specifically built so an AI assistant can read it and "
           "write correct code: a real OpenAPI file, a per-endpoint reference, "
           "every page retrievable as Markdown, and a single file containing the "
           "entire API that you can paste into a chat. Aptly also runs its own "
           "MCP server with real write tools. Two things to know: one link Aptly "
           "advertises as an OpenAPI file actually serves an unrelated sample "
           "document, and the customer help centre is months out of date and "
           "contradicts the developer docs in three places, so trust the "
           "developer portal."),
    (7.5, 15, "Half marks on the heaviest category in the rubric, and the single "
              "biggest reason for the grade. Creating a key is genuinely "
              "self-serve, with no sales call and no approval step. But API "
              "access requires Aptly's Premium plan, and Aptly publishes no plan "
              "tiers or prices at all, so an operator cannot work out what API "
              "entitlement costs without a sales conversation. Worth knowing for "
              "a practical reason too: if a subscription is ever downgraded, the "
              "API and every automation built on it stop working, and nothing in "
              "the developer documentation warns of that dependency."),
  ],
  "strengths": [
    "Fully verified: a fixture card was created, updated, stage-changed and archived on a live board",
    "Documentation built for AI retrieval, including one file containing the entire API",
    "A real OpenAPI 3.0.3 spec plus a first-party MCP server with write tools",
    "A dated changelog current to ten days before the run, with per-endpoint entries",
    "Keys scoped to named boards and to read, insert or update, enforced with a 403",
    "Self-serve keys with optional expiration, revocable by you in seconds",
    "Published numeric rate limits with a worked backoff example",
    "Exemplary card pagination: stable ordering verified across repeat and adjacent pages",
  ],
  "watch": [
    "API access requires a Premium plan, and Aptly publishes no prices at all",
    "No webhooks, so every integration polls on a timer",
    "No idempotency: a timeout followed by a retry can create a duplicate card",
    "No concurrency control: a deliberately stale update was accepted and applied",
    "No delete anywhere in the API; cards can only be archived",
    "A malformed updated-since value returns 200 and every record instead of an error",
    "No version identifier on any endpoint, and no breaking-change policy",
    "No working status page: status.getaptly.com serves a redirect loop",
    "Reads immediately after a write can show the old value for a minute or two",
    "No sandbox, so every test happens in the live account",
  ],
  "bottom": "Aptly's API is unusually well documented and unusually lightly "
            "guaranteed: a genuinely useful tool with almost none of the safety "
            "rails you would want around unattended automation. You can read "
            "every board, card, contact and task, create and update cards, fire "
            "your board workflows by changing a card's stage, and pull either a "
            "full dataset or just what changed since last night. All of it was "
            "verified against a live account, including creating, updating and "
            "archiving a card on a production board. The documentation is "
            "outstanding and the access controls are excellent, letting you hand "
            "an AI agent a key that can only read, only on the boards you choose, "
            "revocable in seconds. What you cannot build is anything that needs "
            "to react the moment something happens, or anything that must not be "
            "allowed to go wrong quietly. There are no webhooks, so every "
            "integration polls. There is no way to mark a write as a retry, so a "
            "timeout can produce a duplicate. There is no protection against two "
            "automations overwriting each other, proven live with a deliberately "
            "stale update. No version number, no breaking-change policy, no "
            "working status page, and no practice environment. The F lands there "
            "for two concrete reasons: those write and reliability guarantees, "
            "and the fact that the API sits behind an unpublished Premium plan. "
            "None of that makes Aptly the wrong tool. It is a "
            "property-management-specialized workflow and communication layer and "
            "that is the job it does. But it is not a system of record and not a "
            "bank: it holds no funds, has no ledger, and documents no trust, "
            "escrow or security-deposit accounting. Use it to read and write "
            "workflow state on a schedule, with a read-only key wherever one will "
            "do, and pause before verifying a write.",
},

"Boom": {
  "score": 64, "grade": "D",
  "meta": {"run": "Sep 3, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Baseline verified", "raw": "31.88 / 50"},
  # The largest run-1 bias recorded on this board: the discovering evaluator
  # published 80 (B-) and the two cold-start graders, who never saw each other's
  # work, landed at 64 and 63. Run 1 was the outlier on four of six splits and
  # was corrected on all four in the same direction, by grading against what
  # Boom has rather than against the classification fixed before inspection.
  "note": "Graded three independent times, and the three runs disagreed sharply. "
          "The discovering evaluator published 80 (B-). The two cold-start "
          "graders, who never saw run 1's marks or each other's, landed at 64 and "
          "63. The reconciled result is 64. Run 1 was the outlier on four of the "
          "six splits and was corrected on all four in the same direction: it "
          "graded against the capabilities Boom happens to have rather than "
          "against the classification fixed before inspection, which is the "
          "adjust-to-fit error the methodology exists to prevent. It also carried "
          "one plain factual error the independents caught, listing decision "
          "reversal as present when no endpoint in either specification performs "
          "it. Four disagreements are recorded rather than averaged away, and one "
          "of them moves the grade: scoring lease lifecycle 0.0 instead of 0.5 "
          "would give 56 (F). The report flags that question as the one deserving "
          "a methodology ruling, namely what lease lifecycle should demand of a "
          "screening tool that deliberately hands the lease to a system of "
          "record. The honest band is 56 to 65. Four checks were "
          "documentation-graded because live write testing was not authorized and "
          "no sandbox credential was available.",
  "cats": [
    (7.5, 15, "You can run the whole screening funnel from your own code: create "
              "a lead, turn it into an application, pull the credit, criminal, "
              "eviction and income reports, read Boom's recommendation, approve "
              "or reject with your own reasons, and have Boom push the approved "
              "applicant into your PMS. You can also enroll residents in rent "
              "reporting, keep lease terms current, and close them out at "
              "move-out. What you cannot do is manage a lease, since there is no "
              "lease record here at all, configure the screening rules, upload or "
              "sign a document, or undo a decision through the API even though a "
              "person can do it in the portal. Plan on a person in the Boom "
              "portal for setup and reversals, and your code for everything in "
              "between."),
    (5.0, 10, "The API works, and the parts you touch first are pleasant: clean "
              "REST, real pagination with totals that survived a repeat-and-"
              "overlap test, validation errors that name the offending field, and "
              "a status page with genuine incident history. The weakness is "
              "everything you need when an integration runs unattended. No "
              "request id to quote when something goes wrong, no ETag to stop two "
              "jobs overwriting each other, no Retry-After to back off against, "
              "and no idempotency key on the call that files rent payments to the "
              "credit bureaus. Budget for defensive code: log your own "
              "correlation ids, serialize your writes, deduplicate webhooks "
              "yourself, and parse what the API actually returns rather than "
              "trusting the published rent-reporting schema."),
    (5, 5, "The best part of the API and the reason it is safe to automate "
           "against at all. You can mint a key that is read-only and limited to a "
           "single owner's property group, hand it to an agent, a reporting tool "
           "or a third party, watch it in a list with the date and the person who "
           "made it, and kill it with one toggle. There is also a real sandbox "
           "with its own credentials that cannot reach the credit bureaus. One "
           "boundary worth knowing: owner scoping does not reach Boom's own "
           "billing objects, so a read-only key can still see your Boom invoices "
           "and your payout account details. Scope by what the key is for, and do "
           "not treat read-only as harmless."),
    (3.1, 5, "Point your developer, or your coding assistant, at the OpenAPI file "
             "on GitHub rather than the documentation site's endpoint pages. The "
             "screening spec is accurate, current and complete enough to generate "
             "a working client. The rent-reporting half will cost you a day of "
             "trial and error: its spec points at the sandbox host, describes "
             "form-encoded bodies the live API does not use, and calls numbers "
             "and booleans strings. All thirteen endpoint pages in the docs "
             "navigation have pointed at a developer's dead tunnel since March "
             "2024. The same warning applies to AI tools, because the AI-readable "
             "corpus looks authoritative and will quietly hand an agent an "
             "endpoint list that does not exist. The redeeming feature is that "
             "Boom clearly maintains this: the changelog is weekly and the spec "
             "repo was updated a week before the run."),
    (11.3, 15, "If you are already a Boom customer you are minutes from a working "
               "key: Settings, API, name it, pick read-only if that is all you "
               "need, save. Nobody to ask and no ticket to file. What you cannot "
               "find out from anything Boom publishes is what it costs. There is "
               "no pricing page anywhere and every pricing question routes to a "
               "sales form, so while nothing evidences a premium gate, nothing "
               "establishes that API access is included or free either. Confirm "
               "in writing that API use carries no charge before you build a "
               "dependency on it, and expect to email Boom if you want a sandbox "
               "to develop against."),
  ],
  "strengths": [
    "Read-only keys scoped to specific owners or property groups, which is unusual in this category",
    "Multiple named keys with creator and date, each revocable by you with one toggle",
    "A real sandbox with separate credentials that cannot reach the credit bureaus",
    "The whole screening funnel is scriptable, from lead to decision to PMS push",
    "A public status page with 11 components and nine resolved incidents",
    "A weekly changelog current to the day before the run, plus a spec repo with dated commits",
    "The screening OpenAPI spec is accurate and complete enough to generate a working client",
    "Pagination with real total counts, verified repeatable and non-overlapping live",
  ],
  "watch": [
    "No pricing published anywhere, so you cannot tell what API access costs",
    "The rent-reporting spec disagrees with the live API on rent amounts, booleans and arrays",
    "All thirteen endpoint pages in the docs point at a developer's dead tunnel from March 2024",
    "No idempotency on the call that files rent payments to three credit bureaus",
    "No concurrency control, so two jobs can silently overwrite each other",
    "No request id on any successful response, so there is nothing to quote to support",
    "No Retry-After on any response, even though a 429 is documented",
    "No lease record, no document upload and no e-signature anywhere in the API",
    "No endpoint reverses a decision, though a person can undo one in the portal",
    "Owner scoping does not cover billing, so a read-only key can still read payout account details",
  ],
  "bottom": "You can build real automation on the screening half today: pull "
            "applications with their credit, criminal, eviction and income "
            "reports, decide with your own criteria, and push approved applicants "
            "into your PMS. You can enroll residents in rent reporting too. But "
            "there is no lease record, no document upload and no e-signature "
            "anywhere in this API, so approval is where Boom stops and your "
            "system of record begins. Its biggest strength is access control: "
            "read-only keys scoped to a single owner's property group, plus a "
            "sandbox that cannot touch the credit bureaus, make this genuinely "
            "safe to hand to an AI agent or an outside vendor. Its biggest "
            "limitation is that the rent-reporting half is unreliable to build "
            "against. The published schema disagrees with what the endpoint "
            "actually returns on rent amounts and booleans, the documentation's "
            "endpoint pages have pointed at a dead developer tunnel since March "
            "2024, and there is no request id, concurrency control, retry "
            "guidance or idempotency key for unattended jobs. Boom is not a bank, "
            "no first-party material names any bank, processor or money "
            "transmitter behind it, and it documents no trust-accounting, "
            "client-fund, security-deposit or escrow workflow. Its financial "
            "endpoints concern Boom's own billing to you, not money you hold for "
            "owners. The score reflects a narrow API with unreliable "
            "documentation rather than a weak product: treat Boom as a screening "
            "and credit-reporting layer beside your PMS, your trust accounting "
            "and your bank rather than a replacement for any of them.",
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
    (5, 5, "A perfect score. Issue a "
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
              "$400 a month, above Essential at $62 and Growth at $192. On those two "
              "plans the run found no API access."),
  ],
  "strengths": [
    "The most complete object coverage of any API graded so far",
    "A real sandbox, with keys that cannot reach production data",
    "Read-only and per-resource scoped keys, self-serve",
    "91 webhook event types across 32 entities",
    "Changelog running monthly since 2020",
  ],
  "watch": [
    "Buildium's pricing page lists the API as Premium-plan only, $400/month",
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
  "score": 85, "grade": "B",
  "meta": {"run": "Sep 2, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Fully verified, sandbox", "raw": "42.50 / 50"},
  # Column sponsors this page, so this note leads with the audit trail rather
  # than the score. The decisive fact is that reconciliation went AGAINST the
  # sponsor: both blind graders would have published an A and the run held a B.
  "note": "Column sponsors this report, and this row has been through six "
          "independent grading runs, more than any other platform here. The first "
          "three graded a frozen evidence packet blind and scored 85, 95 and 92. "
          "Column then sent a written clarification, it was added to the packet, "
          "and three further blinded runs scored 85, 86 and 86. The published 85 "
          "is the reconciled result. The counterintuitive part is worth saying "
          "plainly: more information moved graders toward the stricter mark, not "
          "away from it. The only two runs that passed Column on commercial "
          "gating were the two that had not read Column's statement, and all "
          "three that did read it marked it partial. Three reasons converged. The "
          "methodology requires a publicly auditable citation for a pass, and "
          "private correspondence is not one. The statement addresses the cost of "
          "API access but not the separate finding that several capabilities need "
          "Column to switch them on per platform. And on the reserve, the "
          "statement confirms that a funded reserve is required and disputes only "
          "how it is sized. One reading stays legitimate and is recorded rather "
          "than averaged away: a grader who takes gated to mean strictly a "
          "purchasable plan ladder would pass it, producing 93 and an A. Worth "
          "crediting Column for the outcome anyway: without their statement there "
          "was no first-party evidence either way on cost, the check would have "
          "been unverified, and the whole score would have been withheld.",
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
    (5, 5, "A perfect score, and the category that matters most if you ever point "
           "an AI agent at a bank account. You can mint a key that reads balances "
           "and nothing else, or one that pays vendors by ACH but is structurally "
           "incapable of sending a wire, scoped to a single account. You can "
           "require a human to approve transfers from a given key, issue one key "
           "per tool, and kill any of them instantly. With a sandbox that behaves "
           "like production, you can build something risky without it ever "
           "touching real money."),
    (3.8, 5, "If you hand Claude or ChatGPT the job of writing your Column "
             "integration, it has unusually good material: the entire "
             "documentation as one clean file built for AI tools, plus a full "
             "machine-readable spec. The catch is accuracy rather than coverage, "
             "and it is why this is not a higher mark. A webhook guide prints a "
             "URL that returns 404, three response examples show a status value "
             "in the wrong case, the error table promises a 404 the API never "
             "sends, and one endpoint listed as supporting idempotency is not in "
             "the spec at all. Build from the API reference pages rather than the "
             "narrative guides, and verify against the sandbox rather than "
             "trusting an example."),
    (11.3, 15, "The sandbox is free, self-serve and a complete copy of the "
               "bank, which is unusually generous, and Column has confirmed in "
               "writing that the API itself is free in both sandbox and "
               "production. Two things hold this short of full marks. Production "
               "is not self-serve, and several capabilities, including positive "
               "pay and interest-bearing accounts, need Column to enable them for "
               "your platform. And if you want Column to originate the ACH debits "
               "that pull rent, it requires a funded, locked reserve. Column's own "
               "going-live guide says that reserve must exceed your rolling 60-day "
               "debit volume, while two other pages in the same documentation "
               "describe a Column-determined percentage; Column confirms the "
               "latter is correct, so get your number from them rather than the "
               "guide."),
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
    "Documentation drift: a 404 URL, wrong-case examples, a phantom endpoint",
    "Direct ACH debit origination needs a reserve balance, sized case by case",
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
             "sales call. On the gating question the run relied on the operator "
             "confirming the REST surface they use is available on their own plan, "
             "plus LeadSimple's pricing page gating no API rows by plan. LeadSimple "
             "does market an Enhanced API access tier for higher rate limits, so "
             "confirm your own plan rather than assuming this one."),
  ],
  "strengths": [
    "Gained 9 points by shipping fixes to its two weakest categories",
    "Read-only keys, multiple named keys, and per-key revoke, all self-serve",
    "Public OpenAPI 3.0 spec and reference, no login required",
    "Full coverage of contacts, deals, and processes, with webhooks",
    "The operator confirmed the REST surface they use is on their plan",
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
              "in seconds without talking to anyone. Property Meld's pricing page "
              "lists API access under Miscellaneous as Ops only, and prices Ops "
              "at $2.00 per unit per month against Core at $1.60. What that "
              "difference costs a Core customer in practice was not established "
              "by the run."),
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

"QuickBooks Online": {
  "score": 64, "grade": "D",
  "meta": {"run": "Sep 2, 2026", "method": "1.1", "model": "Claude Fable 5",
           "tier": "Baseline verified", "raw": "32.04 / 50"},
  # Sits under Xero in the same category, which is the comparison that matters:
  # 64 against 80 for two general-ledger platforms on the same rubric.
  "note": "Graded three independent times against the same frozen evidence, with "
          "every disagreement resolved against that evidence before scoring and "
          "none left open. Worth knowing how coverage was judged here, because it "
          "was generous rather than harsh: the run scored property-management "
          "objects by their accounting equivalents, counting tenants as "
          "Customers, properties as Classes or Departments, and the lease ledger "
          "as AR transactions. That mapping is why objects a PMS would have "
          "natively are marked present or partial here rather than absent. Writes "
          "were "
          "exercised in an Intuit sandbox company; only the webhook delivery step "
          "could not be run, because subscriptions are configured in the portal "
          "and need a public endpoint.",
  "cats": [
    (7.5, 15, "Everything the ledger runs on is fully readable and writable, and "
              "the write path was exercised live in a sandbox company. The "
              "problem is fit. Property-management concepts exist only as "
              "accounting workarounds: units are sub-classes or sub-customers, a "
              "lease is a recurring-transaction proxy, and work orders have no "
              "equivalent at all. Reconciliation status is invisible to the API, "
              "so you cannot tell from code whether an account has been "
              "reconciled."),
    (9.2, 10, "The highest Design and Reliability score on this board, and by a "
              "clear margin. Automations get signed webhooks with a documented "
              "retry ladder, duplicate suppression that was proven live, "
              "optimistic locking that actually rejected a stale write, trace ids "
              "on every response, and a real status page with a status API. The "
              "rough edges are legacy conventions, with create, update, delete "
              "and void all going through POST, and a thin version-compatibility "
              "contract."),
    (3.5, 5, "The weak point for anyone automating. The Accounting API has "
             "exactly one scope, and it grants read and write together, so you "
             "cannot hand an integration or an AI agent a key that reads your "
             "books without also being able to post journal entries to them. You "
             "do get multiple apps with separate credentials, self-serve "
             "revocation, and genuinely isolated sandbox companies."),
    (4.4, 5, "A developer or an AI coding tool can build against this from public "
             "documentation alone: a complete per-entity reference with worked "
             "request and response samples, maintained SDKs for Java, .NET and "
             "PHP, and four dated release-note streams. The gap is AI retrieval. "
             "There is no llms.txt and no downloadable corpus, so an AI tool has "
             "to scrape page by page rather than ingest the whole thing."),
    (7.5, 15, "You can build against a sandbox today for free, and the core "
              "Accounting API is included with any QuickBooks Online "
              "subscription. Two things hold it back. Development keys are "
              "instant, but production credentials go through an Intuit "
              "questionnaire and its approval. And Intuit's premium-APIs page "
              "lists Projects, the 12-field Custom Fields API, Sales Tax, "
              "Dimensions and Payroll Compensation as requiring Silver, Gold or "
              "Platinum partner tiers."),
  ],
  "strengths": [
    "The highest Design and Reliability score on the board, 9.2 out of 10",
    "Optimistic locking that works: a stale-token write was rejected live",
    "Duplicate suppression proven live, two identical creates returned one record",
    "Signed webhooks with a documented retry ladder from 10 seconds to 6 hours",
    "Public status page with per-service 90-day uptime and a status API",
  ],
  "watch": [
    "One scope for the whole Accounting API: any key you issue can post entries",
    "No property, unit, lease, work-order or reconciliation objects",
    "Production credentials need Intuit to approve a questionnaire",
    "Minor versions 1 to 74 were retired at once, and old pins are now ignored",
    "No llms.txt or downloadable corpus, so AI tools scrape page by page",
  ],
  "bottom": "You can build real automations on this API today: read and post "
            "anything on the ledger, get signed webhooks when data changes, sync "
            "full datasets incrementally, and retry writes safely thanks to "
            "duplicate suppression that was proven live. The engineering "
            "fundamentals are genuinely strong, and the Design and Reliability "
            "score is the best on this board. What drags the grade down is fit "
            "and access. There are no property, unit, lease, work-order or "
            "reconciliation objects, so QuickBooks Online can only ever be the "
            "general-ledger layer behind a PMS, and the all-or-nothing read and "
            "write scope means any integration or AI agent you connect can write "
            "to your books. It is not a substitute for a PMS or a trust-"
            "accounting system, and nothing in the API evidences trust or "
            "fiduciary workflows.",
},

"RentEngine": {
  "score": 75, "grade": "C",
  "meta": {"run": "Sep 3, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Baseline verified", "raw": "37.54 / 50"},
  # Third RentEngine run: 74 (Aug 27) -> 78 (Sep 1) -> 75 (Sep 3). Three of the
  # five categories went UP this time and the total still fell, because this run
  # adopted the methodology's default leasing classification verbatim and fixed
  # it in writing before looking at the API. Under that classification the
  # critical objects are applications, screening and lease lifecycle, and all
  # three are read-only. The write surface RentEngine does have sits outside the
  # classified core, so it cannot be counted toward it.
  "note": "This replaces the 2026-09-01 run that scored 78 (C+), which itself "
          "replaced a 2026-08-27 run that scored 74. Worth understanding why the "
          "number went down when the API got better. Three of the five categories "
          "improved: Design and Reliability 7.1 to 7.9, Access Control 3.0 to "
          "4.0, and Documentation 4.4 to a perfect 5.0. What fell is functional "
          "coverage, 9.4 to 5.6, and that is a grading change rather than a "
          "product change. This run adopted the methodology's default "
          "leasing-and-screening classification word for word and committed it to "
          "a file before the API was examined. Under it the critical objects are "
          "applications, screening decisions and the lease lifecycle, and all "
          "three are read-only. RentEngine's real write surface, units, prospects, "
          "showings, lockboxes and notes, sits outside that classified core, so "
          "the rubric cannot count it there. Two other things belong on the "
          "record. RentEngine sent a written response to the earlier report card, "
          "and the run used it only to decide where to look: no check was marked "
          "on the vendor's say-so, and every mark cites first-party documentation "
          "or a live observation. And three showing endpoints the vendor said "
          "would ship that afternoon returned 404 when the evidence was frozen, so "
          "they were not credited.",
  "cats": [
    (5.6, 15, "You can see everything and change almost nothing that matters most "
              "in a leasing tool. Reading is excellent: applications, screening "
              "status, the whole funnel, and rich webhooks that tell you the "
              "moment an application is approved or a lease is signed. But you "
              "cannot submit an application, record a screening decision, approve "
              "or reject an applicant, or move a prospect through a lease stage "
              "from your own code. RentEngine says this is deliberate and "
              "compliance-driven for screening, which is a fair reason, but the "
              "effect on what you can build is the same: your automations can "
              "watch and report, not decide and act."),
    (7.9, 10, "The strongest part of the API and genuinely well built. Errors are "
              "machine-readable, rate limiting degrades cleanly with a Retry-After "
              "you can obey, every response is traceable to a log id you can quote "
              "to support, and the versioning promise is written down with 30 days "
              "notice before a breaking change. Three gaps will cost you "
              "engineering time: no documented ordering on paged lists, so a long "
              "sync while records change can miss or repeat rows; no bulk export, "
              "so a full extract means paging everything; and webhooks that are "
              "not cryptographically signed, so you cannot prove a payload is "
              "genuine, only that the caller knew a static secret."),
    (4.0, 5, "The basics are covered. You can mint several keys, hand an "
             "integration a read-only one, and kill any of them yourself in "
             "seconds. Two things to plan around. A key is only ever as narrow as "
             "the user who made it, so create API keys from a purpose-built "
             "limited user rather than from your own admin login. And staging "
             "exists on paper but is not documented well enough to trust as a "
             "rehearsal space, and it is running behind production, so treat "
             "production as your only real environment and test carefully."),
    (5.0, 5, "Full marks, and the reason a project here is predictable to scope. "
             "Everything a developer or an AI coding tool needs is public, "
             "current, and machine-readable: a real OpenAPI 3.1 file you can "
             "generate a client from, an llms.txt, and a live documentation server "
             "an AI agent can query directly. The changelog was updated the "
             "morning this was run. If you hand this API to a contractor or to an "
             "AI coding assistant, they will not be guessing."),
    (15, 15, "No barrier at the door. If you are a RentEngine customer the API is "
             "part of what you already pay for, and you can issue yourself a key "
             "in under a minute without asking anyone. This is the cleanest "
             "possible result on access, and it is worth noting that this category "
             "carries the same 15-point weight as functional coverage."),
  ],
  "strengths": [
    "A perfect documentation score: public OpenAPI 3.1, an llms.txt, and a first-party docs server an AI agent can query",
    "Changelog updated the morning of the run, with the served spec version matching",
    "A written promise of 30 days notice before any breaking change",
    "Read-only keys, multiple named keys, and self-serve revoke",
    "Machine-readable error codes, verified live on four separate error classes",
    "Rate limiting that degrades cleanly: a real Retry-After plus remaining and reset headers",
    "API access included in the standard plan, with a self-serve key in under a minute",
  ],
  "watch": [
    "Applications and screening are read-only: no submit, no approve, no reject",
    "Lease stage advance is unit status only; the events endpoint accepts 2 of 45 event types",
    "No DELETE verb exists anywhere in the API",
    "Webhooks are unsigned; verification is an optional static shared secret",
    "No bulk export, and the updated-since filter reaches only three of roughly twenty list endpoints",
    "No documented ordering on paged lists, so a long sync can skip or repeat rows",
    "No concurrency control: two writers to the same unit are last-write-wins",
    "Keys inherit the creating user's permissions, with no per-resource scoping",
    "One endpoint bills you: the market comps call is metered at $0.50 per successful request",
  ],
  "bottom": "Today you can build reliable read-and-report automation on RentEngine "
            "and very little else. Pull your units, prospects, showings, "
            "applications and screening outcomes, receive webhooks the moment an "
            "application is approved or a lease is signed, and push units, "
            "prospects, showings, lockbox codes and notes back in. What you cannot "
            "do from your own code is the part that decides anything: submit an "
            "application, obtain or record a screening decision, or approve, "
            "reject or advance an applicant. RentEngine says the screening path is "
            "deliberately closed for compliance, which is a legitimate reason, but "
            "the practical result is that your automations can watch and report "
            "while a human still clicks the buttons that matter. The API's biggest "
            "strength is craftsmanship everywhere except coverage: genuinely "
            "excellent documentation, a current OpenAPI spec, machine-readable "
            "errors, honest rate limiting, request ids you can quote to support, a "
            "written 30-day breaking-change promise, and no cost or sales barrier "
            "to getting a key. Its biggest limitation is that it is observational "
            "at its core, compounded by unsigned webhooks and no bulk export.",
},

"Process Street": {
  "score": 73, "grade": "C",
  "meta": {"run": "Aug 31, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Fully verified, controlled live", "raw": "36.25 / 50"},
  # Four entries are Fully verified (Column, Property Meld, Aptly, this one) and
  # several were graded three times, so neither is a distinguishing claim. What
  # IS unique: all eight battery steps run against a LIVE account. Column also
  # ran all eight, but in a sandbox.
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
               "the whole API works on the entry plan. The published plan matrix lists "
               "50 API calls a month on Startup, which would not support real "
               "automation. During this run about 90 calls went through on a "
               "Startup account with no payment-required error, so that cap was "
               "not enforced on that one organization; the run does not establish "
               "how it is applied generally. Confirm your own quota before building "
               "anything business critical, and note that scoped keys are "
               "Enterprise only."),
  ],
  "strengths": [
    "All eight live-test steps run against a live account, writes and a real webhook delivery included",
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

"Rentvine": {
  "score": 69, "grade": "D+",
  "meta": {"run": "Sep 2, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Baseline verified", "raw": "34.38 / 50"},
  # The widest category split on the board: 15/15 on access and 5/5 on access
  # control, against 2.5/10 on design and reliability. The report is explicit
  # that the grade measures engineering discipline, not the product.
  "note": "Graded three independent times. The runs scored 70, 70 and 69 and "
          "agreed on 24 of the 27 checks, including every check in four of the "
          "five categories. All three disagreements sat in Design and "
          "Reliability, all three were resolved against the frozen evidence "
          "rather than averaged, and all three moved the score down. The "
          "reconciled 69 matches the strictest run exactly. Two things about the "
          "evidence. Writes were tested live but only on one throwaway inventory "
          "record, created, updated and deleted with cleanup verified; the "
          "money-moving writes, posting a charge or a payment to a real trust "
          "ledger, were graded from documentation because the protocol forbids "
          "running them. And two checks in Functional Coverage cleared their "
          "threshold by about a point: object coverage scored 85.5% against an "
          "85% bar. The report records that a defensible stricter reading lands "
          "near 65 (D), and that one evaluator's alternative view of the ledger "
          "void question lands near 76 (C). The honest band is roughly 65 to 76.",
  "cats": [
    (9.4, 15, "The strongest part of the API and the reason it is worth building "
              "on. Essentially everything your business runs on is reachable: "
              "properties, units, leases, tenants, owners, work orders, bills, "
              "screening, and the full trust ledger, and most of it can be "
              "created and changed, not just read. Three gaps matter. The API can "
              "post money to a lease but cannot take it back: there is no way to "
              "void or reverse a charge or payment, even though Rentvine can void "
              "a bill or a deposit. You cannot post a journal entry or add a "
              "general-ledger account, so accounting corrections stay manual. And "
              "change notifications are lopsided, firing for properties, units, "
              "leases and work orders but never when money moves."),
    (2.5, 10, "This is where the API is weakest, and it is the part that decides "
              "how much maintenance your automations need. Paging through big "
              "lists works properly, and four export endpoints let you pull "
              "leases, properties, units and applications and then fetch only "
              "what changed. The problems are the unglamorous kind that cause 2am "
              "failures. Every number and yes-or-no value arrives as text, and "
              "Rentvine's own published blueprint says some of them are numbers, "
              "so code generated from it misreads your core records. Failures "
              "come back in five different formats, one of them a bare sentence "
              "and one a blank server error, and a missing property returns the "
              "wrong kind of error. No rate limit is published. Nothing stops a "
              "retried charge from posting twice, or two of your tools from "
              "silently overwriting each other on the same lease. There is no "
              "version contract and no status page."),
    (5, 5, "Full marks, and genuinely good news for anyone pointing an AI agent at "
           "their data. You can create a separate key for every tool you connect, "
           "give each one only the permissions it actually needs including "
           "view-only, and restrict it to part of your portfolio. The permissions "
           "are specific enough that Rentvine's own documentation names which one "
           "each operation needs, right down to Add Charge. If a vendor "
           "relationship ends or a key leaks, you regenerate the secret or delete "
           "the key yourself in seconds. The one real absence is a practice "
           "environment: there is no sandbox, so any testing happens in your live "
           "account."),
    (2.5, 5, "The documentation is better than most property management software "
             "offers and it is completely public, with no login and no sales "
             "call, and each endpoint explains what it is for and which "
             "permission it needs. But it is not something to hand an AI coding "
             "tool and trust blindly. Parts of the API are missing from it "
             "entirely: bank accounts work but are undocumented, and webhooks are "
             "described only in the customer help articles. Some of what it says "
             "is wrong, including 26 endpoints it points developers at that do "
             "not exist. Expect a developer or an AI assistant to get roughly 80% "
             "of the way from the docs and to discover the rest by testing "
             "against your live account."),
    (15, 15, "Full marks, and this is the check most property management vendors "
             "fail. You are already paying for the API. It is in the one plan at "
             "no extra cost, with no premium tier to unlock and no integration "
             "fee, and you can issue your own key in about two minutes without "
             "asking anyone. For an operator who wants to build their own tools, "
             "getting in the door immediately and at no marginal cost is worth a "
             "great deal."),
  ],
  "strengths": [
    "One plan with the API included, and a self-serve key in about two minutes",
    "Action-level key permissions, including view-only, restrictable to part of your portfolio",
    "The full trust ledger is reachable, alongside properties, units, leases, tenants, owners and work orders",
    "A public OpenAPI 3.1 spec with no login, naming the permission each operation requires",
    "Pagination that works, with eight populated headers and live-verified page traversal",
    "Four export endpoints with an updated-since filter, live-verified",
    "A first-party MCP server included in the plan, though still in beta and read-only",
  ],
  "watch": [
    "The API can post a charge or payment to a lease but cannot void or reverse one",
    "No journal-entry posting and no chart-of-accounts writes, so corrections stay manual",
    "No idempotency anywhere, so a retried charge can post twice to a real trust ledger",
    "Numbers and booleans return as text, and the published spec declares some of them numbers",
    "Five error formats, including one unparseable and one empty server error",
    "No published rate limit and no rate-limit headers of any kind",
    "No concurrency control, so two tools can silently overwrite each other on the same lease",
    "No API version contract, and the terms allow changes at any time without notice",
    "No status page: status.rentvine.com is an application portal, not an availability signal",
    "Webhooks cover four object types and nothing on the money side",
  ],
  "bottom": "Rentvine's API is genuinely open in the way that matters most: it is "
            "included in the one plan at no extra cost, you can issue your own key "
            "in two minutes without a sales call, and the permission controls are "
            "excellent, with a separate least-privilege key for every tool or AI "
            "agent, revocable in seconds. Its functional reach is real too. "
            "Properties, units, leases, tenants, owners, work orders, bills, "
            "screening and the full trust ledger are all reachable, and most of it "
            "is changeable. What you can build today is substantial: nightly "
            "portfolio syncs, custom dashboards and reporting, renewal and "
            "delinquency tracking, maintenance automation, and AI assistants that "
            "read your live data. What you cannot build safely today is anything "
            "that posts money unattended. The API will post a charge or payment to "
            "a lease but offers no way to void or reverse one, no protection "
            "against a retried request posting twice, and no journal-entry posting "
            "for corrections. That work belongs in the web application with a "
            "human. The score is held down not by what the API can do but by the "
            "guarantees it does not make: text-typed numbers that contradict the "
            "published schema, five error formats including two that cannot be "
            "parsed, no published rate limit, no way to stop two tools overwriting "
            "each other, no export or change filter for work orders and bills, no "
            "version contract, and no status page. Integrations here need more "
            "babysitting than the feature list suggests. Rentvine is a "
            "property-management system of record with documented trust-accounting "
            "workflows, and it is not a bank: it accounts for money held in trust "
            "accounts you open in your own name at your own institution, so you "
            "still need that bank, a payment processor, and the web application "
            "for corrections the API cannot make. A D+ is a grade for API "
            "engineering discipline, not a verdict on the product. On openness and "
            "cost of entry, where most competitors fail outright, Rentvine scores "
            "full marks.",
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
    (5, 5, "A perfect score, and about as safe as it gets to hand to an app or an "
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

"ShowMojo": {
  "score": 51, "grade": "F",
  "meta": {"run": "Sep 2, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Baseline verified", "raw": "25.63 / 50"},
  # Widest three-run spread on the board so far: 62 / 51 / 54. The discovering
  # evaluator was the outlier on five of the six splits and generous on every
  # one of them, which the report calls out as its own systematic bias rather
  # than averaging it away.
  "note": "Graded three independent times. The runs scored 62, 51 and 54 before "
          "reconciliation and agreed on 21 of the 27 checks; the six splits were "
          "each resolved against the frozen evidence rather than averaged, "
          "landing on 51. The report records that the discovering evaluator was "
          "the outlier on five of those six and generous in every case. The F "
          "holds across every combination of the unresolved positions, which "
          "move the score only within roughly 50 to 55. Two caveats worth "
          "knowing. The account owner declined live write testing in advance, so "
          "four checks were graded from ShowMojo's documentation rather than "
          "observed, and no write, import or webhook-registration call was made "
          "at any point. And one check is unverified: whether an account can "
          "hold several separately revocable tokens, because that page is behind "
          "a login. Resolved either way, the grade stays F.",
  "cats": [
    (1.9, 15, "You can push listings into ShowMojo from your PMS and pull leasing "
              "activity back out in bulk. Beyond that the API does not let you "
              "operate the product. Every showing action your staff performs all "
              "day, confirm, cancel, reschedule, mark a no-show, is something the "
              "API will tell you happened and will not let you cause. There is "
              "also no way to create or update a lead. And because listings have "
              "no updated-since filter and no webhook of their own, detecting "
              "that a listing changed means re-pulling the whole collection."),
    (6.7, 10, "The strongest category, and the parts that exist are mostly well "
              "built: clean typing that matched live responses field for field, "
              "an honest status page, a request id on every response, and an "
              "export that genuinely honors date ranges. The operational gaps are "
              "what bite in production. No rate limit is documented and 60 rapid "
              "requests returned no rate-limit headers at all, so you cannot tell "
              "what the ceiling is or what happens when you hit it. The main "
              "listings call returns everything in one unbounded response. A "
              "failed authentication hands your code an empty body instead of an "
              "error."),
    (0.8, 5, "The weakest area and the one with real risk attached. There is "
             "exactly one kind of key, it can do everything the API can do "
             "including overwriting your entire listing portfolio, and the "
             "account owner confirmed there is no read-only option. So if you "
             "want to give a contractor, a vendor or an AI agent access to read "
             "your showing data, the only credential you can hand over is one "
             "that can also rewrite your listings. You can generate a fresh token "
             "yourself, but nothing documents that doing so kills the old one."),
    (1.3, 5, "A developer can read the listings and properties documentation and "
             "build against it. Pointing an AI coding assistant at it is another "
             "matter: no OpenAPI spec, no SDK in any language, no MCP server, and "
             "no llms.txt. The endpoint details are client-rendered, so fetching "
             "a documentation page returns prose with the parameter and schema "
             "tables missing, which is exactly how a coding tool reads a page. "
             "The report export, the highest-value data path, publishes no column "
             "documentation at all."),
    (15, 15, "Full marks. Credential creation is self-serve, with no sales call, "
             "support ticket or approval step. The pricing page itemizes every "
             "other add-on, down to per-device hardware fees, and never lists the "
             "API as a tier feature or upsell. This single category accounts for "
             "nearly two-thirds of the points ShowMojo earned."),
  ],
  "strengths": [
    "Self-serve token in settings, on any plan, with no API add-on or upsell",
    "Eight named bulk exports in JSON or CSV, with date filtering that works",
    "A webhook enumerating 120-plus lead and showing events, with a documented retry ladder",
    "Precisely typed listing schema that matched live responses field for field",
    "Public status page with uptime percentages and a real dated incident history",
  ],
  "watch": [
    "One all-powerful token: no read-only option, no scoping, no documented revocation",
    "No API endpoint confirms, cancels, reschedules or no-shows a showing",
    "No way to create or update a lead through the API",
    "Listings ignore page, per_page and every updated-since parameter tested",
    "Webhooks authenticate with a replayable static bearer token, not a signature",
    "No rate limit documented anywhere, and no rate-limit headers returned under load",
    "No OpenAPI spec, no SDK, no MCP server, and no AI-readable documentation",
    "The support knowledge base ShowMojo's own links point to is dead, returning HTTP 402",
  ],
  "bottom": "ShowMojo's API is a one-way street, and you should plan around that. "
            "You can push your listings in and pull your leasing activity back "
            "out, leads, showings, no-shows, pre-screening answers, lockbox "
            "access and performance metrics, all date-filterable in JSON or CSV. "
            "What you cannot do is make ShowMojo act. There is no way to confirm, "
            "cancel or reschedule a showing through the API, and no way to create "
            "or update a lead, so the automations most operators actually want "
            "are not buildable today. What you can build is good reporting, a "
            "warehouse sync, and real-time reaction to leasing events, because "
            "the webhook coverage of showing and prospect activity is genuinely "
            "thorough and the export path works exactly as documented. Two "
            "limitations do most of the damage. Access control: one kind of key, "
            "not scopable, not read-only, able to overwrite your whole listing "
            "portfolio. And listing sync: no updated-since filter, no listing "
            "webhook, no pagination on the listings call, so noticing that a "
            "listing changed means re-pulling everything. Against that, the thing "
            "ShowMojo gets clearly right is access. No sales call, no upgrade, no "
            "approval, and that alone accounts for nearly two-thirds of the "
            "points it earned. Read the score for what it measures. This grades "
            "how buildable the API is for an operator, not whether the product "
            "does its job.",
},

"Tenant Turner": {
  "score": 51, "grade": "F",
  "meta": {"run": "Sep 1, 2026", "method": "1.1", "model": "Claude Opus 5",
           "tier": "Baseline verified", "raw": "25.42 / 50"},
  # Sits directly under RentEngine in the same category, which is the comparison
  # that matters: 51 against 75 for two leasing tools graded on the same rubric.
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
    (15, 15, "Full marks. Nothing "
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
                f'<td class="plat">'
                f'<a class="co-btn" href="api-grader-{slug(co)}.html">'
                f'<span class="co-name">{co}</span>{flag}'
                f'<span class="co-hint">Full report &rarr;</span></a></td>'
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


# =============================================================================
# SHARED COPY  -  edit here, it changes everywhere
#
# The preview banner, the correction callout and the rerun disclosure appear on
# the index and on all 15 vendor pages. Andrew said the wording is not locked, so
# every page renders from these strings rather than carrying its own copy. Change
# a line here, rerun the build, and all 16 pages move together.
# =============================================================================

CONTACT = "mailto:peter@rlpmg.com?subject=API%20Report%20Card%3A%20factual%20correction"

COPY = {
    # Thin bar across the top of every page.
    "banner_tag":  "Preview",
    "banner":      ("These are <b>pre-release scores</b>, not final grades. "
                    "Every vendor's full markdown report is published here so the "
                    "scoring can be checked line by line. A complete rerun follows "
                    "in roughly 60 days."),
    "banner_link": "Found a factual error?",

    # Long form. Used at the foot of the index and on every vendor page.
    "fix_head": "Found a factual error in your grade?",
    "fix_body": [
        "Tell us and we will fix it. Every mark on this page traces to a specific "
        "piece of first-party evidence or a live API call, and the full report is "
        "published so you can see exactly what was checked and what it was checked "
        "against.",
        "<strong>Confirmed factual errors are corrected immediately, in real time.</strong> "
        "If a mark rests on something that was wrong, out of date, or misread, that "
        "gets fixed as soon as it is verified, and the page says so.",
        "Everything else waits. We do not rescore piecemeal on request, because a "
        "board where some vendors have been re-run and others have not is not a fair "
        "comparison. Shipped improvements, changed documentation and disagreements "
        "about judgement all go into the next full rerun.",
    ],
    "fix_cta":  "Email peter@rlpmg.com",

    # The rerun policy, stated once.
    "rerun_head": "Preview scores, and what happens next.",
    "rerun_body": [
        "This is a pre-release. It is published now, before it is finished, because "
        "the fastest way to find a bad score is to show it to the people who know the "
        "product. Feedback on the methodology itself is as welcome as feedback on the "
        "facts.",
        "Every graded platform gets its complete markdown report published up front, "
        "so any vendor can see precisely how the score was reached rather than "
        "arguing with a number.",
        "<strong>A full rerun of every platform follows in roughly 30 to 60 days</strong>, "
        "against the same rubric, at the same time. That refreshed board is then "
        "expected to hold for six to twelve months before the next update.",
    ],
}


def banner_html(here=""):
    link = CONTACT if here else "#correct"
    return (
        '<div class="pre-bar">\n  <div class="wrap">\n'
        f'    <span class="pre-tag">{COPY["banner_tag"]}</span>\n'
        f'    <span>{COPY["banner"]} '
        f'<a href="#correct">{COPY["banner_link"]}</a></span>\n'
        '  </div>\n</div>'
    )


def fix_html():
    ps = "\n        ".join(f'<p>{p}</p>' for p in COPY["fix_body"])
    return (
        f'<div class="fix-note" id="correct">\n'
        f'        <h3>{COPY["fix_head"]}</h3>\n'
        f'        {ps}\n'
        f'        <a class="btn btn-primary" href="{CONTACT}">{COPY["fix_cta"]}</a>\n'
        f'      </div>'
    )


def rerun_html():
    ps = "\n        ".join(
        f'<p class="sub" style="margin-top:{14 if i else 12}px;">{p}</p>'
        for i, p in enumerate(COPY["rerun_body"]))
    return (f'<h2 class="h-lead">{COPY["rerun_head"]}</h2>\n        {ps}')


# =============================================================================
# PER-VENDOR PAGES
# =============================================================================

CHECKS_JSON = Path("data/checks.json")
SUB_TMPL_HEAD = Path("index.html")

# Category accent squares, matching the order of CAT_LABELS.
CAT_SQ = ["#2C7CB0", "#3f97cc", "#4bab8f", "#E0703C", "#e0a83c"]

MARK_LABEL = {"yes": "Yes", "partial": "Partial", "no": "No",
              "na": "N-A", "unverified": "Unverified"}


def load_checks():
    if not CHECKS_JSON.exists():
        raise SystemExit(
            "data/checks.json is missing. Run:  python3 extract-checks.py")
    return json.loads(CHECKS_JSON.read_text(encoding="utf-8"))


def code_up(s):
    """`foo` -> <code>foo</code>, after escaping. The reports use backticks
    heavily for endpoints and headers and they carry real meaning."""
    s = html_escape(s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


def html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def grade_letter_class(g):
    return "g-" + g[0].lower()


def build_switcher(current):
    """Every graded vendor, in board order, as a one-click strip. This is the
    thing the modal was actually good at, so it has to survive the move to pages."""
    out = ['<div class="rc-switch" aria-label="Other platforms">']
    for _, _, companies in CATEGORIES:
        for co in companies:
            r = RESULTS.get(co)
            if not r:
                continue
            cur = ' aria-current="page"' if co == current else ""
            out.append(
                f'<a href="api-grader-{slug(co)}.html"{cur}>'
                f'<span class="grade {grade_class(r["grade"])}">{r["grade"]}</span>'
                f'{co}</a>')
    out.append("</div>")
    return "\n        ".join(out)


def build_nextprev(current):
    order = [co for _, _, cos in CATEGORIES for co in cos if co in RESULTS]
    i = order.index(current)
    prev = order[i - 1] if i > 0 else order[-1]
    nxt = order[i + 1] if i < len(order) - 1 else order[0]
    return (
        '<div class="rc-nextprev">'
        f'<a href="api-grader-{slug(prev)}.html">&larr; {prev}</a>'
        f'<a href="api-grader-{slug(nxt)}.html">{nxt} &rarr;</a>'
        '</div>')


SUB_PAGE = """<!--
  PM API REPORT CARD - vendor detail page. GENERATED by build-report-card.py.
  Do not hand-edit: your changes are overwritten on the next build. Change the
  RESULTS entry, data/checks.json, or the SUB_PAGE template instead.
-->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex, nofollow" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preconnect" href="https://use.typekit.net" crossorigin />
<title>{name} API Report Card &middot; Peter Lohmann</title>
<meta name="description" content="{name} scored {score}/100 ({grade}) on the PM API Report Card. All 27 checks, the evidence behind each mark, and the full report." />
<link rel="icon" type="image/svg+xml" href="favicon.svg" />
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png" />
<link rel="apple-touch-icon" href="favicon.png" />
<link rel="stylesheet" href="https://use.typekit.net/dik1zcl.css" media="print" onload="this.media='all'" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" media="print" onload="this.media='all'" /><noscript><link rel="stylesheet" href="https://use.typekit.net/dik1zcl.css" /><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" /></noscript>
<link rel="stylesheet" href="styles.css?v=24" />
<link rel="stylesheet" href="report.css?v=1" />
<style>
  .grade{{ display:inline-flex; align-items:center; justify-content:center; min-width:44px;
          padding:5px 10px; border-radius:8px; font-weight:800; font-size:14px;
          font-variant-numeric:tabular-nums; }}
  .grade-a{{ background:#e7f5ee; color:#248a5c; }}
  .grade-b{{ background:var(--wash); color:var(--primary-dark); }}
  .grade-c{{ background:#fdf3e0; color:#9a6a1c; }}
  .grade-d{{ background:#fdeade; color:#a95a24; }}
  .grade-f{{ background:#fdeaea; color:#a63b3b; }}
  .band.wash .panel, .band.wash .card,
  .band.wash .rc-checks, .band.wash .fix-note{{ background:var(--card); box-shadow:var(--shadow); }}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DRCVXMNK1D"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-DRCVXMNK1D');</script>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<nav class="top" aria-label="Primary">
  <div class="bar">
    <a class="brand" href="https://www.peterlohmann.com/">Peter <span>Lohmann</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="navlinks">Menu</button>
    <div class="links" id="navlinks">
      <a href="https://www.peterlohmann.com/">About</a>
      <a href="https://www.peterlohmann.com/newsletter">Newsletter</a>
      <a href="https://www.peterlohmann.com/podcast">Podcast</a>
      <a href="https://www.peterlohmann.com/largest-pm-companies">Largest PM Companies</a>
      <a href="https://www.peterlohmann.com/blog">Blog</a>
      <a href="https://www.peterlohmann.com/report/">M&amp;A Report</a>
      <a href="https://www.peterlohmann.com/peterbot">PeterBot</a>
      <a href="https://www.peterlohmann.com/products">Products</a>
    </div>
    <a class="btn btn-navy btn-sm cta" href="https://www.peterlohmann.com/contact">Contact</a>
  </div>
</nav>

{banner}

<main id="main">

  <section class="band tight">
    <div class="wrap">
      <a class="rc-back" href="index.html#results">&larr; All platforms</a>
      <p class="rc-eyebrow">API Report Card &middot; {cat} &middot; Methodology v1.1</p>
      <h1 class="rc-title">{name}</h1>

      <div class="rc-slab">
        <div class="rc-score {gcls}">
          <div class="lab">Published grade</div>
          <div class="rc-gnum">
            <span class="letter">{grade}</span>
            <span class="num">{score}<i>/100</i></span>
          </div>
          <div class="raw">{raw} raw</div>
        </div>
        <div class="rc-meta">
          <div><div class="k">Evidence tier</div><div class="v">{tier}</div></div>
          <div><div class="k">Date run</div><div class="v">{run}</div></div>
          <div><div class="k">Evaluating model</div><div class="v">{model}</div></div>
          <div><div class="k">Verification coverage</div><div class="v">{cov}</div></div>
          <div><div class="k">Live-test battery</div><div class="v">{battery}</div></div>
          <div><div class="k">Checks</div><div class="v">{nchecks} of 27 scored</div></div>
        </div>
      </div>
    </div>
  </section>

  <!-- CATEGORY SCORES -->
  <section class="band tight wash">
    <div class="wrap">
      <h2 class="h-lead">Where the points came from.</h2>
      <p class="sub" style="margin:10px 0 22px;">Five categories, each worth a fixed share of the 100 points. A category earns the fraction of its checks it passes, times its maximum.</p>
      <div class="rc-where">
        <div class="rc-cats">
          {catcards}
        </div>
        <div class="rc-rule" aria-hidden="true"></div>
        <div class="rc-scale">
          <h3>Letter grades are absolute, never curved.</h3>
          <p>The same numeric bands apply to every platform. Nothing here is scored relative to the rest of the board.</p>
          {bands}
        </div>
      </div>
    </div>
  </section>

  <!-- PLAIN-LANGUAGE READ -->
  <section class="band tight">
    <div class="wrap">
      <h2 class="h-lead">What this means for you.</h2>
      <p class="sub" style="margin:10px 0 26px;">One paragraph per category, in plain language.</p>
      {reads}
    </div>
  </section>

  <!-- ALL 27 CHECKS -->
  <section class="band tight wash" id="checks">
    <div class="wrap">
      <h2 class="h-lead">Every check, and why it scored that way.</h2>
      <p class="sub" style="margin:10px 0 24px;">The same 27 checks are applied to every platform. What changes is which are N-A and what the core objects mean for that kind of software. Each mark below is quoted from the run's own report.</p>
      {checkblocks}

      <div class="rc-pair" style="margin-top:26px;">
        <div class="panel">
          <h2>What works</h2>
          <ul class="rc-list">{strengths}</ul>
        </div>
        <div class="panel">
          <h2>What to watch</h2>
          <ul class="rc-list">{watch}</ul>
        </div>
      </div>
    </div>
  </section>

  <!-- VERDICT + PROVENANCE, side by side -->
  <section class="band tight">
    <div class="wrap">
      <div class="rc-pair">
        <div class="panel">
          <h2>The bottom line for a property manager</h2>
          <p>{bottom}</p>
        </div>
        {notesec}
      </div>
    </div>
  </section>

  <!-- DOWNLOADS -->
  <section class="band tight wash">
    <div class="wrap">
      <h2 class="h-lead">Check it yourself.</h2>
      <p class="sub" style="margin:10px 0 22px;">Both files behind this page, in full.</p>
      <div class="rc-dl">
        <div class="card">
          <h3>{name}&rsquo;s full report</h3>
          <p>The complete markdown report this page is built from, including the evidence packet, the run metadata and every check in full.</p>
          {dlbtn}
        </div>
        <div class="card">
          <h3>The grading file</h3>
          <p>The exact rubric behind every score on this page. Same file, every platform. Run it yourself and compare.</p>
          <a class="btn btn-ghost" href="files/pm-api-report-card-methodology.md" download>Download the methodology</a>
        </div>
      </div>
    </div>
  </section>

  <!-- CORRECTIONS -->
  <section class="band tight">
    <div class="wrap">
      {fixnote}
    </div>
  </section>

  <!-- SWITCHER -->
  <section class="band tight">
    <div class="wrap">
      <h2 class="h-lead" style="font-size:clamp(22px,2.8vw,28px);">Compare another platform</h2>
      <p class="sub" style="margin:10px 0 16px;">Same rubric, same process, every one.</p>
      {switcher}
      {nextprev}
    </div>
  </section>

  <section class="band tight">
    <div class="wrap center">
      <p class="sponsor-note" style="justify-content:center;">
        Methodology inspired by <a href="https://saastr.ai/api-report-card" target="_blank" rel="noopener">SaaStr&rsquo;s AI Agent API Report Card</a>. Sponsored by <a href="https://column.com/property-management/?utm_source=peter-lohmann&amp;utm_medium=plm-api-grader" target="_blank" rel="noopener">Column</a>.
      </p>
    </div>
  </section>

</main>

<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="brand" style="font-weight:700;color:var(--navy);">Peter <span style="color:var(--primary);">Lohmann</span></div>
      <nav class="foot-links" aria-label="Footer">
        <a href="https://www.peterlohmann.com/">About</a>
        <a href="https://www.peterlohmann.com/newsletter">Newsletter</a>
        <a href="https://www.peterlohmann.com/podcast">Podcast</a>
        <a href="index.html">API Report Card</a>
        <a href="https://www.peterlohmann.com/contact">Contact</a>
      </nav>
    </div>
  </div>
</footer>

<script>
(function(){{
  var t=document.querySelector('.nav-toggle'),l=document.getElementById('navlinks');
  if(t&&l){{t.addEventListener('click',function(){{
    var o=t.getAttribute('aria-expanded')==='true';
    t.setAttribute('aria-expanded',String(!o)); l.classList.toggle('open',!o);
  }});}}
}})();
</script>
</body>
</html>
"""



def short(s, limit=46):
    """Trim a metadata line to its headline fact, on a word or clause boundary.

    The reports write these as full sentences ("100% (26 of 26 applicable checks
    verified; gate satisfied...)"). The slab wants the fact, not the sentence, and
    a blind character slice cuts words in half."""
    s = (s or "").strip()
    if not s:
        return "&ndash;"
    # Tidy what the reports write inconsistently: leftover bold markers, a space
    # before a percent sign, and a leading capital that varies run to run.
    s = s.replace("*", "").replace(" %", "%").strip()
    s = s[:1].upper() + s[1:]
    # Cut at the EARLIEST clause boundary, not the first one in list order:
    # "Steps 1-6 complete. Step 7 (idempotency)..." has a full stop before its
    # parenthesis, and checking "(" first kept the dangling "Step 7".
    cuts = [i for i in (s.find(sep) for sep in (". ", "; ", ";", "(", " - ", " \u2014 "))
            if 0 < i <= limit]
    if cuts:
        return s[:min(cuts)].strip(" .,;:")
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" .,;:") + "&hellip;"



# Letter bands, laid out three to a row so each letter family shares one, with F
# spanning the full width because it is a single open-ended band. Straight from
# the methodology; these are absolute and are never curved to the board.
GRADE_BANDS = [
    ("A+", "97-100"), ("A", "93-96"),  ("A-", "90-92"),
    ("B+", "87-89"),  ("B", "83-86"),  ("B-", "80-82"),
    ("C+", "77-79"),  ("C", "73-76"),  ("C-", "70-72"),
    ("D+", "67-69"),  ("D", "63-66"),  ("D-", "60-62"),
    ("F",  "below 60"),
]


def build_bands(grade):
    out = ['<div class="rc-bands" aria-label="Letter grade bands">']
    for g, rng in GRADE_BANDS:
        fam = "b-" + g[0].lower()
        wide = " f" if g == "F" else ""
        now = ' data-now="1"' if g == grade else ""
        lab = ' aria-current="true"' if g == grade else ""
        out.append(
            f'<div class="rc-band {fam}{wide}"{now}{lab}>'
            f'<span class="g">{g.replace("-", "&minus;")}</span>'
            f'<span class="r">{rng}</span></div>')
    out.append("</div>")
    return "\n        ".join(out)


def build_subpages(checks_data):
    """One standalone page per graded platform. Returns the count written."""
    written = 0
    for _, cat_heading, companies in CATEGORIES:
        for co in companies:
            r = RESULTS.get(co)
            if not r:
                continue
            cd = checks_data.get(co)
            if not cd:
                raise SystemExit(
                    f"{co} is on the board but absent from data/checks.json. "
                    f"Run:  python3 extract-checks.py")

            maxima = (r["legacy"]["maxima"] if r.get("legacy")
                      else [m for _, m in CAT_LABELS])

            # --- category cards -------------------------------------------
            cards = []
            for i, (p, _, _) in enumerate(r["cats"]):
                pct = float(p) / maxima[i] * 100
                cards.append(
                    f'<a class="rc-cat" href="#checks-c{i+1}">'
                    f'<div class="rc-cat-top">'
                    f'<div><div class="n">Category {i+1}</div>'
                    f'<h3>{CAT_LABELS[i][0]}</h3></div>'
                    f'<div class="p">{fmt_pts(p)}<i> / {maxima[i]}</i>'
                    f'<span class="go" aria-hidden="true">&rarr;</span></div>'
                    f'</div>'
                    f'<div class="rc-bar"><span class="{tier(p, maxima[i])}" '
                    f'style="width:{pct:.0f}%"></span></div>'
                    f'</a>')

            # --- plain-language read per category -------------------------
            reads = []
            for i, (p, _, txt) in enumerate(r["cats"]):
                reads.append(
                    f'<div class="rc-read">'
                    f'<h3>{i+1} &middot; {CAT_LABELS[i][0]}</h3>'
                    f'<div class="pts">{fmt_pts(p)} / {maxima[i]} points</div>'
                    f'<p>{txt}</p></div>')

            # --- the 27 checks, grouped by category -----------------------
            blocks = []
            for ci in range(1, 6):
                rows = [c for c in cd["checks"] if c["cat"] == ci]
                if not rows:
                    continue
                p, mx = r["cats"][ci - 1][0], maxima[ci - 1]
                body = []
                for c in rows:
                    body.append(
                        f'<div class="rc-chk">'
                        f'<div class="id">{c["id"]}</div>'
                        f'<div><h4>{html_escape(c["title"])}</h4>'
                        f'<p>{code_up(c["why"])}</p></div>'
                        f'<span class="mark m-{c["mark"]}">'
                        f'{MARK_LABEL[c["mark"]]}</span>'
                        f'</div>')
                blocks.append(
                    f'<div class="rc-checks" id="checks-c{ci}" '
                    f'style="margin-bottom:18px;">'
                    f'<div class="rc-chead">'
                    f'<span class="sq" style="background:{CAT_SQ[ci-1]}"></span>'
                    f'<h3>Category {ci} &middot; {CAT_LABELS[ci-1][0]}</h3>'
                    f'<span class="pts">{fmt_pts(p)} / {mx}</span></div>'
                    f'{"".join(body)}</div>')

            # --- the run note, when the report carries one ----------------
            note = r.get("note") or r.get("rescored")
            notesec = ""
            if note:
                notesec = (
                    '<div class="panel" style="border-left:4px solid var(--primary);">'
                    '<h2>About this run</h2>'
                    f'<p>{note}</p></div>')

            # --- the markdown download ------------------------------------
            md = Path(f"files/reports/{slug(co)}.md")
            if md.exists():
                dl = (f'<a class="btn btn-primary" href="files/reports/{slug(co)}.md" '
                      f'download>Download the {co} report</a>')
            else:
                dl = ('<span class="sub" style="font-size:14.5px;">'
                      'Publishing shortly.</span>')

            page = SUB_PAGE.format(
                name=co,
                cat=re.sub("&amp;", "&", cat_heading),
                score=r["score"], grade=r["grade"],
                gcls=grade_letter_class(r["grade"]),
                raw=r["meta"].get("raw", "&ndash;"),
                tier=r["meta"].get("tier", "&ndash;"),
                run=r["meta"].get("run", "&ndash;"),
                model=r["meta"].get("model", "&ndash;"),
                cov=short(cd["meta"].get("coverage")),
                battery=short(cd["meta"].get("battery"), 52),
                nchecks=len(cd["checks"]),
                catcards="\n        ".join(cards),
                bands=build_bands(r["grade"]),
                reads="\n      ".join(reads),
                strengths="".join(f"<li>{s}</li>" for s in r["strengths"]),
                watch="".join(f"<li>{s}</li>" for s in r["watch"]),
                notesec=notesec,
                bottom=r["bottom"],
                checkblocks="\n      ".join(blocks),
                dlbtn=dl,
                fixnote=fix_html(),
                switcher=build_switcher(co),
                nextprev=build_nextprev(co),
                banner=banner_html(co),
            )
            Path(f"api-grader-{slug(co)}.html").write_text(page, encoding="utf-8")
            written += 1
    return written


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
    checks_data = load_checks()
    html = PAGE.read_text(encoding="utf-8")

    results_block = f"""      {build_stats()}
      <p class="sub" style="margin-top:16px;font-size:14px;">Scores are point-in-time and tied to the evidence access date. Methodology v1.1.</p>

      <h2 class="h-lead" style="margin-top:46px;">The results.</h2>
      <p class="sub" style="margin:10px 0 18px;">Scores are point-in-time, based on first-party documentation and, where available, live testing. Open any graded platform for its own page: all 27 checks, the evidence behind each mark, and the full report to download.</p>

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

    # The per-vendor detail moved out of a modal and onto its own page, so the
    # blob the modal read from is no longer emitted. The marker stays put: it is
    # cheap, and it keeps the option of re-adding an inline preview later.
    html = re.sub(
        r"(<!-- DATA:START -->\n).*?(\s*<!-- DATA:END -->)",
        lambda m: m.group(1) + m.group(2),
        html, flags=re.S,
    )

    # Shared copy blocks, rendered into the index from the same strings the
    # vendor pages use, so the wording can only be changed in one place.
    for marker, blockfn in (("BANNER", lambda: banner_html()),
                            ("FIXNOTE", fix_html),
                            ("RERUN", rerun_html)):
        html = re.sub(
            rf"(<!-- {marker}:START -->\n).*?(\s*<!-- {marker}:END -->)",
            lambda m, f=blockfn: m.group(1) + "      " + f() + m.group(2),
            html, flags=re.S,
        )

    PAGE.write_text(html, encoding="utf-8")
    print(f"Wrote {PAGE}")
    print(f"  {sum(len(c) for _,_,c in CATEGORIES)} companies in "
          f"{len(CATEGORIES)} categories, {len(RESULTS)} graded")

    n = build_subpages(checks_data)
    print(f"Wrote {n} vendor pages: api-grader-<platform>.html")


if __name__ == "__main__":
    main()
