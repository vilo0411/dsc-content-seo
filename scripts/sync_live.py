#!/usr/bin/env python3
"""Snapshot the live article body of every /kien-thuc page into the repo, plus a link graph.

Why: after editing in the CMS, the CSV exports are stale. This keeps a git-tracked copy of what
is actually published, so the next edit starts from the live text and `git diff` shows what
changed between two syncs.

    python scripts/sync_live.py                      # full crawl (sitemap-cache.json, ~5-8 min)
    python scripts/sync_live.py --only slug1,slug2   # re-sync just the pages you edited
    python scripts/sync_live.py --from-sf content.csv  # build the snapshot from a Screaming Frog
                                                       # custom-extraction export instead of fetching
    python scripts/sync_live.py --show <slug>        # in/out links of one page from links.csv
    python scripts/sync_live.py --relink             # rebuild links.csv from html/ (no network)
    python scripts/sync_live.py --compare <slug>     # Final-*.md vs live: CMS-only links, text drift

Output (knowledge/raw/live/):
    html/<slug>.html  article body only (same block the SF extractor takes, minus the
                      "Nội dung liên quan" tag box), one HTML block per line → readable diffs
    pages.csv         slug, title, words, out/in link counts, Xem thêm links, CTA links, hash
    links.csv         one row per in-body link: from, to, anchor, kind, section
    _meta.json        last run info

kind in links.csv: contextual | xem-them (inside a ">> Xem thêm:" line/list) | cta (/mo-tai-khoan)
| other-internal | external.

Stdlib only (urllib + html.parser) — no curl-cffi / playwright (company Kaspersky policy).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
SITEMAP_CACHE = ROOT / ".antigravity/skills/internal-linking/scripts/sitemap-cache.json"
CLUSTERS = ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json"
OUT = ROOT / "knowledge/raw/live"
HTML_DIR = OUT / "html"
PAGES_CSV = OUT / "pages.csv"
LINKS_CSV = OUT / "links.csv"
META = OUT / "_meta.json"

HOST = "https://www.dsc.com.vn"
KB = HOST + "/kien-thuc/"
CONTENT_CLASS = "COSVFIRFRK"  # hashed by the site build — structural fallback below if it changes
USER_AGENT = "Mozilla/5.0 (compatible; DSC-content-snapshot/1.0)"

PAGE_FIELDS = ["slug", "title", "words", "out_kt", "out_kt_unique", "out_contextual", "out_xem_them",
               "out_cta", "out_external", "in_kt", "in_contextual", "sha", "last_changed"]
LINK_FIELDS = ["from", "to", "anchor", "kind", "section"]

BLOCK_TAGS = r"p|h[1-6]|ul|ol|li|table|thead|tbody|tr|figure|blockquote|div|img|hr"
XEM_THEM = re.compile(r"xem\s+th[eê]m\s*:?", re.I)


# ──────────────────────────── fetch + extract ────────────────────────────

def fetch(url: str, retries: int = 2) -> str:
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001 — network errors of every kind are retried the same way
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{type(last).__name__}: {last}")


def _div_block(html: str, start: int) -> tuple[int, int] | None:
    """Return (start, end) of the <div> opening at `start`, matching nested divs."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", html[start:]):
        depth += 1 if m.group() == "<div" else -1
        if depth == 0:
            return start, start + m.end()
    return None


def extract(html: str) -> tuple[str, str] | None:
    """(h1 text, article body HTML) from a full page or a Screaming Frog extractor cell."""
    h1 = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", html)
    title = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>|<!--.*?-->", "", h1.group(1)))).strip() if h1 else ""

    i = html.find(f'class="{CONTENT_CLASS}"')
    if i >= 0:
        span = _div_block(html, html.rfind("<div", 0, i))
    elif h1:
        # Fallback: the body is the first <div> sibling after the div wrapping the <h1>.
        wrap = _div_block(html, html.rfind("<div", 0, h1.start()))
        nxt = html.find("<div", wrap[1]) if wrap else -1
        span = _div_block(html, nxt) if nxt >= 0 else None
    else:
        span = None
    if not span:
        return None
    body = html[span[0]:span[1]]
    body = re.sub(r"^<div[^>]*>|</div>$", "", body)  # drop the hashed wrapper itself
    return title, body


def normalize(body: str) -> str:
    """One block per line, React comment markers removed — stable across syncs, git-diffable."""
    body = body.replace("<!-- -->", "")
    body = re.sub(r"\s*\n\s*", " ", body)
    body = re.sub(rf"(?i)\s*(<(?:{BLOCK_TAGS})\b)", r"\n\1", body)
    return "\n".join(line.rstrip() for line in body.strip().splitlines() if line.strip()) + "\n"


# ──────────────────────────── links ────────────────────────────

class LinkParser(HTMLParser):
    """Collect in-body links with anchor text, current H2/H3 and whether they sit in a Xem thêm list.

    Classification is per block (<p>/<li>): a link is "Xem thêm" when its block contains the words
    "Xem thêm", or when its block is link-only (< 3 words of own text) and directly follows such a
    block — that covers both ">> Xem thêm: <a>" lines and the "Xem thêm:" + <ul> of titles layout.
    """

    BLOCKS = ("p", "li")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[dict] = []
        self.words = 0
        self.section = ""
        self._head: list[str] | None = None
        self._a: dict | None = None
        self._stack: list[dict] = []
        self._run = False  # inside a run of Xem thêm blocks

    def _new_block(self) -> dict:
        return {"links": [], "plain": 0, "xem": False}

    def _close_block(self, blk: dict) -> None:
        if blk["xem"]:
            self._run = True
        is_xem = blk["xem"] or (self._run and blk["plain"] < 3)
        if not blk["xem"] and blk["plain"] >= 3:
            self._run = False
        for ln in blk["links"]:
            ln["xem"] = is_xem
            self.links.append(ln)

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3", "h4"):
            self._head, self._run = [], False
        elif tag in self.BLOCKS:
            self._stack.append(self._new_block())
        elif tag == "a":
            href = dict(attrs).get("href") or ""
            self._a = {"href": href.strip(), "text": []}

    def handle_endtag(self, tag):
        if tag in ("h2", "h3", "h4") and self._head is not None:
            self.section = re.sub(r"\s+", " ", "".join(self._head)).strip()
            self._head = None
        elif tag in self.BLOCKS and self._stack:
            self._close_block(self._stack.pop())
        elif tag == "a" and self._a is not None:
            ln = {"href": self._a["href"], "anchor": re.sub(r"\s+", " ", "".join(self._a["text"])).strip(),
                  "section": self.section}
            if self._stack:
                self._stack[-1]["links"].append(ln)
            else:
                ln["xem"] = self._run
                self.links.append(ln)
            self._a = None

    def handle_data(self, data):
        self.words += len(data.split())
        if self._head is not None:
            self._head.append(data)
        if self._a is not None:
            self._a["text"].append(data)
            return
        blk = self._stack[-1] if self._stack else None
        m = XEM_THEM.search(data)
        # Only a block that *opens* with "Xem thêm" (after ">>" etc.) is a Xem thêm line; "Bạn có thể
        # xem thêm hướng dẫn …" mid-sentence is prose and its link stays contextual.
        if m and not re.search(r"\w", data[:m.start()]) and (blk is None or (blk["plain"] == 0 and not blk["links"])):
            if blk is not None:
                blk["xem"] = True
            else:
                self._run = True
        elif blk is not None:
            blk["plain"] += len(re.findall(r"\w+", data))

    def close(self):
        super().close()
        while self._stack:
            self._close_block(self._stack.pop())


def canon(href: str) -> str | None:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    if href.startswith("//"):
        href = "https:" + href
    elif href.startswith("/"):
        href = HOST + href
    href = href.split("#")[0].split("?")[0]
    href = re.sub(r"^https?://(www\.)?dsc\.com\.vn", HOST, href)
    return href.rstrip("/") if href != HOST + "/" else href


def classify(url: str, xem: bool) -> str:
    if not url.startswith(HOST):
        return "external"
    if url == HOST + "/mo-tai-khoan" or url.startswith(HOST + "/mo-tai-khoan/"):
        return "cta"
    if url.startswith(KB):
        return "xem-them" if xem else "contextual"
    return "other-internal"


def parse_links(slug: str, body: str) -> tuple[list[dict], int]:
    p = LinkParser()
    p.feed(body)
    rows = []
    for ln in p.links:
        url = canon(ln["href"])
        if not url:
            continue
        rows.append({"from": slug, "to": url, "anchor": ln["anchor"], "kind": classify(url, ln["xem"]),
                     "section": ln["section"]})
    return rows, p.words


# ──────────────────────────── storage ────────────────────────────

def slug_of(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def sitemap_urls() -> list[str]:
    data = json.loads(SITEMAP_CACHE.read_text(encoding="utf-8"))
    urls = {u.rstrip("/") for u in (data["urls"] if isinstance(data, dict) else data) if "/kien-thuc/" in u}
    # Cluster members are tracked even when the CMS left them out of the sitemap
    # (e.g. huong-dan-mo-tai-khoan-chung-chi-quy) — otherwise the audit can't see them.
    if CLUSTERS.exists():
        for c in json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"]:
            for g in c["groups"]:
                urls.update(KB + s for s in ([g["hub"]] if g.get("hub") else []) + g["spokes"])
            if c.get("pillar"):
                urls.add(KB + c["pillar"])
    return sorted(urls)


def build_pages(pages: dict[str, dict], links: list[dict]) -> None:
    """Recompute every page's link counts from the full link table (inlinks need all pages)."""
    out: dict[str, dict] = {s: {"kt": [], "ctx": 0, "xem": 0, "cta": 0, "ext": 0} for s in pages}
    inl: dict[str, set] = {s: set() for s in pages}
    inl_ctx: dict[str, set] = {s: set() for s in pages}
    for r in links:
        o = out.get(r["from"])
        if o is None:
            continue
        k = r["kind"]
        if k in ("contextual", "xem-them"):
            o["kt"].append(r["to"])
            o["ctx" if k == "contextual" else "xem"] += 1
            tgt = slug_of(r["to"])
            if tgt in inl and tgt != r["from"]:
                inl[tgt].add(r["from"])
                if k == "contextual":
                    inl_ctx[tgt].add(r["from"])
        elif k == "cta":
            o["cta"] += 1
        elif k == "external":
            o["ext"] += 1
    for s, p in pages.items():
        o = out[s]
        p.update(out_kt=len(o["kt"]), out_kt_unique=len(set(o["kt"])), out_contextual=o["ctx"],
                 out_xem_them=o["xem"], out_cta=o["cta"], out_external=o["ext"],
                 in_kt=len(inl[s]), in_contextual=len(inl_ctx[s]))


def sync(sources: dict[str, str | None], full: bool, workers: int) -> int:
    """sources: url -> pre-fetched html (from --from-sf) or None (fetch it)."""
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    pages = {r["slug"]: r for r in read_csv(PAGES_CSV)}
    links = read_csv(LINKS_CSV)
    today = date.today().isoformat()

    def work(url: str):
        html = sources[url] if sources[url] is not None else fetch(url)
        got = extract(html)
        if not got:
            raise RuntimeError("không tìm thấy khối nội dung (đổi layout?)")
        return url, got

    done: dict[str, tuple[str, str]] = {}
    failed: list[tuple[str, str]] = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(work, u): u for u in sources}
        for n, fut in enumerate(as_completed(futs), 1):
            u = futs[fut]
            try:
                _, got = fut.result()
                done[u] = got
            except Exception as e:  # noqa: BLE001
                failed.append((u, str(e)))
            if n % 50 == 0 or n == len(futs):
                print(f"  {n}/{len(futs)}  ({time.time() - t0:.0f}s)", file=sys.stderr)

    changed, new = [], []
    fresh_links: list[dict] = []
    for url, (title, body) in sorted(done.items()):
        slug = slug_of(url)
        text = normalize(body)
        sha = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
        prev = pages.get(slug)
        if prev is None:
            new.append(slug)
        elif prev.get("sha") != sha:
            changed.append(slug)
        if prev is None or prev.get("sha") != sha or not (HTML_DIR / f"{slug}.html").exists():
            (HTML_DIR / f"{slug}.html").write_text(text, encoding="utf-8", newline="\n")
        rows, words = parse_links(slug, text)
        fresh_links.extend(rows)
        last = today if (prev is None or prev.get("sha") != sha) else prev.get("last_changed", today)
        pages[slug] = {"slug": slug, "title": title, "words": words, "sha": sha, "last_changed": last}

    synced = {slug_of(u) for u in done}
    links = [r for r in links if r["from"] not in synced] + fresh_links

    removed = []
    if full:
        live = {slug_of(u) for u in sources}
        failed_slugs = {slug_of(u) for u, _ in failed}
        for slug in sorted(set(pages) - live - failed_slugs):
            removed.append(slug)
            pages.pop(slug)
            (HTML_DIR / f"{slug}.html").unlink(missing_ok=True)
        links = [r for r in links if r["from"] in pages]

    build_pages(pages, links)
    write_csv(PAGES_CSV, PAGE_FIELDS, sorted(pages.values(), key=lambda r: r["slug"]))
    write_csv(LINKS_CSV, LINK_FIELDS, sorted(links, key=lambda r: (r["from"], r["kind"], r["to"])))
    META.write_text(json.dumps({"last_run": datetime.now().isoformat(timespec="seconds"),
                                "mode": "full" if full else "partial", "pages": len(pages),
                                "links": len(links), "changed": changed, "new": new, "removed": removed,
                                "failed": [u for u, _ in failed]}, ensure_ascii=False, indent=1),
                    encoding="utf-8")

    print(f"\n✓ {len(done)} trang · đổi nội dung: {len(changed)} · mới: {len(new)} · gỡ: {len(removed)} · lỗi: {len(failed)}")
    for label, items in (("Đổi", changed), ("Mới", new), ("Gỡ", removed)):
        if items and len(items) <= 40:
            print(f"  {label}: " + ", ".join(items))
    for u, err in failed:
        print(f"  ✗ {u} — {err}")
    if changed:
        print("\nXem khác biệt:  git diff --word-diff knowledge/raw/live/html/<slug>.html")
    return 1 if failed and not done else 0


# ──────────────────────────── CLI ────────────────────────────

def load_sf(path: Path) -> dict[str, str]:
    csv.field_size_limit(10 ** 9)
    out = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        col = next((c for c in reader.fieldnames or [] if c.lower().startswith("extractor")), None)
        if not col:
            sys.exit(f"{path}: không thấy cột 'Extractor …' (custom extraction HTML)")
        for r in reader:
            if "/kien-thuc/" in r.get("Address", "") and r.get(col):
                out[r["Address"].rstrip("/")] = r[col]
    return out


FINALIZED = ROOT / "knowledge/4-content/3-finalized"


def compare(slug: str) -> int:
    """Final-*.md vs live snapshot: links added/removed in the CMS + how much the text drifted.

    Run before /optimize: anything edited directly in the CMS (e.g. the internal-link pass) exists
    only on live, and optimizing from a stale Final file would silently drop it.
    """
    import difflib
    final = next((p for p in FINALIZED.glob("Final-*.md")
                  if p.stem == f"Final-{slug}" or re.search(rf"^Slug:\s*{re.escape(slug)}\s*$",
                                                            p.read_text(encoding="utf-8", errors="ignore"), re.M)), None)
    snap = HTML_DIR / f"{slug}.html"
    if not snap.exists():
        sys.exit(f"Chưa có snapshot — chạy: python scripts/sync_live.py --only {slug}")
    if final is None:
        print(f"Không có Final-*.md cho '{slug}' — bài chỉ có trên live, lấy {snap.relative_to(ROOT)} làm bản gốc.")
        return 0
    md = final.read_text(encoding="utf-8")
    md_links = {canon(u) for u in re.findall(r"\]\((https?://[^)\s]+)", md) + re.findall(r'href="([^"]+)"', md)}
    md_links = {u for u in md_links if u and u.startswith(HOST)}
    live_rows, _ = parse_links(slug, snap.read_text(encoding="utf-8"))
    live_links = {r["to"]: r for r in live_rows if r["to"].startswith(HOST)}

    def plain_md(t: str) -> str:
        t = re.sub(r"^---.*?---", "", t, flags=re.S)
        t = re.sub(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>", " ", t)
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        return re.sub(r"[#*_>|`-]+|\s+", " ", t).strip().lower()

    live_txt = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", snap.read_text(encoding="utf-8")))).strip().lower()
    ratio = difflib.SequenceMatcher(None, plain_md(md).split(), live_txt.split(), autojunk=False).ratio()
    added = sorted(set(live_links) - md_links)
    removed = sorted(md_links - set(live_links))
    print(f"# {final.name}  ↔  live ({slug})\n")
    print(f"Độ giống văn bản: {ratio:.0%}" + ("  ⚠ live đã sửa nhiều so với Final" if ratio < 0.9 else ""))
    print(f"\n## Link chỉ có trên live ({len(added)}) — đã thêm trên CMS, PHẢI giữ khi optimize")
    for u in added:
        r = live_links[u]
        print(f"  + [{r['kind']}] “{r['anchor']}” → {u}   §{r['section'][:50]}")
    print(f"\n## Link chỉ có trong Final ({len(removed)}) — đã gỡ trên CMS, đừng thêm lại nếu không có lý do")
    for u in removed:
        print(f"  - {u}")
    if added or ratio < 0.9:
        print(f"\n→ Bản gốc để optimize = live: {snap.relative_to(ROOT)} (Final đã cũ).")
    return 0


def relink() -> int:
    """Re-parse links from stored snapshots (no network) — after a parser change or a manual edit."""
    pages = {r["slug"]: r for r in read_csv(PAGES_CSV)}
    links: list[dict] = []
    for slug, p in pages.items():
        f = HTML_DIR / f"{slug}.html"
        if f.exists():
            rows, p["words"] = parse_links(slug, f.read_text(encoding="utf-8"))
            links.extend(rows)
    build_pages(pages, links)
    write_csv(PAGES_CSV, PAGE_FIELDS, sorted(pages.values(), key=lambda r: r["slug"]))
    write_csv(LINKS_CSV, LINK_FIELDS, sorted(links, key=lambda r: (r["from"], r["kind"], r["to"])))
    print(f"✓ relink {len(pages)} trang · {len(links)} link")
    return 0


def show(slug: str) -> int:
    links = read_csv(LINKS_CSV)
    pages = {r["slug"]: r for r in read_csv(PAGES_CSV)}
    if slug not in pages:
        sys.exit(f"Chưa có snapshot cho '{slug}' — chạy: python scripts/sync_live.py --only {slug}")
    p = pages[slug]
    print(f"# {p['title']}\n  {KB}{slug}  · {p['words']} từ · đổi lần cuối {p['last_changed']}\n")
    print("## Link ra")
    for r in (r for r in links if r["from"] == slug):
        print(f"  [{r['kind']:<10}] {r['anchor'][:60]:<60} → {r['to'].replace(KB, '')}   §{r['section'][:40]}")
    print("\n## Link vào")
    for r in (r for r in links if r["to"] == KB + slug and r["from"] != slug):
        print(f"  [{r['kind']:<10}] {r['from']:<70} “{r['anchor'][:50]}”")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="slug hoặc URL, phân cách bằng dấu phẩy")
    ap.add_argument("--from-sf", type=Path, help="CSV custom extraction của Screaming Frog (thay cho fetch)")
    ap.add_argument("--show", metavar="SLUG", help="in link vào/ra của 1 bài từ snapshot")
    ap.add_argument("--compare", metavar="SLUG", help="so Final-*.md với bản live (chạy trước /optimize)")
    ap.add_argument("--relink", action="store_true", help="dựng lại links.csv/pages.csv từ html/ (không fetch)")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    if a.show:
        return show(a.show)
    if a.relink:
        return relink()
    if a.compare:
        return compare(a.compare)
    if a.from_sf:
        sf = load_sf(a.from_sf)
        sources: dict[str, str | None] = dict(sf)
        full = not a.only
    else:
        sources = {u: None for u in sitemap_urls()}
        full = not a.only
    if a.only:
        want = {slug_of(x.strip()) for x in a.only.split(",") if x.strip()}
        sources = {u: h for u, h in sources.items() if slug_of(u) in want}
        for s in want - {slug_of(u) for u in sources}:
            sources[KB + s] = None  # not in sitemap cache / SF export yet — fetch it anyway
    if not sources:
        sys.exit("Không có URL nào để sync.")
    print(f"Sync {len(sources)} trang ({'SF export' if a.from_sf else 'live'}, {'full' if full else 'partial'})…",
          file=sys.stderr)
    return sync(sources, full, a.workers)


if __name__ == "__main__":
    sys.exit(main())
