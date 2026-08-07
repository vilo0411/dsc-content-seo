#!/usr/bin/env python3
"""
Fallback scraper dùng Firecrawl API khi Jina AI Reader quá tải.
Firecrawl xử lý được JavaScript, Cloudflare, và bot protection.
Output format tương thích với SKILL.md — dùng được trực tiếp cho Outline generation.

Usage:
    python scrape.py https://url1.com https://url2.com
    python scrape.py --file urls.txt
    python scrape.py --wait 2000 https://url1.com   # trang load chậm

Setup:
    pip install firecrawl-py
    Thêm FIRECRAWL_API_KEY vào .antigravity/config/api-keys.md
"""

import sys
import os
import re
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

try:
    from firecrawl import FirecrawlApp
except ImportError:
    print("Thiếu thư viện. Chạy: pip install firecrawl-py")
    sys.exit(1)

DATA_PATTERN = re.compile(
    r"\d[\d.,]*\s*(%|tỷ|triệu|nghìn|VND|USD|điểm|lần|năm|tháng|ngày|bp)"
)

SKIP_DOMAINS = {"google.com", "facebook.com", "youtube.com", "tiktok.com"}

# Tags cần loại bỏ thêm ngoài onlyMainContent
EXCLUDE_TAGS = [
    "nav", "header", "footer", "aside",
    ".related", ".sidebar", ".comment", ".social-share",
    ".tags", ".breadcrumb", ".author-box", ".newsletter",
    "#cookie-banner", ".advertisement",
]


def load_api_key() -> str:
    key = os.environ.get("FIRECRAWL_API_KEY", "")
    if key:
        return key

    config_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "../../../config/api-keys.md")
    )
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if line.startswith("FIRECRAWL_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return ""


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    return parsed.scheme in ("http", "https") and domain not in SKIP_DOMAINS


def scrape_url(app: FirecrawlApp, url: str, wait_ms: int) -> tuple[str, dict | None]:
    try:
        params = {
            "formats": ["markdown", "links"],
            "onlyMainContent": True,
            "excludeTags": EXCLUDE_TAGS,
            "location": {
                "country": "VN",
                "languages": ["vi", "vi-VN"],
            },
        }
        if wait_ms > 0:
            params["waitFor"] = wait_ms

        result = app.scrape_url(url, params=params)
        markdown = result.get("markdown", "") or ""
        if len(markdown) < 200:
            return url, None
        return url, {
            "markdown": markdown,
            "links": result.get("links", []),
        }
    except Exception as e:
        return url, None


def extract(url: str, data: dict) -> dict:
    domain = urlparse(url).netloc.replace("www.", "")
    md = data["markdown"]
    links = data.get("links", [])

    # Headings
    headings = []
    for line in md.splitlines():
        m = re.match(r"^(#{1,4})\s+(.+)", line)
        if m:
            level = f"H{len(m.group(1))}"
            text = m.group(2).strip()
            if len(text) > 3:
                headings.append((level, text))

    # Data points — số liệu có đơn vị tài chính/VN
    data_points = []
    seen = set()
    for line in md.splitlines():
        if DATA_PATTERN.search(line):
            sentence = line.strip()[:200]
            if sentence and sentence not in seen:
                data_points.append(sentence)
                seen.add(sentence)

    # Special elements
    specials = []
    lower = md.lower()
    if any(w in lower for w in ["faq", "câu hỏi thường", "hỏi đáp"]):
        specials.append("FAQ")
    if any(w in lower for w in ["bảng so sánh", "so sánh"]):
        specials.append("Bảng so sánh")
    if any(w in lower for w in ["calculator", "tính toán", "công cụ tính"]):
        specials.append("Calculator")

    # Internal links (cùng domain) — hữu ích cho internal linking audit
    internal_links = [
        l for l in links
        if domain in l and l != url
    ]

    return {
        "url": url,
        "domain": domain,
        "headings": headings,
        "data_points": data_points[:8],
        "special_elements": specials,
        "internal_links": internal_links[:10],
    }


def format_output(result: dict) -> str:
    indent = {"H1": "  ", "H2": "    ", "H3": "      ", "H4": "        "}
    lines = [
        f"### Competitor: {result['domain']}",
        f"- URL: {result['url']}",
        "- Headings:",
    ]

    for level, text in result["headings"]:
        lines.append(f"{indent.get(level, '  ')}- {level}: {text}")

    if result["data_points"]:
        lines.append("- Data points:")
        for dp in result["data_points"]:
            lines.append(f"  - {dp}")
    else:
        lines.append("- Data points: (không tìm thấy)")

    if result["special_elements"]:
        lines.append(f"- Special elements: {', '.join(result['special_elements'])}")

    if result["internal_links"]:
        lines.append("- Internal links mẫu:")
        for lnk in result["internal_links"][:5]:
            lines.append(f"  - {lnk}")

    lines.append("- Gap so với bài mình: [điền thủ công]")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Firecrawl scraper fallback cho SERP research")
    parser.add_argument("urls", nargs="*", help="Danh sách URLs")
    parser.add_argument("--file", "-f", help="File chứa URLs (mỗi dòng 1 URL)")
    parser.add_argument("--wait", type=int, default=0, help="Thêm waitFor (ms) cho trang load chậm, ví dụ: --wait 2000")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.file:
        with open(args.file) as f:
            urls += [line.strip() for line in f if line.strip() and not line.startswith("#")]

    urls = [u for u in urls if is_valid_url(u)]
    if not urls:
        print("Không có URL hợp lệ.")
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        print("Thiếu FIRECRAWL_API_KEY. Thêm vào .antigravity/config/api-keys.md hoặc set env var.")
        sys.exit(1)

    app = FirecrawlApp(api_key=api_key)

    wait_info = f" (waitFor: {args.wait}ms)" if args.wait else ""
    print(f"\n⏳ Đang scrape {len(urls)} URLs song song qua Firecrawl{wait_info}...\n")

    raw: dict[str, dict | None] = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_url, app, url, args.wait): url for url in urls}
        for future in as_completed(futures):
            url, data = future.result()
            raw[url] = data

    print("=" * 60)
    for url in urls:
        data = raw.get(url)
        if data:
            print(format_output(extract(url, data)))
        else:
            domain = urlparse(url).netloc.replace("www.", "")
            print(f"### Competitor: {domain}")
            print(f"- URL: {url}")
            print("- Lỗi: Không scrape được")
        print()

    success = sum(1 for d in raw.values() if d)
    print(f"✅ Hoàn tất: {success}/{len(urls)} URLs extract thành công")


if __name__ == "__main__":
    main()
