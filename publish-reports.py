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
    "column":            "column-2026-09-02.md",
    "leadsimple":        "leadsimple-2026-08-28.md",
    "process-street":    "process-street-2026-08-31.md",
    "property-meld":     "property-meld-2026-09-01.md",
    "quickbooks-online": "quickbooks-online-2026-09-02.md",
    "quo":               "quo-2026-09-08.md",
    "rentengine":        "rentengine-2026-09-03.md",
    "rent-manager":      "rent-manager-2026-09-07.md",
    "rentvine":          "rentvine-2026-09-02.md",
    "ringcentral":       "ringcentral-2026-09-01.md",
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
        (DST / f"{slug}.md").write_text(text, encoding="utf-8")
        n += 1
        note = ("  redacted: " + ", ".join(hits)) if hits else ""
        if suppressed:
            note += f"  |  {suppressed} launch-scope passage(s) suppressed"
        print(f"  {slug:20} {len(text):>7,} bytes{note}")
    print(f"\nPublished {n} reports to {DST}/")


if __name__ == "__main__":
    main()
