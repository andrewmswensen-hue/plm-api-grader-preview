# API Report Card: AppFolio Property Manager (AppFolio Database API)

**Published result: 48/100, grade F — reconciled across three independent grading runs** (run 1: evidence-collecting evaluator, 50; runs 2–3: independent graders over the same frozen packet with no visibility into run 1's marks, 45 and 48). 21 of 27 checks were unanimous; the six split checks were resolved against the frozen evidence (details in "Three-run reconciliation" below). The grade is F under every defensible resolution of the remaining ambiguities (plausible band 45–56).

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Fable 5 (claude-fable-5)
- Date run: 2026-09-01
- Provisional evidence-packet version or ID: appfolio-2026-09-01-v0.1
- Final evidence-packet version or ID: appfolio-2026-09-01-v2.1 (frozen 2026-09-01; v2.0 after operator supplied authenticated Developer Space access; v2.1 after operator supplied the in-product Reports API documentation)
- Evidence-discovery mode: tool-enabled discovery (+ operator-authorized authenticated browser session for login-gated documentation)
- Evidence tier: **Baseline verified** — read-path battery (steps 1–5) complete against production; write-path steps (6–8) not run pending operator review of the dry-run plan, so write-dependent checks are graded from first-party documentation and flagged below
- Live-write method and safety: none — writes documentation-graded (controlled-live plan drafted, awaiting operator approval; upgrade to "Fully verified — controlled live" available)
- Minimum live-test battery: steps 1–5 complete; step 6 pending operator; step 7 N-A→pending (idempotency IS documented — live retry test moves to the write plan); step 8 pending operator
- Live tests performed: authenticate; read+paginate properties (3 pages, distinct IDs, next_page_path); incremental filter honored (LastUpdatedAtFrom mandatory); deliberate errors (404/400, structured); header signals (x-request-id on every response; no rate headers on 200s); object read sweep across 28 candidate endpoints
- Live tests not possible this session: fixture write, idempotent retry, webhook trigger (operator authorization steps outstanding)
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8

## Final evidence packet manifest
1. https://developer.appfolio.com/api_documentation/database — authenticated Database API reference (operator-authorized session, 2026-09-01). Single-page reference, ~479KB text: API Overview; HTTP Basic Authentication (+ OAuth Client Credentials flow referenced); Rate Limits; Error Codes; Best Practices (ISO 8601, deprecation, filtering/pagination, Retry-After semantics, user roles, **Idempotency**); Troubleshooting; Webhooks Overview + Getting Started + Topics table; 61 GET + 101 write operations (POST/PATCH/PUT/DELETE) with typed schemas (`string <uuid>`, `string <decimal>`, enums) and worked cURL/request/response samples per endpoint.
2. https://developer.appfolio.com/api_changelog/database — authenticated Database API Changelog: 104 dated entries, 10/30/2023 → 8/28/2026, monthly cadence, deprecation and breaking-change annotations.
3. https://developer.appfolio.com/customers/{developer-id}/credentials — Developer Space Dashboard, "Access Credential Management" (product-interface observation 2026-09-01): one credential pair per customer database, Show Client Id, Age of Client Secret, self-serve **Regenerate Client Secret**, Date Data Last Read/Written audit fields. Portal also exposes AUDIT LOG and WEBHOOKS LOG views.
4. https://www.appfolio.com/stack/partners/api — public Stack API catalog. Accessed 2026-09-01.
5. https://www.appfolio.com/pricing — Core (no API), Plus ("AppFolio API (read only)"), Max ("AppFolio API (read/write)").
6. https://www.appfolio.com/stack/become-a-partner — partner application process; partner sandbox.
7. https://engineering.appfolio.com/appfolio-engineering/2022/12/19/building-apis-that-delight-customers-and-developers — rate-limit philosophy, OpenAPI-adherence claim, version-transition support.
8. https://status.appfolio.com — public status page incl. "AppFolio Database APIs" component, 90-day uptime, incident history.
9. https://github.com/appfolio/stack-webhook-jws-examples — official webhook JWS verification examples (archived 2025-10-16).
10. https://api.appfolio.com/.well-known/jwks.json — live JWKS, RSA, PS256.
11. https://www.appfolio.com/llms.txt — marketing corpus (not API docs). developer.appfolio.com/llms.txt → 404.
12. Live API observations 2026-09-01, api.appfolio.com/api/v0, operator production credential (read-only). Request-ids on file (e.g. 7b6ba8a3-c16c-4e0f-a287-303062514fda).
13. Operator support-history: request-ids submitted in a 2026-06 ticket led to /leases endpoint grant (evidence that request-ids are support-usable and that endpoint entitlements are vendor-mediated).
14. https://croskey.appfolio.com/api_credentials/basic_auth_credentials?selected_tab=documentation — in-product **AppFolio Reports API (2.0.0)** documentation (operator-authorized session, 2026-09-01): 163 read-only report endpoints at `https://{vhost}.appfolio.com/api/v2/reports/{endpoint}.json` incl. General Ledger, Cash Flow (+Detail/12-Month), Income Statements, Tenant/Vendor/Homeowner Ledgers, Balance Sheets, Aged Payables, Bill Detail, Owner 1099s/Withholdings, **Trust Account Balance, Trust Account Detail, Security Deposit Funds Detail, Deposit Register**; saved-report execution by UUID (`GET /saved/{uuid}.json`); documented rate limits (7 requests per 15 seconds; `next_page_url` exempt); `next_page_url` pagination; v1→v2 migration guide.

## Evidence-amendment log
- Post-provisional, operator supplied authenticated Developer Space access (methodology §"Request login-gated documentation"): sources 1–3 added. Checks amended: C1.1–C1.4, C2.2–C2.6, C2.8–C2.11, C3.1–C3.5, C4.1–C4.4, C5.1. All amendments recalculated before freeze v2.0.
- C2.8: sources 9, 10 added during controlled verification pass (signature scheme).
- C1.1: owner_contributions / owner_distributions / gl_transactions rechecked at path variants — 404; absent from the v0 reference (superseded by gl_details/journal_entries reads).
- C4.2: GitHub org sweep — no public SDK/OpenAPI; no spec URL loaded by the reference SPA (network-resource probe); no download link in the portal.
- Post-v2.0, operator supplied source 14 (in-product Reports API docs). Checks recalculated: C1.1 reconciliation item 0.0 → 0.5 (present, materially read-only via Trust Account Detail / Deposit Register reports) — weighted coverage 88.2% → 90.8%, mark unchanged (yes). Provider-fit trust/fiduciary finding upgraded from "not documented" to "documented, read-only". No category score or published-score change. Also confirmed: owner_contributions / owner_distributions appear in NEITHER doc set nor the changelog — removed from the v0 API without a changelog entry (noted; does not alter C4.4's mark, which grades overall currency signal).

## API eligibility
- Qualifying API: **yes**
- API operator: AppFolio, Inc. [source 1: base URL https://api.appfolio.com/api/v0/{endpoint}; server: appfolio]
- Access or credential issuer: AppFolio, under customer plan entitlement (Plus read-only / Max read-write); credentials generated self-serve per customer database (Admin → Developer ID; Generate a Client Secret); per-endpoint and per-field access is agreed with AppFolio ("If the example response contains fields that AppFolio has not previously agreed to send to you, they will be omitted") [sources 1, 3, 5, 13]
- Eligibility basis: authenticated first-party reference documenting 162 operations plus a working production credential [1, 12]

## Context
- Software category: Accounting/PMS platform. **PM-specialized.**
- What the API is for: reading and (selectively) writing a customer's AppFolio Property Manager database — the full PM object graph (properties, units, leases, tenants, owners, vendors, ledgers, GL, bank accounts, work orders, applications, leasing pipeline, inspections, inventories, purchase orders, community associations) — with signed webhooks over 20 topics. Two first-party interfaces share the same credential: the **Database API** (v0, record-level CRUD) and the **Reports API** (v2, 163 read-only report datasets incl. trust-account and 1099 reports, with saved-report execution). [1, 14]

## Provider and property-management fit
- What this product is: cloud property-management platform; the API exposes the customer's own database. [1]
- Bank status: not a bank (payment processing is a product service; no bank claim in reviewed materials). [8]
- Bank service provider: not determined from reviewed materials (N-A to score).
- What the customer receives: software + a per-database API entitlement gated by plan tier. [5]
- Documented PM-specific workflows: work orders (create/update incl. WorkOrderStatus), bills & charges (create/bulk/async), rental-application decisioning (status enum approved/denied/canceled/…), lease term updates (EndOn/IsMtm/RenewedOn), showings, leads, inspections, unit pricing matrices, marketing photos. [1]
- Trust or fiduciary workflow support: **documented, read-only** — the Reports API exposes Trust Account Balance, Trust Account Detail, Security Deposit Funds Detail, and Deposit Register reports; no API surface manages trust accounts, initiates payments, or performs reconciliation. [14, 1, 12]
- Operational role and dependencies: system of record; operator supplies own webhook receiver/middleware; some enablement (webhooks, endpoint/field entitlements, batching) requires an AppFolio representative. [1]

## Coverage classification (fixed before inspection — default Accounting/PMS; unchanged)
As recorded in packet v0.1 (see table in prior section of packet history). Weights: critical=3, important=2, optional=1.

## Category 1: Functional Coverage and Usefulness: 5.6/15 (reconciled)
- C1.1 Object coverage: **partial** (reconciled; run 1 scored yes) — weighted coverage ≈ **84–87%** depending on two contestable half-points, straddling the 85% yes-line; no critical object absent. All 7 critical objects live-read (200s), but leases score 0.5 as an object (3-field PATCH, no create — both independent graders held this and it is the better reading of "operations its role requires"); payments 0.5 (read-only via payables/reports); reconciliation 0–0.5 (no reconciliation resource; trust/deposit reports arguably count read-only); communications 0.0; custom fields 0.5. Resolved to partial: two of three graders, and the mark should not hinge on a contestable half-point. [1, 12, 14]
- C1.2 Core operational actions: **partial** *(documentation-graded)* — weighted 14/19 = **73.7%**. Read core records 1.0 (live); post ledger charges & payments 0.5 (POST /charges + /journal_entries documented; tenant payments/receipts cannot be posted); create/update leases 0.5 (PATCH /leases/{id} — EndOn, IsMtm, RenewedOn — but no lease create); owners 1.0, bills 1.0 (incl. bulk/async), applicants 1.0, work orders 1.0 (POST + PATCH incl. WorkOrderStatus per 8/28/2026 changelog); payments 0.0. [1, 2]
- C1.3 Delete or lifecycle actions: **no** *(documentation-graded)* — weighted 4/10 = **40%**, and move-out (critical) is absent from the API (no MoveOut on tenant PATCH; no occupancy end operation). Present: work-order status transitions 1.0, application decisioning 1.0 (approved/denied/canceled/in_review/…); absent: void/reverse of ledger transactions, archive. DELETEs exist only for inspections, inventories, photos, WO attachments. [1]
- C1.4 Change notification: **partial** (reconciled; run 1 scored yes) — 20 signed webhook topics with create/update/destroy events; the mark turns on the denominator: over objects *present*, push coverage is 89.7% (only bank accounts lack a topic) → yes; over the full predetermined critical+important set (counting absent payments/reconciliation as undetectable) it is 78.8% → partial. Two of three graders used the full-set denominator; published mark is partial with the definitional disagreement disclosed below. Mandatory-filter incremental polling (live-verified), self-serve "Send Test Event", opt-in batching. [1, 12]
Score math (reconciled): earned 1.5 of 4 → 0.375 × 15 = **5.625 → 5.6/15**; verification coverage 4/4 = 100%.
What this means for you: you can read everything and get notified about nearly everything, and you can run maintenance, billing, and application-decision automations — but the leasing money-cycle (lease creation, move-out, payment posting, voids, reconciliation) stays in the AppFolio UI.

## Category 2: API Design, Reliability, and Operability: 7.9/10 (reconciled)
- C2.1 Modern conventions: **yes** — resource-oriented JSON REST, standard verbs incl. DELETE, worked samples. [1, 12]
- C2.2 Consistent typing: **yes** — reference schemas are typed (`string <uuid>`, `string <decimal>`, `boolean`, enums; money documented as decimal-string by design; ISO 8601 mandated) and live reads matched them. [1, 12]
- C2.3 Structured errors: **partial** — documented status table incl. custom codes (533 Data Unavailable, 701 Invalid Credential) and structured `{code, message}` bodies (live-confirmed, actionable); limitation: `code` mirrors the HTTP status rather than identifying the specific error cause (message parsing required), and the 404 shape differs (`{status, error}`). [1, 12]
- C2.4 Duplicate prevention: **yes** *(documentation-graded; live retry in write plan)* — full `Idempotency-Key` support on POST: SHA-256 body fingerprint, `Idempotent-Replayed: true` replay header, same-key/different-body → 422, in-flight → 409 + Retry-After, 24 h TTL, machine-readable error codes. [1 §Idempotency]
- C2.5 Graceful handling under load: **yes** — documented 429 with `Retry-After` header and exact semantics (8 req/s, 256/min, 4096/hr; per-limit Retry-After values; stricter 5-per-15 s on /gl_details and /jobs); exponential backoff guidance for 503. [1 §Rate Limits, §Best Practices]
- C2.6 Pagination: **partial** — documented `page[number]/page[size]` (default 1000) + `next_page_path` on every list endpoint, live-traversed; limitation: no stable-ordering guarantee documented and no total-count signal. [1, 12]
- C2.7 Bulk or incremental export: **yes** — mandatory `LastUpdatedAtFrom` incremental pattern documented as the sync method (1970-01-01 initial import + watermarks), live-verified; plus bulk and async-bulk write endpoints and a /jobs status endpoint. [1, 12]
- C2.8 Webhook security and delivery reliability: **partial** *(documentation-graded)* — JWS PS256 detached signatures with public JWKS (documented + live key set) and duplicate-delivery guidance via `event_id`/`batch_id`; limitation: no documented retry policy (webhook logs record attempts and response codes, but no redelivery contract). [1, 9, 10]
- C2.9 Concurrency and conflict control: **yes** — documented 409 ("conflicts with the current state of the resource — resolve and retry"), documented simultaneous-PATCH behavior (second write fails; stagger/queue guidance), documented concurrency/rate behavior. No ETag/version fields, but the check accepts documented conflict semantics + concurrency behavior. [1 §Error Codes, §Troubleshooting]
- C2.10 Versioning and backward compatibility: **partial** (reconciled; run 1 scored yes, both independent graders partial) — explicit path versioning (`/api/v0`, Reports `/v2`) and deprecation notices exist, but the check's yes requires a compatibility policy *defining breaking vs non-breaking changes* and deprecation *windows* — neither is documented ("removed entirely when a new API version is released", no timelines). [1 §Best Practices, 2, 14]
- C2.11 Request traceability: **partial** — unique `x-request-id` on every live response and demonstrably usable with AppFolio support (2026-06 ticket); limitation: the identifier is not documented in the reference. [12, 13]
- C2.12 Status transparency: **yes** — public status page, per-component 90-day uptime + incident history incl. "AppFolio Database APIs". [8]
Score math (reconciled): earned 9.5 of 12 → 0.7917 × 10 = **7.917 → 7.9/10**; verification coverage 12/12 = 100%. (C2.9 stays yes on the 2-of-3 majority and the mechanical reading of the check; run 3's stricter partial is disclosed below.)
What this means for you: this is a well-engineered, predictable API — typed schemas, real idempotency, exact rate-limit semantics, signed webhooks — with only minor gaps (no domain error codes, no ordering guarantee, undocumented request-id, no webhook retry contract).

## Category 3: Access Control and Safe Automation: 1.9/5 (reconciled)
- C3.1 Read-only credentials: **no** — read-only exists only as a plan tier (Plus), not as an issuable credential type; the credential UI offers no read-only option. [3, 5]
- C3.2 Scoped credentials: **partial** — per-endpoint and per-field scoping demonstrably exists but is administered by AppFolio agreement, not operator-configurable (live 403→grant history; "fields AppFolio has not previously agreed to send… omitted"). [1, 13]
- C3.3 Multiple keys: **no** — one credential pair per customer database; the credential UI shows a single pair with no option to create more ("You'll need separate credentials for each customer database" — separation is per-database, not per-integration). [1, 3]
- C3.4 Rotation and revocation: **yes** — self-serve "Regenerate Client Secret" in the Developer Space dashboard (product-interface observation; secret age displayed). [3]
- C3.5 Test and production isolation: **N-A** (reconciled; run 1 scored no, both independent graders N-A per the check's own instruction "mark N-A when no sandbox or separate test environment exists" — none exists for operators; the partner-only sandbox is not part of the operator offering). The practical consequence — operators test against production with the sole all-powerful credential — is captured in C3.1–C3.3. [3, 6]
Score math (reconciled): earned 1.5 of 4 applicable → 0.375 × 5 = **1.875 → 1.9/5**; verification coverage 4/4 applicable = 100%.
What this means for you: one all-or-nothing production key per database. You can rotate it yourself, but you cannot mint a read-only key for a reporting tool, a scoped key for an AI agent, or a second key you can revoke independently — and there is no sandbox for you to test in.

## Category 4: Documentation and AI-Agent Readiness: 1.3/5 (reconciled)
- C4.1 Complete self-serve reference: **partial** — the reference is complete and example-rich (162 operations, typed schemas, worked requests/responses, guides for auth/errors/webhooks/idempotency), but it is login-gated to customers/partners, not publicly accessible. [1]
- C4.2 Machine-consumable path: **no** — no published OpenAPI/Swagger spec (none served to the docs SPA, none downloadable, none public), no official SDKs, no MCP server. [1, amendment log]
- C4.3 AI-readable documentation: **no** — no API-focused llms.txt/Markdown corpus; the reference is a client-rendered SPA that returns an empty shell to non-browser retrieval. [10, 11]
- C4.4 Kept current: **partial** (reconciled; run 1 scored yes, both independent graders partial — and they are right) — the changelog is rich (104 dated entries, monthly cadence through 8/28/2026, deprecation/breaking annotations), but this run *demonstrated* a silent breaking change: the removal of the owner_contributions/owner_distributions endpoints (live 404s) appears nowhere in it. A currency signal with a proven gap on a breaking removal is "incomplete or otherwise unreliable" → partial. [2, 12]
Score math (reconciled): earned 1.0 of 4 → 0.25 × 5 = **1.25 → 1.3/5**; verification coverage 4/4 = 100%.
What this means for you: a human developer with your login has excellent docs; your AI coding tools do not — no spec to generate a client from, no SDK, and nothing they can retrieve without a browser session.

## Category 5: Accessibility and Cost: 7.5/15 (reconciled)
- C5.1 Self-serve API key: **partial** — once entitled, credential generation and rotation are self-serve in-product (documented steps + observed UI); but usable access is not: per-endpoint/per-field entitlements require AppFolio agreement (proven by this account's /leases support-ticket history), and webhooks/batching require contacting a representative. [1, 3, 13]
- C5.3 Not commercially gated: **partial** (reconciled; run 1 scored no, both independent graders partial) — the check's partial bucket ("some meaningful capabilities are tier-gated") fits the evidence more precisely than its no bucket ("the API requires a premium plan"): a read-only API is available at the mid tier (Plus), while all writes require the top-tier Max plan and Core has no API. [5]
Score math (reconciled): earned 1.0 of 2 → 0.50 × 15 = **7.5/15**; verification coverage 2/2 = 100%.
What this means for you: the API is a premium-plan feature, and even then AppFolio decides endpoint-by-endpoint (and field-by-field) what your key can see.

## Total (reconciled across three runs)
- Raw: 5.625 + 7.917 + 1.875 + 1.25 + 7.5 = **24.17 / 50**
- Normalized before rounding: 48.33 / 100
- Published numeric score: **48 / 100**
- Letter grade: **F**
- Evidence tier: **Baseline verified** (write checks C1.2, C1.3, C2.4, C2.8 documentation-graded; upgrade path: approved controlled-live write plan)
- Overall verification coverage: 26/26 applicable = 100% (C3.5 N-A; gate passed: no category Unable to verify; ≥ 80%)
- Partial-result flag: yes — write-path battery pending operator authorization; executing it would firm up (not likely change) C1.2/C1.3 and could confirm C2.4 idempotency live

## Three-run reconciliation (methodology step 12)
Three grading runs: run 1 (evidence-collecting evaluator) 50/100; runs 2 and 3 (independent graders over the frozen packet v2.1, blind to run 1's marks, one neutral and one instructed to take the strictest defensible readings) 45/100 and 48/100. **21 of 27 checks unanimous.** Check-level resolution of the six splits:
- **C1.1** (R1 yes; R2/R3 partial) → **partial.** The independent graders' 0.5 for the leases *object* (3-field PATCH, no create) is the better reading of "operations its role requires"; the remaining spread (82.9–86.8%) straddles the 85% line on contestable half-points (reconciliation-via-reports, communications-as-notes). A mark should not hinge on those.
- **C1.2** (R1/R3 partial; R2 no) → **partial.** R2 read "critical write workflow absent" to cover lease-create alone; but the fixed workflow is "create AND update leases," and update exists — partially present is not absent. 2-of-3 agree. Noted for reproducibility: the three runs constructed the mutable-item set differently (weighted coverages 59.1–73.7%) yet all land in the partial band except via R2's absent-clause reading.
- **C1.4** (R1 yes; R2/R3 partial) → **partial**, disagreement disclosed. Pure definition question: whether absent objects (payments, reconciliation) count in the push-coverage denominator (78.8% → partial) or are excluded as N-A within the sub-map since their absence is already penalized in C1.1/C1.2 (89.7% → yes). Unresolvable from evidence; majority published; score effect if yes: +1.9 raw (+3.7 normalized).
- **C2.10** (R1 yes; R2/R3 partial) → **partial.** The yes-conjunction requires breaking-vs-non-breaking definitions and deprecation windows; neither is documented. Run 1 conceded.
- **C3.5** (R1 no; R2/R3 N-A) → **N-A** per the check's own instruction when no test environment exists for the evaluated access. Score effect vs no: +0.4 raw.
- **C4.4** (R1 yes; R2/R3 partial) → **partial.** Both independent graders correctly weighed the demonstrated silent breaking change (owner_contributions/owner_distributions removed with no changelog entry) against the otherwise-strong changelog. Run 1 conceded.
- **C5.3** (R1 no; R2/R3 partial) → **partial.** "Some meaningful capabilities are tier-gated" fits the evidence (read-only API at mid-tier Plus; writes top-tier only) more precisely than "requires a premium plan." Run 1 conceded. Largest single mover (+3.75 raw vs run 1's mark).
- **Remaining minority readings (disclosed, not adopted):** R3's C2.9 partial (no ETags; −0.4 raw if adopted); R3's C1.1 payments 0.0 (−0.3 raw within an already-partial check).
- **Robustness:** across every defensible resolution of the disclosed ambiguities the published score stays in the 45–56 band — the letter grade is **F under all of them**.

## Bottom line for a property manager
AppFolio's Database API is a well-engineered read-and-notify platform with a genuinely strong operational core: every object your business runs on is readable with typed schemas, incremental sync is the documented design, webhooks across 20 topics are cryptographically signed, idempotency keys and exact rate-limit semantics are documented, and a monthly changelog keeps it current. Its score is dragged down by the other half of the question — what an operator is *allowed* to build: the API is locked to premium plans, endpoint and field access is negotiated with AppFolio rather than self-serve, there is one all-powerful production key per database with no read-only or scoped option and no operator sandbox, AI tooling gets no spec, SDK, or retrievable docs, and the leasing money-cycle (lease creation, move-out, payment posting, voids, reconciliation) is absent from the API entirely. The F reflects this rubric's heavy weighting of access, control, and workflow completeness, not engineering quality — on design alone it scores 7.9/10, and the 48/100 was confirmed by three independent grading runs (50, 45, 48) that agreed on 21 of 27 checks and on the letter grade under every resolution. Practical read: if you're on the Max plan, AppFolio is an excellent system of record to sync from and to automate maintenance, billing, and application decisions against — and the Reports API lets you pull trust-account, ledger, and 1099 reports programmatically. It is not a platform you can fully run your business through: managing trust accounts, posting payments, and reconciliation stay in the UI.
