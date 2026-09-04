# API Report Card: Boom — BoomScreen / BoomReport / BoomCRM Partner API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 5 (1M context) — all three runs
- Date run: 2026-09-03
- Provisional evidence-packet version or ID: `boom-ev-v1` (frozen before any check was marked)
- Final evidence-packet version or ID: `boom-ev-v2-final` (frozen after the controlled verification pass; runs 2 and 3 graded this and nothing else)
- Evidence-discovery mode: run 1 tool-enabled discovery; runs 2 and 3 supplied final packet
- Evidence tier: baseline verified
- Live-write method and safety: none — writes documentation-graded. The account owner authorized read-path testing only; live-data write testing was not authorized and no sandbox credential existed. No `POST`, `PATCH` or `DELETE` was issued against any business resource.
- Minimum live-test battery: steps 1–5 complete. Step 6 (create/update) not run — no authorization, no sandbox. Step 7 (idempotency replay) **N-A** — no idempotency mechanism is documented anywhere in the vendor's materials. Step 8 (register webhook, trigger, observe) not run — registration is a write.
- Live tests performed: authenticate; read and page 10 collections across both APIs; pagination repeatability and page-overlap comparison; `per_page` cap probe to 1000; five filter and date-range queries; eleven deliberate error conditions; full response-header capture on 30+ responses across 200/400/401/404; local structural validation of both published specifications.
- Live tests not possible: any create/update/delete; idempotency replay; webhook registration and delivery; rate-limit exhaustion (deliberately not attempted against a production account).
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8
- Credential used: one operator-provisioned production key pair, supplied by the account owner. Key values are not reproduced in this report.
- Data handling: at the account owner's instruction, no tenant, owner, or property identifying values appear in this report or in the evidence packet. Live observations are recorded structurally — field names, JSON types, HTTP codes, envelope keys — and record volumes are given in ranges.

## Final evidence packet manifest

Documentation domain (docs.boompay.app) — sitemap 43 URLs, all retrieved:
- `/` (Overview), `/z1wr-authentication`, `/authentication`, `/environments`, `/api`, `/api-reference`, `/2lks-api-reference`
- `/quickstart` (screening), `/Y14m-quickstart` (rent reporting), `/Od3a-quickstart` (SDK)
- `/screening-api`, `/tenant-screening-boomscreen`, `/rent-reporting-as-a-service`, `/payment-verification`
- `/status-dictionary`, `/webhooks`, `/client-events`, `/support`
- `/software-development-kit`, `/introduction-to-the-boom-sdk`, `/plaid-processor-token-integration`, `/co-branded-configuration`, `/sdk-url-query-params`, `/webview`
- `/listings-iframe-snippets`, `/contact-us-form-snippets`
- 13 OAS endpoint pages: `/adminv1reportingaccountenrollments*`, `/adminv1rentalverifications*`, `/partnerv1authenticationauthenticate`, `/9iwb-partnerv1authenticationauthenticate`
- `docs.boompay.app/llms.txt`; `docs.boompay.app/llms-full.txt` (130,425 bytes); per-page `<slug>.md`

Machine-readable specifications:
- `raw.githubusercontent.com/boompay/api-docs/refs/heads/main/rent-reporting-api-docs/api.json` — Swagger 2.0, "Boom Report API" v1.0.0, 16 paths / 25 operations / 12 definitions
- `raw.githubusercontent.com/boompay/api-docs/refs/heads/main/screening-api-docs/api.json` — OpenAPI 3.0.0, "BoomScreen API" v1.0, 49 paths / 61 operations / 126 schemas
- `github.com/boompay/api-docs` — commit history, last push 2026-08-27
- `github.com/boompay/sdk-integration-sample` — TypeScript sample, last push 2024-10-28

Product, corporate and status:
- `www.boompay.app` — sitemap 119 URLs; `/rent-reporting-as-a-service`; `/integrations` (+ 7 PMS integration pages); `/legal`, `/legal/terms-of-use`
- `www.boompay.app/product-updates` — changelog, most recent entry 2026-09-02
- `www.boompay.app/llms.txt` — note: robots-style AI-crawler directives, not a documentation corpus
- `boompay.statuspage.io` — `/api/v2/summary.json`, `/api/v2/incidents.json`, `/api/v2/components.json`, rendered uptime values
- `registry.npmjs.org/@boompay/screening` — v1.3.0, published 2026-06-10

Operator-supplied product-interface evidence:
- Two screenshots of `portal.boompay.app/settings/api` captured by the account owner 2026-09-03: the API Keys list with the "API key created" dialog, and the "Create API key" dialog showing Access type, Owners and Property groups controls

Live API observations:
- `api.production.boompay.app` — 30+ requests, 2026-09-03 18:25–18:30 UTC

Explicitly excluded (different company, not the evaluated vendor):
- `boom.market` / BoomPay crypto payment gateway; npm `boom-pay-sdk` (repo `lab.git.boom.market`)

## Evidence-amendment log
- **C2.4, C2.5, C2.9** — keyword sweep of `llms-full.txt`, both specifications and the changelog for idempotency, rate-limit, backoff, ETag, If-Match, 409 and conflict terms. Confirmed absence. The single "rate limit" hit concerns contact-form spam protection; "backoff" was a false positive on "backoffice API"; "sunset" was a false positive on an example property name. Marks unchanged.
- **C2.12** — boompay.statuspage.io JSON endpoints; changelog "Boom status page now available" (2026-03-24). Raised from unverified to **yes**.
- **C3.1, C3.2, C3.4** — changelog "Scoped API keys" and "Read-only API access" (2026-03-31), "API key regeneration warning" (2026-04-08); operator screenshot of the Create API key dialog. Raised from unverified to **yes**.
- **C4.4** — `www.boompay.app/product-updates`; `boompay/api-docs` commit history. Raised from partial to **yes**; held at yes through reconciliation.
- **C4.2** — npm registry record for `@boompay/screening`; structural validation of both specs. Run 1 held at yes; **reduced to partial in reconciliation**. The npm package is a React UI component library, not an API client.
- **C5.3** — `www.boompay.app` sitemap (no pricing page); `/legal`; changelog scan for tier, add-on and upgrade language. Run 1 set yes; **reduced to partial in reconciliation**.

Runs 2 and 3 added no sources; they graded the frozen packet only.

## API eligibility
- Qualifying API: **yes** (unanimous across all three runs)
- API operator: Boom. Both specifications are published under the vendor's own GitHub organisation and served from vendor-controlled hosts `api.production.boompay.app` and `api.sandbox.boompay.app` [screening spec `servers` block; docs `/environments`]
- Access or credential issuer: Boom, self-serve through the Boom Partner Platform at `portal.boompay.app/settings/api` [operator screenshots, 2026-09-03]
- Eligibility basis: a live production credential issued by Boom authenticated against Boom's own host and returned Boom's own records across both product APIs. The interface exposes the evaluated vendor's functions directly, not another provider's.

## Context
- Software category: **leasing / screening tool** (chosen independently by all three runs)
- What the API is for and its core objects and workflows: Boom sells three products on one partner platform — BoomScreen (tenant screening: applications, applicants, consumer reports, decisions), BoomReport (rent reporting: furnishing rental payment history to Experian, Equifax and TransUnion), and BoomCRM (leasing CRM: leads, listings, magic links). The API's core objects are applications and applicants with their verification reports and decisions, the properties and units they attach to, and — on the reporting side — customers and enrollments carrying lease terms and verified rent payments. Its core workflows are getting an applicant into a screening pipeline, obtaining and acting on a decision, and enrolling a resident so their rent payments reach the bureaus.

## Provider and property-management fit
- What this product is: a rental financial-services platform that screens applicants, reports rent payments to the credit bureaus, and runs a leasing CRM, sold both to property managers directly and as embedded infrastructure to property management software platforms [docs Overview: "today, Boom does this through two offerings: BoomScreen (tenant screening) and BoomReport (rent reporting)…delivered as infrastructure via what we call Rent Reporting-as-a-Service"]
- Bank status, when relevant: **not a bank.** No first-party material reviewed describes Boom as a bank or chartered institution. Boom identifies itself as "a credentialed rental data furnisher with all three major credit bureaus" [docs Overview; `www.boompay.app/legal` — Terms of Use (December 2024) and Privacy Policy carry no banking, money-transmission or fund-custody language]
- Who provides any bank account or regulated banking service: **none evidenced.** The API exposes a `bank_accounts` resource, but the live records contain only a nickname, a routing number and the last four digits of an externally held account — a payout destination for Boom's own billing, not an account Boom provides. Plaid supplies bank-transaction data for payment verification [docs `/payment-verification`]. No bank partner, processor or money transmitter is named in any reviewed material.
- What the customer actually receives: software and a regulated-furnishment service — a screening pipeline that orders consumer reports through Boom's CRA integrations, and a credit-furnishment channel that verifies rent payments and files them to the three bureaus. Billing statements settle Boom's fees against the operator's own bank account. Not an account, not a balance, not custody of anyone's money.
- Property-management fit: **PM-specialized.** Property management is the product's central purpose and multiple core PM workflows are documented [`www.boompay.app/integrations` — first-party integration pages for AppFolio, Buildium, Entrata, ManageAmerica, Quext, Rent Manager, Rentvine, ResMan and Yardi]
- Documented PM-specific workflows: application intake by unit, property or portfolio via magic links; applicant identity, income and housing-history verification; criteria-based decision recommendations; approve / conditionally approve / reject with reasons; push approved applicants to the PMS; resident enrollment in rent reporting; rent-payment verification via ledger share, Plaid, or partner attestation; move-out and unenrollment; per-bureau furnishment records [docs `/screening-api`, `/rent-reporting-as-a-service`, `/payment-verification`, `/status-dictionary`, `/webhooks`]
- Trust or fiduciary workflow support, when relevant: **not documented.** Nothing in the reviewed materials describes trust accounting, client funds, security deposits or escrow, and no such object or endpoint exists in either specification. The financial objects the API exposes — `billing/statements`, `billing/activities`, `bank_accounts` — concern Boom's own fee billing to the operator. The `ledgers` resource accepts a partner's payment-ledger data as evidence that rent was paid, not as a ledger Boom keeps on the operator's behalf.
- Operational role and dependencies: Boom sits beside a PMS rather than replacing one. An operator still needs their property management and accounting system of record for leases and ledgers; Boom handles screening and bureau furnishment and pushes results back into it, with Plaid or shared ledger data behind payment verification.

## Coverage classification (fixed before inspection)

Taken verbatim from the methodology's default table for leasing/screening. No deviation. All three runs used this same table.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Applications | critical | 3 | Present with appropriate operations |
| Screening / decision | critical | 3 | Present with appropriate operations |
| Lease lifecycle | critical | 3 | Materially limited — no lease object; lease terms writable on the reporting enrollment |
| Applicants | important | 2 | Readable and actionable; no create or update of an applicant record |
| Documents / e-sign | important | 2 | Documents read-only; e-sign absent |
| Marketing / listings | optional | 1 | Listings read-only; application links writable |
| Submit an application *(workflow)* | critical | 3 | Partial — creatable by lead conversion; applicant completes it |
| Obtain a screening decision *(workflow)* | critical | 3 | Present with appropriate operations |
| Advance a lease stage *(workflow)* | critical | 3 | Partial — lead and application stages advanceable; no lease stage exists |

**Deviation note.** The default table names "lease lifecycle" as a critical object. Boom has no `/leases` resource — no `Lease` schema among 126 screening schemas, no lease path among 65. It does have a writable lease-term record: the reporting `enrollment`, carrying `move_in_date`, `lease_end_date`, `lease_signed_date`, `lease_month_to_month`, `monthly_rent_amount`, `monthly_rent_day_of_month` and landlord contact, with a `moved_out_date` transition. All three runs independently scored it **0.5**, not 0.0. See "Unresolved evaluator disagreements" for the score effect of the alternative.

## Functional coverage map

- Core objects: `applications` (present, read + eight decision operations; created via lead conversion, no direct create) · `applicants` (readable and actionable — cancel / uncancel / override identity / rerun verification — but no create or update) · verification reports and `stages` (present, read + rerun) · `properties`, `units`, `listings`, `magic_links`, `leads`, `lead_sources`, `users`, `bank_accounts`, `billing` (present) · `customers`, `enrollments`, `ledgers`, Plaid link tokens (present, full CRUD) · **no lease object** · **no e-sign** · **no document upload** · verification templates exist but are explicitly not API-manageable.

- Primary operational workflows: Create a lead and convert it to an application (`POST /partner/v1/leads/{lead_id}/apply`, "Convert lead to application") · generate and deactivate application links (`POST /properties`, `POST /units`, `PATCH /magic_links/{id}`) · retrieve consumer reports and criteria recommendations · decide (`approve` with `conditions` and `conditional_approval`, `reject` with `reasons`, both with `skip_sending_email` and `send_applicants_to_pms`) · create a customer and an enrollment, submit it (`POST /enrollments/{id}/enroll`), attach products, and attest rent payments (`POST /enrollments/{id}/report_rental_payments`).

- Principal lifecycle changes (present): approve · conditionally approve · reject · cancel · uncancel · place on hold · resume · merge · split · override identity · rerun verification · expire identity verification · activate / deactivate magic link · enroll · add products · move out (`PATCH moved_out_date`) · unenroll (`DELETE /enrollments/{id}`) · delete customer, ledger, property, unit, user.

- Principal lifecycle changes (absent): Reverse or undo a decision (the product emits an `application_decision_reverted` webhook and the portal exposes a "configurable undo decision timeframe", but no endpoint in either specification performs it) · void or delete a document · execute, renew or terminate a lease.

## Category 1: Functional Coverage and Usefulness: 7.5/15

- C1.1 Object coverage: partial — weighted coverage = 75–79% (all three runs computed within this range; the mark is stable across it). Applications and screening decisions present with required operations; lease lifecycle 0.5; documents/e-sign 0.5 (readable via `GET /partner/v1/applicants/{id}/additional_documents`, not requestable or uploadable, no e-sign anywhere); listings read-only; applicants readable and actionable but not creatable or updatable. No critical object absent. [screening spec `/partner/v1/applications`, `/applications/{id}/applicants/{applicant_id}`, `/applicants/{id}/additional_documents`, `/listings`; rent-reporting spec `/partner/v1/enrollments`; live reads of 10 collections 2026-09-03]
- C1.2 Core operational actions: partial — weighted coverage = 65–71% across the three runs. All three critical write workflows at least partially present, so the API is not observational. Documents score 0.0 (read-only where upload is expected); applicants have no create or update; no lease can be created or advanced. Documented but absent from the API: the Screening API page advertises a deployment option where "you can programmatically control the entire BoomScreen workflow, including configuring application settings", while the Quickstart states verification templates "can only be created, updated, and assigned to properties via the Boom Partner Platform (e.g., not programmatically)" — so application cost and decision criteria are portal-only. *Documentation-graded.* [`POST /partner/v1/leads/{lead_id}/apply`; `POST /applications/{id}/approve` (`ApproveApplication`); `POST /applications/{id}/reject` (`RejectApplication`); `POST /partner/v1/enrollments`, `PATCH /enrollments/{id}`, `POST /enrollments/{id}/enroll`]
- C1.3 Delete or lifecycle actions: partial — weighted coverage = 78–80%. The reversal surface is rich: `uncancel` alongside `cancel`, `resume` alongside `place_on_hold`, `merge` and `split`, `expire` on an identity verification, plus move-out and unenrollment. Three gaps hold it under 0.85: **no endpoint reverses a decision** (the webhook `application_decision_reverted` and a portal "undo decision timeframe" exist, but no API path performs it), no endpoint voids or deletes a document, and there is no lease to terminate. *Documentation-graded.* [screening spec `/applications/{id}/{approve,reject,cancel,uncancel,place_on_hold,resume,merge,split}`, `/applications/{id}/applicants/{applicant_id}/{cancel,uncancel,override_identity}`, `/leads/{lead_id}/verifications/identity/expire`, `PATCH /magic_links/{id}`; rent-reporting spec `DELETE /enrollments/{enrollment_id}`, `PATCH` with `moved_out_date`]
- C1.4 Change notification: partial — push coverage = 73–75% weighted; **ceiling 84.6%**. The event catalogue is large (application started/submitted/updated/under review/approved/conditionally approved/declined/canceled/merged/decision reverted; applicant started/submitted; identity verification finished/expired; PMS push; note added; and on reporting: customer registered, enrollment pending/approved/rejected, customer unenrolled with reason codes, furnishment finished, rental payment verified, issue pending/resolved, enrollment moved out). But documents/e-sign is an important object carrying weight 2 of the 13 weighted critical-plus-important state changes and has **no events at all**, so the maximum reachable coverage is 11 ÷ 13 = 84.6% — below the 0.85 bar even if every other item scores 1.0. Polling is thin: `last_updated_from_date`/`last_updated_to_date` exist only on `/applications`, with date ranges on the activity logs and billing; properties, units, leads, customers, enrollments, listings and magic links expose no updated-since filter. [docs `/webhooks`; screening spec `/partner/v1/applications` query parameters; live test confirmed `last_updated_from_date` accepted]

Score math: earned 2.0 of 4 applicable checks; unrounded fraction = 0.5000; category points = 0.5000 × 15 = **7.5/15**; verification coverage = 4/4 = 100%.

What this means for you: You can run the whole screening funnel from your own code — create a lead, turn it into an application, pull the credit, criminal, eviction and income reports, read Boom's recommendation, approve or reject with your own reasons and copy, and have Boom push the approved applicant into your PMS. You can enroll residents in rent reporting, keep lease terms current, and close them out at move-out. What you cannot do is manage a lease (there is no lease record here at all), configure the screening rules, upload or sign a document, or undo a decision through the API even though a person can do it in the portal. Plan on a person in the Boom portal for setup and reversals, and your code for everything in between.

## Category 2: API Design, Reliability, and Operability: 5.0/10

- C2.1 Modern API conventions: yes — resource-oriented REST, standard verbs, JSON, bearer auth, correct status semantics observed live. [docs Overview: "the Boom API is organized around REST…predictable resource-oriented URLs…returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs"; confirmed live across 10 collections and 11 error conditions]
- C2.2 Consistent typing: no — both failure conditions met, on core fields. *Schema vs live:* the rent-reporting spec declares `monthly_rent_amount` as `string` (live returns float), `monthly_rent_day_of_month` as `string` (int), `lease_month_to_month` as `string` (bool), `issues` as `string` (array), and `lat`/`lng` as `string` (float) while declaring the same request parameters `integer`, `boolean` and `number`; `months_delinquency` is typed `string` where the webhook sends a number. *Same concept, different types across endpoints:* monthly rent is `{cents, currency}` on `/partner/v1/units` and on `balance` of `/partner/v1/billing/statements`, but a bare float on `/partner/v1/enrollments` — same host, prefix and credential. *Envelope inconsistency:* nine of ten collections return `has_more`; `/partner/v1/applications` returns `last_page`, contradicting its own `allOf: [PaginatedResponse, …]` composition where `has_more` is required. *One endpoint, two content types:* `POST /partner/v1/authenticate` is `application/json` in the screening spec and `formData` in the rent-reporting spec. [rent-reporting spec definitions `Boom_PartnerAPI_ReportingAccount_Enrollment_BaseEntity`, `Boom_Service_Entities_Address`, `Boom_PartnerAPI_ReportingAccount_RentalVerification_BaseEntity`; screening spec `PaginatedResponse`; live reads 2026-09-03]
- C2.3 Structured errors: partial — correct HTTP semantics with populated stable machine codes on the main paths: `{"error":{"message":"Not Found","status":404,"code":"not_found"}}` and `{"error":{"errors":[…],"message":"…","status":400,"code":"validation_error"}}`. **Exact limitation:** shapes vary. The 401 omits `code` entirely (`{"error":{"message":"Unauthorized","status":401}}`) despite the spec declaring `code` required on that schema; an unknown path returns plain-text `404 Not Found`, not JSON; `TooManyRequestsResponse` types `error` as a bare string where every other error schema uses an object; and the rent-reporting spec attaches no error schema to any 400/401/404/422. Also: malformed JSON on the auth endpoint returns HTTP 400 with `code: "api_error"` and the message "An internal error occurred of type…", presenting a caller mistake as a server fault. [live: 11 deliberate error conditions 2026-09-03; screening spec `ValidatorResponse`, `NotFoundResponse`, `ForbiddenErrorResponse`, `InternalErrorResponse`, `TooManyRequestsResponse`, `ErrorResponse`]
- C2.4 Duplicate prevention: partial — no idempotency mechanism documented anywhere (zero occurrences across both specs, the 130 KB corpus and the changelog). Protection covers a meaningful subset through natural idempotency: `POST /partner/v1/enrollments` returns documented `400 "Customer already have active enrollment"`, and customer "email and phone must be unique, meaning neither element should be present in Boom's system". **Exact limitation:** the consequential writes have none — `POST /enrollments/{id}/report_rental_payments` (furnishes to three bureaus), `POST /applications/{id}/approve` and `/reject` (charge fees, email real applicants), `POST /leads/bulk` (up to 100 records). *Documentation-graded; battery step 7 is N-A.*
- C2.5 Graceful handling under load: partial — 429 documented as a modelled response on 47 of 61 screening operations with a `TooManyRequestsResponse` body. **Exact limitation:** no recovery guidance — no `Retry-After` in either spec, none observed on any of 30+ live responses, no numeric backoff guidance anywhere (the sole "rate limiting" mention in the corpus concerns contact-form spam protection), and the rent-reporting spec documents no 429 at all. Rate-limit exhaustion deliberately not forced against production.
- C2.6 Pagination for large collections: partial — documented offset pagination (`page`, `per_page`) with a strong total-count signal (`total_count`, `page_count`, `current_page`, `has_more`, all four required by `PaginatedResponse`). Live: page 1 repeatable in identical order, page 1 vs page 2 zero overlap, `per_page=1000` returned a several-hundred-record collection whole with no cap encountered. **Exact limitation:** no stable ordering *guarantee* is documented (ordering controls exist on one endpoint only — `order_by`/`order_direction` on rent-reporting `/customers`); the per-page ceiling is undocumented, which the check names explicitly; and the envelope is inconsistent (`/applications` returns `last_page`; the rent-reporting spec documents bare `{"items":[…]}` with no count or next signal). [live repeatability, overlap and cap probes 2026-09-03]
- C2.7 Bulk or incremental export: partial — full datasets obtainable without per-record calls (an entire collection in one `per_page=1000` response; list endpoints return complete objects). **Exact limitation:** no dedicated bulk or export path (`POST /leads/bulk` is a bulk *create*), and incremental sync reaches only applications, activity logs and billing. Properties, units, listings, leads, customers, enrollments and magic links carry `updated_at` but expose no updated-since filter, so warehouse sync means re-reading them whole.
- C2.8 Webhook security and delivery reliability: partial — two of three elements present. *Retry policy documented:* "If your server returns a non-2xx status or is unreachable, we retry 2 times at 1 minute intervals." *Verification present but weak:* "Each webhook request **can** include an `x-api-key` header with the secret token configured for your webhook endpoint" — a static shared secret, not an HMAC; no payload integrity, replayable, and conditionally worded. *Replay/idempotency guidance absent:* every payload carries a unique `request_id`, but nothing instructs consumers to deduplicate on it. Note also that the webhooks page says URLs are "configured per partner — contact support", while the changelog for 2026-08-26 says "To subscribe, open Settings → Webhooks and add your URL" — the documentation is stale. *Documentation-graded; step 8 not run.*
- C2.9 Concurrency and conflict control: no — neither mechanism. No ETag or Last-Modified on any live response including single-resource reads; no `If-Match` or conditional-request support documented; no version, revision or lock field on any entity; `409` appears nowhere across 86 operations. Two integrations writing the same record will silently overwrite one another. [zero matches across both specs and the corpus; live header capture 2026-09-03]
- C2.10 Versioning and backward compatibility: partial — explicit version identifier in the path (`/partner/v1/`, `/crm/v1/`) on all 65 paths, plus `info.version` in both specs. **Exact limitation:** no document defines breaking versus non-breaking changes, states a deprecation window, or commits to a notice period; the only deprecation signalling is four webhook events labelled "(Deprecated)" inline with no removal date; the docs repository publishes no releases and no tags. *(Versioning contract only; currency graded in C4.4.)*
- C2.11 Request traceability: partial — no request or correlation identifier on successful responses; the complete live 200 header set is Date, Content-Type, Transfer-Encoding, Connection, Set-Cookie, Vary, Cache-Control. An identifier exists on part of the error surface: `error_id` (UUID) and `error_signature`, observed live and documented in `InternalErrorResponse`. **Exact limitation:** confined to the `api_error` class, absent from 401, 404, validation failures and every success, not in the schema's required list, and never documented as a reference to quote to support.
- C2.12 Service availability and status transparency: yes — public status page with both required elements: 11 named components including API, BoomScreen and BoomReport; nine resolved incidents 2026-02-04 to 2026-05-19 (two platform outages, a Rent Manager sync failure, an application-submission fault), each with 2–5 updates; per-component uptime percentages over a trailing window for the showcased Portal and API components, tracking from 2025-11-01. Minor drift: the changelog points to `status.boompay.app`, which does not resolve; the working address is `boompay.statuspage.io`. [statuspage summary/incidents/components JSON; changelog 2026-03-24]

Score math: earned 6.0 of 12 applicable checks (2 yes, 8 partial, 2 no); unrounded fraction = 0.5000; category points = 0.5000 × 10 = **5.0/10**; verification coverage = 12/12 = 100%.

What this means for you: The API works, and the parts you touch first are pleasant — clean REST, real pagination with totals that survived a repeat-and-overlap test, validation errors that name the offending field, and a status page with genuine incident history. The weakness is everything you need when an integration runs unattended. No request ID to quote when something goes wrong, no ETag to stop two jobs overwriting each other, no `Retry-After` to back off against, and no idempotency key on the call that files rent payments to the credit bureaus. Budget for defensive code: log your own correlation IDs, serialise your writes, de-duplicate webhooks on `request_id` yourself, and parse what the API actually returns rather than trusting the published rent-reporting schema.

## Category 3: Access Control and Safe Automation: 5.0/5

- C3.1 Read-only credentials: yes — the Create API key dialog presents an **Access type** selector with exactly two options, "Read and write" and "Read-only"; Boom describes the effect as restricting the key "to GET requests only". [operator screenshot of `portal.boompay.app/settings/api` with the Access type menu open, 2026-09-03; changelog "Read-only API access", 2026-03-31]
- C3.2 Scoped credentials: yes — fine-grained resource *and* action scoping. The same dialog carries **Owners** and **Property groups** multi-selects; "when a scoped API key is used, it only returns data associated with the assigned owners or property groups". A separate per-user role model with ~20 named permissions sits alongside it. **Boundary worth knowing:** scoping is organised around owners and property groups; account-level resources such as `bank_accounts` and `billing` are not owner-scoped, so a read-only key can still read Boom billing statements and the nickname, routing number and last four of the linked payout account. [operator screenshot 2026-09-03; changelog "Scoped API keys", 2026-03-31; live reads of `/partner/v1/bank_accounts` and `/partner/v1/users`]
- C3.3 Multiple keys: yes — the API Keys screen lists multiple concurrently active keys, each with its own name, creator and creation timestamp; two were present and enabled, created seventeen months apart, with a "New API" control on the same page. [operator screenshot 2026-09-03]
- C3.4 Rotation and revocation: yes, self-serve — each key row carries an enable/disable toggle and a delete control; secrets can be regenerated in place, and Boom added a confirmation modal in April 2026 because the action is destructive ("Regenerating your API secret key will break any active integration using it"). Secrets are shown once and are non-recoverable. [operator screenshots 2026-09-03; changelog "API key regeneration warning", 2026-04-08]
- C3.5 Test and production isolation: yes — separate environments with separate credentials, documented down to distinct portal, API and SDK hosts; operators are instructed to "make sure you have access to Sandbox and Production, and generate keys in both places". Isolation is stated at the credential level and, critically for this product, at the regulatory level: "You can use the Boom API in Sandbox mode, which doesn't affect your live data or interact with other credit bureaus or consumer reporting agencies. The API key you use to authenticate the request determines whether the request is Live mode or Sandbox mode." Documentation-evidenced only — no sandbox credential was available, so isolation was not exercised live. [docs `/environments`, Overview, `/z1wr-authentication`]

Score math: earned 5.0 of 5 applicable checks; unrounded fraction = 1.0000; category points = 1.0000 × 5 = **5.0/5**; verification coverage = 5/5 = 100%.

What this means for you: This is the best part of the API and the reason it is safe to automate against at all. You can mint a key that is read-only and limited to a single owner's property group, hand it to an agent, a reporting tool or a third party, watch it in a list with the date and the person who made it, and kill it with one toggle. Very few tools in this category let you scope by owner. Keep in mind that owner scoping does not reach Boom's own billing objects, so a read-only key can still see your Boom invoices and payout account details — scope by what the key is for, and do not treat "read-only" as "harmless".

## Category 4: Documentation and AI-Agent Readiness: 3.1/5

- C4.1 Complete self-serve reference: partial — the prose documentation is public and genuinely useful: authentication explained with worked cURL, both quickstarts carrying runnable request bodies, a complete status dictionary, and a webhooks page documenting each BoomReport event with a full JSON payload and the note that amounts are in cents. **Exact limitations:** all thirteen endpoint pages in the documentation navigation are unusable — every one names its base URL as an expired ngrok tunnel (`5739-2607-fb91-…ngrok-free.app/api/admin/v1/…`, created 2024-03-27), every one carries `"jsonExample": ""`, and the `/admin/v1/` family they describe appears in neither published specification; the two "API reference" pages contain nothing but a `jsonFileLocation` pointer to raw GitHub; the rent-reporting spec contains zero response examples and zero operation summaries, so the BoomReport half has no worked response example anywhere; and several instructions are stale (keys said to live under "Settings → Developers" when the screen is "Settings → API"; webhook setup said to require support when the changelog says self-serve). Documented capabilities with no published endpoint include the "applicant experience" submission API, document requests, and webhook subscription management. [all 13 endpoint pages retrieved as Markdown 2026-09-03]
- C4.2 Reliable machine-consumable integration path: partial — the screening specification is strong: OpenAPI 3.0.0, 49 paths / 61 operations, 126 schemas, both servers declared, modelled error responses, hundreds of field examples, every `$ref` resolving, repository last pushed 2026-08-27. **Exact limitation:** no single mechanism covers the API. The screening spec covers a limited subset (it omits all 16 rent-reporting paths); the rent-reporting spec covers those but would generate a materially wrong client — `host: api.sandbox.boompay.app` with no production entry (and `api.boompay.app` does not resolve), `formData` where the live endpoint accepts `application/json`, string types for numeric, boolean and array fields, and list responses documented without the pagination envelope the API returns. That is substantial manual correction. Smaller warts: the screening spec reuses one `operationId` (`ApplicationsController_findReport`) across two operations, breaking strict generators. `@boompay/screening` on npm (v1.3.0, 2026-06-10, nine releases) is a React component library for embedding applicant and identity flows, not an API client, so it is recorded but does not satisfy the check. No MCP server evidenced.
- C4.3 AI-readable documentation: partial — qualifying first-party resources exist and are well formed: `docs.boompay.app/llms.txt` indexes every page, `llms-full.txt` is a 130,425-byte Markdown corpus of all 43 pages, and each page is retrievable as `<slug>.md`. **Exact limitation:** the corpus represents only a fraction of the API — 12 distinct `/partner/v1/` paths appear anywhere in it against 65 in the specifications, the endpoint-level content it does contain is the thirteen broken ngrok pages, and the specifications themselves sit outside the corpus behind GitHub pointers. An AI coding tool fed `llms-full.txt` would come away with an `/admin/v1/` family that does not exist and would miss most of the API. Separately, `www.boompay.app/llms.txt` is not documentation at all — it contains robots-style crawler directives for GPTBot, ClaudeBot, Google-Extended, PerplexityBot, CCBot and YouBot.
- C4.4 Kept current: yes — two independent, current mechanisms. The product changelog publishes at roughly weekly cadence with its most recent entry dated 2026-09-02, the day before this run, and more than ninety dated entries back to March 2026, tagged by product, calling out API changes specifically ("Scoped API keys", "Read-only API access", "Activity log via API" 2026-03-31; "API key regeneration warning" 2026-04-08; "Webhook for notes added to an application" 2026-08-26). The specification repository is a second, finer-grained record with dated, descriptive commits through 2026-08-27 ("add GET /partner/v1/listings endpoint", "fix: screening applications status query param as array (status[])", "docs: add verification_last_updated_at field to Lead schema"). Deprecated webhook events are marked inline. *(Currency of change communication only; the versioning contract is graded in C2.10, and the stale endpoint pages are penalised in C4.1 — not counted twice here.)*

Score math: earned 2.5 of 4 applicable checks; unrounded fraction = 0.6250; category points = 0.6250 × 5 = **3.125/5**, displayed **3.1/5**; verification coverage = 4/4 = 100%.

What this means for you: Point your developer — or your coding assistant — at the OpenAPI file on GitHub, not at the documentation site's endpoint pages. The screening spec is accurate, current and complete enough to generate a working client. The rent-reporting half will cost you a day of trial and error: its spec points at the sandbox host, describes form-encoded bodies the live API does not use, and calls numbers and booleans strings. The endpoint pages in the docs navigation have pointed at a developer's dead tunnel since March 2024 — ignore them. The same applies to AI tools: `llms-full.txt` looks authoritative and will quietly give an agent the wrong endpoint list, so hand it the spec file explicitly. The redeeming feature is that Boom clearly maintains this: the changelog is weekly and the spec repo was updated a week before this evaluation.

## Category 5: Accessibility and Cost: 11.3/15

- C5.1 Self-serve API key: yes — directly observed, unanimous across all three runs. The account owner, a property manager rather than a software partner, created a working production key from Settings → API in their own account at 10:59 on the morning of the run, and it authenticated against the production host minutes later. Creation is a form with a name, an access type, optional scopes and a Save button — no sales call, no ticket, no approval step. Boom's documentation describes a slower route ("Fill out the 'Request API documentation' form… Your request will be reviewed, and you will be emailed and invited to a Sandbox and Production Boom Partner Platform"), but that governs partner onboarding and sandbox provisioning, not credential issuance in an existing account; the entitlement question it raises is scored in C5.3. [operator screenshots 2026-09-03; live authentication 18:25 UTC]
- C5.3 Not commercially gated: partial — no evidence of a premium-plan gate exists: Boom publishes no plan tiers, a changelog sweep for tier, upgrade and add-on language returns only screening product add-ons (TransUnion ResidentScore, Persona TIN verification) with no API entitlement attached, scoped and read-only keys are presented as general platform capabilities without plan qualification, and an ordinary property-management account has held an API key since April 2025. **Exact limitation:** "included or free" is not established either, and that is what *yes* requires. Boom publishes no pricing whatsoever — a 119-URL sitemap with no pricing page, `/pricing` returning 404, every pricing question routed to a sales Typeform ("for details about pricing, contact sales") — the documented key-generation route runs through a request form that "will be reviewed", and the account owner cannot confirm whether their own access carried a plan upgrade or fee and has an open question with Boom. Two adjacent capabilities are also vendor-gated rather than self-serve: sandbox access requires the request form and an invitation, and enhanced-security JWT verification requires contacting Boom. Neither is identity or regulatory verification, so neither is excluded on those grounds. [`www.boompay.app` sitemap; `/legal`; docs `/support`, `/z1wr-authentication`; operator statement 2026-09-03]

Score math: earned 1.5 of 2 applicable checks; unrounded fraction = 0.7500; category points = 0.7500 × 15 = **11.25/15**, displayed **11.3/15**; verification coverage = 2/2 = 100%.

What this means for you: If you are already a Boom customer you are minutes from a working key — Settings → API, name it, pick read-only if that is all you need, save. Nobody to ask, no ticket to file. What you cannot find out from anything Boom publishes is what it costs, because there is no pricing page anywhere and every pricing question routes to a sales form. Confirm in writing that API use carries no charge before you build a dependency on it, and expect to email Boom if you want a sandbox to develop against.

## Total
- Raw: **31.875 / 50**
- Normalized before rounding: **63.75 / 100**
- Published numeric score: **64 / 100**
- Letter grade: **D**
- Evidence tier: **baseline verified**
- Overall verification coverage: **100%** — 27 of 27 applicable checks verified (yes + partial + no); 0 N-A, 0 unverified. Gate satisfied: no category below 0.70 (all five at 1.00); overall ≥ 0.80; tier publishable.
- Partial-result flag: **yes.** Four checks — C1.2, C1.3, C2.4, C2.8 — were graded from first-party documentation rather than observation, because live-data write testing was not authorized and no sandbox credential was available. A sandbox key would resolve all four and lift the run to Fully verified: a create-and-delete on a test property for C1.2 and C1.3, an identical repeated create for C2.4, and a subscription pointed at an operator-controlled endpoint for C2.8. They could move in either direction — C2.4 in particular could fall to *no* if a duplicated `report_rental_payments` call proves to create a duplicate furnishment.
- Unresolved evaluator disagreements: **four, none of which changes the letter grade except the first.**

  | Open question | Raised by | Score | Grade |
  |---|---|---|---|
  | *Published result* — lease lifecycle 0.5, C2.11 partial, C2.6 partial, C4.4 yes | reconciled | 64 | D |
  | **Lease lifecycle scored 0.0 instead of 0.5.** A critical object and a critical write workflow become absent, forcing C1.1 and C1.2 to *no*; Category 1 falls to 3.75. All three runs scored 0.5, but the 0.5 band's wording (read-only where writes are expected, or a missing *non-critical* operation) fits poorly. | run 2 | 56 | F |
  | **C2.11 scored *no*.** An identifier confined to internal-error responses, absent from every success and from 30+ captured headers, and never documented for support use, arguably is not a request identifier at all. | run 2 | 63 | D |
  | **C2.6 scored *yes*.** Ordering stability was observed live, and the methodology says to score live-tested checks on observed behaviour. | run 3 | 65 | D |
  | **C4.4 scored *partial*.** The reference is demonstrably not maintained in step with the API, whatever the changelog says. | run 3 | 63 | D |

  The lease-lifecycle question is the one worth a methodology ruling: what "lease lifecycle" should demand of a screening tool that deliberately hands the lease to a system of record.

## Bottom line for a property manager

You can build real automation on the screening half today — pull applications with their credit, criminal, eviction and income reports, decide with your own criteria, and push approved applicants into your PMS — and you can enroll residents in rent reporting, but there is no lease record, no document upload and no e-signature anywhere in this API, so approval is where Boom stops and your system of record begins. Its biggest strength is access control: read-only keys scoped to a single owner's property group make this one of the few tools in this category you can safely hand to an AI agent or an outside vendor. Its biggest limitation is that the rent-reporting half is unreliable to build against — the published schema disagrees with what the endpoint actually returns on rent amounts and booleans, the documentation's endpoint pages have pointed at a dead developer tunnel since March 2024, and there is no request ID, concurrency control, retry guidance or idempotency key for unattended jobs. Boom is not a bank, no first-party material names any bank, processor or money transmitter behind it, and it documents no trust-accounting, client-fund, security-deposit or escrow workflow — its financial endpoints concern Boom's own billing to you, not money you hold for owners. A score of 64 reflects a narrow API with unreliable documentation rather than a weak product: treat Boom as a screening and credit-reporting layer beside your PMS, your trust accounting and your bank rather than a replacement for any of them, and expect to keep Plaid or shared ledger data behind payment verification.


---

# Appendix: multi-run reconciliation

Not part of the Step 4 output format. Recorded because methodology step 12 requires comparing two or three independent runs at check level, resolving disagreements against the final evidence, and reporting any survivor with its score effect rather than averaging.

Run 1 performed discovery, ran the live battery and assembled the packet. Runs 2 and 3 graded the frozen packet only — no web access, no API calls, no sight of run 1's marks. Marks agreed on **21 of 27 checks**.

## Mark table, all three runs

| Check | Run 1 | Run 2 | Run 3 | Resolved |
|---|---|---|---|---|
| C1.1 | partial | partial | partial | partial |
| C1.2 | partial | partial | partial | partial |
| C1.3 | **yes** | partial | partial | **partial** |
| C1.4 | **yes** | partial | partial | **partial** |
| C2.1 | yes | yes | yes | yes |
| C2.2 | no | no | no | no |
| C2.3 | partial | partial | partial | partial |
| C2.4 | partial | partial | partial | partial |
| C2.5 | partial | partial | partial | partial |
| C2.6 | partial | partial | **yes** | **partial** |
| C2.7 | partial | partial | partial | partial |
| C2.8 | partial | partial | partial | partial |
| C2.9 | no | no | no | no |
| C2.10 | partial | partial | partial | partial |
| C2.11 | partial | partial | partial | partial |
| C2.12 | yes | yes | yes | yes |
| C3.1 | yes | yes | yes | yes |
| C3.2 | yes | yes | yes | yes |
| C3.3 | yes | yes | yes | yes |
| C3.4 | yes | yes | yes | yes |
| C3.5 | yes | yes | yes | yes |
| C4.1 | partial | partial | partial | partial |
| C4.2 | **yes** | partial | partial | **partial** |
| C4.3 | partial | partial | partial | partial |
| C4.4 | yes | yes | **partial** | **yes** |
| C5.1 | yes | yes | yes | yes |
| C5.3 | **yes** | partial | partial | **partial** |

## Totals

| Run | Role | Raw | Normalized | Published | Grade |
|---|---|---|---|---|---|
| Run 1 | discovery, live battery, packet assembly | 40.000 | 80.00 | 80 | B− |
| Run 2 | independent, packet only | 31.875 | 63.75 | 64 | D |
| Run 3 | independent, packet only | 31.667 | 63.33 | 63 | D |
| **Resolved** | each split settled against the frozen evidence | **31.875** | **63.75** | **64** | **D** |

## How each split was resolved

- **C1.3 → partial.** Run 1 built its lifecycle item set from the actions Boom exposes and scored them all 1.0 — the adjust-to-fit error the methodology prohibits, which also let a real gap go unnoticed. Runs 2 and 3 derived items from the *predetermined* critical objects, surfacing lease termination, document void, and decision reversal. They also caught a factual error in run 1: it listed "revert decision" as present, but no endpoint performs it in either specification — only a webhook event and a portal setting exist.
- **C1.4 → partial.** Decided by arithmetic. Documents/e-sign carries weight 2 of the 13 weighted critical-plus-important state changes and has no events, so maximum reachable coverage is 11 ÷ 13 = 84.6%, below the 0.85 bar regardless of how generous every other item is. Run 1 assessed coverage against the events the product emits rather than against the fixed classification.
- **C2.6 → partial** (resolved against run 3). The check requires "a stable ordering guarantee". Observing identical ordering across two calls demonstrates behaviour, not a guarantee, and nothing commits to one. Run 2 adds a second partial trigger the check names explicitly: the per-page ceiling is undocumented.
- **C4.2 → partial.** Run 1 applied the "one strong mechanism is sufficient" clause to the screening spec alone. That clause exists to stop vendors earning extra credit for multiple formats, not to let a spec covering half the API stand for the whole. The screening spec "covers a limited subset"; the rent-reporting spec "requires substantial manual correction". Both partial conditions fire.
- **C4.4 → yes** (resolved against run 3). Run 3 marked it down for the stale endpoint pages, but those already carry their penalty in C4.1, and this check's own text confines it to currency of change communication while warning against counting the same evidence twice.
- **C5.3 → partial.** Run 1 read the absence of any tier-gating statement as evidence of inclusion. That is the "never reward opacity" trap: Boom publishes no pricing at all, so "included or free" is not established, merely not contradicted. The account owner's own uncertainty about whether their access carried a fee is direct evidence that entitlement is unsettled.

Run 1 was the outlier on four of six splits and was corrected on all four, all in the same direction — too generous, and consistently by grading against what Boom has rather than against the fixed classification. The two independents, which never saw each other's work, landed one point apart. The resolved mark set coincides with run 2's by argument rather than deference: on C2.6 and C4.4 the resolution went against run 3 and kept run 1's original marks.
