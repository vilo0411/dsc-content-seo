#!/usr/bin/env python3
"""Aggregate People Also Ask + Related Searches from cached SERP files into an opportunity report.

Reads every knowledge/raw/serp/*.json written by serp_research.py (0 API calls), dedupes the
questions/keywords, matches each against existing DSC articles (sitemap-cache + anchor-index)
and writes knowledge/3-pipeline/serp-opportunities.md:

    1. Chưa có bài        -> input for /keyword-plan, /cluster
    2. Có bài, chưa giữ PAA -> input for /optimize (add/refresh FAQ)
    3. DSC đang giữ PAA   -> keep, don't cannibalise
    4. Per-keyword appendix

Usage:
    python scripts/serp_opportunities.py [--json] [--min-count N]
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SERP_DIR = ROOT / "knowledge/raw/serp"
SITEMAP_CACHE = ROOT / ".antigravity/skills/internal-linking/scripts/sitemap-cache.json"
ANCHOR_INDEX = ROOT / "knowledge/3-pipeline/anchor-index.md"
OUT = ROOT / "knowledge/3-pipeline/serp-opportunities.md"
OWN_DOMAIN = "dsc.com.vn"
MATCH_RATIO = 0.7   # share of query content-words that must appear in an article slug/anchor
BIGRAM_RATIO = 0.6  # share of query bigrams that must appear too (keeps compound terms apart)

STOP = {"la", "gi", "co", "cua", "va", "cac", "nhung", "de", "khi", "nao", "the", "thi", "nen",
        "bao", "nhieu", "cach", "lam", "sao", "o", "dau", "toi", "ban", "can", "muon", "khong",
        "phai", "hay", "voi", "cho", "ve", "tu", "su", "giua", "biet", "khac", "nam", "20", "2025",
        "2026", "hien", "nay"}


def ascii_words(text: str) -> list[str]:
    t = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return [w for w in re.split(r"[^a-z0-9]+", t) if len(w) > 1 and w not in STOP]


def key(text: str) -> str:
    return " ".join(ascii_words(text))


# ---------------------------------------------------------------- existing content

def bigrams(words: list[str]) -> set[tuple[str, str]]:
    return {(words[i], words[i + 1]) for i in range(len(words) - 1)}


def load_articles() -> list[tuple[str, set[str], set[tuple[str, str]]]]:
    """(url, words, bigrams) for every known DSC article: sitemap slugs + anchor-index anchors/titles.

    Bigrams keep compound terms apart (chứng khoán ≠ chứng chỉ quỹ) where single words collide."""
    arts: dict[str, tuple[set, set]] = {}

    def add(url, text):
        w = ascii_words(text)
        uni, bi = arts.setdefault(url, (set(), set()))
        uni.update(w)
        bi.update(bigrams(w))

    if SITEMAP_CACHE.exists():
        for u in json.loads(SITEMAP_CACHE.read_text(encoding="utf-8")).get("urls", []):
            u = u.rstrip("/")
            add(u, u.rsplit("/", 1)[-1].replace("-", " "))
    if ANCHOR_INDEX.exists():
        for line in ANCHOR_INDEX.read_text(encoding="utf-8").splitlines():
            if "dsc.com.vn/" not in line or not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            url = next((c for c in cells if c.startswith("http")), None)
            if not url:
                continue
            url = url.rstrip("/")
            add(url, url.rsplit("/", 1)[-1].replace("-", " "))
            for c in cells:
                if not c.startswith("http"):
                    add(url, c)
    return [(u, uni, bi) for u, (uni, bi) in arts.items()]


def find_article(text: str, articles) -> tuple[str | None, int]:
    """(url, confidence%) of the best article covering >=MATCH_RATIO words and >=BIGRAM_RATIO bigrams."""
    words = ascii_words(text)
    if not words:
        return None, 0
    qb = bigrams(words)
    best, best_score = None, 0.0
    for url, uni, bi in articles:
        r_uni = sum(w in uni for w in words) / len(words)
        r_bi = (sum(b in bi for b in qb) / len(qb)) if qb else r_uni
        if r_uni >= MATCH_RATIO and r_bi >= BIGRAM_RATIO and r_uni + r_bi > best_score:
            best, best_score = url, r_uni + r_bi
    return best, int(best_score * 50)


# ---------------------------------------------------------------- SERP cache

def normalize_paa(paa):
    out = []
    for q in paa or []:
        if isinstance(q, str):
            out.append({"question": q, "answer_snippet": "", "source_domain": "", "source_url": ""})
        elif isinstance(q, dict) and q.get("question"):
            out.append(q)
    return out


def load_serp():
    files = sorted(glob.glob(str(SERP_DIR / "*.json")))
    data = []
    for f in files:
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        if not d.get("keyword"):
            continue
        data.append({
            "keyword": d["keyword"],
            "fetched_at": d.get("fetched_at", ""),
            "paa": normalize_paa(d.get("people_also_ask")),
            "related": [r for r in d.get("related_searches") or [] if isinstance(r, str)],
            "featured": (d.get("featured_snippet") or {}).get("domain") or "",
        })
    return data


# ---------------------------------------------------------------- aggregate

def aggregate(serp, articles):
    items: dict[str, dict] = {}
    for s in serp:
        for q in s["paa"]:
            k = key(q["question"])
            if not k:
                continue
            it = items.setdefault(k, {"text": q["question"], "type": "PAA", "seeds": [], "owner": "",
                                      "answer": ""})
            it["seeds"].append(s["keyword"])
            if q.get("source_domain") and not it["owner"]:
                it["owner"] = q["source_domain"]
                it["answer"] = (q.get("answer_snippet") or "")[:160]
        for r in s["related"]:
            k = key(r)
            if not k:
                continue
            it = items.setdefault(k, {"text": r, "type": "Related", "seeds": [], "owner": "", "answer": ""})
            if it["type"] == "Related":
                it["seeds"].append(s["keyword"])
    for it in items.values():
        it["seeds"] = sorted(set(it["seeds"]))
        it["count"] = len(it["seeds"])
        it["article"], it["confidence"] = find_article(it["text"], articles)
        it["dsc_owns"] = OWN_DOMAIN in it["owner"]
    return sorted(items.values(), key=lambda x: (-x["count"], x["type"], x["text"]))


def bucket(items):
    new, optimize, keep = [], [], []
    for it in items:
        if it["dsc_owns"]:
            keep.append(it)
        elif it["article"]:
            optimize.append(it)
        else:
            new.append(it)
    return new, optimize, keep


# ---------------------------------------------------------------- render

def short_url(u: str | None) -> str:
    return u.replace("https://www.dsc.com.vn/kien-thuc/", "") if u else "—"


def render(serp, items, min_count):
    new, optimize, keep = bucket(items)
    n_paa = sum(len(s["paa"]) for s in serp)
    n_rel = sum(len(s["related"]) for s in serp)
    L = [
        "---",
        "generated: %s" % time.strftime("%Y-%m-%d %H:%M"),
        "sources: %d SERP cache files" % len(serp),
        "---",
        "",
        "# SERP Opportunities — People Also Ask & Related Searches",
        "",
        "> Sinh tự động bởi `scripts/serp_opportunities.py` từ `knowledge/raw/serp/*.json`. Không sửa tay.",
        "> Refresh: `python scripts/serp_opportunities.py` (0 API call — chỉ đọc cache).",
        "",
        "**Tổng:** %d keyword đã research · %d câu PAA · %d related searches → %d mục sau dedupe."
        % (len(serp), n_paa, n_rel, len(items)),
        "",
        "| Nhóm | Số mục | Dùng cho |",
        "|---|---|---|",
        "| 1. Chưa có bài | %d | `/keyword-plan`, `/cluster` — ứng viên bài mới |" % len(new),
        "| 2. Có bài, chưa giữ PAA | %d | `/optimize` — bổ sung/sửa FAQ để chiếm PAA |" % len(optimize),
        "| 3. DSC đang giữ PAA | %d | Giữ nguyên, không viết bài trùng |" % len(keep),
        "",
        "*Cột “Bài hiện có” là heuristic từ khoá (≥%d%% từ + ≥%d%% cụm từ khớp slug/anchor, kèm %% tin cậy) — kiểm tra lại trước khi quyết định.*"
        % (int(MATCH_RATIO * 100), int(BIGRAM_RATIO * 100)),
        "",
    ]

    def table(rows, with_article):
        hdr = "| Loại | Câu hỏi / keyword | Xuất hiện ở | " + ("Bài hiện có | Ai giữ PAA |" if with_article else "")
        L.append(hdr)
        L.append("|---|---|---|" + ("---|---|" if with_article else ""))
        for it in rows:
            if it["count"] < min_count:
                continue
            seeds = "; ".join(it["seeds"][:3]) + (" (+%d)" % (it["count"] - 3) if it["count"] > 3 else "")
            row = "| %s | %s | %s |" % (it["type"], it["text"], seeds)
            if with_article:
                row += " %s (%d%%) | %s |" % (short_url(it["article"]), it["confidence"], it["owner"] or "—")
            L.append(row)
        L.append("")

    L += ["## 1. Chưa có bài — ứng viên nội dung mới", "",
          "PAA xuất hiện ở nhiều keyword = nhu cầu rộng, ưu tiên cao. Related khác intent với keyword gốc → bài riêng.", ""]
    table(new, with_article=False)

    L += ["## 2. Có bài nhưng chưa giữ PAA — ứng viên `/optimize`", "",
          "Thêm câu hỏi vào FAQ (câu đầu ≤ 60 từ, có số liệu + mốc thời gian) hoặc nâng thành H2/H3.", ""]
    table(optimize, with_article=True)

    L += ["## 3. DSC đang giữ PAA — giữ vững", ""]
    if keep:
        table(keep, with_article=True)
    else:
        L += ["(Chưa có — cache cũ trước 2026-09-18 không lưu domain nguồn PAA; sẽ có sau lần research kế tiếp.)", ""]

    L += ["## 4. Chi tiết theo keyword", ""]
    for s in serp:
        L.append("### %s  *(fetched %s%s)*" % (s["keyword"], s["fetched_at"],
                                              "; featured: " + s["featured"] if s["featured"] else ""))
        for q in s["paa"]:
            tag = " ⚑ DSC" if OWN_DOMAIN in (q.get("source_domain") or "") else (
                " (%s)" % q["source_domain"] if q.get("source_domain") else "")
            L.append("- PAA: %s%s" % (q["question"], tag))
        if s["related"]:
            L.append("- Related: " + " · ".join(s["related"]))
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="print aggregated items as JSON instead of writing the report")
    ap.add_argument("--min-count", type=int, default=1, help="only list items seen in >= N seed keywords")
    args = ap.parse_args()

    serp = load_serp()
    if not serp:
        sys.exit("No SERP cache in %s — run serp_research.py first." % SERP_DIR)
    items = aggregate(serp, load_articles())
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return
    OUT.write_text(render(serp, items, args.min_count), encoding="utf-8")
    new, optimize, keep = bucket(items)
    print("Wrote %s — %d keywords, %d items (new %d / optimize %d / keep %d)"
          % (OUT.relative_to(ROOT), len(serp), len(items), len(new), len(optimize), len(keep)))


if __name__ == "__main__":
    main()
