# API Report Card — Rent Manager Web API (London Computer Systems)

**Published numeric score: 64 / 100 — Letter grade: D**
**Evidence tier: Baseline verified** (read-path battery executed live; write-path checks documentation-graded)
**Methodology: v1.1** | **Evidence packet: RM-WAPI-2026-09-07-F2 (frozen)**
**Independent runs compared: 3** (scored 66 / 64 / 60; unanimous on 20 of 27 checks; reconciled to 64)
**Instance observed:** `https://monterey.api.rentmanager.com`, server build `12.2607.9741.10976`
**Dates:** live observations 2026-09-06; login-gated reference obtained 2026-09-07

---

## Contents

1. **The report card** — Step 4 output: eligibility, context, coverage map, all 27 checks with citations, category arithmetic, totals, and the plain-language bottom line.
2. **Three-run reconciliation** — check-level comparison across the three independent runs, every disagreement and how it was resolved, the one unresolved disagreement and its score effect, plus two integrity disclosures.
3. **Appendix A — Live read-path test log** — every live observation: endpoint, date, HTTP status, response headers, response body.
4. **Appendix B — Documentation extracts** — verbatim extracts from the vendor's login-gated API reference, preserved because the credential used for this run was disabled afterward and those URLs are no longer reachable without one.

### Two disclosures the grader wishes to make on the record

**A withdrawn citation.** Run 1 originally marked C2.12 (status transparency) `yes` and cited a vendor status page with specific contents. That page was never actually retrieved; the URL surfaced in a search result and was carried into the manifest in error. Independent runs 2 and 3 caught it. The source has been withdrawn from the manifest and the check is now marked `unverified`. Details in the reconciliation.

**A packet contamination.** The evidence log handed to runs 2 and 3 ended with run 1's own score. Both graders spotted it unprompted, declared they were treating it as non-evidence, and then scored 4 and 6 points below run 1. The line has been removed. Disclosed rather than quietly fixed.

---

# Part 1 — The report card

## API Report Card: London Computer Systems — Rent Manager Web API (WAPI)

> **Reconciled across three independent runs** against frozen packet RM-WAPI-2026-09-07-F2.
> Run 1 scored 66, run 2 scored 64, run 3 scored 60; 20 of 27 checks were unanimous.
> Two run-1 marks were corrected on review (**C2.4** partial → no; **C2.12** yes → unverified,
> where run 1's original citation had not been verified). See `RECONCILIATION-three-runs.md`
> for the check-level comparison, every resolution, and the disclosed packet contamination.

### Run metadata
- Methodology version: 1.1
- Evaluating model: claude-opus-5 (the model serving this session may differ)
- Date run: 2026-09-06 / 2026-09-07 (live observations 2026-09-06 21:01–21:40 UTC; login-gated reference obtained 2026-09-07)
- Provisional evidence-packet version or ID: RM-WAPI-2026-09-06-P1
- Final evidence-packet version or ID: **RM-WAPI-2026-09-07-F2** (supersedes F1; frozen before rescoring)
- Packet reopened: F1 was frozen and scored, then **reopened under Core rule 4** when the operator obtained an authenticated session on the login-gated documentation portal. Every page added and the check it affects are recorded in the evidence-amendment log below. No check mark changed on the F1→F2 packet expansion itself; two sub-items within C1.1/C1.2/C1.3 were corrected *upward* on better evidence without moving their marks, and both previously flagged upside scenarios (C2.8, C1.4) resolved negatively.
- **Multi-run reconciliation (methodology item 12):** three independent runs were then compared at check level against this same frozen packet — 66, 64 and 60. Twenty of 27 checks were unanimous. **Two run-1 marks were corrected as a result: C2.4 partial → no, and C2.12 yes → unverified.** The published score below is the reconciled figure, not run 1's. Full comparison in `RECONCILIATION-three-runs.md`.
- Evidence-discovery mode: tool-enabled discovery + operator-supplied login-gated documentation + authenticated first-party documentation portal
- Evidence tier: **Baseline verified**
- Live-write method and safety: **none — writes documentation-graded.** Operator authorized read-path testing only and explicitly prohibited any write against live data. No POST other than the documented `/Authentication/AuthorizeUser`; no DELETE; no webhook registration. No test fixtures created, so no cleanup was required.
- Minimum live-test battery: **steps 1–5 complete.** Step 6 (create/update) not run — operator declined live-data writes. Step 7 (idempotency) not run — the API documents no idempotency mechanism, and no write was authorized. Step 8 (webhooks) not run — no write authorized, and the read-only credential lacks the *Manage Webhooks* privilege.
- Live tests performed: authenticate; read core resource and page through 249 pages; incremental `UpdateDate` filter; four deliberate error classes; rate-limit and traceability header capture; 27 object-coverage probes; 19 result-shaping parameter probes; OPTIONS verb-discovery probe.
- Live tests not possible: steps 6, 7, 8 (all write-path).
- Documentation-graded checks (baseline verified): **C1.2, C1.3, C2.4, C2.8, C2.9.**
- Independent runs compared: **3** (scores 66 / 64 / 60; reconciled 64). Unanimous on 20 of 27 checks.

### Final evidence packet manifest

**Operator-supplied (login-gated first-party, provided under Core rule 4):**
1. `Overview-12.2607.9741.11295.pdf` — Rent Manager Web API Overview
2. `QuickStart-12.2607.9741.11295.pdf` — Rent Manager API Quick Start
3. `Rent Manager API Resources index.webarchive` — `/Help/Resources`, complete index of **369 resources**
4. `Rent Manager Web API Documentation:Leases.html` — `/Help/Resource/Leases`, saved 2026-09-07
5. `Rent Manager Web API Documentation.html` — `/Help/Resource/WebhookDetails`, saved 2026-09-07
6. `Rent Manager Web API Download Resources.html` — `/Help/Download`, saved 2026-09-07
7. `Properties.pdf`, `Units.pdf`, `Tenants.pdf`, `Leases.pdf`, `ServiceManagerIssues.pdf`, `APIInformation.pdf` — collapsed-state resource pages
8. `Rent Manager support email - API access.pdf` — J. Weatherly, Customer Success Specialist III, 2026-09-02
9. `RM user setup - crane (redacted).png` — RM12 Admin ▸ Setup ▸ Users, 2026-09-06 (client addresses and trust-account identifiers masked; nothing check-relevant removed)
10. Operator screenshot of the docs-portal navigation, 2026-09-07

**Publicly discovered first-party:**
11. `https://info.rentmanager.com/hubfs/PDFs/Technical%20Documentation.pdf` — "Rent Manager 12 Web API Documentation"
12. `https://www.rentmanager.com/software-customization/` — API description
13. `https://www.rentmanager.com/pricing/` — Basic / Plus / Premium bundles, quote-gated
14. `https://www.rentmanager.com/submit-api-support-request/`
15. `https://www.rentmanager.com/release-notes-may-july-2026/` and sibling recap posts
16. ~~`https://status.lcs.com/` — LCS status page~~ — **WITHDRAWN.** This URL surfaced in a discovery search result but was never retrieved. It was carried into the F1 manifest and into the C2.12 citation in error. It is not evidence and no check rests on it. See C2.12 and `RECONCILIATION-three-runs.md`.

**Authenticated documentation portal** (added in F2, `https://monterey.api.rentmanager.com/Help`, accessed 2026-09-07 in an operator-authenticated session):
17. `/Help/Method/{Resource}/Save`, `/Delete/Collection`, `/Delete/Instance` and `/Help/Resource/{Resource}` operation inventories for **Charges, Payments, Journals, Leases, Tenants, Properties, Units, Owners, Bills, ServiceManagerIssues, Banks, GLAccounts**
18. `/Help/Method/WebhookDetails/Save` — complete webhook registration request and response model
19. `/Help/Model/TenantOrderingOptions/Tenants-Retrieve-Collection` — ordering usage notes and permitted values
20. `/Help/Model/{Lease,Property,Charge,ServiceManagerIssue,WebhookDetail}OrderingOptions/…` — each stating "This endpoint has no available Ordering Options"
21. `/Help/Model/WebhookDetailFilterFields/WebhookDetails-Retrieve-Collection` — per-field filter operator sets
22. `/Help/Model/eWebhookEventType/…` — **returns Not Found**; the webhook event catalogue has no documentation page
23. `/Help/Overview?nid=Home/Overview/…` — the live narrative overview and its complete 16-topic index

**Live observations** (`https://monterey.api.rentmanager.com`, build `12.2607.9741.10976`, read-only user `crane`, Location MBPM = 1): full log retained as `live_test_log.md`.

### Evidence-amendment log
- **C2.6 / C2.2 — amended during controlled verification.** Provisional scoring found `orderby` silently ignored. The per-resource reference obtained on 2026-09-07 revealed the actual documented parameter is `orderingOptions`. Retested live with 13 value formats; all returned HTTP 404 `KeyNotFoundException`. Finding confirmed and strengthened rather than overturned. Source added: `/Help/Resource/Leases`.
- **C2.3 — amended.** Provisional note claimed `ErrorCode` was a single constant. Retesting produced a second value (`-2146232969`, `KeyNotFoundException`). Corrected: `ErrorCode` is a .NET HRESULT keyed to exception class, not a constant, and not a documented API taxonomy.
- **C2.9 — amended.** Overview PDF names `UpdateDate` as the concurrency key; the live reference marks `ConcurrencyID` with attribute "Concurrency Key". Source added: `/Help/Resource/WebhookDetails`.
- **C4.2 — amended.** Provisional mark was `unverified: could not access`. The API Download Resources page resolved it: exactly two downloads exist. Source added: `/Help/Download`.
- **C2.8 — amended.** Provisional mark was `unverified`. The WebhookDetails model resolved it. Source added: `/Help/Resource/WebhookDetails`.

**F2 amendments (packet reopened under Core rule 4 after the operator authenticated to the documentation portal):**
- **C1.1 and C1.2 — corrected upward.** The *files* item had been scored 0.5 on the basis that no general file collection appears in the resource index. The authenticated portal shows file and attachment operations do exist as action subresources: `Properties/PropertyFiles`, `Properties/PropertyFileFolders`, `Bills/Attachments`, `Bills/UploadAttachment`, `Journals/Attachments`, `Units/Images`, `ServiceManagerIssues/UploadSignatureFile`, and `{Resource}/UploadUserDefinedValueAttachment`. Item raised to 1.0; weighted coverage 98.7% → 100%. **Mark unchanged (yes).**
- **C1.3 — corrected upward.** The *void / reverse* item had been scored 0.5 as "deletion exists but no explicit void or reversal action was evidenced". It is evidenced: `Charges/ConvertChargeToCredit`, `Payments/PaymentReversal`, `Journals/ReverseJournal`, `Journals/RemoveJournalReversal`, `Bills/Reversal`, `Tenants/CreditReversals`, `Tenants/RefundSecurityDeposit`, `Properties/RollbackLastManagementFeePosting`. Item raised to 1.0; weighted coverage 93.8% → 100%. **Mark unchanged (yes).**
- **C1.2 and C1.3 — evidence grade raised.** Both had relied partly on the Overview's general statement that POST works across collection and instance resources, confirmed on only two of 369 resources. All twelve core resources were then checked individually and every one exposes the identical five methods (`Retrieve/Collection`, `Retrieve/Instance`, `Save`, `Delete/Collection`, `Delete/Instance`). No longer inferred. **Marks unchanged (yes).**
- **C2.6 — third parameter name found and tested.** `/Help/Model/TenantOrderingOptions/…` documents a third name, `Orderings`, with a worked example. Retested live; the vendor's own example value fails. **Mark unchanged (partial).**
- **C1.4 — upside scenario resolved negatively.** `/Help/Model/eWebhookEventType/…` returns Not Found in both contexts, and the live Overview's 16-topic index contains no webhooks section. The event catalogue is undocumented, so no weighted event coverage can be computed. **Mark unchanged (partial).**
- **C2.8 — upside scenario resolved negatively.** `/Help/Method/WebhookDetails/Save` shows the complete registration request model; it carries no signing secret or signature configuration. Full-text search of the live Overview returns ABSENT for "signature", "signing", "retry" and "webhook". **Mark unchanged (no).**
- **C2.4 — confirmed.** Full-text search of the live Overview returns ABSENT for "idempot". **Mark unchanged (partial).**
- **C2.11 — confirmed.** Full-text search of the live Overview returns ABSENT for "correlation" and "request id". **Mark unchanged (no).**
- **C4.1 and C4.4 — limitations expanded, marks unchanged.** The live Overview still carries the false `ApiUri` claim and the `embed=Color` example, so those defects are current on the site rather than merely stale in a 2015 PDF; and rate limiting is absent from the live reference entirely.

### API eligibility
- Qualifying API: **yes**
- API operator: **London Computer Systems, Inc. (LCS)** — QuickStart copyright page, "Version 12.2607.9741.11295 … London Computer Systems, Inc."
- Access or credential issuer: **the customer's own Rent Manager administrator**, once LCS has sold API access. Support email 2026-09-02: "The API Access flag on the user grants them access to the API portal." Confirmed live: the operator created user `crane` unaided and it authenticated.
- Eligibility basis: A REST interface at `https://<corpid>.api.rentmanager.com` exposes 369 Rent Manager resources. Verified live against the operator's production instance — authenticated, read 745 tenants, 334 properties, 20,917 charges.

### Context
- Software category: **Accounting / PMS platform**
- What the API is for and its core objects and workflows: The Rent Manager Web API exposes the operator's own Rent Manager database over HTTPS/JSON so they can build custom applications, dashboards, and integrations. Core objects are properties, units, leases, tenants, ledger transactions (charges, payments, credits), the general ledger, and bank accounts; core workflows are reading those records, posting ledger charges and payments, and creating and updating leases. It also reaches maintenance (ServiceManagerIssues), leasing (Prospects, Applications, Screenings), owner accounting, and HOA/association management.

### Provider and property-management fit
- What this product is: Rent Manager is property management software for landlords and property managers; the Web API is its programmatic interface to the customer's own database. *(`rentmanager.com/software-customization/`; QuickStart Introduction)*
- Bank status, when relevant: **not a bank.** No first-party evidence identifies LCS as a bank or as offering banking services.
- Who provides any bank account or regulated banking service: **not evidenced.** The API exposes an `IsEpayEnabled` flag on PropertyModel and `CreditCardTransactions` / `NachaODFIBanks` resources, but no first-party material in this packet names the payment processor or any bank partner. `Banks` here means the customer's own recorded bank accounts, not accounts LCS provides.
- What the customer actually receives: a software licence to Rent Manager plus, as a separately purchased add-on, API access to their own database. No funds are held by LCS on the evidence reviewed.
- Property-management fit: **PM-specialized.** Property management is the product's entire purpose. *(369-resource index; `rentmanager.com/software-customization/`)*
- Documented PM-specific workflows: lease lifecycle including `LeaseRenew` and move-out fields; recurring-charge posting (`RecurringCharges/PostRecurringCharges`); late-fee automation; tenant ledgers and statements; owner statements and disbursements (`OwnerCheckSetups`, `ManagementFeeHistory`); maintenance dispatch (`ServiceManagerIssues`, `ServiceManagerTechTimes`); evictions (`Evictions`, `EvictionWorkflowStages`); prospects, applications and screening; utility billing; HOA violations and architectural requests; short-term rentals and online booking.
- Trust or fiduciary workflow support: **documented.** `SecurityDepositTypes`, `SecurityDepositInterest`, `Banks`, `BankReconciliations`, `Reconciliations`, `Deposits`, `AccountGroups`, `OwnerCheckSetups` appear in the reference index. Confirmed in live data: ChargeModel exposes `DepositStatus` and `IsSecurityDepositPriorToGLStartDate`; OwnerModel exposes `IsBalanceReserves` and `BalanceAccountID`. These are genuine client-fund and security-deposit constructs, not generic accounting.
- Operational role and dependencies: Rent Manager is the operator's system of record; the API is a read/write door onto it. An operator still needs their own bank, their own payment processor relationship, and their own hosting for anything they build.

### Coverage classification (fixed before inspection)

Uses the methodology's **default Accounting/PMS classification, unchanged**. No deviation, so no deviation rationale is required. The weights were fixed by the published methodology before any inspection of this API.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Properties | critical | 3 | Present, full operations |
| Units | critical | 3 | Present, full operations |
| Leases | critical | 3 | Present, full operations + `LeaseRenew` |
| Tenants | critical | 3 | Present, full operations |
| Lease ledgers / transactions | critical | 3 | Present (`Charges`, `Payments`, `Credits`, `AccountStatements`) |
| General ledger | critical | 3 | Present (`GLAccounts`, `Journals`, `GLAccountTypes`) |
| Bank accounts | critical | 3 | Present (`Banks`) — 0 records for this scoped user, not absent |
| Owners | important | 2 | Present |
| Bills | important | 2 | Present |
| Payments | important | 2 | Present |
| Applicants | important | 2 | Present (`Applications`, `Prospects`, `ProspectApplications`) |
| Work orders / tasks | important | 2 | Present (`ServiceManagerIssues`, `Tasks`) |
| Reconciliation | important | 2 | Present (`Reconciliations`, `BankReconciliations`) |
| Files | optional | 1 | Present — `PropertyFiles`, `PropertyFileFolders`, `Bills/Attachments`, `UploadAttachment`, `Images` (F2 correction) |
| Communications | optional | 1 | Present (`Emails`, `OutgoingTexts`, `HistoryNotes`) |
| Custom fields | optional | 1 | Present (`UserDefinedFields`, 261 live) |
| Associations | optional | 1 | Present (`AssociationSettings`, `Committees`, `Violations`) |
| Inventory | optional | 1 | Present (`InventoryItems`, 41 live) |
| **Workflow:** read core records | critical | 3 | Present — live verified |
| **Workflow:** post ledger charges and payments | critical | 3 | Present — documentation-graded |
| **Workflow:** create and update leases | critical | 3 | Present — documentation-graded (`Save` on Leases) |

Principal lifecycle changes assessed: move-out, lease renewal, record deletion, work-order status transition to completion, eviction stage progression, transaction void/reverse, archive/inactivate.

### Functional coverage map
- **Core objects:** all seven critical objects present with create/update/delete operations documented. All six important objects present. Four of five optional objects fully present; *files* partial.
- **Primary operational workflows:** reading core records verified live. Creating and updating records is a single `Save` operation (POST) present on every resource page examined. Charge posting is documented explicitly (`POST /Tenants/{id}/Charges?saveOptions=IgnoreHardClose`).
- **Principal lifecycle changes:** `LeaseRenew` action subresource; move-out via `MoveOutDate` / `NoticeDate` / `IsMoveOutConfirmed`; `Delete Collection` and `Delete Instance` on every resource examined; work-order closure via `IsClosed` / `CloseDate` / `StatusID`; eviction progression via `EvictionWorkflowStages`; archive via `IsActive`. No explicit void/reverse action for posted financial transactions was evidenced.

---

### Category 1: Functional Coverage and Usefulness: 13.1/15

- **C1.1 Object coverage: yes** — weighted coverage = **100%** (38 / 38). All seven critical objects present with operations. *Live: `/Properties` 334, `/Units` 445, `/Leases` 790, `/Tenants` 745, `/Charges` 20,917, `/Payments` 17,493, `/GLAccounts` 521, `/Journals` 1,995, `/Owners` 380, `/Bills` 12,992, `/ServiceManagerIssues` 5,345, `/Prospects` 1,025, `/UserDefinedFields` 261, `/InventoryItems` 41 — all HTTP 200 with `x-total-results`, 2026-09-06. `Banks` returned 204/0 and `Reconciliations` 403 under this deliberately read-only, location-scoped user; both appear in the 369-resource index and are scored present, not absent. Files raised to 1.0 in F2 on `Properties/PropertyFiles`, `Properties/PropertyFileFolders`, `Bills/Attachments`, `Bills/UploadAttachment`, `Journals/Attachments`, `Units/Images`.*
- **C1.2 Core operational actions: yes** — weighted coverage = **100%** (38 / 38). **Documentation-graded.** *Confirmed per-resource in F2: **all twelve core resources** — Charges, Payments, Journals, Leases, Tenants, Properties, Units, Owners, Bills, ServiceManagerIssues, Banks, GLAccounts — expose the identical five methods `Retrieve/Collection`, `Retrieve/Instance`, **`Save`**, `Delete/Collection`, `Delete/Instance` (`/Help/Resource/{Resource}`, 2026-09-07). `/Help/Method/WebhookDetails/Save` shows the request contract: `POST {Resource}` with an `items` list of the resource's model. Corroborated by the Overview: POST to a collection resource "Creates or Updates entities". No write was executed — operator authorized read-path only.*
- **C1.3 Delete or lifecycle actions: yes** — weighted coverage = **100%** (16 / 16). **Documentation-graded.** *`Delete/Collection` and `Delete/Instance` on all twelve core resources. Lifecycle actions as named subresources: `Leases/LeaseRenew`; `ServiceManagerIssues/Advance` and `/Status`; `Tenants/TransferTenant`, `/Evictions`, `/RefundSecurityDeposit`. Void and reversal — raised to 1.0 in F2 — are explicit: `Charges/ConvertChargeToCredit`, `Payments/PaymentReversal`, `Journals/ReverseJournal`, `Journals/RemoveJournalReversal`, `Bills/Reversal`, `Tenants/CreditReversals`, `Properties/RollbackLastManagementFeePosting`. Move-out via LeaseModel `MoveOutDate`/`NoticeDate`/`IsMoveOutConfirmed`; archive via `IsActive` (live).*
- **C1.4 Change notification: partial** — Webhooks exist but their event coverage cannot be established, so credit rests on the polling limb of the rubric. *`WebhookDetails` is a real resource with `WebhookEventType` and `URL` fields, and `/Help/Method/WebhookDetails/Save` documents registration. But **`/Help/Model/eWebhookEventType/…` returns Not Found** in both the Retrieve-Collection and Save contexts, and the live Overview's complete 16-topic index contains no webhooks section — the event catalogue is undocumented, so no weighted event coverage can be computed. Efficient incremental polling is verified live: `GET /Tenants?filters=UpdateDate,gt,2026-01-01` returned `x-total-results: 214` against an unfiltered 745 — the filter is honoured. Combined with `pagesize=5000` (observed) this detects critical state changes reliably.*

**Score math:** earned 3.5 of 4 applicable checks; unrounded fraction = 0.875; category points = 0.875 × 15 = **13.125 → 13.1/15**; verification coverage = 4/4 = **100%**.

**What this means for you:** This is the strongest part of the API by a wide margin, and it is genuinely strong. Everything your business runs on is reachable — properties, units, leases, tenants, the ledger, the general ledger, owners, work orders, prospects, even HOA violations and utility billing. It is not a read-only window either: the documentation is consistent that you can create and update records and drive real workflows like lease renewals. The one gap is knowing *when* something changed. Webhooks exist, but nothing in the available documentation tells you which events they cover, so in practice you would poll — asking "what changed since yesterday?" — which works well here because date filters are honoured and you can pull 5,000 records per call.

### Category 2: API Design, Reliability, and Operability: 5.0/10

- **C2.1 Modern API conventions: yes** — Resource-oriented REST over HTTPS/JSON, standard collection and instance URLs, conventional status codes. *Overview PDF, "Resources" and "HTTP Response Codes"; verified live across 27 resources.* Only GET, POST and DELETE are used — POST serves both create and update — which is a common and interoperable modern pattern rather than a defect.
- **C2.2 Consistent typing: partial** — **Limitation:** primary-key identifiers are numeric on core resources but strings on others. *Live 2026-09-06: `/Properties` returned `"PropertyID":854`, `/Tenants` `"TenantID":920` (numbers), while `/Reports` returned `"ReportID":"1"` and `/SystemPreferences` `"PreferenceID":"1"` (strings). Booleans and numbers are otherwise consistent across all core resources and live reads matched the published models. The inconsistency is confined to non-core resources, hence partial rather than no. Separately, the published schema declares `UnitID` as `Int32` while every other integer is `Integer` — cosmetic, same underlying type.*
- **C2.3 Structured errors: partial** — **Limitation:** four distinct error shapes, no stable API-specific machine code, and incorrect status semantics in several places. *Live: (1) ErrorModel `{DeveloperMessage, UserMessage, ErrorCode, Exception, MoreInfoUri}` on 401/403/500; (2) bare `{"Message":"No HTTP resource was found…"}` on an unknown route; (3) `{Message, ModelState}` on a bad filter; (4) **empty body** on `GET /Properties/99999999`, contradicting the Overview's "All 400 codes should return an ErrorModel object". `ErrorCode` is a .NET HRESULT keyed to exception class (`-2146233088` System.Exception, `-2146232969` KeyNotFoundException), undocumented anywhere in the packet. Status semantics: a forced password reset returned **500**; insufficient privileges returned **403** on `/Reconciliations` but **500** on `/WebhookDetails`; an invalid `orderingOptions` value returned **404**.* The ErrorModel's `DeveloperMessage` is genuinely actionable, which is what keeps this at partial.
- **C2.4 Duplicate prevention: no** — **Documentation-graded. Reconciled from `partial` after runs 2 and 3 independently marked `no`.** *The Overview's 409 clause ("For Create requests this indicates that a record with the same parameters already exists and duplicates are not allowed") describes a database uniqueness constraint, not an idempotency mechanism: it offers nothing for the writes that matter operationally, since posting the same charge or payment twice is legitimate and no uniqueness constraint guards it. A full-text search of the live Overview across all 16 topics returns **ABSENT** for "idempot". No idempotency key, request identifier, or equivalent exists anywhere in the first-party materials, so a consequential write retried after a network timeout can duplicate.*
- **C2.5 Graceful handling under load: yes** — 429 is documented and every response carries machine-readable numeric backoff data. *Overview PDF, "429 – Too Many Requests"; live: every response carried `x-ratelimit-limit: 500`, `x-ratelimit-remaining`, `x-ratelimit-reset` (Unix timestamp) and `x-ratelimit-resettime` (HTTP date, consistently exactly 60 s after the request). No 429 was induced — the limit is shared per company with the operator's live integrations.* The published limit values are wrong (see C4.4); the mechanism itself is sound.
- **C2.6 Pagination for large collections: partial** — **Limitation:** no stable ordering guarantee, and **none of the three documented sort parameters works.** *Strengths, verified live: `Link` header carrying `first`/`previous`/`next`/`last`, plus `x-total-results` and `x-results`; traversed `/Tenants` at 249 pages and `/Charges` at 20,917 records; `pagesize=5000` returned 5,000 rows. Failures, all tested live: (1) **`orderby`** (Overview) — accepted and silently ignored; six spellings including `orderby=NotAField` all returned HTTP 200 with identical default order, on both `/Tenants` and `/Properties`. (2) **`orderingOptions`** (the per-resource URL template) — HTTP 404 `KeyNotFoundException` for all 13 value formats tested, including valid field names. (3) **`Orderings`** (documented in `/Help/Model/TenantOrderingOptions/…` with the worked example `?Orderings=TenantName` and permitted values `LastFirst` and `TenantName`) — **the vendor's own example value returned HTTP 200 with the identical default order.** Most resources define no ordering at all: `/Help/Model/{Lease,Property,Charge,ServiceManagerIssue,WebhookDetail}OrderingOptions/…` each state "This endpoint has no available Ordering Options." No default ordering guarantee is documented anywhere.*
- **C2.7 Bulk or incremental export: partial** — **Limitation:** no dedicated bulk or async export path; extraction runs through standard list endpoints. *Incremental sync verified live (`filters=UpdateDate,gt,…` honoured, 214 of 745). `pagesize=5000` returned 5,000 rows despite the Overview's stated 1,000 cap. A `Reports` resource with 319 reports exists and the QuickStart references report generation and download, but no export-job endpoint was evidenced in the packet.*
- **C2.8 Webhook security and delivery reliability: no** — *`/Help/Method/WebhookDetails/Save` (2026-09-07) documents the complete registration contract — `POST WebhookDetails` with an `items` list of `WebhookDetailModel` — and the model contains exactly: `WebhookDetailID`, `WebhookEventType`, `URL`, `PartnerProductID`, `CreateDate`, `CreateUserID`, `UpdateDate`, `UpdateUserID`, `ConcurrencyID`, `CreateUser`, `UpdateUser`, `MetaTag`. There is **no signing-secret field, no HMAC key, and no signature configuration of any kind** in either the request or the response model, so a consumer cannot verify that a delivered payload genuinely originated from Rent Manager. On retries and replay: a full-text search of the live Overview across all 16 topics returns **ABSENT** for "signature", "signing", "retry" and "webhook" alike; webhooks are likewise unmentioned in the QuickStart and the public Technical Documentation. Neither limb of the check is satisfied.* Not double-counted with C1.4, which scores detection of change; this scores the security and reliability of the push mechanism.
- **C2.9 Concurrency and conflict control: yes** — **Documentation-graded.** *Overview PDF, "Concurrency": enabled by default and "**Concurrency cannot currently be disabled**"; updates must carry the concurrency key. "409 – Conflict": "for Update requests this indicates that a record was found but the concurrency information has changed … the client should request the latest version of the data, and attempt their update again." Version field confirmed in the live reference: `ConcurrencyID` carries the attribute "Concurrency Key" on WebhookDetailModel, and `ConcurrencyID` was observed live on `/Properties` and `/Journals`.* Noted but not penalised here: the Overview names `UpdateDate` as the key while the reference names `ConcurrencyID`, and LeaseModel exposes neither attribute — that documentation conflict is scored in C4.1.
- **C2.10 Versioning and backward compatibility: partial** — **Limitation:** the deprecation policy is informal and there is no client-selectable version. *Overview PDF, "Backwards Compatibility", explicitly defines non-breaking changes (new resource, new data model, added field) versus breaking ones (renaming a resource, removing or renaming a field) — a real policy. "Versioning": a deprecated resource "will respond with a custom header for a period of time before it is removed", then 410 Gone. The header is never named and the period never specified. `x-api-version` is returned on every response (`12.2607.9741.10976`) but is informational only — a client cannot request a version.*
- **C2.11 Request traceability: no** — *No request or correlation identifier appears on any response. The complete authenticated header set observed live is: `cache-control`, `content-length`, `content-type`, `date`, `expires`, `pragma`, `x-api-version`, `x-api-user`, and the five `x-ratelimit-*` headers. No `x-request-id`, `x-correlation-id`, or `traceparent`. `x-api-user` echoes the username, not a per-request identifier. Confirmed in F2: a full-text search of the live Overview returns **ABSENT** for both "correlation" and "request id" — no alternative trace mechanism is documented.*
- **C2.12 Service availability and status transparency: unverified — could not access** — **Corrected from `yes`. Run 1's original citation was not verified.** *The F1 report cited `https://status.lcs.com/` and described its contents specifically (component-level status, incident history to 2026-08-23, 90-day uptime 100.0%). That page was never actually retrieved — the URL surfaced in a discovery search result and was carried into the manifest and the citation without being fetched. The described details were not observed. No status-page, uptime, incident-history or SLA evidence exists anywhere in packet F2 in either direction. Per Core rule 4, `no` requires that relevant first-party materials were accessible and checked; they were not. Marked `unverified`, excluded from the category score and retained in the coverage denominator.*

**Score math:** earned 5.5 of **11 scored** checks (yes: C2.1, C2.5, C2.9 = 3.0; partial: C2.2, C2.3, C2.6, C2.7, C2.10 = 2.5; no: C2.4, C2.8, C2.11 = 0; C2.12 unverified and excluded); unrounded fraction = 0.5000; category points = 0.5000 × 10 = **5.000 → 5.0/10**; verification coverage = 11/12 = **91.7%** (unverified counts in the coverage denominator).

**What this means for you:** The plumbing is decent but leaky in ways that cost developer time. Pagination and rate limiting are handled well — you can pull your whole database efficiently and the server tells you exactly how much budget you have left. But you cannot sort results at all: one sort parameter is silently ignored, the other throws an error for every value I tried. Errors come back in four different formats with no stable error code, and no response carries a request ID, so if you call support about a failed call there is no reference number to give them. The webhook mechanism has no way to sign payloads, which means anything receiving them cannot verify the message genuinely came from Rent Manager.

### Category 3: Access Control and Safe Automation: 4.5/5

- **C3.1 Read-only credentials: yes** — *RM12 Admin ▸ Setup ▸ Users, 2026-09-06: user `crane` has **Read-Only** and **API Access** both checked, Administrator unchecked. Verified live — the credential authenticated and performed reads throughout this run.*
- **C3.2 Scoped credentials: yes** — Fine-grained resource **and** action scoping. *The user record carries per-Property and per-Property-Group selection, per-Location selection (`crane` is restricted to MBPM; CCPM and MBVR unchecked), a Banks/Credit Cards selection list, a Roles list, and a dedicated Privileges tab. Scoping confirmed live by observed enforcement: `/Reconciliations` → 403 "Insufficient privileges to access some or any banks"; `/WebhookDetails` → "Required privilege: Manage Webhooks"; `/Banks` → 0 records.*
- **C3.3 Multiple keys: yes** — *36 users listed in the RM12 user manager, any of which can carry the API Access flag. Support email 2026-09-02 confirms additional dedicated integration users are the intended pattern and that "Logging into the API does NOT take up a session." The operator already runs multiple integrations against this instance.*
- **C3.4 Rotation and revocation: yes** — Fully self-serve for a Rent Manager administrator. *The same user screen exposes the password field, an Active checkbox, the API Access checkbox, and an Unlock User button. Overview PDF, "Authentication Process": "A token is always invalidated if the pertinent information about the user changes, such as permissions or password" — so a password change revokes live tokens immediately. Demonstrated in this run: a forced password reset invalidated the original credential until reset.*
- **C3.5 Test and production isolation: partial** — **Limitation:** a separate environment exists only as a paid additional production location, and no test/live credential distinction is a documented product feature. *Support email 2026-09-02: "You are always able to create a new database location for testing purposes … you would simply need to ensure that the user with API Access has access to that sandbox location. However, just be aware that there are monthly costs involved with adding a new location." Location-level isolation demonstrably works — `crane` is confined to MBPM and `LocationID` is a required authentication parameter — but this is the production authentication system partitioned by location, not an isolated sandbox.*

**Score math:** earned 4.5 of 5 applicable checks; unrounded fraction = 0.9; category points = 0.9 × 5 = **4.5/5**; verification coverage = 5/5 = **100%**.

**What this means for you:** This is the API's best category and it is a real strength for anyone nervous about handing access to an outside developer or an AI agent. You can create a dedicated user, tick Read-Only, restrict it to specific properties, property groups, locations and bank accounts, and hand that over knowing it cannot write anything. You saw this work in this very session — the read-only user was refused on reconciliations and webhooks, exactly as intended. You can revoke it yourself in seconds by changing the password or unticking Active, with no call to Rent Manager. The only real gap is that a proper test environment costs money every month, so most operators end up developing against live data.

### Category 4: Documentation and AI-Agent Readiness: 1.9/5

- **C4.1 Complete self-serve reference: partial** — **Limitation:** the reference is not publicly accessible; its own narrative layer is wrong about core parameters; and rate limiting is undocumented in it entirely. *The reference sits behind a customer login at `<corpid>.api.rentmanager.com/Help` (verified: an API token does not open it — `GET /Help/Resource/Tenants` with a valid `X-RM12Api-ApiToken` redirects to `/Help/Login`). Behind that login the per-resource pages are genuinely good, and better than F1 could establish: URL templates, typed parameter tables, complete model property tables with attributes, per-operation `Save`/`Delete` pages, and `FilterFields` pages documenting the exact operator set available per field (`lt`, `le`, `gt`, `ge`, `ne`, `eq`, `in`, `ni`, `bt`, `ct`, `hv`, `ltn`, `len`, `gtn`, `gen`) with plain-language descriptions. Against that: the **live** Overview — not merely the 2015 PDF — still states "All Data Models include the 'APIURI' field" and gives the `?embed=Color` example, both false against the running build (`GET /Properties/854` returned 32 fields, none of them `ApiUri`; the singular `embed` returns an empty array). The live Overview documents `orderby` while the per-resource reference documents `orderingOptions` and `Orderings` — three mutually inconsistent names for one feature, none functional. **Rate limiting is absent from the live reference altogether** ("rate limit" and "X-RateLimit" both return ABSENT across all 16 Overview topics) even though the server enforces a 500-per-minute budget and returns five headers describing it. Sample response bodies are stubs (`[{"LeaseID":1,"TenantID":2}]`).*
- **C4.2 Reliable machine-consumable integration path: partial** — **Limitation:** the only first-party artefact is a sample application covering a limited subset. *The vendor's own API Download Resources page (`/Help/Download`, 2026-09-07) lists exactly two items: "Quick Start Download" and "Overview Download" — both PDFs. No OpenAPI or Swagger specification (the portal is ASP.NET Web API HelpPage, which emits none; `/swagger` and `/openapi.json` are not served). No official SDK, no Postman collection, no MCP server in any packet source. The QuickStart references a C# sample console application at `/content/quickstartapp/LCS.UI.API.QuickStart.Examples.zip`, described as giving "a head start" — a sample, not a maintained SDK. Third-party GitHub clients exist but are not first-party and are not credited.*
- **C4.3 AI-readable documentation: no** — *No `llms.txt`, `llms-full.txt`, per-endpoint Markdown, or downloadable text/Markdown corpus is offered. The vendor's own downloads inventory enumerates two PDFs and nothing else. The reference itself is login-gated HTML whose content is hidden behind client-side collapse toggles, so it is unreachable to any retrieval tool that is not authenticated as a customer — the printed resource pages in this packet captured only collapsed shells, which is precisely that failure mode.*
- **C4.4 Kept current: partial** — **Limitation:** currency signals exist but demonstrably do not cover the API. *LCS publishes recurring release-note recaps (`rentmanager.com/release-notes-may-july-2026/` and siblings back through 2024) — but the May–July 2026 edition contains no mention of the Web API, endpoints, or resources. The Overview PDF carries a 2015 copyright. Direct evidence of drift: the supplied documentation is build `12.2607.9741.11295` while the server reports `12.2607.9741.10976`, and the guides assert behaviours the running build contradicts (`ApiUri`, `embed`, `orderby`, 206 on pagination, a 1,000-row `pagesize` cap that was not enforced at 5,000). F2 established this is worse than stale downloads: **the same errors are live on the documentation site today**, so the narrative layer is not maintained against the code at all. Offsetting this, the per-resource reference is evidently generated from the running code — it correctly documents `embeds`, `ConcurrencyID`, and per-field filter operators — and deprecated filters carry deprecation dates.* Graded on currency of change communication only; the versioning contract is scored in C2.10.

**Score math:** earned 1.5 of 4 applicable checks; unrounded fraction = 0.375; category points = 0.375 × 5 = **1.875 → 1.9/5**; verification coverage = 4/4 = **100%**.

**What this means for you:** This is where Rent Manager scores worst, and it has a direct cash cost to you. The good reference material is locked behind a customer login, so a developer you hire cannot read the documentation until you have given them a login — and AI coding tools cannot read it at all, which matters a great deal if you plan to build with Claude or similar. Worse, the two guides you *can* download are wrong about things that will silently break working code. Following the published example for pulling a tenant's addresses returns an empty list rather than an error, which looks exactly like "this tenant has no address." I found that by testing, not by reading. Budget for a developer discovering these by trial and error.

### Category 5: Accessibility and Cost: 7.5/15

- **C5.1 Self-serve API key: yes** — *Once an account is entitled, credential creation is entirely self-serve: a Rent Manager administrator ticks API Access on a user in Admin ▸ Setup ▸ Users. Support email 2026-05-26: "You just need to make sure you have 'API' access on your user. Go to Admin – Setup – Users … check the API Access box." No approval step, ticket, or key-request process. Demonstrated in this run — the operator created and enabled user `crane` unaided, and it authenticated live.*
- **C5.3 Not commercially gated: no** — *QuickStart, "Requirements": "**You must purchase access to the RM API – contact your Sales Representative for pricing.**" API access is a separately purchased add-on, not an included capability, and it requires a sales conversation. The pricing page (`rentmanager.com/pricing/`) shows Basic, Plus and Premium bundles with no published figures and quote-gated access throughout. No first-party source states a price or indicates any tier includes API access. This is commercial gating, not identity or regulatory verification.*

**Score math:** earned 1.0 of 2 applicable checks; unrounded fraction = 0.5; category points = 0.5 × 15 = **7.5/15**; verification coverage = 2/2 = **100%**.

**What this means for you:** Two very different answers. Once you are paying for API access, getting a credential is genuinely easy and entirely in your hands — no ticket, no waiting, no Rent Manager involvement, which is better than many competitors. But getting to that point means buying the API as an add-on at a price you can only learn by calling a salesperson. For a hundred-property operator deciding whether to build automation, that unpriced gate is a real barrier, and it is why this category — worth 15 points, the same as functional coverage — costs the overall score so heavily.

---

### Total
- **Raw: 32.00 / 50**
- **Normalized before rounding: 64.00 / 100**
- **Published numeric score: 64 / 100**
- **Letter grade: D**
- Evidence tier: **Baseline verified**
- Overall verification coverage: **96.3%** — 26 of 27 applicable checks verified (C2.12 unverified); lowest category coverage 91.7%, above the 0.70 floor; no category Unable to verify; gate satisfied (overall ≥ 80%)
- Partial-result flag: **yes.** Five checks (C1.2, C1.3, C2.4, C2.8, C2.9) were graded from first-party documentation rather than observed writes, because the operator authorized read-path testing only. One check (**C2.12**) is unverified: no status-page, uptime or SLA evidence exists in the packet in either direction, and run 1's original citation for it was withdrawn as unverified. Resolving C2.12 by actually retrieving the LCS status page moves the score to **66** (if it carries incident history and uptime), **63** (if no such page exists), or leaves it between — all grade D. Executing battery steps 6–8 on operator-provisioned fixtures under the controlled live-data protocol would move the five documentation-graded checks onto observed behaviour and lift the tier to Fully verified.
- Unresolved evaluator disagreements: **one, reported rather than averaged.** **C2.3 (structured errors)** — two of three independent runs marked `partial`; the third marked `no`, reasoning that the check's partial limb requires correct HTTP status codes (contradicted by 500 on a forced password reset, 403 versus 500 for identical privilege failures, and 404 for a bad parameter value) and that three separate HTTP 200 responses silently discard failed instructions. Resolved to `partial` because the ErrorModel carries a discriminating `Exception` string and an actionable `DeveloperMessage` on genuine error paths, and because the partial limb names "error shapes that vary across endpoints" almost verbatim. **Reversal gives 63 / 100, still grade D.** Five further checks split 2–1 (C2.1, C2.7, C2.9, C4.2 toward the majority; C2.12 resolved to the middle position) and are documented with their resolutions in `RECONCILIATION-three-runs.md`.
- Grade robustness: the three runs spanned **60–66** and every contested variant lands between **63 and 66**. **All are grade D.** The letter grade is the robust finding; the specific integer is not.

### Bottom line for a property manager

Rent Manager's API reaches essentially everything your business runs on — all 334 properties, 445 units, 790 leases and 20,917 charges in your database came back cleanly in this test — and it lets you write as well as read, so real automation is genuinely buildable on it. Its standout strength is safety: you can create a read-only user locked to specific properties, locations and bank accounts, hand it to a developer or an AI agent, and switch it off yourself in seconds, which is exactly what happened in this evaluation.

The score is dragged down by two things that have nothing to do with what the API can do. First, the documentation: the good reference is behind a customer login where no AI coding tool can reach it, and the two guides you can actually download are wrong about details that break working code silently rather than loudly — the published example for fetching a tenant's addresses returns an empty list rather than an error. Second, cost: API access is a separately purchased add-on at a price only a salesperson will tell you, and that single fact costs 7.5 of the 15 points in the accessibility category. Add the smaller operational gaps — sorting does not work through either documented parameter, there is no request ID to quote to support, and webhooks cannot be cryptographically verified — and a solid, capable API lands at 66.

Practically: if you are already paying for API access, build on it, plan to poll for changes rather than rely on webhooks, and budget developer hours for discovering documentation errors by testing. If you are not yet paying for it, the number to weigh against the quote is not this score but what the automation would save you. And note what this API is not — Rent Manager is not a bank and holds none of your funds. It does document real trust and security-deposit constructs, which is more than most software in this category, but you still need your own bank, your own payment processor, and your own hosting for anything you build. This grades the API's buildability, not Rent Manager as a product.


---

# Part 2 — Three-run reconciliation

## Rent Manager Web API — three-run reconciliation

**Packet:** RM-WAPI-2026-09-07-F2 (frozen)
**Methodology:** v1.1, item 12 — *"compare two or three independent runs using the same
final frozen packet. Compare check-level marks, not only totals. Resolve disagreements
against the final evidence before calculating the published score."*

| Run | Conditions | Result |
|---|---|---|
| **Run 1** | Live battery steps 1–5 executed against the production instance; discovery permitted | 66 / 100, D |
| **Run 2** | Frozen packet only, no discovery, no live access | 64 / 100, D |
| **Run 3** | Frozen packet only, no discovery, no live access | 60 / 100, D− |
| **Reconciled** | Disagreements resolved against the evidence | **64 / 100, D** |

---

### Integrity disclosure — a packet contamination, self-reported

**Runs 2 and 3 were each handed a packet whose live-test log ended with run 1's own
scoring conclusion** ("Published score unchanged: 66/100, grade D"). That line should
never have been in an evidence file. Both graders independently spotted it, flagged it
unprompted, stated they were treating it as non-evidence, and re-derived every mark and
all arithmetic from the underlying observations. Run 3 then landed six points *below*
run 1 and run 2 four points below, which is behavioural evidence that neither anchored
to it.

The line has since been removed from the evidence log. It is disclosed here rather than
quietly fixed, because a reader assessing the independence of these runs is entitled to
know it happened. Anyone re-running the packet now gets a clean copy.

---

### Check-level comparison

20 of 27 checks were unanimous across all three runs. Seven differed.

| Check | Run 1 | Run 2 | Run 3 | Reconciled | Note |
|---|---|---|---|---|---|
| C1.1 Object coverage | yes | yes | yes | **yes** | unanimous |
| C1.2 Core operational actions | yes | yes | yes | **yes** | unanimous |
| C1.3 Delete / lifecycle | yes | yes | yes | **yes** | unanimous |
| C1.4 Change notification | partial | partial | partial | **partial** | unanimous |
| C2.1 Modern conventions | yes | yes | *partial* | **yes** | 2–1 |
| C2.2 Consistent typing | partial | partial | partial | **partial** | unanimous |
| C2.3 Structured errors | partial | partial | *no* | **partial** | 2–1, closest call on the card |
| **C2.4 Duplicate prevention** | *partial* | **no** | **no** | **no** | **run 1 corrected** |
| C2.5 Graceful under load | yes | yes | yes | **yes** | unanimous |
| C2.6 Pagination | partial | partial | partial | **partial** | unanimous |
| C2.7 Bulk / incremental export | partial | partial | *yes* | **partial** | 2–1 |
| C2.8 Webhook security | no | no | no | **no** | unanimous |
| C2.9 Concurrency control | yes | yes | *partial* | **yes** | 2–1 |
| C2.10 Versioning | partial | partial | partial | **partial** | unanimous |
| C2.11 Request traceability | no | no | no | **no** | unanimous |
| **C2.12 Status transparency** | *yes* | **unverified** | *no* | **unverified** | **run 1 corrected — see below** |
| C3.1 Read-only credentials | yes | yes | yes | **yes** | unanimous |
| C3.2 Scoped credentials | yes | yes | yes | **yes** | unanimous |
| C3.3 Multiple keys | yes | yes | yes | **yes** | unanimous |
| C3.4 Rotation / revocation | yes | yes | yes | **yes** | unanimous |
| C3.5 Test / prod isolation | partial | partial | partial | **partial** | unanimous |
| C4.1 Self-serve reference | partial | partial | partial | **partial** | unanimous |
| C4.2 Machine-consumable path | partial | partial | *no* | **partial** | 2–1 |
| C4.3 AI-readable docs | no | no | no | **no** | unanimous |
| C4.4 Kept current | partial | partial | partial | **partial** | unanimous |
| C5.1 Self-serve API key | yes | yes | yes | **yes** | unanimous |
| C5.3 Not commercially gated | no | no | no | **no** | unanimous |

---

### Resolutions

#### Two marks where run 1 was wrong and has been corrected

**C2.12 Service availability and status transparency — run 1 said `yes`; reconciled to `unverified`.**

This is the serious one. Run 1's report card cited `https://status.lcs.com/` and described
its contents in specifics — "All Systems Operational", component-level status including
Rent Manager Online, incident history back to 2026-08-23, 90-day uptime at 100.0%.
**Run 1 never actually retrieved that page.** The URL surfaced in a search result during
discovery and was carried into the manifest and the citation without being fetched. The
described details were not verified.

Run 2 marked it `unverified` because nothing in the packet evidences a status page in
either direction. Run 3 marked it `no`, reasoning that `unverified` removes the check from
the scoring denominator and so rewards an absence. Run 3's concern is legitimate, but
Core rule 4 is explicit that `no` requires that "the relevant first-party materials were
accessible and the capability was not evidenced" — and no one checked. Asserting absence
would repeat run 1's error in the opposite direction.

Resolved to **`unverified`**. It is excluded from Category 2's score but counts in its
coverage denominator, which is exactly the rubric's anti-gaming design. Category 2
coverage is 11/12 = 91.7%, above the 0.70 floor; overall coverage 26/27 = 96.3%, above
the 0.80 gate. The score remains publishable.

*To resolve this check properly, someone with discovery access should retrieve the LCS
status page and record what it shows. If it carries incident history and uptime figures
it becomes `yes` (+0.83 raw, giving 66); if it exists without them, `partial`; if no such
page exists, `no` (−0.42 raw from the unverified baseline, giving 63). All three outcomes
remain grade D.*

**C2.4 Duplicate prevention — run 1 said `partial`; runs 2 and 3 both said `no`; reconciled to `no`.**

Run 1 credited partial on the Overview's 409 clause: *"For Create requests this indicates
that a record with the same parameters already exists and duplicates are not allowed."*
Both other graders read that as a database uniqueness constraint rather than an
idempotency mechanism, and they are right. It offers nothing for the writes that actually
matter to a property manager — posting a charge or a payment twice is legitimate, so no
uniqueness constraint protects it. A full-text search of the live reference returns
**ABSENT** for "idempot". Retrying a consequential write after a network timeout has no
documented protection whatsoever, which is the `no` limb exactly.

#### Five 2–1 splits resolved against the rubric text

- **C2.3 Structured errors → `partial`.** Run 3 argued `no`, and the argument is strong:
  the check's partial limb requires *correct HTTP status codes*, and this API returns 500
  for a forced password reset, 403 on one resource but 500 on another for identical
  privilege failures, and 404 for a bad parameter value. It also hides three failures
  behind HTTP 200. Held at `partial` because the ErrorModel carries a discriminating
  `Exception` string and genuinely actionable `DeveloperMessage` on real error paths, and
  the partial limb names this case almost verbatim — "error shapes that vary across
  endpoints". **This is the least settled mark on the card.**
- **C2.1 Modern conventions → `yes`.** Run 3 noted no PUT/PATCH, POST overloaded for
  create and update, RPC-style action resources, and no OPTIONS. Real, but POST-for-update
  plus action endpoints is a mainstream modern REST pattern (Stripe among others).
- **C2.7 Bulk export → `partial`.** Run 3 correctly noted the `yes` limb explicitly names
  "documented incremental sync via updated-since plus pagination". Held at partial because
  the partial limb describes this API almost word for word — sync works on standard list
  endpoints, with no dedicated bulk or export path.
- **C2.9 Concurrency → `yes`.** Run 3 downgraded because two first-party sources name
  different concurrency keys and `ConcurrencyID` is missing from LeaseModel. Held at `yes`
  because both required limbs (version field, documented 409 semantics) are present; the
  contradiction is a documentation defect and is scored in C4.1, not counted twice here.
- **C4.2 Machine-consumable path → `partial`.** Run 3 held that a sample console app is
  not an SDK and marked `no`. Held at partial because the check's partial limb covers "the
  only mechanism is incomplete, covers a limited subset", which the first-party C# sample
  is.

---

### Reconciled arithmetic

| Category | Marks | Earned / scored | Fraction | Points | Coverage |
|---|---|---|---|---|---|
| 1 Functional Coverage | 3 yes, 1 partial | 3.5 / 4 | 0.8750 | **13.1** / 15 | 4/4 = 100% |
| 2 Design, Reliability, Operability | 3 yes, 5 partial, 3 no, 1 unverified | 5.5 / 11 | 0.5000 | **5.0** / 10 | 11/12 = 91.7% |
| 3 Access Control | 4 yes, 1 partial | 4.5 / 5 | 0.9000 | **4.5** / 5 | 5/5 = 100% |
| 4 Documentation and AI-Readiness | 2 partial, 1 no, 1 partial | 1.5 / 4 | 0.3750 | **1.9** / 5 | 4/4 = 100% |
| 5 Accessibility and Cost | 1 yes, 1 no | 1.0 / 2 | 0.5000 | **7.5** / 15 | 2/2 = 100% |

- **Raw total: 32.00 / 50** (from unrounded category values)
- **Normalized: 64.00 / 100**
- **Published numeric score: 64 / 100**
- **Letter grade: D**
- **Evidence tier: Baseline verified** — battery steps 1–5 complete; step 6 not run
  (operator authorized read-path only); step 7 **N-A** (the API documents no idempotency);
  step 8 not run (no write authorization, and the read-only credential lacked the
  *Manage Webhooks* privilege).
- **Documentation-graded checks:** C1.2, C1.3, C2.4, C2.8, C2.9.
- **Gate:** no category Unable to verify (minimum coverage 91.7%); overall coverage
  26/27 = 96.3% ≥ 0.80; tier is publishable. **Number may be published.**

### Unresolved disagreement, reported rather than averaged

**C2.3** remains genuinely contested — one of three graders marked it `no` on reasoning
the other two acknowledged as sound. Reversing it gives **63 / 100**, still grade **D**.

**Every run, and every unresolved variant, lands on D.** Runs spanned 60–66 and the
reconciled figure is 64; no combination of the contested calls reaches C− (70) or falls
to F (below 60). The letter grade is the robust finding here; the specific integer is not.

### What a fourth run should fix first

1. Retrieve the LCS status page and settle **C2.12** with an actual observation.
2. Execute battery steps 6–8 on operator-provisioned test fixtures under the methodology's
   controlled live-data protocol, which would move five documentation-graded checks
   (C1.2, C1.3, C2.4, C2.8, C2.9) onto observed behaviour and lift the tier to Fully verified.
3. Retrieve the C# QuickStart sample application itself, so **C4.2** rests on the artefact
   rather than on the guide's description of it.


---

# Appendix A — Live read-path test log

## Rent Manager WAPI — live read-path test log
Instance: https://monterey.api.rentmanager.com/ (Location MBPM = LocationID 1)
Credential: dedicated read-only RM user `crane` (Read-Only + API Access flags)
Server build reported on every response: `x-api-version: 12.2607.9741.10976`
(Note: supplied documentation is build 12.2607.9741.11295 — docs NEWER than server.)
Date of observations: 2026-09-06, ~21:01–21:40 UTC
Method: same-origin `fetch()` from https://monterey.api.rentmanager.com in Claude's
built-in browser pane on the operator's machine (container egress to rentmanager.com
is blocked by policy). All calls GET except the single documented auth POST.

### Step 1 — Authenticate
- POST /Authentication/AuthorizeUser {Username, Password, LocationID:1}
- FIRST ATTEMPT (original password) -> **HTTP 500**, body:
  {"DeveloperMessage":"A password reset is required. Please login to Rent Manager Express
   or Rent Manager 12 to reset it.","ErrorCode":-2146233088,
   "Exception":"AuthenticationForcePasswordResetException","UserMessage":"Unspecified Error",
   "MoreInfoUri":"https://monterey.api.rentmanager.com/Help/Subresource/Authentication/AuthorizeUser"}
  -> FINDING: client-side credential-state condition returned as 500, not 4xx.
- SECOND ATTEMPT (after operator reset) -> HTTP 200, opaque 108-char token string.
- Response adds `x-api-user: crane` on authenticated calls.
- Token expiry per QuickStart: 24h absolute / 15 min idle (documentation-graded).

### Step 5 — Rate limit + traceability headers (observed on every response)
    x-ratelimit-limit:     500
    x-ratelimit-observed:  <n>
    x-ratelimit-remaining: <500-n>
    x-ratelimit-reset:     <unix ts>
    x-ratelimit-resettime: <exactly 60s after request date>
    x-api-version:         12.2607.9741.10976
    x-api-user:            crane   (authenticated calls only)
**CONFLICT RESOLVED:** public Technical Documentation.pdf states hourly limiting with
`X-RateLimit: 60` / `X-RateRemaining` / `X-RateTimeLeft`. NONE of those header names
exist. Actual: five `x-ratelimit-*` headers, 500 per ROLLING MINUTE. Vendor support
(Weatherly, 2 Sep 2026) is correct; published documentation is wrong on the number,
the window, and the header names.
**NO request/correlation ID** on any response (no x-request-id / correlation / traceparent).

### Step 2 — Read core resource + paginate
- GET /Tenants?pagesize=3&pagenumber=1 -> 200; `x-total-results: 745`, `x-results: 3`
  Link: <...PageNumber=2>;rel="next", <...PageNumber=249>;rel="last"
- page 2 -> Link carries first/previous/next/last. Ordering consistent (TenantID asc).
- GET /Charges (no pagesize) -> auto-paginates: 200, x-results 1000, x-total-results 20917,
  Link present. **Docs say 206 Partial Content; observed 200.**
- GET /Charges?pagesize=5000 -> **returned 5000 rows.** Docs say pagesize is capped at
  1000. Cap NOT enforced -> bulk extraction easier than documented (undocumented capability).

### Step 3 — Incremental / filtered query
- GET /Tenants?filters=UpdateDate,gt,2026-01-01 -> 200, x-total-results **214** of 745. HONORED.
- GET /Tenants?filters=UpdateDate,gt,2099-01-01 -> **204 No Content**, x-total-results 0.
  (Docs say 404 for "no records after filter"; observed 204.)
- GET /Tenants?filters=NotAFieldXyz,eq,1 -> **400** {"Message":"The request is invalid.",
  "ModelState":{"filters":["Error parsing filter ... Field is not available for filtering."]}}
  -> filters validate properly and error usefully.

### Step 4 — Deliberate errors (four DISTINCT error shapes observed)
1. No token, GET /Tenants -> **401** ErrorModel {DeveloperMessage:"Missing ApiToken",
   UserMessage:"Authentication Failed.", ErrorCode:-2146233088,
   Exception:"ApiAuthenticationException", MoreInfoUri:.../Help/Resource/Tenants}
2. Bad token -> **401** ErrorModel "The ApiToken could not be validated."
3. Unknown route GET /NotARealResourceXyz -> **404** {"Message":"No HTTP resource was found..."}
   (bare ASP.NET shape, NOT ErrorModel)
4. Bad filter -> **400** {Message, ModelState} (third shape)
5. GET /Properties/99999999 -> **404 with EMPTY BODY** (fourth shape).
   Docs: "All 400 codes should return an ErrorModel object". Contradicted.
- GET /Reconciliations -> **403** ErrorModel "Insufficient privileges to access some or any
  banks. Use the single item get instead of a collection get" (correct status)
- GET /WebhookDetails -> **500** ErrorModel "Insufficient privileges to manage Webhook
  Details." / "Required privilege: Manage Webhooks."
  -> SAME class of condition (insufficient privileges) returns 403 on one resource and
     500 on another. Status semantics inconsistent.
- `ErrorCode` is **-2146233088 on every single error** = 0x80131500, the generic .NET
  System.Exception HRESULT. Not a stable per-error machine code. The `Exception` string
  IS discriminating (ApiAuthenticationException / AuthenticationForcePasswordResetException).

### Result-shaping parameters — what actually works
| Param | Documented | Observed |
|---|---|---|
| `fields` | yes | WORKS |
| `filters` | yes | WORKS (validates, 400s on bad field) |
| `pagenumber`/`pagesize` | yes | WORKS (cap not enforced) |
| `embed` (singular, per docs) | yes, with example `?embed=Color` | **BROKEN — silently returns `"Addresses": []`** |
| `embeds` (plural) | appears once in a doc example only | **WORKS** (field must also be in `fields=`) |
| `orderby` | "Partial Support" | **NON-FUNCTIONAL** |

#### orderby evidence (fair test — 6 spellings, with and without `fields=`)
orderby=Name / orderby=Name DESC / orderbys=Name DESC / orderBy=Name DESC / sort=Name /
orderbys=UpdateDate DESC — ALL returned identical default order (TenantID 920,921,922),
HTTP 200, no error. Also confirmed on /Properties (?orderby=Name%20DESC returned
PropertyID 854,855,856 = ID ascending). Even `orderby=NotAField` returns 200 silently,
while `filters=NotAField` correctly 400s. -> success code hides the failure.

#### embed evidence
- `?embeds=Addresses` alone -> base model, no Addresses key (ignored)
- `?fields=TenantID,Name,Addresses&embed=Addresses` -> `{"Addresses":[]}` **WRONG DATA**
- `?fields=TenantID,Name,Addresses&embeds=Addresses` -> full Addresses array. CORRECT.
- `/Tenants/920/Addresses` sub-resource -> works, returns real addresses.
-> The documented spelling produces a silently empty result that looks like "no data".

### `ApiUri` — documented but ABSENT
Overview doc: "All Data Models include the 'APIURI' field." Observed: /Properties/854
returns 32 keys, none is ApiUri. No collection response contained ApiUri. The documented
linked-data/HATEOAS contract does not exist on this build.

### Null-field omission
Vendors records returned 3,3,3,4 keys — `ColorID` present only when non-null. Response
shape varies record to record. Types themselves stayed consistent (number/boolean/string).

### Object coverage probes (pagesize=1, x-total-results)
| Resource | Status | Total |
|---|---|---|
| Properties | 200 | 334 |
| Units | 200 | 445 |
| Leases | 200 | 790 |
| Tenants | 200 | 745 |
| Charges | 200 | 20,917 |
| Payments | 200 | 17,493 |
| GLAccounts | 200 | 521 |
| Journals | 200 | 1,995 |
| Owners | 200 | 380 |
| Bills | 200 | 12,992 |
| ServiceManagerIssues | 200 | 5,345 |
| Prospects | 200 | 1,025 |
| Vendors | 200 | 499 |
| Contacts | 200 | 4,153 |
| HistoryNotes | 200 | 35,715 |
| UserDefinedFields | 200 | 261 |
| InventoryItems | 200 | 41 |
| SystemPreferences | 200 | 583 |
| Reports | 200 | 319 (incl. `CanAnalyzeWithAI` flag) |
| Banks | 204 | 0  <- permission-scoped, not absent |
| BankReconciliations | 204 | 0 |
| Deposits | 204 | 0 |
| Applications | 204 | 0 |
| Tasks | 204 | 0 |
| Violations | 204 | 0 |
| Reconciliations | 403 | privilege-scoped |
| WebhookDetails | 500 | privilege-scoped ("Manage Webhooks") — **webhooks EXIST** |
CAUTION: 204/0 and 403/500 results reflect this read-only user's scope and this
operator's data, NOT absence of the resource. All appear in the 369-resource index.

### Concurrency fields observed
`UpdateDate` on all core models; `ConcurrencyID` on Properties and Journals.
Docs: concurrency default-enabled, UpdateDate required on POST, 409 on mismatch,
"**Concurrency cannot currently be disabled**".

### Not supported
- OPTIONS -> 404 on every resource tested, no `Allow` header (no verb discovery).

### Call budget
~55 calls total. Limit 500/rolling minute, per company. Never approached; no 429 induced
(deliberately not induced — shared production limit with operator's live integrations).

---
## CORRECTIONS AND ADDITIONS after obtaining the login-gated per-resource reference
(operator supplied /Help/Resource/Leases, /Help/Resource/WebhookDetails, and the
API Download Resources page as saved HTML, 2026-09-07)

### CORRECTION 1 — the real ordering parameter is `orderingOptions`, not `orderby`
The live per-resource reference documents the collection URL as:
  GET Leases?filters={filters}&embeds={embeds}&orderingOptions={orderingOptions}&fields={fields}
with parameters filters / embeds / orderingOptions / fields / pageSize / pageNumber.
`orderby` (the Overview PDF's name) does not appear in the live reference at all.
RETESTED `orderingOptions` live with 13 value formats:
  Name | Name DESC | Name,DESC | Name,Ascending | Name,Descending | Name,asc | Name,ASC |
  (Name,ASC) | Ascending,Name | Name:ASC | TenantID,Descending | UpdateDate,DESC | NotAField
ALL returned **HTTP 404** with:
  {"DeveloperMessage":"The given key was not present in the dictionary.",
   "Exception":"KeyNotFoundException","ErrorCode":-2146232969,"UserMessage":"Unspecified Error"}
=> NET RESULT UNCHANGED, BUT BETTER EVIDENCED: sorting is unusable via EITHER documented
parameter name. `orderby` is silently ignored (HTTP 200, wrong order); `orderingOptions`
throws an unhandled .NET dictionary exception surfaced as 404 for every value including
valid field names. 404 is also the wrong status for a bad parameter value.

### CORRECTION 2 — `ErrorCode` is NOT a single constant (my earlier note was wrong)
ErrorCode maps to the .NET exception class HRESULT:
  -2146233088 = 0x80131500 System.Exception (auth, privilege, force-reset)
  -2146232969 = 0x80131577 KeyNotFoundException (bad orderingOptions)
So it does discriminate somewhat. It remains a .NET runtime HRESULT rather than a
documented, API-specific, stable error taxonomy, and it is not documented anywhere in
the first-party materials. `DeveloperMessage` and `Exception` are the useful fields.

### CORRECTION 3 — `embeds` plural is CORRECT per the live reference
The live reference documents `embeds` (type `LeaseEmbedOptions List`). The Overview PDF's
parameter table and its worked example use singular `embed`. The live reference is right;
the downloadable Overview PDF is wrong. This is a documentation defect, not an API defect.
Impact stands: a developer following the downloadable guide gets `"Addresses": []`.

### CORRECTION 4 — concurrency key is `ConcurrencyID`, not `UpdateDate`
Live reference marks `ConcurrencyID` (Integer) with attribute **"Concurrency Key"** on
WebhookDetailModel. Overview PDF says "request to update a record must include the
UpdateDate field". Observed ConcurrencyID on Properties and Journals. NOT present on
LeaseModel — so the concurrency key is applied inconsistently across resources.

### Per-resource operation pattern (from /Help/Resource/Leases and /WebhookDetails)
Every resource page lists its operations. Leases exposes:
  Retrieve Collection | Retrieve Instance | **Save** | Delete Collection | Delete Instance
  | **LeaseRenew** | ActiveLeaseRenewal | LeaseRenewals | Property | Tenant | Unit
  | RetailSales | CreateUser | UpdateUser | GetByPost | QuickSearch | Search
WebhookDetails exposes: Retrieve Collection | Retrieve Instance | Save | Delete Collection
  | Delete Instance | GetByPost | QuickSearch | Search
=> Create/update = a single **Save** operation (POST). Delete available at both collection
and instance level. Lifecycle actions exist as named subresources (e.g. LeaseRenew).
Each operation has its own page at /Help/Subresource/{Resource}/{Operation}.

### LeaseModel notable fields
IsCommercial, MoveInDate, MoveOutDate, ExpectedMoveOutDate, NoticeDate, IsMoveOutConfirmed,
ArrivalDate, DepartureDate, LeaseRenewals, PromotionPeriods, LeaseVehicles,
RenterInsurancePolicies, ActiveLeaseRenewal.
**StartDate / EndDate are Read Only + Calculated Field + "Requires Embed (LeaseRenewals)"**
— the lease term dates are NOT in the base model; live GET /Leases confirmed their absence.
Typing note: `UnitID` is declared `Int32` while every other integer is `Integer`
(cosmetic naming inconsistency in the published schema, same underlying type).

### WebhookDetailModel — complete field list
WebhookDetailID (Int, PK) | WebhookEventType (eWebhookEventType) | URL (String) |
PartnerProductID (Guid) | CreateDate | CreateUserID | UpdateDate | UpdateUserID |
ConcurrencyID (Concurrency Key) | CreateUser | UpdateUser | MetaTag
**NO signing secret, NO HMAC key, NO signature configuration field of any kind.**
No retry policy, delivery guarantee, or replay/idempotency guidance on the page.
Sample response confirms **no ApiUri field** — corroborating the live observation that
the Overview PDF's "All Data Models include the APIURI field" is false for this build.
`PartnerProductID` (Guid) suggests webhooks are oriented to integration partners
(cf. the "Partner Login" button on the docs portal) rather than end operators.

### API Download Resources page — COMPLETE inventory
The vendor's own downloads page lists exactly TWO items:
  "Quick Start Download"  -> Download Link
  "Overview Download"     -> Download Link
=> No OpenAPI/Swagger spec, no official SDK, no Postman collection, no MCP server.
The only other first-party machine-consumable artifact is the C# sample console app
referenced in the QuickStart (/content/quickstartapp/LCS.UI.API.QuickStart.Examples.zip).

### Docs portal navigation (first-party interface observation, operator screenshot 2026-09-07)
Introduction | Quick Start | Overview of Functionality | API Resources |
API Download Resources | API Test Client
=> An interactive API Test Client exists in the portal.

### Type inconsistency across endpoints (live)
Core resources return numeric primary keys: "PropertyID":854, "TenantID":920, "LeaseID":n.
But /Reports returns "ReportID":"1" (STRING) and /SystemPreferences returns
"PreferenceID":"1" (STRING). Same conceptual field, different JSON type by endpoint.

### Trust / fiduciary evidence (live + index)
ChargeModel exposes DepositStatus and IsSecurityDepositPriorToGLStartDate.
OwnerModel exposes IsBalanceReserves and BalanceAccountID.
Index includes SecurityDepositTypes, SecurityDepositInterest, Banks, BankReconciliations,
Reconciliations, Deposits, OwnerCheckSetups, ManagementFeeSetup(s), ManagementFeeHistory,
AccountGroups.

---
## PACKET F2 — evidence added from the authenticated documentation portal
(operator logged into /Help in the browser pane, 2026-09-07; pages fetched programmatically)

### Documentation URL patterns discovered
  /Help/Resource/{Resource}                      resource page + operation list
  /Help/Method/{Resource}/Save                   create/update operation
  /Help/Method/{Resource}/Retrieve/{Collection|Instance}
  /Help/Method/{Resource}/Delete/{Collection|Instance}
  /Help/Subresource/{Resource}/{Action}          action subresources
  /Help/Model/{ModelName}/{Resource}-{Operation} filter fields, embed options, ordering options
  /Help/Overview?nid=Home/Overview/{Topic}       narrative overview

### CORRECTION 5 — a THIRD ordering parameter name: `Orderings`
`/Help/Model/TenantOrderingOptions/Tenants-Retrieve-Collection` states verbatim:
  "To determine the order of the dataset returned by the API, Ordering Options can be
   added to the request URL. For Example, if you wanted to order by TenantName, you would
   build this url: http://monterey.api.rentmanager.com/{Resource}?Orderings=TenantName"
Possible Values for Tenants: **LastFirst**, **TenantName** (plus default "Unset").
RETESTED LIVE with the vendor's own example value:
  Orderings=TenantName | Orderings=LastFirst | Orderings=TenantName DESC |
  Orderings=Unset | Orderings=NotAnOption
  -> ALL returned HTTP 200 with the identical default order (TenantID 920,921,922,923).
**The vendor's own documented example does not work.**
THREE documented parameter names now tested, none functional:
  `orderby` (Overview)          -> 200, silently ignored
  `orderingOptions` (URL tmpl)  -> 404 KeyNotFoundException for every value
  `Orderings` (OrderingOptions) -> 200, silently ignored
Also: Leases, Properties, Charges, ServiceManagerIssues and WebhookDetails all report
"This endpoint has no available Ordering Options" — so most resources define none at all.

### CORRECTION 6 — void/reverse actions DO exist (I previously scored these 0.5)
Confirmed as action subresources on the financial resources:
  Charges/ConvertChargeToCredit
  Payments/PaymentReversal, Payments/ReversalReconciliation
  Journals/Reversal, Journals/ReverseJournal, Journals/RemoveJournalReversal
  Bills/Reversal
  Tenants/CreditReversals, Tenants/PaymentReversals, Tenants/RefundSecurityDeposit,
    Tenants/TransferSecurityDeposits, Tenants/TransferPayment, Tenants/ApplyNSFFees
  Properties/RollbackLastManagementFeePosting, Properties/AccountingClose
=> C1.3 void/reverse item raised 0.5 -> 1.0 (weighted coverage 15/16 -> 16/16).

### CORRECTION 7 — file/attachment resources DO exist (I previously scored files 0.5)
  Properties/PropertyFiles, Properties/PropertyFileFolders, Properties/Images,
  Properties/UploadImage, Properties/Logo, Properties/LogoFile
  Bills/Attachments, Bills/FileAttachments, Bills/UploadAttachment
  Journals/Attachments
  Units/Images, Units/DownloadImage
  ServiceManagerIssues/SignatureFile, /UploadSignatureFile
  {Resource}/UploadUserDefinedValueAttachment  (Tenants, Properties, Units, Owners, SMI)
  Owners/OWAFile, Owners/OWAFiles
=> C1.1 and C1.2 "files" item raised 0.5 -> 1.0 (weighted coverage 37.5/38 -> 38/38).

### Per-resource operation inventory — CONFIRMED, not inferred
All twelve core resources checked expose the IDENTICAL five methods:
  Retrieve/Collection | Retrieve/Instance | **Save** | Delete/Collection | Delete/Instance
Checked: Charges, Payments, Journals, Leases, Tenants, Properties, Units, Owners, Bills,
ServiceManagerIssues, Banks, GLAccounts.
=> C1.2 and C1.3 are no longer inferred from the Overview's general statement; they are
   confirmed per-resource. Marks unchanged (yes); evidence grade materially improved.

### Notable lifecycle / action subresources
  ServiceManagerIssues/Advance, /WorkOrders, /TechTimes, /CheckListItems, /Status
  Tenants/RunScreening, /Screenings, /Evictions, /Leases, /Transactions, /SecurityDeposits,
    /RecurringCharges, /MakePayments, /TransferTenant
  Properties/PostManagementFees, /PostSecurityDepositInterest, /CalculateManagementFees,
    /AccountingClose, /MergeProperties
  Payments/MakePayments, /PrintReceipt
  Units/ConvertUnitToAsset, /AssignMakeReadyProcess

### WebhookDetails Save — CONFIRMS C2.8 = no
  POST WebhookDetails?fields={fields}&embeds={embeds}
  body: items = WebhookDetailModel List
  Request body sample:
   [{ "WebhookDetailID":1, "URL":"sample string 2",
      "PartnerProductID":"362f6930-abac-401f-b57d-9eb6e8624039",
      "CreateDate":"...", "CreateUserID":3, "UpdateDate":"...", "UpdateUserID":4,
      "ConcurrencyID":5, "MetaTag":"sample string 7" }]
=> Registration accepts a URL and an event type. **No signing secret, no HMAC key, no
   signature configuration anywhere in the request or response model.**

### eWebhookEventType — NO DOCUMENTATION PAGE EXISTS
/Help/Model/eWebhookEventType/... returns the portal's "Not Found" page for both the
Retrieve-Collection and Save contexts. The event catalogue is undocumented.
=> C1.4 stays `partial`: webhook event coverage cannot be established, so credit rests
   on the verified incremental-polling limb of the rubric.

### Live Overview topic list — COMPLETE (16 topics)
RESTfulAPI, DataModels, LinkedData, Attributes, QueryStringParameters, Concurrency,
CreatingARecord, SupportingPartialUpdates, FiniteVsDynamicResults, BackwardsCompatibility,
Versioning, RespondingToRequestsForFeedback, CrossJoinTables, HttpResponseCodes,
ResourcesAndPermissions, AuthenticationProcess.
Full-text search of the live Overview:
  "webhook"      -> ABSENT
  "idempot"      -> ABSENT   (confirms C2.4: no idempotency documented anywhere)
  "retry"        -> ABSENT   (confirms C2.8)
  "signature"    -> ABSENT   (confirms C2.8)
  "signing"      -> ABSENT   (confirms C2.8)
  "rate limit"   -> ABSENT   } rate limiting is NOT documented in the live reference at
  "X-RateLimit"  -> ABSENT   } all, though the server enforces it and returns 5 headers
  "correlation"  -> ABSENT   (confirms C2.11)
  "request id"   -> ABSENT   (confirms C2.11)
  "Orderings"    -> ABSENT   (the Overview still documents `orderby`, contradicting the
                              per-resource reference's `orderingOptions` / `Orderings`)
  "ApiUri"       -> PRESENT, with the same false claim and `embed=Color` example as the
                    2015 PDF. The error is LIVE ON THE SITE TODAY, not merely a stale PDF.

### Filter documentation quality (a genuine strength)
/Help/Model/{X}FilterFields/... documents, per field, the exact operator set available
(lt, le, gt, ge, ne, eq, in, ni, bt, ct, hv, ltn, len, gtn, gen) with plain-language
descriptions, plus both the `?filters=` and `/Search?filterExpression=` forms.

### NET EFFECT ON SCORING
No check mark changed. C1.1/C1.2 weighted coverage rose 98.7% -> 100%; C1.3 rose
93.8% -> 100%; all remained `yes`. Both flagged upside scenarios resolved NEGATIVELY:
C2.8 confirmed `no` (complete Save model, no secret field); C1.4 confirmed `partial`
(event enum has no documentation page). **Scoring conclusions are recorded in the report card, not in this evidence log.**


---

# Appendix B — Documentation extracts (login-gated reference)

## Packet F2 — verbatim extracts from the login-gated documentation portal

Source: `https://monterey.api.rentmanager.com/Help` — accessed 2026-09-07 in an
operator-authenticated session (RM user `crane`, Location MBPM).
Server build at time of access: `12.2607.9741.10976`.

**Why this file exists.** The Rent Manager API reference is behind a customer login and
the credential used for this run was disabled after testing. These extracts preserve the
cited evidence so an independent grader can audit packet F2's citations without
credentials. Content is transcribed from the HTTP responses captured during the run.

---

### 1. Documentation URL patterns

```
/Help/Resource/{Resource}                        resource page + operation list
/Help/Method/{Resource}/Save                     create/update operation
/Help/Method/{Resource}/Retrieve/{Collection|Instance}
/Help/Method/{Resource}/Delete/{Collection|Instance}
/Help/Subresource/{Resource}/{Action}            action subresources
/Help/Model/{ModelName}/{Resource}-{Operation}   filter fields / embed options / ordering options
/Help/Overview?nid=Home/Overview/{Topic}         narrative overview
/Help/Download                                   downloadable materials
```

### 2. Per-resource operation inventory — cited by C1.2 and C1.3

Retrieved from `/Help/Resource/{Resource}` for each. **All twelve expose the identical
five methods:**

```
Retrieve/Collection | Retrieve/Instance | Save | Delete/Collection | Delete/Instance
```

| Resource | HTTP | Methods |
|---|---|---|
| Charges | 200 | Retrieve/Collection, Retrieve/Instance, Save, Delete/Collection, Delete/Instance |
| Payments | 200 | (identical five) |
| Journals | 200 | (identical five) |
| Leases | 200 | (identical five) |
| Tenants | 200 | (identical five) |
| Properties | 200 | (identical five) |
| Units | 200 | (identical five) |
| Owners | 200 | (identical five) |
| Bills | 200 | (identical five) |
| ServiceManagerIssues | 200 | (identical five) |
| Banks | 200 | (identical five) |
| GLAccounts | 200 | (identical five) |

#### Action subresources cited for C1.3 (void / reverse / lifecycle)

```
Charges/ConvertChargeToCredit
Payments/PaymentReversal, Payments/ReversalReconciliation, Payments/MakePayments
Journals/Reversal, Journals/ReverseJournal, Journals/RemoveJournalReversal
Bills/Reversal
Tenants/CreditReversals, Tenants/PaymentReversals, Tenants/RefundSecurityDeposit,
  Tenants/TransferSecurityDeposits, Tenants/TransferPayment, Tenants/ApplyNSFFees,
  Tenants/TransferTenant, Tenants/Evictions, Tenants/RunScreening
Properties/RollbackLastManagementFeePosting, Properties/PostManagementFees,
  Properties/PostSecurityDepositInterest, Properties/AccountingClose
Leases/LeaseRenew, Leases/ActiveLeaseRenewal, Leases/LeaseRenewals
ServiceManagerIssues/Advance, /Status, /WorkOrders, /TechTimes, /CheckListItems
Units/ConvertUnitToAsset, Units/AssignMakeReadyProcess
```

#### File and attachment subresources cited for C1.1 and C1.2

```
Properties/PropertyFiles, Properties/PropertyFileFolders, Properties/Images,
  Properties/UploadImage, Properties/Logo, Properties/LogoFile
Bills/Attachments, Bills/FileAttachments, Bills/UploadAttachment
Journals/Attachments
Units/Images, Units/DownloadImage
ServiceManagerIssues/SignatureFile, ServiceManagerIssues/UploadSignatureFile
Owners/OWAFile, Owners/OWAFiles
{Tenants|Properties|Units|Owners|ServiceManagerIssues}/UploadUserDefinedValueAttachment
```

---

### 3. `/Help/Method/WebhookDetails/Save` — cited by C2.8 (verbatim)

```
WebhookDetails Save
Save a collection of items to the collection.

Request Information
Url
  POST WebhookDetails?fields={fields}&embeds={embeds}
Parameters
  items    WebhookDetailModel List          Define this parameter in the request body.
  fields   String                           Define this parameter in the request URI.
  embeds   WebhookDetailEmbedOptions List   Define this parameter in the request URI.

Request body formats: application/json, text/json, multipart/form-data
Sample:
[
  {
    "WebhookDetailID": 1,
    "URL": "sample string 2",
    "PartnerProductID": "362f6930-abac-401f-b57d-9eb6e8624039",
    "CreateDate": "2026-09-07T12:54:28.4277468-04:00",
    "CreateUserID": 3,
    "UpdateDate": "2026-09-07T12:54:28.4277468-04:00",
    "UpdateUserID": 4,
    "ConcurrencyID": 5,
    "MetaTag": "sample string 7"
  }
]

Response Information
Model: WebhookDetailModel
Properties (Name / Type / Optimized Filters / Attributes):
  WebhookDetailID    Integer            EqualTo, In     Primary Key
  WebhookEventType   eWebhookEventType  EqualTo
  URL                String
  PartnerProductID   Guid               EqualTo
  CreateDate         DateTime
  CreateUserID       Integer            EqualTo, In
  UpdateDate         DateTime
  UpdateUserID       Integer            EqualTo, In
  ConcurrencyID      Integer                            Concurrency Key
  CreateUser         UserModel
  UpdateUser         UserModel
  MetaTag            String
```

**Finding:** the complete registration model contains no signing secret, no HMAC key, and
no signature configuration field. No retry policy or replay guidance appears on the page.

---

### 4. `/Help/Model/eWebhookEventType/…` — cited by C1.4

Requested in both documented contexts:
- `/Help/Model/eWebhookEventType/WebhookDetails-Retrieve-Collection`
- `/Help/Model/eWebhookEventType/WebhookDetails-Save`

Both returned the portal's not-found page:

```
Not Found
The page cannot be found
The page you are looking for might have been removed, had its name changed,
or is temporarily unavailable.
```

**Finding:** the webhook event catalogue has no documentation page.

---

### 5. Ordering options — cited by C2.6

#### `/Help/Model/TenantOrderingOptions/Tenants-Retrieve-Collection` (verbatim)

```
Tenant Ordering Options
Usage Notes
To determine the order of the dataset returned by the API, Ordering Options can be
added to the request URL.
For Example, if you wanted to order by TenantName, you would build this url:
  http://monterey.api.rentmanager.com/{Resource}?Orderings=TenantName
Some Ordering Options can result in very large return sizes. The use of those Ordering
Options is restricted, and they can only be used when retrieveing a single item.
Ordering Options restricted in this way have their IsCollectionOrdering property set to false.
Every set of Ordering Options has one default value:
  Unset - This is equivalent to not ordering at all.
Possible Values
  Name        Description
  LastFirst   LastFirst
  TenantName  Name
```

#### Every other ordering-options page checked (verbatim)

`/Help/Model/{Lease|Property|Charge|ServiceManagerIssue|WebhookDetail}OrderingOptions/…`

```
This endpoint has no available Ordering Options.
```

#### Live retest against the vendor's own documented example

| Request | HTTP | First four rows returned |
|---|---|---|
| `/Tenants?pagesize=4&fields=TenantID,Name&Orderings=TenantName` | 200 | 920 Mary Zoller, 921 Mark Scott Jr., 922 Mohammad & Patricia Borna, 923 Efron Amancio |
| `…&Orderings=LastFirst` | 200 | identical |
| `…&Orderings=TenantName DESC` | 200 | identical |
| `…&Orderings=Unset` | 200 | identical |
| `…&Orderings=NotAnOption` | 200 | identical |

**Finding:** the vendor's own worked example returns the default order (TenantID ascending)
with HTTP 200 and no error. Combined with the earlier `orderby` and `orderingOptions`
tests, all three documented parameter names are non-functional.

---

### 6. `/Help/Model/WebhookDetailFilterFields/…` — cited by C4.1 (verbatim excerpt)

```
Usage Notes
To filter a collection, the Filters property needs to be added to the request URL.
For Example, if you wanted to filter by ConcurrencyID, you would build this url:
  http://monterey.api.rentmanager.com/{Resource}?filters=ConcurrencyID,lt,{value}
  http://monterey.api.rentmanager.com/{Resource}/Search?filterExpression=ConcurrencyID,lt,{value}
You can filter on multiple fields by separating each field with a semicolon.
Possible Values
  ConcurrencyID  Int       lt, le, gt, ge, ne, eq, in, ni, bt, ct
  CreateDate     DateTime  lt, le, gt, ge, ne, eq, in, ni, bt, hv, ltn, len, gtn, gen
  ...
```

Operator glossary rendered per field: lt Less Than, le Less Than or Equal, gt Greater Than,
ge Greater Than or Equal, ne Not Equal To, eq Equal To, in In List, ni Not In List,
bt Between, ct Contains, hv Has Value, ltn Less Than or Null, len Less Than or Equal or Null,
gtn Greater Than or Null, gen Greater Than or Equal or Null.

**Finding:** this is a genuine documentation strength and is cited as such in C4.1.

---

### 7. Live Overview — complete topic index, cited by C2.4, C2.8, C2.11, C4.1, C4.4

`/Help/Overview?nid=Home/Overview/{Topic}` — the complete set of 16 topics:

```
RESTfulAPI            DataModels                      LinkedData
Attributes            QueryStringParameters           Concurrency
CreatingARecord       SupportingPartialUpdates        FiniteVsDynamicResults
BackwardsCompatibility Versioning                     RespondingToRequestsForFeedback
CrossJoinTables       HttpResponseCodes               ResourcesAndPermissions
AuthenticationProcess
```

#### Full-text search results across the live Overview

| Term | Result |
|---|---|
| `webhook` | **ABSENT** |
| `idempot` | **ABSENT** — cited by C2.4 |
| `retry` | **ABSENT** — cited by C2.8 |
| `signature` | **ABSENT** — cited by C2.8 |
| `signing` | **ABSENT** — cited by C2.8 |
| `rate limit` | **ABSENT** — cited by C4.1 |
| `X-RateLimit` | **ABSENT** — cited by C4.1 |
| `correlation` | **ABSENT** — cited by C2.11 |
| `request id` | **ABSENT** — cited by C2.11 |
| `Orderings` | **ABSENT** — the Overview documents `orderby` instead |
| `ApiUri` | **PRESENT**, with the false claim and the `embed=Color` example — cited by C4.1 and C4.4 |

`ApiUri` context, verbatim from the live page:

```
…rentmanager.com/Tenants?embed=Color
Response  Here we see the result of the embed parameter.
{ "ApiUri": "https://sampleco.api.rentmanager.com/Tenants/1", "Id": 1,
  "FirstName": "Joe", "LastName": "Rocker", "ColorId": 1,
  "Color": { "ApiUri": "https://sample…
```

**Finding:** the `ApiUri` claim and the singular `embed` example are live on the site today,
not merely stale in the 2015 PDF. Live `GET /Properties/854` returned 32 fields, none of
them `ApiUri`; `?embed=Addresses` returns an empty array while `?embeds=Addresses` works.

---

### 8. `/Help/Download` — cited by C4.2 (verbatim)

```
Rent Manager Web API Downloads
API Downloads
  Name                    Link
  Quick Start Download    Download Link
  Overview Download       Download Link
```

**Finding:** the vendor's complete downloadable inventory is two PDFs. No OpenAPI or
Swagger specification, no SDK, no Postman collection, no MCP server.

---

### 9. Portal navigation — first-party interface observation

```
Introduction | Quick Start | Overview of Functionality | API Resources |
API Download Resources | API Test Client
```

Captured by operator screenshot, 2026-09-07. An interactive **API Test Client** exists in
the portal; it was not exercised (it would issue live calls).
