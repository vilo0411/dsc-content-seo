#!/usr/bin/env python3
"""Brand fact register checker — keeps DSC facts (fees, margin rate, eKYC time, deposit code…) consistent
across every article. Register: knowledge/1-brand/brand-facts.json (owner, source, verified_at, review cycle).

Usage:
    python scripts/fact_consistency.py                     # scan live snapshot + 3-finalized, list conflicts
    python scripts/fact_consistency.py --source live       # only knowledge/raw/live/html (what Google/AI sees)
    python scripts/fact_consistency.py --source final      # only knowledge/3-seo/content/3-finalized
    python scripts/fact_consistency.py --changed margin_rate   # every article mentioning that fact (to update after a change)
    python scripts/fact_consistency.py --due               # facts past their review date or never verified
    python scripts/fact_consistency.py --list              # print the register

Also imported by qa_lint.py (CL5-fact / FACT-unverified):
    from fact_consistency import load_facts, check_sentence

Exit: 0 = no conflicts / nothing due, 1 = conflicts or facts due, 2 = register missing / invalid.
Stdlib only.
"""

from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, FINAL_DIR, setup_utf8, slug_from_path, read_text  # noqa: E402

FACTS_FILE = ROOT / "knowledge/1-brand/brand-facts.json"
LIVE_HTML = ROOT / "knowledge/raw/live/html"

_NUM = r"(\d+(?:,\d+)?)"


# ─────────────────────────── Register ───────────────────────────

def load_facts(path: Path = FACTS_FILE) -> list[dict]:
    """Return the fact list; [] when the register is missing (callers degrade gracefully)."""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("facts", [])


def _num(s: str) -> float:
    return float(s.replace(",", "."))


def _fmt(v: float) -> str:
    return (f"{v:g}").replace(".", ",")


def _triggered(fact: dict, sl: str) -> bool:
    if "dsc" not in sl:
        return False
    if any(t not in sl for t in fact.get("trigger_all", [])):
        return False
    anyof = fact.get("trigger_any", [])
    return not anyof or any(t in sl for t in anyof)


def check_sentence(sent: str, facts: list[dict]) -> list[tuple[dict, str | None]]:
    """Check one plain-text sentence. Returns [(fact, found_value_or_None)]:
    found != None -> sentence conflicts with the register; None -> sentence uses the fact consistently."""
    sl = sent.lower()
    out: list[tuple[dict, str | None]] = []
    for f in facts:
        if not _triggered(f, sl):
            continue
        c = f["check"]
        kind = c["type"]
        bad: list[str] = []
        seen = False
        if kind == "pct_allowed_range":
            extra = [float(x) for x in c.get("also_allowed", [])]
            for p in re.findall(_NUM + r"\s*%", sent):
                seen = True
                v = _num(p)
                if not (c["min"] <= v <= c["max"]) and v not in extra:
                    bad.append(p)
        elif kind == "unit_value":
            vals = [_num(v) for v in re.findall(_NUM + r"\s*" + re.escape(c["unit"]) + r"\b", sl)]
            if vals:
                seen = True
                if not any(v in [float(a) for a in c["allowed"]] for v in vals):
                    bad.append("–".join(_fmt(v) for v in vals))
        elif kind == "code":
            for m in re.finditer(c["pattern"], sent):
                seen = True
                if m.group(0) != c["expected"]:
                    bad.append(m.group(0))
        for b in bad:
            out.append((f, b))
        if seen and not bad:
            out.append((f, None))
    return out


def message(fact: dict, found: str) -> str:
    msg = fact["message"].format(found=found)
    if fact.get("status") != "verified":
        msg += " [CẦN XÁC NHẬN]"
    return msg


def due(fact: dict, today: date | None = None) -> str | None:
    """Reason the fact needs review, or None."""
    today = today or date.today()
    if fact.get("status") != "verified" or not fact.get("verified_at"):
        return "chưa xác nhận"
    try:
        v = date.fromisoformat(fact["verified_at"])
    except ValueError:
        return f"verified_at sai định dạng: {fact['verified_at']}"
    nxt = v + timedelta(days=int(fact.get("review_every_days", 90)))
    return f"quá hạn review từ {nxt.isoformat()}" if nxt <= today else None


# ─────────────────────────── Corpus ───────────────────────────

def _html_text(raw: str) -> list[str]:
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|li|h[1-6]|tr|td|th|div)>", "\n", raw)
    return [htmllib.unescape(re.sub(r"<[^>]+>", " ", ln)) for ln in raw.split("\n")]


def _md_text(raw: str) -> list[str]:
    lines = raw.split("\n")
    if lines and lines[0].strip() == "---":  # skip frontmatter
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = [""] * (i + 1) + lines[i + 1:]
                break
    out = []
    for ln in lines:
        ln = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", ln)
        ln = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", ln)
        out.append(re.sub(r"[*_`#>|]", " ", ln))
    return out


def _sentences(text: str) -> list[str]:
    t = re.sub(r"(\d)[.,](\d)", r"\1<d>\2", text)
    parts = re.split(r"(?<=[.!?…])\s+(?=\S)", t)
    return [re.sub(r"\s+", " ", p.replace("<d>", ",")).strip() for p in parts if p.strip()]


def corpus(source: str):
    """Yield (origin, slug, path, [lines])."""
    if source in ("live", "all") and LIVE_HTML.exists():
        for p in sorted(LIVE_HTML.glob("*.html")):
            yield "live", p.stem, p, _html_text(p.read_text(encoding="utf-8", errors="replace"))
    if source in ("final", "all") and FINAL_DIR.exists():
        for p in sorted(FINAL_DIR.glob("*.md")):
            yield "final", slug_from_path(p), p, _md_text(read_text(p)[0])


def scan(source: str, facts: list[dict], only: str | None = None):
    """Yield (origin, slug, path, line_no, fact, found, sentence)."""
    if only:
        facts = [f for f in facts if f["id"] == only]
    for origin, slug, path, lines in corpus(source):
        for i, ln in enumerate(lines):
            if "dsc" not in ln.lower():
                continue
            for sent in _sentences(ln):
                for fact, found in check_sentence(sent, facts):
                    yield origin, slug, path, i + 1, fact, found, sent


# ─────────────────────────── CLI ───────────────────────────

def main() -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=["all", "live", "final"], default="all")
    ap.add_argument("--changed", metavar="FACT_ID", help="list every article that mentions this fact")
    ap.add_argument("--due", action="store_true", help="facts past review date / not verified")
    ap.add_argument("--list", action="store_true", help="print the register")
    a = ap.parse_args()

    try:
        facts = load_facts()
    except json.JSONDecodeError as e:
        print(f"brand-facts.json không hợp lệ: {e}")
        return 2
    if not facts:
        print(f"Không thấy register: {FACTS_FILE.relative_to(ROOT)}")
        return 2

    if a.list:
        for f in facts:
            print(f"- {f['id']:<24} {f['value']:<18} {f.get('status', ''):<19} "
                  f"verified {f.get('verified_at') or '—':<10} owner {f.get('owner') or '—'}  ({f['label']})")
        return 0

    if a.due:
        rows = [(f, r) for f in facts if (r := due(f))]
        print(f"## Brand facts cần review — {len(rows)}/{len(facts)}")
        for f, r in rows:
            print(f"- `{f['id']}` {f['label']} = {f['value']} — {r} · owner: {f.get('owner') or 'CHƯA GÁN'}")
        if rows:
            print("\nXác nhận với owner → sửa value / verified_at / status trong knowledge/1-brand/brand-facts.json"
                  " → nếu value đổi: `python scripts/fact_consistency.py --changed <id>`")
        return 1 if rows else 0

    if a.changed:
        if not any(f["id"] == a.changed for f in facts):
            print(f"Không có fact id `{a.changed}`. Dùng --list.")
            return 2
        hits: dict[tuple[str, str], list] = {}
        for origin, slug, path, ln, fact, found, sent in scan(a.source, facts, a.changed):
            hits.setdefault((slug, origin), []).append((ln, found, sent))
        print(f"## Bài nhắc tới `{a.changed}` — {len(hits)} (bài, nguồn)")
        for (slug, origin), rows in sorted(hits.items()):
            flag = " ⚠️ lệch" if any(f for _, f, _ in rows) else ""
            print(f"- {slug} [{origin}]{flag}: dòng {', '.join(str(r[0]) for r in rows[:6])}")
        return 0

    conflicts = [r for r in scan(a.source, facts) if r[5] is not None]
    by_fact: dict[str, list] = {}
    for r in conflicts:
        by_fact.setdefault(r[4]["id"], []).append(r)
    print(f"## Fact lệch register — {len(conflicts)} câu, {len({(r[1], r[0]) for r in conflicts})} (bài, nguồn)")
    for fid, rows in by_fact.items():
        print(f"\n### {fid} — chuẩn: {rows[0][4]['value']}")
        for origin, slug, path, ln, fact, found, sent in rows:
            print(f"- {slug} [{origin}:{ln}] {message(fact, found)}\n    > {sent[:160]}")
    if not conflicts:
        print("Không có bài nào lệch register.")
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
