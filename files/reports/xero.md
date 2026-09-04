# API Report Card: Xero — Accounting API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 4.8
- Date run: 2026-08-27
- Provisional evidence-packet version or ID: XERO-2026-08-27-prov1
- Final evidence-packet version or ID: XERO-2026-08-27-final1
- Evidence-discovery mode: tool-enabled discovery (first-party docs + fetched OpenAPI specs + live tests)
- Evidence tier: **Baseline verified**
- Live-write method and safety: none — writes documentation-graded (operator authorized a READ-ONLY connection to a live production org; no write performed)
- Minimum live-test battery: read-path steps 1–5 complete live; write-path steps 6–8 N/A (read-only connection) and documentation-graded
- Live tests performed: authenticate (GET /Organisation); paginate (Contacts, Invoices pageSize→pagination object); incremental (If-Modified-Since honored) + filter (where Type==ACCREC); deliberate errors (404, 401); rate-limit + trace headers; coverage reads (Accounts, Contacts, Invoices, BankTransactions, ManualJournals, Payments, Items, Reports); scope-enforcement (Journals 401)
- Live tests not possible: write-path (steps 6–8) by operator choice (read-only)
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8
- Live test org: RL Property Management (tenantId 892a8144-…, production, read-only)

## Final evidence packet manifest
- https://developer.xero.com/documentation/api/accounting/invoices
- https://developer.xero.com/documentation/api/accounting/contacts
- https://developer.xero.com/documentation/api/accounting/payments
- https://developer.xero.com/documentation/guides/oauth2/overview/
- https://developer.xero.com/documentation/guides/oauth2/scopes/
- https://developer.xero.com/documentation/guides/oauth2/custom-connections/
- https://developer.xero.com/documentation/guides/oauth2/limits/
- https://developer.xero.com/documentation/guides/idempotent-requests/idempotency/
- https://developer.xero.com/documentation/guides/webhooks/overview/ (rendered in-browser 2026-08-27 — retry policy, replay/idempotency guidance, HMAC signature)
- https://developer.xero.com/documentation/getting-started-guide/
- https://developer.xero.com/changelog
- https://developer.xero.com/pricing
- https://github.com/XeroAPI/Xero-OpenAPI (xero_accounting.yaml v17.0.0; xero-webhooks.yaml; xero_bankfeeds.yaml; xero-identity.yaml)
- https://github.com/XeroAPI/xero-mcp-server ; https://github.com/XeroAPI/xero-agent-toolkit
- https://github.com/orgs/XeroAPI/repositories (SDKs: Xero-NetStandard, Xero-Java, xero-node, xero-php-oauth2, xero-python, xero-ruby)
- https://identity.xero.com/.well-known/openid-configuration (revocation_endpoint)
- https://status.xero.com/
- https://www.xero.com/us/ ; https://apps.xero.com/us/industry/property-realty/
- Live OAuth 2.0 authorization-code connection (app "api grader") + read-path battery observations, 2026-08-27

## Evidence-amendment log
- C2.8 (webhooks) — 2026-08-27: the delivery retry policy and consumer replay/idempotency guidance sat on a JavaScript-rendered webhooks guide the discovery fetch tool could not load. The page was rendered in-browser and confirmed both, plus HMAC-SHA256 signatures, so C2.8 was finalized **yes** (it had been provisionally partial while the page was inaccessible). Source added: developer.xero.com/documentation/guides/webhooks/overview/.
- C2.3 (structured errors): downgraded doc "yes" → **partial** after live observation that 404 returns plain text while 401 returns a JSON envelope and 400 returns a ValidationException — shapes vary. Source added: live battery.
- C4.3 / C5.3 scopes model: added https://developer.xero.com/documentation/guides/oauth2/scopes/ and the app Configuration scope list (granular-scopes migration; accounting.journals.read not assigned to new apps) during verification.
- Live scope enforcement: GET /Journals → 401 confirms per-scope read-only enforcement (supports C3.1, C3.2).

## API eligibility
- Qualifying API: **yes**
- API operator: **Xero** [OpenAPI title "Xero Accounting API" v17.0.0, github.com/XeroAPI/Xero-OpenAPI]
- Access or credential issuer: **Xero** — self-created OAuth 2.0 app in the developer portal (auth-code/PKCE for multi-org; client-credentials "Custom Connections" for single-org M2M) [developer.xero.com/documentation/guides/oauth2/overview/; verified live in My Apps]
- Eligibility basis: A programmatic, authenticated REST API exposing Xero's accounting functions, with self-serve credential issuance. Confirmed live: authenticated and read core resources from a production org.

## Context
- Software category: **Accounting/PMS platform** — specifically a general-purpose cloud accounting platform (not a property-management system).
- What the API is for and its core objects and workflows: The Xero Accounting API lets software read and write a business's general ledger and sub-ledgers — chart of accounts, contacts, invoices (AR/AP), payments, bank transactions, manual journals — and read financial reports. Core objects are accounting objects; core workflows are posting charges/bills and payments, creating/updating contacts and accounts, and reading ledgers and reports. Sibling APIs exist (Payroll, Files, Assets, Projects, Bank Feeds) but were out of scope.

## Provider and property-management fit
- What this product is: Cloud accounting software for small businesses. [title "Accounting Software for Small Businesses | Xero US", www.xero.com/us/]
- Bank status: **not a bank** — accounting software that connects to banks (bank feeds) and moves money via payment features/partners. [www.xero.com/us/]
- Who provides any bank account or regulated banking service: **N-A / third parties** (Xero is not a deposit institution; payments run through partners).
- What the customer actually receives: A software subscription — an accounting ledger, reports, and an API — not an account or fiduciary service.
- Property-management fit: **General-purpose** — no first-party Xero property-management product; PM is served by third-party marketplace add-ons (Re-Leased, Landlord Studio, Loft47). [apps.xero.com/us/industry/property-realty/]
- Documented PM-specific workflows: **none found first-party.** PM concepts are modeled with generic tools: properties/units → Tracking Categories; tenants/owners/vendors → Contacts. [xero_accounting.yaml TrackingCategories, Contacts]
- Trust or fiduciary workflow support: **not documented (first-party).** No Xero-native trust, client-fund, security-deposit, or escrow workflow; such functionality comes from third-party apps. [absence in developer.xero.com; apps.xero.com property category]
- Operational role and dependencies: Xero is the general-ledger/accounting backend. A property manager would still need a PMS (for leases, units, work orders, tenant portals) and, for API-driven bank reconciliation, a partner Bank Feed or a third-party tool.

## Coverage classification (fixed before inspection)
**Recorded deviation:** Xero is a general-purpose accounting platform, not a PMS. Per the scoring boundary "a product is not penalized for a capability that has no legitimate use for its software category," native PM-domain objects (properties, units, leases, tenants-as-first-class, work orders) are **N-A** for this category and are excluded from the C1 sub-map; the PM gap is captured in Provider/PM-fit above. Core objects are the general-ledger accounting set.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Chart of accounts (Accounts, incl. bank accounts) | critical | 3 | Present — full CRUD |
| Contacts (tenants/owners/vendors) | critical | 3 | Present — create/update; archive (no hard delete) |
| Invoices (charges/bills, ACCREC/ACCPAY) | critical | 3 | Present — full write; void via status |
| Payments | critical | 3 | Present — create; delete/reverse via status |
| General ledger (Journals) | critical | 3 | Present — read-only (immutable GL; appropriate) |
| Bank transactions | important | 2 | Present — create/update |
| Bank reconciliation data | important | 2 | **Read-only / limited** — IsReconciled read-only; no statement import or reconcile via API |
| Credit notes | important | 2 | Present — full write |
| Manual journals | important | 2 | Present — create/update |
| Reports (BS, P&L, TB, aged, bank summary) | important | 2 | Present — read-only |
| Tax rates | important | 2 | Present — create/update |
| Tracking categories (PM segmentation) | important | 2 | Present — full CRUD |
| Items / Attachments / POs / Quotes / Budgets | optional | 1 | Present (budgets read-only) |
| Properties / Units / Leases / Work orders | — | — | **N-A** (PM-domain, outside accounting category) |
| Post charges + payments (critical workflow) | critical | 3 | Present — write (createInvoices/createPayment) |
| Create/update leases (critical workflow) | — | — | **N-A** (no lease object) |

## Functional coverage map
- Core objects: Accounts (present, full CRUD), Contacts (present, create/update+archive), Invoices (present, full write), Payments (present, create+delete-via-status), Journals/GL (present, read-only), BankTransactions (present, create/update), CreditNotes/ManualJournals/TaxRates/TrackingCategories/Items (present), Reports (present, read-only), Bank reconciliation (read-only/limited — no API statement import or reconcile).
- Primary operational workflows: read core records (live ✓), post invoices (doc), post payments (doc), create/update contacts & accounts (doc), read reports (live ✓), incremental sync via If-Modified-Since (live ✓).
- Principal lifecycle changes: void/delete invoices, delete/reverse payments, archive contacts/accounts, delete bank transfers/items, status transitions — all via POST status changes (doc).

## Category 1: Functional Coverage and Usefulness: 13.1/15
- C1.1 Object coverage: **yes** — weighted coverage ≈ 97% (33/34); no critical object absent. All core accounting objects present with role-appropriate operations; only the important "bank reconciliation" item is read-only/limited. Live reads returned Accounts (425), Contacts, Invoices (2101), BankTransactions, ManualJournals, Payments, Items, Reports. [xero_accounting.yaml; live battery]
- C1.2 Core operational actions: **yes** *(documentation-graded)* — weighted coverage ≈ 93%; no critical write workflow absent. createInvoices (PUT), createPayment (POST), updateContact (POST), createAccount (PUT) evidenced in spec; writes not live-tested (read-only connection). [xero_accounting.yaml L7605, L11964, L4499, L77]
- C1.3 Delete or lifecycle actions: **yes** *(documentation-graded)* — void/delete/reverse/archive via status changes are broadly available (Invoices Status=VOIDED/DELETED, Payments Status=DELETED, Contacts ARCHIVED, deleteAccount, deleteBankTransfers, deleteItem). [xero_accounting.yaml]
- C1.4 Change notification: **partial** — webhooks cover only Contacts, Invoices, CreditNotes, Prepayments (+ app Subscriptions); no push for Payments, BankTransactions, Accounts, ManualJournals. Efficient incremental polling via If-Modified-Since (18 endpoints) detects the critical changes and was **honored live** (2000→2101 invoices, 2035→0). [xero-webhooks.yaml; xero_accounting.yaml L19841; live battery]
- Score math: earned 3.5 of 4 applicable checks; unrounded fraction = 0.875; category points = (0.875 × 15) = 13.1/15; verification coverage = 100%.
- What this means for you: You can read and change the accounting data your business runs on. You can post invoices and payments, and update contacts and accounts. You cannot import bank statements or reconcile through the API; a partner bank feed or another tool does that. For live updates, plan to poll with the "modified since" filter, because webhooks cover only a few record types.

## Category 2: API Design, Reliability, and Operability: 6.7/10
- C2.1 Modern API conventions: **partial** — resource-oriented HTTP with a versioned base URL (api.xro/2.0) and JSON (via Accept header), but non-standard verbs (PUT=create, POST=update/upsert) and XML by default. Mixed conventions. [xero_accounting.yaml; live JSON reads]
- C2.2 Consistent typing: **partial** — legacy .NET date format `/Date(1476316800000+0000)/` carried alongside ISO `DateString` in the same object. [xero_accounting.yaml; Xero-Java issue #171]
- C2.3 Structured errors: **partial** — write validation returns a structured ValidationException (`ErrorNumber`, `Type`, `ValidationErrors[]`), but **live** a 404 returned plain text and a 401 returned a different JSON envelope — shapes vary across cases; no single stable machine code across all errors. [live battery; Xero-Java issue #171]
- C2.4 Duplicate prevention: **yes** *(documentation-graded)* — first-class `Idempotency-Key` request header (128-char) across write operations. [xero_accounting.yaml $ref idempotencyKey; xero-projects.yaml; idempotency guide]
- C2.5 Graceful handling under load: **yes** — documented 429 + `Retry-After`; live responses carried `X-DayLimit-Remaining`, `X-MinLimit-Remaining`, `X-AppMinLimit-Remaining`. Limits: 60/min, 5000/day, 5 concurrent. [oauth2/limits; live battery]
- C2.6 Pagination for large collections: **yes** — live `Invoices?pageSize=5` returned a `pagination` object {page, pageSize, pageCount 421, itemCount 2101}; Contacts paged 100/page. Total-count signal present. [live battery]
- C2.7 Bulk or incremental export: **partial** — incremental sync via If-Modified-Since works (verified live), but there is no dedicated bulk/async export path; export = paged reads filtered by modified-since. [xero_accounting.yaml; live battery]
- C2.8 Webhook security and delivery: **yes** *(documentation-graded)* — all three legs cited first-party in Xero's webhooks guide (rendered in-browser 2026-08-27): HMAC-SHA256 `x-xero-signature` signatures + Intent-to-Receive validation; a documented **retry policy** (immediate retry, then every 15 minutes for up to 24 hours, then disable + email collaborators); and consumer **replay/idempotency** guidance (events stored up to 31 days and replayed in order; apps must implement idempotency logic and support replayability). [developer.xero.com/documentation/guides/webhooks/overview/; xero-webhooks.yaml]
- C2.9 Concurrency and conflict control: **no** — no ETag/If-Match, no version field, no documented 409 conflict semantics; effectively last-write-wins via UpdatedDateUTC. [xero_accounting.yaml — absence]
- C2.10 Versioning and backward compatibility: **partial** — version "2.0" in the path and a real deprecation process (granular-scopes migration with a Sept 2027 window; deprecation banner seen live), but the versioning contract is informal (single long-lived path version, additive-only, no version negotiation). [xero_accounting.yaml; portal Configuration banner]
- C2.11 Request traceability: **yes** — every live response carried a `Xero-Correlation-Id` GUID usable with support. [live battery; xero-python issue #69]
- C2.12 Service availability and status transparency: **partial** — status.xero.com is public with a dated incident history and scheduled maintenance, but publishes no uptime % or SLA figure. [status.xero.com]
- Score math: earned 8.0 of 12 applicable checks; unrounded fraction = 0.667; category points = (0.667 × 10) = 6.7/10; verification coverage = 100%.
- What this means for you: The API is stable and predictable to run in production. Rate limits, pagination, request tracing, and idempotency are all solid, and you can trace any request with support. Watch three things: dates come in two formats, error shapes are not uniform, and there is no lost-update protection (no ETag/version check), so two writers can overwrite each other.

## Category 3: Access Control and Safe Automation: 4.5/5
- C3.1 Read-only credentials: **yes** — read-only scopes exist and are enforced. Verified live: our read-only token returned 401 on /Journals (scope not granted) and could not write. [oauth2/scopes; live battery]
- C3.2 Scoped credentials: **yes** — granular, per-resource scopes with read/write separation (e.g., accounting.invoices vs accounting.invoices.read). [oauth2/scopes; app Configuration scope list; live]
- C3.3 Multiple keys: **yes** — multiple apps can be created, each with its own client_id/secret; an app supports multiple org connections. [live: My Apps, "New app"]
- C3.4 Rotation and revocation: **yes** — self-serve secret generation ("Generate another secret", seen live), token `revocation_endpoint`, and DELETE /Connections to disconnect a tenant. [openid-configuration; xero-identity.yaml; live portal]
- C3.5 Test and production isolation: **partial** — a free Demo Company exists for development (data isolated as a separate org), but there is no separate sandbox environment or separate credentials; the same app connects to demo or production. [custom-connections guide; live consent screen listed real orgs only]
- Score math: earned 4.5 of 5 applicable checks; unrounded fraction = 0.9; category points = (0.9 × 5) = 4.5/5; verification coverage = 100%.
- What this means for you: You can safely give an app or an AI agent a limited, read-only key, and you can cut off access at any time. This is a strong point. The one gap is testing: there is no true sandbox — you develop against a "Demo Company," which is a separate data set but not a separate environment or key.

## Category 4: Documentation and AI-Agent Readiness: 4.4/5
- C4.1 Complete self-serve reference: **yes** — public, example-rich reference with worked request/response examples for core endpoints (Invoices, Contacts, Payments). [developer.xero.com/documentation/api/accounting/*]
- C4.2 Reliable machine-consumable integration path: **yes** — a maintained OpenAPI 3.0 spec (v17.0.0), six official SDKs (.NET, Java, Node/TS, PHP, Python, Ruby), and an official MCP server + agent toolkit. [github.com/XeroAPI]
- C4.3 AI-readable documentation: **partial** — no llms.txt/llms-full.txt (both 404) and no dedicated Markdown doc corpus, but a comprehensive machine-readable OpenAPI spec (and an official MCP server) serves as an equivalent first-party AI-consumable representation. [developer.xero.com/llms.txt → 404; github.com/XeroAPI/Xero-OpenAPI]
- C4.4 Kept current: **yes** — changelog "Last updated 14 August 2026" with dated entries, deprecation notices (granular scopes → Sept 2027), and per-SDK release notes. [developer.xero.com/changelog]
- Score math: earned 3.5 of 4 applicable checks; unrounded fraction = 0.875; category points = (0.875 × 5) = 4.4/5; verification coverage = 100%.
- What this means for you: A developer or an AI coding tool can build against Xero without reverse-engineering. The reference is complete, the OpenAPI spec and SDKs are current, and Xero even ships an official MCP server for AI agents. The only soft spot is that there is no llms.txt-style text bundle made just for AI retrieval.

## Category 5: Accessibility and Cost: 11.3/15
- C5.1 Self-serve API key: **yes** — an operator signs up and creates an app and credential with no sales call or approval (verified live in My Apps). [getting-started guide; live]
- C5.3 Not commercially gated: **partial** — a genuinely free path exists (standard app, free Starter tier, 5 connections, API included in all Xero subscriptions), so the API is not behind a premium plan; but meaningful capabilities are tier-gated: the higher rate limit (5,000 vs 1,000 calls/day/org) needs paid Core+ ($35 AUD/mo min), per-GB data-egress fees apply on paid tiers, and the machine-to-machine Custom Connections credential is a paid monthly add-on. [developer.xero.com/pricing; custom-connections guide]
- Score math: earned 1.5 of 2 applicable checks; unrounded fraction = 0.75; category points = (0.75 × 15) = 11.3/15; verification coverage = 100%.
- What this means for you: You can get in the door today for free and connect your own organization at no extra cost beyond your Xero subscription. Costs appear only when you scale — higher call volumes, more connections, or the hands-off machine-to-machine key all move you onto a paid developer tier.

## Total
- Raw: 39.92 / 50
- Normalized before rounding: 79.83 / 100
- Published numeric score: **80 / 100**
- Letter grade: **B-**
- Evidence tier: Baseline verified (read-path live; write checks documentation-graded)
- Overall verification coverage: 100% (gate: no category Unable to verify; overall ≥ 80% — passed)
- Reconciliation (methodology step 12) + evidence follow-up: three independent runs on the frozen packet scored **80 / 80 / 78** and agreed on 25 of 27 checks. Disagreement 1 — **C2.8**: two runs said yes, one partial, because the frozen packet could not cite a webhook retry policy. On 2026-08-27 the operator prompted a re-check; Xero's webhooks guide was then rendered in-browser and explicitly documents the retry policy (immediate, then 15-min intervals, 24 h, then disable) and consumer replay/idempotency guidance, so **C2.8 is finalized yes** (all three legs cited). Disagreement 2 — **C4.3** remains unresolved (partial vs no) and is now the sole swing: partial → 80 (B-), no → 79 (C+). C5.3 held at partial. Result: **80 / 100 (B-)**, boundary with C+ on C4.3.
- Unresolved evaluator disagreements: **C4.3** — partial (comprehensive OpenAPI + official MCP server as an equivalent AI-retrievable representation) vs no (both are already credited in C4.2, and no llms.txt/Markdown doc corpus exists). Score effect: **80 (partial, B-) vs 79 (no, C+)** — this is now the only check that moves the letter grade. C2.8 was finalized yes after the webhooks guide was rendered; C5.3 held at partial on the evidence.

## Bottom line for a property manager
Xero has a strong, mature accounting API. You can build your own tools and AI agents on top of your general ledger — read and post invoices, payments, contacts, accounts, and bank transactions, and pull financial reports — with good rate limits, pagination, tracing, and read-only keys you can revoke. The biggest API limits are no bank-statement import or reconciliation through the API, webhooks for only a few record types (so you poll for the rest), and no lost-update protection on concurrent writes. The biggest fit limit is that Xero is general accounting, not property management: there are no native properties, units, leases, tenants, or work orders, and no first-party trust or security-deposit workflows. You would model properties with Tracking Categories and people with Contacts, and you would still run a separate PMS for leases and maintenance. Treat Xero as an excellent accounting backend to connect to — not a replacement for a PMS, a bank, or a trust-accounting system. Score: 80/100 (B-), Baseline verified — three-run reconciled; C2.8 confirmed yes by the rendered webhooks guide (C4.3 the sole B-/C+ swing).
