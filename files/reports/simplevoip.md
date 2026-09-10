# API Report Card: SimpleVoIP LLC — SimpleVoIP Platform API and Customer API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 5 (1M context)
- Date run: 2026-09-10
- Provisional evidence-packet version or ID: SVOIP-2026-09-10-P1
- Final evidence-packet version or ID: SVOIP-2026-09-10-F1 (frozen after one controlled verification pass)
- Evidence-discovery mode: tool-enabled discovery
- Independent grading runs: 3, all against final packet SVOIP-2026-09-10-F1. Runs 2 and 3 were graded by separate evaluators given the frozen packet, the pre-fixed classification, and the corpus, with no sight of this report or its marks. Check-level comparison and reconciliation are in the Total section.
- Evidence tier: **Baseline verified**
- Live-write method and safety: none — writes documentation-graded. The operator declined live-data write testing in writing at the start of the session and reaffirmed it when supplying credentials ("Still no writes anywhere"). No create, update, or delete was issued on either surface. No SMS was sent, no webhook was registered, no call recording audio was downloaded.
- Minimum live-test battery: steps 1–5 complete on both surfaces. Step 6 (create/update) not run — operator declined. Step 7 (idempotency) **N-A** — neither surface documents an idempotency mechanism. Step 8 (webhook registration) not run — operator prohibited it.
- Live tests performed: authentication; core-resource reads across 21 platform collections; cursor pagination across two CDR pages; incremental and filtered queries; sparse fieldsets; bulk CSV export; four deliberate error conditions on the platform API and three on the customer API; response-header and rate-limit-signal capture; credential-scope probing; route-level method advertisement via CORS preflight (non-mutating).
- Live tests not possible: none within the authorized read-only scope.
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, and the delivery half of C2.8. Each is flagged in place below.

## Final evidence packet manifest

**SimpleVoIP first-party**
- https://simplevoip.com — primary navigation and product positioning
- https://simplevoip.com/apis/ — names and links both API surfaces
- https://simplevoip.com/crm-connect/ — property-management offering
- https://simplevoip.com/features-and-plans/ — plan tiers
- https://simplevoip.com/sitemap.xml ; https://simplevoip.com/llms.txt (404)
- https://support.simplevoip.com/hc/en-us/articles/7767228147607-Time-of-Day-Bulk-Change-API
- https://support.simplevoip.com/hc/en-us/articles/13407477118103-Outbound-SMS-API
- https://support.simplevoip.com/hc/en-us/articles/13927479256855-Call-Detail-Record-CDR-Webhooks
- https://support.simplevoip.com/hc/en-us/articles/360058871193-SimpleVoIP-Service-Level-Agreement
- https://support.simplevoip.com/api/v2/help_center/en-us/articles.json — help-center inventory with creation and update dates
- https://documenter.getpostman.com/view/1052474/2s9YXmZ1TL — "SimpleVoIP API" Postman collection, linked from the vendor's own APIs page; retrieved as structured JSON from documenter.gw.postman.com
- https://status.simplevoip.us and https://status.simplevoip.us/history.atom
- Live observation: https://public.simplevoip.us — read-only calls, 2026-09-10
- Live observation: https://portal.simplevoip.us:8443/v2/ — read-only calls, 2026-09-10
- Written statement from a SimpleVoIP engineer dated 2026-09-10, supplied by the operator, describing the parent/child account structure and the self-serve location of the account API key in the portal

**2600Hz, adopted by SimpleVoIP as the platform API reference**
- https://docs.2600hz.com/developers/rest/introduction
- https://docs.2600hz.com/developers/rest/overview/api-basics
- https://docs.2600hz.com/developers/rest/overview/query-string-filters
- https://docs.2600hz.com/developers/rest/overview/json-schema
- https://docs.2600hz.com/developers/rest/overview/rate-limits
- https://docs.2600hz.com/developers/rest/authentication/account-api-authentication
- https://docs.2600hz.com/developers/rest/authentication/scope-restrictions
- https://docs.2600hz.com/developers/rest/authentication/token-restrictions
- https://docs.2600hz.com/developers/rest/webhooks/webhooks
- https://docs.2600hz.com/developers/rest/usage/call-detail-records
- https://docs.2600hz.com/developers/rest/sys-admin/rate-limiting
- https://docs.2600hz.com/developers/changelog/kazoo-51-53-breaking-changes
- https://docs.2600hz.com/more/legacy-http-api/the-basics/quick-start/crossbar-sdks
- https://docs.2600hz.com/sitemap.xml — 742 URLs with last-modified dates
- https://docs.2600hz.com/llms.txt and /llms-full.txt (both 404)
- https://github.com/2600hz/kazoo/blob/master/applications/crossbar/priv/api/swagger.json
- https://github.com/2600hz/kazoo/blob/master/doc/engineering/documentation.md

## Evidence-amendment log
Sources added during the single controlled verification pass, each tied to the check it resolves:
- `swagger.json` and `doc/engineering/documentation.md` in the 2600Hz repository — added for C4.2 after the documentation site was found to publish no specification.
- `developers/rest/sys-admin/rate-limiting` — added for C2.5 after the page titled "Rate Limits" in the developer overview proved to cover SIP packet limits rather than HTTP throttling.
- `more/legacy-http-api/the-basics/quick-start/crossbar-sdks` — added for C4.2 to test whether an official SDK exists.
- One targeted first-party search across 2600hz.com and docs.2600hz.com for If-Match, ETag, 409, conflict, and deprecation policy — added for C2.9 and C2.10.
- Direct probes for `.md` and `.txt` variants of documentation pages, and for `llms.txt` on both domains — added for C4.3.
- Help-center searches for sandbox, test account, trial, and developer account — added for C3.5.
- Sitemap last-modified analysis across all 123 developer pages, plus help-center article dates — added for C4.4.

No source was removed after provisional scoring began.

## API eligibility
- Qualifying API: **yes**
- API operator: SimpleVoIP LLC operates both endpoints. The vendor's own APIs page names them as "Platform APIs — Our core voice platform API, with account, user, device and call routing capabilities" and "Customer APIs — Public API endpoints designed to simplify common API functions for customers" [simplevoip.com/apis/].
- Access or credential issuer: SimpleVoIP LLC. For the platform surface, the vendor's engineer states in writing that the customer logs into the vendor's own instance and reads the account API key from the portal under Authentication, API Key Authentication, API Key Value. For the customer surface, the vendor's published article states the key is "provided by the SimpleVoIP Engineering team" on request through an account manager [Time of Day Bulk Change API, Prerequisites].
- Eligibility basis: Both interfaces run on hostnames the vendor controls, expose the vendor's own service data, and are credentialed by the vendor. Confirmed live on 2026-09-10: an account API key exchanged at `PUT /v2/api_auth` on `portal.simplevoip.us:8443` returned HTTP 201 with a scoped auth token, and a vendor-issued Bearer token returned HTTP 200 from `public.simplevoip.us`.

**Disclosure that affects how several checks below read.** The platform surface is 2600Hz's Kazoo Crossbar API. SimpleVoIP operates the endpoint and issues the credentials, which makes it a qualifying vendor API, but the interface design, the reference documentation, and the release cadence belong to 2600Hz. SimpleVoIP adopts that documentation by reference from its own APIs page rather than publishing its own. Where a capability is 2600Hz's engineering rather than SimpleVoIP's, the report says so.

**Scoring convention for two surfaces, stated for reproducibility.** This vendor ships two API surfaces of very different quality, and several checks resolve differently on each. They are graded as one API — the union an operator actually builds against — rather than as two separate evaluations, because the surfaces are not interchangeable: the customer API is the only documented path to bulk multi-site schedule changes and to outbound SMS, and the platform SMS listing endpoint returns a server error on this cluster, so a complete integration must touch both. Where the surfaces differ, the check is marked partial and both are cited. This convention costs the vendor roughly two points against a counterfactual in which only the platform API existed, and it affects C2.3, C2.8, C2.11, and C5.1. A reproducing evaluator who grades only the platform surface should expect a higher Category 2 result.

## Context
- Software category: **other** — a business VoIP and unified-communications platform used as an operating tool alongside a property management system.
- What the API is for and its core objects and workflows: The platform API configures and reads the phone system itself — the account tree, users and extensions, desk phones and softphones, call routing and menus, schedules, voicemail, recordings, and call detail records. The customer API is a small vendor-built layer over the same platform that performs a few bulk administrative jobs across many sites at once and sends outbound SMS. For a property manager the API's job is to keep staff phone provisioning in step with headcount, change how calls route as offices open and close, and get call history out into reporting.

## Provider and property-management fit
- What this product is: a hosted business phone system with AI call analytics, sold to multi-location organizations [simplevoip.com].
- Bank status, when relevant: N-A.
- Who provides any bank account or regulated banking service: none. The product does not hold, move, or account for funds.
- What the customer actually receives: a managed multi-tenant phone service delivered from the vendor's Kazoo cluster, an administrative portal, desk and mobile clients, and — on request and after approval — API credentials to two interfaces.
- Property-management fit: **dedicated PM offering**. The vendor's property-management page states it is "A complete cloud communications platform for property management teams" and "Purpose-built for property management communications," and identifies the company as an official AppFolio Stack App Partner [simplevoip.com/crm-connect/]. It is not PM-specialized: the company sells across several industries, and its API documentation is written for multi-store retail, describing "the rules governing store open vs. closed logic," "store numbers," and embedding messaging "in your own user portal or POS system."
- Documented PM-specific workflows: click-to-call from the property management system; automatic screen pops on matching tenant, owner, or vendor records; AI call recording, transcription, summaries, and call logging; voice broadcast campaigns to tenants; multi-location portfolio support [simplevoip.com/crm-connect/]. Several help-center articles document the AppFolio connector specifically.
- Trust or fiduciary workflow support, when relevant: N-A. The product does not touch client funds, deposits, or trust accounting, and nothing in the reviewed materials suggests otherwise.
- Operational role and dependencies: This is the phone layer. A property manager still needs a property management system for every record the business runs on, and would use this API to keep phone provisioning and call routing aligned with that system and to feed call history into reporting.

## Coverage classification (fixed before inspection)

Recorded before any documentation or endpoint was inspected. The methodology publishes defaults for five software categories, none of which is telephony, so a classification was constructed and the deviation recorded in advance. It borrows the shape of the workflow/CRM and maintenance/operations defaults: routing objects play the automations-and-triggers role, and staff-provisioning objects play the records role. Change notification is deliberately excluded from the object list so it is graded once in C1.4 and once, for delivery security only, in C2.8.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Accounts and sub-accounts | critical | 3 | present |
| Users and extensions | critical | 3 | present |
| Devices and endpoints | critical | 3 | present |
| Call flows and routing | critical | 3 | present |
| Call detail records | critical | 3 | present, read-only by design |
| Phone numbers | important | 2 | present |
| Voicemail boxes and messages | important | 2 | present |
| Call recordings | important | 2 | present, read-only |
| Time-of-day and holiday schedules | important | 2 | present |
| Ring groups and call queues | important | 2 | partial — groups present, queues absent |
| SMS and messaging | important | 2 | partial — platform listing broken, vendor send endpoint gated |
| Media, greetings, prompts | optional | 1 | present |
| Faxes | optional | 1 | partial — faxboxes present, fax collection not readable |
| Conferences | optional | 1 | present |
| Provision or update a user | critical | 3 | present |
| Assign a device to a user | critical | 3 | present |
| Change call routing | critical | 3 | present |
| Change a time-of-day schedule | important | 2 | present |
| Change ring-group membership | important | 2 | present |
| Send an outbound SMS | important | 2 | partial |
| Update a voicemail box | important | 2 | present |
| Assign a number to a destination | important | 2 | present |
| Toggle call recording | optional | 1 | present |
| Create or modify a conference | optional | 1 | present |
| Disable or delete a user | critical | 3 | present |
| Disable or delete a device | critical | 3 | present |
| Activate or swap a call flow | critical | 3 | present |
| Release or unassign a number | important | 2 | present |
| Delete a voicemail message or recording | important | 2 | partial |
| Suspend or delete a sub-account | important | 2 | present |
| Expire a temporary schedule | optional | 1 | present |

## Functional coverage map

- **Core objects, live-verified by GET on the child account, 2026-09-10.** Returned HTTP 200: accounts and their children and descendants, users, devices, callflows, cdrs, phone_numbers, vmboxes, media, temporal_rules, temporal_rules_sets, groups, conferences, menus, recordings, webhooks, faxboxes, directories, blacklists, notifications. Returned errors: `queues` HTTP 404 (call-queue module not enabled on this cluster), `faxes` HTTP 405 at the collection, `sms` HTTP 500 with machine code `datastore_missing_view`.
- **Primary operational workflows.** Route-level method advertisement observed via CORS preflight, which is non-mutating: collections for users, devices, callflows, vmboxes, media, temporal_rules, groups, conferences, menus, faxboxes, directories, and blacklists advertise `PUT`; item routes for users, devices, callflows, temporal_rules, and vmboxes advertise `PATCH`, `POST`, and `DELETE`; the webhooks collection additionally advertises `PATCH`. The `cdrs`, `phone_numbers`, and `recordings` collections advertise `GET` only, which matches their read-only role.
- **Principal lifecycle changes.** `DELETE` is advertised on user, device, callflow, temporal-rule, and voicemail-box item routes. The user document carries an `enabled` boolean for non-destructive disabling. The vendor's own time-of-day API documents an `enabled` property taking `null`, `true`, or `false` to force a site into standard, always-open, or forced-closed mode.

---

## Category 1: Functional Coverage and Usefulness: 13.1/15

- **C1.1 Object coverage: yes** — weighted coverage = **92%** (27.5 of 30 weight). All five critical objects present with the operations their role requires, live-verified. Deductions: ring groups and queues scored 0.5 because `groups` is fully present with create, update, and delete verbs while `queues` returns HTTP 404 on this cluster; SMS scored 0.5 because the platform `sms` collection returns HTTP 500 `datastore_missing_view` and the vendor's send endpoint requires separate written authorization; faxes scored 0.5 because `faxboxes` is fully present while the `faxes` collection returns HTTP 405. Call detail records were treated as read-appropriate rather than read-only, per the methodology's immutability carve-out for audit records. [Live GET sweep across 21 collections, portal.simplevoip.us:8443/v2, 2026-09-10.]
- **C1.2 Core operational actions: yes** — weighted coverage = **95%** (20 of 21 weight). Documentation-graded, as the operator declined live-data write testing. Create and update paths for users, devices, callflows, voicemail boxes, temporal rules, groups, media, and conferences are documented per-endpoint with worked curl examples and schema tables [docs.2600hz.com/developers/rest/devices-and-users/users; .../call-control/callflows/callflows], and every one of those routes advertised the corresponding verb live. Sending an outbound SMS scored 0.5: the endpoint is documented [Outbound SMS API], but it requires a 10DLC brand and campaign that the vendor sets up, and separate per-account authorization. The authorization requirement is evidenced by the 401 example in the vendor's published Postman collection, which reads, "You have not been authorized to send via this endpoint. Please contact SimpleVoIP support for authorization." The help-center article's own documented error example is different: `{"status":"failed","error":"Invalid sender or recipient number provided."}`.
- **C1.3 Delete or lifecycle actions: partial** — weighted coverage = **81%** (13 of 16 weight). Documentation-graded. Deletion and disabling are available for all three critical lifecycle changes: users, devices, and call flows, so no critical lifecycle action is absent. Two deductions put it in the 0.50–0.84 band. Deleting a voicemail message or a call recording scored 0.0: no delete operation for either is evidenced anywhere in the packet, the `recordings` collection advertised `OPTIONS, GET` only, and the only message route in the reference is a read of the raw audio. Releasing a phone number scored 0.5: it appears only as a documented side effect of enhanced user deletion, never as a direct operation, and the `phone_numbers` collection advertised `GET` only.
- **C1.4 Change notification: yes** — Live query of the system webhook catalogue on this cluster returned 29 hook types, including an `object` hook covering actions `doc_created`, `doc_edited`, and `doc_deleted` across account, callflow, device, user, vmbox, media, fax, faxbox, mailbox_message, and call_recording document types; a `notifications` hook exposing 43 event types including new voicemail, missed call, device registration and de-registration, inbound fax, port request, and new user; a dedicated `cdr` hook; and `channel_create`, `channel_answer`, `channel_bridge`, `channel_hold`, `channel_unhold`, and `channel_destroy`. That covers essentially every critical and important state change in the fixed classification. Efficient incremental polling is independently available and was verified live: `modified_from` narrowed the full user listing to three records, and `created_from` and `created_to` are documented for any collection in Gregorian seconds [.../overview/query-string-filters].

Score math: earned 3.5 of 4 applicable checks; unrounded fraction = 0.875000; category points = 13.1/15; verification coverage = 100% (4 of 4).

**What this means for you:** This is the strongest part of the API by a wide margin. Everything a property manager would want to automate about a phone system is reachable: you can read who has an extension and what phone they are on, change where calls go, adjust office hours, and pull complete call history. Two gaps are worth knowing before you plan work. Call queues are not enabled on this cluster, so queue and agent statistics are not available to you, and the platform's SMS listing endpoint is returning a server error, so text history has to come from the webhook feed rather than a query. A third gap sits on the retention side: nothing in the documentation lets you delete an individual voicemail message or call recording through the API, so a retention policy has to be run by hand. Note also that the vendor's bulk change endpoints are fire-and-forget: a successful response tells you jobs were queued, not that they applied, and no job-status endpoint is documented.

## Category 2: API Design, Reliability, and Operability: 5.8/10

- **C2.1 Modern API conventions: yes** — The platform API is resource-oriented REST over JSON with standard verbs, a version in the path, and a consistent `/v2/accounts/{ACCOUNT_ID}/{resource}/{RESOURCE_ID}` structure [.../overview/api-basics, Basic URI Structure]. Verified live across 21 collections. Disclosed limitation: the vendor's own customer API is RPC-shaped rather than resource-oriented — its bulk endpoints act on no resource identifier and the vendor describes it in its own words as "a REST-like API" [Time of Day Bulk Change API].
- **C2.2 Consistent typing: no** — Core fields are stringly typed and types vary across endpoints. Live-observed on 2026-09-10: in the CDR list view the `timestamp` field is a JSON string, while the single-record view of the same CDR returns `timestamp` as an integer. Also in the list view, `cost`, `rate`, `unix_timestamp`, and `unix_timestamp_micro` are strings while `billing_seconds` and `duration_seconds` are integers in the same record. The vendor's own CDR webhook documentation declares `timestamp` as JSON type `int`, which the list endpoint contradicts [Call Detail Record (CDR) Webhooks, Webhook Payload Structure]. On the customer API, time-of-day rules read back as strings such as `"09:00"` under day-named keys, but are written as integers in seconds past midnight under entirely different key names, so a read cannot be round-tripped into a write [Time of Day Bulk Change API, Rule Objects]. The webhook documentation separately warns that the default `form-data` delivery format results in "integers (like timestamps) being encoded as strings."
- **C2.3 Structured errors: partial** — The platform API is close to exemplary: every failure returned a consistent envelope carrying a populated, stable machine token in `message`, a human-readable string in `data.message`, the HTTP status echoed in `error`, and a `request_id`. Live-observed tokens include `invalid_credentials` (401), `bad_identifier` (404), `not_found` (404), `invalid_method` (405), and `datastore_missing_view` (500), each with the correct HTTP status. Two findings hold it to partial. First, a malformed query filter returned HTTP 200 with `"status": "success"` and an empty data array rather than an error, so a filter typo silently reads as "no matching records." Second, the vendor's own customer API has no structured errors at all: an invalid Bearer token and a missing Authorization header each returned HTTP 401 with a zero-byte body and `Content-Type: text/html`, and an unknown path returned HTTP 404 with an empty body. A nonexistent recording identifier returned HTTP 500 where the vendor's published documentation specifies a 404 "No Recording Found" response.
- **C2.4 Duplicate prevention: no** — Documentation-graded; no write was issued. Neither surface documents idempotency keys, and a search of the developer documentation and the 300-path swagger specification returned zero occurrences of idempotency, If-Match, or ETag parameters. The check expressly carves out operations that are naturally idempotent, so the fact that `POST` and `PATCH` updates set a document to a stated value is not protection, it is exclusion from the requirement. What remains after that carve-out is unprotected: collection-level `PUT` creates produce a duplicate record on retry, `POST /sms/send` sends a second message, and the vendor's bulk endpoints enqueue a fresh batch of jobs on every call, returning a new `enqueued_tasks` count each time. Client-set entity IDs exist but sit behind a system feature flag with no evidence it is enabled here.

- **C2.5 Graceful handling under load: partial** — A 429 response is documented, together with the token-bucket mechanism keyed on client IP and account ID [.../sys-admin/rate-limiting]. What is missing is usable recovery guidance. No `Retry-After` header and no rate-limit response headers were observed on any call. The only numbers published are administrator-configurable defaults, hedged as what "typically" happens and presented on a page written for the platform operator rather than the API consumer, and per-endpoint token costs are themselves tunable. The one live signal the API exposes, a `tokens` object in the response envelope, read `remaining: 0` on authenticated reads that nonetheless succeeded, so an integration cannot pace itself from it. The customer API documents no throttling at all and returned no rate-limit headers.

- **C2.6 Pagination for large collections: yes** — Live-verified. A CDR request with `page_size=5` returned exactly five records plus `start_key`, `next_start_key`, and `page_size`. Requesting the second page with the returned `next_start_key` produced five further records with zero overlapping identifiers and echoed the requested key back as that page's `start_key`. The documentation states that a missing `next_start_key` indicates the last page, gives the ordering default as descending with `ascending=true` available, and states the stability condition, "Assuming no changes are made to the underlying documents, start_key will get you this page of results" [.../overview/api-basics, Pagination].
- **C2.7 Bulk or incremental export: yes** — Live-verified on three independent mechanisms. A single request with `Accept: text/csv` returned 501 CSV rows and 326 KB of call history in one response. `paginate=false` returned the complete user collection unpaginated. `modified_from` narrowed the full user listing to three records, demonstrating working incremental sync. Chunked responses are additionally documented for large datasets, on by default for CDR interaction and ledger endpoints [.../overview/api-basics, Chunked Response].
- **C2.8 Webhook security and delivery reliability: partial** — The platform mechanism alone would earn a yes: payloads can be signed with HMAC-SHA256 through `security_settings.sha256_key`, with the exact construction published as `base64_encode(hmac(SHA256Key, TimestampString + DataJSON))` and a worked example; timestamps are included on all payloads and the documentation states this is to "prevent replay attacks"; `retries` is a first-class field bounded 0 to 4 and defaulting to 2; failing hooks are auto-disabled and surface a `disable_reason`; and a `webhook_attempts` resource records delivery history [.../webhooks/webhooks, Hook Security]. What holds this to partial is that the vendor's own webhooks — the CDR and SMS feeds SimpleVoIP provisions for customers and documents in its help center — are unsigned by the vendor's own admission: "We currently don't support authentication on webhook POST requests. Mention this to your account manager if you would like to see this implemented!" [Call Detail Record (CDR) Webhooks, FAQ]. No retry policy is documented for those either. The vendor ships both a secured mechanism and an unsecured one, and its own support articles route customers to the unsecured one.
- **C2.9 Concurrency and conflict control: partial** — The mechanism exists and was observed live: a single-entity GET returned `ETag: "22-61b6..."` matching a `revision` field in the response envelope, and the API advertises `if-match` in `access-control-allow-headers` and `etag` in `access-control-expose-headers`. What is missing is the documentation half: a targeted first-party search across both 2600Hz domains, plus a scan of the developer documentation and the swagger specification, found no documented conflict semantics, no documented 409 behaviour, and no documented concurrency limits. The capability is discoverable only by inspecting responses.
- **C2.10 Versioning and backward compatibility: partial** — An explicit version identifier is present in the path and documented as the only supported value [.../overview/api-basics], and the running build is reported in every response envelope. One breaking-changes document exists, covering the Kazoo 5.1 to 5.3 transition in field-level detail [.../changelog/kazoo-51-53-breaking-changes]. What is absent is a backward-compatibility policy defining breaking versus non-breaking changes, and any deprecation window or notice commitment. The gap is concrete rather than theoretical: the cluster serving this operator reported version 5.4.7.25 in every response, and no published change record covers 5.4 at all.
- **C2.11 Request traceability: partial** — On the platform API this is a clear strength, verified on every single call including all four deliberate errors: an `x-request-id` response header and a matching `request_id` in the body envelope, documented as "ID of the request; usable for debugging the server-side processing of the request" [.../overview/api-basics, Response Envelope]. On the vendor's own customer API there is no request identifier of any kind — live header capture across successful and failed calls returned only `Date`, `Server`, `X-Powered-By`, and cache headers. A customer reporting a problem on that surface has nothing to quote.
- **C2.12 Service availability and status transparency: yes** — SimpleVoIP publishes a public status page listing named components with current state, a past-incidents section, and 90-day uptime tracking; its incident-history feed contains multiple real prior incidents including regional connectivity events and planned hardware migrations [status.simplevoip.us and /history.atom, retrieved 2026-09-10]. A published SLA commits to "99.99% availability each month of our hosted VoIP platform" with a one-day service credit per whole hour of unavailability below that, and describes the three-datacenter architecture behind it [SimpleVoIP Service Level Agreement]. Disclosed limitation: both the status components and the SLA cover voice, portal, and application services rather than the APIs specifically.

Score math: earned 7.0 of 12 applicable checks (4 yes, 6 partial, 2 no); unrounded fraction = 0.583333; category points = 5.8/10; verification coverage = 100% (12 of 12).

**What this means for you:** The platform API behaves predictably in the ways that matter most for unattended automation. Paging through call history works exactly as documented, you can pull a full dataset as CSV in one request, incremental sync works, and when something fails you get a stable error code and a request ID you can quote. Three things will cost you real engineering time. Field types are not dependable — the same call-record timestamp comes back as text in a list and as a number when you fetch that record on its own, so any code you write has to coerce types defensively rather than trust them. Nothing prevents a duplicate if a create or an SMS send is retried after a timeout, so you have to build your own guard. And the vendor's own layer is materially weaker than the platform underneath it: its failures return empty bodies, its responses carry no request ID, and the call-record webhooks it sets up for customers are unsigned, meaning anyone who learns your endpoint URL can post fabricated call data to it.

## Category 3: Access Control and Safe Automation: 1.3/5

- **C3.1 Read-only credentials: no** — The upstream platform documents both a `crossbar:read_only` scope and a `token_restrictions` mechanism capable of restricting a token to specific HTTP methods and accounts [.../authentication/scope-restrictions; .../authentication/token-restrictions]. Neither is available on SimpleVoIP's cluster: live requests to the token-restrictions route returned HTTP 404 `bad_identifier` at both account and user level, and the scope-restrictions route returned HTTP 404 `not_found`. The single credential issued to this operator carries write access to every route it can reach. The operator states no read-only credential was offered for either surface.
- **C3.2 Scoped credentials: partial** — Coarse scoping exists and was verified: each account in the tree holds its own API key, and the child account exposed a distinct key of its own, so an operator can choose a credential bounded to a lower account rather than the parent. That is the extent of it. The parent credential under test reached the parent account record, its children and descendants listing, the full record set of the child account, and the parent account's own API key value. No restriction by resource, by action, or by role was available, for the reasons cited in C3.1.
- **C3.3 Multiple keys: no** — An account holds exactly one API key; the documented retrieval route returns a single `api_key` value and no route exists to issue an additional credential for the same account [.../authentication/account-api-authentication]. Two integrations against the same account must therefore share one key, which means neither can be revoked without breaking the other. Per-account keys in a parent-child tree are an account-structure artefact, not an integration-credential mechanism.
- **C3.4 Rotation and revocation: partial** — Self-serve rotation is documented for the platform surface, and this corrects an error in the first grading pass of this report. The account reference carries a section headed "Re-create the account's API key," stating that "If you think that your account's API key might be exposed you can create a new one with the api_key endpoint. Issuing a PUT request to this endpoint will generate a new API key for the account and will return the new key in response," gated on an admin token [.../account-actions-and-permissions/accounts]. The route advertised `PUT` live; it was deliberately not executed, since doing so would have invalidated the operator's working credential. Held to partial for two reasons. The customer API Bearer token has no documented rotation or revocation path at all and is reissued by the engineering team through an account manager. And because there is exactly one key per account, rotating is all-or-nothing: it cuts off every integration at once rather than the one you meant to revoke.

- **C3.5 Test and production isolation: N-A** — No sandbox or separate test environment exists for SimpleVoIP customers. Help-center searches for sandbox, test account, trial, and developer account returned no such offering; the 2600Hz documentation sitemap contains no sandbox pages, and its single trial-account page concerns 2600Hz's own hosted trial for testing a different product rather than an environment available to a SimpleVoIP customer. Per the check's own instruction, this is excluded from the math rather than scored zero.

Score math: earned 1.0 of 4 applicable checks (2 partial, 2 no, 1 N-A excluded); unrounded fraction = 0.250000; category points = 1.3/5; verification coverage = 100% (4 of 4).

**What this means for you:** This is the weakest category and the one that should shape how you use the API. You cannot get a read-only key. The credential you hold can change call routing, delete users, and delete devices, so any script, contractor, or AI agent you hand it to has the power to take your phones down, and nothing in the platform will stop it. There is one key per account, so you cannot give a vendor its own revocable credential, and rotating the key to cut off one integration breaks all of them at once. There is no test environment, so anything you build is developed against live phones. The practical mitigations are yours to build: hold the key in a secret store rather than in code, use the child account's key rather than the parent's so the blast radius stops at one account, and put a read-only wrapper of your own in front of anything you do not fully trust.

## Category 4: Documentation and AI-Agent Readiness: 1.9/5

- **C4.1 Complete self-serve reference: partial** — The platform reference is publicly accessible with no login and is genuinely example-rich: 123 developer pages carrying per-endpoint curl request and response examples plus schema tables giving key, description, type, default, and required status. What holds it to partial is that it documents the upstream platform rather than SimpleVoIP's deployment, and nothing first-party tells a SimpleVoIP customer which parts apply to them. Four documented endpoints behaved differently on the live cluster: `queues` returned 404, `sms` returned 500, `about` returned 403, and the documented per-resource schema route returned 404 for the CDR schema. The resource a property manager most needs is the least documented: call detail records have no schema in the live schemas catalogue, no definition in the swagger file, and return 35 fields in the list view versus 71 in the single-record view, with the extra fields described nowhere. On the vendor's own surface, the published Postman collection contains two entries with no method, no URL, and no example — "Fetch Media IDs by account" and "Password Reset" — and its Mobile endpoints reference a `{{provisioning_api_url}}` base variable that the collection never defines, though the host is recoverable by reading it out of the saved example request URLs.
- **C4.2 Reliable machine-consumable integration path: partial** — Three candidate mechanisms exist and none is complete. A Swagger 2.0 specification carrying 300 paths and 783 definitions is present in 2600Hz's repository, but it is not fit for code or tool generation as published: every operation declares only `{"200": {"description": "request succeeded"}}` with no response schema and no error responses, `host` is the placeholder `localhost:8000`, there is no `cdr` definition at all, and it is neither published on nor referenced from the documentation site. 2600Hz's own engineering documentation warns that the generator "would maybe result in generating outdated JSON schema files and Swagger file." The official SDK page is banner-marked as covering a Kazoo version that "is no longer supported," lists "PHP" with no link, and has an empty community section. No MCP server was evidenced. The one genuine strength is a live schemas endpoint, which returned 492 JSON Schemas on this cluster and gives real machine-readable data models — but schemas alone carry no paths or methods, so they cannot generate a client on their own.
- **C4.3 AI-readable documentation: no** — Neither `llms.txt` nor `llms-full.txt` exists on either docs.2600hz.com or simplevoip.com; all four requests returned 404. Probes for `.md` and `.txt` variants of documentation pages returned 404. No downloadable documentation corpus was evidenced. SimpleVoIP's own API documentation consists of Zendesk help-center articles and a client-rendered Postman page, neither structured for reliable retrieval — the Postman page in particular returns only an empty shell to a non-browser client, and its content had to be recovered from a separate JSON endpoint.
- **C4.4 Kept current: partial** — Currency signals exist but are stale and irregular, and the staleness is specific to the API rather than to the vendor's documentation generally. Across all 123 developer pages, none carries a last-modified date later than mid-2025, and the tail reaches back to 2016. The only changelog stops at Kazoo 5.3 while the cluster serving this operator reports 5.4.7.25 in every response, so the running version has no published change record. SimpleVoIP's release notes stop at Sprint 108, released 2 September 2025 — a year before this assessment — even though its help center is otherwise actively maintained, with its newest article created 26 August 2026. Its three API articles were last updated December 2022, August 2024, and July 2025.

Score math: earned 1.5 of 4 applicable checks (3 partial, 1 no); unrounded fraction = 0.375000; category points = 1.9/5; verification coverage = 100% (4 of 4).

**What this means for you:** A developer can build against this, but not quickly and not with an AI coding assistant doing much of the work. The reference is detailed and free to read, which is more than many vendors offer, and pointing a coding tool at the endpoint pages does work. What you will not get is a spec a tool can consume to generate a working client, a maintained SDK in any language, or any AI-oriented documentation format. Budget for reading the reference by hand, and expect to discover by experiment which documented endpoints your particular cluster actually serves. The most consequential gap is that call detail records — the thing you would most want to pull into reporting — are the least documented object in the API, so the field list has to be derived from live responses.

## Category 5: Accessibility and Cost: 11.3/15

- **C5.1 Self-serve API key: partial** — Split evidence across the two surfaces. The platform key is self-serve once a portal login exists: the vendor's engineer states in writing that "to find your Account API key, you may find it in Authentication -> API Key Authentication -> API Key Value," and the operator confirms retrieving it that way. But the prerequisite portal login was not self-serve, taking a project manager and roughly a week to obtain. The customer API key is not self-serve at any stage — the vendor's own published article states, "You will also need an API key provided by the SimpleVoIP Engineering team. These are available upon request. Please reach out to your account manager to initiate this process" [Time of Day Bulk Change API, Prerequisites], and the operator reports that token likewise required a project manager and about a week. Sending SMS requires a further approval step beyond the key, evidenced by the vendor's own documented rejection message directing the caller to contact support for authorization.
- **C5.3 Not commercially gated: yes** — No first-party material conditions API access on a plan tier, and the plans page does not mention API access at all [simplevoip.com/features-and-plans/]. The operator's own record is affirmative rather than merely silent: working credentials for both surfaces were issued against their existing account, with no plan upgrade involved and no charge for API access stated to them. The 10DLC brand and campaign required before sending SMS is carrier-mandated regulatory registration, which this check expressly excludes from counting as commercial gating. Chargeable engineering hours for bespoke webhook customization are custom development work, not a gate on the documented API. Disclosed limitation: SimpleVoIP publishes no pricing for any tier, so this rests on the absence of any evidenced gate plus one operator's live experience rather than on a published entitlement statement.

Score math: earned 1.5 of 2 applicable checks (1 yes, 1 partial); unrounded fraction = 0.750000; category points = 11.3/15; verification coverage = 100% (2 of 2).

**What this means for you:** You can get in, and there is no evidence you have to buy up a tier to do it, but you cannot get in today. Both credentials in this assessment took a named human on the vendor's side and about a week each. Plan API work around a lead time measured in weeks rather than an afternoon, and get the credential requested before you need it. Because pricing is not published at all, confirm in writing with your account manager that API use carries no charge on your contract before you build anything that depends on it.

## Total
- Raw: 33.33 / 50
- Normalized before rounding: 66.67 / 100
- Published numeric score: **67 / 100**
- Letter grade: **D+**
- Evidence tier: Baseline verified
- Overall verification coverage: 100% — 26 of 26 applicable checks verified, no category Unable to verify, gate satisfied
- Partial-result flag: **yes.** Four checks were graded from documentation rather than observation because the operator declined live-data write testing: C1.2, C1.3, C2.4, and the delivery half of C2.8. A controlled write test on a labelled fixture would convert these to observed evidence.

### Independent grading runs and reconciliation

Three independent runs were performed against the same final frozen packet, as the methodology requires for a published number. Runs 2 and 3 were graded by separate evaluators who received the frozen packet, the pre-fixed coverage classification, and the corpus, but never saw this report or any of its marks.

| | Raw / 50 | Normalized | Published | Grade |
|---|---|---|---|---|
| Run 1 | 32.29 | 64.58 | 65 | D |
| Run 2 | 32.71 | 65.42 | 65 | D |
| Run 3 | 32.50 | 65.00 | 65 | D |
| **Reconciled** | **33.33** | **66.67** | **67** | **D+** |

All three runs independently produced 65. The published figure is nonetheless 67, because the methodology directs that disagreements be resolved against the final evidence rather than averaged. Resolution moved four marks off run 1's originals, and the net effect happens to be upward.

The three runs agreed outright on 17 of 27 checks, including every check in Documentation and AI-Agent Readiness and every mark of `no`.

**Disagreements resolved against the evidence, changing run 1's original mark:**

- **C1.3, yes to partial.** Both independent runs scored deletion of a voicemail message or a call recording at zero. Re-checking the packet confirms they were right and run 1 was not: run 1 cited a voicemail reference page that was never actually retrieved, and no delete operation for either object appears anywhere in the frozen corpus. Weighted lifecycle coverage falls from 94% to 81%, into the partial band. Cost: 1.9 points.
- **C2.4, partial to no.** Both independent runs read the check's carve-out correctly and run 1 did not. Because the check excludes naturally idempotent operations from the requirement, the fact that updates are idempotent is not protection covering a subset, it is exclusion from scope. What remains, creates and SMS sends, has no protection at all. Cost: 0.4 points.
- **C2.5, yes to partial.** Both independent runs judged that administrator-configurable defaults, hedged as what "typically" happens on a page addressed to the platform operator, are not client recovery guidance. Combined with no `Retry-After` header, no rate-limit headers, and a live token counter that reads zero while requests succeed, partial is better supported. Cost: 0.4 points.
- **C5.3, partial to yes.** Both independent runs marked this yes. Run 1's first reason for partial does not survive the check's own text, which expressly excludes legally required regulatory verification from counting as commercial gating; the 10DLC registration is exactly that. The second reason, chargeable webhook customization, is bespoke development rather than a gate on the documented API. Gain: 3.75 points.

**Two factual corrections the independent runs surfaced, neither of which changes a mark:**

- Run 1 stated that API key rotation is not documented. It is. The account reference documents re-creating the key by PUT, with the stated purpose of replacing a key you believe is exposed. C3.4 remains partial on other grounds, but the citation has been corrected.
- Run 1 attributed the SMS authorization message to the help-center article. It appears in the vendor's published Postman collection; the article documents a different error example. The attribution has been corrected.

**Unresolved disagreements and their score effect.** Six splits remain where a defensible evaluator could differ. Each is shown as a single change from the reconciled position:

| Check | Reconciled | Dissent | Published if adopted |
|---|---|---|---|
| C1.4 Change notification | yes | partial (run 3) | 63, grade D |
| C3.2 Scoped credentials | partial | no (run 2) | 65, grade D |
| C2.1 Modern conventions | yes | partial (run 3) | 66, grade D |
| C2.6 Pagination | yes | partial (run 3) | 66, grade D |
| C3.4 Rotation | partial | yes (run 3) | 68, grade D+ |
| C3.1 Read-only credentials | no | yes (run 3) | 69, grade D+ |

The most consequential is C1.4. Run 3 computed push coverage at 82.4% by excluding schedules, groups, and phone numbers from the event catalogue, which would drop the score a full grade band. The reconciled position keeps `yes` because the documented event type list includes an `all` value that on its face subscribes to every document change, and because incremental polling is independently documented and was live-verified. That reading is contestable and a reproducing evaluator should test it first. C3.1 is the second: run 3 credited the documented read-only scope, while runs 1 and 2 weighted the live evidence that the mechanism returns 404 on this vendor's cluster and the operator was never offered one.

No run marked any check `unverified`, so the verification-coverage gate is satisfied under all three and under the reconciliation.

## Bottom line for a property manager

You can build real automation on this today, and the useful half of it is not SimpleVoIP's engineering — it is the 2600Hz platform underneath, which SimpleVoIP operates and points you at. Through it you can read your full call history, page and export it reliably, keep extensions and phones in step with staffing, change call routing and office hours in code, and subscribe to webhooks covering essentially every change the phone system makes. SimpleVoIP's own thin layer on top adds bulk hours changes across many sites and outbound texting, but is noticeably rougher: empty error bodies, no request identifiers, and call-record webhooks the vendor confirms are unauthenticated, so treat anything arriving on that endpoint as unverified input.

The two things that should govern your plans are access control and lead time. There is no read-only key, no way to scope a credential to a single action, one key per account, and no test environment, which together mean any credential you issue can delete users and re-route calls against live phones. Keep the key in a secret store, prefer the lower account's key over the parent's, and put your own read-only wrapper in front of anything you would not trust with the phone system. Separately, both credentials in this assessment took a project manager and about a week, so request access well before you need it and confirm in writing that it carries no charge, since no pricing is published.

This is a phone system with a usable API, not a system of record. It does not touch tenant ledgers, deposits, or trust accounting, and nothing in its documentation suggests otherwise. Its property-management value is as a data source and a control surface alongside your property management system — call history for response-time reporting and staff accountability, and routing changes driven by your own calendar or staffing data rather than by hand. The score of 67 reflects excellent functional reach dragged down hard by weak credential controls, thin machine-readable documentation, and API documentation that has gone a year or more without an update while the platform it describes has moved on a full minor version. Three independent graders working from the same frozen evidence each arrived at 65 before reconciliation, so treat the grade band rather than the exact number as the finding.
