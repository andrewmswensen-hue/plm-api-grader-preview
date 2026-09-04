# API Report Card: Buildium Open API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 4.8 (claude-opus-4-8)
- Date run: 2026-08-27
- Provisional evidence-packet version or ID: buildium-pkg-2026-08-27-prov1
- Final evidence-packet version or ID: buildium-pkg-2026-08-27-final (frozen)
- Evidence-discovery mode: tool-enabled discovery (operator-supplied OpenAPI spec + first-party web + live read-path access)
- Evidence tier: Baseline verified
- Live-write method and safety: none — writes documentation-graded (operator standing rule: read-only tests only against live production credentials; no sandbox key supplied)
- Minimum live-test battery: read-path steps 1–5 complete; step 6 (write) not performed (read-only rule); step 7 (idempotency) N-A (no idempotency documented); step 8 (webhook) not performed (would require a production subscription + public endpoint)
- Live tests performed: authenticate; read + paginate; incremental/filtered query; deliberate errors (401/404/400); response-header inspection; core-object read sweep; money-typing reads
- Live tests not possible: create/update writes; idempotency replay; webhook round-trip (all avoided under the read-only safety rule)
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8

## Final evidence packet manifest
- Operator-supplied OpenAPI specification (frozen): `evidence/buildium-openapi-v1-frozen-2026-08-27.json` — "Open API, powered by Buildium", openapi 3.0.4, 298 paths, 462 operations. Downloaded by the operator from developer.buildium.com ("Download OpenAPI specification").
- OpenAPI `info.description` embedded developer guide (sections: Getting Started, API Keys, API Overview, Authentication, Rate Limiting, Pagination, Sorting, Response Codes, API Sandbox, Webhooks, Changelog).
- Live read-path battery log: `evidence/buildium-live-battery-2026-08-27.json` (9 GET calls).
- Live follow-up probes log: `evidence/buildium-live-battery2-2026-08-27.json` (20 GET calls).
- https://developer.buildium.com/ — public ReDoc reference portal (rendered, observed 2026-08-27).
- https://www.buildium.com/pricing/ — plan tiers and API entitlement (observed 2026-08-27).
- https://status.buildium.com/uptime and /history — status page with uptime and incident history (observed 2026-08-27).
- https://developer.buildium.com/llms.txt and /llms-full.txt — both return S3 "AccessDenied" (object absent), observed via rendered browser 2026-08-27.

## Evidence-amendment log
- C2.11 (traceability): added live response-header capture (x-amzn-RequestId, X-Amzn-Trace-Id) — no Buildium-documented request identifier found; downgraded doc-provisional "no request id" to partial (identifier present but undocumented).
- C2.3 (structured errors): added live error captures (401/404/400) showing `ErrorCode: null` and `Errors: []`; downgraded provisional "yes" (schema carries ErrorCode) to partial (code never populated in observed responses).
- C2.12 (status): added status.buildium.com/uptime rendered capture confirming uptime percentages + incident history.
- C4.3 (AI docs): added rendered-browser confirmation that /llms.txt and /llms-full.txt are absent (S3 AccessDenied); finalized "no".
- C5.3 (commercial gating): added buildium.com/pricing confirming Open API is exclusive to the top-tier Premium plan.

## API eligibility
- Qualifying API: yes
- API operator: Buildium (the "Open API, powered by Buildium") — OpenAPI `info.title` "Open API, powered by Buildium"; server `https://api.buildium.com/`.
- Access or credential issuer: Buildium — the account holder self-issues API keys in the Buildium web app at Settings → Developer Tools → Create API Key (`info.description` §Creating API Keys).
- Eligibility basis: First-party evidence establishes a versioned REST API that exposes Buildium's own property-management functions (rentals, leases, ledgers, bank accounts, tasks). Authentication uses account-issued client ID + secret headers (`info.description` §Authentication). Verified live on 2026-08-27: `GET https://api.buildium.com/v1/rentals` returned 200 with 1,613 records.

## Context
- Software category: Accounting / PMS platform
- What the API is for and its core objects and workflows: The Buildium Open API lets a property manager read and write the records their business runs on — rental properties, units, leases, tenants, lease ledgers and transactions, the general ledger, bank accounts, owners, bills, vendors, tasks, and work orders. It supports the central workflows of posting ledger charges and payments, creating and updating leases, running bank reconciliations, and reacting to changes through webhooks. Core objects span the Accounting, Rentals, Associations, Maintenance, Communications, and Files domains (OpenAPI `x-tagGroups`).

## Provider and property-management fit
- What this product is: Buildium is a property-management software platform whose Open API exposes the same accounting, leasing, and maintenance data available in the web application. [buildium.com/pricing; OpenAPI `info.description` §Introduction]
- Bank status, when relevant: not a bank. [No first-party evidence identifies Buildium as a bank; it is property-management software.]
- Who provides any bank account or regulated banking service: N-A / none in-API. Buildium records bank accounts, ledgers, and reconciliations as software objects and routes electronic payments through add-on services; it does not itself provide a bank account. [`info.description` §API Sandbox note "Add-on services, ePay and other paid services"; Bank Accounts tag models ledger objects, not a chartered account.]
- What the customer actually receives: a software system of record for property-management accounting and operations, with an API to read and write that data. [OpenAPI `info.description` §Introduction]
- Property-management fit: PM-specialized. [Property management is the product's central purpose; core PM workflows are documented across Accounting, Rentals, Associations, and Maintenance tag groups.]
- Documented PM-specific workflows: rental and association property/unit management; lease lifecycle (create, renew, move-out); lease and ownership-account ledgers (charges, payments, credits, refunds, deposit withholding); bank accounts with checks, deposits, transfers, withdrawals, and reconciliation; owner contributions and statements; work orders, tasks, and vendors; applicant/application transactions. [OpenAPI paths under Leases, Lease Transactions, Bank Accounts, Ownership Account Transactions, Work Orders, Applicants tags]
- Trust or fiduciary workflow support, when relevant: documented. Buildium models property-management trust/client-fund handling — per-lease and per-ownership-account ledgers, security deposits (`LeaseSecurityDepositPostMessage`), deposit withholding (`LeaseLedgerDepositWithholding*`), undeposited funds (`UndepositedFundsMessage`), owner draws/contributions, and bank reconciliation. [OpenAPI schemas and Bank Accounts / Lease Transactions paths]
- Operational role and dependencies: Buildium can serve as the operator's core PMS and accounting system of record; moving money externally still depends on Buildium's ePay/add-on services and the underlying banks, which sit outside the graded API.

## Coverage classification (fixed before inspection — default Accounting/PMS)
| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Properties (Rental Properties) | critical | 3 | Present (GET/POST/PUT) |
| Units (Rental Units) | critical | 3 | Present (GET/POST/PUT) |
| Leases | critical | 3 | Present (GET/POST/PUT + renewals, move-out) |
| Tenants | critical | 3 | Present (GET/POST/PUT) |
| Lease ledgers / transactions | critical | 3 | Present (GET + POST charges/payments/credits/refunds) |
| General ledger | critical | 3 | Present (GET accounts/entries + POST journal entries) |
| Bank accounts | critical | 3 | Present (GET/POST/PUT + checks/deposits/transfers/reconciliation) |
| Owners (rental + association) | important | 2 | Present (GET/POST/PUT) |
| Bills | important | 2 | Present (GET/POST/PUT/PATCH + payments) |
| Payments | important | 2 | Present (lease/ownership/bill payments, deposits) |
| Applicants | important | 2 | Present (GET/POST/PUT + applications) |
| Work orders / tasks | important | 2 | Present (GET/POST/PUT) |
| Reconciliation | important | 2 | Present (GET/POST/PUT + finalize/clear) |
| Files | optional | 1 | Present (GET/POST/PUT + categories) |
| Communications | optional | 1 | Present (GET/POST announcements, emails) |
| Custom fields | optional | 1 | Present (GET/POST/PATCH) |
| Associations (HOA) | optional | 1 | Present (GET/POST/PUT + sub-objects) |
| Inventory & assets | optional | 1 | Present (GET/POST/PUT/DELETE) |
| Workflow: read core records | critical | 3 | Present (verified live) |
| Workflow: post ledger charges + payments | critical | 3 | Present (documented POST endpoints) |
| Workflow: create + update leases | critical | 3 | Present (documented POST/PUT) |

## Functional coverage map
- Core objects: properties **present**, units **present**, leases **present**, tenants **present**, lease ledgers/transactions **present**, general ledger **present**, bank accounts **present** (all critical, weight 3); owners/bills/payments/applicants/work orders+tasks/reconciliation **present** (important, weight 2); files/communications/custom fields/associations/inventory **present** (optional, weight 1). No object absent; none materially read-only where writes are expected.
- Primary operational workflows: create/update properties, units, leases, tenants, owners, vendors, tasks, work orders, bills; post lease and ownership-account charges, payments, credits, refunds; create bank checks, deposits, transfers, withdrawals; create/update/finalize reconciliations; upsert custom-field values.
- Principal lifecycle changes: lease renewal (`POST /v1/leases/{id}/renewals`); lease move-out (`LeaseMoveOutDataPostMessage`); payment reversal (`LeaseLedgerReversePaymentPostMessage`, NSF/other-bank variants); refunds (`OwnershipAccountRefund`, `VendorRefund`, `ApplicationRefund`); reconciliation finalize / clear / unclear transactions; deposit withholding; deletes on 14 endpoints (custom fields, inventory assets, listings, appliances, files, board members).

## Category 1: Functional Coverage and Usefulness: 15.0/15
- C1.1 Object coverage: **yes** — weighted coverage = 100%. Every predetermined critical, important, and optional object is present with role-appropriate operations; no critical object absent. [OpenAPI tags: Bank Accounts (42 ops), Leases (28), Lease Transactions (24), Rental Properties (24), Ownership Account Transactions (23), Rental Units (18), Vendors (17), Bills (14), Tasks (14), General Ledger (10); live 2026-08-27: properties 1,613 / units 2,486 / leases 3,441 / tenants 5,633 / bank accounts 14 / GL accounts 70 / vendors 715 / owners 941 / tasks 18,963 / work orders 5,684 / applicants 9,922 all returned 200]
- C1.2 Core operational actions: **yes** (documentation-graded) — weighted coverage = 100%. Create/update is documented for every critical mutable workflow: `POST /v1/leases` + `PUT /v1/leases/{leaseId}`; lease-ledger `POST` charges/payments/credits; bank-account checks/deposits/transfers; bills; tasks; work orders. No critical write workflow absent. Writes were not executed live under the read-only safety rule. [OpenAPI POST/PUT paths with request-body schemas, e.g. `LeasePostMessage`, `LeaseChargePostMessage`, `LeaseLedgerPaymentPostMessage`, `BankAccountDepositPostMessage`]
- C1.3 Delete or lifecycle actions: **yes** (documentation-graded) — weighted coverage ≈ 95%. Principal lifecycle changes are documented and broad: renewal, move-out, payment reversal, refunds, reconciliation finalize/clear, deposit withholding, and 14 delete endpoints. No critical lifecycle action absent. [`POST /v1/leases/{leaseId}/renewals`; `LeaseMoveOutDataPostMessage`; `LeaseLedgerReversePaymentPostMessage`; `POST .../reconciliations/{id}/finalizerequest`]
- C1.4 Change notification: **yes** — Buildium publishes 91 webhook event types across 32 entities, covering the critical-plus-important state changes (Lease.Created/Updated/Deleted, LeaseTransaction.*, Payment.*, Transaction.*, Rental.*, RentalUnit.*, Tenant.*, BankAccount.*, Bill.*, GLAccount.*, WorkOrder.*, Task.*, Vendor.*, OwnershipAccount*, Applicant*). Incremental polling via `lastupdatedfrom` supplements it. [`info.description` §Webhooks / §Webhook Events]

Score math: earned 4 of 4 applicable checks; unrounded fraction = 1.00; category points = 15.0/15; verification coverage = 100% (4/4).

What this means for you: You can read and change almost everything your business runs on. The API covers properties, units, leases, tenants, ledgers, bank accounts, and work orders. It also pushes near real-time events for the changes that matter. This is one of the most complete property-management APIs available.

## Category 2: API Design, Reliability, and Operability: 7.5/10
- C2.1 Modern API conventions: **yes** — "built upon standard REST conventions ... consistent resource-oriented URLs ... JSON-encoded messages ... standard HTTP status codes and verbs." [`info.description` §API Overview]
- C2.2 Consistent typing: **yes** — schemas and live reads agree and are type-consistent. Money is numeric, not stringly typed. [Schemas: `BankAccountMessage.Balance` number/double, `LeaseTransactionMessage.TotalAmount` number/double; live 2026-08-27: `Balance=40245.91` (float), `TotalAmount=149.9` (float), `IsDefaultGLAccount=true` (bool), ids integer]
- C2.3 Structured errors: **partial** — errors return a structured JSON body (`UserMessage`, `ErrorCode`, `Errors[]`) with correct HTTP status semantics and a usable human message, but the machine-readable `ErrorCode` is not populated. Live 2026-08-27: 404 → `{"UserMessage":"No property found with the id.","ErrorCode":null,"Errors":[]}`; 401 and 400 likewise returned `ErrorCode:null, Errors:[]`. Limitation: no populated, stable machine code to branch on. [Schema `ApiErrorResponse`; `info.description` §Response Codes; live battery step 4]
- C2.4 Duplicate prevention: **no** (documentation-graded) — no request idempotency key or equivalent is documented for consequential writes (payments, charges, deposits). The only idempotency guidance is for webhook *consumers* ("make your event processing idempotent"), not for API requests. Consequential POST retries can create duplicates. [`info.description` §Webhooks/Best Practices; term "idempoten" appears once in the spec, in the webhook-consumer context only]
- C2.5 Graceful handling under load: **yes** — documented `429` plus explicit numeric backoff guidance ("retry ... after a short interval (~200ms)"; "exponential backoff"). Limit stated as 10 concurrent requests per second. [`info.description` §Rate Limiting; §Response Codes]
- C2.6 Pagination for large collections: **yes** — documented `limit`/`offset` (default 50, max 1000), total-count signal `X-Total-Count`, and stable-ordering guidance ("sort on a unique property such as `Id`"). Verified live: pages disjoint, `X-Total-Count=1613` stable across pages. [`info.description` §Pagination / §Sorting Results; live battery step 2]
- C2.7 Bulk or incremental export: **partial** — full datasets can be pulled without per-record calls via list + `limit`/`offset` pagination, and incremental sync via `lastupdatedfrom`/`updateddatetimefrom` is available on many resources (leases, tenants, owners, vendors, tasks, work orders, rentals). But there is no dedicated bulk/export path (no async export jobs or bulk endpoints), and updated-since filters are absent on several core resources — bank accounts (0/11 list endpoints), bills (0/3), most general-ledger and lease-transaction list endpoints. Live: `leases?lastupdatedfrom=2026-01-01` honored (`X-Total-Count=635`). [`info.description` §Bulk Request Options; OpenAPI query-parameter survey]
- C2.8 Webhook security and delivery reliability: **yes** (documentation-graded delivery) — signed payloads (HMAC-SHA256 via `buildium-webhook-signature` + `buildium-webhook-timestamp`), a documented retry policy (retries at 1 minute, 10 minutes, 1 hour; suspension after 20 consecutive failures), and consumer replay/idempotency guidance. Round-trip delivery not executed live. [`info.description` §Webhooks/Receiving Callbacks, /Signature Checks, /Best Practices]
- C2.9 Concurrency and conflict control: **partial** — a `409 Conflict` response is documented and appears on 26 write operations (e.g. update bill, create bill payment, finalize reconciliation, create ownership account), and a concurrency limit is stated (10 concurrent requests/second). But there is no optimistic-concurrency mechanism — no ETag/If-Match and no version/row-version fields (0 occurrences) — so two concurrent updates can silently overwrite each other (last-write-wins). The 409 is a generic state-conflict, not a concurrency token. [`info.description` §Response Codes (409); OpenAPI response survey; absence of ETag/If-Match]
- C2.10 Versioning and backward compatibility: **yes** — explicit major version in the path (`/v1/`), a documented backward-compatible vs backwards-incompatible change policy with advance notice, and concrete deprecation windows (appliance endpoints deprecated in favor of Inventory & Assets, "will start returning `410 Gone` on 2026-10-19", with successor endpoints mapped; 16 operations already carry 410). [`info.description` §API Versioning; §Changelog/Deprecations 2026-07-21]
- C2.11 Request traceability: **partial** — every response carries a unique identifier (`x-amzn-RequestId`, `X-Amzn-Trace-Id`), but these are AWS-infrastructure headers, not a Buildium-documented request/correlation ID, and Buildium's support form asks for date/URL/status/response body rather than a request identifier. Present but undocumented and not clearly usable with support. [Live battery step 5 headers 2026-08-27; `info.description` §Support]
- C2.12 Service availability and status transparency: **yes** — public status page with incident history and uptime percentages. status.buildium.com/uptime (Atlassian Statuspage) showed Buildium Platform uptime June 2026 100%, July 2026 99.94%, August 2026 100%, with an Incidents/history tab. [status.buildium.com/uptime and /history, observed 2026-08-27]

Score math: earned 9.0 of 12 applicable checks (7 yes, 4 partial ×0.5, 1 no); unrounded fraction = 0.75; category points = 7.5/10; verification coverage = 100% (12/12).

What this means for you: The API is modern, well-typed, paginated, versioned, and openly monitored. Rate limits and webhook security are clear. Four gaps need code on your side. Error responses give no stable machine code, so you must match on text or status. There are no idempotency keys, so a retried payment can double-post — you must guard against this. There is no lock to stop two writes from overwriting each other. The only per-request trace id is an AWS header, not a Buildium id for support.

## Category 3: Access Control and Safe Automation: 5.0/5
- C3.1 Read-only credentials: **yes** — "You can restrict a key ... to read-only access (GET resources only)." [`info.description` §Keeping API Keys Safe]
- C3.2 Scoped credentials: **yes** — key creation lets you "choose which pieces of Buildium data you want this API key to have access to by marking the corresponding checkboxes," and keys can be restricted "to particular Buildium entities." Fine-grained resource/action scoping. [`info.description` §Creating API Keys step 5; §Keeping API Keys Safe]
- C3.3 Multiple keys: **yes** — the key-creation flow and management page describe naming keys so you can "locate the right key when you make a request," i.e. multiple distinct keys per account. [`info.description` §Creating API Keys]
- C3.4 Rotation and revocation: **yes** — self-serve delete ("delete this key and start from scratch") and rotation ("regularly recreate your client IDs and secrets from your Buildium account") in Developer Tools. [`info.description` §Creating API Keys; §Keeping API Keys Safe]
- C3.5 Test and production isolation: **yes** — a separate sandbox environment (`https://apisandbox.buildium.com/`) with isolated data, and keys are environment-bound: "Can I use my production keys to access my sandbox? No ... the API keys are restricted to the environment they were created in." [`info.description` §API Sandbox / §Accessing the Sandbox / FAQs]

Score math: earned 5 of 5 applicable checks; unrounded fraction = 1.00; category points = 5.0/5; verification coverage = 100% (5/5).

What this means for you: You can automate safely. Issue a read-only key for a reporting agent. Scope a key to only the data an app needs. Make one key per integration, and delete or rotate any key yourself. Develop against the sandbox with separate keys so you never touch live data.

## Category 4: Documentation and AI-Agent Readiness: 3.75/5
- C4.1 Complete self-serve reference: **yes** — a complete, public (no login) reference at developer.buildium.com rendered with ReDoc, covering authentication, every endpoint, parameters, and per-operation "Request samples"/"Response samples" bodies, plus a worked first-request walkthrough. Minor limitation: response samples are schema-generated placeholders rather than curated realistic values. [developer.buildium.com, observed 2026-08-27 (Request/Response sample panels confirmed in DOM); `info.description` §How to Make a Request]
- C4.2 Reliable machine-consumable integration path: **yes** — a complete, maintained OpenAPI 3.0.4 specification (298 paths, 462 operations) is published and downloadable ("Download OpenAPI specification" on developer.buildium.com). Sufficient for code and tool generation. [frozen spec `evidence/buildium-openapi-v1-frozen-2026-08-27.json`; developer.buildium.com Download control]
- C4.3 AI-readable documentation: **no** — no `llms.txt`, `llms-full.txt`, per-endpoint Markdown, or downloadable Markdown documentation corpus is published. Both `developer.buildium.com/llms.txt` and `/llms-full.txt` return S3 "AccessDenied" (object absent), confirmed in a rendered browser on 2026-08-27. (The OpenAPI spec — machine-readable and carrying a rich embedded Markdown guide — is credited under C4.2, not here.) [rendered-browser checks 2026-08-27]
- C4.4 Kept current: **yes** — a detailed changelog runs monthly from 2020-07 through 2026-08-18 (nine days before this run), including API Updates and dated Deprecations. [`info.description` §Changelog]

Score math: earned 3 of 4 applicable checks; unrounded fraction = 0.75; category points = 3.75/5; verification coverage = 100% (4/4).

What this means for you: A developer or AI tool can build against Buildium without reverse-engineering. The reference is public and complete, and the OpenAPI file drives code generation. The changelog is current and reliable. The one gap is AI-native docs — there is no llms.txt or Markdown corpus — so an AI agent must consume the OpenAPI file itself.

## Category 5: Accessibility and Cost: 7.5/15
- C5.1 Self-serve API key: **yes** — once the account is entitled, an administrator enables the Open API and self-creates keys at Settings → Developer Tools → Create API Key, with no sales call, ticket, or key-approval step. [`info.description` §Enabling the API / §Creating API Keys]
- C5.3 Not commercially gated: **no** — API access is locked to the top-tier plan. The guide states "To take advantage of the Buildium Open API you must have a Premium Subscription," and the pricing page lists "Open API" as exclusive to Premium ($400/month), above Essential ($62) and Growth ($192). [`info.description` §Getting Started note; www.buildium.com/pricing, observed 2026-08-27]

Score math: earned 1.0 of 2 applicable checks (1 yes, 1 no); unrounded fraction = 0.50; category points = 7.5/15; verification coverage = 100% (2/2).

What this means for you: Getting in the door has one real barrier: cost. If you already pay for the Premium plan, key creation is fully self-serve and needs no sales call. But the API is not available on the Essential or Growth plans. You must be on Premium ($400/month) to use it at all.

## Total
- Raw: 38.75 / 50
- Normalized before rounding: 77.50 / 100
- Published numeric score: 78 / 100
- Letter grade: C+
- Evidence tier: Baseline verified
- Overall verification coverage: 100% (gate: no category Unable to verify; overall ≥ 80%) — passed
- Partial-result flag: no. Write-path checks (C1.2, C1.3, C2.4, C2.8) are documentation-graded under the read-only safety rule; a sandbox key would let these be observed and lift the tier to Fully verified.
- Unresolved evaluator disagreements: C2.9 (concurrency) — a strict reading marks it partial (no ETag/version optimistic concurrency); a literal reading of the checklist could mark it yes (documented 409 conflict semantics + a documented concurrency limit satisfy the second "yes" branch). Yes would raise Category 2 to ~7.9 and the total to ~78 (unchanged grade). C4.3 could be read as partial if the OpenAPI's embedded Markdown guide is credited as an AI corpus; that would raise the total to ~79 (unchanged grade, C+).

## Bottom line for a property manager
Buildium's Open API is one of the most complete property-management APIs you can build on today. You can read and change nearly everything — properties, units, leases, tenants, ledgers, bank accounts, bills, tasks, and work orders — and receive near real-time webhooks for the changes that matter. It is a modern, well-typed, versioned REST API with clear docs, a downloadable OpenAPI file, a sandbox, safe read-only and scoped keys, and a public status page. The main API weaknesses are for money-safe automation: no idempotency keys (guard against double-posting a retried payment yourself), no optimistic-concurrency lock, unpopulated machine error codes, and no AI-native docs. The biggest practical barrier is cost, not capability — the API is available only on the Premium plan ($400/month), so operators on Essential or Growth cannot use it. Buildium is property-management software and a strong system of record; it is not a bank, and moving money still depends on its ePay/add-on services and the underlying banks. Documented trust-accounting workflows (per-lease ledgers, security deposits, deposit withholding, reconciliation) make it suitable as the accounting core, subject to your own controls on the write gaps above.
```
