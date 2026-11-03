#!/usr/bin/env python3
"""Query the internal-link registry without loading the whole anchor-index.md.

Modes:
  python scripts/find_links.py "từ khóa" [--top 8] [--exclude slug] [--json]
      → best-matching published articles to link TO from a new/optimized draft.

  python scripts/find_links.py --backfill <slug> [--top 5] [--json] [--finalized]
      → published articles that should link TO <slug> but don't yet (no in-sentence link), with
        the section + paragraph where an anchor could be wrapped. Scans the live snapshot
        (knowledge/raw/live, sync_live.py); --finalized falls back to 3-finalized/*.md.

Sources: knowledge/3-pipeline/internal-links/anchor-index.md, sitemap-cache.json,
         knowledge/raw/live/{html/,links.csv,pages.csv} (backfill + inlink column),
         knowledge/4-content/3-finalized/*.md (backfill --finalized only),
         knowledge/raw/gsc/pages.csv (optional, ranks backfill sources by clicks).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from datetime import datetime
from html import unescape as html_unescape
from dataclasses import dataclass, asdict
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
ANCHOR_INDEX = ROOT / "knowledge/3-pipeline/internal-links/anchor-index.md"
LIVE_DIR = ROOT / "knowledge/raw/live"
LIVE_HTML = LIVE_DIR / "html"
LIVE_LINKS = LIVE_DIR / "links.csv"
LIVE_PAGES = LIVE_DIR / "pages.csv"
LIVE_META = LIVE_DIR / "_meta.json"
SITEMAP_CACHE = ROOT / ".antigravity/skills/internal-linking/scripts/sitemap-cache.json"
FINALIZED_DIR = ROOT / "knowledge/4-content/3-finalized"
GSC_PAGES = ROOT / "knowledge/raw/gsc/pages.csv"
DSC_KB = "https://www.dsc.com.vn/kien-thuc/"

STOPWORDS = {
    "la", "gi", "va", "cua", "cho", "cac", "nhung", "co", "khong", "duoc", "trong", "khi", "voi", "de",
    "mot", "nay", "nao", "nhu", "the", "cach", "nen", "hay", "ve", "tu", "den", "theo", "tai", "bi", "se",
    "da", "dang", "hon", "nhat", "huong", "dan", "chi", "tiet", "nguoi", "moi", "f0", "kien", "thuc",
    "dsc", "bai", "viet", "2024", "2025", "2026", "cap", "nhat", "top", "nhung", "dieu", "can", "biet",
    "ma", "hieu", "qua", "tot", "nhanh", "an", "toan", "phuong", "phap", "huong", "buoc",
}


def unaccent(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def tokens(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", unaccent(s)) if t and t not in STOPWORDS and len(t) > 1}


@dataclass
class Entry:
    cluster: str
    anchor: str
    url: str
    related: str
    status: str
    line: int

    @property
    def slug(self) -> str:
        return self.url.rstrip("/").rsplit("/", 1)[-1]


def load_index() -> list[Entry]:
    entries, cluster = [], ""
    for i, line in enumerate(ANCHOR_INDEX.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            cluster = re.sub(r"\s*\(\d+ bài\)\s*$", "", line[3:]).strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] in ("Anchor Text Gợi ý", "") or set(cells[0]) <= set(":- "):
            continue
        url = re.sub(r"^\[.*?\]\((.*?)\)$", r"\1", cells[1]).strip("`")
        if not url.startswith("http"):
            continue
        entries.append(Entry(cluster, cells[0], url, cells[2], cells[3], i))
    return entries


def load_sitemap() -> set[str]:
    if not SITEMAP_CACHE.exists():
        return set()
    return {u.rstrip("/") for u in json.loads(SITEMAP_CACHE.read_text(encoding="utf-8")).get("urls", [])}


def load_gsc_clicks() -> dict[str, int]:
    clicks: dict[str, int] = {}
    if not GSC_PAGES.exists():
        return clicks
    with GSC_PAGES.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            url = (row.get("page") or row.get("Page") or row.get("url") or "").rstrip("/")
            try:
                clicks[url] = int(float(row.get("clicks") or row.get("Clicks") or 0))
            except ValueError:
                pass
    return clicks


def live_age() -> str:
    """Human note on snapshot freshness — a stale snapshot means suggestions may already be done."""
    try:
        last = json.loads(LIVE_META.read_text(encoding="utf-8"))["last_run"]
        days = (datetime.now() - datetime.fromisoformat(last)).days
        return f"sync {last[:10]}" + (f" — ⚠ cũ {days} ngày, chạy sync_live.py" if days > 7 else "")
    except (OSError, ValueError, KeyError):
        return "chưa có _meta.json"


def load_inlinks() -> dict[str, str]:
    """slug -> contextual inlink count from the live snapshot ('' when no snapshot)."""
    if not LIVE_PAGES.exists():
        return {}
    with LIVE_PAGES.open(encoding="utf-8-sig", newline="") as f:
        return {r["slug"]: r["in_contextual"] for r in csv.DictReader(f)}


def score(query_tokens: set[str], e: Entry) -> float:
    if not query_tokens:
        return 0.0
    anchor_t, related_t, slug_t = tokens(e.anchor), tokens(e.related), tokens(e.slug.replace("-", " "))
    s = 0.0
    s += 3.0 * len(query_tokens & anchor_t) / len(query_tokens)
    s += 2.0 * len(query_tokens & slug_t) / len(query_tokens)
    s += 1.0 * len(query_tokens & related_t) / len(query_tokens)
    if unaccent(e.anchor) == unaccent(" ".join(sorted(query_tokens))):
        s += 1.0
    return round(s, 3)


def mode_search(args, entries, sitemap):
    q = tokens(args.keyword)
    ranked = []
    for e in entries:
        if args.exclude and args.exclude in e.url:
            continue
        sc = score(q, e)
        if sc > 0:
            ranked.append((sc, e))
    ranked.sort(key=lambda x: (-x[0], x[1].status != "Live Published", x[1].anchor))
    top = ranked[: args.top]
    if args.json:
        print(json.dumps([{**asdict(e), "score": sc, "in_sitemap": e.url.rstrip("/") in sitemap} for sc, e in top],
                         ensure_ascii=False, indent=2))
        return
    print(f"# Internal link candidates for “{args.keyword}” (top {len(top)}/{len(ranked)} matches)\n")
    inl = load_inlinks()
    print("| # | Anchor gợi ý | URL | Cluster | Trạng thái | Sitemap | Inlink ngữ cảnh |")
    print("|---|---|---|---|---|---|---:|")
    for n, (sc, e) in enumerate(top, 1):
        ok = "✓" if e.url.rstrip("/") in sitemap else "✗ (không có trong cache)"
        print(f"| {n} | {e.anchor} | {e.url} | {e.cluster} | {e.status} | {ok} | {inl.get(e.slug, '-')} |")
    if not top:
        print("Không có bài liên quan trong anchor-index. Cân nhắc link về hub cluster hoặc bỏ qua.")
    print("\nChỉ dùng URL có Sitemap ✓. Đặt anchor tự nhiên trong câu, không dùng 'Xem thêm'.")


def live_backfill(target: Entry, q: set[str], core: str, clicks: dict[str, int]) -> list[dict]:
    """Scan every live article snapshot (knowledge/raw/live, ~824 pages) instead of 3-finalized only.

    Pages that already link to the target in a sentence are skipped; pages that only link via a
    "Xem thêm" line are kept and flagged, since the fix there is to move that link into a sentence.
    """
    by_src: dict[str, set[str]] = {}
    with LIVE_LINKS.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["to"].rstrip("/") == target.url.rstrip("/"):
                by_src.setdefault(r["from"], set()).add(r["kind"])
    results = []
    for path in sorted(LIVE_HTML.glob("*.html")):
        src = path.stem
        kinds = by_src.get(src, set())
        if src == target.slug or "contextual" in kinds:
            continue
        section, best = "", None
        for line in path.read_text(encoding="utf-8").splitlines():
            h = re.match(r"<h[23][^>]*>(.*)", line)
            if h:
                section = re.sub(r"<[^>]+>", "", h.group(1)).strip()
                continue
            if not line.startswith(("<p", "<li")):
                continue
            plain = re.sub(r"\s+", " ", html_unescape(re.sub(r"<[^>]+>", "", line))).strip()
            norm_plain = unaccent(plain).replace("-", " ")
            hit = 2.0 if core and core in norm_plain else 0.0
            hit += len(q & tokens(plain)) / max(1, len(q))
            if hit >= 1.0 and (best is None or hit > best[0]):
                best = (hit, section, plain)
        if best:
            results.append({"source": src, "score": round(best[0], 3), "clicks": clicks.get(DSC_KB + src, 0),
                            "section": best[1], "excerpt": best[2], "xem_them_only": "xem-them" in kinds})
    results.sort(key=lambda r: (-r["clicks"], -r["score"], r["source"]))
    return results


def mode_backfill(args, entries, sitemap):
    target = next((e for e in entries if e.slug == args.backfill), None)
    if target is None:
        matches = [e for e in entries if args.backfill in e.url]
        if len(matches) == 1:
            target = matches[0]
        else:
            print(f"Không tìm thấy slug '{args.backfill}' trong anchor-index"
                  + (f" ({len(matches)} URL gần giống)" if matches else ""), file=sys.stderr)
            sys.exit(1)
    q = tokens(target.anchor) | tokens(target.related)
    # Core phrase = anchor without question suffix ("free float là gì" → "free float")
    core = re.sub(r"\s+(la gi|la sao|nhu the nao|co nen khong)\s*$", "", unaccent(target.anchor)).strip()
    clicks = load_gsc_clicks()
    if LIVE_LINKS.exists() and not args.finalized:
        res = live_backfill(target, q, core, clicks)
        top = res[: args.top]
        if args.json:
            print(json.dumps(top, ensure_ascii=False, indent=2))
            return
        print(f"# Backfill candidates → {target.url}  (nguồn: snapshot live, {live_age()})\n")
        print(f"Target anchor: **{target.anchor}** · {len(res)} bài live có đoạn liên quan, chưa link ngữ cảnh tới bài này\n")
        print("| # | Bài nguồn (live) | Mục | Clicks | Đoạn gợi ý chèn link | Ghi chú |")
        print("|---|---|---|---:|---|---|")
        for n, r in enumerate(top, 1):
            ex = r["excerpt"].replace("|", "\\|")
            note = "đang link qua dòng Xem thêm → chuyển vào câu" if r["xem_them_only"] else ""
            print(f"| {n} | {r['source']} | {r['section'][:40]} | {r['clicks'] if clicks else '-'} | "
                  f"{ex[:160]}{'…' if len(ex) > 160 else ''} | {note} |")
        if not top:
            print("Không có bài nào phù hợp — bỏ qua Part B.")
        else:
            print("\nSửa trên CMS: bọc anchor quanh cụm có sẵn trong đoạn (không đổi chữ), xong chạy "
                  "`python scripts/sync_live.py --only <các slug đã sửa>`. HTML hiện tại: knowledge/raw/live/html/<slug>.html")
        return
    results = []
    for path in sorted(FINALIZED_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if target.url.rstrip("/") in text or target.slug in path.stem:
            continue
        src_url = ""
        m = re.search(r"^Slug:\s*(.+)$", text, re.M)
        if m:
            src_url = DSC_KB + m.group(1).strip()
        best = None
        lines = text.splitlines()
        body_start = 0
        if lines and lines[0].strip() == "---":  # skip YAML front matter
            body_start = next((k + 1 for k in range(1, len(lines)) if lines[k].strip() == "---"), 0)
        for ln, line in enumerate(lines, 1):
            s = line.strip()
            if ln <= body_start or not s or s.startswith(("#", "|", "!", ">", "```", "---")):
                continue
            plain = unaccent(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)).replace("-", " ")
            hit = 2.0 if core and core in plain else 0.0
            hit += len(q & tokens(plain)) / max(1, len(q))
            if hit >= 1.0 and (best is None or hit > best[0]):
                best = (hit, ln, s)
        if best:
            results.append((best[0], clicks.get(src_url.rstrip("/"), 0), path.name, best[1], best[2]))
    results.sort(key=lambda r: (-r[1], -r[0], r[2]))
    top = results[: args.top]
    if args.json:
        print(json.dumps([{"file": f, "line": ln, "score": sc, "clicks": c, "excerpt": ex}
                          for sc, c, f, ln, ex in top], ensure_ascii=False, indent=2))
        return
    print(f"# Backfill candidates → {target.url}\n")
    print(f"Target anchor: **{target.anchor}** · {len(results)} bài có đoạn liên quan, chưa link tới bài này\n")
    print("| # | Bài nguồn | Dòng | Clicks | Đoạn gợi ý chèn link |")
    print("|---|---|---:|---:|---|")
    for n, (sc, c, f, ln, ex) in enumerate(top, 1):
        ex = ex.replace("|", "\\|")
        print(f"| {n} | {f} | {ln} | {c if clicks else '-'} | {ex[:160]}{'…' if len(ex) > 160 else ''} |")
    if not top:
        print("Không có bài nào phù hợp — bỏ qua Part B.")
    else:
        print("\nAnchor text phải lấy từ chính câu trong bài nguồn (không exact-match keyword). Chỉ sửa đúng dòng đã nêu.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keyword", nargs="?", help="Keyword / topic to find link targets for")
    ap.add_argument("--backfill", metavar="SLUG", help="Find finalized articles that should link to SLUG")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--exclude", help="Slug of the article being written (skip self-links)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--finalized", action="store_true",
                    help="--backfill quét 3-finalized/*.md thay vì snapshot live (mặc định: live nếu có)")
    args = ap.parse_args()
    if not args.keyword and not args.backfill:
        ap.error("cần keyword hoặc --backfill <slug>")
    if not ANCHOR_INDEX.exists():
        print(f"Không tìm thấy {ANCHOR_INDEX}", file=sys.stderr)
        sys.exit(2)
    entries, sitemap = load_index(), load_sitemap()
    if args.backfill:
        if args.top == 8:
            args.top = 5
        mode_backfill(args, entries, sitemap)
    else:
        mode_search(args, entries, sitemap)


if __name__ == "__main__":
    main()
