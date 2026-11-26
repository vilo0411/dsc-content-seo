#!/usr/bin/env python3
"""Keep every stage of an article instead of deleting it, and diff stages cheaply.

    python scripts/article_snapshot.py <slug> --stage outline   # at Outline-Approved
    python scripts/article_snapshot.py <slug> --stage gate2     # when the draft is shown at Approval Gate 2
    python scripts/article_snapshot.py <slug> --stage final     # at /approve Finalize (also archives the outline)
    python scripts/article_snapshot.py <slug> --diff [--from gate2 --to final]
    python scripts/article_snapshot.py <slug> --path outline    # print archived file path (e.g. for qa_lint --outline)
    python scripts/article_snapshot.py <slug> --baseline "pos 12.3 · clicks 80 · imp 5000"   # /optimize step 1.1

Re-finalizing an article that is already live (or already had a final) counts as an optimize round: the
first `final` date is kept, `optimized` / `optimize_count` are set, the previous Final is kept as
final.prev.md, and the previous round (baseline → result) moves to `optimize_history`. weekly_review.py then
re-measures GSC 28–56 days after the update is seen live and compares it with `optimize_baseline`.

Snapshots: knowledge/3-seo/content/archive/<slug>/<stage>.md (latest of each stage; the previous gate2 is kept
as gate2.prev.md). `--diff` prints only the paragraphs that changed — what /learn needs to see the user's
edits without reading two full articles. Every stage also stamps knowledge/3-seo/logs/publish-ledger.csv,
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from activity_log import emit  # noqa: E402
CONTENT = ROOT / "knowledge/3-seo/content"
ARCHIVE = CONTENT / "archive"
LEDGER = ROOT / "knowledge/3-seo/logs/publish-ledger.csv"
LEDGER_COLS = ["slug", "outline", "gate2", "final", "first_live", "backfill_done", "gsc_checked", "note",
               "qa_at_final", "gsc_result",  # scores vs real outcome, side by side (filled by weekly_review --done gsc --result)
               # /optimize rounds: latest round in its own columns, older rounds folded into optimize_history
               "optimized", "optimize_count", "optimize_baseline", "optimize_live", "optimize_gsc_checked",
               "optimize_result", "optimize_history"]

SOURCES = {
    "outline": [CONTENT / "1-outlines" / "{slug}.md", CONTENT / "1-outlines" / "Proposal-{slug}.md",
                CONTENT / "2-drafts" / "Proposal-{slug}.md"],
    "gate2": [CONTENT / "2-drafts" / "Draft-{slug}.md", CONTENT / "2-drafts" / "Optimize-{slug}.md"],
    "final": [CONTENT / "3-finalized" / "Final-{slug}.md"],
}


def already_live(slug: str) -> bool:
    """Live snapshot exists for the slug or for the URL in the Final's front matter (`source:` / `url:` / `Slug:`)."""
    live = ROOT / "knowledge/raw/live/html"
    names = {slug}
    final = CONTENT / "3-finalized" / f"Final-{slug}.md"
    if final.exists():
        m = re.search(r"^(?:source|url|URL|canonical|Slug)\s*:\s*[\"']?(\S+?)[\"']?\s*$",
                      final.read_text(encoding="utf-8", errors="replace")[:1500], re.M)
        if m:
            names.add(m.group(1).rstrip("/").rsplit("/", 1)[-1])
    return any((live / f"{n}.html").exists() for n in names if n)


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


# ledger column → (activity action, status) — every stamp leaves one line in the activity log
LEDGER_EVENT = {"outline": ("approve", "Outline-Approved"), "gate2": ("approve", "Draft-Approved"),
                "final": ("approve", "Finalized"), "first_live": ("publish", "Live"), "backfill_done": ("link", ""),
                "gsc_checked": ("report", ""), "optimize_live": ("publish", "Live"), "optimize_gsc_checked": ("report", "")}


def stamp(slug: str, col: str, value: str | None = None) -> None:
    rows = read_ledger()
    row = rows.setdefault(slug, {c: "" for c in LEDGER_COLS} | {"slug": slug})
    row[col] = value or date.today().isoformat()
    write_ledger(rows)
    if col in LEDGER_EVENT:
        action, st = LEDGER_EVENT[col]
        emit("seo", action, slug, skill="article_snapshot", status_to=st, note=f"ledger:{col}",
             path="knowledge/3-seo/logs/publish-ledger.csv")


def fold_round(row: dict) -> None:
    """Move the latest optimize round (date: baseline → result) into optimize_history and clear its columns."""
    if not row.get("optimized"):
        return
    prev = f"{row['optimized']}: {row.get('optimize_baseline') or '?'} → {row.get('optimize_result') or 'chưa đo'}"
    row["optimize_history"] = " ;; ".join(x for x in (row.get("optimize_history"), prev) if x)
    for c in ("optimized", "optimize_baseline", "optimize_live", "optimize_gsc_checked", "optimize_result"):
        row[c] = ""


def set_baseline(slug: str, text: str) -> None:
    """/optimize step 1.1: GSC before the rewrite. Starts a new round, so the previous one goes to history first."""
    rows = read_ledger()
    row = rows.setdefault(slug, {c: "" for c in LEDGER_COLS} | {"slug": slug})
    fold_round(row)
    row["optimize_baseline"] = f"{date.today().isoformat()} {text}"
    write_ledger(rows)


def record_optimize(slug: str) -> None:
    """Finalize an optimize round: keep the first `final` date, count the round, reset its live/GSC follow-up."""
    rows = read_ledger()
    row = rows.setdefault(slug, {c: "" for c in LEDGER_COLS} | {"slug": slug})
    today = date.today().isoformat()
    if row.get("optimized") == today:
        pass                        # re-approved the same day: same round
    else:
        if row.get("optimized"):    # no --baseline this time: close the previous round here
            fold_round(row)
        row["optimize_count"] = str(int(row.get("optimize_count") or 0) + 1)
    row["final"] = row.get("final") or today
    row["optimized"] = today
    row["optimize_live"] = row["optimize_gsc_checked"] = row["optimize_result"] = ""
    write_ledger(rows)
    emit("seo", "approve", slug, skill="optimize", status_to="Optimized", note=f"lần {row['optimize_count']}",
         path="knowledge/3-seo/logs/publish-ledger.csv")
    print(f"optimize: lần {row['optimize_count']} · baseline: {row.get('optimize_baseline') or '⚠ chưa ghi (--baseline)'}")


# ─────────────────────────── snapshot ───────────────────────────

def snapshot(slug: str, stage: str) -> int:
    src = find_source(slug, stage)
    if not src:
        print(f"Không tìm thấy file {stage} cho `{slug}` ({', '.join(str(p).format(slug=slug) for p in SOURCES[stage])})")
        return 1
    dest_dir = ARCHIVE / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{stage}.md"
    row = read_ledger().get(slug, {})
    # re-finalizing something already published = optimize round (ledger row may not exist for pre-ledger articles)
    is_optimize = stage == "final" and bool(row.get("first_live") or dest.exists() or already_live(slug))
    if stage == "gate2" and dest.exists():
        shutil.copy2(dest, dest_dir / "gate2.prev.md")
    if is_optimize and dest.exists():
        shutil.copy2(dest, dest_dir / "final.prev.md")  # the version before this optimize round
    shutil.copy2(src, dest)
    print(f"{stage}: {src.relative_to(ROOT)} → {dest.relative_to(ROOT)}")
    if stage == "final":
        outline = find_source(slug, "outline")
        if outline:   # archive instead of deleting, so /optimize can re-run qa_lint --outline later
            target = dest_dir / "outline.md"
            if target.exists() and target.read_bytes() != outline.read_bytes():
                # a new outline for a re-written article: keep the old one instead of dropping the new one
                shutil.copy2(target, dest_dir / "outline.prev.md")
            shutil.copy2(outline, target)
            outline.unlink()
            print(f"outline: {outline.relative_to(ROOT)} → {target.relative_to(ROOT)} (đã chuyển khỏi 1-outlines/)")
            if not read_ledger().get(slug, {}).get("outline"):
                stamp(slug, "outline")  # approved without `--stage outline`: still record that one exists
    if is_optimize:
        record_optimize(slug)
    else:
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
    g.add_argument("--baseline", metavar="TEXT", help='GSC trước khi optimize, vd "pos 12.3 · clicks 80 · imp 5000 (28d)"')
    ap.add_argument("--from", dest="a", default="gate2")
    ap.add_argument("--to", dest="b", default="final")
    args = ap.parse_args()
    if args.stage:
        return snapshot(args.slug, args.stage)
    if args.baseline:
        set_baseline(args.slug, args.baseline)
        print(f"Baseline optimize `{args.slug}`: {args.baseline}")
        return 0
    if args.path:
        p = stage_file(args.slug, args.path)
        print(p.relative_to(ROOT) if p else "")
        return 0 if p else 1
    return diff(args.slug, args.a, args.b)


if __name__ == "__main__":
    sys.exit(main())
