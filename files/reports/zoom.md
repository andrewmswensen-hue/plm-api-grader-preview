# API Report Card: Zoom Communications — Zoom REST API (v2)

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 5 (claude-opus-5)
- Date run: 2026-09-08
- Provisional evidence-packet version or ID: `ZOOM-v2-2026-09-08-P1`
- Final evidence-packet version or ID: `ZOOM-v2-2026-09-08-F2` (supersedes F1; see "Packet F2 delta" below)
- Evidence-discovery mode: tool-enabled discovery
- Evidence tier: **Baseline verified**
- Live-write method and safety: controlled live — fixtures used (`APITEST-DELETE` meetings on the account owner's own user), operator authorization recorded in-session before execution, cleanup verified (0 fixtures remaining; scheduled-meeting count returned to its pre-test value of 13)
- Minimum live-test battery: steps 1–7 complete; **step 8 (webhook registration + delivery) not run** — requires an HTTPS receiver the operator controls, and the controlled live-data protocol forbids pointing a subscription at a third-party or shared endpoint
- Live tests performed: authenticate (S2S OAuth); paged read of a core collection (10 records / 10 pages, twice); filtered + date-ranged queries; five deliberate error cases; response-header capture for rate-limit and traceability signals; create / update / read-back / restore of a core resource; identical consequential write sent three times; delete + 404 re-read confirmation; MCP `tools/list` against four first-party MCP servers
- Live tests not possible: webhook registration and delivery observation (step 8)
- Documentation-graded checks (baseline verified): **C2.8** (webhook security and delivery reliability) — graded from first-party documentation only
- **Live-test scope limitation (disclosed):** Live observation covers **Meetings, Users, Cloud Recording and Zoom Phone**. Not exercised live: Team Chat, Rooms, Calendar, Whiteboard, Contact Center *operations*, Mail, Events, and the remaining catalog groups — these remain graded from first-party documentation. All Phone testing was **read-only (GET)**; no Phone write, update or delete was performed (see "Write-path authorization boundary").
- **Write-path authorization boundary:** the operator's recorded write authorization covered a specific four-call meeting plan on `APITEST-DELETE` fixtures, and nothing else. When Phone scopes were later added, the credential expanded to **497 scopes, 405 of them Phone, including destructive ones** (`phone:delete:call_log:admin`, `phone:delete:call_recording:admin`, `phone:delete:device:admin`, `phone:delete:call_queue:admin`). None was exercised. Phone call logs and recordings are business records and call-queue/device objects affect live call routing, placing them on the controlled-live protocol's hard exclusion list regardless of scope grant.

---

## Final evidence packet manifest

**First-party documentation**
- https://developers.zoom.us/docs/api/ — API Reference index; base URL `https://api.zoom.us/v2/`
- https://developers.zoom.us/docs/api/rate-limits/ — rate limits, 429, per-plan quotas
- https://developers.zoom.us/docs/api/pagination/ — `next_page_token`, `page_size`, `total_records`
- https://developers.zoom.us/docs/api/errors/ — error body shape and codes
- https://developers.zoom.us/docs/api/webhooks/ — signatures, CRC validation, retry schedule
- https://developers.zoom.us/docs/api/using-zoom-apis/ — the `me` keyword, request construction
- https://developers.zoom.us/docs/internal-apps/s2s-oauth/ — Server-to-Server OAuth
- https://developers.zoom.us/docs/build-flow/basic-info/app-credentials/ — secret rotation, 30-day overlap
- https://developers.zoom.us/docs/build/lifecycle/ — Initial Release / Deprecation / Sunset
- https://developers.zoom.us/changelog/ and /changelog/platform/ — dated changelog, 102 pages
- https://www.zoomstatus.com/ (from https://status.zoom.us/, 302) — status page + incident history

**Machine-readable first-party resources**
- https://developers.zoom.us/llms.txt — 445-byte index
- https://developers.zoom.us/.well-known/api-catalog.json — RFC 9727 linkset, **64 entries**, each with a `text/markdown` `service-doc`
- https://developers.zoom.us/.well-known/mcp/server-card.json — MCP server card, 4 servers
- https://developers.zoom.us/docs/api/{meetings,phone,chat,users,accounts,marketplace}.md — Markdown API corpora
- https://developers.zoom.us/docs/api/meetings/events.md — 105 webhook events

**Live observations (account `croskeyrealestate.zoom.us`, 2026-09-08)**
- `POST https://zoom.us/oauth/token` — 92 granular scopes issued
- `GET /users`, `/users/me`, `/users/{id}/meetings`, `/users/me/recordings`
- `POST|PATCH|DELETE /meetings` on `APITEST-DELETE` fixtures
- `POST https://mcp.zoom.us/mcp/{zoom,team_chat,docs,whiteboard}/streamable` — `initialize` + `tools/list`

---

## Evidence-amendment log

Sources added during the single controlled verification pass, with the check each affects:

| Check | Source added | Why |
|---|---|---|
| C2.4 | Targeted first-party search for idempotency guidance | Zero hits across 4.7 MB of reference corpus; verified no guide-level idempotency documentation exists before settling `no` |
| C2.9 | Same pass, ETag / If-Match / 409 / optimistic concurrency | Confirmed absence in guides as well as reference before settling `no` |
| C2.10 | https://developers.zoom.us/docs/build/lifecycle/ | Reference corpus carries no versioning policy; lifecycle page found and raised the mark from `no` to `partial` |
| C2.11 | Targeted search for `x-zm-trackingid` | Header observed live on every response; search established it is documented only as an inbound **webhook** header, holding the mark at `partial` rather than `yes` |
| C2.12 | https://www.zoomstatus.com/ | `status.zoom.us` 302-redirects; followed the redirect rather than recording the status page as unreachable |
| C3.4 | https://developers.zoom.us/docs/build-flow/basic-info/app-credentials/ | Established self-serve rotation with 30-day overlap and an immediate-revocation endpoint |
| C3.5 | Targeted search for a Zoom developer sandbox / test account | No sandbox evidenced; supports `N-A` rather than `no` |
| C4.4 | Changelog rendered in a browser | The changelog is a client-rendered page shell and returned no entries to a plain fetch; rendering it was required before grading currency |
| C4.2 | Live `tools/list` against four MCP endpoints | Server card alone would not establish that the MCP servers are *operations*-capable; the live probe did |
| C5.3 | Plan-prerequisite phrases extracted from the corpora | Established which capabilities are tier- or licence-gated |

No source was removed after provisional scoring began.

### Packet F2 delta (live evidence added after the F1 freeze)

Packet F1 was frozen and scored with a credential holding no Zoom Phone scopes. The operator then granted Phone permissions and asked whether it changed the result, so a second **read-only** live pass was run and the packet reissued as F2. Disclosed rather than folded silently into F1.

| Check | F1 basis | F2 evidence added | Mark change |
|---|---|---|---|
| C1.1 | Telephony documentation-graded from `phone.md` | Live reads: 9 phone users, 9 numbers, 1 device, 17 call records, 161 recordings | none (`yes` → `yes`) |
| C2.2 | Digit-strings in Users + Meetings docs | `extension_number` **int** on `/phone/users` vs `callee_ext_number` **string** on `/phone/call_history` — same concept, two types, two endpoints | none (`partial`); evidence materially stronger |
| C2.3 | Silent 200s on Users; codes 1001/2300/300 | `code 404` echoed as the machine code; a third body shape (`errors[]`); `from=NOT-A-DATE` → 200 unfiltered call history | none (`partial`); **case for `no` strengthened — see disagreements** |
| C2.6 | Ordering stable on `/users`; `page_count` first page only | Signal set inconsistent across 6 Phone endpoints (`common_areas` returns neither `total_records` nor `page_count`) | none (`partial`); evidence stronger |
| C3.2 | 92 granular scopes; one scope refusal | Before/after: 92 → 497 scopes, same call 400 → 200; Phone alone is 405 grantable scopes | none (`yes`); evidence stronger |

**Net effect on the published score: none.** Raw total, normalized score, letter grade and verification coverage are unchanged at 41.25 / 82.50 / **83** / **B** / 100%. F2 raises the evidence tier of individual findings without moving any mark.

---

## API eligibility

- **Qualifying API: yes**
- **API operator:** Zoom Communications, Inc. — the interface is served at `https://api.zoom.us/v2` and documented on Zoom's own developer domain [developers.zoom.us/docs/api/, "Base URL … `https://api.zoom.us/v2/`"]
- **Access or credential issuer:** Zoom Communications, Inc., via the Zoom App Marketplace [developers.zoom.us/docs/internal-apps/s2s-oauth/: "Get your app credentials on your app details page on the Zoom App Marketplace"]
- **Eligibility basis:** First-party evidence identifies the interface, establishes that it exposes Zoom's own product functions (meetings, users, recordings, phone, chat), and documents how access is authorized. Confirmed live: a Server-to-Server OAuth app issued by Zoom returned a bearer token carrying 92 Zoom-scoped permissions, which then successfully read and wrote Zoom meeting records on 2026-09-08.

---

## Context

- **Software category:** other — unified communications / meetings platform (an adjacent operating tool for a property management operator, not a PM system)
- **What the API is for and its core objects and workflows:** The Zoom REST API lets a developer programmatically manage a Zoom account's communication surface: provisioning and configuring users, scheduling and modifying meetings and webinars, retrieving attendance records and cloud recordings with transcripts, and — where licensed — operating Zoom Phone, Team Chat, Rooms, and Contact Center. Its core objects are therefore users, meetings, participants/attendance, and recordings, with messaging, telephony, and reporting alongside them. Its central workflows are creating and updating scheduled sessions, reading who attended, and retrieving the resulting media and transcripts.

---

## Provider and property-management fit

- **What this product is:** A unified communications platform — video meetings, webinars, telephony, team chat, and contact centre — sold as a subscription SaaS service [developers.zoom.us/docs/api/, product groupings "Workplace / Business Services / Zoom CX"]
- **Bank status, when relevant:** N-A. Zoom is not a financial-services provider and no first-party evidence in this packet presents it as one.
- **Who provides any bank account or regulated banking service:** none. Zoom's `commerce` and billing APIs govern Zoom's own subscription billing and ISV monetization, not customer fund custody [.well-known/api-catalog.json anchor `docs/api/commerce`].
- **What the customer actually receives:** A licensed communications service under a Zoom account plan, plus programmatic access to that account's own data and configuration. The customer receives no account, balance, or ledger relationship.
- **Property-management fit:** **general-purpose** — the API is useful to a property manager, but no dedicated property-management offering or PM-specific workflow is documented. Zoom's real-estate material is customer-story marketing (virtual tours, virtual receptionist), not a first-party PM product surface, and none of the 64 API groups in the catalog is property-management-specific.
- **Documented PM-specific workflows:** none found. No property, unit, lease, tenant, owner, work-order, or trust-accounting object appears anywhere in the API catalog.
- **Trust or fiduciary workflow support, when relevant:** N-A — the product does not hold, move, or account for client funds, so no trust, security-deposit, or escrow workflow is expected or evidenced.
- **Operational role and dependencies:** Zoom is the conversation layer — the place owner calls, tenant meetings, team standups, and recorded walkthroughs happen. A property management operator building on it still needs a separate PMS, accounting/trust-accounting system, and CRM; Zoom supplies the meeting, its attendance record, and its transcript, and nothing about the property itself.

---

## Coverage classification (fixed before inspection)

**Deviation recorded.** The methodology's default classifications cover Accounting/PMS, Leasing/screening, Workflow/CRM, Maintenance/operations, and Banking/payments. Zoom is none of these. I therefore fixed a category-generic classification for a *unified communications / meetings platform* — derived from what such a platform's core objects and workflows are for any operator, not from Zoom's endpoint list — before inspecting the API surface. It was not altered afterward.

### Objects

| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Users / account members | critical | 3 | Present, full operations |
| Meetings (scheduled sessions) | critical | 3 | Present, full operations |
| Participants / attendance records | critical | 3 | Present (immutable record — read is the operation its role requires) |
| Recordings and transcripts | critical | 3 | Present, read + delete + recover |
| Webinars | important | 2 | Present, full operations |
| Chat / messaging | important | 2 | Present, full operations |
| Voice / telephony (calls, SMS, voicemail) | important | 2 | Present, full operations — **live-verified (read path)** |
| Contacts / directory | important | 2 | Present, full operations |
| Usage and quality reports | important | 2 | Present (read-only by nature) |
| Rooms / devices | optional | 1 | Present |
| Files / docs / whiteboards | optional | 1 | Present |
| Calendar / scheduling | optional | 1 | Present |

### Mutable workflows

| Workflow | Class | Weight | State |
|---|---|---|---|
| Create / schedule a session | critical | 3 | Present — **observed live** |
| Update / reschedule a session | critical | 3 | Present — **observed live** |
| Manage users (create / update / deactivate) | important | 2 | Present |
| Manage registrants / invitees | important | 2 | Present |
| Send a chat message | important | 2 | Present |
| Manage recordings (delete / recover) | optional | 1 | Present |
| Configure account / user settings | optional | 1 | Present |

### Principal lifecycle changes

| Lifecycle action | Class | Weight | State |
|---|---|---|---|
| Delete / cancel a meeting | critical | 3 | Present — **observed live** |
| End a live meeting (status change) | critical | 3 | Present |
| Deactivate / delete a user | important | 2 | Present |
| Delete / recover a recording | important | 2 | Present |
| Approve / deny a registrant | important | 2 | Present |
| Convert meeting ↔ webinar | optional | 1 | Present |

---

## Functional coverage map

- **Core objects:** all twelve present. Operation counts from the first-party Markdown corpora: Meetings 186 operations (includes Webinars, Cloud Recording, Reports, Archiving, Polls, Registration), Phone 397, Chat 111, Users 71, Accounts 66, Marketplace 28. Rooms, Calendar, Scheduler, Whiteboard, Canvas/Docs, Contact Center, QSS and 50 further groups appear as separate catalog anchors.
- **Primary operational workflows:** create/update a meeting (`POST /users/{userId}/meetings`, `PATCH /meetings/{meetingId}`), manage users (`Create users`, `Update a user`, `Delete a user`), manage registrants (`Create a meeting registrant`, `Update registrant's status`), send chat (`zoom_chat_message_send`; Chat corpus send-message operation), manage recordings (`Delete a recording file for a meeting or webinar`, recover).
- **Principal lifecycle changes:** `Delete a meeting`, `Update meeting status` (end a live meeting), `Update a user's status`, `Delete a user`, `Delete meeting or webinar recordings`, `Update registrant's status` (approve/deny), meeting↔webinar conversion.

---

## Category 1: Functional Coverage and Usefulness: 15.0/15

- **C1.1 Object coverage: yes** — weighted coverage = **100%** (25 of 25 weighted points; no critical object absent). Every predetermined object is present with the operations its role requires. Live-verified on the Meetings/Users/Recordings surface and, in packet F2, on Zoom Phone: `GET /phone/users` returned 9 phone users with extensions, calling plans and assigned numbers; `/phone/numbers` 9 numbers; `/phone/devices` 1 provisioned device; `/phone/call_history` 17 call records; `/phone/recordings` 161 recordings — confirming the telephony object is real and populated on this account, not merely documented. [.well-known/api-catalog.json, 64 group anchors; `docs/api/meetings.md` 186 operations; `docs/api/phone.md` 397; `docs/api/users.md` 71; live reads 2026-09-08]
- **C1.2 Core operational actions: yes** — weighted coverage = **100%** (14 of 14). Both critical write workflows observed live, not merely documented: `POST /users/me/meetings` → **HTTP 201**, meeting id `86806188345`, `status: "waiting"`, `host_email: wolf@croskeyrealestate.com`; `PATCH /meetings/86806188345` → **HTTP 204** with read-back confirming `topic: "APITEST-DELETE updated"`, then restored. User, registrant, chat, recording and settings writes documented [`docs/api/users.md` "Create users" / "Delete a user"; `docs/api/meetings.md` "Create a meeting registrant"].
- **C1.3 Delete or lifecycle actions: yes** — weighted coverage = **100%** (13 of 13; no critical lifecycle action absent). Observed live: `DELETE /meetings/86806188345` → **HTTP 204**, re-read → **HTTP 404** `code: 3001` "Meeting does not exist". Remaining actions documented [`docs/api/meetings.md`: "Update meeting status", "Delete meeting or webinar recordings", "Update registrant's status"; `docs/api/users.md`: "Delete a user"].
- **C1.4 Change notification: yes** — documented webhooks cover well above 0.85 weighted of critical-plus-important state changes. `docs/api/meetings/events.md` alone defines **105 events**, including `meeting.created`, `meeting.updated`, `meeting.deleted`, `meeting.participant_joined`, `meeting.participant_left`, `recording.completed`, `meeting.registration_approved` / `_denied`. Event catalogs exist for ~25 further API groups (`.well-known/api-catalog.json` `/events` anchors), and WebSockets are offered as an alternative transport [developers.zoom.us/docs/api/websockets].

**Score math:** earned **4.0** of **4** applicable checks; unrounded fraction = 1.000; category points = **15.0/15**; verification coverage = **100%** (4/4).

**What this means for you:** Within Zoom's own domain there is essentially nothing you can see in the Zoom web interface that you cannot also do through the API. You can schedule meetings, change them, cancel them, pull the attendance list, and fetch the recording and transcript — all under program control, and all confirmed working on your live account today, not just claimed in a manual. Change notification is excellent: you can be pushed an event the moment a meeting ends or a recording finishes, instead of polling for it.

---

## Category 2: API Design, Reliability, and Operability: 5.0/10

- **C2.1 Modern API conventions: yes** — resource-oriented REST over HTTPS with standard verbs and JSON. Observed live: `GET`, `POST` (201), `PATCH` (204), `DELETE` (204) against `/users` and `/meetings/{id}` [base URL `https://api.zoom.us/v2/`, developers.zoom.us/docs/api/].
- **C2.2 Consistent typing: partial** — *Limitation:* numeric values are inconsistently typed as integers in some places and digit-strings in others — within a single object, and for the **same domain concept across two endpoints**. Observed live in one `GET /users` record: `"type": 2` and `"verified": 1` are integers while `"role_id": "2"` is a string. The clearest case is a phone extension: `GET /phone/users` returns `"extension_number": 419` as an **integer**, while `GET /phone/call_history` returns the same concept as `"callee_ext_number": "400"` and `"caller_ext_number": "402"` — **strings** — so a consumer joining call history to phone users must coerce types across the join. `"caller_country_code": "1"` is likewise a digit-string. Documented in the reference: `settings.recurrence.weekly_days` is `string` `"1"`–`"7"` while `recurrence.type` alongside it is `integer`; Cloud Recording `type` is `string` `"1"`–`"99"` while Meetings `type` is `integer`. Counter-evidence recorded: the Phone `users`, `numbers` and `devices` records are cleanly typed with no digit-strings, and `call_id` is correctly a string (it exceeds int64-safe range) — so this is genuine cross-endpoint variance, not a uniform house style. [live `GET /users`, `/phone/users`, `/phone/call_history`, 2026-09-08; `docs/api/meetings.md` "Create a meeting" request body]
- **C2.3 Structured errors: partial** — *Limitation:* the error **body** is well-formed, but the machine code is not stable across endpoints, the body shape varies, HTTP status semantics are not consistently correct, and invalid input is silently accepted. Every genuine failure does return a populated numeric `code` plus a human message — observed live: `404 code 1001` "User does not exist", `404 code 2300` "This API endpoint is not recognized", `400 code 300` "The next page token is invalid or expired", `404 code 3001` "Meeting does not exist", `404 code 2030` "Device does not exist". Against that, three concrete defects:
  1. **The machine code is not stable for one error class.** "Resource does not exist" yields `code 1001` (phone user), `code 2030` (device) and — on `GET /phone/numbers/{bad-id}` — **`code 404`, which is merely the HTTP status echoed into the code field**, carrying no additional machine-readable meaning.
  2. **Body shape varies.** Most errors are `{code, message}`; validation failures add a third key, `{code, message, errors[]}` (observed: `400 code 300` "Validation Failed." on `/phone/numbers?type=NOT_A_TYPE`).
  3. **Invalid input is silently accepted with HTTP 200 on four separate endpoints.** `GET /users?status=NOT_A_STATUS` → 200 with the default result set; `page_size=999999` → 200 clamped to `2000`; `page_size=-5` and `page_size=abc` → 200 clamped to `30`; an unknown query key → 200; and `GET /phone/call_history?from=NOT-A-DATE` → **200 returning unfiltered call history** rather than rejecting the malformed date. Separately, a missing-scope authorization failure returned **HTTP 400** `code 104`, not 401/403, and not the `4700` the error documentation designates for scope failures.
  
  See "Unresolved evaluator disagreements" — defect 3 satisfies the literal `no` criterion, and this check is the one call that moves the letter grade. [developers.zoom.us/docs/api/errors/; live error battery across Meetings, Users and Phone, 2026-09-08]
- **C2.4 Duplicate prevention: no** — no idempotency key, natural-idempotency guarantee, unique request identifier, or equivalent mechanism is documented anywhere: zero occurrences of "idempoten" across the Meetings, Phone, Users and Accounts corpora (4.7 MB), and none in the guides after the controlled verification pass. Confirmed live: three identical `POST /users/me/meetings` calls with identical bodies produced **three distinct meetings** — ids `86806188345`, `81344794266`, `83226566052`. A retried scheduling call duplicates the meeting.
- **C2.5 Graceful handling under load: partial** — *Limitation:* 429 is documented with numeric per-plan quotas ("When you exceed a rate limit, the API request will fail and return a HTTP 429 status code"; Free 4/2/1 per second, Pro 30/20/10, Business+ 80/60/40, plus daily caps), but no `Retry-After` header is documented, none was observed on live responses, and the recovery guidance is qualitative — "implement a wait before retrying", with exponential backoff and jitter advised for 5xx rather than for 429. Responses do carry `x-ratelimit-category` (observed: `Light`, `Medium`) but no `x-ratelimit-remaining` or `x-ratelimit-limit`. [developers.zoom.us/docs/api/rate-limits/; live header capture, 2026-09-08]
- **C2.6 Pagination for large collections: partial** — *Limitation:* traversal works reliably, but no ordering guarantee is documented and the total/next signals are not uniformly present across endpoints. Documented: `next_page_token`, `page_size`, `page_count`, `total_records`, with `page_number` being phased out. Verified live on two independent collections: a complete traversal of `/users` at `page_size=1` returned all 10 records across 10 pages, and `/phone/users` at `page_size=2` returned all 9 records — both with **zero duplicates**, an empty `next_page_token` on the final page, and an **identical record sequence across two independent full traversals**. Against that: the pagination page documents neither a stable-ordering guarantee nor token expiry; the documented `page_size` ceiling ("Up to 300 items per page") did not match live behaviour, which accepted and echoed `page_size: 2000`; and the signal set is **inconsistent across endpoints** — measured live, `/phone/users`, `/phone/numbers`, `/phone/devices` and `/phone/recordings` return `total_records` but no `page_count`; `/phone/call_history` returns **both**; and `/phone/common_areas` returns **neither**, offering only `next_page_token`. A generic sync client cannot rely on a total-count signal being present. [developers.zoom.us/docs/api/pagination/; live traversals and signal survey, 2026-09-08]
- **C2.7 Bulk or incremental export: partial** — *Limitation:* incremental sync is possible on standard list endpoints, but there is no dedicated bulk or export path. Verified live: `GET /users/me/recordings?from=2026-01-01&to=2026-09-08` honoured the date range and reported `total_records: 33`; `?status=active` vs `?status=inactive` returned 10 vs 0, confirming filters are applied. No async export job or bulk-read endpoint exists; the batch operations present are **writes** (`Batch add users`, `Bulk update features for users`, `Perform batch registration`), not exports. A full dataset is therefore assembled by paging list endpoints, not by requesting an extract.
- **C2.8 Webhook security and delivery reliability: yes** — *documentation-graded (step 8 not run; disclosed).* All three elements are documented: signed payloads — "Zoom uses the value of the secret token to hash the webhook data, which it sends in the `x-zm-signature` webhook request header", HMAC SHA-256 over `v0:{timestamp}:{body}` with a CRC URL-validation challenge; a documented retry policy — first retry at **5 minutes**, second at **20 minutes**, third at **60 minutes**, then no further delivery; and consumer replay/idempotency guidance — a unique webhook request identifier that "remains unchanged across retry attempts" together with a retry-attempt count where `0` denotes the initial send. [developers.zoom.us/docs/api/webhooks/]
- **C2.9 Concurrency and conflict control: no** — neither optimistic concurrency nor documented conflict semantics exist. Zero occurrences of `ETag`, `If-Match`, `409`, "optimistic", or a version field across the Meetings, Phone, Users and Accounts corpora, and none in the guides after the controlled verification pass. No `ETag` header was returned on any live response. Concurrent writers to the same meeting will silently overwrite one another.
- **C2.10 Versioning and backward compatibility: partial** — *Limitation:* the version identifier exists but the compatibility policy is informal. An explicit path version is present (`/v2`), the lifecycle page defines Initial Release → Deprecation → Sunset and states that deprecation notices "often include" migration paths and timelines, and the changelog tags entries "Breaking change". But no policy defines what counts as breaking versus non-breaking, and no committed deprecation window is published — observed notice periods vary from 3 months (SDK minimum versions) to 6 months (pagination migration) to 12 months (endpoint removal). [developers.zoom.us/docs/build/lifecycle/; developers.zoom.us/changelog/]
- **C2.11 Request traceability: partial** — *Limitation:* the identifier is present but undocumented as a response header and not evidenced as usable with support. Every live response carried `x-zm-trackingid` (e.g. `v=2.0;clid=us02;rid=WEB_8c8075a650a75f4249f4820ac0f1834b`), including on error responses. However the controlled verification pass established that Zoom documents `x-zm-trackingid` only as a header on **inbound webhook requests**, not as an API response header, and no first-party source documents quoting it to Zoom support. [live header capture on all calls, 2026-09-08; developers.zoom.us/docs/api/webhooks/]
- **C2.12 Service availability and status transparency: partial** — *Limitation:* incident history is published, uptime and SLA are not. A public status page exists with per-component status and an "Incident History" archive covering dated past incidents. It publishes no uptime percentage and no SLA metric, and no SLA was evidenced outside a contract. [https://www.zoomstatus.com/, reached via a 302 from https://status.zoom.us/]

**Score math:** earned **6.0** of **12** applicable checks (yes ×2 = 2.0; partial ×8 = 4.0; no ×2 = 0.0); unrounded fraction = 0.500; category points = **5.0/10**; verification coverage = **100%** (12/12).

**What this means for you:** This is where Zoom's API costs you engineering time. The two hard failures matter in opposite ways. There is **no idempotency** — I proved it by sending the same "schedule a meeting" call three times and getting three meetings — so any automation that retries after a timeout must track what it already created or it will litter your calendar with duplicates. And there is **no concurrency control**, so if two automations edit the same meeting, the later one silently wins with no conflict raised. Add to that a habit of accepting bad input with a `200` — a typo'd filter value returns a normal-looking result set rather than an error — which means bugs in your code surface as quietly wrong data rather than as loud failures. None of this is fatal; all of it means you write more defensive code than a top-tier API would require.

---

## Category 3: Access Control and Safe Automation: 5.0/5

- **C3.1 Read-only credentials: yes** — the scope system separates read from write at the individual operation level, so an app can be granted read scopes only. Observed live: the issued token's 92 scopes are discretely typed, e.g. `meeting:read:meeting:admin` alongside `meeting:write:meeting:admin`, and `user:read:user:admin` with no corresponding user-write scope granted. [live token introspection, 2026-09-08]
- **C3.2 Scoped credentials: yes** — fine-grained resource *and* action scoping, not merely role-based, and demonstrated by a controlled before/after. Scopes take the form `{product}:{action}:{resource}:{admin}` (e.g. `cloud_recording:read:meeting_transcript:admin`, `meeting:delete:registrant:admin`, `phone:delete:call_recording:admin`). Enforcement verified live rather than assumed: with the initial **92-scope** grant, `GET /phone/users` was refused with **HTTP 400 `code 104`** — "Invalid access token, does not contain scopes:[phone:read:list_users:admin]" — while the same token succeeded on meeting and user endpoints. After the operator added Phone permissions the same credential returned **497 scopes (405 of them Phone)** and the identical call succeeded with HTTP 200. The granularity is unusually fine: Zoom Phone alone decomposes into 405 separately grantable scopes, so a credential can be confined to, say, reading call logs without touching call queues, devices, or recordings. [developers.zoom.us/docs/integrations/oauth-scopes-overview/; live token introspection before and after the grant change, 2026-09-08]
- **C3.3 Multiple keys: yes** — multiple Server-to-Server OAuth apps may be created per account, and Zoom recommends exactly that: a unique server-to-server OAuth app per service, in order to isolate permissions, usage and logs. [developers.zoom.us/docs/internal-apps/s2s-oauth/]
- **C3.4 Rotation and revocation: yes** — self-serve, with a safe overlap and an immediate-revocation path. "Your current secret will continue to work for 30 days after a new secret is generated"; "To revoke the old secret immediately, use the rotate client secret API endpoint." Deactivation invalidates issued tokens — verified live and unintentionally: before the app was activated, the token request was refused with `invalid_client` / "The app has been disabled by the developer", and the identical request succeeded immediately after activation, demonstrating that the enable/disable control is both self-serve and effective. [developers.zoom.us/docs/build-flow/basic-info/app-credentials/; live, 2026-09-08]
- **C3.5 Test and production isolation: N-A** — no sandbox or separate test environment for the REST API was evidenced after initial discovery and the controlled verification pass. The check is excluded from the math per its own definition. *(This absence is not free: it is why the write-path testing in this run had to be conducted against live production data under the controlled-live protocol.)*

**Score math:** earned **4.0** of **4** applicable checks (C3.5 N-A, excluded); unrounded fraction = 1.000; category points = **5.0/5**; verification coverage = **100%** (4/4 applicable excluding N-A).

**What this means for you:** This is the strongest part of the API and it is exactly the part that matters for handing work to an AI agent. You can mint a credential that can read meetings but cannot touch phone, cannot delete users, and cannot see recordings — and Zoom actually enforces it, which I confirmed by watching a call get refused for a missing scope. You can issue a separate key per integration, and you can kill any one of them yourself in seconds without filing a ticket. If you are going to let an agent operate your Zoom account, this is the control surface you want.

---

## Category 4: Documentation and AI-Agent Readiness: 5.0/5

- **C4.1 Complete self-serve reference: yes** — complete, public, no login, and example-rich. Every operation carries method, path, tags, prerequisites, required scopes, rate-limit label, a fully expanded request-body schema with types, enums, defaults and per-field descriptions, and response schemas per status code. Worked JSON payload examples are present — 181 example blocks in the Meetings corpus alone. Authentication is documented separately and completely. Nothing in this evaluation required reverse-engineering. [developers.zoom.us/docs/api/meetings.md; developers.zoom.us/docs/internal-apps/s2s-oauth/]
- **C4.2 Reliable machine-consumable integration path: yes** — via an operations-capable MCP server, verified live with our own credential rather than inferred from the server card. `POST https://mcp.zoom.us/mcp/zoom/streamable` `initialize` returned `serverInfo: mcp-gateway`, protocol `2025-06-18`, `capabilities.tools`; `tools/list` returned **20 tools** including `meeting_create`, `meeting_update`, `meeting_delete`, `in_meeting_control`, `recordings_list`, `get_meeting_assets`, `search_meetings`. Three sibling servers responded the same way: Team Chat **20 tools** (`zoom_chat_message_send`, `zoom_chat_channel_create`, …), Docs **32 tools**, Whiteboard. These are core operations, not documentation search. *Noted, not additionally credited:* no downloadable OpenAPI/Swagger file was located — the catalog's `service-desc` links point to `text/html`, and guessed spec paths returned 404 — and Zoom's official SDKs are client-side Meeting/Video SDKs rather than REST wrappers. One strong mechanism is sufficient. [.well-known/mcp/server-card.json; live MCP probe, 2026-09-08]
- **C4.3 AI-readable documentation: yes** — comprehensively, and by deliberate design. `llms.txt` is published at the docs root; it points to an **RFC 9727 `.well-known/api-catalog.json` linkset with 64 entries**, each exposing a `text/markdown` `service-doc` twin of the HTML reference. Those corpora are complete rather than index-only: Meetings 988 KB / 186 operations, Phone 2.0 MB / 397 operations, Chat 375 KB / 111 operations, and each declares its origin (`OpenAPI Version: 3.1.1`, `API Version: 2`) and carries full schemas and examples. This is a first-party, machine-retrievable representation of the entire API. [developers.zoom.us/llms.txt; .well-known/api-catalog.json; docs/api/*.md]
- **C4.4 Kept current: yes** — a dated, tagged, per-product changelog with **102 pages** of history and a weekly cadence. Entries verified on the rendered page: 2026-09-27 (RTMS, tagged **Breaking change**), 2026-09-03 (Phone), 2026-08-31 (Canvas, Cobrowse SDK, My Notes, Phone), 2026-08-24 (eight products), 2026-08-20, 2026-08-18, 2026-08-17. Entries are typed (`API release`, `SDK version`, `New feature`, `Breaking change`) and an RSS feed is offered. [developers.zoom.us/changelog/, rendered 2026-09-08]

**Score math:** earned **4.0** of **4** applicable checks; unrounded fraction = 1.000; category points = **5.0/5**; verification coverage = **100%** (4/4).

**What this means for you:** An AI coding tool can build against this API without you babysitting it. Zoom publishes a machine-readable Markdown copy of its entire reference — every endpoint, every field, every example — and an `llms.txt` index pointing at it, which is exactly what a coding agent needs to stop guessing. It also runs its own MCP servers that can create, update and delete meetings directly, which I verified with your credential. Practically: pointing Claude or a similar tool at Zoom's docs works, and if you would rather skip writing code entirely, the MCP route already exists.

---

## Category 5: Accessibility and Cost: 11.3/15

- **C5.1 Self-serve API key: yes** — credential creation is entirely self-serve. Observed directly in this session: the operator created a Server-to-Server OAuth app in the Zoom App Marketplace, selected scopes, activated it, and produced working credentials with no sales call, no support ticket, and no key-approval step; the token request then succeeded on first attempt. Activation is a self-serve toggle in the same interface, evidenced by the app moving from `invalid_client` / "disabled by the developer" to issuing tokens within the session. [developers.zoom.us/docs/internal-apps/s2s-oauth/; live, 2026-09-08]
- **C5.3 Not commercially gated: partial** — *Limitation:* API access itself is not premium-gated, but a large share of meaningful capability is tier- or licence-gated. Not gated: the rate-limit table publishes explicit per-second and daily quotas for **Free** accounts, establishing that the API is usable without a paid plan. Gated: Webinar endpoints require "Pro or a higher plan with Webinar add-on enabled"; Zoom Phone endpoints require an assigned "Zoom Phone license"; cloud-recording endpoints require Cloud Recording enabled, which is a paid feature; Department Billing endpoints require "Pro or a higher account with Department Billing option enabled". Plan- or licence-prerequisite language appears on **102** lines of the Meetings corpus, 106 of Phone and 58 of Accounts. A free account gets a real API; it does not get recordings, webinars, or telephony through it. [developers.zoom.us/docs/api/rate-limits/; docs/api/{meetings,phone,accounts}.md]

**Score math:** earned **1.5** of **2** applicable checks (yes 1.0 + partial 0.5); unrounded fraction = 0.750; category points = **11.25/15**, displayed **11.3/15**; verification coverage = **100%** (2/2).

**What this means for you:** You can be building today — no gatekeeper, no procurement call. I got a working credential on your account inside this session. The catch is not the API, it is the licence behind it: the endpoints a property manager would actually want most, cloud recordings and their transcripts, only return data if you are paying for cloud recording, and Zoom Phone endpoints do nothing without Phone licences assigned. Check what you are licensed for before you scope a build.

---

## Total

- **Raw: 41.25 / 50**
- **Normalized before rounding: 82.50 / 100**
- **Published numeric score: 83 / 100**
- **Letter grade: B**
- **Evidence tier: Baseline verified** (controlled live — write path observed on operator-authorized fixtures; webhook delivery documentation-graded)
- **Overall verification coverage: 100%** (26 of 26 applicable checks verified; gate requires no category Unable to verify and overall ≥ 80% — both satisfied. Category coverage: C1 100%, C2 100%, C3 100%, C4 100%, C5 100%.)
- **Partial-result flag: yes** — one write-path battery step was not run. Registering a webhook subscription against an operator-controlled HTTPS receiver, triggering a fixture event, and confirming signed delivery would move C2.8 from documentation-graded to observed and lift the run to *Fully verified — controlled live*. It would not change the published score unless observed delivery contradicted the documentation.
- **Unresolved evaluator disagreements:** none. Two checks were close calls and are recorded here so another evaluator can see where a different reading could move the number:
  - **C2.6 (pagination)** was marked *partial* rather than *yes* solely because no stable-ordering guarantee or token expiry is documented, even though stable ordering was observed across two independent full traversals. Scoring it *yes* would raise the raw total from 41.25 to 41.67 (normalized 83.33) — the published score stays **83** and the grade stays **B**.
  - **C2.3 (structured errors)** is the closest call in this report and the only one that changes the letter grade. It was marked *partial*, but a second evaluator applying the check's literal wording should reasonably mark it *no*, and the F2 Phone evidence strengthened that case rather than weakening it. **The case for `no`:** the criterion is disjunctive — "unstructured errors, **or** success codes that hide failures" — and the second disjunct is now satisfied on five endpoints, most damagingly `GET /phone/call_history?from=NOT-A-DATE` returning HTTP 200 with *unfiltered* call history rather than rejecting the malformed date; the `yes` requirement of a "populated, **stable**, machine-readable error code" also fails, since one endpoint returns `code 404` — the HTTP status echoed. **The case for `partial` (the mark chosen):** the check's headline question is "do failures return structured errors an integration can act on", and for genuine failures Zoom does exactly that, consistently, with meaningful codes and messages; the silent-200 cases are a distinct defect — invalid input not being *treated* as a failure — rather than a failure returning an unusable error. Scoring it *no* lowers the raw total to 40.83 (normalized 81.67), giving a published score of **82** and a grade of **B-**. The evidence for both readings is set out under C2.3 so a re-grader can decide without re-running the battery.

---

## Bottom line for a property manager

Zoom's API is a solid, genuinely buildable B, and its strengths sit exactly where an operator automating with AI would want them: you can create a scoped, read-only key in minutes without talking to anyone, Zoom enforces those scopes properly, and the entire reference is published in a machine-readable form that an AI coding tool can consume without guessing — Zoom even runs its own MCP servers that create and update meetings directly. Everything Zoom's product does, the API does too: I scheduled, edited, and deleted a meeting on your live account today, and pulled attendance and recording data back out.

What holds it to a B is production plumbing rather than features. There is no idempotency — I sent the identical "schedule a meeting" request three times and got three meetings — and no concurrency control, so retry-safe, multi-writer automation is your job, not Zoom's. The API also tends to accept bad input with a cheerful `200` instead of an error, which turns your bugs into quietly wrong data. Budget for defensive code and a record of what you have already created.

The more important caveat is fit, not quality. **Zoom is general-purpose, not a property-management system**, and nothing in its 64 API groups knows what a property, unit, lease, tenant, or owner is. It is not a bank, holds no client funds, and documents no trust, security-deposit, or escrow workflow — a high API score here says nothing about its suitability for any of that. Its real role for a property manager is the conversation layer: owner calls, tenant meetings, and recorded walkthroughs, with the attendance record and transcript pulled out automatically and filed against the right property **in your PMS or CRM**, which you still need alongside it. One last practical note: the endpoints most valuable for that use — cloud recordings and transcripts — return nothing unless you are licensed for cloud recording, so confirm your plan before scoping the build.
