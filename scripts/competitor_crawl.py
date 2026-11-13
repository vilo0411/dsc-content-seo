#!/usr/bin/env python3
"""Snapshot a competitor's knowledge hub (Next.js App Router + headless CMS) for content analysis.

Built for vpbanks.com.vn/trung-tam-kien-thuc: the article body is not in the HTML, it lives in the
React Server Components payload (`self.__next_f.push([1,"..."])`). The CMS record (title, category,
author, published_at/created_at/updated_at, meta title/description) is a JSON object in that payload
and `long_description` points at an RSC text row (`$22` -> `22:T<hexlen>,<html>`).

Reuses the link parser / CSV helpers of sync_live.py (monkeypatched HOST/KB, own output dir —
never touches knowledge/raw/live/). Stdlib only (Kaspersky: no curl-cffi / playwright).

Usage:
  python scripts/competitor_crawl.py                      # vpbanks defaults
  python scripts/competitor_crawl.py --limit 5            # smoke test
  python scripts/competitor_crawl.py --inlink-sample 80   # also sample other sections for links into the hub
  python scripts/competitor_crawl.py --graph-only         # rebuild link-graph.html from existing CSVs
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_live as sl  # noqa: E402

ROOT = sl.ROOT
DEFAULT_HOST = "https://www.vpbanks.com.vn"
DEFAULT_PREFIX = "/trung-tam-kien-thuc/"
CTA_PATTERNS = re.compile(r"mo-tai-khoan|open-account|/app|onelink|apps\.apple|play\.google|ekyc", re.I)

PAGE_FIELDS = ["slug", "title", "meta_title", "meta_desc", "category", "tags", "author",
               "published", "created", "updated", "words", "h2", "h3", "tables", "images", "lists",
               "faq", "out_kt", "out_kt_unique", "out_contextual", "out_xem_them", "out_cta",
               "out_external", "in_kt", "in_contextual"]


def rsc_payload(html: str) -> bytes:
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, re.S)
    return "".join(json.loads('"' + c + '"') for c in chunks).encode("utf-8")


def rsc_text_row(payload: bytes, ref: str) -> str:
    """Resolve an RSC reference like '$22' to the text row '22:T<hexlen>,<utf-8 bytes>'."""
    rid = ref.lstrip("$").encode()
    m = re.search(rb"(?:^|\n)" + re.escape(rid) + rb":T([0-9a-f]+),", payload)
    if not m:
        return ""
    n = int(m.group(1), 16)
    return payload[m.end():m.end() + n].decode("utf-8", "replace")


def find_record(payload: bytes, slug: str) -> dict | None:
    """The CMS record is the JSON object right after '"data":' whose slug matches."""
    text = payload.decode("utf-8", "replace")
    dec = json.JSONDecoder()
    for m in re.finditer(r'"data":\{"_id":"[0-9a-f]+","title"', text):
        try:
            obj, _ = dec.raw_decode(text, m.start() + len('"data":'))
        except ValueError:
            continue
        if obj.get("slug") == slug:
            return obj
    return None


def body_stats(body: str) -> dict:
    h2 = re.findall(r"(?is)<h2[^>]*>(.*?)</h2>", body)
    h2_txt = [re.sub(r"\s+", " ", sl.unescape(re.sub(r"<[^>]+>", "", h))).strip() for h in h2]
    return {
        "h2": len(h2), "h3": len(re.findall(r"(?i)<h3\b", body)),
        "tables": len(re.findall(r"(?i)<table\b", body)), "images": len(re.findall(r"(?i)<img\b", body)),
        "lists": len(re.findall(r"(?i)<(?:ul|ol)\b", body)),
        "faq": int(any(re.search(r"câu hỏi|thường gặp|faq|hỏi đáp", h, re.I) for h in h2_txt)),
        "h2_list": h2_txt,
    }


def setup(host: str, prefix: str) -> None:
    sl.HOST, sl.KB = host, host + prefix

    def classify(url: str, xem: bool) -> str:
        if not url.startswith(sl.HOST):
            return "cta" if CTA_PATTERNS.search(url) else "external"
        if CTA_PATTERNS.search(url):
            return "cta"
        if url.startswith(sl.KB):
            return "xem-them" if xem else "contextual"
        return "other-internal"

    sl.classify = classify  # parse_links resolves the global at call time


def sitemap(host: str) -> list[str]:
    xml = sl.fetch(host + "/sitemap.xml")
    return re.findall(r"<loc>\s*(.*?)\s*</loc>", xml)


def crawl_one(url: str, out: Path, delay: float) -> tuple[dict, list[dict], dict] | None:
    slug = sl.slug_of(url)
    time.sleep(delay * random.uniform(0.7, 1.3))
    try:
        html = sl.fetch(url)
    except RuntimeError as e:
        print(f"  ! {slug}: {e}", file=sys.stderr)
        return None
    payload = rsc_payload(html)
    rec = find_record(payload, slug)
    if not rec:
        print(f"  ! {slug}: CMS record not found", file=sys.stderr)
        return None
    body = rec.get("long_description") or ""
    if isinstance(body, str) and body.startswith("$"):
        body = rsc_text_row(payload, body)
    body = sl.normalize(body) if body else ""
    (out / "html" / f"{slug}.html").write_text(body, encoding="utf-8")

    links, words = sl.parse_links(slug, body)
    st = body_stats(body)
    seo = rec.get("session_seo") or {}
    author = (rec.get("created_by") or {}).get("full_name", "") if isinstance(rec.get("created_by"), dict) else ""
    page = {
        "slug": slug, "title": rec.get("title", ""), "meta_title": (seo.get("meta_title") or "").strip(),
        "meta_desc": (seo.get("meta_description") or "").strip(),
        "category": " | ".join(c.get("title", "") for c in rec.get("category") or [] if isinstance(c, dict)),
        "tags": " | ".join(t.get("title", "") for t in rec.get("session_tag_posts") or [] if isinstance(t, dict)),
        "author": author, "published": (rec.get("published_at") or "")[:10],
        "created": (rec.get("created_at") or "")[:10], "updated": (rec.get("updated_at") or "")[:10],
        "words": words, **{k: v for k, v in st.items() if k != "h2_list"},
    }
    return page, links, {"slug": slug, "title": page["title"], "h2": st["h2_list"]}


def sample_inlinks(host: str, prefix: str, urls: list[str], n: int, delay: float) -> list[dict]:
    """Links into the hub from other sections (whole RSC payload incl. nav/related — page-level signal)."""
    kb_re = re.compile(re.escape(host + prefix) + r"([a-z0-9-]+)|\"" + re.escape(prefix) + r"([a-z0-9-]+)")
    by_sec: dict[str, list[str]] = {}
    for u in urls:
        p = u[len(host):].strip("/").split("/")
        if p and p[0] and not u.startswith(host + prefix) and p[0] != "en" and len(p) > 1:
            by_sec.setdefault(p[0], []).append(u)
    rows = []
    for sec, lst in sorted(by_sec.items()):
        pick = random.Random(42).sample(lst, min(n, len(lst)))
        for u in pick:
            time.sleep(delay)
            try:
                text = rsc_payload(sl.fetch(u)).decode("utf-8", "replace")
            except RuntimeError:
                continue
            tg = Counter(a or b for a, b in kb_re.findall(text))
            rows.append({"section": sec, "url": u, "kb_links": sum(tg.values()), "targets": " ".join(sorted(tg))})
        print(f"  sampled {len(pick)} from /{sec}/")
    return rows


def write_graph(out: Path, host: str, prefix: str, label: str) -> Path:
    """Interactive link graph via link_audit.py's HTML (monkeypatched paths; DSC files untouched).

    Clusters = the competitor's own CMS categories; pillar = most-inlinked page of each category.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "link_audit", ROOT / ".antigravity/skills/internal-linking/scripts/link_audit.py")
    la = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(la)

    pages = sl.read_csv(out / "pages.csv")
    by_cat: dict[str, list[dict]] = {}
    for p in pages:
        by_cat.setdefault(p["category"].split(" | ")[0] or "Khác", []).append(p)
    clusters = []
    for cat, lst in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        lst.sort(key=lambda p: -int(p["in_kt"] or 0))
        clusters.append({"name": cat, "pillar": lst[0]["slug"],
                         "groups": [{"name": cat, "hub": None, "spokes": [p["slug"] for p in lst[1:]]}]})
    cl_path = out / "_clusters.json"
    cl_path.write_text(json.dumps({"clusters": clusters}, ensure_ascii=False, indent=1), encoding="utf-8")

    kb = host + prefix
    la.LIVE, la.CLUSTERS, la.GSC_PAGES, la.KB = out, cl_path, out / "_no_gsc.csv", kb
    la.OUT_HTML = out / "link-graph.html"
    la.HTML = (la.HTML.replace('"https://www.dsc.com.vn/kien-thuc/"', json.dumps(kb))
               .replace("DSC /kien-thuc", label).replace("site live (/kien-thuc)", label)
               .replace("knowledge/raw/live (sync_live.py)", str(out.relative_to(ROOT)).replace("\\", "/")))
    d = la.build()
    d["meta"] = {"last_run": time.strftime("%Y-%m-%dT%H:%M")}
    la.write_html(d)
    return la.OUT_HTML


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--prefix", default=DEFAULT_PREFIX)
    ap.add_argument("--out", default="knowledge/raw/competitors/vpbanks")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--delay", type=float, default=1.5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--inlink-sample", type=int, default=0, help="pages per other section to sample")
    ap.add_argument("--graph-only", action="store_true", help="rebuild link-graph.html from existing CSVs")
    a = ap.parse_args()

    setup(a.host, a.prefix)
    out = ROOT / a.out
    label = a.host.split("//")[-1].replace("www.", "") + a.prefix.rstrip("/")
    if a.graph_only:
        print(f"graph -> {write_graph(out, a.host, a.prefix, label).relative_to(ROOT)}")
        return 0
    (out / "html").mkdir(parents=True, exist_ok=True)
    all_urls = sitemap(a.host)
    urls = sorted({u.rstrip("/") for u in all_urls
                   if u.startswith(a.host + a.prefix) and u.rstrip("/") != a.host + a.prefix.rstrip("/")})
    if a.limit:
        urls = urls[:a.limit]
    print(f"{len(urls)} article URLs in sitemap under {a.prefix}")

    with ThreadPoolExecutor(a.workers) as ex:
        results = [r for r in ex.map(lambda u: crawl_one(u, out, a.delay), urls) if r]
    pages = {p["slug"]: p for p, _, _ in results}
    links = [ln for _, lns, _ in results for ln in lns]
    sl.build_pages(pages, links)
    sl.write_csv(out / "pages.csv", PAGE_FIELDS, sorted(pages.values(), key=lambda p: p["published"]))
    sl.write_csv(out / "links.csv", sl.LINK_FIELDS, links)
    (out / "outlines.json").write_text(json.dumps([o for _, _, o in results], ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    print(f"ok {len(pages)}/{len(urls)} pages, {len(links)} links -> {out.relative_to(ROOT)}")
    print(f"graph -> {write_graph(out, a.host, a.prefix, label).relative_to(ROOT)}")

    if a.inlink_sample:
        rows = sample_inlinks(a.host, a.prefix, all_urls, a.inlink_sample, a.delay)
        sl.write_csv(out / "inlinks_sample.csv", ["section", "url", "kb_links", "targets"], rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
