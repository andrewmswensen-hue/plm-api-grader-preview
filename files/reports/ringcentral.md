# API Report Card: RingCentral RingEX Platform API

## Run metadata
- Methodology version: 1.1
- Evaluating model: claude-opus-4-8
- Date run: 2026-09-01
- Provisional evidence-packet version or ID: RC-2026-09-01-prov1
- Final evidence-packet version or ID: RC-2026-09-01-final1
- Independent runs (step 12): 3 (2026-09-01), reconciled — 93 / 93 / 93; 25 of 27 checks unanimous; only C2.4 and C2.9 split, both within Category 2 and offsetting (see Total).
- Evidence-discovery mode: tool-enabled discovery (first-party docs + live production API)
- Evidence tier: Baseline verified
- Live-write method and safety: none — writes documentation-graded (credential is read-only; RingCentral consequential writes send real communications and are excluded by the controlled-live protocol; no sandbox credential supplied)
- Minimum live-test battery: read-path steps 1–5 complete; step 6 (write) documentation-graded; step 7 (idempotency) N-A (no idempotency documented); step 8 (webhook delivery) documentation-graded (no operator-controlled endpoint)
- Live tests performed: authenticate (JWT bearer), read+paginate extensions, date-filtered call-log query, deliberate 404 error, rate-limit/traceability header capture
- Live tests not possible: create/update, idempotent-retry, live webhook delivery
- Documentation-graded checks (baseline verified): C1.2, C1.3, C2.4, C2.8

## Final evidence packet manifest
- Live (observed, Production): `POST /restapi/oauth/token`; `GET /restapi/v1.0/account/~`; `…/account/~/extension`; `…/extension/~/call-log?dateFrom…dateTo`; `…/extension/999999999999` (deliberate 404). Raw responses saved under `evidence/ringcentral-2026-09-01/live/`.
- https://developers.ringcentral.com/guide/basics/errors
- https://developers.ringcentral.com/guide/basics/rate-limits
- https://developers.ringcentral.com/guide/authentication
- https://developers.ringcentral.com/guide/basics/permissions
- https://developers.ringcentral.com/guide/notifications/webhooks/creating-webhooks
- https://developers.ringcentral.com/guide/notifications/webhooks/troubleshooting
- https://developers.ringcentral.com/guide/voice/call-log/sync
- https://developers.ringcentral.com/guide/messaging/message-store/message-sync
- https://developers.ringcentral.com/api-reference/Call-Log/syncAccountCallLog
- https://developers.ringcentral.com/guide/basics/changelog
- https://developers.ringcentral.com/guide/ai (AI API deprecation notice)
- https://developers.ringcentral.com/guide/voice/call-routing/user-call-handling/migration-guide
- https://developers.ringcentral.com/guide/sdks
- https://netstorage.ringcentral.com/dpw/api-reference/specs/rc-platform.yml (OpenAPI 3.0.x spec; frozen copy `evidence/ringcentral-2026-09-01/packet/rc-platform-openapi.yml`)
- https://developers.ringcentral.com/guide/getting-started and https://developers.ringcentral.com/sign-up
- https://developers.ringcentral.com/guide/basics/sandbox
- https://developers.ringcentral.com/guide/getting-started/create-credential
- https://support.ringcentral.com/article-v2/Accessing-API-credentials-in-the-RingCentral-Developers-Portal.html
- https://status.ringcentral.com

## Evidence-amendment log
- C2.7: added Call Log Sync / Message Store Sync (FSync/ISync + syncToken) — upgraded from live `dateFrom` filtering to documented dedicated incremental sync.
- C3.4: added Developer Console "Credentials" management + `POST /restapi/oauth/revoke` — confirmed self-serve rotation/revocation.
- C2.12: rendered `status.ringcentral.com` (client-side SPA) in a browser — confirmed component status, uptime history, and incident-update sections.
- C4.4: rendered the changelog — confirmed core RingEX changelog latest entry is v.1.0.51 (Apr 2022); offset by more-recent deprecation/migration notices.

## API eligibility
- Qualifying API: yes
- API operator: RingCentral, Inc. [live: `platform.ringcentral.com/restapi/v1.0`; developers.ringcentral.com]
- Access or credential issuer: RingCentral Developer Console — self-serve app registration + auth credential generation [developers.ringcentral.com/guide/getting-started/create-credential; live: operator-issued JWT credential authenticated successfully]
- Eligibility basis: A programmatic REST interface (RingEX Platform API) exposes RingCentral's own communications functions (account, extensions, call log, messages, telephony, events). Verified live by authenticating and reading production resources.

## Context
- Software category: Other — cloud business communications / UCaaS (an adjacent operating tool for a property manager: phone, SMS, fax, messaging, call logging, and event notifications).
- What the API is for and its core objects and workflows: The RingEX Platform API lets software read and act on a company's RingCentral communications. Core objects: account, extensions/users, call log (call records), message store (SMS/MMS/voicemail/fax), phone numbers, presence, call recordings, and event subscriptions. Core workflows: read account/directory/call-log/messages; send SMS/fax; place and control calls (RingOut / Call Control); and subscribe to real-time events by webhook.

## Provider and property-management fit
- What this product is: A cloud phone, messaging, and meetings platform for businesses, with a developer API for its communications functions. [developers.ringcentral.com]
- Bank status, when relevant: N-A
- Who provides any bank account or regulated banking service: N-A
- What the customer actually receives: A software/communications-service relationship — telephony, SMS, fax, messaging, and video, plus programmatic access to them. No funds are held or moved. [developers.ringcentral.com/guide]
- Property-management fit: general-purpose. The API exposes generic communications objects; no dedicated property-management offering or PM-specific API workflows are documented. [developers.ringcentral.com/guide — guide sections are Voice, SMS/Fax, Team Messaging, Video, Webinar, Analytics, AI, Accounts/Users]
- Documented PM-specific workflows: none found.
- Trust or fiduciary workflow support, when relevant: N-A (no fund storage or movement).
- Operational role and dependencies: Provides the communications layer a PM can build on (call logging, SMS reminders, click-to-call, screen-pop, notifications). A PM would still need a PMS, accounting, and maintenance systems separately.

## Coverage classification (fixed before inspection)
Category is "Other (communications/UCaaS)"; classification defined for a PM building on a communications API, before inspecting the API.

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Extensions / users (directory) | critical | 3 | Present (read + EditExtensions) |
| Call log (call records) | critical | 3 | Present (read; records immutable → write N-A) |
| Message store (SMS/MMS/voicemail/fax) | critical | 3 | Present (read + status update + delete) |
| Account | important | 2 | Present (read + edit) |
| Phone numbers | important | 2 | Present (read + provisioning) |
| Call recordings | important | 2 | Present (read/download; content immutable) |
| Event subscriptions (webhooks) | important | 2 | Present (full CRUD) |
| Presence | optional | 1 | Present (read + edit) |
| Workflow: read core records | critical | 3 | Present (live-verified) |
| Workflow: send SMS/MMS | critical | 3 | Present (SMS scope; documentation-graded) |
| Workflow: place/control call (RingOut/Call Control) | important | 2 | Present (documentation-graded) |
| Workflow: subscribe to events | important | 2 | Present (documentation-graded) |
| Workflow: send fax | optional | 1 | Present (documentation-graded) |

## Functional coverage map
- Core objects: account (present, read/edit), extensions (present, read/edit — live), call log (present, read — live), message store (present, read/write/delete), phone numbers (present), recordings (present, read), subscriptions (present, CRUD), presence (present, read/edit). No critical object absent.
- Primary operational workflows: read core records (live-verified); send SMS/fax; place/control calls (RingOut, Call Control); manage event subscriptions.
- Principal lifecycle changes: message send / read-status / delete; subscription create/renew/delete; call lifecycle via Call Control (answer/hold/transfer/hangup) and RingOut cancel; presence update; extension update.

## Category 1: Functional Coverage and Usefulness: 15.0/15
- C1.1 Object coverage: yes — weighted coverage ≈ 100% (all classified objects present with role-appropriate operations; no critical object absent). [live: account, extension, call-log reads; docs: message-store, recordings, subscriptions, presence]
- C1.2 Core operational actions: yes (documentation-graded) — weighted coverage ≈ 100%; consequential write workflows exist: send SMS [guide/messaging/sms], RingOut/Call Control [guide/voice], create subscription [guide/notifications], EditExtensions [guide/basics/permissions]. No critical write workflow absent. Flagged: writes not live-tested (read-only credential).
- C1.3 Delete or lifecycle actions: yes (documentation-graded) — weighted coverage ≈ 90%; message delete/status, subscription delete/renew, Call Control transitions, RingOut cancel, presence update all documented. [guide/notifications; guide/voice; guide/basics/permissions]
- C1.4 Change notification: yes — Subscription API + webhooks cover the critical/important state changes (incoming call/SMS/voicemail/fax, message-store, presence, telephony session), and documented incremental sync (Call Log Sync / Message Store Sync, syncToken) plus `dateFrom` filtering (live-verified) detect changes by polling. [guide/notifications; guide/voice/call-log/sync; live 03-calllog-filtered]
Score math: earned 4 of 4 applicable checks; unrounded fraction = 1.00; category points = 15.0/15; verification coverage = 100%
What this means for you: You can pull essentially all of your RingCentral communications data (calls, texts, voicemail, directory) and act on it (send texts, place/control calls) programmatically, and get real-time events. The write actions are well-documented but were not exercised live here because the supplied key is read-only.

## Category 2: API Design, Reliability, and Operability: 7.9/10
- C2.1 Modern API conventions: yes — resource-oriented REST/JSON over HTTPS with standard verbs. [live JSON responses at /restapi/v1.0/…; api-reference]
- C2.2 Consistent typing: yes — OpenAPI-specified schemas; live reads were type-consistent (integer paging fields, string ids, ISO timestamps). [rc-platform.yml; live 02a/03]
- C2.3 Structured errors: yes — structured body with stable machine code, message, and `errors[]`/`parameterName`; docs say "rely on the `errorCode`". Live 404 = `CMN-102`. [guide/basics/errors; live 04-error-404]
- C2.4 Duplicate prevention: no (documentation-graded) — no idempotency keys and no natural idempotency for consequential writes (SMS/fax/RingOut); the only related signal, `CMN-304 "Duplicate concurrent request"`, rejects a duplicate that is still in flight, not a sequential retry after completion. [guide/basics/errors; rc-platform-openapi.yml] (Reconciled 2026-09-01: 3-run majority + evidence; run 1 initially had partial.)
- C2.5 Graceful handling under load: yes — documented 429 + `Retry-After` + named `X-Rate-Limit-Group/Limit/Remaining/Window`. Live headers observed (Limit 50, Window 60, Group "light"). [guide/basics/rate-limits; live 05-account.headers]
- C2.6 Pagination for large collections: yes — `page`/`perPage`, a `paging` object with `totalElements`/`totalPages`, and `navigation.nextPage`. Live-traversed pages 1→2 of 34 records. [live 02a/02b]
- C2.7 Bulk or incremental export: yes — dedicated Call Log Sync and Message Store Sync APIs (FSync/ISync + `syncToken`) return only changes since last sync, plus `dateFrom`/`dateTo` incremental filtering (live-verified). [guide/voice/call-log/sync; guide/messaging/message-store/message-sync; api-reference/Call-Log/syncAccountCallLog; live 03]
- C2.8 Webhook security and delivery reliability: partial (documentation-graded) — a `Validation-Token` handshake verifies the subscription endpoint and a developer-set verification token can accompany deliveries, and failed deliveries are retried then the subscription is suspended/blacklisted; but verification is a shared token (not HMAC) and no consumer replay/de-duplication guidance is provided. [guide/notifications/webhooks/creating-webhooks; …/troubleshooting]
- C2.9 Concurrency and conflict control: partial — the OpenAPI spec declares `409 Conflict` responses on ~27 write operations (Call Control / telephony and natural-key "already exists"), i.e., documented conflict semantics; but there is no optimistic concurrency (no ETag/If-Match or version fields) on core resources. [rc-platform-openapi.yml; guide/basics/errors] (Reconciled 2026-09-01: both blind graders found the spec 409s that run 1 missed by reading only the errors page; upgraded no→partial.)
- C2.10 Versioning and backward compatibility: partial — explicit path version (`/restapi/v1.0`) and breaking-change labeling (⚠️) plus deprecation notices and migration guides, but no formal backward-compatibility policy with defined deprecation windows. [guide/basics/changelog; guide/ai; user-call-handling/migration-guide]
- C2.11 Request traceability: yes — every response carries a documented `RCRequestId` for support. Live-observed on both a success and the 404. [live 05-account.headers; 04-error-404.headers]
- C2.12 Service availability and status transparency: yes — public status page with per-component status by region, "Core Services Uptime History," and incident status updates. [status.ringcentral.com, rendered 2026-09-01]
Score math: earned 9.5 of 12 applicable checks; unrounded fraction = 0.7917; category points = 7.9/10; verification coverage = 100%
What this means for you: The API is predictable and production-grade — clean REST, structured errors, clear rate-limit and request-id headers, real pagination, and proper incremental sync. The gaps that matter for money/comms automation: no idempotency keys (guard your own retries of SMS/calls) and no optimistic-concurrency control (the API does return 409 on conflicting writes, but there is no ETag/If-Match to prevent lost updates).

## Category 3: Access Control and Safe Automation: 5.0/5
- C3.1 Read-only credentials: yes — read-only scopes are selectable; the supplied key carried exactly `ReadMessages ReadAccounts ReadCallLog`. [guide/basics/permissions; live 00-token scope]
- C3.2 Scoped credentials: yes — fine-grained action scopes (e.g., ReadCallLog, SMS, CallControl, RingOut, Faxes, EditExtensions), and a JWT credential can be restricted to a specific app. [guide/basics/permissions; getting-started/create-credential]
- C3.3 Multiple keys: yes — multiple apps and multiple JWT credentials can be created in the Developer Console. [guide/getting-started/create-credential]
- C3.4 Rotation and revocation: yes — credentials are created/deleted self-serve in the Console "Credentials" area, credentials can be revoked by owner/admin, and access tokens can be revoked via `POST /restapi/oauth/revoke` (RFC-7009). [support.ringcentral.com Accessing-API-credentials; guide/authentication]
- C3.5 Test and production isolation: yes — a separate sandbox environment (`platform.devtest.ringcentral.com`) with its own accounts, credentials, and isolated data, distinct from production; "Developer Sandbox" is a separately monitored component on the status page. [guide/basics/sandbox; status.ringcentral.com]
Score math: earned 5 of 5 applicable checks; unrounded fraction = 1.00; category points = 5.0/5; verification coverage = 100%
What this means for you: This is a safe platform to hand to an app or AI agent — you can issue a read-only, narrowly scoped key (as done here), run separate keys per integration, test in a sandbox, and revoke instantly.

## Category 4: Documentation and AI-Agent Readiness: 3.8/5
- C4.1 Complete self-serve reference: yes — a complete, public API reference with authentication guides, endpoint definitions, parameters, and worked examples; a developer can build without reverse-engineering. [developers.ringcentral.com/api-reference; /guide]
- C4.2 Reliable machine-consumable integration path: yes — a published OpenAPI 3.0.x specification (the `rc-platform` spec; the SDK page also historically references a Swagger 2.0 spec) plus officially maintained SDKs (.NET, Java, JavaScript, PHP, Python, Ruby, Swift, WebRTC). [rc-platform-openapi.yml, inspected; guide/sdks]
- C4.3 AI-readable documentation: partial — no `llms.txt`/`llms-full.txt` (404), but the full developer guide is published as a downloadable first-party Markdown corpus (github.com/ringcentral/ringcentral-api-docs) alongside the OpenAPI spec; no resource is purpose-structured for AI retrieval. [llms.txt 404; github.com/ringcentral/ringcentral-api-docs]
- C4.4 Kept current: partial — the core RingEX API changelog's latest entry is v.1.0.51 (Apr 2022, page "Last updated 2024-02-16"), which is stale; currency is carried instead by recent, scattered deprecation notices and migration guides and by actively updated reference pages. [guide/basics/changelog; guide/ai; user-call-handling/migration-guide]
Score math: earned 3.0 of 4 applicable checks; unrounded fraction = 0.75; category points = 3.8/5; verification coverage = 100%
What this means for you: Documentation is strong and build-ready, with a spec and mature SDKs in every common language. The weak spots are AI-specific retrieval (no llms.txt) and a stale central changelog, so confirm current behavior against the live reference rather than the changelog.

## Category 5: Accessibility and Cost: 15.0/15
- C5.1 Self-serve API key: yes — a free developer account, self-serve app registration, and self-serve auth-credential generation in the Console; the operator's own key was created this way and worked in production. Public app-gallery distribution requires a graduation review, but an operator's own (private) app and credentials are self-serve. [guide/getting-started; sign-up; live auth]
- C5.3 Not commercially gated: yes — the core RingEX API is included with standard accounts (no premium-tier paywall for API access) and free to develop/test; the operator's standard-account key reached production. Some adjacent products (RingCX contact center, RingSense AI, high-volume A2P SMS) are separately entitled, and A2P registration is a carrier/regulatory requirement, not commercial gating. [guide/getting-started; live auth on production]
Score math: earned 2 of 2 applicable checks; unrounded fraction = 1.00; category points = 15.0/15; verification coverage = 100%
What this means for you: You can get in the door today at no extra cost — free developer account, self-issued keys, sandbox included, and API access bundled with a normal RingCentral subscription.

## Total
- Raw: 46.67 / 50
- Normalized before rounding: 93.33 / 100
- Published numeric score: 93 / 100
- Letter grade: A
- Evidence tier: Baseline verified
- Overall verification coverage: 100% (gate: no category Unable to verify; overall ≥ 80%) — passed
- Partial-result flag: no. To reach "Fully verified," run write-path checks (C1.2, C1.3, C2.4, C2.8) in the RingCentral sandbox or under the controlled live-data protocol.
- Evaluator disagreements: 2 of 27 checks split across the 3 independent runs — C2.4 (run 1 partial vs runs B/C no) and C2.9 (run 1 no vs runs B/C partial). Both are within Category 2 and offset exactly, so the category and total are identical (93) under either resolution. Resolved against the evidence to C2.4 = no and C2.9 = partial. No unresolved disagreements.

## Bottom line for a property manager
RingCentral's API is excellent to build on: modern REST with an OpenAPI spec and SDKs in every common language, granular read-only/scoped keys, a real sandbox, structured errors, rate-limit and request-id headers, proper pagination and incremental sync, and self-serve free access. For a property manager, this is the communications layer — you can log every tenant/owner/vendor call and text, send SMS reminders, build click-to-call and screen-pop, and get real-time call/SMS webhooks. It is not a PMS, accounting, or trust-accounting system, and it holds no funds; property management is not a documented use case, only a general fit. The main engineering cautions are the lack of idempotency keys and optimistic-concurrency/409 conflict control (so protect your own retries of any money- or message-sending actions) and a stale central changelog (verify against the live reference). This run is Baseline verified: read paths were tested live on your production account with a read-only key, while write paths (send/create/update, idempotency, webhook delivery) are graded from RingCentral's documentation — supply a sandbox key to lift those to Fully verified.
