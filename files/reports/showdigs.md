# API Report Card: Showdigs API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 4.8 (claude-opus-4-8)
- Date run: 2026-09-10
- Provisional evidence-packet version or ID: PROV-1
- Final evidence-packet version or ID: FINAL-1 (frozen 2026-09-10)
- Evidence-discovery mode: tool-enabled discovery
- Evidence tier: **Baseline verified** (read-path live-tested; write-path documentation-graded)
- Live-write method and safety: none — writes documentation-graded (no sandbox; live-write unsafe: money-moving/communicating/publishing endpoints, and no delete-property rollback)
- Minimum live-test battery: read-path steps 1–5 complete; write-path steps 6–7 N-A (no sandbox, live writes declined for safety); step 8 (webhook delivery) documentation-graded
- Live tests performed: authenticate; read + paginate `/units` (page 1→2, per_page); read `/listings`; read `/webhooks/sample`; filtered `/coverage` query; deliberate 401/404/422 errors; response-header inspection
- Live tests not possible: write-path create/update/delete; idempotency replay; webhook registration + delivery
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8
- Category 3 evidence basis: operator first-party observation of the login-gated Business Settings → Integrations page (Claude-in-Chrome verification authorized but extension offline; screenshot pending as optional upgrade)
- Published number source: reconciled result of three independent grading runs on the frozen packet (Run 1 = 60/D-, Run 2 = 55/F, Run 3 = 54/F). Contested checks C1.4, C2.4, C4.2 resolved against the evidence — see "Three-run reconciliation." This is not an average.

## Final evidence packet manifest
- https://api.showdigs.com/docs/ — full API reference (Scribe), "Last updated: August 4, 2026"
- https://api.showdigs.com/docs.openapi — advertised OpenAPI spec → HTTP 500 (all Accept variants), 2026-09-10
- https://api.showdigs.com/docs.postman — advertised Postman collection → HTTP 404, 2026-09-10
- https://www.showdigs.com — product overview ("leasing automation platform", "all-in-one leasing CRM")
- https://www.showdigs.com/integrations — "Build your own integration with Showdigs API"; integration list
- https://www.showdigs.com/pricing — single tier $1.20/unit/month, $120 minimum, ~100-unit minimum
- https://help.showdigs.com/ and /en/categories/403520-integrations — help center; 10 integration articles, no API-token article
- app.showdigs.com/profile/business-settings/integrations — token retrieval location (login-gated; operator-described)
- Live API observations (2026-09-10), base URL https://api.showdigs.com/api/v1 : `/units`, `/units?page=2`, `/listings`, `/webhooks/sample`, `/coverage`, and deliberate-error responses; response headers captured
- Absence checks (2026-09-10): status.showdigs.com (no DNS); showdigs.statuspage.io (redirects to Atlassian marketing — no real status page); api.showdigs.com/llms.txt & /llms-full.txt (422); www.showdigs.com/llms.txt (redirect loop)

## Evidence-amendment log
- C2.5 (rate limits): added live header observation `X-RateLimit-Limit: 180`, `X-RateLimit-Remaining: 179` — not in documentation.
- C2.6 (pagination): added live `/units` paginator showing `total: 1549`, `last_page`, populated `next`/`prev` links (docs sample was a stripped paginator).
- C2.11 (traceability): added live header inspection — confirmed no request/correlation ID on responses.
- C2.2 (typing): added live confirmation that `bedrooms` is a string while `bathrooms` is numeric in both `/units` and `/listings`; webhook `phone`/`phone_number` key inconsistency.
- C2.3 (errors): added live 401/404/422 bodies confirming `message` + Laravel `errors{}`, no machine code.
- C2.12 (status): added negative checks confirming no first-party status/uptime page.
- C3.1–C3.4: added operator first-party statement that the Integrations page offers no read-only, scoping, multiple-key, or rotation/revocation controls.

## API eligibility
- Qualifying API: **yes**
- API operator: Showdigs (Showdigs, Inc.) [api.showdigs.com/docs/ "Showdigs API"; www.showdigs.com/integrations "Build your own integration with Showdigs API"]
- Access or credential issuer: Showdigs, self-serve via account Business Settings → Integrations [api.showdigs.com/docs/ "Authenticating requests": "You can retrieve your token by visiting your integrations settings page."]
- Eligibility basis: A first-party REST API at `https://api.showdigs.com/api/v1` exposes Showdigs' own functions (units, listings, inquiries, condition reports, properties, webhooks), authenticated with a Showdigs-issued Bearer token; confirmed live with the operator's production credential on 2026-09-10.

## Context
- Software category: **Leasing tool** — specifically a leasing-*showing* / funnel-automation subtype.
- What the API is for and its core objects and workflows: The API lets a property manager push properties/units and listings into Showdigs, feed prospect inquiries into Showdigs' self-scheduling funnel, order on-demand condition-report inspections, and receive webhook events across the inquiry→tour→inspection lifecycle. Core objects: properties, units, listings, inquiries/prospects, tours (event-only), condition reports. It deliberately does not cover rental applications, tenant screening decisions, leases, tenants, or ledgers — those are delegated to the integrated PMS (AppFolio/Buildium/Yardi/etc.).

## Provider and property-management fit
- What this product is: A leasing-automation platform that automates rental showings/tours, prospect handling, listing syndication, and inspections for property managers. [www.showdigs.com]
- Bank status, when relevant: N-A (not a financial institution; no deposit/ledger product). [www.showdigs.com]
- Who provides any bank account or regulated banking service: none. [N-A]
- What the customer actually receives: Software (a leasing CRM + scheduling engine + webhooks) plus optional on-demand field services (agent showings, condition-report inspections). [www.showdigs.com; api.showdigs.com/docs/ Condition reports]
- Property-management fit: **PM-specialized** — property management is the product's central purpose and multiple PM workflows are documented. [www.showdigs.com; api.showdigs.com/docs/]
- Documented PM-specific workflows: listing management + syndication; prospect inquiry intake and pre-screening/qualification; self-showing and agent-showing tour scheduling; move-in/out, periodic, and vacancy-check condition reports; PMS unit/listing ID mapping. [api.showdigs.com/docs/ Listings, Inquiries, Condition reports, Webhooks]
- Trust or fiduciary workflow support, when relevant: N-A — no trust, escrow, client-fund, security-deposit, or ledger functionality is offered by the API (security_deposit is a listing attribute only). [api.showdigs.com/docs/ Create a Listing]
- Operational role and dependencies: Showdigs is a leasing/showing layer that sits on top of the operator's PMS; realizing its full value requires a PMS (for applications, leases, accounting) and, for hardware self-showings, a supported smart-lock provider.

## Coverage classification (fixed before inspection)
Recorded deviation from the generic "Leasing/screening" defaults (applications, screening decision, lease lifecycle as critical): Showdigs does not process applications, formal screening decisions, or lease signing — it delegates them to the integrated PMS. Classifying PMS-owned functions as Showdigs "critical" would violate "not penalized for a capability with no legitimate use for its category." Objects/workflows below reflect a showing/funnel-automation tool and were fixed before API inspection.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Properties (object) | critical | 3 | Present (create+update; no dedicated GET) |
| Units (object) | critical | 3 | Present (read; create/update via properties) |
| Listings (object) | critical | 3 | Present (full CRUD) |
| Inquiries / prospects (object) | critical | 3 | Present but write-only (create; no REST read) |
| Tours / showings (object) | important | 2 | Event-only (webhooks; no REST resource) |
| Pre-screening / qualification (object) | important | 2 | Event-only (in webhook payloads) |
| Condition reports (object) | important | 2 | Present (create+cancel; no REST read) |
| Agent coverage (object) | optional | 1 | Present (query) |
| Scheduling / screening templates (object) | optional | 1 | Absent (referenced by UUID only) |
| Create/update a listing (workflow) | critical | 3 | Present (POST + PUT) |
| Create an inquiry (workflow) | critical | 3 | Present (POST) |
| Create/update property & units (workflow) | important | 2 | Present (POST + PUT) |
| Schedule a condition report (workflow) | important | 2 | Present (POST) |
| Book/modify a tour (workflow) | important | 2 | Absent (prospect self-schedules via URL) |
| Manage webhook subscription (workflow) | optional | 1 | Present (subscribe/unsubscribe) |
| Deactivate/delete a listing (lifecycle) | critical | 3 | Present (DELETE) |
| Update listing rent/availability (lifecycle) | important | 2 | Present (PUT) |
| Cancel a condition report (lifecycle) | important | 2 | Present (DELETE) |
| Cancel/complete a tour (lifecycle) | important | 2 | Absent (observed via webhook only) |

## Functional coverage map
- Core objects: Properties present (create/update; read only via units/listings) · Units present (read; write via properties) · Listings present (full CRUD) · Inquiries present-but-write-only · Tours event-only · Pre-screening event-only · Condition reports present (create/cancel, no read) · Coverage present · Templates absent.
- Primary operational workflows: create/update listing ✓ · create inquiry ✓ · create/update property+units ✓ · schedule condition report ✓ · book/modify tour ✗ · manage webhook subscription ✓.
- Principal lifecycle changes: deactivate listing ✓ · update listing ✓ · cancel condition report ✓ · tour cancel/complete ✗ (webhook-observable only).

## Category 1: Functional Coverage and Usefulness: 7.5/15
- C1.1 Object coverage: **partial** — weighted coverage = 72.5% (Σ 14.5/20; no critical object absent). Properties/Units/Listings=1.0; Inquiries=0.5 (write-only, no REST read); Tours=0.5 (event-only); Pre-screening=0.5 (event-only); Condition reports=0.5 (no read); Coverage=1.0; Templates=0.0. (All three runs = partial; sub-scores ranged 67.5–72.5%.) [api.showdigs.com/docs/ Units, Listings, Inquiries, Condition reports, Properties, Agent Coverage; live GET /units, /listings 2026-09-10]
- C1.2 Core operational actions: **partial** — weighted coverage = 84.6% (Σ 11/13; no critical write absent), just under the 0.85 yes threshold. Listing create/update, inquiry create, property create/update, condition-report create all 1.0; webhook subscription 1.0; book/modify tour 0.0 (no endpoint — prospects self-schedule via the returned scheduling_url). All three runs = partial. Documentation-graded (write). [api.showdigs.com/docs/ Create/Update a Listing, Create an inquiry, Create/Update a Property, Schedule a condition report, Webhooks subscribe]
- C1.3 Delete or lifecycle actions: **partial** — weighted coverage = 77.8% (Σ 7/9; no critical lifecycle absent). Listing DELETE (deactivate) 1.0, listing PUT 1.0, condition-report DELETE (cancel) 1.0; tour cancel/complete 0.0 (not operator-actionable via API). Documentation-graded (write). [api.showdigs.com/docs/ Delete listing, Update a Listing, Cancel a condition report]
- C1.4 Change notification: **partial** — webhooks cover the prospect→tour→inspection lifecycle (new_inquiry, disqualified_lead, tour_scheduled, tour_completed, tour_cancelled, completed_condition_report), but there are NO events for listing or property/unit changes (which can occur via PMS sync, not only operator action) and no updated-since polling fallback; weighted push coverage of critical+important state changes ≈ 0.64–0.72, below the 0.85 yes threshold. [api.showdigs.com/docs/ Webhooks; live GET /webhooks/sample 2026-09-10] (Reconciled yes→partial: 2 of 3 independent graders scored partial on the evidence.)
Score math: earned 2.0 of 4 applicable checks (four partials); unrounded fraction = 0.500; category points = 7.5 → **7.5/15**; verification coverage = 100%.
What this means for you: You can programmatically list and read your units/listings, push properties and listings in, drop prospects into Showdigs' scheduling funnel, order inspections, and receive webhooks for the prospect→tour→inspection journey. The real gaps: there is no way to read or book/cancel a **tour** through the REST API (tours exist only as webhook events), inquiries and condition reports are write-only (no query-back), there is no endpoint for scheduling/screening templates, and change-notification is one-directional — no webhooks fire for listing/property changes and there is no updated-since polling to catch them.

## Category 2: API Design, Reliability, and Operability: 3.3/10
- C2.1 Modern API conventions: **yes** — resource-oriented REST with standard GET/POST/PUT/DELETE verbs and JSON bodies. [api.showdigs.com/docs/; live 2026-09-10]
- C2.2 Consistent typing: **no** — a core field is stringly typed and types vary across endpoints: `bedrooms:"2"`/`"4"` (string) beside `bathrooms:1`/`2.5` (number) in both `/units` and `/listings`; webhook `cost:"20"` (string) vs tour `charge:49` (number); `inquiry_id` documented as `"4789"` (string) but returned `2394` (number) live; and the webhook `prospects[]` array mixes `phone_number` and `phone` keys. [live GET /units, /listings, /webhooks/sample 2026-09-10; api.showdigs.com/docs/ Webhooks]
- C2.3 Structured errors: **partial** — correct HTTP status semantics (401/404/422) with a human-readable `message` and Laravel `errors{}` for validation, but no populated stable machine-readable error code across endpoints (only an occasional ad-hoc `error:"existingInspection"`). [live 401 {"message":"Unauthenticated."}, 404 {"message":"Unit not found."}, 422 {"message":...,"errors":{...}} 2026-09-10; api.showdigs.com/docs/ Schedule a condition report]
- C2.4 Duplicate prevention: **no** — no idempotency-key or request-ID mechanism is documented, and the most consequential communicating write (`POST /inquiries`, which contacts a real prospect) can create duplicate prospects/outreach on retry. Natural idempotency exists only incidentally and undocumented (condition-report in-progress guard — 422 "existingInspection"; property `origin_id` upsert), which is a defensible basis for "partial" but was resolved to "no." Documentation-graded. [api.showdigs.com/docs/ Schedule a condition report, Create a Property, Create an inquiry] (Reconciled partial→no: 2 of 3 independent graders scored no.)
- C2.5 Graceful handling under load: **partial** — responses carry `X-RateLimit-Limit: 180` and `X-RateLimit-Remaining` (standard, machine-readable throttle signalling), but rate limiting is undocumented and no 429/`Retry-After` recovery guidance is published (limit not breached in testing to avoid throttling the production key). [live response headers 2026-09-10]
- C2.6 Pagination for large collections: **partial** — offset pagination (`page`/`per_page`≤100) with a full Laravel paginator observed live (`total:1549`, `last_page`, populated `next`/`prev` and a `links[]` array), usable to traverse the whole collection; but no documented stable-ordering guarantee, so rows can shift between page fetches during a long sync. [live GET /units?page=1/2 2026-09-10; api.showdigs.com/docs/ Get all units]
- C2.7 Bulk or incremental export: **partial** — full datasets are obtainable via list endpoints without per-record calls for units (paginated) and listings (full set), but there is no updated-since incremental sync, no dedicated bulk/export path, and no list endpoint at all for inquiries, tours, or condition reports. [api.showdigs.com/docs/ Get all units, List all listings; live 2026-09-10]
- C2.8 Webhook security and delivery reliability: **partial** — deliveries can be authenticated via an optional shared "webhook access token" echoed as `Authorization: Bearer TOKEN`, but there is no HMAC/per-payload signature, no documented retry policy, and no replay/idempotency guidance for consumers. Documentation-graded. [api.showdigs.com/docs/ Webhooks → Webhook Access Token]
- C2.9 Concurrency and conflict control: **no** — no ETag/If-Match, version fields, or documented 409 conflict semantics; PUTs are last-write-wins and no ETag header appears on responses. [api.showdigs.com/docs/ Update a Listing, Update a Property; live response headers 2026-09-10]
- C2.10 Versioning and backward compatibility: **partial** — an explicit path version exists (`/api/v1/`), but no documented backward-compatibility policy (breaking vs non-breaking) and no deprecation window/notice. [api.showdigs.com/docs/ endpoint paths]
- C2.11 Request traceability: **no** — no request/correlation identifier on any response header, and none documented. [live response headers 2026-09-10 — only Date, Content-Type, Server, Vary, Cache-Control, X-RateLimit-*, X-Frame-Options, X-XSS-Protection, X-Content-Type-Options]
- C2.12 Service availability and status transparency: **no** — no public status page (status.showdigs.com does not resolve; showdigs.statuspage.io redirects to Atlassian marketing) and no published uptime/SLA. [absence checks 2026-09-10]
Score math: earned 4.0 of 12 applicable checks (1 yes + 6 partial + 5 no → 1.0+3.0+0); unrounded fraction = 0.3333; category points = 3.333 → **3.3/10**; verification coverage = 100%.
What this means for you: The API is a clean, modern REST interface with usable errors and genuinely good pagination, and it does emit rate-limit headers. But building production automation on it takes defensive engineering: you must coerce inconsistently-typed fields, you get no request IDs for support tickets, there is no optimistic-concurrency protection against lost updates, idempotency isn't documented, webhook delivery has no signatures or retry contract, and there is no status page to watch. Fine for internal tooling; below the bar you'd want for mission-critical, high-volume sync.

## Category 3: Access Control and Safe Automation: 0.0/5
- C3.1 Read-only credentials: **no** — no read-only credential/identity can be issued; a single all-purpose Bearer token is used. [operator first-party observation of Business Settings → Integrations, 2026-09-10; api.showdigs.com/docs/ Authenticating requests]
- C3.2 Scoped credentials: **no** — the token cannot be restricted to specific resources, actions, or a role; it is all-or-nothing. [operator first-party observation, 2026-09-10]
- C3.3 Multiple keys: **no** — the operator cannot create multiple distinct credentials for separate integrations. [operator first-party observation, 2026-09-10]
- C3.4 Rotation and revocation: **no** — no self-serve mechanism to rotate/regenerate or revoke the token is available to the operator. [operator first-party observation, 2026-09-10]
- C3.5 Test and production isolation: **N-A** — no sandbox/test environment exists. [no test environment evidenced in docs or site]
Score math: earned 0 of 4 applicable checks (C3.5 N-A, excluded); unrounded fraction = 0.0; category points = **0.0/5**; verification coverage = 100% (4/4 applicable checks verified via operator observation).
What this means for you: This is the weakest area and it carries a real security implication. You get one powerful token that can do everything the API allows, you cannot hand a limited (read-only or scoped) slice to a third-party app or AI agent, you cannot issue separate keys per integration, and — most importantly — if that token leaks you have no self-serve way to revoke or rotate it. Treat the token as a high-value secret and, if it's ever exposed, contact Showdigs support immediately. (This rests on your first-party account observation; a screenshot of the Integrations page would make it fully auditable and I'll revise if any control was missed — e.g., a regenerate button would move C3.4.)

## Category 4: Documentation and AI-Agent Readiness: 1.3/5
- C4.1 Complete self-serve reference: **partial** — a complete, example-rich Scribe reference covers the core endpoints with worked request/response examples, but every example uses `http://localhost` as the base URL (the real host is never stated), and the webhook subscribe/unsubscribe request bodies are under-documented (example `url` is just `"https:"`), so a developer must infer the real base URL and webhook payload. [api.showdigs.com/docs/ Introduction, all endpoints, Webhooks subscribe]
- C4.2 Reliable machine-consumable integration path: **no** — the two advertised machine-consumable artifacts are both broken (View OpenAPI spec → `docs.openapi` returns HTTP 500; View Postman collection → `docs.postman` returns HTTP 404), there is no official SDK and no MCP server, and the per-endpoint multi-language snippets are copy-paste examples, not a spec/SDK. (A first-party Zapier app exists but is a no-code connector within Zapier, not one of the qualifying build mechanisms.) [api.showdigs.com/docs/ menu links; live 500/404 across Accept variants 2026-09-10; help.showdigs.com Zapier integrations]
- C4.3 AI-readable documentation: **no** — no `llms.txt`/`llms-full.txt` (422), no per-endpoint Markdown, and no downloadable plain-text/Markdown corpus; the single Scribe HTML page is human documentation, not a resource structured for AI retrieval. [absence checks 2026-09-10]
- C4.4 Kept current: **partial** — the only currency signal is the reference's "Last updated: August 4, 2026" date (plus a few inline forward-looking notes); there is no changelog, release notes, or deprecation guidance. [api.showdigs.com/docs/ footer "Last updated"]
Score math: earned 1.0 of 4 applicable checks (2 partial + 2 no); unrounded fraction = 0.25; category points = 1.25 → **1.3/5**; verification coverage = 100%.
What this means for you: A developer can build from the reference, but not smoothly — they'll hit the `localhost` base-URL trap, get no working OpenAPI/Postman file to generate a client or feed an AI tool, and have no machine-readable docs corpus. Expect more hand-coding and reverse-engineering than a well-tooled API requires, and no reliable changelog to watch for breaking changes.

## Category 5: Accessibility and Cost: 15.0/15
- C5.1 Self-serve API key: **yes** — an entitled operator retrieves the token self-serve from Business Settings → Integrations, with no sales call, support ticket, or key-approval step; confirmed by the operator obtaining and using a working production token. [api.showdigs.com/docs/ Authenticating requests: "You can retrieve your token by visiting your integrations settings page."; operator token verified live 2026-09-10]
- C5.3 Not commercially gated: **yes** — Showdigs sells a single plan ($1.20/unit/month, $120 minimum); API access is not locked behind a premium/top-tier upgrade and is not shown as a paid add-on. The ~100-unit account minimum is a commercial-scale threshold for the product itself, not API-specific gating. [www.showdigs.com/pricing]
Score math: earned 2.0 of 2 applicable checks; unrounded fraction = 1.0; category points = **15.0/15**; verification coverage = 100%.
What this means for you: This is the API's strongest area. If you already have a Showdigs account, the API is right there — self-serve token, no upsell, no gatekeeping. Nothing about cost or access stops you from building today.

## Total
- Raw: 27.08 / 50
- Normalized before rounding: 54.17 / 100
- Published numeric score: **54 / 100**
- Letter grade: **F**
- Evidence tier: Baseline verified
- Overall verification coverage: 100% (gate satisfied: no category Unable to verify; overall ≥ 80%; minimum read-path battery complete)
- Partial-result flag: no (score published). Category 3 rests on operator first-party observation; a screenshot would upgrade its auditability.
- Published number = reconciled result of three independent runs (not an average); see "Three-run reconciliation."
- Unresolved / boundary evaluator disagreements (resolved for the published number; effects disclosed):
  - C1.4 (yes vs partial): resolved to partial (2 of 3 runs). The yes reading raises the total by ~3.8 normalized → ≈58 (still F).
  - C2.4 (partial vs no): resolved to no (2 of 3 runs). The partial reading raises the total by ~1.7 normalized → ≈56 (still F).
  - C4.2 (no vs partial): resolved to no (2 of 3 runs). The partial reading raises the total by ~1.3 normalized → ≈55 (still F).
  - C1.2 (unanimous partial at 84.6%, at the 0.85 boundary): if programmatic tour-booking were treated as N-A, C1.2 = yes. Grade stability: D- (60) is reached only if all borderline calls simultaneously take their most generous reading (ceiling ≈ 61); under the consensus/strict reads the grade is F.

## Three-run reconciliation (methodology Step 12)
The published number is the single reconciled result of three independent grading runs on the frozen evidence packet, each disagreement resolved against the evidence — not an average of the three totals.
- Run 1 (primary, read-path live-tested): 60 / 100 (D-)
- Run 2 (independent grader, frozen packet): 55 / 100 (F)
- Run 3 (independent grader, frozen packet): 54 / 100 (F)
- Reconciled published result: **54 / 100 (F)**

Agreement: all three runs assigned identical marks on 23 of 26 applicable checks — including all of Category 3 (0/5), all of Category 5 (15/15), C1.1/C1.2/C1.3 (partial), C2.1 (yes), C2.2 (no), C2.3/C2.5/C2.6/C2.7/C2.8/C2.10 (partial), C2.9/C2.11/C2.12 (no), C4.1/C4.4 (partial), and C4.3 (no). Three checks were contested and resolved against the frozen evidence:
- **C1.4** — Run 1 yes vs Runs 2 & 3 partial → **partial**. Webhooks cover the prospect→tour→inspection lifecycle but not listing/property/unit changes (which can arrive via PMS sync), and there is no updated-since polling fallback; weighted push coverage ≈ 0.64–0.72 < 0.85. Run 1's yes over-narrowed the "critical+important state changes" set.
- **C2.4** — Run 1 partial vs Runs 2 & 3 no → **no**. Nothing is documented and the highest-value consequential write (POST /inquiries → real-person contact) can duplicate on retry; the only protection is an incidental, undocumented in-progress guard. Partial stays defensible (the checklist credits "natural idempotency"), which is why it is logged as a boundary call.
- **C4.2** — Run 2 partial vs Runs 1 & 3 no → **no**. Both advertised code-grade paths are broken (OpenAPI 500, Postman 404) and there is no SDK/MCP; the first-party Zapier connector is a no-code path within Zapier, not one of the checklist's qualifying build mechanisms.
Convergence: the three independent runs fell within a 6-point band (54–60) and, after resolving the three contested checks on the evidence, agree the grade is **F** (the reconciled marks coincide with Run 3). The only path to D- requires all three boundary calls to break the generous way at once.

## Bottom line for a property manager
Showdigs has a real, first-party REST API that is easy to get into (self-serve token, single plan, no upsell) and covers its core leasing-showing job well: you can sync properties and listings, push prospects into its self-scheduling funnel, order condition-report inspections, and receive webhooks across the inquiry→tour→inspection lifecycle. What you can build today is solid listing-sync and lead/inspection automation with event-driven notifications. What you cannot build well: anything needing to read or manage **tours** via REST (they're webhook-only), query inquiries/inspections back, or run at mission-critical scale — the API lacks consistent typing, request IDs, concurrency control, documented idempotency, signed/retried webhooks, a status page, and any working OpenAPI/SDK. The most serious limitation is access control: a single all-powerful token with no read-only/scoped keys and no self-serve rotation or revocation, so guard it carefully. Showdigs is not a bank, PMS, or trust-accounting system and does not handle applications, leases, or funds — it is a leasing/showing layer that sits on top of your PMS (AppFolio/Buildium/Yardi/etc.), which you still need for the rest. Net: a genuinely useful integration surface for leasing automation, but held to a failing API grade by production-hardening and credential-security gaps — one non-scopable, non-revocable token, thin operability (no request IDs, no concurrency control, undocumented idempotency), one-directional change notification, and no working spec/SDK. Reconciled across three independent grading runs (60 / 55 / 54): **54/100 (F)**.
