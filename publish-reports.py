#!/usr/bin/env python3
"""
Copy the vendor grader reports into files/reports/ so each vendor page can offer
its own markdown for download.

Redaction: the reports were written against LIVE accounts and a few name them.
Both repos are public, so a small list of account identifiers is replaced on the
way out. This touches identifiers only. No mark, score, category, finding or
sentence of reasoning is altered, and every substitution made is printed so it
can be checked against the source.

Run after a new report lands:

    python3 publish-reports.py
"""
import re
from pathlib import Path

SRC = Path("../peterlohmann-website/grader-reports/reports")
DST = Path("files/reports")

# vendor slug -> the report file behind the PUBLISHED score. Kept in step with
# SOURCES in extract-checks.py; a superseded run must never be offered here.
SOURCES = {
    "appfolio":          "appfolio-2026-09-01.md",
    "aptly":             "aptly-2026-09-03.md",
    "boom":              "boom-2026-09-03.md",
    "buildium":          "buildium-2026-08-27.md",
    "column":            "column-2026-09-09.md",
    "latchel":           "latchel-2026-09-10.md",
    "leadsimple":        "leadsimple-2026-08-28.md",
    "magic-door":        "magic-door-2026-09-10.md",
    "process-street":    "process-street-2026-08-31.md",
    "property-meld":     "property-meld-2026-09-01.md",
    "quickbooks-online": "quickbooks-online-2026-09-02.md",
    "quo":               "quo-2026-09-08.md",
    "rentengine":        "rentengine-2026-09-03.md",
    "rent-manager":      "rent-manager-2026-09-07.md",
    "rentvine":          "rentvine-2026-09-02.md",
    "ringcentral":       "ringcentral-2026-09-01.md",
    "showdigs":          "showdigs-2026-09-10.md",
    "showmojo":          "showmojo-2026-09-02.md",
    "tenant-turner":     "tenant-turner-2026-09-01.md",
    "xero":              "xero-2026-08-27.md",
    "zoom":              "zoom-2026-09-08.md",
}

REDACT = [
    (r"cucPATSDM9kbS3xKg",                 "[account id withheld]"),
    (r"Dream Big Property Management",     "[operator account]"),
    (r"dreambig\.rentvine\.com",           "[account].rentvine.com"),
    (r"`dreambig`",                        "`[account]`"),
    (r"BANK-ENTERPRISE CLIENT TRUST MAIN", "[trust account name withheld]"),
]


# ---------------------------------------------------------------------------
# LAUNCH-SCOPE SUPPRESSION
#
# For the preview launch, published reports must not indicate that any vendor
# made changes or upgrades, or that any vendor saw an earlier grade. Two reports
# carried that framing. Removing it changes NO mark, score, category total or
# finding: only the before-and-after narration around them, and one manifest
# entry recording vendor correspondence.
#
# The archived reports under grader-reports/ are untouched and remain the record
# of what was submitted. This suppression is applied on the way out, here, so a
# rebuild cannot quietly reintroduce it.
#
# When re-scores resume and updates become publishable, delete this block.
# ---------------------------------------------------------------------------
SUPPRESS = {
    "leadsimple": [
        ("- Date run: 2026-08-28 (re-run after LeadSimple shipped access-control "
         "and documentation improvements)",
         "- Date run: 2026-08-28"),
        # the whole "what changed" section, opening line through its closing paragraph
        (r"- \*\*What changed since the 2026-08-27 run.*?This run supersedes the "
         r"2026-08-27 re-score\.\n", "", "regex"),
        (' Previously the single key was full read/write (the existing default key '
         'is tagged "Read and write").', ""),
        (" Previously one key per account.", ""),
        (" Previously rotate-only.", ""),
        ("This used to be the weakest area and is now much stronger. ", ""),
        ("LeadSimple's REST API has improved markedly. Under clean methodology v1.1 "
         "it now scores 87/100 (B+), up from 78 (C+), because LeadSimple fixed its "
         "two weakest areas: access control and documentation. You can now create",
         "Under clean methodology v1.1, LeadSimple's REST API scores 87/100 (B+). "
         "You can create"),
    ],
    "rentengine": [
        ('- Operator-supplied vendor communication: "Response to API Report Card '
         'v1.1" (PDF, 4 pages, received 2026-09-03)\n', ""),
        (r"\n\*\*Use of the vendor communication:\*\*.*?live observation\.\n", "", "regex"),
        (" The vendor states these are built and due to ship by 2 pm on 2026-09-03; "
         "they were not in production when this packet was frozen and are therefore "
         "not credited.", ""),
    ],
}


# ---------------------------------------------------------------------------
# PUBLISHED CORRECTIONS
#
# Applied on the way out, like SUPPRESS, so a rebuild cannot revert them. Each
# rule must match or the build aborts.
#
# Boom C5.3, corrected 2026-09-09. The run marked "not commercially gated" as
# partial while its own text established that no gate exists, withholding a pass
# because Boom publishes no pricing. The methodology does not ask for published
# pricing: C5.3 awards yes "when included or free", partial "when some meaningful
# capabilities are tier-gated", no "when the API requires a premium plan". No
# tier-gating was found. The one genuine gap, that the account owner could not
# confirm whether their access carried a fee, has since been answered by the
# operator: they were not charged extra, so access was included. Run 1 originally
# marked this yes; the correction restores that mark.
#
# Nothing else in the run changes. All other marks, the evidence and the findings
# stand; only the figures derived from C5.3 move.
# ---------------------------------------------------------------------------
CORRECTIONS = {
    "aptly": [
        # Aptly C5.3 language, corrected 2026-09-09. The run reported that Aptly
        # publishes no plan tiers or prices. It does: getaptly.com/pricing shows
        # Essential, Premium and Enterprise with prices, and lists "Access to
        # Aptly API" as a Premium feature. That does not change the mark, which
        # rests on the Help Center's Premium requirement; the pricing page
        # independently confirms it. Verified against the live page 2026-09-09.
        ("# API Report Card: Aptly",
         "> **Correction, 2026-09-09.** This report stated that Aptly publishes no\n"
         "> plan tiers or prices. That was wrong. getaptly.com/pricing publishes three\n"
         "> tiers, Essential, Premium and Enterprise, with prices, and lists \"Access to\n"
         "> Aptly API\" as a Premium plan feature. The language below is corrected.\n"
         "> **The score is unchanged at 58 (F).** C5.3 was never scored on the pricing\n"
         "> page: it rests on Aptly's Help Center stating the API requires a Premium\n"
         "> Subscription, which the pricing page now independently corroborates.\n\n"
         "# API Report Card: Aptly"),
        ("- https://www.getaptly.com/pricing \u2014 no published plan tiers; demo-gated pricing",
         "- https://www.getaptly.com/pricing \u2014 three published tiers (Essential, "
         "Premium, Enterprise) with prices; \"Access to Aptly API\" listed as a Premium "
         "plan feature [rechecked live 2026-09-09]"),
        ('Aggravating rather than mitigating: Aptly publishes no plan tiers or prices at all \u2014 https://www.getaptly.com/pricing carries only "Book a demo to get custom pricing for your portfolio" \u2014 so an operator cannot determine the cost of API entitlement without a sales conversation.',
         'Corroborated by the pricing page: https://www.getaptly.com/pricing publishes '
         'three named tiers \u2014 Essential, Premium and Enterprise \u2014 with prices, and '
         'lists "Access to Aptly API" as a Premium plan feature and "Enterprise API" '
         'under Enterprise. That independently confirms the Help Center\'s Premium '
         'requirement, so an operator can both see the gate and price it '
         '[rechecked live 2026-09-09].'),
    ],
    "boom": [
        # 1. dated notice at the top, so a reader knows this differs from the run as first reconciled
        ("# API Report Card: Boom",
         "> **Correction, 2026-09-09.** C5.3 (not commercially gated) was published\n"
         "> as *partial* and has been corrected to *yes*. The check asks whether API\n"
         "> access is included or free, not whether pricing is published; the run found\n"
         "> no tier gating, and the account owner has since confirmed they were not\n"
         "> charged extra for API access. Run 1 marked this yes originally. The\n"
         "> published score moves from **64 (D)** to **71 (C-)**. No other mark,\n"
         "> finding or piece of evidence changed. Figures below that derive from C5.3\n"
         "> have been recomputed; the archived report retains the original.\n\n"
         "# API Report Card: Boom"),
        # 2. evidence-amendment log
        ("Run 1 set yes; **reduced to partial in reconciliation**.",
         "Run 1 set yes; reduced to partial in reconciliation, then **restored to yes "
         "by the 2026-09-09 correction**."),
        # 3-5. the check, its category heading and its score math
        ("## Category 5: Accessibility and Cost: 11.3/15",
         "## Category 5: Accessibility and Cost: 15.0/15"),
        ("- C5.3 Not commercially gated: partial \u2014 no evidence of a premium-plan gate exists:",
         "- C5.3 Not commercially gated: yes \u2014 no evidence of a premium-plan gate exists:"),
        ('**Exact limitation:** "included or free" is not established either, and that is what *yes* requires. Boom publishes no pricing whatsoever \u2014 a 119-URL sitemap with no pricing page, `/pricing` returning 404, every pricing question routed to a sales Typeform ("for details about pricing, contact sales") \u2014 the documented key-generation route runs through a request form that "will be reviewed", and the account owner cannot confirm whether their own access carried a plan upgrade or fee and has an open question with Boom.',
         '**Recorded for transparency, not scored against the check:** Boom publishes no pricing \u2014 a 119-URL sitemap with no pricing page, `/pricing` returning 404, every pricing question routed to a sales Typeform \u2014 so an operator cannot learn the cost without contacting sales. That is an opacity problem, not a commercial gate, and C5.3 asks only whether access is included or free. The account owner has confirmed they were not charged extra for API access.'),
        ("Score math: earned 1.5 of 2 applicable checks; unrounded fraction = 0.7500; category points = 0.7500 \u00d7 15 = **11.25/15**, displayed **11.3/15**;",
         "Score math: earned 2.0 of 2 applicable checks; unrounded fraction = 1.0000; category points = 1.0000 \u00d7 15 = **15.0/15**;"),
        # 6. totals
        ("- Raw: **31.875 / 50**", "- Raw: **35.625 / 50**"),
        ("- Normalized before rounding: **63.75 / 100**", "- Normalized before rounding: **71.25 / 100**"),
        ("- Published numeric score: **64 / 100**", "- Published numeric score: **71 / 100**"),
        ("- Letter grade: **D**", "- Letter grade: **C-**"),
        # 7. sensitivity table, recomputed from the corrected baseline
        ("| *Published result* \u2014 lease lifecycle 0.5, C2.11 partial, C2.6 partial, C4.4 yes | reconciled | 64 | D |",
         "| *Published result* \u2014 lease lifecycle 0.5, C2.11 partial, C2.6 partial, C4.4 yes | reconciled | 71 | C- |"),
        ("| run 2 | 56 | F |", "| run 2 | 64 | D |"),
        ("| run 2 | 63 | D |", "| run 2 | 70 | C- |"),
        ("| run 3 | 65 | D |", "| run 3 | 72 | C- |"),
        ("| run 3 | 63 | D |", "| run 3 | 70 | C- |"),
        # 8. reconciliation mark table and run totals
        ("| C5.3 | **yes** | partial | partial | **partial** |",
         "| C5.3 | **yes** | partial | partial | **yes** (corrected 2026-09-09) |"),
        ("| **Resolved** | each split settled against the frozen evidence | **31.875** | **63.75** | **64** | **D** |",
         "| **Resolved** | each split settled against the frozen evidence, C5.3 corrected 2026-09-09 | **35.625** | **71.25** | **71** | **C-** |"),
        # 9. the resolution paragraph and the outlier count that depended on it
        ('- **C5.3 \u2192 partial.** Run 1 read the absence of any tier-gating statement as evidence of inclusion. That is the "never reward opacity" trap: Boom publishes no pricing at all, so "included or free" is not established, merely not contradicted. The account owner\'s own uncertainty about whether their access carried a fee is direct evidence that entitlement is unsettled.',
         '- **C5.3 \u2192 yes (corrected 2026-09-09).** Reconciliation moved run 1\u2019s yes to partial on a "never reward opacity" argument: Boom publishes no pricing, so inclusion was not established, merely not contradicted. That reasoning does not track the check, which asks whether access is included or free rather than whether pricing is published, and no tier gating was found. The account owner has since confirmed they were not charged extra. Run 1\u2019s original mark is restored.'),
        ("Run 1 was the outlier on four of six splits and was corrected on all four, all in the same direction",
         "Run 1 was the outlier on four of six splits and was corrected on three of them, all in the same direction"),
        # 10. bottom line
        ("A score of 64 reflects a narrow API", "A score of 71 reflects a narrow API"),
    ],
}


def main():
    if not SRC.is_dir():
        raise SystemExit(f"source reports not found: {SRC.resolve()}")
    DST.mkdir(parents=True, exist_ok=True)
    n = 0
    for slug, fname in sorted(SOURCES.items()):
        src = SRC / fname
        if not src.exists():
            print(f"  ! {slug}: missing {fname}")
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        hits = []
        suppressed = 0
        corrected = 0
        for pat, repl in REDACT:
            text, count = re.subn(pat, repl, text)
            if count:
                hits.append(f"{pat} x{count}")
        for rule in SUPPRESS.get(slug, []):
            find, repl = rule[0], rule[1]
            if len(rule) > 2 and rule[2] == "regex":
                text, count = re.subn(find, repl, text, flags=re.S)
            else:
                count = text.count(find)
                text = text.replace(find, repl)
            if not count:
                raise SystemExit(
                    f"{slug}: suppression rule matched nothing, so the report may "
                    f"have changed underneath it:\n  {find[:90]}")
            suppressed += count
        for find, repl in CORRECTIONS.get(slug, []):
            count = text.count(find)
            if not count:
                raise SystemExit(
                    f"{slug}: correction rule matched nothing, so the report may "
                    f"have changed underneath it:\n  {find[:90]}")
            text = text.replace(find, repl)
            corrected += count
        (DST / f"{slug}.md").write_text(text, encoding="utf-8")
        n += 1
        note = ("  redacted: " + ", ".join(hits)) if hits else ""
        if suppressed:
            note += f"  |  {suppressed} launch-scope passage(s) suppressed"
        if corrected:
            note += f"  |  {corrected} correction(s) applied"
        print(f"  {slug:20} {len(text):>7,} bytes{note}")
    print(f"\nPublished {n} reports to {DST}/")


if __name__ == "__main__":
    main()
