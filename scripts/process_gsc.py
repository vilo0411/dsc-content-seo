"""
Analyze GSC cache CSVs and generate knowledge/3-pipeline/gsc-opportunities.md.

Usage:
    python scripts/process_gsc.py
    python scripts/process_gsc.py --min-impressions=200 --max-ctr=0.04
"""

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

CACHE_DIR = Path("knowledge/raw/gsc")
QUERIES_CSV = CACHE_DIR / "queries.csv"
PAGES_CSV = CACHE_DIR / "pages.csv"
META_FILE = CACHE_DIR / "cache-meta.json"
OUTPUT_FILE = Path("knowledge/3-pipeline/gsc-opportunities.md")
ANCHOR_INDEX = Path("knowledge/3-pipeline/anchor-index.md")

BASE_URL = "https://www.dsc.com.vn/kien-thuc/"


def load_csv(filepath):
    if not filepath.exists():
        return []
    with open(filepath, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def url_to_slug(url):
    return url.rstrip("/").split("/")[-1]


def extract_anchor_index_slugs():
    """Extract all known slugs from anchor-index.md (lines containing dsc.com.vn URLs)."""
    if not ANCHOR_INDEX.exists():
        return set()
    slugs = set()
    with open(ANCHOR_INDEX, encoding="utf-8") as f:
        for line in f:
            if "dsc.com.vn/kien-thuc/" in line:
                parts = line.split("dsc.com.vn/kien-thuc/")
                if len(parts) > 1:
                    slug = parts[1].split("|")[0].split(")")[0].strip().rstrip("/")
                    if slug:
                        slugs.add(slug)
    return slugs


def find_ctr_gaps(pages, min_impressions, max_ctr, top_n=20):
    gaps = [
        p for p in pages
        if int(p["impressions"]) >= min_impressions
        and float(p["ctr"]) <= max_ctr
        and float(p["position"]) <= 30
    ]
    gaps.sort(key=lambda x: int(x["impressions"]), reverse=True)
    return gaps[:top_n]


def find_position_gaps(pages, top_n=20):
    gaps = [
        p for p in pages
        if 4 <= float(p["position"]) <= 15
        and int(p["clicks"]) < 30
        and int(p["impressions"]) >= 100
    ]
    gaps.sort(key=lambda x: float(x["position"]))
    return gaps[:top_n]


def find_sleeping_keywords(queries, pages_by_url, top_n=20):
    """Queries ranking for a page but likely not the page's primary target keyword."""
    page_top_query = {}
    for row in queries:
        url = row["page"]
        if url not in page_top_query or int(row["clicks"]) > int(page_top_query[url]["clicks"]):
            page_top_query[url] = row

    sleeping = []
    seen = set()
    for row in queries:
        url = row["page"]
        query = row["query"]
        key = f"{url}|{query}"
        if key in seen:
            continue
        seen.add(key)

        top = page_top_query.get(url, {})
        # A query is "sleeping" if it's not the top query for that page, has decent position, and clicks
        if (top.get("query") != query
                and float(row["position"]) <= 20
                and int(row["clicks"]) >= 5
                and int(row["impressions"]) >= 50):
            sleeping.append(row)

    sleeping.sort(key=lambda x: int(x["clicks"]), reverse=True)
    return sleeping[:top_n]


def find_backfill_candidates(pages, anchor_slugs, top_n=20):
    """Pages with good traffic that may lack inbound internal links."""
    candidates = [
        p for p in pages
        if int(p["clicks"]) >= 30
        and "kien-thuc" in p["page"]
    ]
    candidates.sort(key=lambda x: int(x["clicks"]), reverse=True)
    return candidates[:top_n]


def format_ctr(val):
    return f"{float(val)*100:.1f}%"


def format_pos(val):
    return f"{float(val):.1f}"


def build_report(ctr_gaps, position_gaps, sleeping_kws, backfill, meta):
    period = "N/A"
    if meta:
        days = meta.get("days", 30)
        cached_at = meta.get("cached_at", "")[:10]
        period = f"{days} ngày trước → {cached_at}"

    lines = [
        f"---",
        f"generated: {datetime.now().strftime('%Y-%m-%d')}",
        f"period: {period}",
        f"---",
        "",
        "# GSC Opportunities Report",
        "",
        "> File này được tạo tự động bởi `scripts/process_gsc.py`. Không sửa tay.",
        "> Để refresh: chạy `/gsc-sync` hoặc `python scripts/sync_gsc.py && python scripts/process_gsc.py`",
        "",
    ]

    # Section 1: CTR Gap
    lines += [
        "## 1. Optimize ngay — CTR Gap",
        "",
        "Bài có impressions cao nhưng CTR thấp → cơ hội rewrite title/meta description.",
        "",
        "| URL Slug | Impr | CTR | Pos | Đề xuất |",
        "|----------|------|-----|-----|---------|",
    ]
    for p in ctr_gaps:
        slug = url_to_slug(p["page"])
        suggestion = "Rewrite title (CTR thấp)" if float(p["ctr"]) < 0.02 else "Cải thiện meta description"
        lines.append(f"| {slug} | {p['impressions']} | {format_ctr(p['ctr'])} | {format_pos(p['position'])} | {suggestion} |")
    if not ctr_gaps:
        lines.append("| — | — | — | — | Không có dữ liệu đủ ngưỡng |")
    lines.append("")

    # Section 2: Position Gap
    lines += [
        "## 2. Tăng authority — Position Gap",
        "",
        "Bài đang ở position 4–15 nhưng clicks thấp → cần thêm internal links + E-E-A-T.",
        "",
        "| URL Slug | Impr | Clicks | Pos | Đề xuất |",
        "|----------|------|--------|-----|---------|",
    ]
    for p in position_gaps:
        slug = url_to_slug(p["page"])
        lines.append(f"| {slug} | {p['impressions']} | {p['clicks']} | {format_pos(p['position'])} | Thêm internal links + strengthen section |")
    if not position_gaps:
        lines.append("| — | — | — | — | Không có dữ liệu đủ ngưỡng |")
    lines.append("")

    # Section 3: Sleeping keywords
    lines += [
        "## 3. Keyword ngủ quên",
        "",
        "Query đang rank cho bài nhưng KHÔNG phải target keyword chính → thêm H2/section mới.",
        "",
        "| URL Slug | Query đang rank | Clicks | Pos | Đề xuất |",
        "|----------|----------------|--------|-----|---------|",
    ]
    for row in sleeping_kws:
        slug = url_to_slug(row["page"])
        lines.append(f"| {slug} | {row['query']} | {row['clicks']} | {format_pos(row['position'])} | Thêm H2 target query này |")
    if not sleeping_kws:
        lines.append("| — | — | — | — | Không có dữ liệu đủ ngưỡng |")
    lines.append("")

    # Section 4: Backfill internal link
    lines += [
        "## 4. Backfill Internal Link — Trang traffic cao",
        "",
        "Trang đang nhận clicks cao → ưu tiên làm nguồn link cho bài mới hoặc optimize.",
        "",
        "| URL Slug | Clicks/kỳ | Impr | CTR | Đề xuất |",
        "|----------|-----------|------|-----|---------|",
    ]
    for p in backfill:
        slug = url_to_slug(p["page"])
        lines.append(f"| {slug} | {p['clicks']} | {p['impressions']} | {format_ctr(p['ctr'])} | Dùng làm nguồn backfill link |")
    if not backfill:
        lines.append("| — | — | — | — | Không có dữ liệu đủ ngưỡng |")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate GSC opportunity report")
    parser.add_argument("--min-impressions", type=int, default=300, help="Min impressions for CTR gap (default: 300)")
    parser.add_argument("--max-ctr", type=float, default=0.04, help="Max CTR for CTR gap (default: 0.04 = 4%%)")
    args = parser.parse_args()

    if not QUERIES_CSV.exists() or not PAGES_CSV.exists():
        print("[ERROR] Cache files not found. Run 'python scripts/sync_gsc.py' first.")
        return

    meta = json.loads(META_FILE.read_text()) if META_FILE.exists() else {}
    queries = load_csv(QUERIES_CSV)
    pages = load_csv(PAGES_CSV)

    print(f"[INFO] Loaded {len(queries)} query rows, {len(pages)} page rows")

    pages_by_url = {p["page"]: p for p in pages}
    anchor_slugs = extract_anchor_index_slugs()

    ctr_gaps = find_ctr_gaps(pages, args.min_impressions, args.max_ctr)
    position_gaps = find_position_gaps(pages)
    sleeping_kws = find_sleeping_keywords(queries, pages_by_url)
    backfill = find_backfill_candidates(pages, anchor_slugs)

    report = build_report(ctr_gaps, position_gaps, sleeping_kws, backfill, meta)

    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"[OK] Report written: {OUTPUT_FILE}")
    print(f"     CTR gaps: {len(ctr_gaps)} | Position gaps: {len(position_gaps)} | "
          f"Sleeping KWs: {len(sleeping_kws)} | Backfill candidates: {len(backfill)}")


if __name__ == "__main__":
    main()
