#!/usr/bin/env python3
"""Statistical AI-slop detector for DSC SEO articles (layer B of the 3-layer QA).

Layer A = qa_lint.py (lexicon + format, deterministic).
Layer B = this script: measures *behaviour* of the text, not banned words - flat
          sentence rhythm, low evidence density, empty sentences, synonym cycling,
          template reuse across the corpus. Catches AI slop whose vocabulary is clean.
Layer C = Quality Guardian CL1-CL10 (judgement).

Usage:
    python scripts/slop_check.py <file.md> [--json] [--verbose]
    python scripts/slop_check.py --baseline [--glob 3-finalized] [--csv out.csv] [--top 15]
    python scripts/slop_check.py --thresholds

Exit:   0 = PASS   1 = FAIL (slop score < 80)   2 = usage / IO error
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FINAL_DIR, setup_utf8, split_frontmatter, body_end, slug_from_path,  # noqa: E402
                     read_text, unaccent)

setup_utf8()

# --------------------- Thresholds ---------------------
# RELATIVE, calibrated on the 182-article Final corpus (2026-10-16 DSC baseline):
# MAJOR sits at ~p90-p95 of the bad tail, MINOR at ~p75. A flag therefore means
# "worse than most of what we already ship", which is what a gate can enforce today.
# Re-derive after any big content push:  python scripts/slop_check.py --baseline
#
# NOTE - the corpus is itself flat on rhythm (median burstiness 5.3 words, median
# short_share 0.00 - the average article has no sentence <=7 words - median uniform_run 8).
# ABSOLUTE targets to migrate to once new articles clear the relative gate:
# rhythm_gap <= 12, burstiness >= 8, uniform_run <= 9, evidence_per_100w >= 2.5.
# Tighten in steps; do not jump straight to absolute or most of the back-catalogue
# fails at once. Evidence density is already the corpus' strong axis (median 2.20/100w).
T = {
    "burstiness_major": 3.2,      # stdev of sentence length (words); lower = flat AI rhythm
    "burstiness_minor": 4.2,
    "uniform_run_major": 24,      # consecutive sentences all 14-24 words
    "uniform_run_minor": 14,
    "rhythm_gap_major": 82,       # consecutive sentences all > 7 words (no breath)
    "rhythm_gap_minor": 55,
    "evidence_major": 0.75,       # evidence tokens per 100 words; lower = claim-only prose
    "evidence_minor": 1.30,
    "unanchored_major": 0.80,     # share of prose sentences with no verifiable anchor
    "unanchored_minor": 0.66,
    "vague_major": 1.10,          # vague/filler sentences per 1000 words
    "vague_minor": 0.60,
    "hedge_para_major": 3,        # hedge words inside a single paragraph
    "hedge_para_minor": 2,
    "synonym_major": 3,           # distinct variants used for the same object
    "synonym_minor": 2,
    "template_major": 0.55,       # H2-skeleton Jaccard vs. nearest other article
    "template_minor": 0.42,
    "h2_open_major": 0.50,        # share of H2 sections opening with "<X> la ..."
    "h2_open_minor": 0.34,
    "para_shape_major": 0.46,     # stdev of sentences-per-paragraph; lower = same shape
    "para_shape_minor": 0.55,
    "inline_header_major": 3,     # "**Tu:** Tu do giup..." pseudo-headings
    "inline_header_minor": 1,
    "thin_table_minor": 0,        # tables with <=2 data rows (rule `bang_thua`)
}

SEVERITY_PENALTY = {"CRITICAL": 25, "MAJOR": 10, "MINOR": 3}
# A single MAJOR is a warning, not a block: 13 independent rules at ~p90 each would fail
# ~40% of the corpus. The gate trips at 2+ MAJOR (or 1 MAJOR plus several MINOR).
PASS_SCORE = 80

# --------------------- Lexical resources ---------------------
HEDGE = ["nên", "cần", "có lẽ", "có thể nói", "phần nào", "thường thì", "tùy trường hợp",
         "khá là", "tương đối", "nhìn chung"]

SYNONYM_GROUPS = {
    "broker": ["công ty chứng khoán", "ctck", "nhà môi giới", "công ty môi giới",
               "đơn vị môi giới", "tổ chức môi giới"],
    "investor": ["nhà đầu tư", "trader", "người đầu tư", "nhà giao dịch", "người chơi",
                 "giới đầu tư"],
    "stock": ["cổ phiếu", "mã chứng khoán", "mã cp", "chứng khoán vốn"],
    "market": ["thị trường chứng khoán", "ttck", "sàn chứng khoán", "thị trường vốn",
               "thị trường cổ phiếu"],
}

TICKER_STOP = {"VND", "USD", "CEO", "CFO", "GDP", "CPI", "IPO", "NAV", "ROE", "ROA",
               "EPS", "ETF", "FDI", "VAT", "ATO", "ATC", "LTD", "JSC", "FAQ", "SEO", "CTA",
               "API", "PDF", "KPI", "MMO", "TNC", "VIP", "AND", "THE", "FOR", "MUA", "BAN"}

RE_TICKER = re.compile(r"\b[A-Z]{3}\b")
RE_EXCHANGE = re.compile(r"\b(HOSE|HNX|UPCoM|UPCOM|VN-?Index|HNX-?Index|VN30|VN100)\b", re.I)
RE_ORG = re.compile(r"(VSD|UBCKNN|SSC|Ngân hàng Nhà nước|Bộ Tài chính|Sở Giao dịch|"
                    r"vanban\.chinhphu\.vn|vbpl\.vn|Thông tư|Nghị định|Luật Chứng khoán)", re.I)
RE_NUMBER = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|tỷ|triệu|nghìn|đồng|vnđ|vnd|điểm|lần|phiên|vòng|"
                       r"ngày|tuần|tháng|quý|năm|phút|giờ|cổ phiếu|đơn vị|kỳ)", re.I)
# Financial ratios are written without a unit (Cash Ratio 0.2, P/E 9, vòng quay 6), so a bare
# decimal or a number right after a ratio name also counts as a verifiable anchor.
RE_RATIO = re.compile(r"\d+[.,]\d+|(?:P/E|P/B|ROE|ROA|EPS|RSI|MACD|R:R|D/E)\s*[<>=]?\s*\d*", re.I)
RE_TPLUS = re.compile(r"\bT\s*\+\s*\d\b")
RE_DATE = re.compile(r"(tháng\s*\d{1,2}/20\d{2}|quý\s*[1-4]/20\d{2}|năm\s*20\d{2}|\b\d{1,2}/20\d{2}\b)", re.I)
RE_PRICE_BAND = re.compile(r"[±+]\s*\d+(?:[.,]\d+)?\s*%")
RE_PROPER = re.compile(r"\b[A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][\wÀ-ỹ]{2,}")
RE_INLINE_HEADER = re.compile(r"^\s*\*\*[^*\n]{2,40}\*\*\s*[:：]|^\s*\*\*[^*\n]{2,40}[:：]\s*\*\*")

# High-precision vagueness patterns. Implements the declared-but-never-coded rules
# `số_mơ_hồ` and `generic_source` from anti-ai-rules.md §0, plus the filler phrases that
# survive a clean lexicon check. Each hit is a sentence that asserts without committing.
VAGUE_PATTERNS = [
    (r"(các|nhiều|một số|giới)\s+(chuyên gia|nhà phân tích|người)\s+(cho rằng|tin rằng|nhận định|đánh giá|khuyên)", "nguồn chung chung"),
    (r"\b(một khoản|một mức|một con số|một tỷ lệ|một lượng)\s+\w*\s*(nhỏ|lớn|đáng kể|khiêm tốn|cao|thấp)", "số mơ hồ"),
    (r"\b(một|các)\s+(doanh nghiệp|công ty|cổ phiếu|mã)\s+(lớn|nhỏ|tốt|uy tín|tiềm năng|chất lượng)\b", "định tính không tiêu chí"),
    (r"\bđóng vai trò (quan trọng|then chốt|thiết yếu)", "sáo rỗng"),
    (r"\b(rất|vô cùng|cực kỳ|hết sức) (quan trọng|cần thiết|hữu ích|quan trọng)", "cường điệu rỗng"),
    (r"\bkhông thể thiếu\b", "sáo rỗng"),
    (r"\bngày càng (trở nên|được|phổ biến|quan trọng)", "xu hướng không dẫn chứng"),
    (r"\btùy thuộc vào (nhiều|các) yếu tố\b", "né trả lời"),
    (r"\b(một cách|theo cách) (hiệu quả|tối ưu|khoa học|hợp lý|thông minh)\b", "trạng từ rỗng"),
    (r"\b(cải thiện|tối ưu hóa|nâng cao) (đáng kể|hiệu quả|rõ rệt)\b", "kết quả không số"),
    (r"\bphù hợp với (nhu cầu|mục tiêu|khẩu vị) (của bạn|riêng|cá nhân)\b", "né khuyến nghị"),
    (r"\b(luôn|bao giờ cũng) (tiềm ẩn|có) rủi ro\b", "truism rủi ro"),
    (r"\b(khá nhiều|không ít|rất nhiều) (nhà đầu tư|người|trường hợp)\b", "lượng mơ hồ"),
    (r"\bthị trường luôn (biến động|thay đổi)\b", "truism thị trường"),
    (r"\bkiên nhẫn và (kỷ luật|bản lĩnh)\b.*\b(là chìa khóa|quyết định|quan trọng)", "lời khuyên rỗng"),
]
VAGUE_RE = [(re.compile(p, re.I), label) for p, label in VAGUE_PATTERNS]

SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+(?=[^\s])")


def strip_md(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"`[^`]*`", "", s)
    return re.sub(r"[*_]", "", s).strip()


def split_sentences(text: str) -> list[str]:
    t = re.sub(r"(\d)[.,](\d)", r"\1<d>\2", text)
    t = re.sub(r"\b(TP|Tp|TS|ThS|PGS|GS|Q|P|vs|VD|Ví dụ)\.", r"\1<a>", t)
    return [p.replace("<d>", ",").replace("<a>", ".").strip()
            for p in SENT_SPLIT.split(t) if p.strip()]


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


# --------------------- Parsing ---------------------
class Doc:
    """Body of one article, split into prose paragraphs / sentences / H2 sections."""

    def __init__(self, path: Path):
        text, _ = read_text(path)
        self.path = path
        self.slug = slug_from_path(path)
        fm, start, lines = split_frontmatter(text)
        self.fm = fm
        end = body_end(lines, start)

        self.paragraphs: list[list[str]] = []          # prose paragraphs -> sentences
        self.sentences: list[tuple[int, str]] = []     # (line_no, sentence), prose only
        self.h2s: list[str] = []
        self.h2_first_sentence: list[str] = []
        self.inline_headers: list[int] = []
        self.thin_tables = 0
        self.all_text_words = 0
        self.body_lines: list[str] = []

        in_fence = False
        cur: list[str] = []
        pending_h2 = False
        table_rows: list[str] = []

        def flush_para():
            nonlocal cur
            if cur:
                self.paragraphs.append(cur)
                cur = []

        def flush_table():
            nonlocal table_rows
            if table_rows:
                cols = max(r.strip().strip("|").count("|") + 1 for r in table_rows)
                data = [r for r in table_rows if not re.match(r"^\s*\|[\s:|-]+\|\s*$", r)]
                rows_n = max(0, len(data) - 1)         # minus header row
                if rows_n <= 2 or (cols <= 2 and rows_n < 4):   # rule `bang_thua`
                    self.thin_tables += 1
                table_rows = []

        for i in range(start, end):
            raw = lines[i]
            s = raw.strip()
            if s.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            kind = classify(raw)
            if kind != "table":
                flush_table()
            if kind in ("blank", "hr", "image", "html", "fence"):
                flush_para()
                continue
            if kind == "heading":
                flush_para()
                if re.match(r"^##\s+[^#]", s):
                    self.h2s.append(strip_md(re.sub(r"^#+\s*", "", s)))
                    pending_h2 = True
                continue
            if kind == "table":
                table_rows.append(raw)
                continue

            clean = strip_md(raw)
            if not clean:
                continue
            self.body_lines.append(clean)
            self.all_text_words += len(clean.split())

            if kind == "quote":
                flush_para()
                continue
            if RE_INLINE_HEADER.match(raw):
                self.inline_headers.append(i + 1)
            if kind == "list":
                flush_para()
                continue                               # list items have their own rhythm

            sents = split_sentences(clean)
            if pending_h2 and sents:
                self.h2_first_sentence.append(sents[0])
                pending_h2 = False
            cur.extend(sents)
            for sn in sents:
                self.sentences.append((i + 1, sn))
        flush_para()
        flush_table()

        self.prose_text = " ".join(self.body_lines)
        self.prose_low = self.prose_text.lower()
        self.words = self.prose_text.split()

    def h2_tokens(self) -> set[str]:
        stop = {"la", "gi", "cac", "va", "cho", "nhu", "the", "nao", "cua", "trong", "mot",
                "khi", "de", "voi", "tai", "nhung", "co", "ban", "ve", "dsc", "ket", "luan"}
        toks = set()
        for h in self.h2s:
            for w in re.findall(r"[a-z0-9]+", unaccent(h)):
                if len(w) > 2 and w not in stop:
                    toks.add(w)
        return toks


# --------------------- Metrics ---------------------
def evidence_hits(text: str) -> int:
    n = len(RE_NUMBER.findall(text))
    n += len(RE_EXCHANGE.findall(text))
    n += len(RE_ORG.findall(text))
    n += len(RE_TPLUS.findall(text))
    n += len(RE_DATE.findall(text))
    n += len(RE_PRICE_BAND.findall(text))
    n += len(RE_RATIO.findall(text))
    n += len([t for t in RE_TICKER.findall(text) if t not in TICKER_STOP])
    return n


def is_unanchored(sent: str) -> bool:
    """No verifiable anchor: no number, no named entity, no legal/market reference.
    A proxy, not a semantic judgement - a conceptual sentence can be legitimately
    unanchored, which is why the rule only ever fires at corpus-tail density."""
    if len(sent.split()) < 8:
        return False
    if evidence_hits(sent):
        return False
    return not RE_PROPER.search(sent[1:])              # skip sentence-initial capital


#) Labels that stay a hit even in a data-rich sentence - these are pure filler.
STRONG_VAGUE = {"sáo rỗng", "cường điệu rỗng", "nguồn chung chung", "truism rủi ro",
                "truism thị trường", "né trả lời", "lời khuyên rỗng"}


def vague_hits(sentences: list[tuple[int, str]]) -> list[tuple[int, str, str]]:
    """Return [(line, label, sentence)] for sentences matching a vagueness pattern.
    A weak pattern is forgiven when the same sentence already carries >=2 anchors
    ("lọc cổ phiếu tiềm năng dựa trên P/E < 15" is specific despite the phrase)."""
    out = []
    for ln, s in sentences:
        for rx, label in VAGUE_RE:
            if rx.search(s):
                if label not in STRONG_VAGUE and evidence_hits(s) >= 2:
                    break
                out.append((ln, label, s))
                break
    return out


def ttr_windows(words: list[str], win: int = 300) -> list[float]:
    out = []
    step = max(1, win // 2)
    for i in range(0, max(1, len(words) - win + 1), step):
        chunk = [unaccent(w).strip(".,;:!?()\"'") for w in words[i:i + win]]
        chunk = [c for c in chunk if c]
        if len(chunk) >= win // 2:
            out.append(len(set(chunk)) / len(chunk))
    return out


def measure(doc: Doc) -> dict:
    lens = [len(s.split()) for _, s in doc.sentences]
    m: dict = {}
    m["words"] = doc.all_text_words
    m["n_sent"] = len(lens)
    m["n_h2"] = len(doc.h2s)

    m["burstiness"] = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    m["mean_sent"] = statistics.mean(lens) if lens else 0.0

    run = best = 0
    run_at = best_at = 0
    for i, L in enumerate(lens):
        if 14 <= L <= 24:
            if run == 0:
                run_at = doc.sentences[i][0]
            run += 1
        else:
            run = 0
        if run > best:
            best, best_at = run, run_at
    m["uniform_run"] = best
    m["_uniform_line"] = best_at

    gap = worst = 0
    gap_at = worst_at = 0
    for i, L in enumerate(lens):
        if L <= 7:
            gap = 0
        else:
            if gap == 0:
                gap_at = doc.sentences[i][0]
            gap += 1
        if gap > worst:
            worst, worst_at = gap, gap_at
    m["rhythm_gap"] = worst
    m["_rhythm_line"] = worst_at
    m["short_share"] = (sum(1 for L in lens if L <= 7) / len(lens)) if lens else 0.0

    m["evidence_per_100w"] = (evidence_hits(doc.prose_text) / doc.all_text_words * 100) if doc.all_text_words else 0.0

    unanchored = [(ln, s) for ln, s in doc.sentences if is_unanchored(s)]
    m["unanchored_ratio"] = len(unanchored) / len(doc.sentences) if doc.sentences else 0.0
    m["_unanchored"] = unanchored[:5]

    vg = vague_hits(doc.sentences)
    m["vague_per_1000w"] = (len(vg) / doc.all_text_words * 1000) if doc.all_text_words else 0.0
    m["vague_n"] = len(vg)
    m["_vague"] = vg[:6]

    hedge_max = 0
    for p in doc.paragraphs:
        txt = " ".join(p).lower()
        c = sum(len(re.findall(r"(?<!\w)" + re.escape(h) + r"(?!\w)", txt)) for h in HEDGE)
        hedge_max = max(hedge_max, c)
    m["hedge_para_max"] = hedge_max

    syn_worst, syn_group, syn_used = 0, "", []
    for g, variants in SYNONYM_GROUPS.items():
        used = [v for v in variants if re.search(r"(?<!\w)" + re.escape(v) + r"(?!\w)", doc.prose_low)]
        if len(used) > syn_worst:
            syn_worst, syn_group, syn_used = len(used), g, used
    m["synonym_variants"] = syn_worst
    m["_synonym"] = (syn_group, syn_used)

    defs = sum(1 for s in doc.h2_first_sentence
               if re.match(r"^\s*(\S+\s+){0,6}(là|chính là|được hiểu là)\b", s, re.I))
    m["h2_def_open"] = defs / len(doc.h2_first_sentence) if doc.h2_first_sentence else 0.0

    shapes = [len(p) for p in doc.paragraphs]
    m["para_shape_sd"] = statistics.pstdev(shapes) if len(shapes) > 1 else 0.0
    m["n_para"] = len(shapes)

    tw = ttr_windows(doc.words)
    m["ttr_min"] = min(tw) if tw else 0.0
    m["ttr_max"] = max(tw) if tw else 0.0

    m["inline_headers"] = len(doc.inline_headers)
    m["thin_tables"] = doc.thin_tables
    return m


def same_series(a: str, b: str) -> bool:
    """Two slugs belong to one deliberate series (e.g. cach-mua-co-phieu-<ticker>),
    where a shared H2 skeleton is the format, not laziness."""
    ta, tb = a.split("-"), b.split("-")
    return len(ta) > 3 and len(tb) > 3 and ta[:-1] == tb[:-1]


def template_similarity(target: Doc, corpus: list[tuple[str, set[str]]]) -> tuple[float, str]:
    a = target.h2_tokens()
    if len(a) < 3:
        return 0.0, ""
    best, who = 0.0, ""
    for slug, b in corpus:
        if slug == target.slug or len(b) < 3 or same_series(slug, target.slug):
            continue
        j = len(a & b) / len(a | b)
        if j > best:
            best, who = j, slug
    return best, who


# --------------------- Findings ---------------------
def judge(m: dict, tmpl: tuple[float, str]) -> list[tuple[str, str, str]]:
    """Return [(rule_id, severity, message)]."""
    f: list[tuple[str, str, str]] = []

    def cmp_low(key, mj, mi, cid, fmt):      # lower value = worse
        v = m[key]
        if v < T[mj]:
            f.append((cid, "MAJOR", fmt.format(v=v, t=T[mj])))
        elif v < T[mi]:
            f.append((cid, "MINOR", fmt.format(v=v, t=T[mi])))

    def cmp_high(key, mj, mi, cid, fmt):     # higher value = worse
        v = m[key]
        if v > T[mj]:
            f.append((cid, "MAJOR", fmt.format(v=v, t=T[mj])))
        elif v > T[mi]:
            f.append((cid, "MINOR", fmt.format(v=v, t=T[mi])))

    cmp_low("burstiness", "burstiness_major", "burstiness_minor", "SLOP-burstiness",
            "Nhịp câu phẳng: stdev độ dài câu {v:.1f} từ (chuẩn >= {t}) - thêm câu ngắn 3-7 từ và câu dài 30+ từ")
    cmp_high("uniform_run", "uniform_run_major", "uniform_run_minor", "SLOP-uniform-run",
             "{v:.0f} câu liên tiếp cùng khoảng 14-24 từ (tối đa {t}) - cắt/gộp câu để đổi nhịp, từ dòng "
             + str(m.get("_uniform_line", 0)))
    cmp_high("rhythm_gap", "rhythm_gap_major", "rhythm_gap_minor", "SLOP-rhythm",
             "{v:.0f} câu liên tiếp không có câu nào <=7 từ (tối đa {t}) - vi phạm REQUIRED rhythm_break, từ dòng "
             + str(m.get("_rhythm_line", 0)))
    cmp_low("evidence_per_100w", "evidence_major", "evidence_minor", "SLOP-evidence",
            "Mật độ bằng chứng {v:.1f}/100 từ (chuẩn >= {t}) - thêm mã CP, %, sàn, mốc Tháng M/YYYY")
    cmp_high("unanchored_ratio", "unanchored_major", "unanchored_minor", "SLOP-anchor",
             "{v:.0%} câu không có mỏ neo kiểm chứng được (số / thực thể / sàn / mốc thời gian) - tối đa {t:.0%}")
    cmp_high("vague_per_1000w", "vague_major", "vague_minor", "SLOP-vague",
             "{v:.1f} câu sáo rỗng / 1000 từ (tối đa {t}) - xem danh sách bằng -v, thay bằng số hoặc tiêu chí")
    cmp_high("hedge_para_max", "hedge_para_major", "hedge_para_minor", "SLOP-hedge-para",
             "1 đoạn chứa {v:.0f} hedge word (tối đa {t}) - viết khẳng định, nêu điều kiện cụ thể")
    cmp_high("synonym_variants", "synonym_major", "synonym_minor", "SLOP-synonym",
             "{v:.0f} biến thể đồng nghĩa cho cùng một đối tượng (tối đa {t}) - chốt 1 từ chuẩn")
    cmp_high("h2_def_open", "h2_open_major", "h2_open_minor", "SLOP-h2-open",
             "{v:.0%} H2 mở bằng câu định nghĩa \"X là...\" (tối đa {t:.0%}) - đổi kiểu mở: số liệu, kịch bản, câu lệnh")
    cmp_low("para_shape_sd", "para_shape_major", "para_shape_minor", "SLOP-para-shape",
            "Mọi đoạn cùng hình dạng: stdev số câu/đoạn {v:.2f} (chuẩn >= {t})")
    cmp_high("inline_headers", "inline_header_major", "inline_header_minor", "SLOP-inline-header",
             "{v:.0f} pseudo-heading `**Từ:**` (tối đa {t}) - viết thành đoạn văn hoặc dùng H4")
    if m["thin_tables"] > T["thin_table_minor"]:
        f.append(("SLOP-table-thin", "MINOR",
                  f"{m['thin_tables']:.0f} bảng mỏng (<3 cột & <4 dòng) - dùng bullet list"))

    sim, who = tmpl
    if sim > T["template_major"]:
        f.append(("SLOP-template", "MAJOR",
                  f"Khung H2 trùng {sim:.0%} với bài `{who}` - bài đang là template cũ đổi chủ đề"))
    elif sim > T["template_minor"]:
        f.append(("SLOP-template", "MINOR", f"Khung H2 trùng {sim:.0%} với bài `{who}`"))
    return f


def slop_score(findings) -> int:
    return max(0, 100 - sum(SEVERITY_PENALTY[s] for _, s, _ in findings))


# --------------------- Corpus index ---------------------
def build_corpus(files: list[Path]) -> tuple[list[Doc], list[tuple[str, set[str]]]]:
    docs, idx = [], []
    for p in files:
        try:
            d = Doc(p)
        except Exception as e:                         # noqa: BLE001 - keep scanning
            print(f"  ! skip {p.name}: {e}", file=sys.stderr)
            continue
        docs.append(d)
        idx.append((d.slug, d.h2_tokens()))
    return docs, idx


def pct(vals, q):
    if not vals:
        return 0.0
    s = sorted(vals)
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


BASELINE_KEYS = [
    ("burstiness", "{:.1f}", "low"), ("mean_sent", "{:.1f}", "-"),
    ("uniform_run", "{:.0f}", "high"), ("rhythm_gap", "{:.0f}", "high"),
    ("short_share", "{:.2f}", "low"), ("evidence_per_100w", "{:.2f}", "low"),
    ("unanchored_ratio", "{:.2f}", "high"), ("vague_per_1000w", "{:.2f}", "high"),
    ("hedge_para_max", "{:.0f}", "high"),
    ("synonym_variants", "{:.0f}", "high"), ("h2_def_open", "{:.2f}", "high"),
    ("para_shape_sd", "{:.2f}", "low"), ("ttr_min", "{:.2f}", "-"),
    ("inline_headers", "{:.0f}", "high"), ("thin_tables", "{:.0f}", "high"),
    ("template_sim", "{:.2f}", "high"), ("words", "{:.0f}", "-"),
]


def run_baseline(files: list[Path], csv_out: Path | None, top: int) -> int:
    print(f"Scanning {len(files)} file...", file=sys.stderr)
    docs, idx = build_corpus(files)
    rows = []
    for d in docs:
        m = measure(d)
        sim, who = template_similarity(d, idx)
        m["template_sim"] = sim
        m["_twin"] = who
        fs = judge(m, (sim, who))
        rows.append((d.slug, m, fs, slop_score(fs)))

    print(f"\n{'metric':<20} {'bad-dir':<8} {'p10':>8} {'p25':>8} {'p50':>8} {'p75':>8} {'p90':>8} {'min':>8} {'max':>8}")
    print("-" * 94)
    for key, fmt, direction in BASELINE_KEYS:
        v = [r[1][key] for r in rows]
        cells = [pct(v, q) for q in (0.10, 0.25, 0.50, 0.75, 0.90)] + [min(v), max(v)]
        print(f"{key:<20} {direction:<8} " + " ".join(f"{fmt.format(c):>8}" for c in cells))

    sev_count: dict[str, list[int]] = {}
    for _, _, fs, _ in rows:
        for cid, sev, _msg in fs:
            sev_count.setdefault(cid, [0, 0])
            sev_count[cid][0 if sev == "MAJOR" else 1] += 1
    print(f"\n{'rule':<22} {'MAJOR':>7} {'MINOR':>7}  {'% bai bi flag':>14}")
    print("-" * 56)
    for cid, (mj, mi) in sorted(sev_count.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        print(f"{cid:<22} {mj:>7} {mi:>7}  {(mj + mi) / len(rows):>13.0%}")

    scores = [r[3] for r in rows]
    fails = [r for r in rows if r[3] < PASS_SCORE]
    print(f"\nSlop score: p10={pct(scores, 0.1):.0f} p50={pct(scores, 0.5):.0f} p90={pct(scores, 0.9):.0f}"
          f" | FAIL (score < {PASS_SCORE}): {len(fails)}/{len(rows)} = {len(fails) / len(rows):.0%}")

    print(f"\n-- {top} bai te nhat --")
    for slug, m, fs, sc in sorted(rows, key=lambda r: r[3])[:top]:
        ids = ", ".join(c.replace("SLOP-", "") for c, s, _ in fs if s == "MAJOR") or "-"
        print(f"{sc:>4}  {slug[:56]:<56} {ids}")

    if csv_out:
        keys = [k for k, _, _ in BASELINE_KEYS]
        with csv_out.open("w", encoding="utf-8", newline="") as fh:
            fh.write("slug,slop_score,n_major,n_minor," + ",".join(keys) + ",twin\n")
            for slug, m, fs, sc in sorted(rows, key=lambda r: r[3]):
                mj = sum(1 for _, s, _ in fs if s == "MAJOR")
                mi = sum(1 for _, s, _ in fs if s == "MINOR")
                fh.write(f"{slug},{sc},{mj},{mi}," +
                         ",".join(f"{m[k]:.4f}" for k in keys) + f",{m.get('_twin', '')}\n")
        print(f"\n-> CSV: {csv_out}")
    return 0


# --------------------- Single file ---------------------
def run_one(path: Path, as_json: bool, verbose: bool) -> int:
    doc = Doc(path)
    m = measure(doc)
    _, idx = build_corpus(sorted(FINAL_DIR.glob("Final-*.md")))
    sim, who = template_similarity(doc, idx)
    m["template_sim"] = sim
    fs = judge(m, (sim, who))
    score = slop_score(fs)
    ok = score >= PASS_SCORE

    if as_json:
        print(json.dumps({"file": str(path), "pass": ok, "slop_score": score,
                          "metrics": {k: v for k, v in m.items() if not k.startswith("_")},
                          "twin": who,
                          "findings": [{"check": c, "severity": s, "message": g} for c, s, g in fs]},
                         ensure_ascii=False, indent=2))
        return 0 if ok else 1

    print(f"\nSLOP CHECK - {path.name}")
    print(f"{'PASS' if ok else 'FAIL'}  ·  Slop score {score}/100  ·  {m['words']:.0f} từ, "
          f"{m['n_sent']:.0f} câu, {m['n_h2']:.0f} H2")
    print("-" * 78)
    if not fs:
        print("Không phát hiện dấu hiệu slop thống kê.")
    for cid, sev, msg in sorted(fs, key=lambda x: {"MAJOR": 0, "MINOR": 1}[x[1]]):
        print(f"[{sev:<5}] {cid:<20} {msg}")
    if verbose:
        print("\n-- Metrics --")
        for k, fmt, _ in BASELINE_KEYS:
            print(f"  {k:<20} {fmt.format(m[k])}")
        g, used = m["_synonym"]
        if used:
            print(f"  synonym group '{g}': {', '.join(used)}")
        if m["_vague"]:
            print("\n-- Câu sáo rỗng --")
            for ln, label, s in m["_vague"]:
                print(f"  L{ln} [{label}]: {s[:100]}")
        if m["_unanchored"]:
            print("\n-- Câu không có mỏ neo (mẫu) --")
            for ln, s in m["_unanchored"]:
                print(f"  L{ln}: {s[:100]}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--glob", default="3-finalized", help="thu muc con trong knowledge/4-content")
    ap.add_argument("--csv")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--thresholds", action="store_true")
    args = ap.parse_args()

    if args.thresholds:
        for k, v in T.items():
            print(f"{k:<24} {v}")
        return 0
    if args.baseline:
        base = FINAL_DIR if args.glob == "3-finalized" else FINAL_DIR.parent / args.glob
        files = sorted(base.glob("*.md"))
        if not files:
            print(f"Khong co file .md trong {base}", file=sys.stderr)
            return 2
        return run_baseline(files, Path(args.csv) if args.csv else None, args.top)
    if not args.file:
        ap.error("can <file.md> hoac --baseline")
    p = Path(args.file)
    if not p.exists():
        print(f"Khong tim thay {p}", file=sys.stderr)
        return 2
    return run_one(p, args.json, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
