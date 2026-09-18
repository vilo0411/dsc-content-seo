#!/usr/bin/env python3
"""DataForSEO SERP (Google, Vietnam) + competitor content extraction, with cache.

Usage:
    python serp_research.py "chi so ROA la gi" [--top 10] [--extract 5] [--json] [--raw] [--no-cache]

Cost policy (DataForSEO is paid):
    - Cache first: knowledge/raw/serp/<slug>.json is reused for CACHE_DAYS days -> 0 API calls.
    - Exactly one API call per keyword (depth=10, live/advanced). No retries.
    - Extraction is local first (urllib + Scrapling parser, ~1s/page, no API) and falls
      back to Jina AI Reader (free, ~8s/page) for JS-rendered pages. Also stored in the cache.

Config (env vars, or .antigravity/config/api-keys.md as KEY=value lines):
    DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD   required
    JINA_API_KEY                            optional, raises Jina rate limit
    LOCAL_FETCH=0                           optional, skip local extraction and go straight to Jina

Local extraction needs `pip install scrapling markdownify` (parser only — do NOT install
`scrapling[fetchers]`: its TLS-impersonation deps get flagged by endpoint AV on managed machines).
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

API_URL = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
LOCATION_CODE = 2704   # Vietnam
LANGUAGE_CODE = "vi"
DEPTH = 10             # billed per 10 results — never over-fetch
CACHE_DAYS = 30
JINA_TIMEOUT = 40
LOCAL_TIMEOUT = 20
LOCAL_MIN_WORDS = 300  # below this the page is probably JS-rendered -> fall back to Jina
MAX_WORDS = 2000       # keep only the first N words of each competitor page

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
CONFIG = os.path.join(ROOT, ".antigravity", "config", "api-keys.md")
CACHE_DIR = os.path.join(ROOT, "knowledge", "raw", "serp")

# Domains that are never useful as competitor references.
BLOCKLIST = (
    "google.", "facebook.com", "youtube.com", "tiktok.com", "instagram.com",
    "twitter.com", "x.com", "pinterest.com", "linkedin.com",
)

DATA_PATTERN = re.compile(r"\d[\d.,]*\s*(%|tỷ|triệu|nghìn|VND|USD|điểm|lần|năm|tháng|ngày|bp)")
FOOTER_HINTS = ("bài viết liên quan", "xem thêm", "tags:", "chính sách", "liên hệ", "bình luận")


# ---------------------------------------------------------------- config / cache

def load_config():
    """Env wins; fall back to KEY=value lines in api-keys.md."""
    cfg = {}
    if os.path.exists(CONFIG):
        with open(CONFIG, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"\s*([A-Z_][A-Z0-9_]*)\s*=\s*(\S+)", line)
                if m:
                    cfg[m.group(1)] = m.group(2)
    for k in ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD", "JINA_API_KEY"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


def slugify(text):
    text = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "keyword"


def cache_path(keyword):
    return os.path.join(CACHE_DIR, slugify(keyword) + ".json")


def load_cache(keyword):
    path = cache_path(keyword)
    if not os.path.exists(path):
        return None
    age_days = (time.time() - os.path.getmtime(path)) / 86400
    if age_days > CACHE_DAYS:
        return None
    with open(path, encoding="utf-8-sig") as fh:  # tolerate BOM from hand-edited files
        return json.load(fh)


def save_cache(keyword, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path(keyword), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- DataForSEO

def fetch_serp(cfg, keyword, timeout):
    """One live/advanced call. Exits on any error — no retry, no extra cost."""
    body = json.dumps([{
        "keyword": keyword,
        "location_code": LOCATION_CODE,
        "language_code": LANGUAGE_CODE,
        "device": "desktop",
        "depth": DEPTH,
    }]).encode()
    token = base64.b64encode(
        ("%s:%s" % (cfg["DATAFORSEO_LOGIN"], cfg["DATAFORSEO_PASSWORD"])).encode()
    ).decode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": "Basic " + token,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        sys.exit("DataForSEO HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    except urllib.error.URLError as e:
        sys.exit("DataForSEO connection error: %s" % e.reason)

    if payload.get("status_code") != 20000:
        sys.exit("DataForSEO error %s: %s" % (payload.get("status_code"), payload.get("status_message")))
    task = (payload.get("tasks") or [{}])[0]
    if task.get("status_code") != 20000:
        sys.exit("DataForSEO task error %s: %s" % (task.get("status_code"), task.get("status_message")))
    return payload


def parse_serp(payload, top):
    task = payload["tasks"][0]
    result = (task.get("result") or [{}])[0]
    organic, paa, related, snippet = [], [], [], None
    for item in result.get("items") or []:
        t = item.get("type")
        if t == "organic":
            link = item.get("url") or ""
            host = urllib.parse.urlparse(link).netloc.lower()
            if not link.startswith("http") or any(b in host for b in BLOCKLIST):
                continue
            organic.append({
                "rank": item.get("rank_group") or len(organic) + 1,
                "title": (item.get("title") or "").strip(),
                "url": link,
                "domain": host,
                "description": (item.get("description") or "").strip(),
            })
        elif t == "people_also_ask":
            paa += [q.get("title") for q in item.get("items") or [] if q.get("title")]
        elif t == "related_searches":
            related += [k for k in item.get("items") or [] if isinstance(k, str)]
        elif t == "featured_snippet" and snippet is None:
            snippet = {
                "domain": item.get("domain"),
                "url": item.get("url"),
                "title": item.get("title"),
                "text": (item.get("description") or "")[:400],
            }
    return {
        "organic": organic[:top],
        "people_also_ask": paa,
        "related_searches": related,
        "featured_snippet": snippet,
        "se_results_count": result.get("se_results_count"),
        "cost": task.get("cost") or 0,
    }


# ---------------------------------------------------------------- local extraction (Scrapling parser)

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi,en;q=0.8",
}
# Removed before conversion so nav/footer never reach trim_main_content.
NOISE_TAGS = ("nav", "header", "footer", "aside", "form", "iframe", "button", "select")
NOISE_CSS = (".breadcrumb", ".related", ".sidebar", ".comment", ".comments", ".social-share",
             ".share", ".tags", ".author-box", ".newsletter", ".advertisement", ".ads", "#cookie-banner")
# Candidate content containers; the densest match wins, body is the fallback.
CONTENT_CSS = ("article", '[itemprop="articleBody"]', ".post-content", ".entry-content",
               ".article-content", ".detail-content", ".content-detail", "main", "#content")


def fetch_local(cfg, url):
    """Fetch with urllib and convert the main content to ATX markdown via Scrapling + markdownify.

    Returns None when the deps are missing, the request fails, or the page has too few words
    (JS-rendered SPA) — the caller then falls back to Jina.
    """
    if cfg.get("LOCAL_FETCH", "1") == "0":
        return None
    try:
        from scrapling.parser import Selector
        from scrapling.core.shell import Convertor
        from markdownify import markdownify
    except ImportError:
        return None
    try:
        req = urllib.request.Request(url, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=LOCAL_TIMEOUT) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "html" not in ctype and "xml" not in ctype:
                return None
            html = resp.read().decode("utf-8", "replace")
    except Exception:
        return None

    page = Convertor._sanitize_for_ai(Convertor._strip_noise_tags(Selector(html)))
    root = page._root
    for el in list(root.iter(*NOISE_TAGS)):
        el.drop_tree()
    for sel in NOISE_CSS:
        for el in list(page.css(sel)):
            el._root.drop_tree()

    # Pick the single densest candidate: sites like prudential.com.vn wrap every
    # related-post card in <article>, so "first selector that matches" is not enough.
    candidates = [n for sel in CONTENT_CSS for n in page.css(sel)]
    best = max(candidates, key=lambda n: len(n.get_all_text().split()), default=None)
    node = best or page.css("body").first or page
    md = markdownify(node.html_content, heading_style="ATX")

    title = page.css("title::text").first or page.css("h1::text").first or ""
    if title and not re.search(r"^# ", md, re.M):
        md = "# " + str(title).strip() + "\n\n" + md
    return md if len(md.split()) >= LOCAL_MIN_WORDS else None


# ---------------------------------------------------------------- Jina extraction

def fetch_jina(cfg, url):
    req = urllib.request.Request("https://r.jina.ai/" + url, headers={
        "Accept": "text/plain",
        "User-Agent": "Mozilla/5.0",
        **({"Authorization": "Bearer " + cfg["JINA_API_KEY"]} if cfg.get("JINA_API_KEY") else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=JINA_TIMEOUT) as resp:
            md = resp.read().decode("utf-8", "replace")
    except Exception:
        return None
    return md if len(md) >= 200 else None


LINK_ONLY = re.compile(r"^[\s*\-•>]*(\[[^\]]*\]\([^)]*\)[\s|·,]*)+$")
NOISE = re.compile(r"!\[|javascript:|^\s*[×✕]\s*$|^\s*Sao chép|^\s*Tải ứng dụng")


def _is_nav_line(line):
    s = line.strip()
    return bool(s) and (LINK_ONLY.match(s) is not None or len(s.split()) <= 3)


def trim_main_content(md):
    """Keep the article body only:
    - drop Jina preamble (Title:/URL Source:/Markdown Content:)
    - start at the first H1 if present
    - stop at the first footer-ish heading or at the first run of >= 5 nav-like lines
    - drop image / javascript / cookie-style noise lines
    - cap at MAX_WORDS
    """
    lines = md.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("Markdown Content:"):
            lines = lines[i + 1:]
            break
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines = lines[i:]
            break

    kept = []
    for line in lines:
        if line.startswith("#") and any(h in line.lower() for h in FOOTER_HINTS):
            break
        if not NOISE.search(line):
            kept.append(line)

    # Locate runs of >= 5 short/link-only lines (ignoring blanks) after real text has appeared.
    runs, start, run, seen_text = [], None, 0, 0
    for i, line in enumerate(kept):
        if not line.strip():
            continue
        if _is_nav_line(line):
            if run == 0:
                start = i
            run += 1
            if run == 5 and seen_text >= 3:
                runs.append(start)
        else:
            run, seen_text = 0, seen_text + 1

    def _is_footer(tail):
        """A TOC is followed by headings and real paragraphs; a footer is not."""
        has_heading = any(l.startswith("#") for l in tail)
        paragraphs = sum(1 for l in tail if len(l.split()) >= 20)
        return not has_heading and paragraphs < 3

    body = kept
    for s in runs:
        if _is_footer(kept[s:]):
            body = kept[:s]
            break

    # Trim trailing short/link-only lines left before the cut.
    while body and (not body[-1].strip() or _is_nav_line(body[-1])):
        body.pop()
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip()
    words = text.split(" ")
    return " ".join(words[:MAX_WORDS])


MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)")
ENTITY_STOP = {"H1", "H2", "H3", "H4", "VND", "USD", "XEM", "ĐỌC", "NGAY", "THÊM", "FAQ", "URL", "PDF", "ABC", "XYZ"}


def _clean_text(s):
    """Strip markdown emphasis/links so word counts and snippets are plain text."""
    s = MD_LINK.sub(r"\1", s)
    s = re.sub(r"[*_`>]+", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _first_sentence(text, limit=160):
    text = _clean_text(text)
    m = re.search(r"^(.+?[.!?])(\s|$)", text)
    s = (m.group(1) if m else text).strip()
    return s if len(s) <= limit else s[:limit].rsplit(" ", 1)[0] + "…"


def split_sections(md):
    """[{level, title, word_count, snippet}] — level 'Intro' for text before the first heading."""
    sections, cur = [], {"level": "Intro", "title": "(mở bài)", "lines": []}
    for line in md.splitlines():
        m = re.match(r"^(#{1,4})\s+(.+)", line)
        if m:
            sections.append(cur)
            title = re.sub(r"[*_]{1,3}", "", m.group(2)).strip()
            cur = {"level": "H%d" % len(m.group(1)), "title": title, "lines": []}
        else:
            cur["lines"].append(line)
    sections.append(cur)
    out = []
    for s in sections:
        body = _clean_text(" ".join(l for l in s["lines"] if l.strip()))
        if s["level"] == "Intro" and not body:
            continue
        out.append({
            "level": s["level"],
            "title": s["title"],
            "word_count": len(body.split()) if body else 0,
            "snippet": _first_sentence(body) if body else "",
        })
    return out


def _is_cap_word(w):
    return len(w) > 1 and w[0].isupper() and not w.isupper() and w[1:].islower()


def _is_acronym(w):
    # ASCII only: Vietnamese ALL-CAPS words (CHỦ, VIẾT) are shouting, not tickers.
    return 2 <= len(w) <= 6 and w.isupper() and w.isalpha() and w.isascii() and w not in ENTITY_STOP


def extract_entities(md, limit=15):
    """Proper-noun phrases (>= 2 Capitalised words, not sentence-initial) + acronyms/tickers, by frequency."""
    text = _clean_text(md)
    counts = {}
    for sentence in re.split(r"[.!?:;,]\s+|\n|[()\"“”\[\]|/]", text):
        words = re.findall(r"[\w/&.-]+", sentence)
        i = 1  # index 0 is sentence-initial → always capitalised in Vietnamese, skip it
        while i < len(words):
            w = words[i].strip(".,")
            if _is_acronym(w):
                counts[w] = counts.get(w, 0) + 1
                i += 1
                continue
            if _is_cap_word(w):
                j = i
                while j < len(words) and (_is_cap_word(words[j].strip(".,")) or _is_acronym(words[j].strip(".,"))):
                    j += 1
                if j - i >= 2:
                    phrase = " ".join(x.strip(".,") for x in words[i:j])
                    counts[phrase] = counts.get(phrase, 0) + 1
                i = j
            else:
                i += 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [{"name": k, "count": v} for k, v in ranked][:limit]


def extract_links(url, md):
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    internal, external, seen = [], [], set()
    for anchor, link in MD_LINK.findall(md):
        anchor = _clean_text(anchor)
        link = link.split("#")[0]  # same-page TOC anchors are not links
        if not link or link in seen or link.rstrip("/") == url.rstrip("/") or not anchor:
            continue
        seen.add(link)
        target = urllib.parse.urlparse(link).netloc.replace("www.", "")
        (internal if target == host else external).append({"anchor": anchor[:80], "url": link})
    return internal, external


def extract(url, md):
    data_points, seen = [], set()
    for line in md.splitlines():
        if line.startswith("#") or "](http" in line or "**" in line[:2]:
            continue
        if DATA_PATTERN.search(line):
            s = _clean_text(line)[:200]
            if s and s not in seen:
                data_points.append(s)
                seen.add(s)
    lower = md.lower()
    specials = []
    if any(w in lower for w in ("faq", "câu hỏi thường", "hỏi đáp")):
        specials.append("FAQ")
    if "so sánh" in lower:
        specials.append("So sánh")
    if any(w in lower for w in ("calculator", "công cụ tính")):
        specials.append("Calculator")
    if "\n|" in md:
        specials.append("Table")
    if re.search(r"^\s*(\*|-|\d+\.)\s", md, re.M):
        specials.append("List")
    sections = split_sections(md)
    internal, external = extract_links(url, md)
    return {
        "url": url,
        "domain": urllib.parse.urlparse(url).netloc.replace("www.", ""),
        "word_count": len(_clean_text(md).split()),
        "sections": sections,
        "headings": [(s["level"], s["title"]) for s in sections if s["level"] != "Intro"],
        "entities": extract_entities(md),
        "data_points": data_points[:8],
        "internal_links": internal[:12],
        "external_links": external[:8],
        "special_elements": specials,
        "content": md,  # trimmed main content, kept in cache for --content
    }


def fetch_page(cfg, url):
    """Local parser first (fast, no API); Jina for JS-rendered pages. Returns (markdown, source)."""
    md = fetch_local(cfg, url)
    if md:
        return md, "local"
    md = fetch_jina(cfg, url)
    return (md, "jina") if md else (None, None)


def extract_competitors(cfg, urls):
    def work(url):
        md, source = fetch_page(cfg, url)
        if not md:
            return {"url": url, "error": "Không extract được"}
        data = extract(url, trim_main_content(md))
        data["source"] = source
        return data
    with ThreadPoolExecutor(max_workers=5) as pool:
        return list(pool.map(work, urls))


# ---------------------------------------------------------------- output

def format_competitor(i, c):
    domain = c.get("domain") or urllib.parse.urlparse(c["url"]).netloc
    lines = ["### Competitor %d: %s" % (i, domain), "- URL: %s" % c["url"]]
    if c.get("error"):
        lines.append("- Lỗi: %s" % c["error"])
        return "\n".join(lines)
    indent = {"Intro": "  ", "H1": "  ", "H2": "  ", "H3": "    ", "H4": "      "}
    sections = c.get("sections") or []
    lines.append("- Tổng: ~%d từ | %d sections | %d internal links | %d external links" % (
        c["word_count"], sum(1 for s in sections if s["level"] != "Intro"),
        len(c.get("internal_links") or []), len(c.get("external_links") or [])))
    lines.append("- Outline (số từ / section — câu chủ đề):")
    for s in sections:
        label = "[Intro]" if s["level"] == "Intro" else "%s: %s" % (s["level"], s["title"])
        tail = " — " + s["snippet"] if s["snippet"] else ""
        lines.append("%s- %s (%d từ)%s" % (indent.get(s["level"], "  "), label, s["word_count"], tail))
    if c.get("entities"):
        lines.append("- Entities: " + ", ".join(
            "%s×%d" % (e["name"], e["count"]) if e["count"] > 1 else e["name"] for e in c["entities"]))
    lines.append("- Data points:" if c["data_points"] else "- Data points: (không tìm thấy)")
    lines += ["  - " + dp for dp in c["data_points"]]
    if c.get("internal_links"):
        lines.append("- Internal links (anchor → URL):")
        lines += ['  - "%s" → %s' % (l["anchor"], l["url"]) for l in c["internal_links"]]
    if c.get("external_links"):
        lines.append("- External links: " + ", ".join(
            urllib.parse.urlparse(l["url"]).netloc.replace("www.", "") for l in c["external_links"]))
    lines.append("- Special elements: %s" % (", ".join(c["special_elements"]) or "(không)"))
    lines.append("- Gap so với bài mình: [điền]")
    return "\n".join(lines)


def print_content(data):
    """Full trimmed markdown of each extracted competitor (for reading, not for Outline input)."""
    for i, c in enumerate(data.get("competitors") or [], 1):
        print("=" * 70)
        print("### Competitor %d: %s\n%s\n" % (i, c.get("domain", ""), c["url"]))
        print(c.get("content") or "(%s)" % c.get("error", "no content"))
        print()


def print_text(keyword, data, from_cache):
    print("### SERP Results: %s  (Google VN, vi)%s" % (keyword, "  [cache]" if from_cache else ""))
    print("Organic hợp lệ: %d\n" % len(data["organic"]))
    for i, r in enumerate(data["organic"], 1):
        print("%2d. %s" % (i, r["title"] or "(no title)"))
        print("    %s" % r["url"])
        if r["description"]:
            print("    %s" % r["description"][:200])
        print()
    fs = data.get("featured_snippet")
    if fs:
        print("### Featured Snippet")
        print("- %s — %s" % (fs.get("domain"), fs.get("url")))
        print("- %s\n" % fs.get("text"))
    if data.get("people_also_ask"):
        print("### People Also Ask")
        print("\n".join("- " + q for q in data["people_also_ask"]) + "\n")
    if data.get("related_searches"):
        print("### Related Searches")
        print("\n".join("- " + k for k in data["related_searches"]) + "\n")
    comps = data.get("competitors") or []
    if comps:
        print("---\n")
        for i, c in enumerate(comps, 1):
            print(format_competitor(i, c) + "\n")
        print("## Competitor Gap Synthesis: %s\n" % keyword)
        print("### Gaps — tất cả/hầu hết competitors đều bỏ qua:\n1. \n2. \n")
        print("### Unique angles DSC có thể khai thác:\n- \n")
        print("### Content format gaps:\n- \n")
        print("### Recommended Featured Snippet target:\n- Dạng: [Paragraph | List | Table | None]\n- Lý do: \n")
    print("Cost: $%.4f%s" % (data.get("cost") or 0, " (cached, no API call)" if from_cache else ""))


def main():
    ap = argparse.ArgumentParser(description="DataForSEO SERP + competitor extraction (local parser, Jina fallback), cached")
    ap.add_argument("keyword")
    ap.add_argument("--top", type=int, default=10, help="organic results to show (max 10)")
    ap.add_argument("--extract", type=int, default=0, metavar="N", help="extract content of top N URLs (local parser first, Jina fallback)")
    ap.add_argument("--content", action="store_true", help="print full trimmed markdown of extracted competitors")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("--raw", action="store_true", help="dump the raw DataForSEO payload (forces API call)")
    ap.add_argument("--no-cache", action="store_true", help="ignore cache and call the API again (costs money)")
    ap.add_argument("--timeout", type=int, default=90)
    args = ap.parse_args()
    top = min(args.top, DEPTH)

    cfg = load_config()
    data = None if (args.no_cache or args.raw) else load_cache(args.keyword)
    from_cache = data is not None

    if data is None:
        missing = [k for k in ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD") if not cfg.get(k)]
        if missing:
            sys.exit("Missing config: %s (set as env var or in %s)" % (", ".join(missing), CONFIG))
        payload = fetch_serp(cfg, args.keyword, args.timeout)
        if args.raw:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return
        data = parse_serp(payload, DEPTH)
        data["keyword"] = args.keyword
        data["fetched_at"] = time.strftime("%Y-%m-%d %H:%M")
        data["competitors"] = []
        save_cache(args.keyword, data)

    # Extract only URLs not already in cache; Jina is free but slow.
    if args.extract:
        wanted = [r["url"] for r in data["organic"][:args.extract]]
        # Re-extract entries from older cache files that lack stored content.
        have = {c["url"] for c in data.get("competitors", []) if not c.get("error") and c.get("sections")}
        todo = [u for u in wanted if u not in have]
        if todo:
            fresh = extract_competitors(cfg, todo)
            keep = [c for c in data.get("competitors", []) if c["url"] not in todo]
            data["competitors"] = keep + fresh
            save_cache(args.keyword, data)
        order = {u: i for i, u in enumerate(wanted)}
        data["competitors"] = sorted(
            [c for c in data["competitors"] if c["url"] in order], key=lambda c: order[c["url"]]
        )
    else:
        data["competitors"] = []

    view = dict(data, organic=data["organic"][:top])
    if args.content:
        print_content(view)
    elif args.json:
        view["competitors"] = [{k: v for k, v in c.items() if k != "content"} for c in view["competitors"]]
        print(json.dumps(view, ensure_ascii=False, indent=2))
    else:
        print_text(args.keyword, view, from_cache)


if __name__ == "__main__":
    main()
