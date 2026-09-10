# API Report Card: MagicDoor (MagicDoor Property Management Platform)

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 5 (claude-opus-5)
- Date run: 2026-09-10
- Provisional evidence-packet version or ID: MD-2026-09-10-P1
- Final evidence-packet version or ID: MD-2026-09-10-F3 (frozen before the published score was calculated; all three grading runs used this packet)
- Evidence-discovery mode: tool-enabled discovery (run 1); supplied final packet (runs 2 and 3)
- Evidence tier: Fully verified, sandbox (staging environment `magicdoor-test.com`, proven isolated from production by A4)
- Live-write method and safety: sandbox (staging). Operator authorized write testing in writing for this session. All writes operated only inside `APITEST-DELETE` sentinel fixtures. No money-moving, notifying, or irreversible operation was run. Cleanup verified: the property list returned to its exact pre-test state of two pre-existing operator fixtures, and every test credential was revoked. Disclosure against Step 10 ("The grader never creates accounts, generates keys, probes endpoints it was not given access to"): this run generated two API keys, later revoked, and used hostname and path enumeration plus decoding of a first-party JavaScript bundle to locate the API, because no published documentation identifies it. C3.1, C3.2 and C5.1 depend on that evidence and are flagged at each check.
- Minimum live-test battery: complete. Steps 1 to 6 performed. Step 7 N-A (the API documents no idempotency for operator writes; the equivalent duplicate probe was run anyway and is cited at C2.4). Step 8 N-A (no operator-facing webhooks).
- Live tests performed: authenticate and confirm the credential; read core resources (properties, units, portfolios, tenants); page through a collection; run filtered queries and confirm they are honored; trigger deliberate 400, 401 and 404 errors; drive the rate limit to a real 429; observe rate-limit and traceability headers; create, read, update and delete a property fixture; send an identical consequential write twice; issue and test two scoped credentials; revoke a credential and confirm rejection; test the staging credential against the production auth host; retrieve a bulk report.
- Live tests not possible: none
- Documentation-graded checks: within C1.2, the ledger-posting and lease-create workflows; within C1.3, every lifecycle action except hard delete. These were graded from first-party specifications because the controlled live-data protocol's hard-exclusion list bars posting charges to a ledger and other money-moving or irreversible operations.

## Final evidence packet manifest

Live API observations (staging, operator-supplied credentials, 2026-09-10):
- `POST https://auth.magicdoor-test.com/api-keys/token`
- `GET/POST/DELETE https://auth.magicdoor-test.com/company-portal/api-keys`, `/company-portal/api-keys/{id}`
- `GET https://auth.magicdoor-test.com/company-portal/permissions`
- `GET https://auth.magicdoor-test.com/.well-known/openid-configuration`, `/.well-known/jwks.json`
- `GET/POST/PUT/DELETE https://api.portal.magicdoor-test.com/company-app/properties`, `/properties/{id}`
- `GET https://api.portal.magicdoor-test.com/company-app/units`, `/portfolios`, `/tenants`, `/reports/rent-roll`
- `POST https://auth.magicdoor.com/api-keys/token` (production host; staging credential rejected 401)

First-party OpenAPI specifications, publicly served with no authentication required, 19 services:
- `https://auth.magicdoor-test.com/openapi/{CompanyPortal,Default,Internal,Debug,OwnerPortal,TenantPortal,VendorPortal}.json`
- `https://api.portal.magicdoor-test.com/openapi/{CompanyApp,CompanyWeb,Default,Debug,Homepage,InternalApp,OwnerApp,TenantApp,VendorApp}.json`
- `https://accounting.magicdoor-test.com/openapi/{CompanyPortal,OwnerPortal,Internal,Debug,Webhook}.json`
- `https://pay.magicdoor-test.com/openapi/{CompanyPortal,OwnerPortal,TenantPortal,VendorPortal,Internal,Debug,Webhook}.json`
- `https://files.magicdoor-test.com/openapi/{Portal,Public,Debug}.json`
- `https://services.magicdoor-test.com/{leasing,maintenance,settings,companies,communications,hoa,audits,ai,subscriptions,salesworkflows,tenantinsurance,productexperiences,education,frauddetection}/openapi/*.json`
- Two registry entries yielded no specification: `webhook.magicdoor-test.com` (empty 200 responses, no spec list) and `ws.magicdoor-test.com` (404)

First-party web pages:
- `https://magicdoor.com/pricing`
- `https://magicdoor.com/features/accounting/trust-accounting`
- `https://magicdoor.com/sitemap.xml` (294 URLs, 79 help articles)
- `https://magicdoor.com/llms.txt` (404)
- `https://status.magicdoor.com/` (no service)
- `https://portal.magicdoor-test.com/` and its build assets on `https://resources.magicdoor-test.com/company-portal/assets/`

Sources referenced but not read, and therefore treated as evidence in neither direction: MagicDoor's terms of service and account agreements; any search for official SDKs; the help article at `magicdoor.com/help/how-to-link-a-bank-account-using-plaid`.

## Evidence-amendment log
- C2.5: provisional marking rested on response headers alone. The controlled verification pass drove the limit to an actual 429 returning `retry-after: 40`. Upgraded to `yes` on observed behavior.
- C3.1, C3.2: provisional marking from `CreateApiKeyDto`, which accepts a `permissions` array, suggested fine-grained scoping. The verification pass tested enforcement twice with two independently scoped credentials, and both writes succeeded. Downgraded to `no`.
- C1.4, C2.8: the verification pass searched every specification across all 19 services for webhook and event-subscription resources. Only four webhook paths exist and all are inbound. C2.8 finalized `N-A`.
- C2.7, C1.4: all 1,510 company-facing operations were parsed for an updated-since style parameter. None exists. C2.7 finalized `partial`.
- C4.2: added the full OpenAPI specification set after establishing it is fetchable without authentication.
- C4.3: `llms.txt` and `llms-full.txt` checked on the vendor and documentation-candidate domains; none exist. Finalized `no`.
- The packet was frozen as MD-2026-09-10-F3 at the close of this pass. No source was added afterward.

## API eligibility
- Qualifying API: yes
- API operator: MagicDoor [tokens issued by `auth.magicdoor-test.com` carry `iss` of that host and `aud` of `magicdoor.com`; 19 first-party services serve the interface]
- Access or credential issuer: MagicDoor, via company-portal API keys [`POST /company-portal/api-keys` returned a working credential; `DELETE /company-portal/api-keys/{id}` revoked it]
- Eligibility basis: An authorized MagicDoor customer obtains an API key from their company portal, exchanges it for a 15-minute Bearer JWT at `POST https://auth.magicdoor.com/api-keys/token`, and calls 1,510 company-facing operations against MagicDoor's own property-management functions. Verified live end to end on staging.

## Context
- Software category: Accounting/PMS
- What the API is for and its core objects and workflows: MagicDoor is an all-in-one property management platform, and its API exposes essentially the whole product surface as REST services. Core objects are portfolios, properties, units, leases, tenants, owners, vendors, lease ledgers (charges, credits, payments, late fees), the general ledger and chart of accounts, bank accounts and reconciliations, work orders and maintenance requests, and rental applications with screening. Core workflows are reading and writing those records, posting ledger charges and payments, running the lease lifecycle from draft through renewal to move-out, and running maintenance from request to work order to vendor bill.

## Provider and property-management fit
- What this product is: An AI-enabled, all-in-one property management software platform sold per unit per month to property management companies [`https://magicdoor.com/pricing`]
- Bank status, when relevant: not evidenced as a bank. No source examined described MagicDoor as a bank or as a provider of regulated banking services. This is an absence of evidence rather than a confirmed negative, because the terms of service were not among the sources read.
- Who provides any bank account or regulated banking service: the operator's own external bank accounts, connected through named third parties. First-party specification enums name them: `pay/CompanyPortal PaymentMethodSetupProvider = [payabli, plaid]`; `apiportal/CompanyApp BankAccountConnectType = [plaid, stripe]`; `PaymentAccountProvider = [plaid, stripe, zelle, none]`; `accounting/CompanyPortal BankFeedSourceType = [plaid, yodlee, manual, pdfImport, csvImport, ofxImport, apiImport]`. The company portal additionally loads `embedded-component.payabli.com` and carries Stripe publishable keys. MagicDoor itself holds no customer bank account in any source examined.
- What the customer actually receives: Property management software with a ledger and accounting system that records and reconciles money held in the operator's own trust and operating bank accounts, plus payment processing and bank connectivity supplied by third parties.
- Property-management fit: PM-specialized [the entire product and all 19 services are property management]
- Documented PM-specific workflows: lease creation, renewal and move-out; rent collection and lease ledger posting; owner distributions and owner statements; management fees; trust accounting; three-way reconciliation and period locks; maintenance requests, work orders and vendor bills; rental applications with TransUnion screening; 1099 filing with IRS IRIS; rent roll, delinquency and general-ledger reporting [endpoint inventory across `accounting`, `leasing`, `maintenance` and `api.portal`; `https://magicdoor.com/features/accounting/trust-accounting`]
- Trust or fiduciary workflow support, when relevant: documented as vendor assertion, not behaviorally verified. The trust-accounting page claims separate trust and operating accounts with no commingling, per-property and per-owner balance tracking, tenant deposits held separately and tied continuously to the trust bank balance, company payout as an explicit audited trust-to-operating transfer, dual-basis atomic posting, and period locks enforced at the data layer. Those are marketing claims. What the API structurally corroborates is the matching object surface: `/company-portal/bank-accounts`, `/manual-reconciliations` with `complete` and `cancel`, `/manual-journal-entries` with `approve`, `post` and `reject`, owner contributions, distributions and transfers, and Bank Ledger Transfers, Deposit Slips and Lease Deposits in the permission catalog. No trust-segregation, period-lock or dual-basis behavior was tested.
- Operational role and dependencies: MagicDoor can serve as the operator's system of record for properties, leases, accounting and maintenance, but it depends on the operator's own bank accounts plus Plaid for bank connectivity and Payabli and Stripe for card and ACH processing.

## Coverage classification (fixed before inspection)

Default Accounting/PMS classification from the methodology, adopted without deviation.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Properties | critical | 3 | Present, full write |
| Units | critical | 3 | Present, full write |
| Leases | critical | 3 | Present, full write |
| Tenants | critical | 3 | Present, full write |
| Lease ledgers / transactions | critical | 3 | Present, full write |
| General ledger | critical | 3 | Present, full write |
| Bank accounts | critical | 3 | Present, full write |
| Owners | important | 2 | Present, full write |
| Bills | important | 2 | Present, full write |
| Payments | important | 2 | Present, full write |
| Applicants | important | 2 | Present, full write |
| Work orders / tasks | important | 2 | Present, full write |
| Reconciliation | important | 2 | Present, full write |
| Files | optional | 1 | Present, full write |
| Communications | optional | 1 | Present, full write |
| Custom fields | optional | 1 | Present, full write |
| Associations | optional | 1 | Present, full write |
| Inventory | optional | 1 | Present but read-only (report endpoint only) |
| Workflow: read core records | critical | 3 | Present |
| Workflow: post ledger charges and payments | critical | 3 | Present |
| Workflow: create and update leases | critical | 3 | Present |

## Functional coverage map

- Core objects: Properties `GET/POST /company-app/properties`, `GET/PUT/DELETE /company-app/properties/{id}`, plus `/deactivate`. Units, tenants, owners and portfolios follow the same pattern. Leases `GET/POST /company-app/leases`, `GET/PUT/DELETE /{leaseId}`. Lease ledger `POST /company-app/leases/{leaseId}/charges`, `/charges/credits`, `/charges/payments`, `GET /charges/ledger`. General ledger `/company-portal/manual-journal-entries` and `/company-portal/chart-of-accounts`. Bank accounts `GET/POST /company-portal/bank-accounts`, `PATCH/DELETE /{bankAccountId}`. Inventory is present only as `GET /company-app/reports/inventory`.
- Primary operational workflows: create and update every core record (create, update and delete on properties verified live); post lease charges, credits and payments; create and update leases, including `/renewals` and `/activate-draft`; create maintenance requests, convert to work orders, assign vendors and produce vendor bills; submit rental applications and request TransUnion screening.
- Principal lifecycle changes: lease `activate-draft`, `renewals/{offerId}/apply`, `renewals/{offerId}/send-signing`, `move-outs` with `accept` and `reject`, `DELETE` lease; ledger `POST /charges/payments/{paymentId}/return` and `DELETE /company-app/checks/{checkId}/void`; `deactivate` on 11 entity types; work-order `status` enum `pending / inProgress / completed / closed / cancelled` via `UpdateWorkOrderStatusDto`; accounting journal entry `approve` / `post` / `reject` and reconciliation `complete` / `cancel`; leasing `POST /company-portal/rental-applications/{id}/decision`.

## Category 1: Functional Coverage and Usefulness: 13.1/15

- C1.1 Object coverage: yes — weighted coverage = 98.7% (37.5 of 38 weight), no critical object absent. Every critical object carries full write operations; only inventory is read-only. [endpoint inventory across the 17 company-facing specifications; `GET /company-app/properties` verified live]
- C1.2 Core operational actions: yes — weighted coverage = 100% (inventory marked N-A within this sub-map as a generated report). All three critical write workflows present. Verified live: `POST /company-app/properties` created id `1547630408379088896`, `PUT` renamed it, `GET` confirmed both. Ledger and lease writes documentation-graded per the hard-exclusion list. [H5, H3]
- C1.3 Delete or lifecycle actions: yes — weighted coverage = 100%. Verified live: `DELETE /company-app/properties/{id}` returned 200 and the record left the collection. Remaining lifecycle actions documentation-graded. [H10 to H14]
- C1.4 Change notification: partial — There is no push mechanism. Across all 19 services only four webhook paths exist, and all are inbound endpoints where TransUnion and bank-feed providers post into MagicDoor; no subscription-management endpoint and no event catalogue exist. No operation among the 1,510 accepts an updated-since, modified-after or delta parameter; only `created.start`/`created.end` and `closedAfter`. The mechanism that carries this to `partial` rather than `no` is `GET /company-portal/audit-entries` on the audits service, whose `entityType` and `entityId` filters are declared optional and whose response returns `AuditEntryAction` of created, updated or deleted, per-field `oldValue`/`newValue` diffs, `occurredAt`, a cross-entity `names` map spanning tenants, owners, vendors, property managers, portfolios, properties, units and leases, and a `nextCursor` for continuation. That is a documented cursor-paginated change feed. It was not exercised in the live battery, its `entityType` values are not enumerated, and no ordering or retention guarantee is stated, so it does not reach `yes`. [G6, G9, specs/audits/CompanyPortal.json]

Score math: earned 3.5 of 4 applicable checks; unrounded fraction = 0.875; category points = 0.875 × 15 = 13.125, displayed 13.1/15; verification coverage = 4/4 = 100%

What this means for you: Almost anything you can do in the MagicDoor screens you can do from code. You can create and update properties, units, leases and tenants, post rent charges and payments to a lease ledger, run renewals and move-outs, and drive maintenance from request through work order to vendor bill. The weak spot is being told when something changes. There are no webhooks and no "what changed since yesterday" filter on any list, so an integration cannot subscribe to events. There is an audit-log endpoint that on paper can be paged as a change feed with before-and-after values, which is the one thing standing between this and a failing mark here, but it is undocumented outside the specification file and we did not exercise it. Plan on polling, and treat that audit feed as something to prototype before you depend on it.

## Category 2: API Design, Reliability, and Operability: 4.1/10

- C2.1 Modern API conventions: yes — Resource-oriented REST over HTTPS with standard verbs and JSON, described by OpenAPI 3.0.4. Verified live across GET, POST, PUT and DELETE.
- C2.2 Consistent typing: partial — Live payloads are type-clean: `totalRent: 1650` and `currentBalance: 1650` are numbers, `active: true` is boolean, and 19-digit snowflake identifiers return as strings. The exact limitation is that the published schemas are not internally consistent about identifier types. 851 path parameters declare identifiers as `integer` against 273 as `string`, and 12 identifier names are declared with both types on different endpoints, including `propertyId`, `leaseId`, `tenantId`, `unitId`, `ownerId`, `vendorId` and `portfolioId`. Separately, 11 company-facing fields carrying `format: snowflake` are typed `integer` while 350 are typed `string`. A 19-digit snowflake typed as a JSON integer exceeds JavaScript's safe integer range. [specs/apiportal/CompanyApp.json, specs/auth/CompanyPortal.json]
- C2.3 Structured errors: partial — Validation failures return a correct RFC 9457 `application/problem+json` body with per-field messages and an echoed `traceId` [D1]. The exact limitations: no populated stable machine-readable error code, only a generic RFC hyperlink identical on every 400; error shapes vary, and one auth-service 400 additionally returned `detail`, `instance` and an `exception` object leaking an internal .NET `ArgumentException` [D4]; a 404 and a 401 both returned completely empty bodies [D2, D3]; and none of the 1,510 operations documents any non-200 response [G1].
- C2.4 Duplicate prevention: no — Verified live: the identical property-create payload sent twice with no intervening change produced two distinct records, ids `1547630408379088896` and `1547630412229459968` [E5]. Zero header parameters are declared across all 1,510 operations, so no idempotency key header exists [G2]. The single idempotency mechanism in the surface is a body field, `PayCompanyInvoiceDto.idempotencyKey` on `POST /company-app/invoices/{billId}/pay`, which protects paying MagicDoor's own subscription invoice and not one operator-consequential write.
- C2.5 Graceful handling under load: yes — Every response carries `x-rate-limit-limit`, `x-rate-limit-remaining` and an ISO `x-rate-limit-reset` [C2]. Verified live by exhausting the limit: request 101 in a one-minute window returned HTTP 429 with a machine-readable `retry-after: 40` [D5]. Scored on observed behavior; this behavior is documented nowhere, which is penalized in Category 4.
- C2.6 Pagination for large collections: partial — A consistent envelope (`items`, `totalCount`, `totalPages`, `page`, `pageSize`) is used by 71 collection endpoints and works live [C1, C3]. The exact limitations: 100 other collection-returning GETs deliver a bare unpaginated array instead [G8, C5]; only 2 of roughly 600 GETs accept any sort or order parameter [G7]; no stable ordering guarantee is stated anywhere; and the staging account held only 2 properties, 4 units and 3 tenants, so traversal of a genuinely large collection was never exercised.
- C2.7 Bulk or incremental export: partial — Full datasets are retrievable without per-record calls via 27 report endpoints, with rent roll verified live returning every property and unit in one response [C6, G13], plus 9 `/batch` fetch-by-id endpoints. The exact limitation: no async export job, no CSV or file export, and no incremental sync of any kind [G6], so every refresh is a full re-pull.
- C2.8 Webhook security and delivery reliability: N-A — No operator-facing webhooks or events exist [G9]. Their absence is scored in C1.4 and is not double-counted here.
- C2.9 Concurrency and conflict control: no — Zero header parameters are declared, so there is no ETag or If-Match [G2]. No 409 semantics are documented; all 1,510 operations document only a 200 [G1]. No concurrency limits are published. Two `version` integer fields exist, on `DepositSlipTransactionSnapshotDto` and `ManualReconciliationTransactionSnapshotDto`, but both are read-only snapshot records with no If-Match or 409 path to use them with, so they are not concurrency tokens.
- C2.10 Versioning and backward compatibility: no — No path carries a `/vN/` segment, every specification's `info` block contains only a `title` with no `version`, and no version header is documented [G4]. No backward-compatibility policy, deprecation window or notice mechanism exists.
- C2.11 Request traceability: partial — Every response carries a unique `x-trace-id`, echoed into error bodies as `traceId` [C2, D1, D4]. The exact limitation: the header is declared in none of the 1,510 operations [G2] and no published support channel references it, so an operator has no documented way to have it used.
- C2.12 Service availability and status transparency: no — No public status page. `status.magicdoor.com` serves nothing and the 294-URL sitemap contains no status, uptime, incident-history or SLA page [I4, I1].

Score math: earned 4.5 of 11 applicable checks (C2.8 N-A); unrounded fraction = 0.4091; category points = 0.4091 × 10 = 4.0909, displayed 4.1/10; verification coverage = 11/11 = 100%

What this means for you: It is a clean modern REST API that behaves well when you push it too hard, returning a proper 429 that tells you exactly how long to wait. Where it will hurt you is production hardening. If a payment-posting call times out and your script retries it, you get a duplicate, which we proved by creating the same property twice. There is no versioning, so MagicDoor can change the API underneath you with no notice and no policy saying they will not. Two people or two automations editing the same record overwrite each other with no conflict warning. There is no status page, so when something breaks you cannot tell whether it is you or them. And the published schemas disagree with themselves about whether a property id is a number or a string, which is the kind of thing that generates a client library that quietly corrupts your identifiers.

## Category 3: Access Control and Safe Automation: 3.0/5

- C3.1 Read-only credentials: no — A read-only credential can be requested but is not enforced, so it is not read-only. `CreateApiKeyDto` accepts a `permissions` array, and a credential created with `{"permissions":["properties:read"]}` returned a JWT correctly carrying `"permissions":"properties:read"`. That credential then executed `POST /company-app/properties` and created a real property, HTTP 200 [F5]. Confirmed with a second, differently scoped credential limited to `audits:read`, which also created a property and read the full tenant list [F6]. Both test properties were deleted and both credentials revoked. Evidence obtained via the Step 10 disclosure recorded in the run metadata.
- C3.2 Scoped credentials: no — Scope is declarable against a granular 144-permission catalog across 53 categories [F1], and it is enforced by the auth service, which correctly refused the `audits:read` credential with 403 on `GET /company-portal/api-keys` [F6]. But the business API at `api.portal.magicdoor-test.com/company-app/*`, which holds every property, unit, lease, tenant and ledger, ignored the scope entirely on two independent tests [F5, F6]. In practice every credential is all-or-nothing over the whole portfolio, for reads and writes alike. Same disclosure as C3.1.
- C3.3 Multiple keys: yes — Four distinct credentials coexisted, each with its own id, name, creation and last-used timestamps [F4, F5, F6, F7].
- C3.4 Rotation and revocation: yes — Fully self-serve. Verified live: `POST /company-portal/api-keys` minted a credential, `DELETE /company-portal/api-keys/{id}` revoked it, re-exchanging the revoked credential returned 401, and the listing showed a populated `revoked` timestamp [F7]. Rotation is create-new plus revoke-old. `CreateApiKeyDto` also declares an `expires` field, but every attempt to use it failed with HTTP 400 ("The UTC Offset for Utc DateTime instances must be 0"), so time-boxed credentials are declared but were never made to work [D4, F3].
- C3.5 Test and production isolation: yes — A separate staging environment exists with its own auth and service hosts and its own credentials [B1, B2]. Verified live: the staging credential was rejected with HTTP 401 by the production host `auth.magicdoor.com` [A4].

Score math: earned 3 of 5 applicable checks; unrounded fraction = 0.6; category points = 0.6 × 5 = 3.0/5; verification coverage = 5/5 = 100%

What this means for you: Key management itself is good. You can mint as many credentials as you want, name them, revoke them instantly yourself, and there is a real staging environment so you can build without risking live data. But the part that matters most for safe automation does not work. MagicDoor lets you create a key labelled read-only, and the API holding your portfolio does not honour that label. We created a key restricted to reading audit records and it went on to create a property and read every tenant. You cannot safely hand a MagicDoor key to a contractor, a third-party app or an AI agent on the assumption it can only look. Treat every key you issue as a full-access admin credential.

## Category 4: Documentation and AI-Agent Readiness: 1.3/5

- C4.1 Complete self-serve reference: no — There is no publicly accessible API reference. The sitemap lists 294 URLs including 79 help articles, and not one concerns the API, developers, webhooks or integrations [I1]. No documentation subdomain exists [I3]. The only reference material is a per-service Swagger UI on hostnames advertised nowhere, located in this run only by decoding a minified service registry out of the company portal's JavaScript bundle [B2, run metadata disclosure]. Even once found, 1,142 of the 1,510 operation descriptions (76%) are the `operationId` echoed back verbatim rather than prose, only 522 of 9,508 DTO properties (5.5%) carry any description, there are zero worked examples [G12], no error response is documented [G1], and the authentication note is a single line that never explains the token-exchange flow [G10].
- C4.2 Machine-consumable path: partial — Complete OpenAPI 3.0.4 specifications exist for 19 services, are fetchable without authentication, and cover all 1,510 company-facing operations with typed schemas, enums and validation constraints [B3, B4, G11]. The exact limitations that require substantial manual correction: not one operation declares any error response, so a generated client models only the success path [G1]; there are no examples [G12]; identifier types conflict across endpoints (see C2.2); and the declared `servers[0].url` omits the path prefix for the 14 services routed under `services.magicdoor-test.com/<name>`, so a generated client would call the wrong URL [B4, B7]. No official SDK was found, though no SDK search was performed [I9]. The pricing page advertises "API/MCP Access", but no MCP server exists in any specification, in the service registry, or at the endpoints tested [I8].
- C4.3 AI-readable documentation: no — No `llms.txt` (404) or `llms-full.txt` [I2], no per-endpoint Markdown, no downloadable documentation corpus [I1]. The OpenAPI files are credited under C4.2 and are not counted twice.
- C4.4 Kept current: partial — 17 operations carry `deprecated: true` and one DTO field carries a migration instruction ("[DEPRECATED] Use ImageSessionId instead") [G5], which is genuine first-party evidence that the specification is maintained as the API changes. The exact limitation: there is no changelog, no release notes, no versioning notes, no dates, no deprecation policy or window, and no channel through which a change would be announced [I5], so a builder has no way to learn that the API has changed.

Score math: earned 1 of 4 applicable checks; unrounded fraction = 0.25; category points = 0.25 × 5 = 1.25, displayed 1.3/5; verification coverage = 4/4 = 100%

What this means for you: This is the weakest part of MagicDoor's API, and it is a documentation problem rather than a capability problem. The API underneath is large and well built, but MagicDoor publishes nothing about it: no developer site, no reference, no examples, no changelog, and no mention of the API in any of their 79 help articles. Three-quarters of the endpoint descriptions are just the function name repeated. The one genuinely valuable asset is a complete machine-readable specification covering every endpoint, which is what a coding tool needs to generate a client, but nothing tells you it exists, it never describes what an error looks like, and its own server addresses are wrong for most of the services. Anyone building here should expect to ask MagicDoor directly for the specification files and base URLs, and to get no warning when something changes.

## Category 5: Accessibility and Cost: 15.0/15

- C5.1 Self-serve API key: yes — Credential creation is self-serve with no sales call, support ticket or approval step. Verified live: credentials were created and revoked over HTTP [F5, F6, F7, F8]. The api-keys endpoints sit on the CompanyPortal audience surface [F2] and `api_keys:read`, `api_keys:write` and `api_keys:delete` are ordinary CompanyPortal permissions [F1]. Disclosed limitation: the company-portal web UI was not accessed in this run, so the mechanism by which an operator obtains a first credential was not directly observed [F8].
- C5.3 Not commercially gated: yes — API access is included on every plan. The pricing comparison table contains a row reading verbatim "API/MCP Access: Included / Included / Included", alongside "All plans include full access to the MagicDoor platform" and "No tiers, no gated features" [I6]. Pricing is $2.50 per unit per month (Advanced) and $3.50 (Professional) month to month, or $1.50 and $2.50 with a one-year contract, Enterprise custom, with a one-time onboarding fee of $500 / $500 / $1,000 and a 25-unit minimum. No tier gates the API.

Score math: earned 2 of 2 applicable checks; unrounded fraction = 1.0; category points = 1.0 × 15 = 15.0/15; verification coverage = 2/2 = 100%

What this means for you: Nothing stands between you and the API. It is included on every plan including the cheapest, MagicDoor explicitly advertises no gated features, and you can create and revoke your own keys without talking to anyone. This is the best-scoring category in the report.

## Total
- Raw: 36.47 / 50
- Normalized before rounding: 72.93 / 100
- Published numeric score: 73 / 100
- Letter grade: C
- Evidence tier: Fully verified, sandbox
- Overall verification coverage: 100% (26 of 26 applicable checks verified, zero unverified; gate requires no category Unable to verify and overall at or above 80%). No category fell below 0.70. Of the 27 checks in the rubric, one (C2.8) is N-A and excluded from the math.
- Partial-result flag: no
- Unresolved evaluator disagreements: Three independent runs graded the same frozen packet MD-2026-09-10-F3. Twenty-two of 27 checks were unanimous. Five disagreed, and each was resolved against the final evidence before this score was calculated. **C1.4** run 1 `no`, runs 2 and 3 `partial`, resolved `partial`: runs 2 and 3 read `specs/audits/CompanyPortal.json` and established that the audit-entries filters are optional and the response is a cursor-paginated created/updated/deleted feed, which the packet's own summary had understated; `no` would give 69 (D+). **C2.2** run 1 `yes`, runs 2 and 3 `partial`, resolved `partial`: both found identifier type conflicts run 1 missed; a strict reading of the `no` trigger, "types vary across endpoints", is literally satisfied and would give 72 (C-). **C4.2** run 1 `yes`, runs 2 and 3 `partial`, resolved `partial` on the undocumented error responses, absent examples and incorrect server URLs. **C4.4** run 1 `no`, runs 2 and 3 `partial`, resolved `partial`; `no` would give 72 (C-). **C3.5** run 2 `partial`, runs 1 and 3 `yes`, resolved `yes` because the `partial` clause is specifically "credential isolation is unclear" and A4 proves isolation directly; `partial` would give 72 (C-). Pre-reconciliation totals were 70, 72 and 73. One check remains materially unresolved by evidence rather than by judgment: **C5.1**, where no run observed how an operator obtains a first credential. All three marked it `yes` by inference; `partial` would give 65 (D), and `unverified` would drop Category 5 coverage to 0.50, below the 0.70 floor, and withhold the numeric score entirely. A single screenshot of the portal's API-keys screen would settle it.

## Bottom line for a property manager

MagicDoor has a genuinely capable API hiding behind almost no documentation. Nearly everything the product does is reachable from code across roughly 1,500 operations, and it is not just readable: we created, renamed and deleted a property live, and you can post rent charges and payments to a lease ledger, run renewals and move-outs, and drive maintenance from request through work order to vendor bill. Access is the easiest of any platform in this category, included on every plan from $1.50 per unit per month on an annual contract, with self-serve keys and a real staging environment to build against. The two things you cannot rely on today are event-driven automation and safe delegation. There are no webhooks and no "what changed since" filter, so integrations must poll; there is an audit feed that looks like it could fill the gap but is undocumented and untested. There is no idempotency protection, so a retried payment call will duplicate. Most seriously, we created an API key scoped to read-only and it created a property and read every tenant, so treat every key you issue as a full-access admin credential and do not hand one to a third-party app or an AI agent expecting it to be limited.

MagicDoor is not evidenced as a bank and does not hold your money. It is the software and the ledger of record; your funds sit in your own trust and operating bank accounts, connected through Plaid, with card and ACH processing run by Payabli and Stripe. Its trust accounting is unusually well specified for a platform at this price, and the API exposes the matching reconciliation, journal-entry and owner-distribution workflows, though this run verified the object surface rather than the accounting behavior itself. The score of 73 reflects a strong, buildable product surface held back by an operability and documentation gap rather than by missing features: enforce the key scopes that already exist, add webhooks and idempotency, publish a developer reference, and this would be among the better property management APIs available. Until then, plan on asking MagicDoor directly for the OpenAPI files and base URLs, budget for polling, and keep your keys tightly held.
