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
    "rentengine":        "rentengine-2026-09-03.md",
    "rentvine":          "rentvine-2026-09-02.md",
    "ringcentral":       "ringcentral-2026-09-01.md",
    "showmojo":          "showmojo-2026-09-02.md",
    "tenant-turner":     "tenant-turner-2026-09-01.md",
    "xero":              "xero-2026-08-27.md",
}

REDACT = [
    (r"cucPATSDM9kbS3xKg",                 "[account id withheld]"),
    (r"Dream Big Property Management",     "[operator account]"),
    (r"dreambig\.rentvine\.com",           "[account].rentvine.com"),
    (r"`dreambig`",                        "`[account]`"),
    (r"BANK-ENTERPRISE CLIENT TRUST MAIN", "[trust account name withheld]"),
]


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
        for pat, repl in REDACT:
            text, count = re.subn(pat, repl, text)
            if count:
                hits.append(f"{pat} x{count}")
        (DST / f"{slug}.md").write_text(text, encoding="utf-8")
        n += 1
        note = ("  redacted: " + ", ".join(hits)) if hits else ""
        print(f"  {slug:20} {len(text):>7,} bytes{note}")
    print(f"\nPublished {n} reports to {DST}/")


if __name__ == "__main__":
    main()
