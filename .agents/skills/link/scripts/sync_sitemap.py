#!/usr/bin/env python3
"""Sync DSC knowledge sitemap to local cache and verify internal link URLs.

Usage:
  python sync_sitemap.py [--update-index]
"""

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

SITEMAP_URL = "https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml"
CACHE_FILE = os.path.join(os.path.dirname(__file__), "sitemap-cache.json")


def fetch_sitemap() -> list[str]:
    print(f"Fetching sitemap from {SITEMAP_URL}...")
    req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
    
    urls = re.findall(r"<loc>(https://www\.dsc\.com\.vn/kien-thuc/[^<]+)</loc>", content)
    print(f"Fetched {len(urls)} live URLs from sitemap.")
    return urls


def save_cache(urls: list[str]) -> None:
    cache_data = {}
    for url in urls:
        slug = url.replace("https://www.dsc.com.vn/kien-thuc/", "")
        cache_data[slug] = url
        # also map keywords/words inside slug
        key_words = slug.split("-")
        cache_data[" ".join(key_words)] = url
    
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"urls": urls, "mapping": cache_data}, f, ensure_ascii=False, indent=2)
    print(f"Saved sitemap cache to {CACHE_FILE}")


def search_url(term: str) -> list[str]:
    if not os.path.exists(CACHE_FILE):
        urls = fetch_sitemap()
        save_cache(urls)
    
    with open(CACHE_FILE, encoding="utf-8") as f:
        data = json.load(f)
    
    matches = []
    clean_term = term.lower().strip()
    for url in data["urls"]:
        if clean_term in url.lower():
            matches.append(url)
    return matches


if __name__ == "__main__":
    urls = fetch_sitemap()
    save_cache(urls)
