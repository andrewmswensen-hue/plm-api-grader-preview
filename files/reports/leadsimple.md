# API Report Card: LeadSimple REST API

## Run metadata
- Methodology version: 1.1
- Evaluating model: Claude Opus 4.8 (claude-opus-4-8)
- Date run: 2026-08-28 (re-run after LeadSimple shipped access-control and documentation improvements)
- Provisional evidence-packet version or ID: LS-REST-2026-08-28-prov1
- Final evidence-packet version or ID: LS-REST-2026-08-28-final (frozen)
- Evidence-discovery mode: tool-enabled discovery — new public docs + public OpenAPI 3.0 (2026-08-28), operator report of key-management changes (2026-08-28), and carried-forward live read-path evidence from 2026-08-25 (API surface unchanged, re-confirmed against the new spec)
- Evidence tier: Baseline verified (read-path battery run live 2026-08-25; write-path documentation-graded)
- Live-write method and safety: none — writes documentation-graded (operator authorized read-only live testing only; standing safety rule for live production accounts)
- Minimum live-test battery: read-path steps 1–5 complete (2026-08-25, unchanged endpoints); write-path steps 6–8 documentation-graded
- Documentation-graded checks (baseline verified): C1.2 (write portion), C1.3 (write portion), C2.4 (idempotency), C2.8 (webhook security/retry)
- **What changed since the 2026-08-27 run (78/100, C+) → 87/100 (B+), reconciled across two independent runs.** LeadSimple shipped five first-party improvements (operator report 2026-08-28), all in the two weakest categories:
  1. New public documentation site at `https://docs.leadsimple.com/` — a complete, no-login API reference (previously the Swagger UI was login-gated).
  2. Multiple API keys can now be created (previously one key per account).
  3. Keys can be **read-only** for the first time (previously the single key was full read/write).
  4. Keys can be **revoked**, not just rotated (previously rotate-only).
  5. Keys can be **labeled**.
  These moved **C3.1 no→yes**, **C3.2 no→partial**, **C3.3 no→yes**, and **C4.1 partial→yes**; the public OpenAPI also strengthened C4.2. Category 3 rose from 1.3/5 to 4.4/5 and Category 4 from 2.5/5 to 3.1/5. Categories 1 and 5 are unchanged (the API surface, data model, and plan access did not change — re-confirmed against the new OpenAPI 3.0 spec). The LeadSimple improvements did not touch Category 2; the two-independent-run reconciliation (methodology step 12) then resolved C2.10 (versioning) from no to partial, lifting Category 2 from 5.4 to 5.8 and the reconciled published score to 87 (B+). This run supersedes the 2026-08-27 re-score.

## Final evidence packet manifest
- https://docs.leadsimple.com/ — new **public** API reference (Scalar-rendered; no login), observed 2026-08-28: "Download OpenAPI Document", client-library request samples in Shell/Ruby/Node.js/PHP/Python, full operation set
- https://docs.leadsimple.com/openapi.json — **public** OpenAPI 3.0.0 spec (frozen copy: `evidence/leadsimple-openapi-3.0-2026-08-28.json`, 327,810 bytes, 59 paths / 72 operations, `securitySchemes.api_key` bearer)
- Operator-supplied API Keys screenshot (2026-08-28): the REST API settings page + Create REST API key dialog — a "Create API key" button, per-key "Rotate" and "Revoke" controls, a required key name, and a "Read-only access" checkbox (only read-only vs. read-and-write; no per-resource scoping)
- https://api.leadsimple.com/rest/* — live API responses observed 2026-08-25 with the operator's production key (read-only); endpoints unchanged in the 2026-08-28 spec
- https://status.leadsimple.com/ — status page (16 components incl. REST API; 100% 90-day uptime)
- https://www.leadsimple.com/platform, https://www.leadsimple.com/pricing — product/pricing (C5 context; observed 2026-08-27)
- https://docs.leadsimple.com/llms.txt and /llms-full.txt — both HTTP 404 (no AI-doc corpus), observed 2026-08-28
- https://product.leadsimple.com/, https://feedback.leadsimple.com/changelog — product-wide changelog (not API-specific)

## Evidence-amendment log
- C3.1 / C3.3 / C3.4: raised on an operator-supplied screenshot (2026-08-28) of the API Keys page and Create-key dialog — a "Read-only access" checkbox, a "Create API key" button with named keys, and per-key "Rotate" + "Revoke". C3.2 raised no→partial (read-only vs. read-and-write is a role-level scope; the create-key dialog shows no per-resource scoping option).
- C4.1: raised partial→yes — the reference is now public (docs.leadsimple.com) with multi-language request samples; login gate removed.
- C4.2: re-confirmed yes — the OpenAPI is now public (OpenAPI 3.0.0) and downloadable, upgraded from the prior auth-gated 2.0 spec.
- C4.3: re-verified no — `/llms.txt` and `/llms-full.txt` both 404 on the new docs; the site is a reference-only SPA with no Markdown corpus.
- C2.2 / C2.3 / C2.9 / C2.10: re-confirmed against the new spec — money fields still typed as strings (`Deal.value`, `Deal.cost`, `Unit.market_rent`, `Unit.current_rent`, `Unit.estimated_rent`), error schemas unchanged (`Errors_Authorization/NotFound/Validation`), no 409/ETag/If-Match, server still `/rest` with no version in path.

## API eligibility
- Qualifying API: yes
- API operator: LeadSimple (`api.leadsimple.com/rest`; spec `info.title: "LeadSimple REST API"`, OpenAPI 3.0.0)
- Access or credential issuer: LeadSimple — self-serve API keys at Settings → Integrations → REST API
- Eligibility basis: A public OpenAPI 3.0 spec and public reference expose LeadSimple's own functions (contacts, deals, processes, tasks, calls, messages, webhooks, reports) over authenticated REST; access is via account API keys. Confirmed live 2026-08-25 (`GET /info/user` → 200 with a bearer key).

## Context
- Software category: Workflow / CRM tool (with maintenance-operations overlap). Default Workflow/CRM coverage classification applied.
- What the API is for and its core objects and workflows: The LeadSimple REST API lets an operator read and change the CRM and operations data that runs a property-management front office — contacts, deals/leads, processes (which carry maintenance work orders), tasks, calls, text messages, conversations, notes, pipelines, custom fields, and properties/units — and subscribe to change events via webhooks. Core workflows are create/update records, advance pipeline/process stages, and fire/receive triggers. It is not the system of record for the underlying PMS (it "sits on top of your PMS").

## Provider and property-management fit
- What this product is: A property-management CRM, phone/inbox, and operations-automation platform that consolidates leads, communications, processes, and maintenance coordination. [leadsimple.com/platform]
- Bank status, when relevant: N-A (not a financial-services provider).
- Who provides any bank account or regulated banking service: none.
- What the customer actually receives: SaaS CRM + workflow/communication software; the API returns the operator's own account data. [live reads 2026-08-25]
- Property-management fit: PM-specialized — property management is the product's central purpose, with documented PM workflows (owner/lead pipelines, maintenance triage/dispatch, resident/owner update automation). [leadsimple.com/platform]
- Documented PM-specific workflows: lead → owner conversion pipelines; recurring operational processes with SLAs; maintenance triage/dispatch as processes; resident/owner automated updates; direct sync from AppFolio/Buildium/Rentvine/Propertyware/Rent Manager. [leadsimple.com/platform; help-center integration articles]
- Trust or fiduciary workflow support, when relevant: N-A — no trust/escrow/deposit or money-movement objects in the API. Deal `value`/`cost` are CRM annotations, not fiduciary ledgers. [spec: no accounting/payment endpoints]
- Operational role and dependencies: LeadSimple is the front-office CRM/operations layer; the operator still needs the underlying PMS (AppFolio/Buildium/etc.) for property, lease, ledger, and money data.

## Coverage classification (fixed before inspection — default Workflow/CRM)
| Object or workflow | Class | Weight | Present / read-only / absent |
|---|---|---|---|
| Contacts (record) | critical | 3 | Present — create/read/update (`POST/GET/PUT /contacts`) |
| Deals / leads (record) | critical | 3 | Present — create/read/update (`POST/GET/PUT /deals`) |
| Processes / work-orders (record + workflow) | critical | 3 | Present — create/read/update + stage transitions |
| Automations / triggers (fire + receive) | critical | 3 | Present — webhook CRUD + 19 event types; process create/advance |
| Tasks (record) | important | 2 | Present but read-only (`GET /tasks` only) |
| Communications (calls, texts, conversations, notes) | important | 2 | Present — create/update |
| Pipelines / stages / steps (boards) | important | 2 | Present, read-only (configuration) |
| Custom fields | important | 2 | Present — create/read |
| Properties / units (context) | important | 2 | Present, update-only (no create) |
| Reports / analytics | optional | 1 | Present — deal report endpoints |
| Users / accounts | optional | 1 | Present, read-only |
| Bulk / warehouse export | optional | 1 | Incremental sync only; no dedicated bulk endpoint |

## Functional coverage map
- Core objects: contacts (CRUD-), deals (CRUD-), processes (CRUD-), custom_fields (create/read), tasks (read-only), calls/text_messages/conversations/notes (create/update), pipelines/stages/steps (read-only), properties/units (read/update), reports (action), users/accounts (read-only), webhook_subscriptions (full CRUD). ("CRUD-" = create/read/update, no delete.)
- Primary operational workflows: create/update contacts, deals, processes; advance stages; reassign; tag/untag; run reports; subscribe to and receive events.
- Principal lifecycle changes: deal/process stage transitions + close; conversation status change; reassignment; tag changes; delete webhook subscription. Absent: hard delete/archive of core records; task completion via API.

## Category 1: Functional Coverage and Usefulness: 15.0/15
- C1.1 Object coverage: **yes** — weighted coverage 92%. All critical objects present with write operations; tasks read-only and properties update-only are the only reductions. [spec paths; live reads 2026-08-25]
- C1.2 Core operational actions: **yes** (borderline; documentation-graded) — weighted coverage 85%. Create/update for contacts, deals, processes, custom fields, communications; properties update-only; tasks not writable. [`POST/PUT /contacts`, `/deals`, `/processes`; `POST /custom_fields`, `/notes`, `/calls`; `PATCH /conversations/{id}`]
- C1.3 Delete or lifecycle actions: **yes** (documentation-graded) — weighted coverage 89%. Stage transitions, close, reassign, tag changes, webhook deletion; no record delete/archive, no direct task completion. [`PUT /deals/{id}`, `PUT /processes/{id}`, `PATCH /conversations/{id}`, `DELETE /webhook_subscriptions/{id}`]
- C1.4 Change notification: **yes** — documented webhooks cover the critical + important state changes (deal/process created, stage/tag changes, reassigned; task; call; conversation), plus incremental polling (`updated_since`) proven live. [spec `event_name` enum; live 2026-08-25]

Score math: earned 4 of 4 applicable checks; unrounded fraction = 1.000; category points = 15.0/15; verification coverage = 100% (4/4).
What this means for you: You can build real tools on this API. You can read and change contacts, deals, and processes, and receive change events with webhooks. Two gaps remain: you cannot create or complete a task, and you cannot delete records, through the API.

## Category 2: API Design, Reliability, and Operability: 5.8/10
- C2.1 Modern API conventions: **yes** — resource-oriented REST, standard verbs, JSON, now OpenAPI 3.0.0. [new spec; live calls]
- C2.2 Consistent typing: **partial** — ids/timestamps/booleans/counts are clean, but monetary/decimal fields are JSON strings (`Deal.value`, `Deal.cost`, `Unit.market_rent`, `Unit.current_rent`, `Unit.estimated_rent`, `amount_receivable`). [new spec schema types; live 2026-08-25]
- C2.3 Structured errors: **partial** — structured JSON with correct HTTP status and message, but no populated stable machine code, and the shape varies (string vs. array). [live errors 2026-08-25; spec `Errors_Authorization/NotFound/Validation`]
- C2.4 Duplicate prevention: **partial** (documentation-graded) — deal creation has de-duplication (`accept_duplicates`), but no general idempotency-key for other writes. [spec `POST /deals`; `idempoten`=0]
- C2.5 Graceful handling under load: **yes** — documented and live rate-limit headers (`X-RateLimit-*`, `X-RateLimit-Retry-After`); 429 behavior evidenced; the new spec documents rate-limit responses per operation. [spec; live headers 2026-08-25]
- C2.6 Pagination for large collections: **partial** — offset pagination (`page`/`per_page`, cap 200) with a `meta` total_count/total_pages signal, but no stable-ordering guarantee and no cursor. [spec params; live `meta` 2026-08-25]
- C2.7 Bulk or incremental export: **partial** — incremental sync via `updated_since` + pagination on most list endpoints, but no dedicated bulk/export endpoint, and some resources lack `updated_since`. [spec; live filter test]
- C2.8 Webhook security and delivery reliability: **no** (documentation-graded) — webhooks exist (19 event types) but with no payload signature/HMAC, no retry policy, and no replay/idempotency guidance. [spec `webhook_subscriptions`; `signature`/`hmac`=0]
- C2.9 Concurrency and conflict control: **partial** — a weak read `ETag` is honored (`If-None-Match` → 304, confirmed live), but no `If-Match`-on-write and no 409 conflict semantics (409 absent from the spec). [live ETag/304 2026-08-25; new spec]
- C2.10 Versioning and backward compatibility: **partial** — a version is declared (`info.version 1.0.0`) and deprecations are signalled informally via `[Deprecated]` field markers, but there is no consumer-facing version identifier in the path (`/rest`, no `/v1`) or a header, and no documented backward-compatibility or deprecation-window policy. (Reconciled from an initial `no`: both independent runs marked this partial, and a declared version plus deprecation markers fit "versioning exists but thin/informal" better than "no versioning scheme.") [new spec `server:/rest`, `info.version:1.0.0`, 5 `deprecated` markers]
- C2.11 Request traceability: **partial** — every response carries `x-request-id` (confirmed live), but it is undocumented and not described as usable with support. [live headers 2026-08-25]
- C2.12 Service availability and status transparency: **yes** — public status page with 16 components including "REST API", 100% 90-day uptime and incident history. [status.leadsimple.com]

Score math: earned 7.0 of 12 applicable checks (yes×3 = 3.0; partial×8 = 4.0; no×1 = 0); unrounded fraction = 0.5833; category points = 5.833 → 5.8/10; verification coverage = 100% (12/12).
What this means for you: The API behaves well in many ways — live rate-limit counters, a request ID per response, and page totals for planning a sync. Weaknesses are unchanged: money fields are text not numbers, errors give a message but no fixed error code, webhooks have no signature or stated retry rule, and there is no clear API version policy.

## Category 3: Access Control and Safe Automation: 4.4/5
- C3.1 Read-only credentials: **yes** — the Create REST API key dialog has a "Read-only access" checkbox ("Read-only keys can retrieve data but cannot create, change, or delete it"). Previously the single key was full read/write (the existing default key is tagged "Read and write"). [operator-supplied API Keys screenshot, 2026-08-28]
- C3.2 Scoped credentials: **partial** — the create-key dialog offers only two access levels, "Read-only access" vs. "Read and write"; there is no per-resource or per-endpoint scoping (no option to limit a key to specific data such as contacts or a single pipeline). This is broad role-level scoping, not fine-grained. [operator-supplied API Keys screenshot, 2026-08-28 — the dialog shows only a key-name field and a read-only checkbox]
- C3.3 Multiple keys: **yes** — a "Create API key" button issues multiple distinct keys, each given a required name; the page states "use a separate key for each integration" and "you can revoke this key later without interrupting your other integrations." Previously one key per account. [operator-supplied API Keys screenshot, 2026-08-28]
- C3.4 Rotation and revocation: **yes** — each key exposes both "Rotate" and "Revoke" controls, self-serve; the page guidance says "revoke a key immediately if it's exposed." Previously rotate-only. [operator-supplied API Keys screenshot, 2026-08-28]
- C3.5 Test and production isolation: **N-A** — no sandbox / separate test environment exists.

Score math: earned 3.5 of 4 applicable checks (C3.5 N-A; yes×3 = 3.0; partial×1 = 0.5); unrounded fraction = 0.875; category points = 4.375 → 4.4/5; verification coverage = 100% (4/4).
What this means for you: This used to be the weakest area and is now much stronger. You can issue a read-only key for a reporting agent, create separate named keys per integration, and revoke any one key without breaking the others. The one remaining gap is fine-grained scoping: the key-creation screen offers only read-only vs. full read/write, so a key cannot be limited to specific data — which is why C3.2 is partial rather than yes.

## Category 4: Documentation and AI-Agent Readiness: 3.1/5
- C4.1 Complete self-serve reference: **yes** — a complete, **public** (no login) API reference at docs.leadsimple.com covering all operations, with a "Download OpenAPI Document" control and client-library request samples in Shell, Ruby, Node.js, PHP, and Python. Minor limitation: response samples are schema-generated (the spec carries 0 curated example values). [docs.leadsimple.com, observed 2026-08-28]
- C4.2 Reliable machine-consumable integration path: **yes** — a complete, published, **public** OpenAPI 3.0.0 specification (59 paths / 72 operations) at docs.leadsimple.com/openapi.json, suitable for code and tool generation (upgraded from the prior auth-gated 2.0 spec). [frozen `evidence/leadsimple-openapi-3.0-2026-08-28.json`]
- C4.3 AI-readable documentation: **no** — no `llms.txt`/`llms-full.txt` or Markdown corpus. Both `/llms.txt` and `/llms-full.txt` return 404 on the new docs, which are a reference-only SPA. (The public OpenAPI is credited under C4.2.) [404 probes 2026-08-28]
- C4.4 Kept current: **partial** — an active product changelog and in-spec `[Deprecated]` markers show maintenance, but there is no API-specific changelog, release notes, or deprecation policy on the reference site. [product.leadsimple.com; new spec `deprecated` markers]

Score math: earned 2.5 of 4 applicable checks (yes×2 = 2.0; partial×1 = 0.5; no×1 = 0); unrounded fraction = 0.625; category points = 3.125 → 3.1/5; verification coverage = 100% (4/4).
What this means for you: A developer or AI tool can now build against LeadSimple from public docs — a complete reference plus a public OpenAPI 3.0 file with request samples in five languages. Two gaps remain: no AI-ready `llms.txt` for the API, and no API-specific change log.

## Category 5: Accessibility and Cost: 15.0/15
- C5.1 Self-serve API key: **yes** — an account admin enables REST API access and creates keys self-serve in Settings; no Support needed. [Settings page 2026-08-25; operator report]
- C5.3 Not commercially gated: **yes** — the operator confirmed (2026-08-27) that the full REST API surface they use is available on their plan, not restricted to the top Platform tier. LeadSimple markets an "Enhanced API access — Platform" tier for higher rate limits, but the API and object surface are reachable on the operator's plan, and pricing gates no API rows per plan. [operator confirmation 2026-08-27; leadsimple.com/pricing]

Score math: earned 2.0 of 2 applicable checks (yes×2 = 2.0); unrounded fraction = 1.000; category points = 15.0/15; verification coverage = 100% (2/2).
What this means for you: Access is easy and not gated. You enable the API and create keys yourself, with no sales call, and the full REST API surface you need is included in your plan.

## Total
- Raw: 43.33 / 50 (15.000 + 5.833 + 4.375 + 3.125 + 15.000)
- Normalized before rounding: 86.67 / 100
- Published numeric score: 87 / 100
- Letter grade: B+
- Evidence tier: Baseline verified (read-path live 2026-08-25; write-path documentation-graded; Cat 3 from an operator-supplied screenshot; Cat 4 from public docs, both 2026-08-28)
- Overall verification coverage: 100% (25 of 25 applicable checks verified; C3.5 is N-A; no category Unable to verify; gate satisfied — overall ≥ 80%)
- Reproducibility: published after two independent grading runs against this frozen packet (see "Reproducibility" below). 25 of 27 checks were unanimous across all three runs; the two disagreements were resolved against the evidence, not averaged.
- Partial-result flag: yes — C2.4, C2.8, and the write portions of C1.2/C1.3 were graded from documentation because live write testing was declined (read-only). The Category 3 marks are backed by an operator-supplied screenshot of the API Keys page and the Create-key dialog (2026-08-28).
- Evaluator disagreements (resolved against the evidence during reconciliation):
  1. **C2.10 no → partial (resolved to partial).** This run initially marked no; both independent runs marked partial. A declared `info.version 1.0.0` plus `[Deprecated]` field markers fit "versioning exists but thin/informal" better than "no versioning scheme." This raised the published score from 86 to 87; a strict "no" holds it at 86 (B).
  2. **C4.1 yes vs. partial (resolved to yes).** One independent run marked partial because the response samples are schema-generated; two runs (including this one) marked yes — the reference is complete and public with real multi-language request samples and needs no reverse-engineering, the same standard applied to Buildium. A partial reading gives 85 (B).
  3. **C3.2 partial — resolved.** The operator-supplied Create-key screenshot shows only read-only vs. read-and-write, no per-resource scoping, so C3.2 = partial is confirmed.
  4. **C1.2 borderline at 0.85** (yes). A stricter reading (task-completion as a critical write) → Category 1 = 13.1/15 → ~83/100 (still B).
  Net: the three independent runs landed at 86 / 87 / 85 — a ±1 band, all B / B+; reconciled published = 87 (B+).

## Reproducibility (independent runs — methodology step 12)
Two independent graders scored this same frozen packet from scratch, each without seeing this run's marks or the other's. Across all three sets of 27 marks:
- Agreement: 25 of 27 checks were identical in all three runs — strong reproducibility.
- Disagreement 1 — C2.10 (versioning): this run initially `no`; both independent runs `partial`. Resolved to **partial** (a declared `info.version` + informal `[Deprecated]` markers is thin/informal versioning, not "none").
- Disagreement 2 — C4.1 (reference): two runs `yes`, one `partial` (over schema-generated vs. curated response samples). Resolved to **yes** (complete public reference with real request samples; the Buildium C4.1 standard).
- The highest-leverage check, C5.3 (commercial gating), was a unanimous **yes** across all three runs — settled by your plan confirmation — so the grade does not hinge on it.
- Published per run: 86 (this run) / 87 (A) / 85 (B). Reconciled published = **87 (B+)**; a stricter reading of either open call lands at 85–86 (B). The result is robustly B / B+.

## Bottom line for a property manager
LeadSimple's REST API has improved markedly. Under clean methodology v1.1 it now scores 87/100 (B+), up from 78 (C+), because LeadSimple fixed its two weakest areas: access control and documentation. You can now create multiple labeled API keys, make a key read-only, and revoke any key on its own — so you can hand a reporting agent a safe read-only key and cut off one integration without breaking the rest. The documentation is now public (docs.leadsimple.com) with a downloadable OpenAPI 3.0 file and request samples in five languages, so a developer or AI tool can build against it without a login. The remaining weaknesses are in reliability, not access: money fields come back as text, errors carry no stable machine code, webhooks have no signatures or retry policy, and there is no clear API version policy or AI-ready `llms.txt`. LeadSimple is not a bank and not your system of record; it sits on top of your PMS, so you still need your PMS (AppFolio, Buildium, and the like) for property, lease, ledger, and money data. This is a Baseline-verified result: reads were live-tested, the docs and spec were verified public today, and the new key controls were confirmed from your first-party screenshot of the API Keys screen.
