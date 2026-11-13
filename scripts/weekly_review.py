#!/usr/bin/env python3
"""Weekly post-publish review — one place for everything that used to be a manual reminder.

    python scripts/weekly_review.py                     # report + exact commands for this week
    python scripts/weekly_review.py --done backfill slug1 slug2
    python scripts/weekly_review.py --done gsc slug1      # after reviewing GSC for that article
    python scripts/weekly_review.py --seed                # one-time: add existing Final-*.md to the ledger

Reads knowledge/3-pipeline/publish-ledger.csv (written by article_snapshot.py at each stage) and the live
snapshot (knowledge/raw/live/html/<slug>.html, written by sync_live.py) and prints:
  1. Finalized but not seen live → paste 4-cms/<slug>.html into the CMS, then one sync_live command.
  2. Live, backfill not done → ONE batched link plan for all of them (instead of one CMS session per article).
  3. Live 28–56 days, GSC not checked → the MCP query to run + decision rule (→ /optimize or OK).
  4. Housekeeping: revision-log rotation, drafts older than 30 days in 2-drafts/.
Stdlib only, 0 network.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import article_snapshot as snap  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = snap.ROOT
LIVE = ROOT / "knowledge/raw/live/html"
FINAL = ROOT / "knowledge/4-content/3-finalized"
DRAFTS = ROOT / "knowledge/4-content/2-drafts"
CMS = ROOT / "knowledge/4-content/4-cms"
GSC_FROM, GSC_TO = 28, 56          # days after first seen live
STALE_DRAFT_DAYS = 30


def d(s: str) -> date | None:
    try:
        return date.fromisoformat(s[:10])
    except (TypeError, ValueError):
        return None


def live_slug(slug: str) -> str:
    """Slug on dsc.com.vn — Final files often keep a shorter local name (Final-adx-la-gi → chi-bao-adx-la-gi);
    the real URL is in the front matter (`source:` / `url:` / `Slug:`)."""
    f = FINAL / f"Final-{slug}.md"
    if f.exists():
        head = f.read_text(encoding="utf-8", errors="replace")[:1500]
        m = re.search(r"^(?:source|url|URL|canonical|Slug)\s*:\s*[\"']?(\S+?)[\"']?\s*$", head, re.M)
        if m:
            return m.group(1).rstrip("/").rsplit("/", 1)[-1] or slug
    return slug


def is_live(slug: str) -> bool:
    return (LIVE / f"{slug}.html").exists() or (LIVE / f"{live_slug(slug)}.html").exists()


def seed() -> int:
    rows = snap.read_ledger()
    added = 0
    for f in sorted(FINAL.glob("Final-*.md")):
        slug = f.name[len("Final-"):-3]
        if slug in rows:
            continue
        row = {c: "" for c in snap.LEDGER_COLS} | {"slug": slug, "note": "seed"}
        row["final"] = date.fromtimestamp(f.stat().st_mtime).isoformat()
        if (date.today() - date.fromisoformat(row["final"])).days <= 21 and not is_live(slug):
            row["note"] = ""            # finalized recently → track like a new article
        if is_live(slug):
            # already published before the ledger existed: don't flood this week's queues
            row["first_live"] = row["backfill_done"] = row["gsc_checked"] = "seed"
        rows[slug] = row
        added += 1
    snap.write_ledger(rows)
    print(f"Seed: thêm {added} bài vào {snap.LEDGER.relative_to(ROOT)} (bài đã live trước đây đánh dấu `seed`, "
          "không vào hàng đợi; bài cũ cần đo dùng MCP get_content_decay).")
    return 0


def qa_scores(slug: str) -> str:
    """Latest qa-score-log row of the article: "score 96 · coverage 84 · trust 87 · slop 97"."""
    log = snap.ROOT / "knowledge/3-pipeline/qa-score-log.csv"
    if not log.exists():
        return ""
    import csv
    last = None
    with log.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("slug") == slug:
                last = r
    if not last:
        return ""
    return " · ".join(f"{k} {last[k]}" for k in ("score", "coverage", "trust", "slop") if last.get(k))


def done(col: str, slugs: list[str], result: str = "") -> int:
    key = {"backfill": "backfill_done", "gsc": "gsc_checked", "live": "first_live"}[col]
    for s in slugs:
        snap.stamp(s, key)
        if col == "gsc":
            # Keep the outcome next to the QA scores: the only way to learn whether the scores predict ranking.
            if result:
                snap.stamp(s, "gsc_result", f"{date.today().isoformat()} {result}")
            qa = qa_scores(s)
            if qa:
                snap.stamp(s, "qa_at_final", qa)
    print(f"Đã ghi {key} = {date.today().isoformat()} cho: {', '.join(slugs)}" + (f" · kết quả: {result}" if result else ""))
    return 0


def outcomes() -> int:
    """Articles with both QA scores and a GSC result — read this before changing QA rules."""
    rows = [(s, r) for s, r in sorted(snap.read_ledger().items()) if r.get("gsc_result")]
    if not rows:
        print("Chưa có bài nào được ghi kết quả GSC (`--done gsc <slug> --result \"pos 8.2 · clicks 120 · imp 3400\"`).")
        return 0
    print("| Slug | Final | Điểm QA lúc final | Kết quả GSC |\n|---|---|---|---|")
    for s, r in rows:
        print(f"| {s} | {r['final']} | {r.get('qa_at_final') or '-'} | {r['gsc_result']} |")
    return 0


def report() -> int:
    rows = snap.read_ledger()
    today = date.today()
    # 0. auto-detect first time a finalized article shows up in the live snapshot
    for slug, r in rows.items():
        if r["final"] and not r["first_live"] and is_live(slug):
            r["first_live"] = today.isoformat()
    snap.write_ledger(rows)

    unpublished = [s for s, r in rows.items() if r["final"] and not r["first_live"]]
    pending = [s for s in unpublished if rows[s]["note"] != "seed"]
    old_unpublished = [s for s in unpublished if rows[s]["note"] == "seed"]
    backfill = [s for s, r in rows.items() if d(r["first_live"]) and not r["backfill_done"]]
    gsc_due = []
    for s, r in rows.items():
        live = d(r["first_live"])
        if live and not r["gsc_checked"] and GSC_FROM <= (today - live).days:
            gsc_due.append((s, (today - live).days))

    print(f"# Weekly review {today.isoformat()} · ledger {len(rows)} bài\n")

    print(f"## 1. Chờ publish / chưa thấy trên live ({len(pending)})")
    for s in pending:
        cms = CMS / f"{s}.html"
        print(f"- {s} · final {rows[s]['final']} · HTML: {cms.relative_to(ROOT) if cms.exists() else '(chưa có — chạy md_to_cms_html.py)'}")
    if old_unpublished:
        print(f"- (+ {len(old_unpublished)} bài Final cũ, trước khi có sổ, chưa thấy trên snapshot live — "
              "`python scripts/weekly_review.py --unpublished` để xem; có thể nằm ngoài /kien-thuc hoặc chưa đăng)")
    if pending:
        print(f"\nSau khi dán CMS: `python scripts/sync_live.py --only {','.join(live_slug(x) for x in pending)}` rồi chạy lại lệnh này.\n")

    print(f"## 2. Backfill link theo lô ({len(backfill)})")
    if backfill:
        for s in backfill:
            print(f"- `python scripts/find_links.py --backfill {s}`")
        print(f"\nGộp gợi ý của cả {len(backfill)} bài vào **1 spec** "
              f"`knowledge/3-pipeline/internal-links/plans/{today.isoformat()}-weekly-backfill.json` "
              "(quy tắc: internal-linking/SKILL.md §Quy tắc đặt link) → `python scripts/link_plan.py build <spec>` → sửa CMS một lượt "
              "→ `sync_live.py --only <các bài nguồn>` → `link_plan.py verify <spec>` → "
              f"`python scripts/weekly_review.py --done backfill {' '.join(backfill)}`\n")

    print(f"## 3. Đo GSC sau publish ({len(gsc_due)})")
    for s, days in sorted(gsc_due, key=lambda x: -x[1]):
        print(f"- {s} · live {days} ngày · https://www.dsc.com.vn/kien-thuc/{live_slug(s)}")
    if gsc_due:
        print("\nVới từng bài: MCP `query_search_analytics` (property `sc-domain:dsc.com.vn`, dimensions [\"query\"], "
              "page = URL trên, days 28) → `python scripts/dashboard_cache.py save page-queries <slug>`.\n"
              "Quyết định: impressions có nhưng CTR < 1% ở vị trí 1–10 → `/optimize` Title/Meta · vị trí 11–30 → `/optimize` nội dung "
              "(query thiếu trong H2/FAQ) · < 50 impressions sau 8 tuần → kiểm index/cannibalization (`get_cannibalization`) · còn lại OK.\n"
              "Xong: `python scripts/weekly_review.py --done gsc <slug…>`. Bài cũ (seed): MCP `get_content_decay`.\n")

    print("## 4. Dọn dẹp")
    print("- `python scripts/rotate_revision_log.py` (revision-log chỉ giữ 30 ngày)")
    stale = [f for f in DRAFTS.glob("*.md")
             if (today - date.fromtimestamp(f.stat().st_mtime)).days > STALE_DRAFT_DAYS]
    if stale:
        print(f"- {len(stale)} file trong 2-drafts/ không đổi > {STALE_DRAFT_DAYS} ngày (hỏi user trước khi xoá/lưu trữ): "
              + ", ".join(f.name for f in sorted(stale)[:15]) + (" …" if len(stale) > 15 else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", action="store_true")
    ap.add_argument("--unpublished", action="store_true", help="liệt kê mọi Final chưa thấy trên snapshot live")
    ap.add_argument("--done", nargs="+", metavar=("backfill|gsc|live", "SLUG"))
    ap.add_argument("--result", default="", help='với --done gsc: kết quả đo, ví dụ "pos 8.2 · clicks 120 · imp 3400 · AI cited 0"')
    ap.add_argument("--outcomes", action="store_true", help="bảng điểm QA lúc final ↔ kết quả GSC của các bài đã đo")
    a = ap.parse_args()
    if a.outcomes:
        return outcomes()
    if a.seed:
        return seed()
    if a.unpublished:
        for slug, r in sorted(snap.read_ledger().items()):
            if r["final"] and not r["first_live"]:
                print(f"{slug}\tfinal {r['final']}\tlive slug: {live_slug(slug)}")
        return 0
    if a.done:
        if len(a.done) < 2 or a.done[0] not in ("backfill", "gsc", "live"):
            ap.error("--done backfill|gsc|live <slug…>")
        return done(a.done[0], a.done[1:], a.result)
    return report()


if __name__ == "__main__":
    sys.exit(main())
