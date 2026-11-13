#!/usr/bin/env python3
"""Keep every stage of an article instead of deleting it, and diff stages cheaply.

    python scripts/article_snapshot.py <slug> --stage outline   # at Outline-Approved
    python scripts/article_snapshot.py <slug> --stage gate2     # when the draft is shown at Approval Gate 2
    python scripts/article_snapshot.py <slug> --stage final     # at /approve Finalize (also archives the outline)
    python scripts/article_snapshot.py <slug> --diff [--from gate2 --to final]
    python scripts/article_snapshot.py <slug> --path outline    # print archived file path (e.g. for qa_lint --outline)

Snapshots: knowledge/4-content/archive/<slug>/<stage>.md (latest of each stage; the previous gate2 is kept
as gate2.prev.md). `--diff` prints only the paragraphs that changed — what /learn needs to see the user's
edits without reading two full articles. Every stage also stamps knowledge/3-pipeline/publish-ledger.csv,
which scripts/weekly_review.py uses for sync/backfill/GSC follow-ups. Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import re
import shutil
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "knowledge/4-content"
ARCHIVE = CONTENT / "archive"
LEDGER = ROOT / "knowledge/3-pipeline/publish-ledger.csv"
LEDGER_COLS = ["slug", "outline", "gate2", "final", "first_live", "backfill_done", "gsc_checked", "note",
               "qa_at_final", "gsc_result"]  # scores vs real outcome, side by side (filled by weekly_review --done gsc --result)

SOURCES = {
    "outline": [CONTENT / "1-outlines" / "{slug}.md", CONTENT / "1-outlines" / "Proposal-{slug}.md",
                CONTENT / "2-drafts" / "Proposal-{slug}.md"],
    "gate2": [CONTENT / "2-drafts" / "Draft-{slug}.md", CONTENT / "2-drafts" / "Optimize-{slug}.md"],
    "final": [CONTENT / "3-finalized" / "Final-{slug}.md"],
}


def find_source(slug: str, stage: str) -> Path | None:
    for pattern in SOURCES[stage]:
        p = Path(str(pattern).format(slug=slug))
        if p.exists():
            return p
    return None


# ─────────────────────────── ledger ───────────────────────────

def read_ledger() -> dict[str, dict]:
    if not LEDGER.exists():
        return {}
    with LEDGER.open(encoding="utf-8", newline="") as fh:
        return {r["slug"]: {c: r.get(c, "") for c in LEDGER_COLS} for r in csv.DictReader(fh)}


def write_ledger(rows: dict[str, dict]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS)
        w.writeheader()
        for slug in sorted(rows):
            w.writerow(rows[slug])


def stamp(slug: str, col: str, value: str | None = None) -> None:
    rows = read_ledger()
    row = rows.setdefault(slug, {c: "" for c in LEDGER_COLS} | {"slug": slug})
    row[col] = value or date.today().isoformat()
    write_ledger(rows)


# ─────────────────────────── snapshot ───────────────────────────

def snapshot(slug: str, stage: str) -> int:
    src = find_source(slug, stage)
    if not src:
        print(f"Không tìm thấy file {stage} cho `{slug}` ({', '.join(str(p).format(slug=slug) for p in SOURCES[stage])})")
        return 1
    dest_dir = ARCHIVE / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{stage}.md"
    if stage == "gate2" and dest.exists():
        shutil.copy2(dest, dest_dir / "gate2.prev.md")
    shutil.copy2(src, dest)
    print(f"{stage}: {src.relative_to(ROOT)} → {dest.relative_to(ROOT)}")
    if stage == "final":
        outline = find_source(slug, "outline")
        if outline:   # archive instead of deleting, so /optimize can re-run qa_lint --outline later
            target = dest_dir / "outline.md"
            if not target.exists():
                shutil.copy2(outline, target)
            outline.unlink()
            print(f"outline: {outline.relative_to(ROOT)} → {target.relative_to(ROOT)} (đã chuyển khỏi 1-outlines/)")
            if not read_ledger().get(slug, {}).get("outline"):
                stamp(slug, "outline")  # approved without `--stage outline`: still record that one exists
    stamp(slug, stage)
    if stage in ("gate2", "final") and not (dest_dir / "outline.md").exists() and not find_source(slug, "outline"):
        # The outline is the only record of Thesis / Information_Gain / PAA plan. Without it qa_lint cannot
        # check them now, and /optimize cannot later. Non-zero exit so the caller sees it.
        print(f"⚠ KHÔNG CÓ OUTLINE cho `{slug}` (1-outlines/ lẫn archive/{slug}/outline.md): "
              "Information_Gain / PAA / entity của bài này không được kiểm và không còn lưu. Báo user.")
        return 3
    return 0


# ─────────────────────────── diff ───────────────────────────

def blocks(text: str) -> list[str]:
    text = re.sub(r"^---\n[\s\S]*?\n---\n", "", text.replace("\r\n", "\n"))
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]


def stage_file(slug: str, stage: str) -> Path | None:
    p = ARCHIVE / slug / f"{stage}.md"
    if p.exists():
        return p
    return find_source(slug, stage)


def diff(slug: str, a: str, b: str) -> int:
    fa, fb = stage_file(slug, a), stage_file(slug, b)
    if not fa or not fb:
        print(f"Thiếu bản `{a if not fa else b}` của `{slug}` — chưa snapshot stage đó.")
        return 1
    A, B = blocks(fa.read_text(encoding="utf-8")), blocks(fb.read_text(encoding="utf-8"))
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    changed = [op for op in sm.get_opcodes() if op[0] != "equal"]
    same = sum(i2 - i1 for tag, i1, i2, _, _ in sm.get_opcodes() if tag == "equal")
    print(f"# Diff {slug}: {a} → {b} · {len(A)} → {len(B)} đoạn · giữ nguyên {same} · thay đổi {len(changed)} cụm\n")
    for tag, i1, i2, j1, j2 in changed:
        old, new = A[i1:i2], B[j1:j2]
        # pair up 1:1 replacements with a word-level ratio so trivial edits are visible as such
        if tag == "replace" and len(old) == len(new):
            for o, n in zip(old, new):
                r = difflib.SequenceMatcher(a=o.split(), b=n.split()).ratio()
                print(f"## sửa (giống {r:.0%})\n- {o}\n+ {n}\n")
            continue
        label = {"delete": "xoá", "insert": "thêm", "replace": "viết lại"}[tag]
        print(f"## {label}")
        for o in old:
            print(f"- {o}")
        for n in new:
            print(f"+ {n}")
        print()
    if not changed:
        print("Không có thay đổi.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--stage", choices=list(SOURCES))
    g.add_argument("--diff", action="store_true")
    g.add_argument("--path", choices=["outline", "gate2", "final"])
    ap.add_argument("--from", dest="a", default="gate2")
    ap.add_argument("--to", dest="b", default="final")
    args = ap.parse_args()
    if args.stage:
        return snapshot(args.slug, args.stage)
    if args.path:
        p = stage_file(args.slug, args.path)
        print(p.relative_to(ROOT) if p else "")
        return 0 if p else 1
    return diff(args.slug, args.a, args.b)


if __name__ == "__main__":
    sys.exit(main())
