#!/usr/bin/env python3
"""Deterministic QA linter for DSC SEO articles.

Runs the machine-checkable subset of the Quality Guardian checklist so the LLM
only has to reason about semantics (persona, market facts, So-What / Prove-It).

Usage:
    python scripts/qa_lint.py <draft.md> [--outline outline.md] [--original Final-x.md]
                              [--keyword "..."] [--fix] [--json] [--log] [--no-sitemap]

Exit:   0 = PASS (0 CRITICAL, 0 MAJOR)   1 = FAIL   2 = usage / IO error

Rule sources (parsed at runtime, never hardcoded when a file exists):
    knowledge/3-pipeline/anti-ai-rules-blacklist.md     -> CL2 trigger phrases
    knowledge/3-pipeline/glossary.md  (section 7)        -> CL3 forbidden terms
    .antigravity/skills/internal-linking/scripts/sitemap-cache.json -> link verification
    <outline>.md  PAA_Questions: (with --outline)         -> PAA-missing / FAQ-few-paa (AEO)
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import unicodedata
import sys
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # reconfigure in place: a new TextIOWrapper would close the buffer when GC'd
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
BLACKLIST_FILE = ROOT / "knowledge/3-pipeline/anti-ai-rules-blacklist.md"
GLOSSARY_FILE = ROOT / "knowledge/3-pipeline/glossary.md"
SITEMAP_CACHE = ROOT / ".antigravity/skills/internal-linking/scripts/sitemap-cache.json"
REVISION_LOG = ROOT / "knowledge/3-pipeline/revision-log.md"
COUNT_WORDS_DIR = ROOT / ".antigravity/skills/qa-qc"

DSC_HOST = "https://www.dsc.com.vn"
OPEN_ACCOUNT_URL = f"{DSC_HOST}/mo-tai-khoan"

MAX_TITLE = 59
META_RANGE = (140, 160)
MAX_SENTENCE_WORDS = 30
MAX_PARA_SENTENCES = 3
MAX_PROSE_RUN = 3
MIN_INTERNAL_LINKS = 3

# Composite score weights (sum = 100)
WEIGHTS = {"anti_ai": 30, "seo": 25, "readability": 20, "link": 15, "geo": 10}
PENALTY = {"CRITICAL": 25, "MAJOR": 10, "MINOR": 3}
MINOR_CAP = 30  # MINOR findings can cost a category at most this many points

HIDDEN_UNICODE = re.compile("[​‌‍⁠﻿­]")
VAGUE_TEMPORAL = [
    "gần đây,", "hiện nay,", "trong những năm qua", "thời gian gần đây",
    "trong thời gian qua", "những năm gần đây",
]
TEMPORAL_MARKER = re.compile(
    r"(tính đến tháng \d{1,2}/\d{4}|tháng \d{1,2}/\d{4}|quý \d/\d{4}|q[1-4][/–-]?(q[1-4]/)?\d{4}|năm 20\d{2}|"
    r"\b\d{1,2}/\d{4}\b)", re.I)
DATA_POINT = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|tỷ|triệu|nghìn|điểm)", re.I)
GENERIC_ANCHORS = {"xem thêm", "tại đây", "click vào đây", "ở đây", "bài viết này", "link"}


@dataclass
class Finding:
    check: str
    category: str
    severity: str
    line: int
    message: str
    excerpt: str = ""


@dataclass
class Report:
    file: str
    findings: list[Finding] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def add(self, check, category, severity, line, message, excerpt=""):
        self.findings.append(Finding(check, category, severity, line, message, excerpt.strip()[:120]))

    def count(self, sev):
        return sum(1 for f in self.findings if f.severity == sev)

    def score(self) -> tuple[int, dict]:
        per_cat = {}
        for cat, w in WEIGHTS.items():
            s, minor = 100, 0
            for f in self.findings:
                if f.category != cat:
                    continue
                if f.severity == "MINOR":
                    minor += PENALTY["MINOR"]
                else:
                    s -= PENALTY[f.severity]
            per_cat[cat] = max(0, s - min(minor, MINOR_CAP))
        composite = round(sum(per_cat[c] * WEIGHTS[c] for c in WEIGHTS) / 100)
        return composite, per_cat

    def passed(self) -> bool:
        return self.count("CRITICAL") == 0 and self.count("MAJOR") == 0


# ─────────────────────────── Rule loading ───────────────────────────

def load_blacklist() -> tuple[list[str], list[str], list[str]]:
    """Return (hard_phrases, hedge_words, soft_words) from anti-ai-rules-blacklist.md."""
    hard, hedge, soft = [], [], []
    if not BLACKLIST_FILE.exists():
        return hard, hedge, soft
    section, sub = "", ""
    for line in BLACKLIST_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section, sub = line, ""
            continue
        if line.startswith("**"):
            sub = line.lower()
            continue
        if not line.strip().startswith("- "):
            continue
        # Section 3 lines look like: - "a" / "b" → dùng "c"  → keep left-hand side only
        src = line.split("→")[0] if "## 3" in section else line
        for q in re.findall(r'"([^"]+)"', src):
            q = q.replace("...", "").strip().rstrip(".,").strip()
            if not q or "[" in q:  # skip templates like "[Keyword] là gì?"
                continue
            if "## 3" in section:
                soft.append(q)
            elif "## 1" in section:
                (hedge if "hedge" in sub else hard).append(q)
    return hard, hedge, soft


def load_forbidden_terms() -> list[str]:
    terms = []
    if not GLOSSARY_FILE.exists():
        return terms
    in_sec = False
    for line in GLOSSARY_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_sec = "Từ bị cấm" in line or "Forbidden" in line
            continue
        if in_sec and line.startswith("|") and not line.startswith("|---") and "Từ bị cấm" not in line:
            cell = line.split("|")[1]
            for part in cell.split("/"):
                t = re.sub(r"\(.*?\)", "", part).strip().strip('"').strip()
                if t:
                    terms.append(t)
    return terms


def load_sitemap() -> set[str]:
    if not SITEMAP_CACHE.exists():
        return set()
    data = json.loads(SITEMAP_CACHE.read_text(encoding="utf-8"))
    return {u.rstrip("/") for u in data.get("urls", [])}


# ─────────────────────────── Parsing ───────────────────────────

def split_frontmatter(text: str) -> tuple[dict, int, list[str]]:
    """Return (frontmatter dict, body_start_line_index, all_lines)."""
    lines = text.split("\n")
    fm = {}
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return fm, i + 1, lines
            m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", lines[i])
            if m:
                fm[m.group(1)] = m.group(2).strip()
    return fm, 0, lines


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def strip_md(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[*_`]", "", s)
    return s.strip()


def split_sentences(text: str) -> list[str]:
    # Protect decimals / thousands (5,8 / 1.000) and common abbreviations
    t = re.sub(r"(\d)[.,](\d)", r"\1<d>\2", text)
    t = re.sub(r"\b(TP|Tp|TS|ThS|PGS|GS|Q)\.", r"\1<a>", t)
    parts = re.split(r"(?<=[.!?…])\s+(?=[^\s])", t)
    return [p.replace("<d>", ",").replace("<a>", ".").strip() for p in parts if p.strip()]


def word_count(s: str) -> int:
    return len(strip_md(s).split())


def classify(line: str) -> str:
    s = line.strip()
    if not s:
        return "blank"
    if s.startswith("```"):
        return "fence"
    if re.match(r"^#{1,6}\s", s):
        return "heading"
    if re.match(r"^(\*|-|\+|\d+[.)])\s", s):
        return "list"
    if s.startswith("|"):
        return "table"
    if s.startswith(">"):
        return "quote"
    if re.match(r"^!\[", s) or re.match(r"^\[!\[", s):
        return "image"
    if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
        return "hr"
    if s.startswith("<"):
        return "html"
    return "text"


# ─────────────────────────── Checks ───────────────────────────

def check_frontmatter(rep: Report, fm: dict, keyword: str):
    if not fm:
        rep.add("CL1-frontmatter", "seo", "MAJOR", 1,
                "Không có front matter (Title / Meta_Description / Target_Keyword / Slug) — bỏ qua check title/meta/keyword")
        return
    title = fm.get("Title", "")
    meta = fm.get("Meta_Description", "")
    if not title:
        rep.add("CL1-title", "seo", "CRITICAL", 1, "Thiếu Title trong front matter")
    else:
        if len(title) > MAX_TITLE:
            rep.add("CL1-title", "seo", "CRITICAL", 2,
                    f"Title dài {len(title)} ký tự (tối đa {MAX_TITLE})", title)
        if keyword and norm(keyword) not in norm(title):
            rep.add("CL1-title", "seo", "MAJOR", 2, "Title không chứa target keyword", title)
    if not meta:
        rep.add("CL1-meta", "seo", "CRITICAL", 1, "Thiếu Meta_Description")
    else:
        lo, hi = META_RANGE
        if not (lo <= len(meta) <= hi):
            rep.add("CL1-meta", "seo", "CRITICAL", 3,
                    f"Meta description dài {len(meta)} ký tự (cần {lo}–{hi})", meta)
        if keyword and norm(keyword) not in norm(meta):
            rep.add("CL1-meta", "seo", "MAJOR", 3, "Meta description không chứa target keyword", meta)
    for k, v in fm.items():
        if v.startswith('"') and v.endswith('"'):
            rep.add("FM-quotes", "seo", "MINOR", 1, f"Front matter `{k}` bọc trong ngoặc kép", v)


def check_headings(rep: Report, lines, start, keyword):
    h1s, prev = [], 0
    in_fence = False
    for i in range(start, len(lines)):
        s = lines[i].strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if not m:
            continue
        lvl, text = len(m.group(1)), m.group(2)
        if lvl == 1:
            h1s.append((i + 1, text))
        if prev and lvl > prev + 1:
            rep.add("CL1-hierarchy", "seo", "MAJOR", i + 1, f"Nhảy cấp heading H{prev} → H{lvl}", text)
        prev = lvl
    if len(h1s) != 1:
        rep.add("CL1-h1", "seo", "CRITICAL", h1s[0][0] if h1s else start + 1,
                f"Bài có {len(h1s)} H1 (cần đúng 1)")
    elif keyword and norm(keyword) not in norm(h1s[0][1]):
        rep.add("CL1-h1", "seo", "CRITICAL", h1s[0][0], "H1 không chứa target keyword chính xác", h1s[0][1])
    rep.stats["h1"] = h1s[0][1] if h1s else ""


def check_keyword_in_sapo(rep, lines, start, keyword):
    if not keyword:
        return
    words, first_line = [], None
    for i in range(start, len(lines)):
        if classify(lines[i]) == "text":
            first_line = first_line or i + 1
            words += strip_md(lines[i]).split()
            if len(words) >= 150:
                break
    # Sapo only needs the core term, not question suffixes like "là gì"
    core = re.sub(r"\s+(là gì|là sao|như thế nào|có nên không)\s*$", "", norm(keyword)).strip() or norm(keyword)
    if words and core not in norm(" ".join(words)):
        rep.add("CL1-sapo", "seo", "MINOR", first_line or start + 1,
                f"Target keyword “{core}” không xuất hiện trong 150 từ đầu (sapo)")


def check_anti_ai(rep, lines, start, hard, hedge, soft, forbidden):
    hedge_hits = []
    in_fence = False
    for i in range(start, len(lines)):
        raw = lines[i]
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        low = raw.lower()
        for p in hard:
            if p.lower() in low:
                rep.add("CL2-blacklist", "anti_ai", "CRITICAL", i + 1, f"Trigger phrase bị cấm: “{p}”", raw)
        for p in soft:
            if p.lower() in low:
                sev = "MINOR" if p.lower() == "rõ ràng" else "MAJOR"
                rep.add("CL2-softban", "anti_ai", sev, i + 1, f"Từ bị cấm (instincts): “{p}”", raw)
        for p in hedge:
            if re.search(r"(?<!\w)" + re.escape(p.lower()) + r"(?!\w)", low):
                hedge_hits.append((i + 1, p))
        for t in forbidden:
            if t.lower() in low:
                rep.add("CL3-forbidden", "seo", "CRITICAL", i + 1, f"Forbidden term (glossary §7): “{t}”", raw)
        for m in re.finditer(r"[\"“]([^\"”\n]{1,60})[\"”]", raw):
            inner = m.group(1).strip()
            n = len(inner.split())
            before = raw[max(0, m.start() - 12):m.start()].lower()
            if 1 <= n <= 4 and not inner[0].isupper() and not re.search(r"\d", inner) \
                    and not re.search(r"(:|nói|rằng|gọi là|từ khóa|lệnh|nút|tab|mục)\s*$", before):
                rep.add("CL2-quotes", "anti_ai", "MAJOR", i + 1, f"Emphatic quotes quanh từ thường: “{inner}”", raw)
        if HIDDEN_UNICODE.search(raw):
            rep.add("SCRUB-unicode", "anti_ai", "MINOR", i + 1, "Ký tự unicode ẩn (zero-width/BOM)")
        if re.match(r"^\s*>\s*\[!\w+\]", raw):
            rep.add("FMT-callout", "readability", "MAJOR", i + 1, "Callout `> [!NOTE]` không render trên CMS", raw)
        for vt in VAGUE_TEMPORAL:
            if vt in low:
                rep.add("GEO-vague-time", "geo", "MAJOR", i + 1, f"Mốc thời gian mơ hồ “{vt.strip(',')}” — thay bằng Tháng M/Y", raw)
    if len(hedge_hits) > 3:
        rep.add("CL2-hedge", "anti_ai", "MAJOR", hedge_hits[0][0],
                f"Hedge words dùng {len(hedge_hits)} lần (>3): " + ", ".join(sorted({h for _, h in hedge_hits})))


def check_brand_format(rep, lines, start):
    in_fence = False
    for i in range(start, len(lines)):
        raw = lines[i]
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.search(r"\bVN\s?Index\b", raw) and "VN-Index" not in raw:
            rep.add("CL3-vnindex", "seo", "MAJOR", i + 1, "Viết `VN-Index` (có gạch ngang)", raw)
        for m in re.finditer(r"\d\.\d{1,2}(?!\d)\s*%", raw):
            rep.add("CL3-decimal", "seo", "MAJOR", i + 1, f"Số thập phân dùng dấu chấm: “{m.group(0)}” → dùng dấu phẩy", raw)
        low = raw.lower()
        if "lãi suất" in low:
            for m in re.finditer(r"\d+(?:,\d+)?\s*%(?!\s*/\s*năm)(?!\s*[-–]\s*\d)", raw):
                tail = raw[m.end():m.end() + 12].lower()
                if "/năm" not in tail and "năm" not in tail:
                    rep.add("CL3-rate-unit", "seo", "MINOR", i + 1, f"Lãi suất thiếu `/năm`: “{m.group(0)}”", raw)
                    break
        # DSC fact constants (CL5) — checked per sentence that names DSC
        if "dsc" in low:
            for sent in split_sentences(strip_md(raw)):
                sl = sent.lower()
                if "dsc" not in sl:
                    continue
                pcts = re.findall(r"(\d+(?:,\d+)?)\s*%", sent)
                if "phí giao dịch" in sl:
                    for p in pcts:
                        if float(p.replace(",", ".")) > 0.5:
                            rep.add("CL5-fact", "seo", "MAJOR", i + 1,
                                    f"Phí giao dịch DSC ghi {p}% — chuẩn là từ 0,1% [CẦN XÁC NHẬN]", sent)
                if "margin" in sl:
                    for p in pcts:
                        v = float(p.replace(",", "."))
                        if not (10 <= v <= 13.5):
                            rep.add("CL5-fact", "seo", "MAJOR", i + 1,
                                    f"Lãi margin DSC ghi {p}% — chuẩn 10–13,5%/năm [CẦN XÁC NHẬN]", sent)
                if "ekyc" in sl and re.search(r"\d+\s*phút", sl) and "3 phút" not in sl:
                    rep.add("CL5-fact", "seo", "MAJOR", i + 1, "Thời gian eKYC DSC chuẩn là 3 phút", sent)
                if "định danh" in sl:
                    for m in re.finditer(r"\b\d{6}\b", sent):
                        if m.group(0) != "963369":
                            rep.add("CL5-fact", "seo", "MAJOR", i + 1, "Mã định danh nạp tiền DSC chuẩn là 963369", sent)
        if re.search(r"\$\$?[^$\n]{1,80}\$\$?", raw) and "VNĐ" not in raw and "USD" not in raw:
            rep.add("FMT-latex", "readability", "MAJOR", i + 1, "Công thức LaTeX `$...$` — viết bằng in đậm thường", raw)
        if classify(raw) == "list":
            if re.match(r"^\s*(\*|-|\+|\d+[.)])\s+\*\*[^*]+\.\*\*", raw):
                rep.add("FMT-bold-label", "readability", "MINOR", i + 1, "Nhãn in đậm kết thúc bằng `.` — dùng `**Nhãn**:`", raw)
            elif re.match(r"^\s*(\*|-|\+|\d+[.)])\s+\*\*[^*]+:\*\*", raw):
                rep.add("FMT-bold-label", "readability", "MINOR", i + 1, "Dấu `:` phải nằm ngoài bold — `**Nhãn**:`", raw)


def check_structure(rep, lines, start):
    kinds = [classify(l) for l in lines]
    in_fence = False
    prose_run = 0
    long_sent, long_para = [], []
    fence_lines = []
    for i in range(start, len(lines)):
        k = kinds[i]
        if k == "fence":
            in_fence = not in_fence
            if in_fence:
                fence_lines.append(i + 1)
            continue
        if in_fence:
            continue
        if k == "hr":
            rep.add("FMT-hr", "readability", "MAJOR", i + 1, "Đường kẻ ngang `---` giữa các phần — xóa")
        if k == "text":
            prose_run += 1
            sents = split_sentences(strip_md(lines[i]))
            if len(sents) > MAX_PARA_SENTENCES:
                long_para.append((i + 1, len(sents)))
            for s in sents:
                n = len(s.split())
                if n > MAX_SENTENCE_WORDS:
                    long_sent.append((i + 1, n, s))
        elif k == "list":
            sents = split_sentences(strip_md(re.sub(r"^\s*(\*|-|\+|\d+[.)])\s+", "", lines[i])))
            for s in sents:
                n = len(s.split())
                if n > MAX_SENTENCE_WORDS:
                    long_sent.append((i + 1, n, s))
            if len(sents) > 2:
                rep.add("CL6-list-item", "readability", "MINOR", i + 1, f"List item chứa {len(sents)} câu — tách hoặc chuyển thành đoạn văn")
        if k in ("heading", "list", "table", "image", "quote", "html"):
            prose_run = 0
        if prose_run > MAX_PROSE_RUN:
            rep.add("CL6-prose-run", "readability", "MINOR", i + 1, f"> {MAX_PROSE_RUN} đoạn văn liên tiếp không có visual (list/bảng/ảnh)")
            prose_run = 0
    for ln in fence_lines:
        rep.add("FMT-codeblock", "readability", "MAJOR", ln, "Code block trong bài — CMS không render, dùng bảng Markdown")
    for ln, n, s in long_sent:
        rep.add("CL6-sentence", "readability", "MINOR", ln, f"Câu dài {n} từ (>{MAX_SENTENCE_WORDS})", s)
    for ln, n in long_para:
        rep.add("CL6-paragraph", "readability", "MINOR", ln, f"Đoạn có {n} câu (>{MAX_PARA_SENTENCES})")
    if len(long_sent) > 5:
        rep.add("CL6-sentence", "readability", "MAJOR", long_sent[0][0], f"{len(long_sent)} câu vượt {MAX_SENTENCE_WORDS} từ — vi phạm nhiều")
    if len(long_para) > 3:
        rep.add("CL6-paragraph", "readability", "MAJOR", long_para[0][0], f"{len(long_para)} đoạn vượt {MAX_PARA_SENTENCES} câu — vi phạm nhiều")
    # consecutive lists with no prose between
    i = start
    while i < len(lines):
        if kinds[i] == "list":
            j = i
            while j < len(lines) and kinds[j] in ("list", "blank"):
                j += 1
            block = [k for k in kinds[i:j] if k != "blank"]
            # detect two list blocks separated by a blank line inside this run
            seg = kinds[i:j]
            if "blank" in seg:
                segs = "".join("L" if k == "list" else "_" for k in seg)
                if re.search(r"L_+L", segs):
                    # only flag when marker style changes (true separate lists)
                    markers = [re.match(r"^\s*(\*|-|\+|\d+[.)])", lines[x]).group(1)[0] for x in range(i, j) if kinds[x] == "list"]
                    if len(set(("n" if m.isdigit() else m) for m in markers)) > 1:
                        rep.add("CL6-lists", "readability", "MAJOR", i + 1, "2 danh sách liên tiếp không có đoạn văn ở giữa")
            i = j
        else:
            i += 1
    rep.stats["long_sentences"] = len(long_sent)
    rep.stats["long_paragraphs"] = len(long_para)


def check_links(rep, lines, start, sitemap: set[str], use_sitemap: bool):
    internal, has_open = [], False
    in_fence = False
    for i in range(start, len(lines)):
        raw = lines[i]
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r"(!?)\[([^\]]*)\]\(([^)\s]+)[^)]*\)", raw):
            is_img, text, url = m.group(1) == "!", m.group(2), m.group(3)
            if is_img:
                continue
            if url.startswith("file:///") or url.endswith(".md") or url.startswith("../") or url.startswith("./"):
                rep.add("LINK-local", "link", "CRITICAL", i + 1, f"Link cục bộ / relative: {url}", raw)
                continue
            if url.startswith("/"):
                rep.add("LINK-relative", "link", "CRITICAL", i + 1, f"URL tương đối `{url}` — dùng {DSC_HOST}{url}", raw)
                continue
            if url.startswith(DSC_HOST):
                if url.startswith(OPEN_ACCOUNT_URL):
                    has_open = True
                if "/kien-thuc/" in url:
                    internal.append((i + 1, text, url))
                    clean = url.split("?")[0].split("#")[0].rstrip("/")
                    if use_sitemap and sitemap and clean not in sitemap:
                        close = difflib.get_close_matches(clean, sitemap, n=1, cutoff=0.8)
                        hint = f" → gần nhất: {close[0]}" if close else " (chạy sync_sitemap.py nếu cache cũ)"
                        rep.add("LINK-sitemap", "link", "MAJOR", i + 1, f"URL không có trong sitemap: {url}{hint}", raw)
                if norm(text) in GENERIC_ANCHORS:
                    rep.add("LINK-anchor", "link", "MINOR", i + 1, f"Anchor text chung chung: “{text}”", raw)
            elif "dsc.com.vn" in url:
                rep.add("LINK-host", "link", "MAJOR", i + 1, f"URL DSC không chuẩn host `{DSC_HOST}`: {url}", raw)
    if not has_open:
        rep.add("LINK-cta", "link", "CRITICAL", start + 1, f"Thiếu link mở tài khoản {OPEN_ACCOUNT_URL}")
    if len(internal) < MIN_INTERNAL_LINKS:
        rep.add("LINK-count", "link", "MAJOR", start + 1, f"Chỉ có {len(internal)} internal link /kien-thuc/ (cần ≥ {MIN_INTERNAL_LINKS})")
    rep.stats["internal_links"] = len(internal)


def check_geo(rep, lines, start):
    body = "\n".join(lines[start:])
    h2 = len(re.findall(r"^##\s", body, re.M))
    markers = len(TEMPORAL_MARKER.findall(body))
    data_points = len(DATA_POINT.findall(body))
    rep.stats.update({"h2": h2, "temporal_markers": markers, "data_points": data_points})
    if data_points >= 5 and markers == 0:
        rep.add("GEO-no-marker", "geo", "MAJOR", start + 1,
                f"{data_points} data point nhưng 0 mốc thời gian (Tính đến tháng M/Y / Tháng M/Y:)")
    elif data_points >= 10 and markers < 2:
        rep.add("GEO-few-marker", "geo", "MINOR", start + 1, f"{data_points} data point, chỉ {markers} mốc thời gian")
    if h2 and markers > h2 * 2:
        rep.add("GEO-overuse", "geo", "MINOR", start + 1, f"{markers} mốc thời gian cho {h2} H2 — có dấu hiệu lạm dụng (§8.3)")


def check_images(rep, lines, start, original: Path):
    try:
        orig = original.read_text(encoding="utf-8")
    except OSError as e:
        rep.add("CL1-images", "seo", "MAJOR", 1, f"Không đọc được bài gốc: {e}")
        return
    body = "\n".join(lines[start:])
    orig_imgs = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", orig)
    missing = [u for u in orig_imgs if u not in body]
    for u in missing:
        rep.add("CL1-images", "seo", "CRITICAL", start + 1, f"Mất ảnh gốc: {u}")
    rep.stats["images_original"] = len(orig_imgs)
    rep.stats["images_missing"] = len(missing)


def check_word_count(rep, draft_path: Path, outline_path: Path):
    sys.path.insert(0, str(COUNT_WORDS_DIR))
    try:
        import count_words as cw  # type: ignore
    except ImportError:
        rep.add("WC", "seo", "MINOR", 1, "Không import được count_words.py — bỏ qua word count")
        return
    outline = cw.parse_outline(outline_path.read_text(encoding="utf-8"))
    draft = cw.parse_draft(draft_path.read_text(encoding="utf-8"))
    rep.stats["total_words"] = sum(s.words for s in draft)
    if not outline:
        return
    for o in outline:
        d = cw.find_best_match(o, draft)
        actual = d.words if d else 0
        if o.target is not None and actual < o.target * 0.9:
            rep.add("WC-under", "seo", "MAJOR", 1, f"[{o.title}] {actual}/{o.target} từ — thêm ~{o.target - actual} từ")
        elif o.max_words is not None and actual > o.max_words * 1.1:
            rep.add("WC-over", "seo", "MAJOR", 1, f"[{o.title}] {actual} từ vượt max {o.max_words} — rút ~{actual - o.max_words} từ")


# ─────────────────────────── PAA / FAQ (AEO) ───────────────────────────

FAQ_HEADING = re.compile(r"^##\s+.*(faq|câu hỏi thường gặp)", re.I)
FAQ_ITEM = re.compile(r"^(?:#{3,4}\s+(.+)|[-*+]\s+\*\*(.+?)\*\*\s*\??)")  # "### Q?" or "* **Q**?"
FAQ_MAX_FIRST_SENTENCE = 60
FAQ_MIN_PAA = 3
FAQ_BAD_OPENERS = ("câu trả lời là", "như đã đề cập", "như đã nói", "như đã phân tích", "có thể nói")
_PAA_STOP = {"la", "gi", "co", "cua", "va", "cac", "nhung", "de", "khi", "nao", "the", "thi", "nen",
             "bao", "nhieu", "cach", "lam", "sao", "o", "dau", "toi", "ban", "can", "muon", "khong",
             "phai", "hay", "voi", "cho", "ve", "tu", "su", "giua", "biet", "khac"}


def _ascii_words(text: str) -> list[str]:
    t = unicodedata.normalize("NFD", strip_md(text).lower().replace("đ", "d"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return [w for w in re.split(r"[^a-z0-9]+", t) if len(w) > 1 and w not in _PAA_STOP]


def _paa_match(question: str, candidate: str) -> bool:
    """Question is covered when ≥70% of its content words (accent-stripped) appear in candidate."""
    q, c = _ascii_words(question), set(_ascii_words(candidate))
    return bool(q) and sum(w in c for w in q) / len(q) >= 0.7


def parse_outline_paa(outline_text: str) -> list[dict]:
    """Read PAA_Questions from the outline YAML: `- q: "..."` + optional `placement: body|faq`."""
    out, cur, inside = [], None, False
    for line in outline_text.split("\n"):
        if re.match(r"^PAA_Questions\s*:", line):
            inside = True
            continue
        if inside:
            if re.match(r"^[A-Za-z_]+\s*:", line) or line.strip() in ("---", "```"):
                break
            m = re.match(r"""^\s*-\s*q\s*:\s*["']?(.+?)["']?\s*$""", line)
            if m:
                cur = {"q": m.group(1).strip(), "placement": "faq"}
                out.append(cur)
                continue
            m = re.match(r"^\s*placement\s*:\s*(\w+)", line)
            if m and cur:
                cur["placement"] = m.group(1).lower()
    return [q for q in out if q["q"] and not q["q"].startswith("[")]


def faq_items(lines, start) -> list[tuple[int, str, str]]:
    """(line_no, question, answer_text) for every item under the FAQ H2."""
    items, in_faq, i = [], False, start
    while i < len(lines):
        s = lines[i].strip()
        if re.match(r"^##\s", s):
            in_faq = bool(FAQ_HEADING.match(s))
            i += 1
            continue
        m = FAQ_ITEM.match(s) if in_faq else None
        if m:
            heading_q = m.group(1)
            if heading_q:  # heading item: answer is the following prose lines
                ans, j = [], i + 1
                while j < len(lines) and not re.match(r"^#{2,4}\s", lines[j].strip()):
                    if lines[j].strip():
                        ans.append(lines[j].strip())
                    j += 1
                items.append((i + 1, heading_q, " ".join(ans)))
                i = j
                continue
            items.append((i + 1, m.group(2), s[m.end():].lstrip("? ").strip()))  # bullet item
        i += 1
    return items


def check_faq_format(rep, lines, start, paa_count: int):
    items = faq_items(lines, start)
    rep.stats["faq_items"] = len(items)
    if not items:
        if paa_count:
            rep.add("FAQ-missing", "geo", "MAJOR", start + 1,
                    f"Outline có {paa_count} câu PAA nhưng draft không có H2 FAQ / câu hỏi thường gặp")
        return
    for ln, q, ans in items:
        first = split_sentences(strip_md(ans))[:1]
        first = first[0] if first else ""
        n = len(first.split())
        if n > FAQ_MAX_FIRST_SENTENCE:
            rep.add("FAQ-long-answer", "geo", "MINOR", ln,
                    f"Câu đầu đáp án FAQ {n} từ (> {FAQ_MAX_FIRST_SENTENCE}) — khó được trích làm PAA/AI Overview", q)
        if any(first.lower().startswith(o) for o in FAQ_BAD_OPENERS):
            rep.add("FAQ-indirect", "geo", "MINOR", ln, "Đáp án FAQ không trả lời trực diện ở câu đầu", first)


def check_paa(rep, lines, start, outline_path: Path) -> int:
    """Every PAA_Questions entry in the outline must surface as a heading or FAQ item in the draft."""
    try:
        paa = parse_outline_paa(outline_path.read_text(encoding="utf-8"))
    except OSError:
        return 0
    rep.stats["paa_questions"] = len(paa)
    if not paa:
        return 0
    headings = [strip_md(l.strip().lstrip("#").strip()) for l in lines[start:] if re.match(r"^#{2,4}\s", l.strip())]
    faq_qs = [q for _, q, _ in faq_items(lines, start)]
    missing = [it for it in paa if not any(_paa_match(it["q"], c) for c in headings + faq_qs)]
    for it in missing:
        where = "H2/H3 thân bài" if it["placement"] == "body" else "FAQ"
        rep.add("PAA-missing", "geo", "MAJOR", start + 1, f"Câu PAA chưa xuất hiện làm {where}: “{it['q']}”")
    in_faq = sum(1 for it in paa if any(_paa_match(it["q"], c) for c in faq_qs))
    need = min(FAQ_MIN_PAA, len(paa))
    if faq_qs and in_faq < need:
        rep.add("FAQ-few-paa", "geo", "MINOR", start + 1, f"FAQ chỉ có {in_faq}/{len(paa)} câu lấy từ PAA (cần ≥ {need})")
    rep.stats["paa_covered"] = len(paa) - len(missing)
    return len(paa)


# ─────────────────────────── Fix (safe, idempotent) ───────────────────────────

def apply_fixes(text: str) -> tuple[str, list[str]]:
    fixes = []
    fm_end = 0
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i + 1
                break
    head, body = "\n".join(lines[:fm_end]), "\n".join(lines[fm_end:])

    def sub(pattern, repl, label, flags=0):
        nonlocal body
        new, n = re.subn(pattern, repl, body, flags=flags)
        if n:
            fixes.append(f"{label} ×{n}")
            body = new

    sub(HIDDEN_UNICODE.pattern, "", "Xóa unicode ẩn")
    sub(r"\bVN\s?Index\b", "VN-Index", "VN Index → VN-Index")
    sub(r"(\d)\.(\d{1,2})(?!\d)(\s*%)", r"\1,\2\3", "Thập phân . → ,")
    sub(r"^[ \t]*>[ \t]*\[!(?:NOTE|TIP|INFO|WARNING|IMPORTANT)\][ \t]*\n[ \t]*>[ \t]*", "> **Lưu ý:** ",
        "Callout → > **Lưu ý:**", re.M | re.I)
    sub(r"^[ \t]*>[ \t]*\[!(?:NOTE|TIP|INFO|WARNING|IMPORTANT)\][ \t]*$", "> **Lưu ý:**",
        "Callout → > **Lưu ý:**", re.M | re.I)
    sub(r"^([ \t]*(?:\*|-|\+|\d+[.)])[ \t]+\*\*[^*\n]+?)\.\*\*([ \t]*)", r"\1**:\2", "**Nhãn.** → **Nhãn**:", re.M)
    sub(r"^([ \t]*(?:\*|-|\+|\d+[.)])[ \t]+\*\*[^*\n]+?):\*\*([ \t]*)", r"\1**:\2", "**Nhãn:** → **Nhãn**:", re.M)
    sub(r"^[ \t]*(-{3,}|\*{3,}|_{3,})[ \t]*\n", "", "Xóa --- giữa các phần", re.M)
    sub(r"[ \t]+$", "", "Xóa khoảng trắng cuối dòng", re.M)
    sub(r"(?<=\S)  +(?=\S)", " ", "Gộp khoảng trắng kép")
    sub(r"\n{3,}", "\n\n", "Gộp dòng trống thừa")
    out = (head + "\n" + body) if head else body
    return out, fixes


# ─────────────────────────── Output ───────────────────────────

def render(rep: Report) -> str:
    comp, cats = rep.score()
    out = [f"# QA LINT — {rep.file}", ""]
    out.append(f"**Kết quả:** {'PASS' if rep.passed() else 'FAIL'} · "
               f"CRITICAL {rep.count('CRITICAL')} · MAJOR {rep.count('MAJOR')} · MINOR {rep.count('MINOR')} · "
               f"**Score {comp}/100** (" + ", ".join(f"{k} {v}" for k, v in cats.items()) + ")")
    if rep.stats:
        out.append("Stats: " + ", ".join(f"{k}={v}" for k, v in rep.stats.items() if k != "h1"))
    if rep.fixes:
        out += ["", "Auto-fix đã áp dụng: " + "; ".join(rep.fixes)]
    order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}
    for sev in ("CRITICAL", "MAJOR", "MINOR"):
        items = [f for f in rep.findings if f.severity == sev]
        if not items:
            continue
        out += ["", f"## {sev} ({len(items)})", "", "| Dòng | Check | Vấn đề | Trích |", "|---:|---|---|---|"]
        for f in sorted(items, key=lambda x: (x.line, x.check)):
            ex = f.excerpt.replace("|", "\\|")
            out.append(f"| {f.line} | {f.check} | {f.message.replace('|', '\\|')} | {ex} |")
    if rep.passed():
        out += ["", "Lint PASS. Quality Guardian chỉ cần kiểm tra: CL4 Persona, CL5 số liệu thị trường, So-What / Prove-It, Load-Bearing Claim."]
    else:
        out += ["", "Sửa đúng các dòng CRITICAL/MAJOR ở trên rồi chạy lại. Tối đa 2 vòng — nếu vẫn FAIL, trình bày kèm danh sách còn lại."]
    return "\n".join(out)


def append_log(rep: Report, slug: str):
    comp, cats = rep.score()
    header = "## QA Score Log (auto — qa_lint.py)"
    # Append-only, preserving the file's existing line endings (repo files mix CRLF/LF).
    raw = REVISION_LOG.read_bytes() if REVISION_LOG.exists() else b""
    nl = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    row = (f"| {date.today().isoformat()} | {slug} | {comp} | {rep.count('CRITICAL')}/{rep.count('MAJOR')}/{rep.count('MINOR')} | "
           + " ".join(f"{k[:4]}={v}" for k, v in cats.items()) + " |")
    body = text.rstrip("\r\n")
    if header not in text:
        body += f"{nl}{nl}{header}{nl}{nl}| Ngày | Slug | Score | C/M/m | Theo nhóm |{nl}|---|---|---:|---|---|"
    body += nl + row + nl
    REVISION_LOG.write_bytes(body.encode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--outline", help="Outline file for section word-count targets")
    ap.add_argument("--original", help="Original Final file (optimize mode) to verify image preservation")
    ap.add_argument("--keyword", help="Override Target_Keyword from front matter")
    ap.add_argument("--fix", action="store_true", help="Apply safe idempotent fixes in place before linting")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of markdown")
    ap.add_argument("--log", action="store_true", help="Append score row to revision-log.md")
    ap.add_argument("--no-sitemap", action="store_true", help="Skip sitemap-cache URL verification")
    args = ap.parse_args()

    path = Path(args.draft)
    try:
        raw = path.read_bytes()
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    nl = "\r\n" if b"\r\n" in raw else "\n"  # remember original line endings for --fix
    text = raw.decode("utf-8").replace("\r\n", "\n")

    rep = Report(file=str(path))
    if args.fix:
        fixed, fixes = apply_fixes(text)
        if fixed != text:
            path.write_bytes(fixed.replace("\n", nl).encode("utf-8"))
            text = fixed
        rep.fixes = fixes

    fm, start, lines = split_frontmatter(text)
    keyword = args.keyword or fm.get("Target_Keyword", "")
    slug = fm.get("Slug") or re.sub(r"^(Final|Draft|Optimize)-", "", path.stem)
    rep.stats["keyword"] = keyword

    hard, hedge, soft = load_blacklist()
    forbidden = load_forbidden_terms()
    sitemap = set() if args.no_sitemap else load_sitemap()

    check_frontmatter(rep, fm, keyword)
    check_headings(rep, lines, start, keyword)
    check_keyword_in_sapo(rep, lines, start, keyword)
    check_anti_ai(rep, lines, start, hard, hedge, soft, forbidden)
    check_brand_format(rep, lines, start)
    check_structure(rep, lines, start)
    check_links(rep, lines, start, sitemap, not args.no_sitemap)
    check_geo(rep, lines, start)
    if args.original:
        check_images(rep, lines, start, Path(args.original))
    paa_count = 0
    if args.outline:
        check_word_count(rep, path, Path(args.outline))
        paa_count = check_paa(rep, lines, start, Path(args.outline))
    check_faq_format(rep, lines, start, paa_count)

    if args.log:
        append_log(rep, slug)

    if args.json:
        comp, cats = rep.score()
        print(json.dumps({"file": rep.file, "pass": rep.passed(), "score": comp, "categories": cats,
                          "stats": rep.stats, "fixes": rep.fixes,
                          "findings": [asdict(f) for f in rep.findings]}, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    return 0 if rep.passed() else 1


if __name__ == "__main__":
    sys.exit(main())
