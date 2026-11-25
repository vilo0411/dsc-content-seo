#!/usr/bin/env python3
"""Query the article registry (knowledge/3-seo/strategy/pages.csv, scripts/registry.py) for internal links.

Modes:
  python scripts/find_links.py "từ khóa" [--top 8] [--exclude slug] [--json]
      → best-matching published articles to link TO from a new/optimized draft.

  python scripts/find_links.py --backfill <slug> [--top 5] [--json] [--finalized]
      → published articles that should link TO <slug> but don't yet (no in-sentence link), with
        the section + paragraph where an anchor could be wrapped. Scans the live snapshot
        (knowledge/raw/live, sync_live.py); --finalized falls back to 3-finalized/*.md.

Sources: knowledge/3-seo/strategy/pages.csv (registry.py), sitemap-cache.json,
         knowledge/raw/live/{html/,links.csv,pages.csv} (backfill + inlink column),
         knowledge/3-seo/content/3-finalized/*.md (backfill --finalized only),
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry  # noqa: E402  single source: strategy/pages.csv
LIVE_DIR = ROOT / "knowledge/raw/live"
LIVE_HTML = LIVE_DIR / "html"
LIVE_LINKS = LIVE_DIR / "links.csv"
LIVE_PAGES = LIVE_DIR / "pages.csv"
LIVE_META = LIVE_DIR / "_meta.json"
SITEMAP_CACHE = ROOT / ".agents/skills/link/scripts/sitemap-cache.json"
FINALIZED_DIR = ROOT / "knowledge/3-seo/content/3-finalized"
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
    """One Entry per registry row (Merged rows excluded); cluster = "<subgroup> <subgroup name>"."""
    entries = []
    for i, r in enumerate(registry.load(), 2):
        if r["status"] == "Merged":
            continue
        cluster = f"{r['subgroup']} {r['subgroup_name']}".strip() or f"{r['cluster']} {r['cluster_name']}".strip()
        anchor = r["anchor"] or r["key_chinh"] or r["title"]
        related = " | ".join(x for x in (r["key_chinh"], r["key_phu"], r["keywords"], r["title"]) if x and x != anchor)
        status = "Live Published" if r["live"] == "yes" else r["status"]
        entries.append(Entry(cluster, anchor, registry.url(r), related, status, i))
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
        print("Không có bài liên quan trong registry. Cân nhắc link về hub cluster hoặc bỏ qua.")
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
            print(f"Không tìm thấy slug '{args.backfill}' trong registry pages.csv"
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


def add_anchor(args, entries) -> int:
    """Set anchor + cluster of one article in the registry (adds the row if missing)."""
    slug = args.add_anchor.strip("/").split("/")[-1]
    if not args.anchor or not args.cluster:
        print("--add-anchor cần --anchor \"<anchor chính>\" và --cluster \"<subgroup / tên cluster>\"", file=sys.stderr)
        return 2
    rows = registry.load()
    hit = registry.match_cluster(rows, args.cluster)
    if not hit:
        names = sorted({f"{r['subgroup']} {r['subgroup_name']}" for r in rows if r["subgroup"]})
        print(f"--cluster '{args.cluster}' không khớp đúng 1 nhóm. Ví dụ hợp lệ: 3b, 10a hoặc tên nhóm:", file=sys.stderr)
        print("  " + "\n  ".join(names), file=sys.stderr)
        return 1
    found = registry.find(rows, slug)
    row = found[0] if len(found) == 1 else None
    if row is None:
        row = {k: "" for k in registry.FIELDS} | {"slug": slug, "file_slug": slug, "live": "no", "status": "Finalized"}
        rows.append(row)
    row["anchor"] = args.anchor
    row["key_chinh"] = row["key_chinh"] or args.anchor
    row["title"] = row["title"] or (args.title or "")
    if not row["cluster"] or hit[2]:
        row["cluster"], row["cluster_name"], row["subgroup"], row["subgroup_name"] = hit
    registry.save(rows)
    print(f"Registry: {row['slug']} · anchor “{args.anchor}” · {row['subgroup'] or row['cluster']} {row['subgroup_name'] or row['cluster_name']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keyword", nargs="?", help="Keyword / topic to find link targets for")
    ap.add_argument("--backfill", metavar="SLUG", help="Find finalized articles that should link to SLUG")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--exclude", help="Slug of the article being written (skip self-links)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--finalized", action="store_true",
                    help="--backfill quét 3-finalized/*.md thay vì snapshot live (mặc định: live nếu có)")
    ap.add_argument("--add-anchor", metavar="SLUG", help="Đặt anchor + cluster cho bài trong registry pages.csv (cần --anchor, --cluster)")
    ap.add_argument("--anchor", help="Anchor text chính cho --add-anchor")
    ap.add_argument("--cluster", help="Mã subgroup (3b) hoặc tên nhóm/cluster (khớp 1 phần, không dấu) cho --add-anchor")
    ap.add_argument("--title", help="Title bài (cột Từ khóa liên quan) cho --add-anchor; mặc định = anchor")
    args = ap.parse_args()
    if not args.keyword and not args.backfill and not args.add_anchor:
        ap.error("cần keyword, --backfill <slug> hoặc --add-anchor <slug>")
    entries, sitemap = load_index(), load_sitemap()
    if args.add_anchor:
        sys.exit(add_anchor(args, entries))
    if args.backfill:
        if args.top == 8:
            args.top = 5
        mode_backfill(args, entries, sitemap)
    else:
        mode_search(args, entries, sitemap)


if __name__ == "__main__":
    main()
