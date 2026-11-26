"""Competitor content watch: who ranks for our keywords, what they published this week, how often.

    python scripts/competitor_watch.py discover [--keyword "cách chơi chứng khoán"] [--top 15] [--add N]
        Domains in the Google top 10 of our cached SERPs (knowledge/raw/serp/*.json, 0 API cost), scored by
        rank, with the folder their ranking URLs live in (= content hub). --add N writes the top N to the config.
    python scripts/competitor_watch.py run [--only domain] [--max-new 40]
        For each competitor: collect hub URLs (robots.txt -> sitemaps; fallback: crawl hub listing pages),
        diff against the snapshot, fetch NEW URLs once (title, published date, words, H2s), classify into
        our clusters. First run of a domain = baseline (old URLs marked, not counted as "new").
    python scripts/competitor_watch.py gap <domain> [--top 30]
        Cached SERPs where <domain> is in the top 10 and DSC is absent or ranks lower: keyword, their rank + URL,
        DSC rank + URL (input for /competitor-profile and /keyword-plan; 0 API cost).
    python scripts/competitor_watch.py report [--week 2026-W47]
        knowledge/2-market/competitors/watch/<week>.md: new posts per competitor, 12-week cadence, cluster
        mix, and which of their new topics DSC has no article for (input for /keyword-plan).

Config: knowledge/2-market/competitors/competitors.json · snapshots: knowledge/raw/competitors/<domain>/urls.csv
Sitemap lastmod is NOT trusted (VPBankS stamps every URL with the deploy date); "new" = URL not seen
before, dated by the page's own published date when it exposes one. Stdlib only (no browser automation).
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import REGISTRY, ROOT, setup_utf8, unaccent  # noqa: E402
from activity_log import emit  # noqa: E402

CONFIG = ROOT / "knowledge/2-market/competitors/competitors.json"
WATCH_DIR = ROOT / "knowledge/2-market/competitors/watch"
VELOCITY = ROOT / "knowledge/2-market/competitors/velocity.csv"
SNAP_DIR = ROOT / "knowledge/raw/competitors"
SERP_DIR = ROOT / "knowledge/raw/serp"
OWN = ("dsc.com.vn",)
SKIP_DOMAINS = ("google.", "facebook.", "youtube.", "tiktok.", "wikipedia.", "linkedin.", "x.com", "twitter.",
                "instagram.", "pinterest.", "reddit.", "quora.")
UA = {"User-Agent": "Mozilla/5.0 (compatible; dsc-competitor-watch/1.0)"}
SNAP_FIELDS = ["url", "first_seen", "baseline", "lastmod", "published", "title", "words", "h2", "subgroup", "fetched"]
CATEGORY_SLUGS = {"kien-thuc-chung", "webinar", "tin-chung-khoan", "tat-ca", "video", "podcast", "tin-tuc", "kien-thuc",
                  "blog", "hoc", "category", "page", "tag", "tin-moi", "thong-bao"}
PR_RX = re.compile(r"^(thong bao|hoi thao|cong bo|khuyen mai|tuyen dung|thu moi|lich nghi|tb |vfs thong bao|ra mat|chuc mung)")
STOP = set("la gi va cua cho cac nhung co khong duoc trong khi voi de mot nay nao nhu the cach nen hay ve tu "
           "den theo tai se da dang hon nhat huong dan chi tiet nguoi moi bai viet top 2024 2025 2026 cap nhat "
           "dieu can biet ma hieu qua tot nhanh".split())


# ---------------------------------------------------------------- http helpers

CURL = shutil.which("curl", path=r"C:\Windows\System32") or shutil.which("curl")


def fetch(url: str, timeout: int = 20) -> str:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            raw = r.read()
    except Exception as exc:  # noqa: BLE001 - one bad URL must not stop the run
        raw = b""
        # Some hosts fail Python's TLS (incomplete chain, handshake). System curl uses the OS certificate
        # store (Schannel on Windows); certificate verification stays ON.
        if CURL and "ssl" in str(exc).lower():
            try:
                raw = subprocess.run([CURL, "-s", "-L", "--compressed", "-m", str(timeout), "-A", UA["User-Agent"], url],
                                     capture_output=True, timeout=timeout + 5).stdout
            except (OSError, subprocess.SubprocessError):
                raw = b""
        if not raw:
            return f"ERR {type(exc).__name__}: {str(exc)[:80]}"
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def sitemap_urls(domain: str, limit_maps: int = 80) -> list[tuple[str, str]]:
    """(loc, lastmod) from robots.txt sitemaps, following sitemap indexes."""
    robots = fetch(f"https://{domain}/robots.txt")
    queue = [] if robots.startswith("ERR") else re.findall(r"(?im)^sitemap:\s*(\S+)", robots)
    queue = queue or [f"https://{domain}/sitemap.xml", f"https://{domain}/sitemap_index.xml"]
    seen, out = set(), []
    while queue and len(seen) < limit_maps:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        xml = fetch(sm)
        if xml.startswith("ERR"):
            continue
        if "<sitemapindex" in xml:
            queue += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
            continue
        for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
            loc = re.search(r"<loc>\s*([^<\s]+)", block)
            lm = re.search(r"<lastmod>\s*([^<\s]+)", block)
            if loc:
                out.append((unescape(loc.group(1)), lm.group(1)[:10] if lm else ""))
        time.sleep(0.3)
    return out


def listing_urls(comp: dict, pages: int = 5) -> list[tuple[str, str]]:
    """Fallback when there is no usable sitemap: crawl the hub listing pages for article links."""
    base = comp.get("listing") or f"https://{comp['domain']}{comp.get('hub') or '/'}"
    found: dict[str, str] = {}
    for n in range(1, pages + 1):
        url = base if n == 1 else (f"{base.rstrip('/')}/page/{n}" if "{n}" not in base else base.format(n=n))
        if n > 1 and "?" not in base and "{n}" not in base:
            alt = f"{base}{'&' if '?' in base else '?'}page={n}"
            html = fetch(url)
            html = html if not html.startswith("ERR") else fetch(alt)
        else:
            html = fetch(url)
        if html.startswith("ERR"):
            break
        before = len(found)
        for href in re.findall(r'href="([^"#]+)"', html):
            full = urllib.parse.urljoin(base, unescape(href)).split("?")[0]
            if in_hub(full, comp) and full.rstrip("/") != base.rstrip("/"):
                found.setdefault(full.rstrip("/"), "")
        if len(found) == before:
            break
        time.sleep(0.5)
    return list(found.items())


def in_hub(url: str, comp: dict) -> bool:
    p = urllib.parse.urlparse(url)
    if comp["domain"] not in p.netloc:
        return False
    hub = comp.get("hub") or "/"
    path = p.path.rstrip("/")
    if path.rsplit("/", 1)[-1] in CATEGORY_SLUGS or any(re.search(x, path) for x in comp.get("exclude", [])):
        return False
    if hub != "/":
        return path.startswith(hub.rstrip("/") + "/")
    # hub "/" = articles live at the site root: keep long slugs only (skip /lien-he, /gioi-thieu…)
    return path.count("/") == 1 and path.count("-") >= 3


def page_meta(html: str) -> dict:
    """Title, published date, word count, H2 count from an article page (best effort, no JS)."""
    def first(*pats):
        for pat in pats:
            m = re.search(pat, html, re.I | re.S)
            if m:
                return unescape(m.group(1)).strip()
        return ""
    title = first(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', r"<title[^>]*>(.*?)</title>", r"<h1[^>]*>(.*?)</h1>")
    pub = first(r'"datePublished"\s*:\s*"([^"]+)"', r'property="article:published_time"[^>]+content="([^"]+)"',
                r'content="([^"]+)"[^>]+property="article:published_time"', r'itemprop="datePublished"[^>]+content="([^"]+)"',
                r'\\?"published_at\\?"\s*:\s*\\?"([0-9]{4}-[0-9]{2}-[0-9]{2})', r"<time[^>]+datetime=\"([^\"]+)\"")
    if not pub:  # fallback: first dd/mm/yyyy on the page (Vietcap prints the post date before related-post dates)
        m = re.search(r"\b([0-3]?[0-9])/([01]?[0-9])/(20[0-9]{2})\b", html)
        if m and 1 <= int(m.group(2)) <= 12 and 1 <= int(m.group(1)) <= 31:
            guess = f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
            pub = guess if guess <= date.today().isoformat() else ""
    body = re.sub(r"<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = unescape(re.sub(r"<[^>]+>", " ", body))
    return {"title": re.sub(r"<[^>]+>", "", title)[:200], "published": pub[:10],
            # JS-rendered pages (body in a script payload) give near-zero counts: record blank, not a fake number
            "words": (lambda n: str(n) if n >= 150 else "")(len(re.findall(r"\w+", text))),
            "h2": (lambda n: str(n) if n else "")(len(re.findall(r"<h2[\s>]", html, re.I)))}


# ---------------------------------------------------------------- config / snapshot

def load_config() -> list[dict]:
    return json.loads(CONFIG.read_text(encoding="utf-8")).get("competitors", []) if CONFIG.exists() else []


def save_config(comps: list[dict]) -> None:
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    doc = {"_doc": "Competitors watched by scripts/competitor_watch.py. hub = folder of their articles "
                   "('/' = site root); listing = page to crawl when the sitemap misses articles; "
                   "source = serp (from discover) | manual.", "competitors": comps}
    CONFIG.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def snap_path(domain: str) -> Path:
    return SNAP_DIR / domain.replace("www.", "") / "urls.csv"


def load_snap(domain: str) -> dict[str, dict]:
    p = snap_path(domain)
    if not p.exists():
        return {}
    with p.open(encoding="utf-8-sig", newline="") as f:
        return {r["url"]: r for r in csv.DictReader(f)}


def save_snap(domain: str, rows: dict[str, dict]) -> None:
    p = snap_path(domain)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SNAP_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: (r.get("published") or r["first_seen"]), reverse=True))


def classifier():
    import page_groups as pg
    overrides = {r["slug"].strip(): r["subgroup"].strip() for r in pg.read_csv(pg.OVERRIDES)} if pg.OVERRIDES.exists() else {}
    sector = {r["ticker"].upper(): r["subgroup"] for r in pg.read_csv(pg.TICKER_SECTOR)}
    links = pg.link_groups()
    return lambda slug, title: pg.classify(slug, title, overrides, links, sector)[0], pg.SUBGROUPS


# ---------------------------------------------------------------- commands

def cmd_discover(a) -> int:
    score, kws, ranks, dirs, example = Counter(), defaultdict(set), defaultdict(list), defaultdict(Counter), {}
    files = sorted(SERP_DIR.glob("*.json"))
    used = 0
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        kw = d.get("keyword") or f.stem
        if a.keyword and unaccent(a.keyword) not in unaccent(kw):
            continue
        used += 1
        for o in d.get("organic", [])[:10]:
            dom = (o.get("domain") or urllib.parse.urlparse(o.get("url", "")).netloc).lower()
            if not dom or any(x in dom for x in OWN + SKIP_DOMAINS):
                continue
            r = int(o.get("rank") or 10)
            score[dom] += max(0, 11 - r)
            kws[dom].add(kw)
            ranks[dom].append(r)
            path = urllib.parse.urlparse(o["url"]).path.rstrip("/")
            dirs[dom][path.rsplit("/", 1)[0] + "/" if path.count("/") > 1 else "/"] += 1
            example.setdefault(dom, o["url"])
    if not used:
        print("Không có SERP cache khớp. Chạy serp_research.py cho keyword trước (có phí) hoặc bỏ --keyword.")
        return 1
    top = score.most_common(a.top)
    print(f"# Domain rank tốt trên {used} SERP đã cache{' (lọc: ' + a.keyword + ')' if a.keyword else ''}\n")
    print("| # | Domain | Số keyword top 10 | Hạng TB | Điểm | Hub (thư mục bài) | Ví dụ |\n|---|---|---|---|---|---|---|")
    watched = {c["domain"] for c in load_config()}
    for i, (dom, sc) in enumerate(top, 1):
        hub = dirs[dom].most_common(1)[0][0]
        mark = " ✓" if dom in watched else ""
        print(f"| {i} | {dom}{mark} | {len(kws[dom])} | {sum(ranks[dom]) / len(ranks[dom]):.1f} | {sc} | `{hub}` | {example[dom]} |")
    if a.add:
        comps = load_config()
        for dom, _ in top[: a.add]:
            if dom not in watched:
                comps.append({"name": dom.replace("www.", "").split(".")[0], "domain": dom,
                              "hub": dirs[dom].most_common(1)[0][0], "listing": "", "source": "serp",
                              "added": date.today().isoformat()})
        save_config(comps)
        print(f"\nĐã ghi {CONFIG.relative_to(ROOT)} ({len(comps)} đối thủ). Kiểm tra cột hub rồi chạy `run`.")
    return 0


def cmd_run(a) -> int:
    comps = [c for c in load_config() if (not a.only or a.only in c["domain"]) and not c.get("disabled")]
    if not comps:
        print(f"Chưa có đối thủ trong {CONFIG.relative_to(ROOT)} — chạy `discover --add N` hoặc thêm tay.")
        return 1
    classify, _ = classifier()
    today = date.today().isoformat()
    for comp in comps:
        dom = comp["domain"]
        snap = load_snap(dom)
        baseline = not snap
        urls = [(u, lm) for u, lm in sitemap_urls(dom) if in_hub(u, comp)]
        source = "sitemap"
        if len(urls) < 5:
            urls, source = listing_urls(comp), "listing"
        new = [u for u, _ in urls if u.rstrip("/") not in snap and u not in snap]
        for u, lm in urls:
            key = u.rstrip("/")
            if key not in snap and u not in snap:
                snap[key] = {"url": key, "first_seen": today, "baseline": "1" if baseline else "", "lastmod": lm}
            else:
                (snap.get(key) or snap[u])["lastmod"] = lm
        # fetch unread pages: new URLs first, then baseline URLs a batch per run until history is complete
        unread = [k for k, r in snap.items() if not r.get("fetched")]
        unread.sort(key=lambda k: snap[k].get("lastmod", ""), reverse=True)          # newest lastmod first
        unread.sort(key=lambda k: snap[k].get("baseline") == "1")                    # then: new URLs before baseline
        todo = unread[: a.max_new]
        for u in todo:
            html = fetch(u)
            row = snap[u]
            if not html.startswith("ERR"):
                row.update(page_meta(html))
            row["subgroup"] = classify(urllib.parse.urlparse(u).path.rstrip("/").rsplit("/", 1)[-1], row.get("title", ""))
            row["fetched"] = today
            time.sleep(0.5)
        save_snap(dom, snap)
        left = sum(1 for r in snap.values() if not r.get("fetched"))
        print(f"{dom}: {len(urls)} URL ({source}) · mới {0 if baseline else len(new)}"
              f"{' · BASELINE lần đầu' if baseline else ''} · đã đọc {len(todo)} trang · còn {left} chưa đọc")
    return 0


def iso_week(d: str) -> str:
    y, w, _ = date.fromisoformat(d[:10]).isocalendar()
    return f"{y}-W{w:02d}"


def event_date(r: dict) -> str:
    """Date a post 'appeared': its own published date, else first_seen unless it was in the baseline."""
    if re.match(r"\d{4}-\d{2}-\d{2}", r.get("published") or ""):
        return r["published"][:10]
    return "" if r.get("baseline") else r.get("first_seen", "")


def dsc_terms() -> list[tuple[str, set[str]]]:
    if not REGISTRY.exists():
        return []
    with REGISTRY.open(encoding="utf-8-sig", newline="") as f:
        return [(r["slug"], tokens(" ".join([r["key_chinh"], r["anchor"], r["title"], r["slug"].replace("-", " ")])))
                for r in csv.DictReader(f) if r["status"] != "Merged"]


def tokens(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", unaccent(s)) if len(t) > 1 and t not in STOP}


def dsc_match(title: str, slug: str, own: list) -> str:
    q = tokens(title + " " + slug.replace("-", " "))
    best, who = 0.0, ""
    for s, t in own:
        if q and t:
            sc = len(q & t) / len(q | t)
            if sc > best:
                best, who = sc, s
    return who if best >= 0.4 else ""


def cmd_report(a) -> int:
    comps = load_config()
    if not comps:
        print("Chưa có đối thủ — chạy `discover --add N`.")
        return 1
    week = a.week or iso_week(date.today().isoformat())
    y, w = map(int, week.split("-W"))
    monday = date.fromisocalendar(y, w, 1)
    weeks = [iso_week((monday - timedelta(weeks=i)).isoformat()) for i in range(11, -1, -1)]
    _, names = classifier()
    own = dsc_terms()
    out = [f"# Đối thủ tuần {week} ({monday} → {monday + timedelta(days=6)})", "",
           f"Sinh bởi `python scripts/competitor_watch.py report` lúc {datetime.now():%Y-%m-%d %H:%M}. "
           "\"Mới\" = URL chưa thấy ở lần chạy trước, ngày theo published của chính trang (nếu có).", ""]
    summary, gaps, vel_rows = [], [], []
    for comp in comps:
        snap = load_snap(comp["domain"])
        if comp.get("disabled") or not snap:
            why = comp.get("note") or "chưa chạy `run`"
            summary.append(f"| {comp['name']} | — | — | — | {why} |")
            continue
        dated = [(event_date(r), r) for r in snap.values()]
        per_week = Counter(iso_week(d) for d, _ in dated if d)
        dated = [(d, r) for d, r in dated if in_hub(r["url"], comp)]   # config/category filters apply to old rows too
        this = [r for d, r in dated if d and iso_week(d) == week]
        last4 = [r for d, r in dated if d and iso_week(d) in weeks[-4:]]
        avg4 = sum(per_week[x] for x in weeks[-4:]) / 4
        mix = Counter(r.get("subgroup") or "?" for r in last4).most_common(3)
        baseline_only = all(r.get("baseline") for r in snap.values())
        summary.append(f"| {comp['name']} | {len(this)} | {avg4:.1f} | {len(snap)} | "
                       f"{', '.join(f'{k} {names.get(k, k)[:22]} ({v})' for k, v in mix) or '—'}"
                       f"{' · chỉ có baseline' if baseline_only else ''} |")
        vel_rows.append({"week": week, "domain": comp["domain"], "new": len(this), "avg4": f"{avg4:.1f}", "total": len(snap)})
        out += [f"## {comp['name']} — `{comp['domain']}{comp.get('hub') or ''}`", "",
                "Nhịp đăng 12 tuần: " + " ".join(f"{x[-3:]}:{per_week[x]}" for x in weeks), ""]
        if this:
            out += ["| Ngày | Bài | Nhóm | Số từ | DSC đã có |", "|---|---|---|---|---|"]
            for r in sorted(this, key=event_date, reverse=True):
                slug = r["url"].rsplit("/", 1)[-1]
                pr = bool(PR_RX.match(unaccent(r.get("title", ""))))
                has = "PR / thông báo" if pr else dsc_match(r.get("title", ""), slug, own)
                if not has:
                    gaps.append((comp["name"], r))
                out.append(f"| {event_date(r)} | [{(r.get('title') or slug)[:80]}]({r['url']}) | {r.get('subgroup') or '?'} | "
                           f"{r.get('words') or '?'} | {(has if has.startswith("PR") else '`' + has + '`') if has else '**chưa có**'} |")
        else:
            out.append("_Không có bài mới trong tuần._")
        out.append("")
    out[4:4] = ["## Tóm tắt", "", "| Đối thủ | Bài mới tuần này | TB 4 tuần | Tổng URL theo dõi | Nhóm chủ đề 4 tuần gần nhất |",
                "|---|---|---|---|---|", *summary, ""]
    if gaps:
        out += ["## Chủ đề đối thủ vừa đăng mà DSC chưa có bài → xem xét ở `/keyword-plan`", ""]
        out += [f"- {r.get('title') or r['url']} — {name} · nhóm {r.get('subgroup') or '?'} · {r['url']}" for name, r in gaps]
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    path = WATCH_DIR / f"{week}.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    old = []
    if VELOCITY.exists():
        with VELOCITY.open(encoding="utf-8", newline="") as f:
            old = [r for r in csv.DictReader(f) if r["week"] != week]
    with VELOCITY.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["week", "domain", "new", "avg4", "total"])
        wr.writeheader()
        wr.writerows(old + vel_rows)
    print("\n".join(out[:8 + len(summary)]))
    print(f"\n→ {path.relative_to(ROOT)} · {len(gaps)} chủ đề DSC chưa có")
    emit("market", "report", week, skill="competitor-watch", path=path,
         result=f"{sum(int(r['new']) for r in vel_rows)} bài mới đối thủ · {len(gaps)} chủ đề DSC chưa có")
    return 0


def cmd_gap(a) -> int:
    rows = []
    for f in sorted(SERP_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        org = d.get("organic", [])[:10]
        theirs = next((o for o in org if a.domain in (o.get("domain") or o.get("url", ""))), None)
        ours = next((o for o in org if any(x in (o.get("domain") or o.get("url", "")) for x in OWN)), None)
        if theirs and (not ours or int(ours["rank"]) > int(theirs["rank"])):
            rows.append((int(theirs["rank"]), d.get("keyword") or f.stem, theirs["url"],
                         int(ours["rank"]) if ours else None, ours["url"] if ours else "", d.get("fetched_at", "")[:10]))
    rows.sort(key=lambda r: (r[3] is not None, r[0]))
    print(f"# {a.domain} hơn DSC trên {len(rows)} SERP đã cache (DSC vắng mặt trước)\n")
    print("| Keyword | Hạng họ | URL họ | Hạng DSC | URL DSC | SERP ngày |\n|---|---|---|---|---|---|")
    for r, kw, u, dr, du, at in rows[: a.top]:
        print(f"| {kw} | {r} | {u} | {dr or '—'} | {du or '—'} | {at} |")
    return 0


def main() -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover")
    d.add_argument("--keyword", help="only SERPs whose keyword contains this (accent-insensitive)")
    d.add_argument("--top", type=int, default=15)
    d.add_argument("--add", type=int, default=0, help="write the top N domains to competitors.json")
    d.set_defaults(fn=cmd_discover)
    r = sub.add_parser("run")
    r.add_argument("--only", help="domain substring")
    r.add_argument("--max-new", type=int, default=40, help="max pages fetched per competitor per run")
    r.set_defaults(fn=cmd_run)
    g = sub.add_parser("gap")
    g.add_argument("domain")
    g.add_argument("--top", type=int, default=30)
    g.set_defaults(fn=cmd_gap)
    p = sub.add_parser("report")
    p.add_argument("--week", help="ISO week, e.g. 2026-W47 (default: current)")
    p.set_defaults(fn=cmd_report)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
