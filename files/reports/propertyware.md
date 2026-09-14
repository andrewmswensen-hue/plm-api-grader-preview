# API Report Card: Propertyware Open API (REST v1)

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude (Anthropic), Cowork session — configured model ID `claude-sonnet-5`; the serving model may differ (the environment reported `claude-opus-5`)
- Date run: 2026-09-11
- Provisional evidence-packet version or ID: PW-2026-09-11-v0.1
- Final evidence-packet version or ID: PW-2026-09-11-v1.0 (frozen; see `Propertyware_API_Evidence_Packet_v1.0.md`)
- Evidence-discovery mode: tool-enabled discovery (web search/fetch, plus an authenticated browser session on the operator's computer for client-rendered and login-gated pages)
- Evidence tier: **Fully verified — sandbox**
- Live-write method and safety: sandbox (operator-provisioned Propertyware test organization, confirmed separate from production). Operator authorization was recorded before any write. Writes were limited to one contact and two $1.00 charges, all labeled APITEST. The API could not delete them (DELETE is beta opt-in), so both charges were deleted in the sandbox UI at the operator's direction and cleanup was verified (lease balance back to $0.00). The test contact was left in the sandbox at the operator's direction. No keys were created and no webhooks were registered.
- Minimum live-test battery: complete. Steps 1–6 were performed. Step 7 is N-A (no idempotency mechanism is claimed). Step 8 is N-A (no webhooks or events are offered).
- Live tests performed: authentication (L1); paged reads of units, contacts and bills (L2); `lastModifiedDateTime` filters on 5 resources (L3); 13 deliberate errors (L4); response-header inspection (L5); general-ledger date-window limits (L6); field-type survey of 17 endpoints (L7); validation errors (L8); contact create and update (L9); lease-charge create, update and identical-resubmission test (L10); DELETE attempts on existing records (L11); deletion visibility to polling (L12)
- Live tests not possible: none required. A 429 response was not deliberately provoked; step 5 only observes signals.
- Documentation-graded checks (baseline verified): none at tier level. Within otherwise live-verified checks, these elements rest on documentation alone: lease status transitions, refunds, bill approval and work-order close (C1.3); lease-payment creation (C1.2); versioning policy (C2.10); status page (C2.12).

## Final evidence packet manifest
- S1 — operator-supplied `swagger2.json` (OpenAPI 3.0.0, "Open API, powered by Propertyware" v1.0). Its canonical content hash matches the spec embedded in U1 on 2026-09-11.
- S2 — operator-supplied screenshots (`pw api info.docx`): the "New API Key" permission dialog and the "Generated API Key" dialog
- U1 — https://app.propertyware.com/pw/apidocs/ (public API reference and changelog)
- U2 — https://www.propertyware.com/open-api/
- U3 — https://www.propertyware.com/pricing/
- U4 — https://www.propertyware.com/
- U5 — https://www.propertyware.com/property-management-accounting/ and https://www.propertyware.com/property-management-accounting/bank-reconciliations/
- U6 — https://www.propertyware.com/terms-of-use/
- U7 — https://www.propertyware.com/blog/propertyware-open-api/
- U8 — https://status.propertyware.com/ (with `/history`, `/history.rss`, `/api/v2/summary.json`, `/api/v2/incidents.json`)
- U9 — https://support.propertyware.com/s/article/Who-do-I-contact-to-request-a-sandbox-testing-account-for-API
- U10 — https://support.propertyware.com/s/article/Creating-an-API-Access-Link-for-a-Report
- U11 — https://support.propertyware.com/s/article/Access-Denied-when-using-Propertyware-API (legacy SOAP API; context only)
- U12 — https://support.propertyware.com/s/article/Create-A-New-API-Key (reviewed; about Google Maps keys, so not relevant)
- U13 — https://www.propertyware.com/sitemap.xml and https://www.propertyware.com/page-sitemap.xml
- U14 — https://www.propertyware.com/llms.txt (404); https://api.propertyware.com/llms.txt and /llms-full.txt (404); https://api.propertyware.com/robots.txt
- U15 — https://www.propertyware.com/whats-new/ (added in the verification pass)
- U16 — https://app.propertyware.com/llms.txt, /llms-full.txt, /pw/apidocs/llms.txt (all 404) and https://app.propertyware.com/robots.txt (added in the verification pass)
- P1 — product-interface observation: Setup › Administration Setup › API Keys in the operator's sandbox, 2026-09-11, view only
- P2 — product-interface observation: sandbox lease ledger, used only for cleanup
- L1–L12 — live-test observations, 2026-09-11 14:18–14:52 UTC (logged in the packet)

## Evidence-amendment log
- C4.3: added U16 (docs-domain `llms.txt` / `llms-full.txt` return 404). Confirms no.
- C4.4: added U15 (the "What's New" page is marketing copy with no dated API release notes). Confirms partial.
- C1.1 and C1.3: a targeted first-party search for bank reconciliation, journal entries, NSF and returned payments found only product-UI help articles, with no API capability. Marks unchanged.
- C5.3: a targeted search for API pricing or enablement found nothing beyond U3 and U7. Unchanged.
- C1.4, C2.4, C2.5, C2.9, C2.11: targeted searches for webhooks, rate limits, idempotency and request IDs returned no first-party results. Unchanged.
- C2.2, C2.3, C2.7, C4.1: targeted searches for error codes, a Postman collection, release notes and export found no new API evidence. Unchanged.
- No mark changed during the verification pass.

## API eligibility
- Qualifying API: **yes**
- API operator: Propertyware — Propertyware LLC, "A RealPage Company" [U1 spec info/contact "Propertyware, support@propertyware.com"; U4 footer; U6]
- Access or credential issuer: the customer's own Propertyware administrator, who creates keys self-serve under Setup › Administration Setup › API Keys [U1 § Creating API Keys; S2; P1]
- Eligibility basis: U1 documents a REST interface at `https://api.propertyware.com/pw/api/rest/v1` that exposes Propertyware's own leasing, accounting, maintenance, contact and document functions (S1: 124 paths, 177 operations). Requests authenticate with account-level API keys: client ID, secret and organization ID headers [U1 § Authentication]. Authentication was live-verified [L1].

## Context
- Software category: **Accounting/PMS**
- What the API is for and its core objects and workflows: Propertyware's Open API gives read/write access to a property manager's system of record. That covers portfolios, buildings, units, leases and tenants, the tenant ledger (charges, payments, refunds, adjustments, journal entries), payables (bills, bill payments, vendor checks), owner draws and contributions, the chart of accounts and general-ledger transactions, prospects and applicants, work orders, documents and custom fields. The core workflows are reading core records, posting ledger charges and payments, and creating and updating leases.

## Provider and property-management fit
- What this product is: cloud property-management and trust-accounting software for residential, especially single-family, management companies [U4 hero text; U5]
- Bank status, when relevant: **not a bank** — Propertyware sells subscription software services [U6]. The bank accounts in the API are the operator's own accounts, recorded as general-ledger accounts with institution, routing and account fields [S1 `AccountDTO`/`SaveAccountDTO`].
- Who provides any bank account or regulated banking service: none; the operator's own banks. Payment processors (ePayments) are not exposed through this API.
- What the customer actually receives: property-management software and its accounting ledger. Propertyware does not provide a deposit account or hold funds.
- Property-management fit: **PM-specialized** [U4; U5; S1 resource list]
- Documented PM-specific workflows: lease creation with security-deposit charge and recurring rent auto-charge [S1 `SaveLeaseDTO`]; notice, move-out and termination through lease status [S1 `PatchLeaseDTO`]; tenant-ledger charges, payments, refunds, adjustments and journal entries [S1 `/leases/*`]; owner draws and contributions [S1 `/accounting/ownerdraws`, `/accounting/ownercontributions`]; building management-fee rules [S1 `GET /buildings/{id}/managementfees`]; bill approval workflow [S1 `PATCH /bills/{id}`]; work orders and tasks [S1 `/workorders`]; prospect/applicant status pipeline [S1 `/prospects/statuses`; live read 2026-09-11 returned "Application In Progress", "Application Submitted", "Converted" and other stages]
- Trust or fiduciary workflow support, when relevant: **limited**. The product markets trust-account management and bank reconciliation [U5: "Manage trust accounts seamlessly"]. The API exposes security-deposit and escrow account designations (`securityDepositAccount`, `escrowAccount`, portfolio `defaultSecurityDepositBankAccountID`, building `defaultSecDepAccID`) and owner-fund transactions. It has no bank reconciliation, no bank-balance or register endpoint, and deposits are write-only [S1].
- Operational role and dependencies: Propertyware is the operator's system of record for leases, the tenant/owner ledger and trust accounting. The operator still needs its own bank(s), plus Propertyware's product UI for reconciliation and for most deletions and voids.

## Coverage classification (fixed before inspection)
| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Properties | critical | 3 | present (full read/write) |
| Units | critical | 3 | present |
| Leases | critical | 3 | present |
| Tenants | critical | 3 | present |
| Lease ledgers / transactions | critical | 3 | present |
| General ledger | critical | 3 | present, limited (lease-scoped journal entries only; reads limited to <30-day windows) |
| Bank accounts | critical | 3 | present, limited (deposits can't be read back; no balance or register) |
| Owners | important | 2 | present |
| Bills | important | 2 | present |
| Payments | important | 2 | present |
| Applicants | important | 2 | present (as prospects with application statuses) |
| Work orders / tasks | important | 2 | present |
| Reconciliation | important | 2 | absent |
| Files | optional | 1 | present |
| Communications | optional | 1 | present, mostly read-only |
| Custom fields | optional | 1 | present |
| Associations | optional | 1 | absent |
| Inventory | optional | 1 | absent |
| Workflow: read core records | critical | 3 | present (live-verified) |
| Workflow: post ledger charges and payments | critical | 3 | present (charges live-verified; payments documented) |
| Workflow: create and update leases | critical | 3 | present (documented) |

The methodology's default Accounting/PMS classification, adopted verbatim and recorded 2026-09-11 14:06:51 UTC. "Associations" is read as HOA/community-association records. Disclosure: the evaluator had listed the spec's path names before recording this table. Because the table is the unmodified methodology default, that exposure could not have shaped it.

## Functional coverage map
- Core objects: Properties 3 = 1.0; Units 3 = 1.0; Leases 3 = 1.0; Tenants 3 = 1.0; Lease ledgers 3 = 1.0; General ledger 3 = 0.5; Bank accounts 3 = 0.5; Owners 2 = 1.0; Bills 2 = 1.0; Payments 2 = 1.0; Applicants 2 = 1.0; Work orders 2 = 1.0; Reconciliation 2 = 0.0; Files 1 = 1.0; Communications 1 = 0.5; Custom fields 1 = 1.0; Associations 1 = 0.0; Inventory 1 = 0.0. Per-item citations are in packet §3.
- Primary operational workflows: post lease charges (`POST /leases/charges`, bulk; live L10), lease payments (`POST /leases/payments`), refunds, adjustments and lease journal entries; create, update and patch leases; create and update properties, units, contacts, owners, bills, bill payments and work orders; update custom fields; upload documents.
- Principal lifecycle changes: lease notice, move-out and termination (1.0); void a charge (0.5, beta-gated delete); reverse a payment or NSF (**0.0**); refund a deposit (1.0); archive a property or unit (0.5, beta-gated); approve or reject a bill (1.0); void a bill or vendor payment (0.5); close a work order (0.5, reference says beta); advance or reject an applicant (1.0); finalize a reconciliation (0.0); delete a document (0.5, beta).

## Category 1: Functional Coverage and Usefulness: 7.5/15
- C1.1 Object coverage: **partial** — weighted coverage = 80.3% (30.5 / 38); no critical object absent. Every critical object is exposed [S1 `/portfolios`, `/buildings`, `/units`, `/leases`, `/contacts`, `/leases/charges`…, `/accounting/glaccounts`, `/accounting/generalledger`]. Two critical objects are only partly covered. The general ledger has lease-scoped journal entries only (`POST /leases/journalentries` requires `leaseID` [S1 `SaveLeaseJournalEntryDTO`]), and ledger reads are limited to windows under 30 days with no per-account filter [S1 `GET /accounting/generalledger`; L6]. Bank accounts can be created and updated as bank-type GL accounts, but deposits can't be read back (`POST /accounting/bankdeposits` has no GET) and there is no balance or register endpoint [S1]. Reconciliation, associations and inventory are absent. Communications can be created only on leases and prospects [S1 `/leases/{id}/conversations`, `/prospects/{id}/conversations`].
- C1.2 Core operational actions: **yes** — weighted coverage = 86.4% (38 / 44); no critical write workflow absent. Ledger posting was live-verified: `POST /leases/charges` → 201 and `PUT /leases/charges/{id}` → 200 [L10]. Contacts were live-verified: `POST /contacts` → 201 and `PATCH /contacts/{id}` → 200 [L9]. Documented writes: `POST/PUT/PATCH /leases`, `POST /leases/payments`, `/leases/refunds`, `/leases/adjustments`, `/bills` (+bulk, PATCH approval), `/bills/payment(s)`, `/accounting/ownerdraws`, `/workorders` (+tasks), `/units`, `/buildings`, `/portfolios` [S1]. The general-ledger item scores 0.5 because there are no general journal entries.
- C1.3 Delete or lifecycle actions: **no** — weighted coverage = 59.6% (15.5 / 26), and a critical lifecycle action is absent. S1 has no endpoint to reverse, void or NSF a lease payment. All 18 DELETE operations are marked "(BETA)… only available to customers who have opted in to our beta program" [U1 per-operation note]. DELETE on an existing contact and an existing charge both returned 404 [L11]. No write DTO exposes an `active` flag for archiving [S1]. There is no reconciliation resource. Lease notice, move-out and termination (status) [S1 `PATCH /leases/{id}`], deposit refunds [S1 `POST /leases/refunds`], bill approve/reject [S1 `PATCH /bills/{id}`] and applicant status [S1 `PATCH /prospects/{id}`] are available.
- C1.4 Change notification: **partial** — no webhooks or events anywhere [S1; U1]. The only mechanism is efficient incremental polling: `lastModifiedDateTimeStart/End` plus status/entity filters on every top-level list endpoint [S1, e.g. `GET /leases` parameters]. It was honored exactly in live tests [L3], and it picked up the newly created contact and charges [L9, L10]. Deleted records disappear with no signal [L12].

Score math: earned 2.0 of 4 applicable checks; unrounded fraction = 0.5000; category points = 7.5/15; verification coverage = 100% (4/4)

What this means for you: You can build real two-way automations on Propertyware: move-in paperwork into leases, post charges, record payments, sync units and tenants, and create work orders. The gaps show up when something has to be undone or reconciled. The API can't reverse an NSF payment, reconcile a bank account, read back a deposit or post a general journal entry, and deleting anything requires Propertyware's beta program. Plan on staff finishing those steps in the Propertyware screens. To keep a warehouse current, poll for recently modified records; nothing is pushed to you, and deletions won't show up.

## Category 2: API Design, Reliability, and Operability: 5.5/10
- C2.1 Modern API conventions: **yes** — a resource-oriented REST API with JSON and standard GET/POST/PUT/PATCH/DELETE [U1 § API Overview: "built upon standard REST conventions"; S1]. Live-verified [L1–L10].
- C2.2 Consistent typing: **partial** — core fields are consistently typed. In a live survey, 634 of 635 non-null field observations across 17 endpoints matched the published schema [L7]. A limited set of documented inconsistencies sits in non-core fields: `targetDeposit` is money-as-string (`"1615.0"`), deprecated 2026-05-10 in favor of numeric `targetDepositAmount` [U1 Changelog; L7]; building `multiUnit` is `"Yes"/"No"` [L7]; vendor `timeTracking` is boolean on write but `"Disabled"` on read [S1 `SaveVendorDTO`/`VendorDTO`; L7]; work order `requestedBy` is an integer on write but a string on read, `dateToEnter` is a date on write but a date-time on read, and `unitIDs` is schema `object` but a live array [S1; L7]; custom-field values are always strings [L7]. One difference touches a critical object: GL `accountType` is an integer code on write but a text label on read [S1 `SaveAccountDTO`/`AccountDTO`]. Also observed, though not a typing issue: `createdDateTime` runs 2 hours behind `lastModifiedDateTime` and the server clock, both labeled UTC [L9].
- C2.3 Structured errors: **partial** — the documented JSON error body `{userMessage, errorCode, errors[{key,message}]}` [S1 `ErrorResponse`] is returned for most 400/401/404 responses, with field-level validation errors [L4, L8]. But `errorCode` was `"1001"` for every error observed, so it can't tell errors apart. Error shapes also vary: 400 type-conversion errors and the 406 have empty bodies, unknown paths return an HTML page, and DELETE 404s have a null message. Some status codes are wrong: missing credentials return 400 where U1 § Authentication says 401, and DELETE on an existing record returns 404 [L4, L11].
- C2.4 Duplicate prevention: **no** — no idempotency key or duplicate protection is documented [S1; U1]. Sending the identical `POST /leases/charges` twice created two charges and doubled the lease balance [L10].
- C2.5 Graceful handling under load: **partial** — 429 is documented with the guidance "We recommend an exponential backoff of your requests" [U1 § Response Codes]. There is no `Retry-After` header or numeric backoff guidance, and no rate-limit headers were observed [L5]. A "Rate Limiting (FUTURE)" note sits inside a hidden HTML comment in the spec and was not credited [S1 `info.description`].
- C2.6 Pagination for large collections: **yes** — `limit`/`offset` are documented (default 100, max 500) along with the `X-Total-Count` header [U1 § Pagination], and `orderby` (including `id`) is documented on every core list [S1 "Sortable by"]. Full traversal was live-verified with no gaps or duplicates [L2]. Contradiction noted: on the final partial page, `X-Total-Count` returns that page's row count rather than the total [L2].
- C2.7 Bulk or incremental export: **partial** — incremental sync is possible on the standard list endpoints ("All top-level API resources support bulk fetches" [U1 § Bulk Request Options], with updated-since filters honored [L3]). There is no dedicated export path in the API, and some data can't be fully exported: no deleted-record signal [L12], general-ledger transactions only in windows under 30 days [L6], bank deposits not readable [S1], and child lists (lease notes, conversations, work-order tasks, lease contacts) need one call per parent record [S1]. Report publishing with "Individual/API Access" exists [U10], but its format and limits are undocumented.
- C2.8 Webhook security and delivery reliability: **N-A** — no webhooks or events are offered [S1; U1]. Their absence is scored in C1.4.
- C2.9 Concurrency and conflict control: **no** — no ETag/If-Match, version field or 409 conflict semantics is documented [S1; U1], and no ETag header was observed [L5].
- C2.10 Versioning and backward compatibility: **yes** — the version is in the path (`/v1`; requests without it return 404) [U1 § API Versioning]. The docs define backward-compatible and backwards-incompatible changes and promise "advance notice for all API releases". The changelog carries deprecation notices (`managementFeeType` 2024-04-10; `targetDeposit` 2026-05-10; old journal-entry and auto-charge URLs) [U1 § Changelog]. Caveats: no deprecation time windows are stated, and the 2024-06-09 changelog records a type change to generally available fields inside v1, which departs from the stated policy.
- C2.11 Request traceability: **no** — no request or correlation ID is documented [S1; U1] or returned [L5]. Responses carry only a CDN `server-timing` performance header. Its per-request token is undocumented and not shown to be usable with support, so it was not credited.
- C2.12 Service availability and status transparency: **yes** — a public status page lists an "Open API" component with a per-component uptime display and incident history back to 2022 [U8].

Score math: earned 6.0 of 11 applicable checks (C2.8 N-A); unrounded fraction = 0.5455; category points = 5.5/10 (5.4545); verification coverage = 100% (11/11)

What this means for you: Day-to-day reads are predictable. Records page cleanly, numbers are numbers, and "changed since" filters work, which makes it a good fit for syncing to Google Sheets or a warehouse. Writes need more care. A retried request can post a duplicate charge, two people editing the same record can overwrite each other silently, every error carries the same code (so your code has to read the message text), and there's no request ID to hand to support. Add your own duplicate checks, slow down on 429s, and log what you send.

## Category 3: Access Control and Safe Automation: 5.0/5
- C3.1 Read-only credentials: **yes** — each resource can be set to READ [S2]; "You can restrict a key to particular Propertyware entities or to read-only access (GET resources only)" [U1 § Keeping API Keys Safe].
- C3.2 Scoped credentials: **yes** — each key is scoped per resource group (14 groups) × NONE/READ/WRITE/DELETE [S2], and a 403 is documented when a key lacks permission [U1 § Response Codes].
- C3.3 Multiple keys: **yes** — five separately named keys with distinct client IDs coexist in one organization [P1]. The docs advise naming keys so you can "locate the right key" [U1 § Creating API Keys].
- C3.4 Rotation and revocation: **yes** — each key has a self-serve Delete (and Edit) action in the admin UI [P1], and requests with a deleted key return 401 [U1 § API Keys]. The docs recommend regularly recreating keys [U1 § Keeping API Keys Safe]. Rotation means creating a new key and deleting the old one; there is no in-place secret regeneration.
- C3.5 Test and production isolation: **yes** — separate sandbox/testing accounts are available on request [U9]. A key "will only work with the organization it belongs to" [U1 § How to Make a Request], and live, the key was rejected (401) under a different organization ID [L4]. The operator confirmed the sandbox is separate from production. Caveats: sandboxes are provisioned through Sales Ops, share the production hosts, and their side-effect behavior (for example, emails) is not documented.

Score math: earned 5.0 of 5 applicable checks; unrounded fraction = 1.0000; category points = 5.0/5; verification coverage = 100% (5/5)

What this means for you: This is Propertyware's strongest area. You can give an AI agent or a vendor a key that reads only leases and work orders, give each integration its own key, and kill any key yourself in Setup › API Keys. Test in a sandbox (request one from Propertyware Sales Ops) before pointing anything at live data.

## Category 4: Documentation and AI-Agent Readiness: 2.5/5
- C4.1 Complete self-serve reference: **partial** — a public, no-login reference covers authentication, every endpoint, parameters, field-level schemas and a step-by-step first request [U1]. The request/response samples are schema placeholders (`"amount": 0`, `"comments": "string"`), with no worked examples for core write flows [U1 per-operation samples; S1 has 0 operation-level examples]. Live use required reverse-engineering: contact creation has undocumented required fields (country, street, city, state, zip) [L8], and a PATCH was rejected by an unrelated default setting (`emailAlerts`) [L9]. (Behavior differences already scored elsewhere, such as status codes in C2.3 and changelog accuracy in C4.4, are not counted again here.)
- C4.2 Reliable machine-consumable integration path: **yes** — a complete OpenAPI 3.0 spec (124 paths, 177 operations, 141 schemas) can be downloaded from the public reference and matches the live docs exactly (content hash, 2026-09-11) [U1 "Download OpenAPI specification"; S1]. It has defects that need light manual correction: no security schemes (0 of 177 operations declare the three auth headers), 7 duplicate templated paths (OAS 3.0 says MUST NOT), one schema type error, a scheme-relative server URL, and no stable spec URL (download button only) [packet §4]. No official SDK or MCP server was found.
- C4.3 AI-readable documentation: **no** — no Propertyware domain has an `llms.txt` or `llms-full.txt` [U14; U16], and there is no per-endpoint Markdown, plain-text corpus or MCP documentation resource. The OpenAPI download is credited under C4.2 only.
- C4.4 Kept current: **partial** — the reference has a dated changelog (2022-09-21 → 2026-05-10) with frequent entries and deprecation notes [U1 § Changelog], but it is unreliable in places. The reference still labels `PUT /leases/refunds/{id}` and `PUT /workorders/closeworkorder/{id}` BETA/opt-in after the changelog announced beta removal (2026-04-22, 2026-05-10) [S1]. The general-ledger window now enforced (under 30 days, L6) contradicts the last recorded change (7 days, 2024-02-25). No subscription channel for API change notices was found [U1; U15].

Score math: earned 2.0 of 4 applicable checks; unrounded fraction = 0.5000; category points = 2.5/5; verification coverage = 100% (4/4)

What this means for you: An AI coding tool can get started from the OpenAPI file. Download it from the docs page and add the three `x-propertyware-*` headers yourself. Expect some trial and error on writes, because the docs don't list every required field and the examples are placeholders. Check behavior in a sandbox rather than trusting the docs or changelog alone.

## Category 5: Accessibility and Cost: 7.5/15
- C5.1 Self-serve API key: **yes** — once an account is entitled, its administrator creates keys self-serve (name, description, per-resource permissions, Generate Key) [U1 § Creating API Keys; S2]. The admin page shows five keys created by three different users, with no key-approval step [P1].
- C5.3 Not commercially gated: **no** — API access is not included in any published package: "For Enterprise/API: Add $1 per unit/per month to any package" [U3]. A paid add-on required for any API use is treated as the rubric's "API requires a premium plan" (see disagreements). Separately, sandbox accounts go through Sales Ops [U9], and write-side DELETEs require joining a beta program [U1].

Score math: earned 1.0 of 2 applicable checks; unrounded fraction = 0.5000; category points = 7.5/15; verification coverage = 100% (2/2)

What this means for you: Once API access is turned on, you can make keys yourself in minutes. Turning it on costs extra on every plan, per unit per month, and deletes and sandboxes require going through Propertyware staff.

## Total
- Raw: 27.95 / 50 (27.9545)
- Normalized before rounding: 55.91 / 100
- Published numeric score: **56 / 100**
- Letter grade: **F**
- Evidence tier: Fully verified — sandbox
- Overall verification coverage: 100% (26 of 26 applicable checks verified; no category Unable to verify; gate passed)
- Partial-result flag: no
- Unresolved evaluator disagreements: this is a single evaluator run, and the independent re-grading of the frozen packet that methodology step 12 calls for has not yet been done. These checks turn on judgment; each line gives the possible effect on the normalized score:
  - C5.3 no → partial, if a per-unit add-on available on every plan is read as partial gating rather than "requires a premium plan": +7.5 (→ 63, D)
  - C1.1 partial → yes, if the general ledger and bank accounts score 1.0 despite the missing general journal entries and deposit/balance reads: +3.75
  - C1.3 no → partial, if payment reversal is not treated as a critical lifecycle action: +3.75
  - C4.3 no → partial; C4.4 partial → yes: +1.25 each
  - C2.11 no → partial (CDN token accepted as an undocumented identifier); C2.7 or C2.2 partial → yes: +0.91 each
  - Downward risks: C4.2 yes → partial: −1.25; C2.6 or C2.10 yes → partial, or C2.2 partial → no: −0.91 each
  - If every one of these readings broke the same way, the score would range from about 52 to 76. Most single changes move it by 1–4 points; the C5.3 reading alone would lift it to 63 (D).

## Bottom line for a property manager
Propertyware's Open API is a real, broad two-way REST API. You can read and write the records a single-family property-management business runs on (properties, units, leases, tenants, tenant charges and payments, bills, owner draws and work orders), and you can keep a spreadsheet or warehouse in sync by polling for recent changes. Its biggest strength is access control: keys can be limited by resource and action, and you create and revoke them yourself. The biggest limitations are the missing undo and reconcile steps (deletes are beta-only; there's no NSF reversal, bank reconciliation or deposit read-back) and thin operability (retries can duplicate charges, errors share one code, and there are no request IDs or conflict protection). The rubric weighs the paid API add-on heavily, and together these pull the score to an F despite solid fundamentals. Propertyware is a PM-specialized system of record with trust-accounting features, not a bank: you still need your own bank accounts, and the Propertyware UI for reconciliation and corrections.
