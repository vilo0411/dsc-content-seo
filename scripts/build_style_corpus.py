#!/usr/bin/env python3
"""Crawl authentic Vietnamese financial press & brokerage research analysis
(Vietstock Fundamental Analysis 582, Vietstock Technical Analysis 585, Vietstock Market/Derivatives 1636,
CafeF Securities/Enterprise/Banking, VnExpress Business) and extract clean, high-density,
zero-translationese paragraphs as few-shot style anchors for DSC writers.

Usage:
    python3 scripts/build_style_corpus.py [--per-feed 12]
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "knowledge/raw/style-corpus"

FEEDS = [
    ("Vietstock Phân tích cơ bản (BCTC & Cổ phiếu)", "https://vietstock.vn/582/chung-khoan/phan-tich-co-ban.rss", "analytical_fa"),
    ("Vietstock Phân tích kỹ thuật (Chỉ báo & Đồ thị)", "https://vietstock.vn/585/chung-khoan/phan-tich-ky-thuat.rss", "analytical_ta"),
    ("Vietstock Nhận định, Phái sinh & Chứng quyền", "https://vietstock.vn/1636/chung-khoan/nhan-dinh-phan-tich.rss", "analytical_market"),
    ("CafeF Thị trường chứng khoán", "https://cafef.vn/thi-truong-chung-khoan.rss", "securities"),
    ("CafeF Doanh nghiệp niêm yết", "https://cafef.vn/doanh-nghiep.rss", "enterprise"),
    ("CafeF Tài chính ngân hàng", "https://cafef.vn/tai-chinh-ngan-hang.rss", "banking"),
    ("VnExpress Kinh doanh", "https://vnexpress.net/rss/kinh-doanh.rss", "macro_business"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi,en;q=0.9",
}

RE_ITEM = re.compile(r"<item>(.*?)</item>", re.S | re.I)
RE_TAG = re.compile(r"<{t}[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{t}>", re.S | re.I)

TRANSLATIONESE_BAD = re.compile(
    r"(?i)\b(vạch chia|bức tranh toàn cảnh|mở khóa|điều hướng|chìa khóa vàng|"
    r"trong kỷ nguyên|không thể phủ nhận|đóng vai trò then chốt|một cách hiệu quả|"
    r"nơi mà|điều mà|thứ mà|được xem là|được coi như|được thực hiện bởi)\b"
)
NUM_OR_FIN_TERM = re.compile(
    r"(\d[\d.,]*\s*(%|tỷ|triệu|nghìn|đồng|VNĐ|USD|điểm|cp|cổ phiếu|năm|tháng|phiên|lần|tấn)\b|"
    r"\b(MACD|RSI|Bollinger Bands|SMA|EMA|Doji|Fibonacci|P/E|P/B|ROE|ROA|biên lợi nhuận|thanh khoản|kháng cự|hỗ trợ|vùng\s+\d[\d.,-]*)\b)",
    re.I,
)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _field(block: str, tag: str) -> str:
    m = re.search(RE_TAG.pattern.format(t=tag), block, re.S | re.I)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def fetch_rss_urls(per_feed: int = 12) -> list[dict]:
    socket.setdefaulttimeout(12)
    items = []
    seen = set()
    for source, url, feed_cat in FEEDS:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                xml = resp.read().decode("utf-8", "replace")
            count = 0
            for blk in RE_ITEM.findall(xml):
                title = _field(blk, "title")
                link = _field(blk, "link") or _field(blk, "guid")
                if not link.startswith("http") or link in seen:
                    continue
                seen.add(link)
                items.append({"source": source, "feed_cat": feed_cat, "title": title, "url": link})
                count += 1
                if count >= per_feed:
                    break
        except Exception as e:
            print(f"[warn] RSS {source}: {e}", file=sys.stderr)
    return items


def fetch_article_paragraphs(item: dict) -> dict:
    url = item["url"]
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8", "replace")
    except Exception as e:
        return {**item, "paragraphs": [], "error": str(e)}

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside", "figcaption"]):
        tag.decompose()

    selectors = [
        "#vst_detail", "article.fck_detail", ".detail-content", ".singular-content",
        '[itemprop="articleBody"]', ".article-content", ".post-content", "article"
    ]
    container = None
    for sel in selectors:
        found = soup.select_one(sel)
        if found and len(found.get_text(" ", strip=True).split()) >= 100:
            container = found
            break
    if not container:
        container = soup.body or soup

    raw_ps = []
    for p in container.find_all("p"):
        txt = re.sub(r"\s+", " ", p.get_text(" ", strip=True)).strip()
        if len(txt.split()) < 10:
            continue
        if any(bad in txt.lower() for bad in ("ảnh:", "nguồn:", "xem thêm", "đọc thêm", "theo dõi trên", "bộ phận phân tích", "miễn trừ trách nhiệm", ">>>", "phòng tư vấn vietstock")):
            continue
        raw_ps.append(txt)

    # For Vietstock TA/FA where each sentence is a <p>, merge consecutive short paragraphs (10-25w) into 2-3 sentence blocks
    merged_ps = []
    buf = []
    for txt in raw_ps:
        w = len(txt.split())
        if w < 28 and (not buf or sum(len(x.split()) for x in buf) + w <= 75):
            buf.append(txt)
            if sum(len(x.split()) for x in buf) >= 30:
                merged_ps.append(" ".join(buf))
                buf = []
        else:
            if buf:
                merged_ps.append(" ".join(buf))
                buf = []
            merged_ps.append(txt)
    if buf:
        merged_ps.append(" ".join(buf))

    paras = []
    for txt in merged_ps:
        words = txt.split()
        if not (25 <= len(words) <= 85):
            continue
        if TRANSLATIONESE_BAD.search(txt):
            continue
        sents = [s for s in SENT_SPLIT.split(txt) if s.strip()]
        if not (1 <= len(sents) <= 4):
            continue
        if any(len(s.split()) > 34 for s in sents):
            continue
        nums = len(NUM_OR_FIN_TERM.findall(txt))
        if nums < 2:
            continue
        paras.append({"text": txt, "words": len(words), "sents": len(sents), "nums": nums})

    return {**item, "paragraphs": paras}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-feed", type=int, default=12)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rss_items = fetch_rss_urls(args.per_feed)
    print(f"Fetched {len(rss_items)} URLs from {len(FEEDS)} feeds.")

    with ThreadPoolExecutor(max_workers=10) as pool:
        articles = list(pool.map(fetch_article_paragraphs, rss_items))

    by_cat: dict[str, list[dict]] = {}
    total_paras = 0
    for art in articles:
        cat = art["feed_cat"]
        by_cat.setdefault(cat, [])
        for p in art.get("paragraphs", []):
            total_paras += 1
            by_cat[cat].append({
                "source": art["source"],
                "title": art["title"],
                "url": art["url"],
                **p,
            })

    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: (-x["nums"], abs(x["words"] - 50)))

    out_file = OUT_DIR / "vn_press_corpus.json"
    out_file.write_text(
        json.dumps(
            {
                "articles_crawled": len(articles),
                "paragraphs_extracted": total_paras,
                "categories": {k: v[:20] for k, v in by_cat.items()},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Saved {total_paras} filtered paragraphs across {len(by_cat)} categories to {out_file}")
    for k, v in by_cat.items():
        print(f"\n=== Category: {k} ({len(v)} paragraphs) ===")
        for sample in v[:3]:
            print(f"- [{sample['title'][:55]}...] ({sample['words']}w): {sample['text']}")


if __name__ == "__main__":
    main()
