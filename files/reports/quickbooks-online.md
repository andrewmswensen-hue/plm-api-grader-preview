# API Report Card: Intuit QuickBooks Online Accounting API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Fable 5
- Date run: September 2, 2026
- Provisional evidence-packet version or ID: qbo-2026-09-02-v1
- Final evidence-packet version or ID: qbo-2026-09-02-v2
- Evidence-discovery mode: tool-enabled discovery
- Evidence tier: baseline verified
- Live-write method and safety: sandbox (Sandbox Company US bb1d, realm 9341457843926067, operator-supplied Development credential; all fixtures carried the APITEST-DELETE sentinel, were deactivated after testing, and cleanup was verified and logged)
- Minimum live-test battery: steps 1-7 complete; step 8 not possible (webhook subscriptions are configured only in the developer portal UI and require a public operator-controlled endpoint, which was not available)
- Live tests performed: authenticate (production and sandbox); read and paginate a core resource (disjoint pages, totalCount); incremental updated-since query honored; CDC endpoint call; deliberate-error probe; rate-limit and traceability header observation; sandbox customer create, sparse update, and Active=false archival; stale-SyncToken conflict probe; identical create sent twice with the same requestid
- Live tests not possible: step 8 webhook delivery
- Documentation-graded checks (baseline verified): C2.8

## Final evidence packet manifest
- https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks
- https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks/configure-webhooks
- https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks/best-practices
- https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks/data-objects
- https://developer.intuit.com/app/developer/qbo/docs/learn/rest-api-features
- https://developer.intuit.com/app/developer/qbo/docs/learn/limits-and-throttles
- https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/data-queries
- https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/change-data-capture
- https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/batch
- https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/minor-versions
- https://developer.intuit.com/app/developer/qbo/docs/learn/scopes
- https://developer.intuit.com/app/developer/qbo/docs/learn/premium-apis
- https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0
- https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes
- https://developer.intuit.com/app/developer/qbo/docs/develop/troubleshooting/error-codes
- https://developer.intuit.com/app/developer/qbo/docs/develop/troubleshooting/api-status
- https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples
- https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples-collections/java/request-and-response-tracking
- https://developer.intuit.com/app/developer/qbo/docs/release-notes
- https://developer.intuit.com/app/developer/qbo/docs/get-started/get-client-id-and-client-secret
- https://developer.intuit.com/app/developer/qbo/docs/get-started/create-a-request
- https://developer.intuit.com/app/developer/qbo/docs/go-live
- https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice
- https://status.developer.intuit.com/
- https://developer.intuit.com/llms.txt and https://developer.intuit.com/llms-full.txt (verified 404)
- Live-test observation logs: production read-path battery (realm 680422830) and sandbox write battery with request/response log (realm 9341457843926067), September 2, 2026

## Evidence-amendment log
- C2.4, C2.11: added sdks-and-samples-collections/java/request-and-response-tracking while verifying requestid and trace-identifier semantics
- C2.4: checked get-started/create-a-request for requestid duplicate-suppression semantics; none found (negative finding recorded)
- C2.12: added rendered status.developer.intuit.com to verify incident history and uptime data
- C5.3: added learn/premium-apis while verifying commercial gating
- C1.4: added develop/webhooks/data-objects while verifying event payload structure

## API eligibility
- Qualifying API: yes
- API operator: Intuit [developer.intuit.com documentation; API host quickbooks.api.intuit.com]
- Access or credential issuer: Intuit developer portal, per-app OAuth 2.0 client credentials [get-client-id-and-client-secret page]
- Eligibility basis: first-party REST API v3 exposing QuickBooks Online accounting functions, with documented credential issuance; live-verified by authenticated calls to production and sandbox companies

## Context
- Software category: accounting/PMS platform (general accounting)
- What the API is for and its core objects and workflows: the API exposes the QuickBooks Online accounting engine - chart of accounts, customers and vendors, AR/AP transactions, journal entries, payments, and 30+ report entities - with query, change-data-capture, batch, and webhook facilities.

## Provider and property-management fit
- What this product is: general-purpose small-business accounting software with a public developer API [developer.intuit.com docs]
- Bank status, when relevant: N-A
- Who provides any bank account or regulated banking service: N-A
- What the customer actually receives: a hosted accounting system (general ledger, AR/AP, reporting) with API access to its records [docs/learn section]
- Property-management fit: general-purpose [docs/workflows navigation: invoicing, billing, inventory, projects, business units; no PM workflows]
- Documented PM-specific workflows: none found
- Trust or fiduciary workflow support: not documented - no trust-accounting, security-deposit, client-fund, or escrow workflows appear in first-party materials
- Operational role and dependencies: the general-ledger layer a property manager syncs into; a PMS and any trust-accounting layer must come from other systems

## Coverage classification (fixed before inspection)
Default Accounting/PMS classification. Pre-recorded interpretation: PM objects are scored by their accounting function through Intuit-documented native constructs (tenants as Customer; properties as Class/Department; lease ledger as AR transactions; general ledger as JournalEntry plus reports). Applicants pre-marked N-A (leasing-specific, no accounting function). Associations interpreted as HOA associations.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Properties | Critical | 3 | Present (Class/Department, full operations) |
| Units | Critical | 3 | Partial (sub-class/sub-customer nesting only) |
| Leases | Critical | 3 | Partial (RecurringTransaction proxy only) |
| Tenants | Critical | 3 | Present (Customer, full operations) |
| Lease ledgers/transactions | Critical | 3 | Present (Invoice/Payment/CreditMemo/JournalEntry) |
| General ledger | Critical | 3 | Present (JournalEntry plus GL/TrialBalance reports) |
| Bank accounts | Critical | 3 | Present (Account) |
| Owners | Important | 2 | Present (Vendor/Customer records) |
| Bills | Important | 2 | Present (Bill) |
| Payments | Important | 2 | Present (Payment/BillPayment) |
| Applicants | Important | 2 | N-A (pre-recorded) |
| Work orders/tasks | Important | 2 | Absent |
| Reconciliation | Important | 2 | Absent |
| Files | Optional | 1 | Present (Attachable) |
| Communications | Optional | 1 | Partial (invoice send-email only) |
| Custom fields | Optional | 1 | Partial (3 legacy sales-form fields; 12-field API tier-gated) |
| Associations (HOA) | Optional | 1 | Absent |
| Inventory | Optional | 1 | Present (Item, InventoryAdjustment) |

## Functional coverage map
- Core objects: as classified above; presence and operations cited from the all-entities API reference [invoice entity page navigation] and live reads (Customer, Vendor, BillPayment, Purchase)
- Primary operational workflows: read core records (present, live-verified); post ledger charges and payments (present - Invoice/JournalEntry/Payment create with worked samples); create and update leases (partial - RecurringTransaction proxy only)
- Principal lifecycle changes: invoice void/delete/send (present); credit and refund via CreditMemo/RefundReceipt/VendorCredit (present); archive via Active flag (present, live-observed); lease termination (partial proxy); work-order status transitions (absent); reconciliation close (absent)

## Category 1: Functional Coverage and Usefulness: 7.5/15
- C1.1 Object coverage: partial - weighted coverage = 78%; no critical object fully absent [all-entities reference navigation; live reads]
- C1.2 Core operational actions: partial - weighted coverage = 78%; posting charges and payments fully supported and the write path live-observed in sandbox; lease create/update only a 0.5 proxy [invoice entity reference; sandbox write battery]
- C1.3 Delete or lifecycle actions: partial - weighted coverage = 75%; void/delete/send and credit/refund present, Active-flag archival live-observed; lease termination a proxy; work-order and reconciliation lifecycle actions absent [invoice entity reference; sandbox write battery]
- C1.4 Change notification: partial - efficient incremental polling live-verified (updated-since filter honored; CDC endpoint, 30-day window); webhooks exist but the supported-entities list was not evidenced in the packet, so 85%+ push coverage could not be established [cdc page; live step 3; configure-webhooks page]

Score math: earned 2.0 of 4 applicable checks; unrounded fraction = 0.500; category points = 7.5/15; verification coverage = 100%

What this means for you: everything the ledger runs on is fully readable and writable, but property-management concepts (units, leases, work orders) exist only as accounting workarounds, and reconciliation status is invisible to the API.

## Category 2: API Design, Reliability, and Operability: 9.2/10
- C2.1 Modern conventions: partial - resource-oriented JSON REST, but create, update, delete, and void all use POST (delete via ?operation=delete) and query/CDC use text bodies [api-features, data-queries pages]
- C2.2 Consistent typing: yes - published attribute types consistent with rendered samples; live reads matched [invoice entity reference; live steps 2-3]
- C2.3 Structured errors: yes - live 400 with Fault type ValidationFault, stable code 4001, message and detail; documented code tables [error-codes page; live step 4]
- C2.4 Duplicate prevention: yes - live-observed: two identical creates with the same requestid returned the same record (same Id, SyncToken, CreateTime); exactly one record verified by query [sandbox write battery log]
- C2.5 Graceful handling under load: yes - documented limits with 429 and explicit wait-60-seconds recovery guidance [limits-and-throttles page]
- C2.6 Pagination: yes - STARTPOSITION/MAXRESULTS with ORDERBY and totalCount, documented 1000-row cap; disjoint pages live-verified [data-queries page; live step 2]
- C2.7 Bulk or incremental export: yes - CDC endpoint (30-day lookback) plus updated-since queries with pagination, live-verified; batch endpoint supplements [cdc, batch pages; live step 3]
- C2.8 Webhook security and delivery reliability: yes (documentation-graded) - HMAC-SHA256 intuit-signature with verifier token, documented retry ladder (10s to 6h), and consumer ordering/dedup guidance [configure-webhooks, best-practices pages]
- C2.9 Concurrency and conflict control: yes - SyncToken optimistic locking live-observed: stale-token write returned 400 with stable code 5010 Stale Object Error; concurrency limits documented [sandbox write battery log; limits page]
- C2.10 Versioning and backward compatibility: partial - explicit version identifiers (v3 path plus minorversion parameter) and release notes, but the compatibility policy is thin: minor versions 1-74 were discontinued en masse in August 2025 and sub-75 pins are now silently ignored [minor-versions page]
- C2.11 Request traceability: yes - intuit_tid and x-request-id observed on every live response; tracking identifier documented for support correlation [live step 5; SDK request-tracking page]
- C2.12 Service availability and status transparency: yes - public status page with per-service 90-day uptime percentages, incident history, and a status API [status.developer.intuit.com]

Score math: earned 11.0 of 12 applicable checks; unrounded fraction = 0.9167; category points = 9.2/10; verification coverage = 100%

What this means for you: a mature, operable API. Automations get signed webhooks, working duplicate suppression, optimistic locking, trace IDs, and a real status page. The rough edges are legacy conventions, an under-documented idempotency feature, and a weak version-compatibility contract.

## Category 3: Access Control and Safe Automation: 3.5/5
- C3.1 Read-only credentials: no - the Accounting API has exactly one scope, com.intuit.quickbooks.accounting, granting read and write; no read-only option [scopes page]
- C3.2 Scoped credentials: partial - bucket-level scoping only (accounting vs payments vs openid); nothing finer within accounting [scopes page]
- C3.3 Multiple keys: yes - multiple apps per developer account, each with its own credential pair, plus separate Development and Production sets [credentials page; oauth guide]
- C3.4 Rotation and revocation: yes - self-serve revoke endpoint documented; secrets regenerable in the dashboard [oauth guide]
- C3.5 Test and production isolation: yes - separate Development and Production credentials, separate sandbox host, isolated sandbox companies (exercised by this run's sandbox battery) [credentials, sandboxes pages; live]

Score math: earned 3.5 of 5 applicable checks; unrounded fraction = 0.700; category points = 3.5/5; verification coverage = 100%

What this means for you: you cannot hand an integration or AI agent a read-only key to your books. Any credential you issue can post journal entries.

## Category 4: Documentation and AI-Agent Readiness: 4.4/5
- C4.1 Complete self-serve reference: yes - public per-entity reference with attributes, business rules, and worked request/response samples for every operation [invoice entity reference]
- C4.2 Reliable machine-consumable integration path: yes - maintained official SDKs for Java/.NET/PHP covering core operations (Node/Ruby/Python are OAuth-focused); XSDs downloadable; no official OpenAPI specification evidenced [sdks page; release notes]
- C4.3 AI-readable documentation: partial - per-page "Copy all for AI" affordance and an AI prompt library exist, but no llms.txt (404 verified) or downloadable documentation corpus [verified negative findings]
- C4.4 Kept current: yes - four maintained release-note streams (general, Accounting API, minor versions, SDK) with dated entries [release-notes, minor-versions pages]

Score math: earned 3.5 of 4 applicable checks; unrounded fraction = 0.875; category points = 4.4/5; verification coverage = 100%

What this means for you: a developer or AI coding tool can build against this API from public documentation alone, though AI tools must scrape page by page rather than ingest a corpus.

## Category 5: Accessibility and Cost: 7.5/15
- C5.1 Self-serve API key: partial - Development keys are instant, but Production credentials are gated behind a Production Key questionnaire and its approval [get-client-id-and-client-secret page]
- C5.3 Not commercially gated: partial - the core Accounting API is included with any QBO subscription, but Premium APIs (Projects, 12-field Custom Fields, Sales Tax, Dimensions, Payroll Compensation) require Silver/Gold/Platinum partner tiers, and the Builder tier caps at 500K CorePlus calls per month [premium-apis, limits-and-throttles pages]

Score math: earned 1.0 of 2 applicable checks; unrounded fraction = 0.500; category points = 7.5/15; verification coverage = 100%

What this means for you: you can start building against a sandbox today for free, but going live requires Intuit's questionnaire approval, and some newer APIs sit behind partner tiers.

## Total
- Raw: 32.04 / 50
- Normalized before rounding: 64.08 / 100
- Published numeric score: 64 / 100
- Letter grade: D
- Evidence tier: baseline verified
- Overall verification coverage: 100% (gate: no category Unable to verify; overall at least 80%)
- Partial-result flag: no
- Unresolved evaluator disagreements: none - three independent runs compared at check level against the same final packet; all disagreements (C1.3, C1.4, C2.3) resolved against the evidence before calculating the published score

## Bottom line for a property manager
You can build real automations on this API today: read and post anything on the ledger, get signed webhooks when data changes, sync full datasets incrementally, and retry writes safely thanks to working duplicate suppression. The engineering fundamentals are genuinely strong. What drags the grade down is fit and access: there are no property, unit, lease, work-order, or reconciliation objects, so QuickBooks Online can only ever be the general-ledger layer behind a PMS, and the all-or-nothing read/write scope means any integration or AI agent you connect can write to your books. QuickBooks Online is not a substitute for a PMS or a trust-accounting system, and nothing in its API evidences trust or fiduciary workflows.
