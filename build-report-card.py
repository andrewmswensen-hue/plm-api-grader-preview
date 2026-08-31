#!/usr/bin/env python3
"""
Builds the results table, the category jump pills, and the per-company detail
modals on index.html (the v1 "spreadsheet" layout).

WHY THIS EXISTS
    The scores appear in two places: the table cells and the pop-open modal.
    Hand-editing both is how they drift apart. This file is the single source of
    truth: edit DATA below, run `python3 build-report-card.py`, and both are
    rewritten from the same numbers.

TO ADD A NEW GRADED COMPANY
    Find it in CATEGORIES (the name must match exactly), then add an entry to
    RESULTS keyed by that same name. Re-run this script. That is the whole job.

    Each RESULTS entry needs:
      score / grade   the published 0-100 number and its letter
      cats            five (points, max, plain-English note) tuples, in order
      strengths       short bullets, the good news
      watch           short bullets, the things that cost you work
      bottom          one paragraph, the verdict a PM should read
      meta            run date, methodology version, model, evidence tier

HOUSE RULE
    No em dashes or en dashes anywhere in the copy. Commas, parens, hyphens,
    or split the sentence instead.
"""

import json, re, pathlib

HERE = pathlib.Path(__file__).parent
PAGE = HERE / "index.html"

# The five scoring categories, in table-column order, with their v1.2 maxima.
CAT_LABELS = [
    ("Functional Coverage",  15),
    ("Design &amp; Reliability", 10),
    ("Access Control",        5),
    ("Docs &amp; AI-Ready",       5),
    ("Access &amp; Cost",        15),
]

# ---------------------------------------------------------------------------
# THE LIST. Slug, display heading, and the companies in it.
# Source: Andrew's "PM Software List for API Grader" sheet.
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("pm-software",  "PM Software",
        ["AppFolio", "Buildium", "Rentvine", "Propertyware", "Rent Manager"]),
    ("listings",     "Listings, Applications &amp; Tenant Screening",
        ["Boom", "ShowMojo", "Tenant Turner", "RentEngine", "Rently"]),
    ("workflow",     "Workflow &amp; CRM",
        ["LeadSimple", "Aptly", "Process Street"]),
    ("maintenance",  "Maintenance",
        ["Property Meld", "Vendoroo", "Mason", "Latchel", "Lula"]),
    ("inspections",  "Inspections",
        ["zInspector", "ResidentInspect", "RentCheck", "HappyCo", "SnapInspect",
         "PropertyInspect"]),
    ("banks",        "Banks",
        ["Column", "Enterprise Bank"]),
    ("accounting",   "Corporate Accounting",
        ["Xero", "QuickBooks Online"]),
    ("deposits",     "Deposits",
        ["Obligo", "Lighthouse", "Rhino", "Jetty"]),
    ("phone",        "Phone",
        ["RingCentral", "LeadSimple Phone", "SimpleVOIP", "Zoom Phone", "OpenPhone"]),
]

# Short labels for the pills (the headings above are too long for a pill row).
PILL_LABELS = {
    "pm-software": "PM Software", "listings": "Listings &amp; Screening",
    "workflow": "Workflow &amp; CRM", "maintenance": "Maintenance",
    "inspections": "Inspections", "banks": "Banks",
    "accounting": "Corp Accounting", "deposits": "Deposits", "phone": "Phone",
}

# ---------------------------------------------------------------------------
# THE RESULTS. Only companies that have actually been graded appear here.
# ---------------------------------------------------------------------------
RESULTS = {

"Buildium": {
  "score": 78, "grade": "C+",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "38.75 / 50"},
  "cats": [
    (15, 15, "Reads and writes nearly everything the business runs on: properties, "
             "units, leases, tenants, ledgers, bank accounts, bills, tasks, and work "
             "orders. Nothing critical is missing, and 91 webhook event types push "
             "changes to you in near real time."),
    (7.5, 10, "Modern, well typed, paginated, versioned, and openly monitored. Four "
              "gaps need code on your side: error responses carry no stable machine "
              "code, there are no idempotency keys (so a retried payment can double "
              "post), there is no lock stopping two writes from overwriting each "
              "other, and the only per-request trace id is an AWS header rather than "
              "a Buildium one."),
    (5, 5, "A perfect score, and the best access control graded so far. Issue a "
           "read-only key for a reporting agent, scope a key to just the data an app "
           "needs, make one key per integration, and rotate or delete any of them "
           "yourself. A real sandbox exists and its keys cannot touch production."),
    (3.75, 5, "A developer or an AI tool can build against Buildium without "
              "reverse-engineering it. The reference is public and complete, the "
              "OpenAPI file drives code generation, and the changelog was current to "
              "nine days before the run. The gap is AI-native docs: no llms.txt, so "
              "an agent has to consume the OpenAPI file itself."),
    (7.5, 15, "One real barrier, and it is cost. Key creation is fully self-serve "
              "with no sales call, but the API is exclusive to the Premium plan at "
              "$400 a month. On Essential ($62) or Growth ($192) you cannot use it "
              "at all."),
  ],
  "strengths": [
    "The most complete object coverage of any API graded so far",
    "A real sandbox, with keys that cannot reach production data",
    "Read-only and per-resource scoped keys, self-serve",
    "91 webhook event types across 32 entities",
    "Changelog running monthly since 2020",
  ],
  "watch": [
    "Premium plan only, $400/month, so most operators are locked out",
    "No idempotency keys, so a retried payment can post twice",
    "Error responses never populate a machine-readable code",
    "No optimistic concurrency, so two writers can silently overwrite",
  ],
  "bottom": "Buildium's Open API is one of the most complete property management "
            "APIs you can build on today. It is a modern, well typed, versioned REST "
            "API with clear docs, a downloadable OpenAPI file, a sandbox, safe "
            "read-only keys, and a public status page. Its weak spots are all in "
            "money-safe automation: guard against double-posting a retried payment "
            "yourself, because the API will not. The biggest practical barrier is "
            "cost rather than capability, since the API is Premium-plan only. "
            "Buildium is not a bank, and moving money still depends on its ePay "
            "add-on and the underlying banks.",
},

"LeadSimple": {
  "score": 78, "grade": "C+",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "39.17 / 50"},
  "cats": [
    (15, 15, "You can build real tools on this. Read and change your main records, "
             "contacts, deals, and processes, and receive change events by webhook. "
             "Two gaps: you cannot create or complete a task through the API, and "
             "you cannot delete records through it."),
    (5.4, 10, "Good in places: live rate-limit counters on every response, a request "
              "id on each one, and page totals so you can plan a full sync. Weaker "
              "elsewhere: money fields come back as text rather than numbers, errors "
              "give a message but no fixed code, webhooks have no signature and no "
              "stated retry rule, and there is no API version policy at all."),
    (1.3, 5, "The weakest single score on the board. LeadSimple gives one API key "
             "for the whole account, and that key can read and change everything. "
             "No read-only key, no way to limit a key to certain data, and no "
             "separate keys per tool. You can rotate it yourself, but a leaked key "
             "puts the entire account at risk."),
    (2.5, 5, "Workable for a developer, with limits. There is a full OpenAPI file "
             "for code tools, but the reference sits behind a login rather than "
             "being public, there are no AI-ready docs for the API, and no "
             "API-specific changelog."),
    (15, 15, "Full marks. You enable the API and copy the key yourself with no sales "
             "call, and the REST surface you need is included in the plan rather "
             "than locked behind the top tier."),
  ],
  "strengths": [
    "Full coverage of contacts, deals, and processes, with webhooks",
    "Included in the plan, not gated to the top tier",
    "Self-serve key with no sales call",
    "Live rate-limit counters and a request id on every response",
  ],
  "watch": [
    "One all-powerful account key, with no read-only or scoped option",
    "Webhooks have no signature and no documented retry policy",
    "Money fields return as text, not numbers",
    "No API version or deprecation policy",
    "Docs require a login",
  ],
  "bottom": "LeadSimple gives you a real, useful REST API. You can read and change "
            "your core CRM and operations data, contacts, deals, processes, "
            "communications, custom fields, and reports, and get change events by "
            "webhook. Its two clear weaknesses are safe automation and "
            "documentation. There is exactly one account key, it can do everything, "
            "and you cannot narrow it, so guard and rotate it carefully. Access "
            "itself is a genuine strength: self-serve and included on the plan. "
            "LeadSimple is not your system of record, it sits on top of your PMS, so "
            "you still need AppFolio, Buildium, or the like for property, lease, and "
            "money data.",
},

"Property Meld": {
  "score": 72, "grade": "C-",
  "meta": {"run": "Aug 25, 2026", "method": "1.2", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "36.19 / 50"},
  # Originally run and published under methodology v2.0 (76/100, C). Re-scored
  # here under v1.2 from the same frozen evidence packet. Not one check mark was
  # changed; only the category weighting differs, exactly as the LeadSimple run
  # was re-scored from v2.0 to v1.1. See "rescored" below for the reader-facing
  # version of this note.
  "rescored": "Originally run on 2026-08-25 under methodology v2.0, which scored "
              "all five categories out of 10 and published 76 / 100 (C). Despite "
              "the higher number, v2.0 came before the current file: the line ran "
              "v2.0, then v1.1, then v1.2. This row re-scores the same evidence "
              "under v1.2, whose categories are weighted 15 / 10 / 5 / 5 / 15. No "
              "check mark was changed and the API was not re-tested; only the "
              "weighting differs. The score moves to 72 because Access Control and "
              "Documentation, where Property Meld is strongest, are now capped at 5 "
              "points each instead of 10. Two retired checks, free sandbox and "
              "onboarding friction, no longer score.",
  "cats": [
    (13.1, 15, "You can build the whole maintenance workflow: intake a work order, "
              "assign a vendor or technician, schedule it, complete it, and review "
              "it. The only coverage limit is change detection. There are no "
              "webhooks, so you poll for changes instead."),
    (6.8, 10, "Modern, well typed, idempotent, paginated, and transparent about "
              "uptime. The reliability gaps are real though: no protection against "
              "two writes overwriting each other, no bulk export, no Retry-After "
              "header, no documented request id for support, and error codes you "
              "cannot branch on."),
    (4.4, 5, "You can run several keys, revoke any of them yourself, and get a "
              "read-limited identity. Scoping is role-based rather than "
              "fine-grained, so you pick from set tiers rather than choosing "
              "exactly what a key can touch."),
    (4.4, 5, "Genuinely AI-friendly, and among the best documentation in this "
             "group. A public OpenAPI spec plus a real llms.txt corpus, with a "
              "Markdown twin of every page. The only weak signal is the changelog, "
              "which has two entries and has not been touched in about three years."),
    (7.5, 15, "Split decision on the two checks that count here. Key creation is "
              "self-serve in the app with no sales call, which is a real "
              "improvement. But the API is gated to the higher Ops plan rather than "
              "the cheaper Core plan, so you cannot reach it without paying up."),
  ],
  "strengths": [
    "Best-in-class AI-readable docs: llms.txt plus a Markdown twin per page",
    "Real idempotency keys on writes, with 24-hour retention",
    "Multiple keys, self-serve create and revoke",
    "Public status page showing 99.98% to 100% uptime",
  ],
  "watch": [
    "No webhooks at all, so you have to poll for every change",
    "No protection against two writes overwriting each other",
    "No free sandbox, so write testing happens against production",
    "Needs the higher Ops plan",
    "Changelog is about three years stale",
  ],
  "bottom": "Property Meld is a strong, genuinely AI-friendly build target for the "
            "full maintenance workflow, with idempotency keys, a public uptime page, "
            "and documentation as good as any here. The reliability gaps are "
            "real: no webhooks (you poll instead), no lost-update protection, no "
            "bulk export, and no support-usable request id. Access still costs the "
            "higher Ops plan with no free sandbox. Reads were live-tested, but write "
            "behavior is graded from documentation, because there is no sandbox to "
            "write against.",
},

"RentEngine": {
  "score": 74, "grade": "C",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "36.96 / 50"},
  "cats": [
    (11.3, 15, "You can build real leasing automation: sync leads, drive the "
               "pipeline, schedule showings, and manage units and listings. What you "
               "cannot do through the API is submit an application, run or read a "
               "screening decision, cancel a showing, or delete anything. "
               "Applications and prescreening are read-only, so RentEngine's own "
               "hosted flow stays the front door."),
    (4.6, 10, "The lowest Design and Reliability score in this group. It behaves "
              "predictably where you touch it most, with clean REST, honest "
              "rate-limit headers, and useful validation errors. But rent, bedrooms, "
              "and bathrooms are typed as strings in the contract (and the live data "
              "disagrees with the contract), there is no concurrency protection, "
              "most list endpoints give no has-more signal, and there is no status "
              "page at all."),
    (3.0, 5, "You can hand out several named keys and cut any of them off yourself "
             "in seconds, which is good. But you cannot issue a read-only or "
             "narrowly scoped key: every token inherits the full power of the user "
             "who created it, across all their accounts. Make a dedicated "
             "limited-permission user and mint the token from that."),
    (3.1, 5, "The reference is genuinely good and machine-ready. A downloadable "
             "OpenAPI 3.1 spec plus a docs MCP server means Claude Code can build "
             "against it quickly. The gap is currency: there is no changelog, so you "
             "get no warning when something changes."),
    (15, 15, "The strongest part of the card. Open API access is included for every "
             "RentEngine customer, and you can mint your own key without a sales "
             "call. Nothing forces a plan upgrade to build."),
  ],
  "strengths": [
    "API access included for every customer, no upgrade needed",
    "OpenAPI 3.1 spec plus a live docs MCP server for AI tools",
    "Seven webhook event types covering the mutable objects",
    "Write path was verified with real controlled live testing",
  ],
  "watch": [
    "Rent, bedrooms, and bathrooms are typed as strings, and live data disagrees",
    "No read-only or scoped keys: every token inherits full user power",
    "No delete and no showing cancel; applications and screening are read-only",
    "No status page and no changelog",
  ],
  "bottom": "RentEngine has a real, modern, self-serve API, and access is its "
            "strongest feature. You can build genuine leasing automation today: sync "
            "prospects, drive the pipeline, schedule showings, and manage units and "
            "listings, with webhooks for changes. The limitations are that the API "
            "is read-only for applications and screening, there is no delete and no "
            "cancel, and production hygiene is uneven. Build defensive parsing and "
            "your own retry safety net. It is a leasing and CRM layer, not a PMS, so "
            "you still run your PMS as the system of record.",
},

"Xero": {
  "score": 80, "grade": "B-",
  "meta": {"run": "Aug 27, 2026", "method": "1.1", "model": "Claude Opus 4.8",
           "tier": "Baseline verified", "raw": "39.92 / 50"},
  "cats": [
    (13.1, 15, "You can read and change the accounting data your business runs on, "
               "post invoices and payments, and update contacts and accounts. What "
               "you cannot do is import bank statements or reconcile through the "
               "API; a partner bank feed or another tool does that. Plan to poll "
               "with the modified-since filter, because webhooks only cover a few "
               "record types."),
    (6.7, 10, "Stable and predictable to run in production. Rate limits, "
              "pagination, request tracing, and idempotency are all solid, and you "
              "can trace any request with support. Watch three things: dates arrive "
              "in two different formats, error shapes are not uniform, and there is "
              "no lost-update protection, so two writers can overwrite each other."),
    (4.5, 5, "A strong point. You can safely give an app or an AI agent a limited, "
             "read-only key, and cut off access at any time. The one gap is testing: "
             "there is no true sandbox, you develop against a Demo Company, which is "
             "a separate data set but not a separate environment or key."),
    (4.4, 5, "Among the best documentation in this group. A developer or an AI "
             "coding tool can build against Xero without reverse-engineering. The "
             "reference is complete, the OpenAPI spec and six official SDKs are "
             "current, and Xero ships an official MCP server for AI agents. The only "
             "soft spot is no llms.txt-style bundle."),
    (11.3, 15, "You can get in the door today for free and connect your own "
               "organization at no cost beyond your Xero subscription. Costs appear "
               "only when you scale: higher call volumes, more connections, or the "
               "hands-off machine-to-machine key all move you to a paid tier."),
  ],
  "strengths": [
    "Highest score graded so far, and the only B so far",
    "Granular read/write scopes, verified enforced in live testing",
    "Six official SDKs plus an official MCP server for AI agents",
    "First-class idempotency keys on writes",
    "A correlation id on every response that support can actually use",
  ],
  "watch": [
    "Not property management software: no properties, units, leases, or work orders",
    "No bank statement import or reconciliation through the API",
    "Webhooks cover only four record types, so you poll for the rest",
    "Dates come back in two different formats",
    "No true sandbox, only a Demo Company",
  ],
  "bottom": "Xero has a strong, mature accounting API. You can build your own tools "
            "and AI agents on top of your general ledger, with good rate limits, "
            "pagination, tracing, and read-only keys you can revoke. The biggest API "
            "limits are no bank statement import or reconciliation, webhooks for "
            "only a few record types, and no lost-update protection. The biggest fit "
            "limit is that Xero is general accounting, not property management: no "
            "native properties, units, leases, or work orders, and no first-party "
            "trust or security deposit workflows. Treat Xero as an excellent "
            "accounting backend to connect to, not a replacement for a PMS, a bank, "
            "or a trust accounting system.",
},

}

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def grade_class(g):
    return "grade-" + g[0].lower() if g else "grade-none"

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def fmt_pts(v):
    """15.0 -> 15, 7.5 -> 7.5. Keeps the table from reading like a spreadsheet."""
    return str(int(v)) if float(v) == int(v) else str(v)


def build_pills():
    out = ['<div class="pill-row" aria-label="Jump to a category">']
    for s, _, _ in CATEGORIES:
        out.append(f'<a class="jump-pill" href="#cat-{s}">{PILL_LABELS[s]}</a>')
    out.append("</div>")
    return "\n        ".join(out)


def build_rows():
    rows = []
    for s, heading, companies in CATEGORIES:
        rows.append(
            f'<tr class="grp" id="cat-{s}"><td colspan="8">{heading}'
            f'<span class="grp-n">{len(companies)} listed</span></td></tr>'
        )
        for co in companies:
            r = RESULTS.get(co)
            if not r:
                cells = '<td class="num"><span class="cat-none">&ndash;</span></td>' * 5
                rows.append(
                    f'<tr><td class="plat"><span class="co-name">{co}</span></td>'
                    f'{cells}'
                    f'<td class="num"><span class="cat-none">&ndash;</span></td>'
                    f'<td class="num"><span class="grade grade-none">&ndash;</span></td></tr>'
                )
                continue

            if r.get("legacy"):
                # Subscores are on a different scale, so showing them in these
                # columns would invite a false comparison. Flag instead.
                cells = ('<td class="num" colspan="5"><span class="cat-legacy">'
                         'graded on the older v2.0 scale, see details</span></td>')
            else:
                cells = "".join(
                    f'<td class="num"><span class="cat-score">{fmt_pts(p)}</span></td>'
                    for p, _, _ in r["cats"]
                )
            flag = ' <span class="row-flag">v2.0</span>' if r.get("legacy") else ""
            rows.append(
                f'<tr class="has-detail" data-co="{slug(co)}">'
                f'<td class="plat"><button class="co-btn" type="button">'
                f'<span class="co-name">{co}</span>{flag}'
                f'<span class="co-hint">Click for details</span></button></td>'
                f'{cells}'
                f'<td class="num"><span class="cat-total">{r["score"]}</span></td>'
                f'<td class="num"><span class="grade {grade_class(r["grade"])}">'
                f'{r["grade"]}</span></td></tr>'
            )
    return "\n            ".join(rows)


def build_stats():
    graded = [r for r in RESULTS.values()]
    listed = sum(len(c) for _, _, c in CATEGORIES)
    avg = round(sum(r["score"] for r in graded) / len(graded)) if graded else "&ndash;"
    best = max(graded, key=lambda r: r["score"]) if graded else None
    best_txt = f'{best["grade"]}' if best else "&ndash;"
    best_who = next((n for n, r in RESULTS.items() if r is best), "")
    return (
        '<div class="stats stats-color g4" aria-label="At a glance">'
        f'<div class="stat"><div class="v">{listed}</div><div class="k">Platforms listed</div></div>'
        f'<div class="stat"><div class="v">{len(graded)}</div><div class="k">Graded so far</div></div>'
        f'<div class="stat"><div class="v">{avg}</div><div class="k">Average score</div></div>'
        f'<div class="stat"><div class="v">{best_txt}</div><div class="k">Highest grade ({best_who})</div></div>'
        '</div>'
    )


def build_data():
    """The JSON the modal renders from. Same numbers as the table, by construction."""
    out = {}
    for name, r in RESULTS.items():
        maxima = r["legacy"]["maxima"] if r.get("legacy") else [m for _, m in CAT_LABELS]
        cat = next(h for _, h, cos in CATEGORIES if name in cos)
        out[slug(name)] = {
            "n": name, "cat": re.sub("&amp;", "&", cat),
            "s": r["score"], "g": r["grade"], "gc": grade_class(r["grade"]),
            "m": r["meta"],
            "c": [{"l": re.sub("&amp;", "&", CAT_LABELS[i][0]),
                   "p": fmt_pts(p), "x": maxima[i],
                   "pct": round(float(p) / maxima[i] * 100),
                   "t": t}
                  for i, (p, _, t) in enumerate(r["cats"])],
            "st": r["strengths"], "w": r["watch"], "b": r["bottom"],
            "lg": r["legacy"]["note"] if r.get("legacy") else None,
            "rs": r.get("rescored"),
        }
    return json.dumps(out, separators=(",", ":"), ensure_ascii=False)


BANDS = [(97,"A+"),(93,"A"),(90,"A-"),(87,"B+"),(83,"B"),(80,"B-"),
         (77,"C+"),(73,"C"),(70,"C-"),(67,"D+"),(63,"D"),(60,"D-"),(0,"F")]


def check_math():
    """Every row must add up, and its letter must match the published number.

    The category points, the headline score, and the grade are three separate
    fields that a careless edit can knock out of step. This recomputes the score
    from the parts and re-derives the letter from the v1.2 bands, and refuses to
    build if either disagrees. Rounding tolerance is one point, because the
    displayed category points are rounded to one decimal.
    """
    for name, r in RESULTS.items():
        maxima = r["legacy"]["maxima"] if r.get("legacy") else [m for _, m in CAT_LABELS]
        raw = sum(float(p) for p, _, _ in r["cats"])
        got = raw / sum(maxima) * 100
        if abs(got - r["score"]) > 1.0:
            raise SystemExit(
                f"{name}: categories sum to {raw:.2f}/{sum(maxima)} = {got:.1f}, "
                f"but the published score is {r['score']}")
        letter = next(g for lo, g in BANDS if r["score"] >= lo)
        if letter != r["grade"]:
            raise SystemExit(
                f"{name}: {r['score']}/100 is {letter} under the v1.2 bands, "
                f"but the grade is set to {r['grade']}")
        print(f"  ok  {name:15} {raw:5.2f}/{sum(maxima)} -> {r['score']} {r['grade']}")


def main():
    check_math()
    html = PAGE.read_text(encoding="utf-8")

    results_block = f"""      {build_stats()}
      <p class="sub" style="margin-top:16px;font-size:14px;">Scores are point-in-time and tied to the evidence access date. Methodology v1.2.</p>

      <h2 class="h-lead" style="margin-top:46px;">The results.</h2>
      <p class="sub" style="margin:10px 0 18px;">Scores are point-in-time, based on first-party documentation and, where available, live testing. Click any graded platform for the full breakdown.</p>

        {build_pills()}

      <p class="tbl-hint">Scroll the table sideways to see every category &rarr;</p>
      <div class="table-scroll">
        <table class="rank-table">
          <thead>
            <tr>
              <th>Platform</th>
{chr(10).join(f'              <th class="num col-cat">{l}<span class="th-max">/{m}</span></th>' for l, m in CAT_LABELS)}
              <th class="num">Score</th>
              <th class="num">Grade</th>
            </tr>
          </thead>
          <tbody>
            {build_rows()}
          </tbody>
        </table>
      </div>"""

    html = re.sub(
        r"(<!-- RESULTS:START -->\n).*?(\s*<!-- RESULTS:END -->)",
        lambda m: m.group(1) + results_block + m.group(2),
        html, flags=re.S,
    )

    html = re.sub(
        r"(<!-- DATA:START -->\n).*?(\s*<!-- DATA:END -->)",
        lambda m: (m.group(1)
                   + '<script type="application/json" id="coData">'
                   + build_data() + "</script>" + m.group(2)),
        html, flags=re.S,
    )

    PAGE.write_text(html, encoding="utf-8")
    print(f"Wrote {PAGE}")
    print(f"  {sum(len(c) for _,_,c in CATEGORIES)} companies in "
          f"{len(CATEGORIES)} categories, {len(RESULTS)} graded")


if __name__ == "__main__":
    main()
