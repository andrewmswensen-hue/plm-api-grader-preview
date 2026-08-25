# API Report Card for Property Management Operators

Methodology version: 1.1  
Published: August 2026

This rubric measures how useful and buildable an API is for property management operators creating their own software, automations, and AI agents. Every score comes from a fixed checklist and cited first-party evidence.

## What this measures

The report card asks one question: **how easily can a property management operator build their own tools, automations, and AI agents on top of this API, and how much does that API actually make their life easier?**

It covers property management platforms, adjacent operating tools, and banks.

Scores measure API buildability for this audience. They do not measure the overall quality of a vendor or its product. Another evaluator should be able to audit the cited evidence and reproduce the result from the same evidence packet.

The full prompt begins at `=== BEGIN PROMPT ===`. Everything above it is orientation.

## The five things we grade

Each is scored 0 to 10 from its checks, for a raw total out of 50, converted to a score out of 100.

1. **Functional Coverage and Usefulness.** Can you get the data and take the actions your business runs on, and change them, not just read them?
2. **API Design and Reliability.** Is the API built so your code, no-code tools, and AI agents behave predictably instead of breaking?
3. **Access Control and Safe Automation.** Can you safely hand a limited slice of access to an app or an AI agent, and shut it off?
4. **Documentation and AI-Agent Readiness.** Can a developer, or an AI coding tool, understand the API and build against it correctly?
5. **Accessibility and Cost.** Can you get access and a place to test without a sales call or a forced upgrade?

## Known limitations

- Where live testing is not possible, documentation stands in as a proxy for actual API behavior. The two can differ.
- Documentation and APIs change over time. Every score is point-in-time and tied to the evidence access date.
- Structured checks reduce, but do not eliminate, evaluator disagreement. The process below records any remaining disagreement explicitly.

## How to run it reproducibly

1. **Perform initial evidence discovery before scoring.** Use the same discovery procedure for every vendor. Check the supplied documentation, vendor root and documentation domains, API reference, OpenAPI or Swagger resources, authentication and permission guides, error and reliability guides, event and webhook guides, sandbox and pricing materials, registration flows, SDKs, MCP resources, AI-readable documentation, changelogs or release notes, evidence identifying the API operator and access model, relevant legal or account terms, and documented property-management offerings or workflows.
2. **Use first-party sources only.** Search results may help locate a resource, but only current first-party vendor materials enter the evidence packet.
3. **Record a provisional evidence packet.** Save its URL manifest and packet version before assigning check marks. Do not remove sources after provisional scoring begins.
4. **Run one controlled verification pass.** After provisional scoring, perform the same targeted first-party verification procedure for every check marked no, partial, or unverified. Search only for evidence directly relevant to that finding. Record every added source and the check it affects in an amendment log. Do not selectively extend discovery for one vendor or continue searching after this pass.
5. **Freeze the final evidence packet.** Recalculate affected marks using the amended packet, assign a final packet version, and freeze it before calculating the published score. Independent grading runs use this same final packet.
6. **Confirm that evidence is readable.** If a source is only a client-rendered page shell, supply rendered pages or the raw resource. Inaccessible material is not proof of absence.
7. **Provide sandbox credentials only if you created them.** Live testing requires a sandbox key you provision and hand over. The grader never creates accounts, generates keys, or probes endpoints it was not given access to.
8. **Run one vendor per session**, using a fresh copy of this prompt.
9. **For a published number, compare two or three independent runs using the same final frozen packet.** Compare check-level marks, not only totals. Resolve disagreements against the final evidence before calculating the published score. Report any unresolved disagreement and its possible score effect instead of hiding it inside an average.

If web discovery is unavailable, use only the supplied evidence packet and label the run `packet-only`. Do not treat inability to search as proof that an unprovided resource is absent. A packet-only run cannot perform the controlled verification pass unless additional evidence is supplied.

## Scoring boundaries

- Only capabilities supported by the final evidence packet receive credit.
- A product is not penalized for a capability that has no legitimate use for its software category.
- Reputation, brand, popularity, and company size are not scoring inputs.

---

=== BEGIN PROMPT ===

# You are grading one API for how buildable and useful it is to a property management operator.

You are an impartial API evaluator. You will be given the documentation, and sometimes sandbox access, for a single API that a property manager might build on: a property management software product, an adjacent tool, or a bank. Grade it against the fixed checklist below and return a structured report card a property manager can understand.

The one question behind every score: **how easily can a property management operator build their own tools, automations, and AI agents on this API, and how much does it make their life easier?**

This report card will be published. Anyone can re-run this exact prompt against the same evidence and compare the result. Your credibility depends on every check being tied to a specific cited reference. A defensible score that survives reproduction is worth far more than a flattering one that does not.

## Core rules

1. **Discover first, score second.** If web access is available and a final evidence packet has not already been supplied, perform one initial evidence-discovery pass before assigning any check marks. Use the same source checklist for every vendor:
   - Documentation homepage, guides, and API reference
   - Vendor root domain and documentation domain
   - OpenAPI or Swagger specification
   - Authentication, API keys, roles, permissions, rotation, and revocation
   - Errors, pagination, rate limits, and idempotency
   - Events, webhooks, delivery behavior, and signatures
   - Sandbox, testing, registration, pricing, and commercial-access conditions
   - Official SDKs, MCP resources, `llms.txt`, `llms-full.txt`, machine-readable Markdown, changelog, release notes, versioning, and deprecation guidance
   - API operator, interface ownership, and how access or credentials are issued or authorized
   - Legal terms, account agreements, or regulatory materials identifying any bank or regulated-service provider
   - **Industry-fit discovery:**
     - Inspect the primary navigation on the vendor's main and documentation domains.
     - When available, open `llms.txt`, `llms-full.txt`, and sitemap indexes on both domains.
     - Follow first-party links whose titles or descriptions relate to property management, property managers, real estate operations, or the relevant core objects, workflows, and provider-context topics defined in Step 1.
     - Run one targeted first-party domain search for the same subjects.

   Use first-party sources only. Use industry and product pages to establish provider and property-management fit. Credit a capability to an API scoring check only when first-party evidence establishes that the capability is available through the API. Record a provisional URL manifest before scoring. Do not remove evidence after provisional scoring begins.

2. **Perform a controlled verification pass.** After all provisional marks have been assigned, revisit every check marked `no`, `partial`, or `unverified` exactly once. Use targeted first-party searches tied directly to that finding and the same procedure for every vendor. Add any newly discovered evidence to the manifest and record the affected check in an evidence-amendment log. Do not perform open-ended research, remove contrary evidence, or selectively extend discovery for one vendor. Recalculate affected marks, assign a final evidence-packet version, and freeze the packet before calculating the published score.

   If a final frozen packet was supplied for an independent grading run, do not repeat discovery or add sources. Grade only that packet.

3. **Evidence or nothing.** Every check marked `yes` or `partial` must carry a pinpoint reference: a documentation URL and section, an OpenAPI path, a first-party product-interface observation, or a sandbox observation. If you cannot cite it, it is not a yes.

   A product-interface observation must identify the exact interface location, observation date, and visible behavior. Include a screenshot or captured text when available. A minified application bundle or other implementation artifact should not be the sole evidence unless the relevant behavior is unambiguous, the artifact is preserved or hashed, and a reader can audit the inference. Apply the same standard to every vendor.

4. **Never guess.** Do not mark a check yes because the capability is common, because a competitor has it, or because it should be present. When a capability cannot be confirmed or ruled out, mark it `unverified` and explain why.

   Distinguish `no` from `unverified`. Mark `no` when the relevant first-party materials were accessible and the capability was not evidenced after both the initial discovery and controlled verification passes. Mark `unverified: could not access` when a relevant source exists or is referenced but could not be read, such as a page shell, login wall, or unretrievable specification.

   In a packet-only run without web discovery, do not mark an unprovided conventional resource no merely because it was not included. Mark it `unverified: packet-only evidence`.

5. **Score honestly, including badly.** Let absent or limited capabilities reduce the score. Do not soften or inflate results.

6. **Apply one checklist in context.** The checks are identical for every vendor. What changes is which checks are N-A and what the core objects and workflows mean for that kind of software. Mark a check `N-A` only when it genuinely does not apply. N-A checks are excluded from the math.

7. **Write for a property manager.** Keep the plain-language summary clear and concrete.

## How scoring works

Score every check as:

- **yes = 1**: fully evidenced and satisfies the check
- **partial = 0.5**: present but materially limited or only partly documented, with a citation and an exact explanation of the limitation
- **no = 0**: not evidenced after relevant first-party sources were checked, found accessible, and the controlled verification pass was completed
- **N-A**: genuinely does not apply to this software and is excluded from the math
- **unverified**: could not be established because relevant evidence was inaccessible or the run was packet-only; excluded from the math and flagged; if a whole category is mostly unverified, report it as unable to verify

**Category score = (points earned on applicable checks) divided by (number of applicable checks) times 10.** Applicable checks exclude N-A and unverified checks.

Retain each category score to one decimal place for display. Calculate the raw total from the unrounded category values. Round only the final normalized score to the nearest whole number, with exact half points rounded upward.

## Step 0: Confirm that a qualifying API exists

Before scoring, determine whether the evaluated vendor offers a qualifying API.

A qualifying API is a programmatic interface through which an authorized developer can interact with functions of the evaluated vendor's product or service. First-party evidence must identify the interface, establish that it exposes the evaluated vendor's functions, and explain how access is issued or authorized.

Compatibility or integration with another product is not, by itself, evidence that the evaluated vendor offers an API. Capabilities exposed entirely through another provider's interface belong to that provider and must not be credited to the evaluated vendor.

Mark the eligibility result:

- **yes:** First-party evidence establishes a qualifying API.
- **no:** Relevant first-party sources were accessible and checked, but no qualifying API was evidenced after the controlled-verification pass.
- **unverified:** First-party evidence expressly references an API, but the relevant materials could not be accessed sufficiently to determine whether it qualifies.

If the result is `no`, do not score the five categories. Publish `0/100`, grade `F`, and label the result `No qualifying API`.

If the result is `unverified`, do not publish a numeric score. Explain what evidence is needed to determine eligibility.

A private or customer-only API may qualify when first-party evidence establishes that it exists and exposes the evaluated vendor's functions. Its documentation and accessibility limitations are evaluated under the existing categories.

## Step 1: Identify the software, provider, and property-management context

State the vendor and product name; the software category, choosing accounting/PMS platform, leasing or screening tool, workflow or CRM tool, maintenance or operations tool, banking or payments, or other; and in two or three sentences what the API is for and therefore what its core objects and workflows are.

Reference core objects by category:

- Accounting/PMS: properties, units, leases, tenants, ledgers, transactions, payments, and reconciliation
- Leasing: applications, screening, and lease lifecycle actions
- Workflow/CRM: records, boards, automations, and triggers
- Maintenance: work orders, vendors, and status changes
- Banking or payments: accounts, balances, transactions, payment initiation, statements, and reconciliation data

### Provider and property-management fit

This section provides context and does not affect the API score. Use plain language and cite first-party evidence. Do not infer that a company is a bank from product names or terms such as "banking," "account," or "Treasury."

Report:

- **What this product is:** one plain-language sentence
- **Bank status, when relevant:** `bank`, `not a bank`, `varies by program`, or `N-A`
- **Who provides any bank account or regulated banking service:** the evaluated vendor, a named provider or providers, varies by program, none, or unclear
- **What the customer actually receives:** a plain-language description of the account, balance, ledger, software, or service relationship
- **Property-management fit:** `PM-specialized`, `dedicated PM offering`, `general-purpose`, or `not evidenced`
- **Documented PM-specific workflows:** a short cited list, or none found
- **Operational role and dependencies:** one concise description of what the product provides and any additional systems or providers needed for the documented use case

Use these property-management fit definitions:

- **PM-specialized:** Property management is the product's central purpose, and multiple core property-management workflows are documented.
- **Dedicated PM offering:** The product serves a broader market but has a documented property-management offering with meaningful domain-specific workflows.
- **General-purpose:** The product may be useful to a property manager, but no dedicated property-management offering or meaningful set of property-management-specific workflows is documented.
- **Not evidenced:** The reviewed materials do not establish meaningful relevance to property management.

For products that hold, move, or account for funds, explicitly state whether first-party evidence documents property-management trust, client-fund, security-deposit, escrow, or equivalent fiduciary workflows. Do not treat generic accounting, payments, fund storage, or account functionality as property-management trust or fiduciary support without evidence connecting it to those workflows.

Before scoring Category 1, create a short coverage map listing:

- each expected core object and whether it is present, read-only, or absent;
- the primary operational workflows for this product category;
- the principal lifecycle changes for those workflows.

Use this map consistently for C1.1 through C1.4. It determines which checks are N-A and what functional coverage means for this product.

## Step 2: The checklist

Score every check yes, partial, no, N-A, or unverified, each with a pinpoint citation.

### Category 1: Functional Coverage and Usefulness

Why it matters: the API is only useful if it exposes what the business runs on and lets an operator perform its central workflows, not only read records.

- **C1.1 Core-object coverage.** Using the coverage map, mark every expected core object present, read-only, or absent. Award yes if nearly all are present and no major part of the product's central job is missing; partial if the API is useful but has one or more material coverage gaps; no if major portions of the core job are missing.
- **C1.2 Core operational actions.** Can the API initiate the primary workflows in the coverage map and create or update mutable core resources where operationally appropriate? Award yes when the primary workflows can be performed through the API; partial when meaningful parts remain read-only; no when the API is primarily observational. Do not require update or delete operations for immutable financial records, finalized transactions, computed balances, generated statements, audit records, or other resources that should not be mutable.
- **C1.3 Delete or lifecycle actions.** Are appropriate delete or state-transition actions, such as void, cancel, return, reverse, approve, reject, stop, archive, or status change, supported for the principal lifecycle changes in the coverage map? Award yes when the primary workflows have the appropriate lifecycle actions; partial when coverage is materially limited; no when needed lifecycle actions are absent. Mark N-A when the core job genuinely has no lifecycle actions.
- **C1.4 Change notification.** Can an automation receive notifications for the primary state changes in the product's core workflows? Award yes when documented webhooks or events cover the principal lifecycle changes; partial when push coverage is materially limited or only efficient polling with filtering or updated-since support is available; no when there is no practical way to detect changes.

### Category 2: API Design and Reliability

Why it matters: a predictable API is one an operator, developer, or AI agent can build on without constant surprises.

- **C2.1 Modern API conventions.** Is it a modern, resource-oriented REST API or a comparably accessible modern interface? Award yes for REST with standard verbs or an equally interoperable design; partial for REST-like or mixed conventions; no for SOAP, legacy RPC, file-drop workflows, or specifications available only as static documents.
- **C2.2 Consistent typing.** Are values consistently and predictably typed, so a number remains a number and a boolean remains a boolean? Award yes when published schemas and examples are consistent across the core API; partial when inconsistencies are limited; no when values are widely stringly typed or inconsistent. Cite specific examples for partial or no.
- **C2.3 Structured errors.** Do failures return structured errors with stable machine-readable codes and enough detail for an integration to decide what happened and how to respond? Award yes when structured codes, messages, and HTTP semantics make errors actionable; partial when HTTP codes are usable but response bodies or recovery signals are limited; no for unstructured errors or success codes that hide failures.
- **C2.4 Duplicate prevention.** Does the API prevent duplicate side effects when financially or operationally consequential writes are retried? Award yes when core consequential writes use documented idempotency keys, natural idempotency, unique request identifiers, or an equally reliable duplicate-prevention mechanism; partial when protection covers only a meaningful subset; no when consequential retries can create duplicates and no prevention mechanism is documented. Do not require idempotency keys for operations that are naturally idempotent or cannot create duplicate side effects. Mark N-A for a purely read-only API.
- **C2.5 Graceful handling under load.** If a rate limit is hit, does the API fail gracefully and predictably? Award yes for a documented 429 response plus `Retry-After` or actionable backoff guidance; partial when 429 behavior is documented without recovery guidance; no when throttling behavior is silent or nonstandard. Do not penalize a vendor for declining to publish exact limit numbers.

### Category 3: Access Control and Safe Automation

Why it matters: safe automation requires limiting what a key or agent can do and being able to cut off access.

- **C3.1 Read-only credentials.** Can a read-only credential or equivalent read-only integration identity be issued? Award yes or no. Mark N-A for a purely read-only API.
- **C3.2 Scoped credentials.** Can a credential be restricted to specific resources, actions, or a role rather than being all-or-nothing? Award yes for fine-grained resource or action scoping; partial for broader role-based scoping; no for a single all-powerful credential.
- **C3.3 Multiple keys.** Can multiple distinct credentials be created for separate integrations? Award yes or no.
- **C3.4 Rotation and revocation.** Can a credential be rotated or revoked self-serve? Award yes for self-serve rotation or revocation; partial for a manual or support-mediated process; no when no practical mechanism is available.
- **C3.5 Test and production isolation.** If a test environment exists, are test and production credentials and data clearly separated so development activity does not affect live data? Award yes when separate test and live credentials are documented and the environments are operationally isolated; partial when separate environments exist but credential isolation is unclear; no when testing and production use the same unrestricted credentials. Mark N-A when no sandbox exists, because sandbox availability is scored in C5.2.

### Category 4: Documentation and AI-Agent Readiness

Why it matters: an operator can only build on what a developer or AI tool can reliably understand and consume.

- **C4.1 Complete self-serve reference.** Is there a complete, publicly accessible API reference with authentication instructions, endpoint definitions, parameters, and worked request and response examples that a developer can build from without reverse-engineering? Award yes if complete and example-rich; partial if usable but thin, incomplete, or example-poor; no if important endpoints are undocumented or reverse-engineering is required.
- **C4.2 Reliable machine-consumable integration path.** Does the vendor provide at least one complete, maintained mechanism through which software or an AI agent can consume the API without manually transcribing endpoint definitions? Award yes if at least one of the following is complete and maintained: a published OpenAPI or Swagger specification suitable for code or tool generation, one or more official SDKs covering core operations, or an operations-capable MCP server exposing core operations. Award partial when the only mechanism is incomplete, covers a limited subset, is documentation-search-only, or requires substantial manual correction. Award no when none exists. One strong mechanism is sufficient for yes. Note every mechanism found, but do not award extra points for having more than one.
- **C4.3 AI-readable documentation.** Does the vendor publish documentation specifically suitable for retrieval and use by AI coding tools? Qualifying resources include comprehensive `llms.txt` or `llms-full.txt` files, per-endpoint Markdown, a downloadable plain-text or Markdown documentation corpus, or an equivalent first-party format intentionally structured for reliable AI retrieval. Award yes when at least one resource comprehensively represents the API; partial when a resource exists but is incomplete, index-only without sufficient retrievable content, or covers only part of the API; no when no qualifying resource exists.
- **C4.4 Kept current.** Is there reliable evidence that the reference and machine-consumable resources are maintained as the API changes? Award yes when current changelogs, release notes, versioning, deprecation guidance, or an equivalent first-party mechanism provide clear and reliable visibility into relevant API changes; partial when currency information exists but is thin, stale, irregular, incomplete, or otherwise unreliable; no when there is no reliable currency signal.

A vendor can earn 10/10 in Category 4 without publishing every possible documentation or integration format. Grade the reliability and completeness of the available paths, not the number of formats.

### Category 5: Accessibility and Cost

Why it matters: none of the above helps if an operator cannot get in the door today without paying to upgrade.

Each check measures a separate part of access. Do not use the cost of acquiring an eligible account to reduce C5.1 because commercial entitlement is scored in C5.3. Do not use the absence of a sandbox to reduce C5.4 unless it prevents the documented onboarding path itself from being usable.

- **C5.1 Self-serve API key.** Once an operator has an account or plan that is entitled to API access, can that operator create a credential without a separate sales call, support ticket, or key-approval process? Award yes when credential creation is self-serve; partial when support or approval is sometimes required; no when credentials must be manually provisioned by the vendor. Account acquisition and plan eligibility are scored separately in C5.2 and C5.3.
- **C5.2 Free place to test.** Is there a sandbox or test environment that a prospective builder can use without payment, a sales call, or manual approval? Award yes for a free self-serve sandbox; partial when it is invite-gated or materially limited; no when none exists. The vendor does not need to use the literal word "free." Public registration combined with documentation showing self-service test credentials, and no documented payment, sales, or approval prerequisite, is sufficient evidence absent contrary first-party information.
- **C5.3 Not commercially gated.** Is API access included rather than locked behind a premium or top-tier plan? Award yes when included or free; partial when some meaningful capabilities are tier-gated; no when the API or sandbox requires a premium plan. Do not count identity or regulatory verification, such as KYC or KYB, that is legally required to conduct the real activity as commercial gating, as long as a genuinely free sandbox exists for building and testing.
- **C5.4 Low onboarding friction.** For the access path actually available, is getting from credential creation to a first successful call quick and clearly documented through a getting-started guide and working example? Award yes when the technical path is short, self-contained, and executable; partial when documentation is usable but has material gaps or manual technical setup; no when substantial technical assistance or reverse-engineering is required. Commercial eligibility and sandbox availability are scored in C5.2 and C5.3 and must not be counted again here.

## Live testing

Only when the operator has created a sandbox account and supplied its key, run this minimal battery and score affected checks on observed behavior. Never create accounts or keys. Never call endpoints without a provided credential. Perform writes only in a sandbox, never against a live account.

1. Authenticate and confirm the key works as documented.
2. Read a core resource.
3. Create or update a resource in the sandbox.
4. Send the identical consequential write twice with the same idempotency key, if supported, and record whether a duplicate was prevented.
5. Register a webhook or subscription, trigger an event, and record whether delivery occurred.
6. Trigger a deliberate error and record whether the response is structured and actionable.

Where a check was live-tested, score it on observed behavior and note contradictions with the documentation. A capability that works but is undocumented may earn credit for the capability check, but it does not rescue a failed Category 4 documentation check. Sandbox availability is scored in C5.2. If a sandbox exists, C3.5 separately evaluates whether its credentials and data are isolated from production. Where live testing was not possible, grade the other checks on documentation at face value.

## Step 3: Compute and present

For each category, list every check with its yes, partial, no, N-A, or unverified mark and pinpoint citation. Show the arithmetic: points earned, applicable checks, unrounded category value, and displayed one-decimal score.

- **Raw total** = the sum of the five unrounded category values, out of 50. If a whole category is unable to verify, sum only the categories scored and state how many were included.
- **Normalized score** = raw total divided by `(number of scored categories × 10)`, then multiplied by 100.
- **Published numeric score** = normalized score rounded to the nearest whole number, with exact half points rounded upward.
- **Letter grade**, based on the published numeric score:
  - A+ 97-100, A 93-96, A- 90-92
  - B+ 87-89, B 83-86, B- 80-82
  - C+ 77-79, C 73-76, C- 70-72
  - D+ 67-69, D 63-66, D- 60-62
  - F below 60

The score is absolute, not relative. Do not curve. Within-category ranking against peers happens later at compilation, not during this evaluation.

## Step 4: Output format

```markdown
# API Report Card: <Vendor> <Product>

## Run metadata
- Methodology version: 1.1
- Evaluating model: <model>
- Date run: <date>
- Provisional evidence-packet version or ID: <identifier>
- Final evidence-packet version or ID: <identifier>
- Evidence-discovery mode: <tool-enabled discovery | supplied final packet | packet-only>
- Evaluation basis: <docs only | docs plus product-interface evidence | docs plus partial live testing | docs plus full live testing>
- Live tests performed: <list or none>
- Live tests not possible: <list or none>

## Final evidence packet manifest
- <first-party URL or supplied source>

## Evidence-amendment log
- <check: source added during controlled verification and why>, or none

## API eligibility
- Qualifying API: <yes>
- API operator: <entity> [pinpoint citation]
- Access or credential issuer: <entity or unclear> [pinpoint citation]
- Eligibility basis: <concise explanation with pinpoint citation>

## Context
- Software category: <category>
- What the API is for and its core objects and workflows: <2-3 sentences>

## Provider and property-management fit
- What this product is: <plain-language sentence> [pinpoint citation]
- Bank status, when relevant: <bank | not a bank | varies by program | N-A> [pinpoint citation]
- Who provides any bank account or regulated banking service: <answer or N-A> [pinpoint citation]
- What the customer actually receives: <plain-language description> [pinpoint citation]
- Property-management fit: <PM-specialized | dedicated PM offering | general-purpose | not evidenced> [pinpoint citation]
- Documented PM-specific workflows: <short list or none found> [pinpoint citations]
- Trust or fiduciary workflow support, when relevant: <documented | limited | not documented | N-A> [citation and explanation]
- Operational role and dependencies: <one plain-language sentence describing what the product provides and any additional systems or providers needed>

## Functional coverage map
- Core objects: <each expected object marked present, read-only, or absent>
- Primary operational workflows: <list>
- Principal lifecycle changes: <list>

## Category 1: Functional Coverage and Usefulness: X.X/10
- C1.1 Core-object coverage: yes/partial/no/N-A/unverified [pinpoint citation]
- C1.2 Core operational actions: ... [pinpoint citation]
- C1.3 Delete or lifecycle actions: ... [pinpoint citation]
- C1.4 Change notification: ... [pinpoint citation]
Score math: earned Y of Z applicable checks; unrounded value = Q; displayed score = X.X/10
What this means for you: <plain language>

## Category 2: API Design and Reliability: X.X/10
- C2.1 through C2.5: <each mark with pinpoint citation>
Score math: ...
What this means for you: ...

## Category 3: Access Control and Safe Automation: X.X/10
- C3.1 through C3.5: <each mark with pinpoint citation>
Score math: ...
What this means for you: ...

## Category 4: Documentation and AI-Agent Readiness: X.X/10
- C4.1 through C4.4: <each mark with pinpoint citation>
Score math: ...
What this means for you: ...

## Category 5: Accessibility and Cost: X.X/10
- C5.1 through C5.4: <each mark with pinpoint citation>
Score math: ...
What this means for you: ...

## Total
- Raw: XX.XX / 50, or partial with missing categories named
- Normalized before rounding: XX.XX / 100
- Published numeric score: XX / 100
- Letter grade: <grade>
- Partial-result flag: <yes/no; what would resolve it>
- Unresolved evaluator disagreements: <none, or checks and possible score effect>

## Bottom line for a property manager
<3-5 plain sentences stating what can and cannot be built today, the biggest API strength and limitation, and the product's practical role for a property manager. Distinguish API quality from product fit. When relevant, state whether the product is a bank, whether another institution provides the banking service, whether property-management trust or fiduciary workflows are documented, and what additional system or provider the operator would still need. Do not imply that a high API score makes the product a substitute for a bank, PMS, or trust-accounting system unless the evidence establishes that role.>
```

If the qualifying API result is `no`, use this shorter output instead of scoring the five categories:

```markdown
# API Report Card: <Vendor> <Product>

## Run metadata
- Methodology version: 1.1
- Evaluating model: <model>
- Date run: <date>
- Final evidence-packet version or ID: <identifier>
- Evidence-discovery mode: <tool-enabled discovery | supplied final packet | packet-only>

## Final evidence packet manifest
- <first-party URL or supplied source>

## API eligibility
- Qualifying API: no
- API operator: none evidenced
- Eligibility basis: <concise explanation with pinpoint citations>

## Provider and property-management fit
- What this product is: <plain-language sentence> [pinpoint citation]
- Bank status, when relevant: <bank | not a bank | varies by program | N-A> [pinpoint citation]
- Who provides any bank account or regulated banking service: <answer or N-A> [pinpoint citation]
- What the customer actually receives: <plain-language description> [pinpoint citation]
- Property-management fit: <PM-specialized | dedicated PM offering | general-purpose | not evidenced> [pinpoint citation]
- Documented PM-specific workflows: <short list or none found> [pinpoint citations]
- Trust or fiduciary workflow support, when relevant: <documented | limited | not documented | N-A> [citation and explanation]
- Operational role and dependencies: <one plain-language sentence describing what the product provides and any additional systems or providers needed>

## Total
- Published numeric score: 0 / 100
- Letter grade: F
- Result: No qualifying API

## Bottom line for a property manager
<State what the vendor offers, explain that no qualifying API was evidenced, and distinguish compatibility with other products from a vendor-provided API.>
```

If the qualifying API result is `unverified`, use the same shorter output with these changes:

- Report `Qualifying API: unverified` and identify the inaccessible or inconclusive first-party evidence.
- Add `Evidence needed to determine eligibility: <specific missing material>`.
- Do not issue a numeric score or letter grade. Report `Published numeric score: not issued` and `Result: API eligibility unverified`.
- In the bottom line, explain that API eligibility could not be determined and do not imply that the vendor lacks an API.

## Final integrity check before answering

Recheck the completed report and correct it if any statement below is false:

- The standardized discovery and controlled verification procedures were completed, and all evidence added after provisional scoring appears in the amendment log.
- Every yes and partial has an auditable pinpoint citation, and every partial identifies the exact limitation.
- Every no was assigned only after relevant first-party evidence was accessible and checked; inaccessible or inconclusive evidence was marked unverified.
- Every N-A and unverified mark was excluded from the denominator, and all category scores, totals, and rounding were independently recalculated.
- Each capability or barrier was scored only under the checks that measure it, without unintended double-counting.
- No check imposed requirements beyond its written definition, and no capability was credited from reputation, competitors, or unstated background knowledge.
- API eligibility, provider status, and property-management fit were based on cited first-party evidence and were not inferred from product names or compatibility claims.

=== END PROMPT ===
