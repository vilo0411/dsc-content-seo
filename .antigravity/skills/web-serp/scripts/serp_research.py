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
OWN_DOMAIN = "dsc.com.vn"  # flag PAA answers Google already takes from our site
PAA_MAX_DEPTH = 4      # DataForSEO people_also_ask_click_depth upper bound

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
CONFIG = os.path.join(ROOT, ".antigravity", "config", "api-keys.md")
CACHE_DIR = os.path.join(ROOT, "knowledge", "raw", "serp")
# Keyword plans: an API call is only made for keywords listed here unless --force is passed.
PLAN_FILES = (
    os.path.join(ROOT, "knowledge", "4-content", "topic-clusters.md"),
    os.path.join(ROOT, "knowledge", "4-content", "sprint-backlog.md"),
)

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


def keyword_planned(keyword):
    """True if the keyword (accent-insensitive) appears in any plan file. Missing files -> True (no gate)."""
    files = [f for f in PLAN_FILES if os.path.exists(f)]
    if not files:
        return True
    needle = slugify(keyword)
    for f in files:
        with open(f, encoding="utf-8-sig") as fh:
            for line in fh:
                if not line.startswith("|"):
                    continue
                for cell in line.split("|"):
                    if slugify(cell.replace("**", "").replace("[HUB]", "")) == needle:
                        return True
    return False


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
        data = json.load(fh)
    # Caches written before the Google /goto fix (2026-11-09) have no `serp_features` and lost
    # their organic list (every result looked like google.com). Treat them as expired → refetch.
    if "serp_features" not in data and not data.get("serp_source") and len(data.get("organic") or []) < 5:
        print("Cache %s hỏng (lỗi link google /goto 11/2026, %d organic) → gọi lại API."
              % (os.path.basename(path), len(data.get("organic") or [])), file=sys.stderr)
        return None
    return data


def save_cache(keyword, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path(keyword), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- DataForSEO

def fetch_serp(cfg, keyword, timeout, paa_depth=0):
    """One live/advanced call. Exits on any error — no retry, no extra cost.

    paa_depth > 0 sets people_also_ask_click_depth (1-4): Google expands the PAA tree on click,
    each level adds more questions. Costs extra — only for pillar articles.
    """
    task = {
        "keyword": keyword,
        "location_code": LOCATION_CODE,
        "language_code": LANGUAGE_CODE,
        "device": "desktop",
        "depth": DEPTH,
    }
    if paa_depth:
        task["people_also_ask_click_depth"] = min(paa_depth, PAA_MAX_DEPTH)
    body = json.dumps([task]).encode()
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


# ---------------------------------------------------------------- Google /goto unwrapping
# Since ~2026-11 DataForSEO returns organic URLs as opaque Google redirects
# (https://google.com/goto?url=CAES...) with domain "google.com". The real host only survives in
# `breadcrumb` ("https://acbs.com.vn › Kiến thức"). We follow the redirect (no API cost); Google
# throttles after a few hops with a <meta refresh="N;url=..."> page — we honour the wait once,
# then fall back to the breadcrumb host (URL unknown -> competitor extraction skipped).
GOTO_BUDGET_S = 90      # total seconds allowed for unwrapping one SERP
GOTO_MAX_WAIT = 20      # longest meta-refresh wait we accept
SOCIAL_HINTS = ("facebook", "tiktok", "youtube", "instagram", "threads", "zalo", "reddit")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_GOTO_OPENER = urllib.request.build_opener(_NoRedirect)


def _is_google_wrapper(url):
    p = urllib.parse.urlparse(url or "")
    return "google." in p.netloc and p.path.startswith(("/goto", "/url"))


def _breadcrumb_host(item):
    m = re.match(r"\s*(https?://[^\s›]+)", item.get("breadcrumb") or "")
    return urllib.parse.urlparse(m.group(1)).netloc.lower() if m else ""


def resolve_google_url(url, deadline):
    """Follow Google /goto redirects to the publisher URL. Returns the URL or None."""
    for _ in range(5):
        if time.time() > deadline:
            return None
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with _GOTO_OPENER.open(req, timeout=15) as r:
                body = r.read(6000).decode("utf-8", "replace")
            m = re.search(r'content="(\d+);\s*url=([^"]+)"', body)
            if not m:
                m2 = re.search(r'href="(https?://(?![^"]*google\.)[^"]+)"', body)
                return m2.group(1) if m2 else None
            wait = int(m.group(1))
            if wait > GOTO_MAX_WAIT or time.time() + wait > deadline:
                return None
            time.sleep(wait)  # throttle interstitial: wait as asked, then follow
            url = urllib.parse.urljoin(url, m.group(2).replace("&amp;", "&"))
        except urllib.error.HTTPError as e:
            loc = e.headers.get("Location")
            if not loc:
                return None
            loc = urllib.parse.urljoin(url, loc)
            if "google." not in urllib.parse.urlparse(loc).netloc:
                return loc
            url = loc
        except Exception:
            return None
    return None


def unwrap_organic(item, deadline):
    """Return (url, host, resolved_flag) for an organic item, unwrapping Google redirects."""
    link = item.get("url") or ""
    if not _is_google_wrapper(link):
        return link, urllib.parse.urlparse(link).netloc.lower(), True
    real = resolve_google_url(link, deadline)
    if real:
        return real, urllib.parse.urlparse(real).netloc.lower(), True
    host = _breadcrumb_host(item)
    if not host and any(h in (item.get("website_name") or "").lower() for h in SOCIAL_HINTS):
        host = "facebook.com" if "facebook" in (item.get("website_name") or "").lower() else "social"
    return ("https://%s/" % host if host else ""), host, False


def parse_serp(payload, top):
    task = payload["tasks"][0]
    result = (task.get("result") or [{}])[0]
    organic, paa, related, snippet, ai_overview = [], [], [], None, None
    features = []  # non-organic SERP blocks (ai_overview, video, local_pack...) -> intent signal
    deadline = time.time() + GOTO_BUDGET_S
    for item in result.get("items") or []:
        t = item.get("type")
        if t and t != "organic" and t not in features:
            features.append(t)
        if t == "organic":
            link, host, resolved = unwrap_organic(item, deadline)
            if not link.startswith("http") or host == "social" or any(b in host for b in BLOCKLIST):
                continue
            row = {
                "rank": item.get("rank_group") or len(organic) + 1,
                "title": (item.get("title") or "").strip(),
                "url": link,
                "domain": host,
                "description": (item.get("description") or "").strip(),
            }
            if not resolved:
                row["url_unresolved"] = True  # only the host is known (from breadcrumb)
            organic.append(row)
        elif t == "people_also_ask":
            for q in item.get("items") or []:
                if not q.get("title"):
                    continue
                # expanded_element = the answer Google currently shows under the question
                exp = (q.get("expanded_element") or [{}])[0]
                paa.append({
                    "question": q["title"].strip(),
                    "answer_snippet": (exp.get("description") or "").strip()[:400],
                    "source_title": (exp.get("title") or "").strip(),
                    "source_url": exp.get("url") or "",
                    "source_domain": (exp.get("domain") or "").lower(),
                })
        elif t == "related_searches":
            related += [k for k in item.get("items") or [] if isinstance(k, str)]
        elif t == "ai_overview" and ai_overview is None:
            ai_overview = _parse_ai_overview(item)
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
        "ai_overview": ai_overview,
        "serp_features": features,
        "se_results_count": result.get("se_results_count"),
        "cost": task.get("cost") or 0,
    }


def _parse_ai_overview(item):
    """Text + cited sources of the AI Overview block, when the API returns them.
    Reads whichever of markdown/text/description and references exist; nothing is assumed."""
    texts, refs = [], []

    def walk(node):
        if not isinstance(node, dict):
            return
        for key in ("markdown", "text", "description"):
            v = node.get(key)
            if isinstance(v, str) and v.strip():
                texts.append(v.strip())
                break
        for r in node.get("references") or []:
            if isinstance(r, dict) and (r.get("url") or r.get("domain")):
                refs.append({"domain": (r.get("domain") or "").lower(), "url": r.get("url") or "",
                             "title": (r.get("title") or "").strip()})
        for child in node.get("items") or []:
            walk(child)

    walk(item)
    seen, uniq = set(), []
    for r in refs:
        k = r["url"] or r["domain"]
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    return {"text": "\n".join(dict.fromkeys(texts))[:1500], "references": uniq[:10]}


def normalize_paa(paa):
    """Old cache files store PAA as plain strings; newer ones as dicts. Always return dicts."""
    out = []
    for q in paa or []:
        if isinstance(q, str):
            out.append({"question": q, "answer_snippet": "", "source_title": "",
                        "source_url": "", "source_domain": ""})
        elif isinstance(q, dict) and q.get("question"):
            out.append(q)
    return out


_VI_STOP = {"la", "gi", "co", "cua", "va", "cac", "nhung", "de", "khi", "nao", "the", "thi",
            "nen", "bao", "nhieu", "cach", "lam", "sao", "o", "dau", "toi", "ban", "can", "muon",
            "khong", "phai", "hay", "voi", "cho", "ve", "tu", "su", "giua", "biet", "khac"}


def _bigrams(text):
    """Accent-stripped word bigrams minus stopwords. Bigrams keep compound terms apart
    (chứng khoán ≠ chứng chỉ quỹ) where single tokens would collide on "chứng"."""
    ws = [w for w in slugify(text).split("-") if len(w) > 1 and w not in _VI_STOP]
    return {(ws[i], ws[i + 1]) for i in range(len(ws) - 1)} if len(ws) > 1 else set(ws)


def paa_coverage(paa, competitors):
    """For each PAA question, list competitor domains with a heading covering it
    (every question bigram appears in the heading). Heuristic — good enough to spot gaps."""
    rows = []
    for q in paa:
        qb = _bigrams(q["question"])
        hit = []
        for c in competitors or []:
            if c.get("error"):
                continue
            for _, title in c.get("headings") or []:
                if qb and qb <= _bigrams(title):
                    hit.append(c.get("domain") or urllib.parse.urlparse(c["url"]).netloc)
                    break
        rows.append((q, hit))
    return rows


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


def trim_main_content(md, cap=True):
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
    return " ".join(words[:MAX_WORDS]) if cap else text


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
        # word_count is measured on the capped text; keep the real length for the median
        data["word_count_full"] = len(_clean_text(trim_main_content(md, cap=False)).split())
        data["source"] = source
        return data
    with ThreadPoolExecutor(max_workers=5) as pool:
        return list(pool.map(work, urls))


# ---------------------------------------------------------------- topic coverage (cross-competitor)

MIN_COMPETITOR_WORDS = 300
JUNK_PAGE = re.compile(r"(?i)performing security verification|just a moment|access denied|"
                       r"verify you are human|attention required|enable javascript")
SOCIAL_SOURCES = ("facebook.", "youtube.", "tiktok.", "zalo.", "twitter.", "x.com", "instagram.",
                  "linkedin.", "t.me", "apple.com", "google.com", "play.google")
# Function words: a term may not start or end with one (keeps "chứng chỉ quỹ", drops "quỹ là").
TERM_STOP = set("""và là của có các những cho với trong khi để thì mà này đó được bị sẽ đã đang cũng như hay
hoặc nếu vì do nên tại từ về theo trên dưới ra vào lên xuống một hai ba không rất hơn nhất bạn người nào gì
sao thế vậy còn lại đến tới qua sau trước giữa ngoài cần phải muốn ở đây kia ấy nhiều ít mỗi mọi cả việc
giúp càng rằng nhưng tuy bởi nhằm chưa đều thường luôn chính thêm khác ai đâu bao lúc nhé nha à ơi ta họ
tôi chúng mình nó the of and to in for a is on""".split())
TERM_BOILERPLATE = ("bài viết", "xem thêm", "liên hệ", "đăng ký", "chia sẻ", "bình luận", "mục lục",
                    "trang chủ", "tin tức", "tải app", "tải ứng dụng", "hotline", "tham khảo", "tìm hiểu",
                    "lưu ý", "ví dụ", "hiện nay", "sau đây", "dưới đây", "tổng hợp", "thông tin")
# Everyday words that are frequent on a topic's SERP without being a concept of it. The background
# file cannot separate these from real finance terms ("cổ tức" is as common as "trường hợp"), so they are listed.
TERM_COMMON = set("""số lượng|chấp nhận|phân biệt|trường hợp|câu hỏi|yêu cầu|tối đa|tối thiểu|bổ sung|thuật ngữ|hoàn toàn
chuyên gia|nguyên nhân|năng lực|tập trung|chủ động|hiểu rõ|gia tăng|tương ứng|kết hợp|thiết lập|tự động|điều kiện
quan tâm|rõ ràng|nguy cơ|thời gian|mục tiêu|tham gia|cá nhân|hiệu quả|quyết định|lựa chọn|phù hợp|quan trọng|cơ bản
phổ biến|đặc điểm|ưu điểm|nhược điểm|lợi ích|hạn chế|kinh nghiệm|khái niệm|định nghĩa|ý nghĩa|vai trò|mức độ|khả năng
xác định|thực hiện|sử dụng|áp dụng|đảm bảo|cung cấp|hỗ trợ|bao gồm|liên quan|tương tự|đơn giản|chi tiết|cụ thể
hình thức|phương pháp|quy trình|điểm khác biệt|cao hơn|thấp hơn|so với|tổng giá trị|số vốn|huy động|điều hành
đầu tiên|cân nhắc|đáp ứng|nắm giữ|trạng thái|triệu đồng|tiền mặt|hình thức đầu tư|đầu tư hiệu quả|chuyên gia đầu tư""".replace("\n", "|").split("|"))
MUST_DF = 3    # a term used by >= 3 competitors is expected by the SERP
MUST_MAX = 15  # strongest terms only: the list gates the outline and the draft, noise there costs rewrites
_TERM_SPLIT = re.compile(r"[.!?:;,()\[\]|/\"“”–—\n]+")
_TERM_WORD = re.compile(r"[^\W\d_]+")


def usable_competitors(competitors):
    """Extracted pages worth comparing against: no errors, no bot-check pages, no stubs, not our own site."""
    out = []
    for c in competitors or []:
        if c.get("error") or OWN_DOMAIN in (c.get("domain") or ""):
            continue
        if (c.get("word_count") or 0) < MIN_COMPETITOR_WORDS:
            continue
        if any(JUNK_PAGE.search(h[1]) for h in c.get("headings") or []):
            continue
        out.append(c)
    return out


def _term_counts(text):
    """{n-gram: tf} for 2-4 word lowercase n-grams inside one sentence, function words trimmed."""
    counts = {}
    for sent in _TERM_SPLIT.split(_clean_text(text).lower()):
        ws = _TERM_WORD.findall(sent)
        for n in (2, 3, 4):
            for i in range(len(ws) - n + 1):
                g = ws[i:i + n]
                if g[0] in TERM_STOP or g[-1] in TERM_STOP or any(len(w) > 12 for w in g):
                    continue
                t = " ".join(g)
                counts[t] = counts.get(t, 0) + 1
    return counts


BACKGROUND_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "term-background.json")
LIVE_HTML_DIR = os.path.join(ROOT, "knowledge", "raw", "live", "html")
GENERIC_SHARE = {"serp": 0.30, "live": 0.25}  # share of pages a term must reach to count as generic vocabulary
_BG = None


def build_background():
    """Count in how many pages each term appears, over (a) every cached competitor page and
    (b) the live DSC corpus. Terms common to unrelated pages ("nhà đầu tư", "thị trường") say
    nothing about one topic. Saved once; rebuild with --rebuild-background after the corpus grows."""
    out = {"built": time.strftime("%Y-%m-%d"), "serp_pages": 0, "live_pages": 0, "serp": {}, "live": {}}
    try:
        names = [n for n in os.listdir(CACHE_DIR) if n.endswith(".json")]
    except OSError:
        names = []
    for name in names:
        try:
            with open(os.path.join(CACHE_DIR, name), encoding="utf-8-sig") as f:
                other = json.load(f)
        except (OSError, ValueError):
            continue
        for c in usable_competitors(other.get("competitors") if isinstance(other, dict) else None):
            out["serp_pages"] += 1
            for t in _term_counts(c.get("content") or ""):
                out["serp"][t] = out["serp"].get(t, 0) + 1
    try:
        pages = [n for n in os.listdir(LIVE_HTML_DIR) if n.endswith(".html")]
    except OSError:
        pages = []
    for name in pages:
        try:
            with open(os.path.join(LIVE_HTML_DIR, name), encoding="utf-8") as f:
                text = re.sub(r"<[^>]+>", " ", f.read())
        except OSError:
            continue
        out["live_pages"] += 1
        for t in _term_counts(text):
            out["live"][t] = out["live"].get(t, 0) + 1
    # keep only terms that could ever cross the threshold (file stays small)
    for kind, pages_n in (("serp", out["serp_pages"]), ("live", out["live_pages"])):
        floor = max(3, pages_n * GENERIC_SHARE[kind] * 0.6)
        out[kind] = {t: n for t, n in out[kind].items() if n >= floor}
    with open(BACKGROUND_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    return out


def _generic_terms(own_df):
    """Set of generic terms. own_df = {term: pages of THIS keyword using it}; those pages are
    subtracted from the SERP counts so a topic term is not penalised by its own cache."""
    global _BG
    if _BG is None:
        try:
            with open(BACKGROUND_FILE, encoding="utf-8") as f:
                _BG = json.load(f)
        except (OSError, ValueError):
            _BG = build_background()
    own_pages = max(own_df.values()) if own_df else 0
    generic = set()
    if _BG["live_pages"] >= 50:
        generic |= {t for t, n in _BG["live"].items() if n >= _BG["live_pages"] * GENERIC_SHARE["live"]}
    rest = _BG["serp_pages"] - own_pages
    if rest >= 15:
        generic |= {t for t, n in _BG["serp"].items() if n - own_df.get(t, 0) >= rest * GENERIC_SHARE["serp"]}
    return generic


def _neighbours(text, wanted):
    """{term: ({prev_word: n}, {next_word: n})} — used to spot fragments of longer phrases."""
    out = {t: ({}, {}) for t in wanted}
    for sent in _TERM_SPLIT.split(_clean_text(text).lower()):
        ws = _TERM_WORD.findall(sent)
        for n in (2, 3, 4):
            for i in range(len(ws) - n + 1):
                t = " ".join(ws[i:i + n])
                if t in out:
                    prev = ws[i - 1] if i else ""
                    nxt = ws[i + n] if i + n < len(ws) else ""
                    out[t][0][prev] = out[t][0].get(prev, 0) + 1
                    out[t][1][nxt] = out[t][1].get(nxt, 0) + 1
    return out


def content_headings(c):
    """H2/H3 of the article itself: drops nav/widget headings (links, repeats, footer blocks)."""
    out, seen = [], set()
    for s in c.get("sections") or []:
        title = s["title"]
        if s["level"] not in ("H2", "H3") or "](" in title or title in seen:
            continue
        if any(h in title.lower() for h in FOOTER_HINTS) or JUNK_PAGE.search(title):
            continue
        seen.add(title)
        out.append(s)
    # a real H3 sits under an H2 of the article; pages whose headings are all widgets have no H2
    return out if any(s["level"] == "H2" for s in out) else []


def topic_coverage(data, limit=25):
    """What the ranking pages have in common: the input for entity coverage.
       terms    n-grams used by >= 2 competitors (df = number of competitors, tf = total uses)
       must     subset with df >= MUST_DF: the outline/draft is expected to cover these
       topics   sub-topics (H2/H3) that >= 2 competitors cover
       sources  external domains competitors cite
    Computed from the cache on every call, so old cache files work without migration."""
    # Every cached page that still ranks, not just the ones printed: the digest and the linters
    # (which read the raw cache) must compute the same list.
    ranking = {r["url"] for r in data.get("organic") or []}
    pool = data.get("competitors_all") or data.get("competitors")
    comps = [c for c in usable_competitors(pool) if not ranking or c["url"] in ranking]
    kw_words = set(_TERM_WORD.findall((data.get("keyword") or "").lower()))

    df, tf = {}, {}
    for c in comps:
        for t, n in _term_counts(c.get("content") or "").items():
            df[t] = df.get(t, 0) + 1
            tf[t] = tf.get(t, 0) + n
    generic = _generic_terms(df)
    cands = []
    for t, d in df.items():
        ws = t.split()
        if d < 2 or tf[t] < 3 or t in generic or t in TERM_COMMON or any(b in t for b in TERM_BOILERPLATE):
            continue
        if sum(w in kw_words for w in ws) * 2 > len(ws):  # mostly the keyword itself
            continue
        cands.append((t, d, tf[t]))
    # Fragment filter: "ty quản lý quỹ" is always preceded by "công", "vốn tự" always followed by "có".
    left, right = {}, {}
    wanted = {t for t, _, _ in cands}
    for c in comps:
        for t, (lp, rn) in _neighbours(c.get("content") or "", wanted).items():
            for w, n in lp.items():
                left.setdefault(t, {})[w] = left.get(t, {}).get(w, 0) + n
            for w, n in rn.items():
                right.setdefault(t, {})[w] = right.get(t, {}).get(w, 0) + n

    def fragment(t, total):
        for side in (left.get(t, {}), right.get(t, {})):
            w, n = max(side.items(), key=lambda kv: kv[1], default=("", 0))
            if w and n >= total * 0.5:
                return True
        return False

    cands = [x for x in cands if not fragment(x[0], x[2])]
    cands.sort(key=lambda x: (-x[1], -len(x[0].split()), -x[2], x[0]))
    picked = []
    for t, d, n in cands:
        # a fragment of a longer phrase with the same reach adds nothing
        pad = " " + t + " "
        if any(d == pd and (pad in " " + pt + " " or " " + pt + " " in pad) for pt, pd, _ in picked):
            continue
        picked.append((t, d, n))
    picked.sort(key=lambda x: (-x[1], -x[2], x[0]))
    terms = [{"term": t, "df": d, "tf": n} for t, d, n in picked[:limit]]

    clusters = []  # [{"bigrams", "titles", "domains"}]
    for c in comps:
        for sec in content_headings(c):
            title = sec["title"]
            bg = {b for b in _bigrams(title) if isinstance(b, tuple)}
            if not bg:
                continue
            for cl in clusters:
                if len(bg & cl["bigrams"]) / min(len(bg), len(cl["bigrams"])) >= 0.6:
                    cl["titles"].append(title)
                    cl["domains"].add(c.get("domain"))
                    break
            else:
                clusters.append({"bigrams": bg, "titles": [title], "domains": {c.get("domain")}})
    topics = [{"topic": min(cl["titles"], key=len), "n": len(cl["domains"]), "domains": sorted(cl["domains"])}
              for cl in clusters if len(cl["domains"]) >= 2]
    topics.sort(key=lambda x: -x["n"])

    src = {}
    for c in comps:
        hosts = {urllib.parse.urlparse(l["url"]).netloc.replace("www.", "") for l in c.get("external_links") or []}
        for host in hosts:
            if host and not any(x in host for x in SOCIAL_SOURCES):
                src[host] = src.get(host, 0) + 1
    used = {c["url"] for c in comps}
    return {
        "competitors_used": len(comps),
        "competitors_dropped": [c.get("domain") or c.get("url") for c in pool or [] if c.get("url") not in used],
        "terms": terms,
        "must": [t["term"] for t in terms if t["df"] >= MUST_DF][:MUST_MAX],
        "topics": topics[:15],
        "sources": sorted(src.items(), key=lambda kv: (-kv[1], kv[0]))[:10],
    }


def print_topic_coverage(tc):
    if not tc["competitors_used"]:
        return
    print("### Topic Coverage — gộp từ %d đối thủ hợp lệ%s" % (
        tc["competitors_used"],
        " (loại: %s)" % ", ".join(tc["competitors_dropped"]) if tc["competitors_dropped"] else ""))
    if tc["must"]:
        print("- **Thuật ngữ BẮT BUỘC phủ** (≥ %d đối thủ dùng) → copy vào `Entities:` của outline; bỏ cụm nào"
              " phải ghi `Entities_Skipped:` kèm lý do:\n  %s" % (MUST_DF, " · ".join(tc["must"])))
    rest = [t for t in tc["terms"] if t["term"] not in tc["must"]]
    if rest:
        print("- Thuật ngữ nên có: " + " · ".join(t["term"] for t in rest))
    if tc["topics"]:
        print("- Chủ đề con nhiều đối thủ cùng có (số đối thủ):")
        for t in tc["topics"]:
            print("  - %s (%d)" % (t["topic"], t["n"]))
    if tc["sources"]:
        print("- Nguồn đối thủ trích (gợi ý nguồn gốc để link): " + ", ".join(
            "%s×%d" % (h, n) if n > 1 else h for h, n in tc["sources"]))
    print()


# ---------------------------------------------------------------- SERP format / intent

FORMAT_LABELS = {
    "toplist": "Toplist (Top N / N mục đánh số)",
    "comparison": "So sánh (A vs B / phân biệt)",
    "howto": "How-to (hướng dẫn, các bước)",
    "definition": "Định nghĩa (X là gì)",
    "review": "Review / có nên",
    "news": "Tin tức / bài báo",
    "guide": "Guide tổng hợp (không rõ khung)",
}
# Accent-stripped, space-separated patterns (matched against _fold(title)).
_NUM_UNITS = r"(?:phantram|nam|thang|ngay|tuan|gio|phut|ty|trieu|nghin|ngan|dong|usd|vnd|diem|lan|phien|buoc)\b"
FORMAT_RULES = (
    ("toplist", (r"\btop\s*\d+", r"(?:^|[\s:,(])\d{1,2}\s+(?!" + _NUM_UNITS + r")[a-z]{2,}",
                 r"\b(?:tot|uy tin|re|cao|pho bien|hieu qua|an toan|hang dau) nhat\b",
                 r"\bdanh sach\b", r"\bbang xep hang\b")),
    ("comparison", (r"\bso sanh\b", r"\bvs\b", r"\bkhac nhau\b", r"\bphan biet\b",
                    r"\b\w+ hay (?!nhat\b|khong\b)\w+")),
    ("howto", (r"\bcach\b", r"\bhuong dan\b", r"\bcac buoc\b", r"\b\d+ buoc\b", r"\blam sao\b",
               r"\blam the nao\b", r"\bquy trinh\b", r"\bthu tuc\b")),
    ("definition", (r"\bla gi\b", r"\bkhai niem\b", r"\bdinh nghia\b", r"\bnghia la\b")),
    ("review", (r"\bdanh gia\b", r"\breview\b", r"\bco nen\b", r"\bco tot khong\b",
                r"\bco an toan khong\b", r"\bco lua dao\b")),
)
# "Những / các X" with no number = soft list signal (list article without a count).
SOFT_LIST = re.compile(r"^(?:nhung|cac)\s+\w+")
NEWS_DOMAINS = (
    "vnexpress", "cafef", "vietstock", "tuoitre", "dantri", "vneconomy", "nhadautu", "vnbusiness",
    "thanhnien", "baodautu", "tinnhanhchungkhoan", "znews", "vtv", "laodong", "vietnamnet",
    "nld.com", "kinhtechungkhoan", "thoibaonganhang", "bnews", "vov.vn", "baomoi", "plo.vn",
)
NUMBERED_HEADING = re.compile(r"^(?:top\s*)?\d{1,2}\s+\S")  # matched on _fold(): "1. X" -> "1 x"
INTENT_RULES = (
    ("Transactional", (r"\bmo tai khoan\b", r"\bdang ky\b", r"\btai app\b", r"\bmua\b", r"\bgia\b", r"\bphi\b")),
    ("Commercial", (r"\btot nhat\b", r"\bnao tot\b", r"\btop\b", r"\breview\b", r"\bdanh gia\b",
                    r"\bso sanh\b", r"\bco nen\b", r"\buy tin\b", r"\bapp\b", r"\bsan nao\b")),
    ("Informational", (r"\bla gi\b", r"\bcach\b", r"\btai sao\b", r"\bvi sao\b", r"\brui ro\b",
                       r"\by nghia\b", r"\bcong thuc\b", r"\bhuong dan\b")),
)


def _fold(text):
    return slugify(text or "").replace("-", " ")


def classify_format(title, domain="", headings=None):
    """Return (format, [signals], list_count|None) for one SERP result.

    The pattern that appears EARLIEST in the title wins ("X là gì? Cách dùng" = definition,
    "7 cách ..." = toplist). Numbered headings only decide when the title has no signal,
    because how-to articles number their steps too."""
    t = _fold((title or "").replace("%", " phantram "))
    found = []  # (position, order, fmt, matched text)
    for order, (fmt, pats) in enumerate(FORMAT_RULES):
        best = None
        for p in pats:
            m = re.search(p, t)
            if m and (best is None or m.start() < best.start()):
                best = m
        if best:
            found.append((best.start(), order, fmt, best.group(0).strip()))
    found.sort()
    signals = ["title~'%s'" % f[3] for f in found]
    count = None
    m = re.search(r"top\s*(\d{1,2})", t) or re.search(
        r"(?:^|[\s:,(])(\d{1,2})\s+(?!" + _NUM_UNITS + r")[a-z]{2,}", t)
    if m and int(m.group(1)) >= 3:
        count = int(m.group(1))
    elif found and found[0][2] == "toplist" and m:
        found = [f for f in found if f[2] != "toplist"]  # "1 hợp đồng", "2 loại" is not a list article
    numbered = sum(1 for lvl, h in headings or [] if lvl in ("H2", "H3") and NUMBERED_HEADING.match(_fold(h)))
    if numbered >= 3:
        signals.append("%d heading đánh số" % numbered)
    if found:
        fmt = found[0][2]
        return fmt, signals, count if fmt == "toplist" else None
    if numbered >= 3:
        return "toplist", signals, numbered
    if SOFT_LIST.match(t):
        return "toplist", ["title 'những/các …' (list không đánh số)"], None
    if any(n in (domain or "") for n in NEWS_DOMAINS):
        return "news", ["domain báo"], None
    return "guide", signals, None


def guess_intent(keyword, features):
    k = _fold(keyword)
    for intent, pats in INTENT_RULES:
        if any(re.search(p, k) for p in pats):
            return intent
    if any(f in (features or []) for f in ("shopping", "local_pack", "paid")):
        return "Transactional"
    return "Informational"


def serp_format_summary(data, top=10):
    """Classify each organic result; weight top 3 ×2. Dominant format = what the outline must follow."""
    comps = {c["url"]: c for c in data.get("competitors") or [] if not c.get("error")}
    usable = {c["url"] for c in usable_competitors(data.get("competitors"))}
    rows, weights = [], {}
    for r in data.get("organic", [])[:top]:
        c = comps.get(r["url"])
        fmt, signals, count = classify_format(r.get("title", ""), r.get("domain", ""),
                                              c.get("headings") if c else None)
        w = 2 if (r.get("rank") or 99) <= 3 else 1
        weights[fmt] = weights.get(fmt, 0) + w
        rows.append({"rank": r.get("rank"), "domain": r.get("domain", "").replace("www.", ""),
                     "title": r.get("title", ""), "format": fmt, "signals": signals, "count": count,
                     "words": (c.get("word_count_full") or c.get("word_count"))
                     if c and c["url"] in usable else None})
    total = sum(weights.values()) or 1
    ranked = sorted(weights.items(), key=lambda kv: -kv[1])
    # news/guide are "no clear frame" — never the format to copy; dominant = best structural frame.
    structural = [(f, w) for f, w in ranked if f not in ("news", "guide")]
    dominant, share = (structural[0][0], structural[0][1] / total) if structural else ("guide", 0)
    tie = [f for f, w in structural if structural and w == structural[0][1]]
    if len(tie) > 1:  # equal weight: prefer the frame of the best-ranked result, but call it mixed
        best = next((r for r in data.get("organic", [])[:top]
                     if classify_format(r.get("title", ""), r.get("domain", ""),
                                        (comps.get(r["url"]) or {}).get("headings"))[0] in tie), None)
        if best:
            dominant = classify_format(best.get("title", ""), best.get("domain", ""),
                                       (comps.get(best["url"]) or {}).get("headings"))[0]
    counts = sorted(r["count"] for r in rows if r["format"] == "toplist" and r["count"])
    words = sorted(r["words"] for r in rows[:5] if r["words"])
    organic_n = len(data.get("organic") or [])
    degraded = organic_n < 5 or (data.get("serp_source") not in (None, "dataforseo"))
    return {
        "rows": rows,
        "shares": [(f, round(w / total * 100)) for f, w in ranked],
        "dominant": dominant,
        "share": round(share * 100),
        "verdict": "HỖN HỢP" if len(tie) > 1 else (
            "BẮT BUỘC" if share >= 0.5 else ("NGHIÊNG VỀ" if share >= 0.35 else "HỖN HỢP")),
        "tie": tie if len(tie) > 1 else [],
        "list_count_median": counts[len(counts) // 2] if counts else None,
        "list_count_max": counts[-1] if counts else None,
        "words_median_top5": words[len(words) // 2] if words else None,
        "intent": guess_intent(data.get("keyword", ""), data.get("serp_features")),
        "serp_features": data.get("serp_features"),
        "degraded": degraded,
        "degraded_reason": ("organic %d < 5" % organic_n if organic_n < 5 else
                            "nguồn SERP = %s (không phải DataForSEO)" % data.get("serp_source")) if degraded else "",
    }


def print_format_summary(s):
    print("### SERP Format & Intent — Outline PHẢI theo khung bài đang thắng")
    if s["degraded"]:
        print("⚠️ SERP_STATUS: degraded (%s) → ghi `SERP_Status: degraded` vào outline, PAA tự suy ra ghi"
              " `source: inferred`, số từ tính theo intent (không theo đối thủ). Báo user trước khi chốt khung bài."
              % s["degraded_reason"])
    print("| # | Domain | Loại bài | Tín hiệu | Số mục | Số từ |\n|---|---|---|---|---|---|")
    for r in s["rows"]:
        print("| %s | %s | %s | %s | %s | %s |" % (
            r["rank"], r["domain"], r["format"], "; ".join(r["signals"]) or "-",
            r["count"] or "-", r["words"] or "-"))
    print("\n- Tỷ trọng (top 3 ×2): " + ", ".join("%s %d%%" % (f, p) for f, p in s["shares"]))
    print("- **Khung bài thống trị: %s — %s (%d%%)**" % (
        FORMAT_LABELS.get(s["dominant"], s["dominant"]), s["verdict"], s["share"]))
    if s.get("tie"):
        print("- Hoà giữa: %s → chọn theo kết quả rank cao nhất (%s), xác nhận bằng outline top 3"
              % (" / ".join(s["tie"]), s["dominant"]))
    if s["dominant"] == "toplist" and s["list_count_max"]:
        print("- Toplist: đối thủ dùng median %s mục, max %s → bài mình ≥ median, Title/H1 có con số N"
              % (s["list_count_median"], s["list_count_max"]))
    if s["words_median_top5"]:
        print("- Số từ median top 5 đã extract: %d" % s["words_median_top5"])
    unclear = sum(p for f, p in s["shares"] if f in ("news", "guide"))
    if unclear >= 40:
        print("- %d%% kết quả là bài báo / guide không rõ khung → đọc outline top 3 để xác nhận, đừng chỉ dựa vào nhãn" % unclear)
    print("- Intent gợi ý theo keyword/SERP features: %s%s" % (
        s["intent"], " | features: " + ", ".join(s["serp_features"]) if s["serp_features"] else ""))
    print("- Quy tắc: BẮT BUỘC → `Content_Type` = khung này. NGHIÊNG VỀ → theo khung này trừ khi có lý do."
          " HỖN HỢP → chọn khung của top 3, ghi lý do. Lệch khung → điền `Format_Deviation` + báo user.\n")


# ---------------------------------------------------------------- output

def format_competitor(i, c, full=False):
    domain = c.get("domain") or urllib.parse.urlparse(c["url"]).netloc
    lines = ["### Competitor %d: %s" % (i, domain), "- URL: %s" % c["url"]]
    if c.get("error"):
        lines.append("- Lỗi: %s" % c["error"])
        return "\n".join(lines)
    if not full:
        # Compact digest: heading tree + word counts. Terms / sources are merged once in Topic Coverage.
        capped = not c.get("word_count_full") and c["word_count"] >= MAX_WORDS - 50
        lines.append("- ~%d%s từ | %s" % (
            c.get("word_count_full") or c["word_count"], "+" if capped else "",
            ", ".join(c.get("special_elements") or []) or "không có bảng/FAQ"))
        heads = content_headings(c)
        for s in heads:
            lines.append("%s- %s: %s (%d)" % ("  " if s["level"] == "H2" else "    ",
                                             s["level"], s["title"], s["word_count"]))
        if not heads:
            lines.append("  - (không có heading nội dung — bài báo liền mạch)")
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


def print_text(keyword, data, from_cache, full=False):
    print("### SERP Results: %s  (Google VN, vi)%s" % (keyword, "  [cache]" if from_cache else ""))
    print("Organic hợp lệ: %d\n" % len(data["organic"]))
    for i, r in enumerate(data["organic"], 1):
        print("%2d. %s" % (i, r["title"] or "(no title)"))
        print("    %s%s" % (r["url"], "  [chỉ biết domain — Google không cho giải link, không extract]"
                               if r.get("url_unresolved") else ""))
        if r["description"]:
            print("    %s" % r["description"][:200])
        print()
    print_format_summary(serp_format_summary(data))
    ao = data.get("ai_overview")
    if ao and (ao.get("text") or ao.get("references")):
        print("### AI Overview — Google đang trả lời thế nào, trích ai")
        if ao.get("text"):
            print("- %s" % ao["text"][:600].replace("\n", " "))
        if ao.get("references"):
            print("- Nguồn được trích: " + ", ".join(r["domain"] or r["url"] for r in ao["references"]))
        print()
    fs = data.get("featured_snippet")
    if fs:
        print("### Featured Snippet")
        print("- %s — %s" % (fs.get("domain"), fs.get("url")))
        print("- %s\n" % fs.get("text"))
    comps = data.get("competitors") or []
    paa = normalize_paa(data.get("people_also_ask"))
    if paa:
        print("### People Also Ask (%d) — mỗi câu phải thành H2/H3 hoặc FAQ trong Outline" % len(paa))
        for q, hit in paa_coverage(paa, comps):
            print("- Q: %s" % q["question"])
            if q.get("answer_snippet"):
                own = "  ⚑ DSC đang giữ PAA này" if OWN_DOMAIN in q.get("source_domain", "") else ""
                print("  Google answer (%s):%s" % (q.get("source_domain") or "?", own))
                print("    %s" % q["answer_snippet"][:250])
            if comps:
                print("  Heading khớp ở: %s" % (", ".join(sorted(set(hit))) if hit else "không đối thủ nào → gap tiềm năng, xác nhận bằng outline bên dưới"))
        print()
    if data.get("related_searches"):
        print("### Related Searches — cùng intent → Secondary/LSI; khác intent → spin-off candidate")
        print("\n".join("- " + k for k in data["related_searches"]) + "\n")
    if comps:
        print_topic_coverage(topic_coverage(data))
        for i, c in enumerate(comps, 1):
            print(format_competitor(i, c, full) + "\n")
        if full:
            print("## Competitor Gap Synthesis: %s\n" % keyword)
            print("### Gaps — tất cả/hầu hết competitors đều bỏ qua:\n1. \n2. \n")
            print("### Unique angles DSC có thể khai thác:\n- \n")
            print("### Content format gaps:\n- \n")
            print("### Recommended Featured Snippet target:\n- Dạng: [Paragraph | List | Table | None]\n- Lý do: \n")
            print("### PAA plan:\n- Thân bài (H2/H3): \n- FAQ: \n- Spin-off từ Related Searches: \n")
        else:
            print("→ Điền mục 2 “Competitor Gap Synthesis” của brief-template từ dữ liệu trên. Cần câu chủ đề,"
                  " data point, link của từng đối thủ: thêm `--full`.\n")
    print("Cost: $%.4f%s" % (data.get("cost") or 0, " (cached, no API call)" if from_cache else ""))


def main():
    ap = argparse.ArgumentParser(description="DataForSEO SERP + competitor extraction (local parser, Jina fallback), cached")
    ap.add_argument("keyword", nargs="?", default="")
    ap.add_argument("--rebuild-background", action="store_true",
                    help="rebuild term-background.json (generic vocabulary) from SERP cache + live corpus, then exit")
    ap.add_argument("--top", type=int, default=10, help="organic results to show (max 10)")
    ap.add_argument("--extract", type=int, default=0, metavar="N", help="extract content of top N URLs (local parser first, Jina fallback)")
    ap.add_argument("--content", action="store_true", help="print full trimmed markdown of extracted competitors")
    ap.add_argument("--full", action="store_true",
                    help="per-competitor detail (topic sentences, entities, data points, links): ~3x longer digest")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("--raw", action="store_true", help="dump the raw DataForSEO payload (forces API call)")
    ap.add_argument("--no-cache", action="store_true", help="ignore cache and call the API again (costs money)")
    ap.add_argument("--force", action="store_true",
                    help="call the API even if the keyword is not listed in topic-clusters.md / sprint-backlog.md")
    ap.add_argument("--paa-depth", type=int, default=0, metavar="N",
                    help="expand People Also Ask tree N levels (1-4, extra cost; pillar articles only)")
    ap.add_argument("--timeout", type=int, default=90)
    args = ap.parse_args()
    if args.rebuild_background:
        bg = build_background()
        print("term-background.json: %d SERP pages, %d live pages, %d + %d terms kept" % (
            bg["serp_pages"], bg["live_pages"], len(bg["serp"]), len(bg["live"])))
        return
    args.keyword = args.keyword.strip()
    if not args.keyword:
        sys.exit("Empty keyword — refusing to call the API.")
    top = min(args.top, DEPTH)

    cfg = load_config()
    data = None if (args.no_cache or args.raw) else load_cache(args.keyword)
    from_cache = data is not None

    if data is None:
        if not args.force and not keyword_planned(args.keyword):
            sys.exit("Keyword \"%s\" không có trong topic-clusters.md / sprint-backlog.md — có thể gõ nhầm. "
                     "Kiểm tra lại, hoặc thêm --force để gọi API (có phí)." % args.keyword)
        missing = [k for k in ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD") if not cfg.get(k)]
        if missing:
            sys.exit("Missing config: %s (set as env var or in %s)" % (", ".join(missing), CONFIG))
        payload = fetch_serp(cfg, args.keyword, args.timeout, args.paa_depth)
        if args.raw:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return
        data = parse_serp(payload, DEPTH)
        data["keyword"] = args.keyword
        data["paa_depth"] = args.paa_depth
        data["fetched_at"] = time.strftime("%Y-%m-%d %H:%M")
        data["competitors"] = []
        save_cache(args.keyword, data)

    all_cached = list(data.get("competitors") or [])
    # Extract only URLs not already in cache; Jina is free but slow.
    if args.extract:
        wanted = [r["url"] for r in data["organic"][:args.extract] if not r.get("url_unresolved")]
        # Re-extract entries from older cache files that lack stored content.
        have = {c["url"] for c in data.get("competitors", []) if not c.get("error") and c.get("sections")}
        todo = [u for u in wanted if u not in have]
        if todo:
            fresh = extract_competitors(cfg, todo)
            keep = [c for c in data.get("competitors", []) if c["url"] not in todo]
            data["competitors"] = keep + fresh
            save_cache(args.keyword, data)
            all_cached = list(data["competitors"])
        order = {u: i for i, u in enumerate(wanted)}
        data["competitors"] = sorted(
            [c for c in data["competitors"] if c["url"] in order], key=lambda c: order[c["url"]]
        )
    else:
        data["competitors"] = []

    view = dict(data, organic=data["organic"][:top], competitors_all=all_cached,
                people_also_ask=normalize_paa(data.get("people_also_ask")))
    if args.content:
        print_content(view)
    elif args.json:
        view["topic_coverage"] = topic_coverage(view)
        view["competitors"] = [{k: v for k, v in c.items() if k != "content"} for c in view["competitors"]]
        view.pop("competitors_all")
        view["format_summary"] = serp_format_summary(view)
        print(json.dumps(view, ensure_ascii=False, indent=2))
    else:
        print_text(args.keyword, view, from_cache, args.full)


if __name__ == "__main__":
    main()
