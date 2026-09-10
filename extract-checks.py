#!/usr/bin/env python3
"""
Pull the per-check detail out of the grader markdown reports and freeze it into
data/checks.json, which build-report-card.py reads.

Reads the PUBLISHED reports in files/reports/, not the archive. Those are the
copies a reader can actually download, so whatever this extracts is by
construction the same text the download shows. Run publish-reports.py first: it
copies the archive into files/reports/ and applies redaction and suppression on
the way.

    python3 publish-reports.py && python3 extract-checks.py

Nothing here scores anything. It copies marks and reasoning verbatim.
"""
import json, re, sys, unicodedata
from pathlib import Path

REPORTS = Path("files/reports")
OUT     = Path("data/checks.json")

# Company -> the report file that produced the PUBLISHED score. Kept explicit
# rather than inferred, so a superseded run can never leak onto the page.
SOURCES = {
    "AppFolio":            "appfolio.md",
    "Aptly":               "aptly.md",
    "Boom":                "boom.md",
    "Buildium":            "buildium.md",
    "Column":              "column.md",
    "LeadSimple":          "leadsimple.md",
    "Magic Door":          "magic-door.md",
    "Process Street":      "process-street.md",
    "Property Meld":       "property-meld.md",
    "QuickBooks Online":   "quickbooks-online.md",
    "Quo":                 "quo.md",
    "Rent Manager":        "rent-manager.md",
    "RentEngine":          "rentengine.md",
    "Rentvine":            "rentvine.md",
    "RingCentral":         "ringcentral.md",
    "ShowMojo":            "showmojo.md",
    "Tenant Turner":       "tenant-turner.md",
    "Xero":                "xero.md",
    "Zoom":                "zoom.md",
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
