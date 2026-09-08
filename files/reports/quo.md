# API Report Card: Quo (formerly OpenPhone) Public API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 4.8 (claude-opus-4-8)
- Date run: 2026-09-08
- Provisional evidence-packet version or ID: quo-grader-packet-prov-2026-09-08
- Final evidence-packet version or ID: quo-grader-packet-v1.1-2026-09-08 (frozen; amended after 3-run reconciliation — see `evidence/reconciliation.md`)
- Reconciliation: published score is the result of 3 independent runs (1 orchestrator + 2 blind subagent graders) compared check-by-check; 23/26 marks identical, 3 resolved against evidence (C2.3→partial, C2.11→yes, C2.12→yes). Not an average.
- Evidence-discovery mode: tool-enabled discovery (first-party sources) + live API access
- Evidence tier: **Baseline verified — controlled live** (read-path fully live; write-path C1.2/C1.3 observed on operator-authorized sentinel fixtures with verified cleanup; C2.8 webhook delivery and the message-send portion of C1.2 documentation-graded)
- Live-write method and safety: controlled live — net-new sentinel fixtures (`APITEST-DELETE`) created then deleted; operator authorization recorded in-session; cleanup verified (post-test audit: 0 lingering fixtures); no money moved, no SMS/calls sent, no task assigned to a real user, no real record touched
- Minimum live-test battery: complete for a Baseline-verified run — steps 1–6 performed live; step 7 (idempotency) N-A (no idempotency mechanism exists); step 8 (webhook delivery) documentation-graded (no operator-controlled HTTPS endpoint available and webhook writes were out of the authorized scope)
- Live tests performed: authenticate; read + multi-page paginate (users, contacts, conversations, phone numbers, organization); incremental filter (`updatedAfter` honored); 4 deliberate errors (400 missing-version, 400 field-validation, 401, 404, plus v1 400 with granular `code`); rate-limit & correlation headers; contact create→read→update→delete; task create→read→update→complete→reopen→delete
- Live tests not possible: webhook end-to-end delivery (no operator-controlled endpoint; not in authorized write scope); message send (hard-excluded external communication)
- Documentation-graded checks (baseline verified): C2.8 (webhook signing/retry/delivery — management ops observed, delivery not); message-send sub-item within C1.2/C1.4

## Final evidence packet manifest
First-party sources (accessed 2026-09-08):
- OpenAPI 3.1 spec, current version: `https://openphone-public-api-prod.s3.us-west-2.amazonaws.com/public/openphone-public-api-2026-03-30-prod.json` (base URL `https://api.quo.com`, 22 paths)
- OpenAPI 3.1 spec, v1: `https://openphone-public-api-prod.s3.us-west-2.amazonaws.com/public/openphone-public-api-v1-prod.json` (35 paths, `/v1/...`)
- Docs index / llms.txt: `https://www.quo.com/docs/llms.txt`; AI resources: `https://www.quo.com/docs/2026-03-30/ai-agents` (cites llms.txt, llms-full.txt, spec, docs-bundle zip)
- Introduction: `https://www.quo.com/docs/2026-03-30/introduction`; Quickstart: `.../quickstart`
- Authentication: `https://www.quo.com/docs/2026-03-30/authentication`
- Versioning: `https://www.quo.com/docs/2026-03-30/versioning`
- Making requests (envelopes/ids/timestamps/pagination): `https://www.quo.com/docs/2026-03-30/requests`
- Errors: `https://www.quo.com/docs/2026-03-30/errors`
- Rate limits: `https://www.quo.com/docs/2026-03-30/rate-limits`
- Changelog: `https://www.quo.com/docs/2026-03-30/changelog`
- Webhooks overview / signature validation: `https://www.quo.com/docs/2026-03-30/webhooks-overview`, `.../webhooks-signature-validation`
- API pricing: `https://www.quo.com/docs/mdx/pricing-support/pricing-overview`; Plans: `https://www.quo.com/pricing`
- Status/uptime: `https://status.quo.com` (persisted in packet: `evidence/live/status_page.html`, `evidence/live/status_summary.json`)
- MCP: `https://www.quo.com/docs/2026-03-30/mcp/overview`, `.../mcp/tools`
- Live API observations against `https://api.quo.com` using the operator-supplied key (raw responses retained locally in `evidence/live/`)

## Evidence-amendment log
- None. Discovery and the controlled verification pass were completed in one run; no source was removed after provisional scoring. Live write observations (contact/task fixtures) were added under recorded operator authorization and affect C1.2 and C1.3 (upgraded from documentation-graded to observed).

## API eligibility
- Qualifying API: **yes**
- API operator: Quo (the OpenPhone product, rebranded; S3 spec bucket `openphone-public-api-prod`, spec `info.title` = "Quo Public API") [openphone-public-api-2026-03-30-prod.json → `info`]
- Access or credential issuer: the customer's own workspace owner/admin, self-serve in **Workspace Settings → API** [docs/2026-03-30/authentication → "Get an API key"]
- Eligibility basis: a first-party, documented REST API at `https://api.quo.com` exposing Quo's own communication functions (messages, calls, contacts, conversations, tasks, phone numbers, users, webhooks, organization), authenticated by a workspace API key; confirmed live (HTTP 200 to `GET /users`, 2026-09-08).

## Context
- Software category: **Workflow/CRM tool** (a business telephony/communications platform — an *adjacent operating tool* for a property manager, not a PMS or bank). Deviation note: the Workflow/CRM default classes were instantiated for a communications product — "records" = contacts + conversations + messages + calls; "automations/triggers" = webhooks/events; "custom fields" = contact custom fields; "boards/pipelines" = N-A (no such concept).
- What the API is for and its core objects/workflows: Quo opens its shared phone system to software. Core objects: contacts, conversations, messages (SMS), calls (+ recordings/summaries/transcripts/voicemails), phone numbers, tasks, users, webhooks, organization. Core workflows: sync contacts, send/receive texts, read call logs and AI transcripts/summaries, manage conversation state, create/track tasks, and receive real-time webhook events.

## Provider and property-management fit
- What this product is: a cloud business phone system (shared numbers, SMS, calls, AI call summaries/transcripts, contacts) with a REST API and an official MCP server [docs/2026-03-30/introduction].
- Bank status, when relevant: **N-A** (not a financial product).
- Who provides any bank account or regulated banking service: **N-A**.
- What the customer actually receives: per-seat SaaS communications software plus API access; API messaging is billed from a prepaid credit balance [docs/mdx/pricing-support/pricing-overview → "How our billing works"].
- Property-management fit: **general-purpose** — no dedicated property-management offering or PM-specific workflows are documented; the product is a general business phone system usable by (but not specialized for) property managers.
- Documented PM-specific workflows: **none found**.
- Trust or fiduciary workflow support, when relevant: **N-A** (no funds-holding or ledger functionality).
- Operational role and dependencies: Quo is the tenant/owner/vendor communications layer; a property manager would still need a separate PMS, accounting, and trust-accounting system, and would typically wire Quo to those via its contacts sync + webhooks.

## Coverage classification (fixed before inspection)
| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Contacts (records) | critical | 3 | Present, full CRUD (+ custom-field values) |
| Messages / SMS (records) | critical | 3 | Present (send, list, get, retry) |
| Webhooks & events (automations/triggers) | critical | 3 | Present, full management + delivery inspection |
| Conversations | important | 2 | Present (list + state changes) |
| Calls (+ media/AI) | important | 2 | Present, read-only (appropriate for logs) |
| Phone numbers | important | 2 | Present, read-only (provisioned in-app) |
| Tasks | important | 2 | Present, full lifecycle |
| Contact custom fields | important | 2 | Present (definitions read-only; values writable) |
| Users | optional | 1 | Present, read-only |
| Organization | optional | 1 | Present, read-only |
| Reporting / exports | optional | 1 | Partial (AI summaries/transcripts; no bulk export) |
| Boards / pipelines | N-A | — | Concept absent in a comms tool |
| Workflow: create/update records | critical | 3 | Present (contacts observed; send documented) |
| Workflow: fire/receive triggers | critical | 3 | Present (webhooks + polling) |
| Workflow: conversation state change | important | 2 | Present (mark read/done/open) |
| Workflow: task lifecycle | important | 2 | Present (observed complete/reopen/delete) |

## Functional coverage map
- Core objects: contacts **present (CRUD)**; messages **present (send/list/get/retry)**; webhooks/events **present**; conversations **present (list + mark read/done/open)**; calls **present, read-only** (+ recordings/summaries/transcripts/voicemails); phone numbers **present, read-only**; tasks **present (full)**; contact custom fields **present** (defs read-only, values writable); users **present, read-only**; organization **present, read-only**; reporting/export **partial**.
- Primary operational workflows: contact sync (create/update/delete — observed live); SMS send/receive (send documented; receipt via webhook); conversation triage (mark read/done/open); task management (create/update/complete/reopen/delete — observed live); real-time eventing (webhooks).
- Principal lifecycle changes: contact delete (observed 204→404); task complete/reopen/delete (observed); conversation mark done/open/read; message retry-failed; webhook delete + signing-secret rotate.

## Category 1: Functional Coverage and Usefulness: 15.0/15
- **C1.1 Object coverage: yes** — weighted coverage = **98%** (21.5/22; no critical object absent). Contacts [v1 `/v1/contacts` GET/POST/PATCH/DELETE; 2026-03-30 `/contacts`], messages [v1 `/v1/messages` GET/POST, `/v1/messages/{id}`], calls + media [v1 `/v1/calls`, `/v1/call-recordings|summaries|transcripts|voicemails/{id}`], conversations [v1 `/v1/conversations` + `/conversations/{id}/mark-as-*`], phone numbers [v1 `/v1/phone-numbers`], tasks [`/v1/tasks*`], users [`/users`], webhooks [`/webhooks*`], organization [`GET /organization`], contact custom fields [`/v1/contact-custom-fields`]. Live-confirmed reads 2026-09-08 on users, contacts, conversations, phone numbers (4), organization.
- **C1.2 Core operational actions: yes** — weighted coverage = **100%** (no critical write absent). Observed live 2026-09-08: contact create (`POST /v1/contacts` → 201) and update (`PATCH /v1/contacts/{id}` → 200, `company` changed); task create (`POST /v1/tasks` → 201) and update (`PUT /v1/tasks/{id}` → 200). Message send [`POST /v1/messages`] and conversation-state writes [`/conversations/{id}/mark-as-*`] and webhook create/update [`POST/PATCH /webhooks`] present; message send is **documentation-graded** (hard-excluded from live test as external communication).
- **C1.3 Delete or lifecycle actions: yes** — weighted coverage = **100%** (no critical lifecycle absent). Observed live: contact delete (`DELETE /v1/contacts/{id}` → 204, then 404); task complete (`/complete` → 200), reopen (`/reopen` → 200), delete (→ 204, then 404). Also documented: conversation mark done/open, message retry, webhook delete + `POST /webhooks/{id}/rotate`.
- **C1.4 Change notification: yes** — webhooks cover message (`received`/`delivered`/`failed`/`undelivered`), the full call lifecycle (incl. `call.completed`, `call.summary.completed`, `call.transcript.completed`, `call.menu.selected`), `contact.updated`/`deleted`, and 12 `task.*` events [docs/2026-03-30/webhooks-overview; changelog 2026-06-18/07-09/08-25]; incremental polling (`updatedAfter`/`since`/`createdAfter`) is available as a backup and was honored live on conversations.

Score math: earned 4 of 4 applicable checks; unrounded fraction = 1.000; category points = **15.0/15**; verification coverage = 4/4 = **100%**.
What this means for you: For its domain — business phone/SMS — this API is genuinely complete. You can sync your tenant/owner/vendor contacts both ways, send and receive texts, pull call logs with AI transcripts and summaries, manage conversations and tasks, and get real-time events. The main gaps are richness, not reach: no outbound *call initiation* via API and no MMS in the current version.

## Category 2: API Design, Reliability, and Operability: 7.9/10
- **C2.1 Modern API conventions: yes** — resource-oriented REST, JSON in/out, standard verbs (GET/POST/PATCH/PUT/DELETE) observed live [OpenAPI paths; docs/2026-03-30/requests].
- **C2.2 Consistent typing: yes** — OpenAPI 3.1 with explicit types, `anyOf`+`{type:null}` nullability, `format`/`pattern` constraints; live `GET /users` and `GET /contacts` payloads matched documented types exactly (2026-09-08).
- **C2.3 Structured errors: partial** *(reconciled: R1 yes → resolved partial with R2/R3)* — structured envelope with correct HTTP status semantics, human-readable `message`, field-level `errors[].path/value/schema`, and a `trace` id, all observed live (`live/e_ver.json`, `e_lim.json`, `e_auth.json`, `e_404.json`). **Limitation — error shapes vary across endpoints:** the flagship 2026-03-30 core-resource errors (users/contacts/tasks) carry no stable top-level machine `code`, whereas v1 and webhook-family errors do (e.g. `live/msg.json` `code:"0100400"`; spec consts `0300401`/`0301500`). No single populated stable machine code across the surface → partial.
- **C2.4 Duplicate prevention: no** — no idempotency mechanism is documented in either spec (0 occurrences of idempotency/`Idempotency-Key`), and the errors guide explicitly warns that a retried `POST` such as a message send "can repeat its effect" [docs/2026-03-30/errors → "Retrying"]. Consequential creates/sends are unprotected. (Not N-A: the API has consequential writes.)
- **C2.5 Graceful handling under load: yes** — documented `429` at 10 req/s/key plus machine-readable `ratelimit` and `ratelimit-policy` response headers observed live (`"per-second"; q=10; w=1`, `r=9; t=1`) and explicit exponential-backoff-with-jitter guidance [docs/2026-03-30/rate-limits; live headers 2026-09-08].
- **C2.6 Pagination for large collections: yes** — cursor pagination (`limit` 1–50 default 10, `after`, `nextCursor`) in 2026-03-30; v1 adds `totalItems` + `nextPageToken`. Live multi-page traversal returned distinct, stable pages [docs/2026-03-30/requests; live 2026-09-08].
- **C2.7 Bulk or incremental export: partial** — incremental sync is possible on list endpoints (`since`/`createdAfter`/`updatedAfter` + pagination; `updatedAfter` honored live on conversations), **but** there is no dedicated bulk/export path (no async export jobs or bulk endpoints), messages/calls lists require `phoneNumberId`+`participants` (per-conversation scope, not a whole-dataset pull — confirmed live via a 400), and contacts have no updated-since filter.
- **C2.8 Webhook security and delivery reliability: yes (documentation-graded)** — HMAC-SHA256 signatures (`webhook-signature`, svix-compatible, `whsec_` secret), a documented 8-attempt retry schedule (~27h), consumer idempotency via `webhook-id`, replay protection, and delivery inspection/retry endpoints [docs/2026-03-30/webhooks-overview, webhooks-signature-validation]. Management endpoints exist and are in-spec; end-to-end delivery was not live-observed (no operator-controlled endpoint; out of authorized write scope).
- **C2.9 Concurrency and conflict control: partial** — documented `409 Conflict` on all contact writes [v1 `/v1/contacts*`] and a `revision` version field on tasks (observed incrementing on update, 2026-09-08), **but** no documented optimistic-concurrency mechanism (no `If-Match`/`ETag` write path — the response `etag` is a generic weak validator — and no way to submit an expected `revision`) and no documented concurrency behavior.
- **C2.10 Versioning and backward compatibility: yes** — required dated `Quo-Api-Version` header, an explicit breaking-vs-non-breaking policy, and a retirement/migration-window commitment [docs/2026-03-30/versioning; changelog 2026-03-30].
- **C2.11 Request traceability: yes** *(reconciled: R1/R2 yes, R3 partial → resolved yes)* — a documented `trace` id explicitly usable with support ("we can pull up the exact request") satisfies the yes clause "an equivalent documented trace mechanism"; an `x-correlation-id` is additionally present on every response observed live [docs/2026-03-30/errors → "The trace id"; `live/headers_users.txt`].
- **C2.12 Service availability and status transparency: yes** *(reconciled: R1 yes, R2/R3 no due to a packet-completeness gap, now fixed → resolved yes)* — public first-party status page `status.quo.com` (statuspage.io) with a **Quo API** component, per-service uptime (API 99.997%) and a Jun–Sep 2026 incident-history calendar; persisted to the packet as `live/status_page.html` + `live/status_summary.json` ("All Systems Operational", 0 active incidents).

Score math: earned 8 yes + 3×0.5 (C2.3, C2.7, C2.9) + 0 (C2.4) = 9.5 of 12 applicable; unrounded fraction = 0.792; category points = **7.9/10**; verification coverage = 12/12 = **100%**.
What this means for you: This is a modern, well-instrumented API that code and AI agents can run in production — predictable types, actionable errors with trace ids, real rate-limit headers, clean pagination, a real versioning contract, and excellent webhook security. Two things to engineer around: there is **no idempotency key**, so you must dedupe consequential retries (especially message sends) yourself, and there is **no bulk export** or cross-workspace message/call pull.

## Category 3: Access Control and Safe Automation: 2.5/5
- **C3.1 Read-only credentials: no** — keys are full workspace access; no read-only credential option ("each key has full access to your workspace's API"; "the same reach as an admin") [docs/2026-03-30/authentication].
- **C3.2 Scoped credentials: no** — a key cannot be restricted to specific resources/actions/roles; it is a single all-powerful credential [same citation].
- **C3.3 Multiple keys: yes** — multiple named keys, one per integration, are supported and encouraged [docs/2026-03-30/authentication → "one key per integration"].
- **C3.4 Rotation and revocation: yes** — self-serve generate/delete in Workspace Settings → API; "access ends immediately" [docs/2026-03-30/authentication → "Revoke a key"].
- **C3.5 Test and production isolation: N-A** — no sandbox/separate test environment is documented.

Score math: earned 2 of 4 applicable checks (C3.5 N-A); unrounded fraction = 0.500; category points = **2.5/5**; verification coverage = 4/4 = **100%**.
What this means for you: This is the API's weakest area. Every key is an admin-equivalent, full-access credential — you cannot mint a read-only or narrowly scoped key for an AI agent or a third-party tool. Your only real controls are issuing separate keys per integration and revoking them fast. Treat each key like an admin password.

## Category 4: Documentation and AI-Agent Readiness: 5.0/5
- **C4.1 Complete self-serve reference: yes** — complete public reference with auth, per-endpoint params, and worked request/response examples; usable without reverse-engineering (verified across many pages, 2026-09-08).
- **C4.2 Reliable machine-consumable path: yes** — published, complete OpenAPI 3.1 specs (v1 and 2026-03-30) plus an official MCP server; the docs name the spec the "ground truth" [docs/2026-03-30/ai-agents].
- **C4.3 AI-readable documentation: yes** — `llms.txt`, `llms-full.txt`, per-endpoint `.md`, and a downloadable docs-bundle zip [docs/2026-03-30/ai-agents; docs/llms.txt].
- **C4.4 Kept current: yes** — a detailed, dated changelog through September 2026 with RSS, plus versioning/deprecation guidance [docs/2026-03-30/changelog].

Score math: earned 4 of 4 applicable checks; unrounded fraction = 1.000; category points = **5.0/5**; verification coverage = 4/4 = **100%**.
What this means for you: Best-in-class for building — including with AI. A coding agent handed `llms.txt` and the OpenAPI spec can build against this correctly, and the changelog keeps you current.

## Category 5: Accessibility and Cost: 11.3/15
- **C5.1 Self-serve API key: yes** — an owner/admin generates a key in Workspace Settings → API with no sales call, ticket, or approval step [docs/2026-03-30/authentication].
- **C5.3 Not commercially gated: partial** — the core API (messaging, contacts, calls metadata, conversations, tasks, webhooks, users) and the MCP connector are included on **all three plans**, including entry-level Starter ($15/user/mo annual) [quo.com/pricing]; **but** two meaningful capabilities — AI **call summaries** and **transcripts** — require Business/Scale plans [docs/mdx/api-reference/calls/get-a-summary-for-a-call, .../get-a-transcription-for-a-call], and an active paid subscription is required for any API access [pricing-overview → "Requirements & limitations"].

Score math: earned 1 + 0.5 = 1.5 of 2 applicable checks; unrounded fraction = 0.750; category points = **11.3/15**; verification coverage = 2/2 = **100%**.
What this means for you: You can get in the door on the cheapest paid plan and turn on the API yourself in a minute — no sales call. Budget for two things: per-segment SMS credits ($0.01+/segment) billed from a prepaid balance, and an upgrade to Business/Scale if you need AI call summaries or transcripts via the API.

## Total (3-run reconciled)
- Raw: **41.67 / 50** (C1 15.0 + C2 7.9 + C3 2.5 + C4 5.0 + C5 11.3)
- Normalized before rounding: **83.33 / 100**
- Published numeric score: **83 / 100**
- Letter grade: **B**
- Evidence tier: **Baseline verified — controlled live**
- Overall verification coverage: **100%** (26/26 applicable checks verified; no category Unable to verify; overall ≥ 80% — gate passes)
- Partial-result flag: no (publishable). Write-path C1.2/C1.3 observed live; C2.8 webhook delivery documentation-graded.
- Cross-run reproducibility: 3 runs → 23/26 marks identical (88%). Pre-reconciliation published numbers were 84 (R1) / 82 (R2) / 81 (R3). Three checks resolved against evidence: **C2.3** yes→partial (error `code` shapes vary across endpoints), **C2.11** resolved yes (documented `trace` mechanism), **C2.12** resolved yes (status page real; packet gap fixed). Details in `evidence/reconciliation.md`.
- Residual (agreed) sensitivity — **C5.3 (highest impact).** All three runs marked it **partial**, and all three independently flagged it as the pivotal call: if the Business/Scale gate on AI call summaries/transcripts is read as premium *product-feature* pricing rather than API commercial gating, C5.3 = yes → Category 5 = 15.0/15, raw = 45.42/50, normalized = **90.8 → 91 (A-)**. Published result holds the literal reading (partial).
- Other latent close calls (no grade change): **C2.4** no vs partial (naturally-idempotent state ops); **C2.7** partial vs yes (updated-since sync); **C2.9** partial vs no (`revision` field not wired to conditional writes).

## Bottom line for a property manager
Quo (formerly OpenPhone) is a **general-purpose business phone system with an unusually good, modern API** — not a property-management platform, not a bank, and it holds no funds. Today you can build a lot on it: two-way contact sync for tenants, owners, and vendors; automated SMS (send documented, receive via signed webhooks); call logs with AI transcripts and summaries; conversation triage; and task tracking — all live-verified here except message send (excluded from testing because it would text real people). The API's real strengths are developer- and agent-readiness: clean REST, strong typing, actionable errors with trace ids, real versioning, first-class webhooks, and an OpenAPI spec plus MCP server. Its real weaknesses are **access control** (every key is full-access — no read-only or scoped keys, which matters if you hand a key to an AI agent) and the absence of **idempotency keys** and a **bulk export** path. It scores a **B (83/100)** as an API (three independent runs landed at 84/82/81 and reconciled to 83); as a *tool*, it is the communications layer of a property-management stack, and you would still run a separate PMS, accounting, and trust-accounting system alongside it.
