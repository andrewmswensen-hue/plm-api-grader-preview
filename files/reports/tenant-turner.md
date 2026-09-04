# API Report Card: Tenant Turner API (v1)

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 5
- Date run: 2026-09-01
- Provisional evidence-packet version or ID: v0.9-provisional (2026-09-01)
- Final evidence-packet version or ID: v1.0-FROZEN (2026-09-01)
- Evidence-discovery mode: tool-enabled discovery + operator-supplied authenticated access to login-gated documentation
- Evidence tier: **Baseline verified**
- Live-write method and safety: none — writes documentation-graded. No sandbox is evidenced; the operator supplied a production key and did not provide the written authorization or labeled test fixtures the controlled live-data protocol requires. No write of any kind was performed.
- Minimum live-test battery: steps 1–5 complete; step 7 N-A (no idempotency documented); steps 6 and 8 not run
- Live tests performed: authenticate; read core resource; cursor pagination across pages; incremental `SinceDateUpdated` query; deliberate error battery (404/400/422/401); rate-limit and traceability header inspection; bounded 25-request throttling probe; ETag/validator inspection
- Live tests not possible: step 6 (create/update a core resource), step 8 (register webhook + trigger event) — both require live-account writes without a sandbox
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8
- Independent grading runs: 3, all on evidence packet v1.0-FROZEN. Runs 2 and 3 were given the frozen packet only — no discovery, no web access, no sight of run 1's marks. Pre-reconciliation totals: 56 / 50 / 51. 23 of 26 checks unanimous.

## Final evidence packet manifest

**Public first-party**
- `https://tenantturner.com/` — product purpose and navigation
- `https://tenantturner.com/plans-pricing/` — Pro/Ultra plans; no API tier gate stated
- `https://tenantturner.com/integrations/`
- `https://api.tenantturner.com/` — API landing page; two auth paths (customer sign-in, Partner API key)
- `https://status.tenantturner.com/` — Atlassian Statuspage: components, 90-day uptime 100.0%, incident history
- Tenant Turner press release, 2026-07-06 (vendor-issued via GlobeNewswire) — API "available to all customers at no cost"; "documentation that lives right in the customer portal"; PropertyTek is the parent portfolio (ShowMojo + Tenant Turner)

**Customer-login-gated first-party, supplied via the operator's authenticated session on 2026-09-01**
- `https://api.tenantturner.com/docs` — Redocly reference, "Tenant Turner API (v1)"; sections: Applications, Multi-Family Properties, Properties, Showings only
- `https://api.tenantturner.com/swagger/v1/swagger.json` — OpenAPI 3.0.1, 14 paths
- `https://app.tenantturner.com/api/key` — API key and webhook signing key; "Refresh API Key"; HMACSHA256 `X-Payload-Signature` documented here
- `https://app.tenantturner.com/api/webhooks` — webhook list (Name / URL / Events / Logs / Actions)
- `https://app.tenantturner.com/api/create-webhook` — 21 webhook trigger event types
- `https://app.tenantturner.com/api/logs` — in-product API request log
- `https://app.tenantturner.com/account/settings` — account-level leasing and syndication configuration

**Verified absent (HTTP 404 / no DNS, 2026-09-01)**
- `tenantturner.com/llms.txt`, `/llms-full.txt`; `help.tenantturner.com/llms.txt`; `api.tenantturner.com/llms.txt`, `/llms-full.txt`, `/openapi.json`, `/robots.txt`; `docs.tenantturner.com`; `developers.tenantturner.com`
- No changelog, release-notes, deprecation, rate-limit, idempotency, ETag/concurrency, or webhook section anywhere in the developer documentation. Spec term scan returned zero hits for rate limit, ratelimit, idempot, webhook, event, subscription, deprecat, etag, if-match, concurren, retry, correlation, request-id, sunset. "429" appears only inside the `HttpStatusCode` enum.

**Located but excluded (third-party, not credited)**
- `github.com/tenantcloud/php-tenant-turner-sdk` — published by TenantCloud, does not claim official status. Not counted as an official SDK under C4.2.

## Evidence-amendment log
- **C4.1, C4.2, C1.1–C1.4, C2.x (all):** The API reference and OpenAPI specification are behind a customer login (`/docs` 302s to OIDC; `/swagger/v1/swagger.json` returns 401). Per methodology rule 4, these were requested from the operator rather than settled as `no`/`unverified`; the operator supplied authenticated access, and the documentation entered the packet on 2026-09-01. Without this step, most of Categories 1, 2 and 4 would have been `unverified: could not access` and the run would have failed the coverage gate.
- **C1.4, C2.8:** Webhooks are entirely absent from the developer documentation and were discovered only in the first-party product interface (`/api/key`, `/api/webhooks`, `/api/create-webhook`) during the controlled verification pass. Added to the manifest; changed C1.4 from a provisional `partial` (polling only) to `yes` within run 1, and C2.8 from provisional `N-A` to `partial`. C1.4 was subsequently returned to `partial` on three-run reconciliation because the events are nowhere documented.
- **C2.11:** In-product API request log at `/api/logs` discovered during the verification pass; changed C2.11 from provisional `no` to `partial`.
- **C5.3:** Vendor press release establishing "available to all customers at no cost" added during the verification pass; changed C5.3 from provisional `unverified` to `yes`.

## API eligibility
- Qualifying API: **yes**
- API operator: Tenant Turner, Inc. [`api.tenantturner.com/swagger/v1/swagger.json`, `info.title` "Tenant Turner API"; portal footer "Copyright © 2013 - 2026 Tenant Turner, Inc."]
- Access or credential issuer: Tenant Turner, Inc., self-serve inside the customer portal [`app.tenantturner.com/api/key`: "All API requests require your account specific private key"]
- Eligibility basis: A first-party REST interface at `https://api.tenantturner.com/v1/*` exposes Tenant Turner's own property, showing and application functions, documented by a vendor-published OpenAPI 3.0.1 specification, with credentials issued self-serve in the vendor's own portal. Confirmed live: `GET /v1/properties` returned HTTP 200 with 189 records from this operator's account on 2026-09-01.

## Context
- Software category: **Leasing or screening tool**
- What the API is for and its core objects and workflows: The Tenant Turner API exposes the pre-application leasing funnel — marketed rental listings, prospect applications and their pre-qualification outcomes, and showing appointments. Its core objects are properties (single-family and multi-family), applications (leads), and showings; its primary workflows are publishing and activating a listing, capturing and pre-qualifying a lead, and booking a showing. Lease documents, screening decisions and accounting live in the connected PMS, not here.

## Provider and property-management fit
- What this product is: An automated leasing platform that markets rentals, pre-qualifies inbound leads, and schedules and controls access for showings. [`tenantturner.com`: "Automate every step from lead to lease—save time, reduce no-shows, and close faster."]
- Bank status, when relevant: **N-A** — no banking, deposit-holding or funds-movement functionality is offered or claimed.
- Who provides any bank account or regulated banking service: **none** — no account, balance, or payment-initiation object exists anywhere in the API surface (14 paths, none financial).
- What the customer actually receives: A software subscription for leasing automation, priced per unit or per listing, plus optional lockbox hardware. [`tenantturner.com/plans-pricing/`: Pro from $1.17/unit annually, Ultra from $2.43/unit annually; MojoBox $64, MojoLock $85 one-time]
- Property-management fit: **PM-specialized** — property management is the product's central purpose and multiple core leasing workflows are documented. [`tenantturner.com` nav sections Listings / Leads / Showings; API objects are properties, applications, showings]
- Documented PM-specific workflows: listing syndication to 12 named rental portals; lead pre-qualification with configurable income-ratio, pet, eviction, bankruptcy and civil-judgment rules; in-person and self-access showing scheduling; electronic lockbox access (CodeBox, SentriLock, PointCentral, iglooworks, Seros); showing confirmation and no-show handling. [`app.tenantturner.com/account/settings`; `api.tenantturner.com/docs`]
- Trust or fiduciary workflow support, when relevant: **N-A** — the product does not hold, move or account for funds. Application and lease-processing fees appear only as descriptive amounts on a listing, not as transactions.
- Operational role and dependencies: Tenant Turner is the top-of-funnel leasing layer; an operator still needs a PMS or accounting platform (this tenant syncs from Rentvine) for applications-of-record, screening decisions, leases, ledgers and payments.

## Coverage classification (fixed before inspection)

Fixed 2026-09-01 before any API documentation was read or any call was made. Recorded deviation from the default Leasing/screening classification: Tenant Turner's documented scope is the pre-application funnel, and credit screening and the lease-document lifecycle happen in the connected PMS. Applying the default names verbatim would mark "screening decision" and "lease lifecycle" as absent critical objects and force C1.1/C1.2 to `no`, measuring product scope rather than API buildability — contrary to the stated scoring boundary. Class structure and weights (3/2/1) are unchanged; only the object and workflow names are mapped onto this leasing subtype.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Listings / marketed rental units | critical | 3 | Present with create, update, activate, deactivate |
| Leads / prospects (application record) | critical | 3 | Present; create and read only, no update |
| Showings / appointments | critical | 3 | Present; create and read only, no update or cancel |
| Lead qualification criteria and outcome | important | 2 | Present with read and a prequalify action |
| Property access / self-access credential | important | 2 | Read-only (config fields absent from write schema) |
| Showing feedback / outcome | important | 2 | Read-only |
| Applications / e-sign documents (PMS handoff) | optional | 1 | Partial — `applicationUrl` only |
| Users / leasing agents | optional | 1 | Partial — read on showings, `assignedUserEmail` on write |
| **Workflow:** create/update a listing and its availability | critical | 3 | Present |
| **Workflow:** capture/update a lead and its qualification state | critical | 3 | Partial — create and qualify, no update |
| **Workflow:** schedule / reschedule a showing | critical | 3 | Partial — create only |
| **Workflow:** issue or manage self-access credential | important | 2 | Absent |
| **Workflow:** record showing outcome / feedback | important | 2 | Absent (read-only) |
| **Workflow:** manage listing syndication targets | optional | 1 | Partial — one boolean flag |
| **Lifecycle:** cancel / reschedule a showing | critical | 3 | Absent |
| **Lifecycle:** mark listing rented / inactive | critical | 3 | Present (`/activate`, `/deactivate`) |
| **Lifecycle:** disqualify or archive a lead | important | 2 | Partial — prequalify only, no archive or decline |
| **Lifecycle:** revoke or expire self-access credential | important | 2 | Absent |
| **Lifecycle:** complete / no-show a showing | important | 2 | Absent |

## Functional coverage map
- **Core objects:** Properties — present, full create/update plus activate/deactivate (critical, 3). Multi-family properties — present, create/update/read. Applications (leads) — present, create/read/prequalify, no update (critical, 3). Showings — present, create/read only (critical, 3). Qualification criteria and outcome — present (important, 2). Self-access credential — read-only (important, 2). Showing feedback — read-only (important, 2). Documents/e-sign — `applicationUrl` string only (optional, 1). Users — partial (optional, 1).
- **Primary operational workflows:** create and update a listing (present); activate/deactivate a listing (present); create an application (present); run pre-qualification and receive `isQualified` plus reasons (present); create a showing with requested times (present); update or cancel a showing (**absent**); write showing feedback (**absent**); configure self-access viewing (**absent from the write schema**).
- **Principal lifecycle changes:** property activate and deactivate are the only lifecycle transitions exposed. There is no DELETE verb anywhere in the specification, no showing cancellation or reschedule, no lead archive or decline, and no self-access credential revocation.

## Category 1: Functional Coverage and Usefulness: 3.8/15

- **C1.1 Object coverage: partial** — weighted coverage = 64.7% (11.0 of 17 weight). Every critical object is present, but two of the three are read-mostly. [`swagger.json` paths `/v1/properties` (post,get), `/v1/properties/{propertyId}` (put,get), `/v1/multifamilyproperties`, `/v1/applications` (post,get), `/v1/applications/{applicationId}` (get), `/v1/showings` (get,post), `/v1/showings/{showingId}` (get); live `GET /v1/properties` → 189 records, 2026-09-01]
- **C1.2 Core operational actions: no** — weighted coverage = 46.4% (6.5 of 14 weight), below the 0.50 threshold. Listings are fully writable (1.0); lead capture plus pre-qualification but no lead update (0.5); showing creation but no reschedule (0.5); self-access credential issuance absent (0.0); showing feedback read-only (0.0); syndication limited to one boolean (0.5). *Documentation-graded — no live write was authorized.* [`swagger.json`: `PropertyPostPutRequest` contains 31 writable fields; `enableSelfAccessViewings`, `selfAccessViewingType`, `selfAccessViewingInstructions`, `enableShowings`, `showingInstructions`, `enableWaitlist` appear in `ApiProperty` responses but are absent from the write schema]
- **C1.3 Delete or lifecycle actions: no** — weighted coverage = 33.3% (4.0 of 12 weight), and a critical lifecycle action is absent: a showing cannot be cancelled or rescheduled through the API. Only property `/activate` and `/deactivate` exist; there is no DELETE verb in the specification. *Documentation-graded.* [`swagger.json` paths: `/v1/properties/{propertyId}/activate` (put), `/v1/properties/{propertyId}/deactivate` (put); `/v1/showings/{showingId}` exposes `get` only]
- **C1.4 Change notification: partial** (reconciled; run 1 marked yes, runs 2 and 3 partial) — weighted coverage = 100% of the critical-plus-important state changes fixed in Step 1. 21 event types are offered, covering lead creation, qualification and disqualification, viewing scheduled / confirmed / cancelled / no-show / feedback, rental activation and deactivation, and lockbox code sent. **Exact limitation:** the check requires *documented* events, and no payload schema, event reference or developer-facing event list is published anywhere — the 21 triggers are discoverable only by opening the webhook form in the product, so a consumer cannot be built from documentation alone. Efficient incremental polling exists as a second mechanism and was verified live. [`app.tenantturner.com/api/create-webhook`, observed 2026-09-01: Lead Created, Lead Archived, Lead Unarchived, Lead Declined, Lead Qualified, Lead Disqualified, Lead Contact Info Updated, Tenant Selected, Viewing Confirmed, Viewing Requested, Viewing Cancelled, Viewing No Show, Viewing Scheduled, Viewing Feedback, Rental Activated, Rental Deactivated, Rental Off Waitlist, Rental On Waitlist, Rental Ready To Activate, Rental Ready To Deactivate, Lockbox Code Sent; live `SinceDateUpdated` filter honored exactly — 2394 → 634 → 54 records as the cutoff tightened]

Score math: earned 1.0 of 4 applicable checks; unrounded fraction = 0.25; category points = 3.75/15 (displayed 3.8); verification coverage = 100%

**What this means for you:** You can read almost everything Tenant Turner knows about your listings, leads and showings, and you can publish and activate a listing end to end. What you largely cannot do is *change* things: no cancelling or rescheduling a showing, no updating a lead, no writing back showing feedback, no turning self-access viewing on or off. The event coverage is genuinely strong — 21 triggers with a signed payload means you can drive a CRM or dashboard in near real time — but for anything beyond listings you will be reading Tenant Turner and acting somewhere else.

## Category 2: API Design, Reliability, and Operability: 4.2/10

- **C2.1 Modern API conventions: yes** — resource-oriented REST over JSON with standard verbs and a `/v1` path version. [`swagger.json`, OpenAPI 3.0.1, 14 paths using GET/POST/PUT; live `GET /v1/properties` → 200]
- **C2.2 Consistent typing: no** — seven core fields are written as numbers and read back as strings on the same resource: `squareFootage` and `bedrooms` (`integer/int32` → `string`), and `bathrooms`, `rentAmount`, `depositAmount`, `applicationFee`, `leaseProcessingFee` (`number/double` → `string`). Confirmed live. The response envelope also differs from the published sample: the API returns `Data` (PascalCase) where the documentation shows `data`. [`swagger.json`, `PropertyPostPutRequest` vs `ApiProperty`; live `GET /v1/properties` 2026-09-01 returned `RentAmount`, `DepositAmount`, `Bedrooms`, `Bathrooms`, `SquareFootage` as JSON strings]
- **C2.3 Structured errors: partial** — a structured JSON body and correct HTTP status semantics are present (404 for a missing id, 400 for a type mismatch, 422 for a missing required parameter, 401 unauthenticated), but there is **no stable machine-readable error code**: the `statusCode` field merely echoes the HTTP status. Error shapes also vary across endpoints — PascalCase `{"StatusCode":404,"ErrorMessages":[...]}` on some paths and camelCase `{"statusCode":400,"errorMessages":[...]}` on others — and 400s return the uninformative `"General error."`. `GET /v1/nosuchresource` returns 404 with an empty body. [`swagger.json` `ApiErrorResponse`; live error battery 2026-09-01]
- **C2.4 Duplicate prevention: no** — no idempotency keys, request identifiers or equivalent mechanism is documented, and `POST /v1/showings` and `POST /v1/applications` are operationally consequential (creating a showing initiates prospect coordination). A retried create can duplicate. Zero specification hits for "idempot". *Documentation-graded.* [`swagger.json`, full-text scan 2026-09-01]
- **C2.5 Graceful handling under load: no** — no documented 429, no `Retry-After`, no backoff guidance; "429" appears in the specification only as a member of the `HttpStatusCode` enum. Throttling behaviour is silent: a bounded 25-request probe returned 25× HTTP 200 with no rate-limit headers of any kind. [live probe 2026-09-01; `swagger.json` scan]
- **C2.6 Pagination for large collections: partial** — cursor pagination on `/v1/showings` and `/v1/applications` works well and returned `totalCount` 2394, a 144-character `nextPage` token, and disjoint ascending pages across two hops. But ordering stability is nowhere documented (only observed), and `/v1/properties` and `/v1/multifamilyproperties` have no pagination at all — the properties list returned all 189 records in a single 443 KB response with no documented cap. [live 2026-09-01; `swagger.json` list parameters]
- **C2.7 Bulk or incremental export: partial** — incremental sync works on standard list endpoints via `SinceDateUpdated` plus cursor pagination, and `/v1/properties/sync` returns a lightweight address list, but there is no dedicated bulk or async export path and **history is capped at two years**: `SinceDateUpdated` is mandatory and rejected beyond that window, so a full historical backfill of showings or applications is impossible. [live: `GET /v1/showings` without the parameter → 422 "SinceDateUpdated is required and must be less than 2 years ago."]
- **C2.8 Webhook security and delivery reliability: partial** — payloads are signed (`X-Payload-Signature`, HMAC-SHA256 over the payload using the account's private key) and per-webhook delivery logs exist in the product, but **no retry policy and no replay or idempotency guidance for consumers is documented anywhere**, and webhooks are absent from the developer documentation entirely. *Documentation- and product-interface-graded; step 8 not run.* [`app.tenantturner.com/api/key`; `app.tenantturner.com/api/webhooks` Logs column, observed 2026-09-01]
- **C2.9 Concurrency and conflict control: no** — no ETag or If-Match, no version field, no documented 409 semantics, and no documented concurrency limits. No validator headers were returned on any live response. [`swagger.json` scan: zero hits for etag, if-match, concurren; live header inspection 2026-09-01]
- **C2.10 Versioning and backward compatibility: partial** — an explicit `/v1` path version exists, but no backward-compatibility policy defining breaking versus non-breaking changes and no deprecation window or notice mechanism was found. Zero specification hits for "deprecat" or "sunset". [`swagger.json` `info.version` "v1"; documentation site has no policy page]
- **C2.11 Request traceability: partial** — responses carry no API request or correlation identifier; the only identifiers present are `x-azure-ref` (Azure Front Door infrastructure) and `Request-Context` (an Application Insights application id, constant across requests). A genuine first-party trace mechanism does exist in the product — `/api/logs` listed this run's exact calls with response code, verb, route and timestamp — but it exposes no unique per-request id and is not mentioned in the developer documentation. [live headers 2026-09-01; `app.tenantturner.com/api/logs` observed showing `200 GET /v1/properties/sync`, `422 GET /v1/applications`, `404 GET /v1/properties/999999999`]
- **C2.12 Service availability and status transparency: yes** — a public Atlassian Statuspage with per-component status, 90-day uptime of 100.0%, and dated incident history. [`status.tenantturner.com`, observed 2026-09-01: components Tenant Turner, CodeBox, SentriLock]

Score math: earned 5.0 of 12 applicable checks; unrounded fraction = 0.416667; category points = 4.1667/10 (displayed 4.2); verification coverage = 100%

**What this means for you:** The shape of the API is fine and the pagination and incremental filters are genuinely well behaved — that part will not fight you. The problems are the ones that bite in production. Money-adjacent numbers arrive as strings, so every rent and deposit needs parsing and your types will not round-trip. Retrying a failed showing creation can double-book a prospect, because nothing prevents duplicates. Nothing tells you what a rate limit is or when you hit one. Nothing protects you from two updates overwriting each other. And you cannot quote a request id to support when something goes wrong.

## Category 3: Access Control and Safe Automation: 1.3/5

- **C3.1 Read-only credentials: no** — a single account key carries the full read and write surface; no read-only credential or read-only integration identity is offered. [`app.tenantturner.com/api/key`, observed 2026-09-01: one key, no scope or permission controls]
- **C3.2 Scoped credentials: no** — the key cannot be restricted to particular resources, actions or a role. It is a single all-powerful account credential. [`app.tenantturner.com/api/key`]
- **C3.3 Multiple keys: no** — the account holds exactly one API key, presented as "your account specific private key", with a single "Refresh API Key" control; there is no facility to issue distinct keys per integration. A separate webhook signing key exists but is a signing secret, not a second API credential. [`app.tenantturner.com/api/key`]
- **C3.4 Rotation and revocation: yes** — self-serve rotation via the "Refresh API Key" button, with explicit vendor instruction to use it. [`app.tenantturner.com/api/key`: "Keep this key secret and refresh the key if you feel your private key is no longer private."]
- **C3.5 Test and production isolation: N-A** — no sandbox or separate test environment is evidenced anywhere in the documentation, the specification (no `servers` block) or the product.

Score math: earned 1.0 of 4 applicable checks (C3.5 N-A, excluded); unrounded fraction = 0.25; category points = 1.25/5 (displayed 1.3); verification coverage = 100%

**What this means for you:** This is the weakest area and the one with real operational risk. There is one key, it can do everything your account can do, and you cannot give a contractor, a vendor or an AI agent a narrower slice. If you hand that key to an automation and it misbehaves, your only lever is to refresh the key — which instantly breaks every other integration using it. With no sandbox either, there is nowhere safe to develop against.

## Category 4: Documentation and AI-Agent Readiness: 1.3/5

- **C4.1 Complete self-serve reference: partial** — the Redocly reference is well structured and example-rich, with request and response samples for all 14 endpoints. Three material limitations: it is **not publicly accessible** (requires a customer login or a Partner API key; `/docs` 302s to OIDC and `/swagger/v1/swagger.json` returns 401); **webhooks are entirely undocumented** despite being a shipped feature with 21 event types, so payload shapes must be reverse-engineered; and the reference is inaccurate in at least two respects — `SinceDateUpdated` is marked optional but is enforced as required, and response samples show a `data` envelope where the API returns `Data`. [`api.tenantturner.com/docs`; live 422 and live `GET /v1/properties`, 2026-09-01]
- **C4.2 Reliable machine-consumable integration path: partial** (reconciled; run 1 marked yes, runs 2 and 3 partial) — an OpenAPI 3.0.1 specification covers all 14 paths with full request and response schemas. **Exact limitation:** three defects each break a generated client and require manual correction — there is no `servers` block, so generated code has no base URL; `SinceDateUpdated` is declared optional but enforced as required, so generated calls return 422; and responses are documented with a `data` envelope where the API returns `Data`, so deserialization fails. No official SDK and no MCP server was found; the PHP SDK on GitHub is published by TenantCloud, a different vendor, and does not claim official status, so it is not credited. [`api.tenantturner.com/swagger/v1/swagger.json`]
- **C4.3 AI-readable documentation: no** — no `llms.txt` or `llms-full.txt` on either the marketing, help or API domain (all 404 on 2026-09-01), no per-endpoint Markdown, and no downloadable plain-text or Markdown documentation corpus. The vendor's July 2026 announcement claims documentation "better formatted for both human developers and AI agents", but no qualifying retrieval artifact was found. The OpenAPI file is credited under C4.2 and is not counted twice here.
- **C4.4 Kept current: no** — no changelog, no release notes, no versioning notes and no deprecation guidance anywhere on the documentation site; zero specification hits for "deprecat" or "sunset". The single July 2026 press release is an announcement, not an ongoing currency mechanism, and gives a reader no way to learn that an endpoint changed.

Score math: earned 1.0 of 4 applicable checks; unrounded fraction = 0.25; category points = 1.25/5 (displayed 1.3); verification coverage = 100%

**What this means for you:** For the REST endpoints, a developer or coding agent handed the OpenAPI file can build quickly and correctly — that part works. Everything around it is thin. The docs sit behind a login, so a coding tool cannot reach them unaided; webhooks, the single most useful capability here, have no documentation at all; and there is no changelog, so the first sign that something changed will be your integration breaking.

## Category 5: Accessibility and Cost: 15.0/15

- **C5.1 Self-serve API key: yes** — the key is generated and visible in the customer portal with a self-serve "Refresh API Key" control. No sales call, support ticket or vendor approval step is involved; this operator's key was present and active, and authenticated successfully on the first live call. [`app.tenantturner.com/api/key`, observed 2026-09-01; live `GET /v1/properties` → 200]
- **C5.3 Not commercially gated: yes** — the vendor states the API update is "available to all customers at no cost", and the published plan comparison ties no API or integration capability to a tier. [Tenant Turner press release, 2026-07-06; `tenantturner.com/plans-pricing/`]

Score math: earned 2.0 of 2 applicable checks; unrounded fraction = 1.0; category points = 15.0/15; verification coverage = 100%

**What this means for you:** Nothing stands between you and the API. If you are a Tenant Turner customer on any plan, the key is already sitting in your portal, it costs nothing extra today, and you can start building this afternoon. This is the category Tenant Turner wins outright.

## Total
- Raw: 25.42 / 50
- Normalized before rounding: 50.83 / 100
- **Published numeric score: 51 / 100** (reconciled across three independent runs; pre-reconciliation totals 56 / 50 / 51)
- **Letter grade: F**
- Evidence tier: Baseline verified
- Overall verification coverage: 100% — 26 applicable checks, all resolved to yes, partial or no; zero unverified; no category Unable to verify (gate: no category below 70%, overall at least 80%) — passed
- Partial-result flag: **yes** — C1.2, C1.3, C2.4 and C2.8 were graded from documentation and product-interface evidence rather than observed writes. A sandbox, or written authorization plus labeled test fixtures under the controlled live-data protocol, would let steps 6 and 8 run and move this to Fully verified.
- Unresolved evaluator disagreements: **none.** Three independent runs on the frozen packet agreed on 23 of 26 checks. The three disagreements were resolved against the evidence rather than averaged:
  - **C1.4 → partial.** Run 1 marked yes on the ground that the 21 events cover 100% of classified state changes and that the documentation gap belongs to C4.1. Runs 2 and 3 both marked partial because the check requires *documented* events and none are published. The majority reading was adopted: "documented" is a stated requirement of the check, and the check's own alternative clause shows it contemplates partial for changes that are detectable but not properly published. Effect: Category 1 from 5.625 to 3.75; score from 55 to 51.
  - **C4.2 → partial.** Run 1 marked yes on spec completeness. Runs 2 and 3 marked partial. Adopted: the missing `servers` block, the wrongly-optional required parameter, and the wrong response-envelope casing are three defects that each break a generated client, matching the check's "requires substantial manual correction" clause. Effect: Category 4 from 1.875 to 1.25; score down 1 point.
  - **C2.1 → held at yes.** Runs 1 and 3 marked yes; run 2 marked partial for the non-standard `Basic {base64(key)}` scheme. Rejected: C2.1's stated criteria are resource orientation and standard verbs, both satisfied. The auth non-conformance is recorded under authentication and does not make the interface "REST-like or mixed conventions."
- Independent confirmation of the run 1 knife-edge call: **all three runs computed C1.2 at 46.4% weighted coverage** against the 50% floor and marked it `no`, runs 2 and 3 from their own per-item tables. The boundary call was confirmed, not overturned.
- Letter grade stability: F in all three runs, and under every single-check alternative either independent evaluator considered (their full plausible ranges were 43–54 and 50–58).

## Bottom line for a property manager

Tenant Turner has done the hard part of access exactly right: the API is free, on every plan, and the key is already in your portal — no sales call, no upgrade, no waiting. What you get for that is a solid read surface over your listings, leads and showings, full write control over listings themselves, and a broad webhook system — 21 signed event triggers that can keep a CRM or dashboard current in near real time. If your goal is "get my leasing data out of Tenant Turner and into something else", you can build that today and it will work, though you will be reverse-engineering the event payloads and correcting the generated client as you go, because neither is documented accurately.

What you cannot build is write-back automation for the things that move fastest. A showing cannot be cancelled or rescheduled through the API, a lead cannot be updated, and showing feedback cannot be written — so any workflow that ends in "and then change it in Tenant Turner" ends with a human in the portal instead. The engineering details compound this: rent and deposit amounts come back as strings even though you write them as numbers, retrying a failed showing creation can double-book a prospect because nothing prevents duplicates, and there is exactly one all-powerful key with no read-only or scoped option and no sandbox — so there is no safe way to hand limited access to an AI agent or a contractor, and rotating the key to cut one integration off cuts them all off.

Read the score for what it measures. This is a rating of API buildability, not of the product: Tenant Turner is a PM-specialized leasing tool that clearly does its job, and it is not a bank, a PMS, or a trust-accounting system — it holds no funds and exposes no financial objects at all. You will still need your PMS (Rentvine, in this account) for applications of record, screening decisions, leases and money. Treat this API as a very good read-and-notify feed with a narrow write path for listings, and keep a person in the loop for showing changes.
