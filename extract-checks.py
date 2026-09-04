#!/usr/bin/env python3
"""
Pull the per-check detail out of the grader markdown reports and freeze it into
data/checks.json, which build-report-card.py reads.

Why a separate step: the reports live in the OTHER repo under grader-reports/,
which is gitignored because both repos are public and the reports carry live
account details. Extraction runs on Andrew's machine only. What lands in git is
this script's OUTPUT, which is reviewed before it is committed. That also makes
the page build reproducible without the reports present.

Run it only when a new report arrives:

    python3 extract-checks.py

Nothing here scores anything. It copies marks and reasoning verbatim.
"""
import json, re, sys, unicodedata
from pathlib import Path

REPORTS = Path("../peterlohmann-website/grader-reports/reports")
OUT     = Path("data/checks.json")

# Company -> the report file that produced the PUBLISHED score. Kept explicit
# rather than inferred, so a superseded run can never leak onto the page.
SOURCES = {
    "AppFolio":          "appfolio-2026-09-01.md",
    "Aptly":             "aptly-2026-09-03.md",
    "Boom":              "boom-2026-09-03.md",
    "Buildium":          "buildium-2026-08-27.md",   # + reconciliation, below
    "Column":            "column-2026-09-02.md",
    "LeadSimple":        "leadsimple-2026-08-28.md",
    "Property Meld":     "property-meld-2026-09-01.md",
    "QuickBooks Online": "quickbooks-online-2026-09-02.md",
    "RentEngine":        "rentengine-2026-09-03.md",
    "Process Street":    "process-street-2026-08-31.md",
    "Rentvine":          "rentvine-2026-09-02.md",
    "RingCentral":       "ringcentral-2026-09-01.md",
    "ShowMojo":          "showmojo-2026-09-02.md",
    "Tenant Turner":     "tenant-turner-2026-09-01.md",
    "Xero":              "xero-2026-08-27.md",
}

# Live account identifiers that must never reach a public repo. Applied to the
# extracted TEXT only; no mark, score or finding is touched.
REDACTIONS = [
    (re.compile(r"cucPATSDM9kbS3xKg"), "[account id withheld]"),
    (re.compile(r"Dream Big Property Management"), "[operator account]"),
    (re.compile(r"BANK-ENTERPRISE CLIENT TRUST MAIN"), "[trust account name withheld]"),
]

CAT_H  = re.compile(r"^#{2,3}\s*Category\s*([1-5])\b.*$", re.M)
# "- **C1.1 Object coverage: no** — ..."  and the unbolded variant both appear.
CHECK  = re.compile(
    r"^-\s*\*{0,2}(C[1-5]\.\d{1,2})\*{0,2}\s*([^:*\n]+?)\s*:\s*\*{0,2}\s*"
    r"(yes|no|partial|N-?A|unverified)\b\*{0,2}\s*(.*)$",
    re.I | re.M)

MARKS = {"yes": "yes", "no": "no", "partial": "partial",
         "na": "na", "n-a": "na", "n/a": "na", "unverified": "unverified"}


def clean(s):
    """Markdown to plain text. Keeps `code` as a marker the builder turns into
    <code>, drops emphasis, collapses whitespace."""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)      # links -> label
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^[—–-]\s*", "", s)
    for pat, repl in REDACTIONS:
        s = pat.sub(repl, s)
    return s


def field(text, label):
    m = re.search(rf"^-\s*\*{{0,2}}{re.escape(label)}\*{{0,2}}\s*:\s*(.+)$", text, re.I | re.M)
    return clean(m.group(1)) if m else ""


def parse(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    cats = list(CAT_H.finditer(t))
    if len(cats) != 5:
        raise SystemExit(f"{path.name}: expected 5 category headings, found {len(cats)}")

    checks, seen = [], set()
    for i, m in enumerate(cats):
        end = cats[i + 1].start() if i + 1 < len(cats) else len(t)
        body = t[m.end():end]
        # Stop at the category's own score-math / prose tail so sub-bullets in
        # "What this means for you" cannot be mistaken for checks.
        cut = re.search(r"^\*{0,2}(Score math|What this means)", body, re.M)
        if cut:
            body = body[:cut.start()]
        for cm in CHECK.finditer(body):
            cid = cm.group(1).upper()
            if cid in seen:            # first mention wins
                continue
            seen.add(cid)
            checks.append({
                "id":    cid,
                "cat":   int(cid[1]),
                "title": clean(cm.group(2)),
                "mark":  MARKS[cm.group(3).lower().replace("/", "-")],
                "why":   clean(cm.group(4)),
            })

    meta = {
        "tier":     field(t, "Evidence tier"),
        "battery":  field(t, "Minimum live-test battery"),
        "date":     field(t, "Date run"),
        "model":    field(t, "Evaluating model"),
        "coverage": field(t, "Overall verification coverage"),
    }
    return checks, meta


def main():
    if not REPORTS.is_dir():
        sys.exit(f"reports directory not found: {REPORTS.resolve()}")
    out, problems = {}, []
    for company, fname in sorted(SOURCES.items()):
        p = REPORTS / fname
        if not p.exists():
            problems.append(f"{company}: missing {fname}")
            continue
        checks, meta = parse(p)
        out[company] = {"source": fname, "meta": meta, "checks": checks}
        flag = "" if len(checks) == 27 else f"   <-- {len(checks)} checks, expected 27"
        print(f"  {company:20} {len(checks):>2} checks   {fname}{flag}")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT}  ({OUT.stat().st_size:,} bytes, {len(out)} companies)")
    for pr in problems:
        print("  !", pr)


if __name__ == "__main__":
    main()
