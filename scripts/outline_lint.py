#!/usr/bin/env python3
"""Lint an SEO outline BEFORE it is shown to the user (Gate cuối của /outlining).

Usage:
    python scripts/outline_lint.py knowledge/4-content/1-outlines/<slug>.md [--json]

Checks (deterministic, offline):
    FMT-*      Content_Type must match the format that wins the SERP (re-computed from the SERP cache
               knowledge/raw/serp/<keyword>.json via serp_research.serp_format_summary — not trusted from YAML)
    LIST-*     Toplist: Title/H1 carry the number N, outline has >= median list items of competitors
    YAML-*     required fields, enums, Thesis, SERP_Status, internal-link count
    WC-sum     sum of section Target/Max vs Word_Count_Target
    META-*     Title <= 59 chars, Meta 140-160 chars, Sapo mentions DSC
    H2-*       keyword in an H2, Kết luận H2, Product Bridge H2, FAQ H2, per-H2 reader question + takeaway
    DATA-*     [CẦN XÁC NHẬN] left in the outline, no current-year data, template placeholders left,
               data rows without a source URL
    SERP-*     degraded SERP not declared, competitor blocks missing, inferred PAA not marked,
               PAA labelled as Google's but absent from the SERP cache
    ENT-*      terms used by >= 3 ranking pages (serp_research.topic_coverage) must be in the outline
    IG-*       Information_Gain is a list of claims, each with the H2 that delivers it and a checkable proof
Exit 1 when any CRITICAL/MAJOR finding exists.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
SERP_DIR = ROOT / ".antigravity/skills/web-serp/scripts"
COUNT_WORDS_DIR = ROOT / ".antigravity/skills/qa-qc"

MAX_TITLE = 59
META_RANGE = (140, 160)
LINK_RANGE = (3, 6)  # /kien-thuc links; /mo-tai-khoan not counted
CONTENT_TYPES = {"Toplist", "How-to", "Definition", "Comparison", "Review", "Comprehensive Guide"}
SNIPPETS = {"Paragraph", "List", "Table", "None"}
INTENTS = {"Informational", "Commercial", "Transactional", "Navigational"}
FORMAT_TO_TYPE = {"toplist": "Toplist", "howto": "How-to", "definition": "Definition",
                  "comparison": "Comparison", "review": "Review", "news": "Comprehensive Guide",
                  "guide": "Comprehensive Guide"}
SPECIAL_H2 = re.compile(r"(faq|câu hỏi thường gặp|kết luận|dsc)", re.I)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower().replace("đ", "d"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


class Report:
    def __init__(self, path):
        self.path, self.items, self.stats = path, [], {}

    def add(self, sev, check, msg):
        self.items.append({"severity": sev, "check": check, "message": msg})

    def count(self, sev):
        return sum(1 for i in self.items if i["severity"] == sev)

    def passed(self):
        return not (self.count("CRITICAL") or self.count("MAJOR"))


# ---------------------------------------------------------------- parsing

def parse_yaml(text: str) -> tuple[dict, str, str]:
    """Minimal YAML reader: top-level scalars + one level of nested `key: value`. Returns (fm, yaml, body)."""
    m = re.match(r"^\ufeff?---\n([\s\S]*?)\n---\n", text)
    if not m:  # old template: YAML fenced in ```yaml after the title
        m = re.search(r"^```ya?ml\n---\n([\s\S]*?)\n---\n```\n?", text, re.M)
    if not m:
        return {}, "", text
    if m.start() > 0:
        return _read_yaml(m.group(1)), m.group(1), text[:m.start()] + text[m.end():]
    return _read_yaml(m.group(1)), m.group(1), text[m.end():]


def _read_yaml(raw: str) -> dict:
    fm, parent = {}, None
    for line in raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
        if top:
            key, val = top.group(1), top.group(2).split(" #")[0].strip().strip('"\'')
            fm[key] = val
            parent = key if not val else None
            if parent:
                fm[key] = {}
            continue
        sub = re.match(r"^\s+([A-Za-z_]+)\s*:\s*(.*)$", line)
        if parent and isinstance(fm.get(parent), dict) and sub:
            fm[parent][sub.group(1)] = sub.group(2).split(" #")[0].strip().strip('"\'')
    return fm


def field_line(body: str, label: str) -> str:
    m = re.search(r"^\s*[-*]?\s*\*\*%s:\*\*\s*(.+)$" % re.escape(label), body, re.M | re.I)
    if not m:
        return ""
    return re.sub(r"\s*\((?:~?\d+\s*ký tự|~?\d+\s*chars?)\)\s*$", "", m.group(1)).strip()


def headings(body: str) -> list[tuple[str, str, str]]:
    """[(level, title, block_text)] for `### H2:` / `#### H3:` outline headings."""
    out, cur, buf = [], None, []
    for line in body.split("\n"):
        m = re.match(r"^#{2,5}\s+(H[1-4]):\s*(.+)", line)
        if m or re.match(r"^#{1,2}\s+\S", line):
            if cur:
                out.append((cur[0], cur[1], "\n".join(buf)))
            cur, buf = ((m.group(1), m.group(2).strip()) if m else None), []
            continue
        if cur:
            buf.append(line)
    if cur:
        out.append((cur[0], cur[1], "\n".join(buf)))
    return out


def word_range(val: str) -> tuple[int, int] | None:
    nums = [int(n.replace(".", "").replace(",", "")) for n in re.findall(r"\d[\d.,]*", val or "")]
    nums = [n for n in nums if n >= 300]
    if not nums:
        return None
    return (min(nums), max(nums))


def serp_data(keyword: str):
    """(serp_research module, cached SERP dict) or (None, None) when there is no cache."""
    sys.path.insert(0, str(SERP_DIR))
    try:
        import serp_research as sr  # type: ignore
    except Exception:
        return None, None
    path = Path(sr.cache_path(keyword))
    if not path.exists():
        return sr, None
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data.setdefault("keyword", keyword)
    return sr, data


def serp_summary(keyword: str):
    sr, data = serp_data(keyword)
    return sr.serp_format_summary(data) if data else None


def yaml_list(val) -> list[str]:
    """Inline YAML list `[a, b, c]` (or a comma string) -> items."""
    if not isinstance(val, str):
        return []
    return [x.strip().strip('"\'') for x in val.strip().strip("[]").split(",") if x.strip().strip('"\'')]


def parse_information_gain(yaml_raw: str) -> list[dict]:
    """Information_Gain block: `- claim:` items with h2 / type / proof."""
    block = re.search(r"^Information_Gain:[ \t]*\n([\s\S]*?)(?=^[A-Za-z_#]|\Z)", yaml_raw, re.M)
    if not block:
        return []
    items = []
    for chunk in re.split(r"^\s*-\s*(?=claim\s*:)", block.group(1), flags=re.M)[1:]:
        it = {}
        for key in ("claim", "h2", "type", "proof"):
            m = re.search(r"^\s*%s\s*:\s*(.+)$" % key, chunk, re.M)
            it[key] = m.group(1).split(" #")[0].strip().strip('"\'') if m else ""
        items.append(it)
    return items


def must_terms(keyword: str) -> tuple[list[str], dict]:
    """Terms the ranking pages share (df >= 3) + the full coverage dict. Empty when no competitors cached."""
    sr, data = serp_data(keyword)
    if not data:
        return [], {}
    tc = sr.topic_coverage(data)
    return tc["must"], tc


def skipped_terms(fm: dict) -> set[str]:
    """Entities_Skipped: [term — lý do, ...] -> folded terms (text before the dash)."""
    return {fold(re.split(r"\s+[—–-]\s+", x)[0]) for x in yaml_list(fm.get("Entities_Skipped", ""))}


IG_TYPES = {"calc", "dsc-data", "regulation", "screenshot", "comparison"}
ENT_MIN_COVERAGE = 0.7


# ---------------------------------------------------------------- checks

def lint(path: Path) -> Report:
    rep = Report(str(path))
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    fm, yaml_raw, body = parse_yaml(text)
    if not fm:
        rep.add("CRITICAL", "YAML-missing", "Không có YAML frontmatter `---`")
        return rep

    kw = fm.get("Target_Keyword", "")
    ctype = fm.get("Content_Type", "")
    for key in ("Target_Keyword", "Search_Intent", "Content_Type", "Thesis", "Persona", "Writer_Profile",
                "Word_Count_Target", "Featured_Snippet", "SERP_Status"):
        v = fm.get(key)
        if not v or (isinstance(v, str) and v.startswith("[")):
            rep.add("MAJOR", "YAML-field", f"Thiếu / chưa điền `{key}`")
    if not yaml_list(fm.get("Entities", "")) or "..." in str(fm.get("Entities")):
        rep.add("MAJOR", "YAML-field", "Thiếu / chưa điền `Entities` — copy từ block Topic Coverage của serp_research.py")

    # --- information gain: each claim names where it lands and what proves it
    ig = parse_information_gain(yaml_raw)
    rep.stats["information_gain"] = len(ig)
    if not ig:
        rep.add("MAJOR", "IG-shape", "`Information_Gain` phải là danh sách ≥ 2 mục `- claim / h2 / type / proof` "
                                     "(xem brief-template) — 1 câu mô tả chung không kiểm được ở draft")
    else:
        if len(ig) < 2:
            rep.add("MAJOR", "IG-shape", "Information_Gain chỉ có 1 mục — cần ≥ 2 điều top 5 không có")
        for it in ig:
            lack = [k for k in ("claim", "h2", "proof") if not it[k] or it[k].startswith("[")]
            if lack:
                rep.add("MAJOR", "IG-shape", f"Mục Information_Gain thiếu {', '.join(lack)}: “{it['claim'][:60]}”")
            if it["type"] and it["type"] not in IG_TYPES:
                rep.add("MINOR", "IG-shape", f"Information_Gain type `{it['type']}` — chọn 1 trong {sorted(IG_TYPES)}")
    if ctype and ctype not in CONTENT_TYPES:
        rep.add("MAJOR", "YAML-enum", f"Content_Type `{ctype}` không thuộc {sorted(CONTENT_TYPES)}")
    if fm.get("Featured_Snippet") and fm["Featured_Snippet"] not in SNIPPETS:
        rep.add("MINOR", "YAML-enum", f"Featured_Snippet `{fm['Featured_Snippet']}` — chọn 1 trong {sorted(SNIPPETS)}")
    if fm.get("Search_Intent") and fm["Search_Intent"].split()[0] not in INTENTS:
        rep.add("MINOR", "YAML-enum", f"Search_Intent `{fm['Search_Intent']}` — chọn 1 trong {sorted(INTENTS)}")
    thesis = fm.get("Thesis", "")
    if isinstance(thesis, str) and thesis and len(thesis.split()) < 8:
        rep.add("MAJOR", "YAML-thesis", "Thesis quá ngắn — cần 1–2 câu lập trường cả bài, không phải chủ đề")

    # --- SERP format / intent (re-computed from cache, YAML is not trusted)
    s = serp_summary(kw) if kw else None
    yfmt = fm.get("SERP_Format") if isinstance(fm.get("SERP_Format"), dict) else {}
    sr, sdata = serp_data(kw) if kw else (None, None)
    if sdata and sr:
        # --- entity coverage: what >= 3 ranking pages all talk about must be planned in the outline
        tc = sr.topic_coverage(sdata)
        must, skipped, folded = tc["must"], skipped_terms(fm), fold(text)
        if must:
            missing = [t for t in must if fold(t) not in folded and fold(t) not in skipped]
            cov = 1 - len(missing) / len(must)
            rep.stats["entity_coverage"] = f"{round(cov * 100)}% ({len(must) - len(missing)}/{len(must)})"
            if cov < ENT_MIN_COVERAGE:
                rep.add("MAJOR", "ENT-outline",
                        f"Outline phủ {round(cov * 100)}% thuật ngữ mà ≥ 3 đối thủ đều dùng (cần ≥ {round(ENT_MIN_COVERAGE * 100)}%). "
                        f"Thiếu: {' · '.join(missing)}. Đưa vào H2/Entities, hoặc ghi `Entities_Skipped: [cụm — lý do]`")
        # --- information gain must not already be on a ranking page
        comp_text = fold(" ".join(c.get("content") or "" for c in sr.usable_competitors(sdata.get("competitors"))))
        for it in ig:
            if it["proof"] and len(fold(it["proof"])) >= 4 and fold(it["proof"]) in comp_text:
                rep.add("MINOR", "IG-not-new", f"Proof “{it['proof']}” đã có trong bài đối thủ — chưa phải thông tin mới")
        # --- PAA labelled as Google's must exist in the cache
        real = [fold(q["question"]) for q in sr.normalize_paa(sdata.get("people_also_ask"))]
        rep.stats["paa_in_cache"] = len(real)
    else:
        real = None
    if s is None:
        rep.add("MAJOR", "FMT-no-cache", "Không tìm thấy cache SERP cho keyword — chạy serp_research.py trước khi outline")
    else:
        want = FORMAT_TO_TYPE.get(s["dominant"], "Comprehensive Guide")
        rep.stats.update(serp_format=f"{s['dominant']} {s['share']}% {s['verdict']}", content_type=ctype)
        deviation = fm.get("Format_Deviation", "")
        if ctype and ctype != want and not deviation:
            sev = {"BẮT BUỘC": "CRITICAL", "NGHIÊNG VỀ": "MAJOR"}.get(s["verdict"], "MINOR")
            note = " (SERP degraded — tín hiệu yếu, hỏi user)" if s["degraded"] else ""
            rep.add(sev, "FMT-mismatch",
                    f"SERP {s['verdict']} khung `{s['dominant']}` ({s['share']}%) nhưng Content_Type = `{ctype}`{note}. "
                    f"Đổi sang `{want}` hoặc điền Format_Deviation (lý do) và báo user")
        if yfmt.get("dominant") and yfmt["dominant"] != s["dominant"]:
            rep.add("MINOR", "FMT-yaml", f"SERP_Format.dominant ghi `{yfmt['dominant']}`, cache tính ra `{s['dominant']}`")
        if s["degraded"] and fm.get("SERP_Status") != "degraded":
            rep.add("MAJOR", "SERP-degraded", f"SERP degraded ({s['degraded_reason']}) nhưng YAML không ghi `SERP_Status: degraded`")
        if not s["degraded"] and len(re.findall(r"^#{3,4}\s+Competitor\s+\d", body, re.M)) < 3:
            rep.add("MAJOR", "SERP-competitors", "Outline thiếu block `### Competitor N` (≥3) — mất cấu trúc heading đối thủ")
        elif not s["degraded"] and not re.search(r"\d+\s*/\s*40", body):
            rep.add("MINOR", "SERP-score", "Block Competitor chưa có điểm /40 (Độ sâu · Trình bày · SEO · UX)")
        if ctype == "Toplist" and s.get("list_count_median"):
            items = sum(1 for lvl, _, _ in headings(body) if lvl == "H3")
            rep.stats["list_items"] = items
            if items < s["list_count_median"]:
                rep.add("MAJOR", "LIST-count", f"Toplist có {items} mục H3, đối thủ median {s['list_count_median']} mục")

    # --- PAA
    paa_block = re.search(r"^PAA_Questions:[\s\S]*?(?=^[A-Za-z_]+:|\Z)", yaml_raw, re.M)
    if paa_block:
        entries = re.split(r"^\s*-\s*q\s*:", paa_block.group(0), flags=re.M)[1:]
        rep.stats["paa"] = len(entries)
        for e in entries:
            q = e.split("\n")[0].strip().strip('"\'')
            if "source: inferred" not in e and not re.search(r"google_source\s*:\s*\S*\.\w", e):
                rep.add("MINOR", "SERP-paa-source", f"PAA không có nguồn Google, cần ghi `source: inferred`: “{q}”")
            elif "source: inferred" not in e and real is not None:
                qw = set(fold(q).split())
                hit = any(qw and len(qw & set(r.split())) / len(qw | set(r.split())) >= 0.8 for r in real)
                if not hit:
                    rep.add("MAJOR", "SERP-paa-fake",
                            f"PAA ghi nguồn Google nhưng không có trong cache SERP ({len(real)} câu): “{q}” — "
                            "copy nguyên văn từ serp_research.py, hoặc đổi thành `source: inferred`")

    # --- links
    links = re.findall(r"^\s*-\s*anchor\s*:.*\n\s*url\s*:\s*(\S+)", yaml_raw, re.M)
    kt = [u for u in links if "/kien-thuc/" in u]
    rep.stats["internal_links"] = len(kt)
    if len(kt) < LINK_RANGE[0]:
        rep.add("MAJOR", "YAML-links", f"{len(kt)} link /kien-thuc/ — cần ≥ {LINK_RANGE[0]} (qa_lint draft đòi ≥ 3)")
    elif len(kt) > LINK_RANGE[1]:
        rep.add("MINOR", "YAML-links", f"{len(kt)} link /kien-thuc/ — quá {LINK_RANGE[1]}, chọn link gắn với ý của H2")

    # --- title / meta / sapo
    title, meta, sapo = field_line(body, "Title"), field_line(body, "Meta description"), field_line(body, "Sapo")
    h1 = field_line(body, "H1") or next((t for lvl, t, _ in headings(body) if lvl == "H1"), "")
    if not title:
        rep.add("MAJOR", "META-title", "Thiếu Title")
    elif len(title) > MAX_TITLE:
        rep.add("MAJOR", "META-title", f"Title {len(title)} ký tự (> {MAX_TITLE})")
    if title and kw and fold(kw) not in fold(title):
        rep.add("MAJOR", "META-title-kw", "Title không chứa nguyên keyword")
    if not meta:
        rep.add("MAJOR", "META-desc", "Thiếu Meta description")
    elif not META_RANGE[0] <= len(meta) <= META_RANGE[1]:
        rep.add("MINOR", "META-desc", f"Meta {len(meta)} ký tự (chuẩn {META_RANGE[0]}–{META_RANGE[1]})")
    if sapo and "dsc" not in sapo.lower():
        rep.add("MAJOR", "META-sapo-dsc", "Sapo không nhắc DSC + câu dẫn vào bài (yêu cầu user 2026-11-09)")
    if ctype == "Toplist":
        if title and not re.search(r"\d", title):
            rep.add("MAJOR", "LIST-title-n", "Toplist nhưng Title không có con số N")
        if h1 and not re.search(r"\d", h1):
            rep.add("MAJOR", "LIST-h1-n", "Toplist nhưng H1 không có con số N")

    # --- headings
    hs = headings(body)
    h2s = [(t, b) for lvl, t, b in hs if lvl == "H2"]
    if kw and not any(set(fold(kw).split()) <= set(fold(t).split()) for t, _ in h2s):
        rep.add("MAJOR", "H2-keyword", f"Không H2 nào chứa keyword “{kw}”")
    if not any("kết luận" in t.lower() for t, _ in h2s):
        rep.add("MAJOR", "H2-conclusion", "Thiếu H2 Kết luận (tóm tắt bài rồi CTA)")
    if not any("dsc" in t.lower() for t, _ in h2s):
        rep.add("MAJOR", "H2-bridge", "Thiếu H2 Product Bridge có DSC")
    if paa_block and "placement: faq" in paa_block.group(0) and not any(
            re.search(r"faq|câu hỏi thường gặp", t, re.I) for t, _ in h2s):
        rep.add("MAJOR", "H2-faq", "Có PAA placement: faq nhưng không có H2 FAQ")
    for t, b in h2s:
        if SPECIAL_H2.search(t):
            continue
        for label, check in (("Câu hỏi người đọc", "H2-reader-q"), ("Ý chính", "H2-takeaway")):
            if not re.search(r"\*\*%s" % label, b):
                rep.add("MAJOR", check, f"[{t}] thiếu `**{label}:**`")

    # --- word budget
    wc = word_range(fm.get("Word_Count_Target", ""))
    sys.path.insert(0, str(COUNT_WORDS_DIR))
    try:
        import count_words as cw  # type: ignore
        secs = cw.parse_outline(body)
        total = sum((x.target or 0) + (x.max_words or 0) for x in secs)
        rep.stats["section_words_sum"] = total
        if wc and total:
            lo, hi = wc
            if total > hi * 1.1:
                rep.add("MAJOR", "WC-sum", f"Tổng target các section {total} từ > Word_Count_Target {lo}–{hi} (+10%)")
            elif total < lo * 0.9:
                rep.add("MAJOR", "WC-sum", f"Tổng target các section {total} từ < Word_Count_Target {lo}–{hi} (−10%)")
    except ImportError:
        pass

    # --- data hygiene
    pending = [l.strip()[:90] for l in body.split("\n") if "CẦN XÁC NHẬN" in l]
    for l in pending:
        rep.add("MAJOR", "DATA-unverified", f"Còn số liệu chưa xác minh — xác minh hoặc bỏ trước khi trình bày: {l}")
    data_sec = re.search(r"^##\s*3\.\s*Dữ liệu[^\n]*\n([\s\S]*?)(?=^##\s|\Z)", body, re.M)
    if data_sec:
        rows = [r for r in data_sec.group(1).split("\n") if r.startswith("|") and not re.match(r"^\|\s*[-:]", r)][1:]
        nosrc = [r for r in rows if not re.search(r"https?://|market_facts|DSC nội bộ", r)]
        rep.stats["data_rows"] = len(rows)
        for r in nosrc:
            fact = r.strip("|").split("|")[0].strip()[:60]
            rep.add("MAJOR", "DATA-source", f"Dữ kiện không có URL nguồn (hoặc `market_facts` / `DSC nội bộ`): “{fact}” — "
                                            "không có nguồn gốc thì bài không link được, QG không đối chiếu được")
    year = date.today().year
    if str(year) not in body:
        rep.add("MAJOR", "DATA-stale", f"Outline không có số liệu/mốc nào năm {year}")
    left = re.findall(r"\[(?:Tên|Số|Tiêu đề|Câu hỏi|List|Từ khóa|điền)[^\]]*\]", text)
    if left:
        rep.add("MINOR", "DATA-placeholder", f"Còn {len(left)} placeholder template: {left[0]}")
    if re.search(r"Brand Context", body, re.I) is None:
        rep.add("MAJOR", "YAML-brand", "Thiếu section Brand Context (output Brand Guardian) — drafting sẽ mất tone/USP")
    return rep


def render(rep: Report) -> str:
    out = [f"# OUTLINE LINT — {rep.path}",
           f"**Kết quả:** {'PASS' if rep.passed() else 'FAIL'} · CRITICAL {rep.count('CRITICAL')} · "
           f"MAJOR {rep.count('MAJOR')} · MINOR {rep.count('MINOR')}"]
    if rep.stats:
        out.append("Stats: " + ", ".join(f"{k}={v}" for k, v in rep.stats.items()))
    for sev in ("CRITICAL", "MAJOR", "MINOR"):
        items = [i for i in rep.items if i["severity"] == sev]
        if items:
            out += ["", f"## {sev} ({len(items)})"] + [f"- [{i['check']}] {i['message']}" for i in items]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outline")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rep = lint(Path(a.outline))
    if a.json:
        print(json.dumps({"passed": rep.passed(), "stats": rep.stats, "findings": rep.items}, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    return 0 if rep.passed() else 1


if __name__ == "__main__":
    sys.exit(main())
