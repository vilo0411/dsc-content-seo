#!/usr/bin/env python3
"""Vietnamese financial news via RSS - for freshness signals, not for copying content.

What it is FOR:
  1. Dated event anchors: an article claiming "thị trường đang điều chỉnh" can cite a real
     headline with a real date instead of a vague assertion (see `SLOP-anchor`).
  2. Angle / PAA discovery: what the press is covering this week on a keyword, so a new
     article says something the SERP does not already repeat.
  3. Spotting Final articles that went stale: if a topic has fresh coverage and our article
     has no marker newer than 18 months, it needs an update (`market_facts.py --verify`).

What it is NOT for: rewriting news into blog posts. DSC content is evergreen educational
material; a headline is a citation with a date, never a source of paragraphs.

Usage:
    python scripts/news_feed.py --topic "margin" [--days 14] [--limit 15] [--json]
    python scripts/news_feed.py --latest [--limit 20]
    python scripts/news_feed.py --feeds            # health check from each source
    python scripts/news_feed.py --refresh

Exit:   0 = OK   2 = usage   3 = every feed unreachable (soft failure, do not block)
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, setup_utf8, unaccent  # noqa: E402

setup_utf8()

CACHE = ROOT / "scripts/news-cache.json"
CACHE_TTL = 6 * 3600
TIMEOUT = 12

# Verified reachable 2026-10-15. VnEconomy (SSL chain) and Thanh Nien (truncated response)
# are intentionally left out; add them back only if they start responding cleanly.
FEEDS = [
    ("CafeF chứng khoán", "https://cafef.vn/thi-truong-chung-khoan.rss"),
    ("CafeF doanh nghiệp", "https://cafef.vn/doanh-nghiep.rss"),
    ("VnExpress kinh doanh", "https://vnexpress.net/rss/kinh-doanh.rss"),
    ("Vietstock cổ phiếu", "https://vietstock.vn/830/chung-khoan/co-phieu.rss"),
    ("Tuổi Trẻ kinh doanh", "https://tuoitre.vn/rss/kinh-doanh.rss"),
    ("Dân Trí kinh doanh", "https://dantri.com.vn/rss/kinh-doanh.rss"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "vi,en;q=0.9",
}

RE_ITEM = re.compile(r"<item>(.*?)</item>", re.S | re.I)
RE_TAG = re.compile(r"<{t}[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{t}>", re.S | re.I)


def _field(block: str, tag: str) -> str:
    m = re.search(RE_TAG.pattern.format(t=tag), block, re.S | re.I)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def fetch_feed(url: str) -> list[dict]:
    socket.setdefaulttimeout(TIMEOUT)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        body = r.read().decode("utf-8", "replace")
    out = []
    for block in RE_ITEM.findall(body):
        title = _field(block, "title")
        if not title:
            continue
        link = _field(block, "link") or _field(block, "guid")
        pub = _field(block, "pubDate")
        ts = 0.0
        if pub:
            try:
                ts = parsedate_to_datetime(pub).timestamp()
            except (TypeError, ValueError):
                ts = 0.0
        out.append({"title": title, "url": link, "ts": ts})
    return out


def load_all(refresh: bool = False) -> tuple[list[dict], list[str]]:
    cache = {}
    if CACHE.exists() and not refresh:
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}
    if cache and (time.time() - cache.get("_at", 0)) < CACHE_TTL:
        return cache["items"], cache.get("errors", [])

    items: list[dict] = []
    errors: list[str] = []
    for name, url in FEEDS:
        try:
            for it in fetch_feed(url):
                it["source"] = name
                items.append(it)
        except (urllib.error.URLError, urllib.error.HTTPError, socket.error, OSError, ValueError) as e:
            errors.append(f"{name}: {type(e).__name__}")
    if not items:
        return [], errors
    items.sort(key=lambda x: x["ts"], reverse=True)
    CACHE.write_text(json.dumps({"_at": time.time(), "items": items, "errors": errors},
                                ensure_ascii=False), encoding="utf-8")
    return items, errors


def match(item: dict, terms: list[str]) -> bool:
    t = unaccent(item["title"])
    return all(any(unaccent(w) in t for w in term.split("|")) for term in terms)


def show(items: list[dict], limit: int, as_json: bool, errors: list[str]) -> int:
    if as_json:
        print(json.dumps({"count": len(items), "items": items[:limit], "errors": errors},
                         ensure_ascii=False, indent=2))
        return 0
    if not items:
        print("Không có tin khớp trong khoảng thời gian yêu cầu.")
    for it in items[:limit]:
        day = datetime.fromtimestamp(it["ts"], timezone.utc).strftime("%d/%m") if it["ts"] else "  ?  "
        print(f"{day}  {it['source'][:22]:<22} {it['title'][:88]}")
        print(f"{'':6}{it['url']}")
    for e in errors:
        print(f"[soft] feed lỗi — {e}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topic", help="từ khóa; dùng | cho OR, nhiều --topic nối bằng AND")
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--feeds", action="store_true", help="health check từng nguồn")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    if a.feeds:
        for name, url in FEEDS:
            try:
                n = len(fetch_feed(url))
                print(f"{name:24} OK  {n:3} item")
            except Exception as e:                       # noqa: BLE001 - health check
                print(f"{name:24} ERR {type(e).__name__}: {str(e)[:50]}")
        return 0

    items, errors = load_all(a.refresh)
    if not items:
        print("Không truy cập được feed nào — bỏ qua bước tin tức, KHÔNG chặn pipeline.", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 3

    cutoff = (datetime.now(timezone.utc) - timedelta(days=a.days)).timestamp()
    items = [i for i in items if i["ts"] >= cutoff or not i["ts"]]
    if a.topic:
        terms = [a.topic] if isinstance(a.topic, str) else a.topic
        items = [i for i in items if match(i, terms)]
    elif not a.latest:
        ap.error("cần --topic hoặc --latest")
    return show(items, a.limit, a.json, errors)


if __name__ == "__main__":
    sys.exit(main())
