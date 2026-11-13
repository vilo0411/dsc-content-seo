#!/usr/bin/env python3
"""Keep revision-log.md small: keep the last 30 days, move older entries to knowledge/3-pipeline/revision-log/YYYY-Qn.md
and the old markdown "QA Score Log" table to qa-score-log.csv. Idempotent; run any time (also from /weekly).

    python scripts/rotate_revision_log.py [--dry-run]

Search across all quarters: `grep -rn "<slug>" knowledge/3-pipeline/revision-log*`
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date, timedelta
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "knowledge/3-pipeline/revision-log.md"
ARCH = ROOT / "knowledge/3-pipeline/revision-log"
SCORE_CSV = ROOT / "knowledge/3-pipeline/qa-score-log.csv"
SCORE_COLS = ["date", "slug", "score", "critical", "major", "minor", "anti_ai", "seo", "readability", "link", "geo", "slop"]
ENTRY = re.compile(r"^### \[(\d{4})-(\d{2})-(\d{2})\]")
KEEP_DAYS = 30


def quarter(y: str, m: str) -> str:
    return f"{y}-Q{(int(m) - 1) // 3 + 1}"


def split(text: str):
    """→ (head_lines, entries[(iso_date, block)], score_rows[list])"""
    lines = text.replace("\r\n", "\n").split("\n")
    head, entries, score_rows = [], [], []
    cur, cur_q, in_score = None, None, False
    for line in lines:
        m = ENTRY.match(line)
        if line.startswith("## QA Score Log"):
            in_score = True
            if cur:
                entries.append((cur_q, "\n".join(cur).rstrip()))
                cur = None
            continue
        if in_score:
            if line.startswith("## ") or m:
                in_score = False
            else:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 5 and re.match(r"\d{4}-\d{2}-\d{2}", cells[0]):
                    score_rows.append(cells)
                continue
        if m:
            if cur:
                entries.append((cur_q, "\n".join(cur).rstrip()))
            cur, cur_q = [line], f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            continue
        if line.startswith("## ") and cur:            # a section header ends the running entry
            entries.append((cur_q, "\n".join(cur).rstrip()))
            cur = None
        if cur is not None:
            cur.append(line)
        else:
            head.append(line)
    if cur:
        entries.append((cur_q, "\n".join(cur).rstrip()))
    return head, entries, score_rows


def score_row(cells: list[str]) -> list[str]:
    """| Ngày | Slug | Score | C/M/m | anti=100 seo=100 read=94 link=100 geo=100 [slop=94] |"""
    c, mj, mn = (cells[3].split("/") + ["", "", ""])[:3]
    kv = dict(re.findall(r"(\w+)=(\d+)", cells[4]))
    return [cells[0], cells[1], cells[2], c, mj, mn, kv.get("anti", ""), kv.get("seo", ""), kv.get("read", ""),
            kv.get("link", ""), kv.get("geo", ""), kv.get("slop", "")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    head, entries, scores = split(LOG.read_text(encoding="utf-8"))
    cutoff = (date.today() - timedelta(days=KEEP_DAYS)).isoformat()
    keep = [b for d, b in entries if d >= cutoff]
    move: dict[str, list[str]] = {}
    for d, b in entries:
        if d < cutoff:
            move.setdefault(quarter(d[:4], d[5:7]), []).append(b)
    print(f"revision-log.md: {len(entries)} mục → giữ {len(keep)} (từ {cutoff}), chuyển "
          + ", ".join(f"{q}: {len(v)}" for q, v in sorted(move.items())) + f"; {len(scores)} dòng điểm → CSV")
    if a.dry_run:
        return 0
    ARCH.mkdir(parents=True, exist_ok=True)
    for q, blocks in move.items():
        f = ARCH / f"{q}.md"
        existing = f.read_text(encoding="utf-8") if f.exists() else f"# Revision log {q}\n"
        new = [b for b in blocks if b not in existing]
        if new:
            f.write_text(existing.rstrip() + "\n\n" + "\n\n".join(new) + "\n", encoding="utf-8")
    if scores:
        newfile = not SCORE_CSV.exists()
        with SCORE_CSV.open("a", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            if newfile:
                w.writerow(SCORE_COLS)
            for cells in scores:
                w.writerow(score_row(cells))
    head_text = "\n".join(head).rstrip()
    note = (f"\n\n> Mục quý trước nằm ở `knowledge/3-pipeline/revision-log/YYYY-Qn.md` (`python scripts/rotate_revision_log.py`). "
            f"Tìm theo bài: `grep -rn \"<slug>\" knowledge/3-pipeline/revision-log*`. Điểm QA: `qa-score-log.csv`.")
    if "revision-log/YYYY-Qn.md" in head_text:
        note = ""
    LOG.write_text(head_text + note + "\n\n" + "\n\n".join(keep) + "\n", encoding="utf-8")
    print("Đã xoay vòng.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
