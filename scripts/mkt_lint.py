#!/usr/bin/env python3
"""QA máy cho output marketing ngoài bài SEO: post social, ad copy Meta, copy landing.

Dùng:
    python scripts/mkt_lint.py <file> --channel facebook|zalo|linkedin|meta-ad|landing [--json]

File: markdown. Mỗi biến thể là 1 mục `## <tên>` (mục có tên Ghi chú / Notes / Brief bị bỏ qua).
Không có `## ` nào → cả file là 1 biến thể. Với meta-ad, mỗi biến thể ghi các trường:
    Primary text: …   (hoặc "Văn bản chính:")
    Headline: …       (hoặc "Tiêu đề:")
    Description: …    (hoặc "Mô tả:")

Rule:
    COMP-*  compliance tài chính (.agents/core/rules/compliance-finance.md)
    AI-*    cụm cấm trong knowledge/1-brand/anti-ai-rules-blacklist.md + glossary Từ bị cấm
    LEN-*, TAG-*, CTA-*, FIELD-*  hình thức theo kênh (giới hạn biên tập, không phải giới hạn kỹ thuật chắc chắn)
Exit 1 nếu có CRITICAL hoặc MAJOR.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import setup_utf8  # noqa: E402
from activity_log import emit  # noqa: E402
import qa_lint as ql  # noqa: E402

CHANNELS = ("facebook", "zalo", "linkedin", "meta-ad", "landing")
MKT_DOMAIN = {"meta-ad": "ads-meta", "landing": "landing"}  # activity-log domain; others = social
SEVERITIES = ("CRITICAL", "MAJOR", "MINOR", "INFO")

# body_max = (MINOR threshold, MAJOR threshold or None); hook = chars visible before "Xem thêm"
LIMITS = {
    "facebook": {"body_max": (2000, None), "hook": 125, "tags": 5},
    "zalo": {"body_max": (2000, None), "hook": None, "tags": 5},
    "linkedin": {"body_max": (2500, 3000), "hook": 210, "tags": 5},
    "meta-ad": {"primary": (125, 500), "headline": (40, 255), "description": (30, 255), "tags": 0},
    "landing": {},
}

PROMISE = re.compile(
    r"(?i)((chắc chắn|đảm bảo|bảo đảm|cam kết)\s+(có\s+)?(lãi|lời|lợi nhuận|sinh lời)"
    r"|lãi\s+\d+(?:[.,]\d+)?\s*%\s*/?\s*(một\s+)?(tháng|tuần|ngày)"
    r"|không\s+(lo|sợ)\s+(lỗ|thua lỗ)|an toàn tuyệt đối|siêu lợi nhuận|nhân đôi tài sản|làm giàu nhanh"
    r"|\bx\s?\d+\s+tài sản)")
NO_RISK = re.compile(r"(?i)\b(không|zero|0)\s+(có\s+)?rủi ro\b")
RATE = re.compile(r"(?i)(phí|lãi suất|lãi vay|margin|ký quỹ)[^.\n]{0,40}\d+(?:[.,]\d+)?\s*%")
RATE_CONDITION = re.compile(r"(?i)(áp dụng|điều kiện|thể lệ|biểu phí|từ ngày|đến ngày|chương trình)")
PAST_PERF = re.compile(r"(?i)(hiệu quả|lợi nhuận|sinh lời|tăng trưởng danh mục)[^.\n]{0,40}\d+(?:[.,]\d+)?\s*%")
PAST_DISCLAIMER = re.compile(r"(?i)quá khứ\s+không\s+(đảm bảo|phản ánh|bảo đảm)")
LEVERAGE = re.compile(r"(?i)\b(margin|ký quỹ|phái sinh|đòn bẩy)\b")
VIEW = re.compile(r"(?i)\b(tăng giá|giảm giá|bứt phá|triển vọng|định giá rẻ|tiềm năng tăng|sắp tăng)\b")
COMPETITOR = re.compile(r"\b(VPS|TCBS|SSI|VNDirect|VNDIRECT|MBS|HSC|VCBS|Vietcap|VPBankS)\b")
NEGATIVE = re.compile(r"(?i)\b(kém|tệ|lừa|chậm hơn|đắt hơn|thua xa|không bằng)\b")
FOMO = re.compile(r"(?i)(cơ hội cuối cùng|đừng bỏ lỡ|nhanh tay|kẻo lỡ|siêu cổ|duy nhất hôm nay|chỉ còn \d+ (giờ|phút))")
CTA = re.compile(r"(?i)(https?://|mở tài khoản|đăng ký|tìm hiểu|xem chi tiết|đọc (thêm|bài)|liên hệ|tải app|nhắn tin|inbox|bình luận)")
HASHTAG = re.compile(r"(?<![\w&])#[\wÀ-ỹ]+")
PLACEHOLDER = re.compile(r"(?i)\bTODO\b|\bxxx\b|\[\.\.\.\]|\[điền[^\]]*\]")
LEGAL_TAG = "[CẦN PHÁP CHẾ DUYỆT]"
TICKER = re.compile(r"(?<![\w-])[A-Z][A-Z0-9]{2,7}(?![\w-])")
SKIP_SECTION = re.compile(r"(?i)^(ghi chú|notes?|brief|nguồn|sources?)\b")
FIELD_RE = {
    "primary": re.compile(r"(?im)^\**\s*(primary text|primary|văn bản chính)\s*:?\**\s*:?\s*(.*)$"),
    "headline": re.compile(r"(?im)^\**\s*(headline|tiêu đề)\s*:?\**\s*:?\s*(.*)$"),
    "description": re.compile(r"(?im)^\**\s*(description|mô tả)\s*:?\**\s*:?\s*(.*)$"),
}


@dataclass
class Issue:
    rule: str
    severity: str
    variant: str
    msg: str
    text: str = ""


@dataclass
class Report:
    file: str
    channel: str
    issues: list[Issue] = field(default_factory=list)
    variants: int = 0

    def add(self, rule, sev, variant, msg, text=""):
        self.issues.append(Issue(rule, sev, variant, msg, text.strip()[:160]))

    def count(self, sev):
        return sum(1 for i in self.issues if i.severity == sev)

    @property
    def passed(self):
        return self.count("CRITICAL") == 0 and self.count("MAJOR") == 0


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def split_variants(text: str) -> list[tuple[str, str]]:
    body = strip_frontmatter(text)
    parts = re.split(r"(?m)^##\s+(.+)$", body)
    if len(parts) == 1:
        return [("(toàn bài)", body.strip())]
    out = []
    lead = parts[0].strip()
    if lead and not lead.startswith("# "):
        out.append(("(mở đầu)", lead))
    for name, content in zip(parts[1::2], parts[2::2]):
        if SKIP_SECTION.match(name.strip()):
            continue
        out.append((name.strip(), content.strip()))
    return out


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?…])\s+|\n+", text) if s.strip()]


def extract_fields(block: str) -> dict[str, str]:
    out = {}
    for key, rx in FIELD_RE.items():
        m = rx.search(block)
        if m:
            out[key] = m.group(2).strip().strip("*").strip()
    return out


def check_compliance(rep: Report, name: str, block: str, channel: str) -> None:
    for m in PROMISE.finditer(block):
        rep.add("COMP-promise", "CRITICAL", name, "Hứa hẹn / bảo đảm lợi nhuận — bỏ hẳn", m.group(0))
    for m in NO_RISK.finditer(block):
        rep.add("COMP-no-risk", "MAJOR", name, "Hàm ý đầu tư không rủi ro — đổi thành mô tả rủi ro cụ thể", m.group(0))
    has_disclaimer = bool(ql.DISCLAIMER.search(block))
    for s in sentences(block):
        tickers = [t for t in TICKER.findall(s) if t not in ql.NOT_TICKER and not COMPETITOR.fullmatch(t)]
        if tickers and ql.ADVICE.search(s):
            sev = "MAJOR" if channel == "landing" else "CRITICAL"
            rep.add("COMP-advice", sev, name, f"Khuyến nghị mua/bán mã cụ thể ({', '.join(tickers)}) trên kênh quảng bá", s)
        elif tickers and VIEW.search(s) and not has_disclaimer:
            rep.add("COMP-disclaimer", "MAJOR", name,
                    "Nhận định về mã cụ thể nhưng thiếu câu “…chỉ mang tính tham khảo, không phải khuyến nghị đầu tư”", s)
        if COMPETITOR.search(s):
            if NEGATIVE.search(s):
                rep.add("COMP-competitor", "MAJOR", name, "So sánh hạ thấp đích danh đối thủ", s)
            else:
                rep.add("COMP-competitor", "MINOR", name, "Nhắc tên đối thủ — chỉ so sánh khách quan, có nguồn + mốc thời gian", s)
    rate = RATE.search(block)
    if rate and not (RATE_CONDITION.search(block) or ql.TEMPORAL_MARKER.search(block)):
        rep.add("COMP-rate-condition", "MAJOR", name, "Nêu phí / lãi suất nhưng thiếu điều kiện hoặc mốc áp dụng", rate.group(0))
    past = PAST_PERF.search(block)
    if past and not PAST_DISCLAIMER.search(block):
        rep.add("COMP-past-performance", "MAJOR", name,
                "Nêu hiệu quả quá khứ — thêm “kết quả quá khứ không đảm bảo kết quả tương lai”", past.group(0))
    lev = LEVERAGE.search(block)
    if lev and "rủi ro" not in block.lower():
        rep.add("COMP-leverage-risk", "MAJOR", name, f"Nhắc {lev.group(0)} nhưng không nêu rủi ro đòn bẩy", lev.group(0))
    for m in FOMO.finditer(block):
        rep.add("COMP-fomo", "MINOR", name, "Giật tít FOMO, lệch giọng thương hiệu", m.group(0))
    if LEGAL_TAG in block:
        rep.add("COMP-legal-review", "INFO", name, "Có claim chờ pháp chế duyệt — không đăng trước khi duyệt")


def check_anti_ai(rep: Report, name: str, block: str, hard: list[str], forbidden: list[str]) -> None:
    low = block.lower()
    for p in hard:
        if p.lower() in low:
            rep.add("AI-blacklist", "MAJOR", name, f"Cụm cấm (anti-ai-rules-blacklist): “{p}”")
    for t in forbidden:
        if t and t.lower() in low:
            rep.add("AI-forbidden-term", "MAJOR", name, f"Từ cấm trong glossary: “{t}”")
    for m in PLACEHOLDER.finditer(block):
        rep.add("FIELD-placeholder", "MAJOR", name, "Còn placeholder chưa điền", m.group(0))


def _len_check(rep, name, rule, label, text, limits):
    soft, hard = limits
    n = len(text)
    if hard and n > hard:
        rep.add(rule, "MAJOR", name, f"{label} {n} ký tự > {hard}")
    elif soft and n > soft:
        rep.add(rule, "MINOR", name, f"{label} {n} ký tự > {soft} (dễ bị cắt / dài so với kênh)")


def check_format(rep: Report, name: str, block: str, channel: str) -> None:
    lim = LIMITS[channel]
    tags = HASHTAG.findall(block)
    if channel == "meta-ad":
        fields = extract_fields(block)
        for key in ("primary", "headline"):
            if not fields.get(key):
                rep.add("FIELD-missing", "MAJOR", name, f"Thiếu trường {key}")
        for key in ("primary", "headline", "description"):
            if fields.get(key):
                _len_check(rep, name, f"LEN-{key}", key, fields[key], lim[key])
        if tags:
            rep.add("TAG-count", "MINOR", name, f"Ad copy có {len(tags)} hashtag — thường bỏ để giữ chỗ cho thông điệp")
        return
    if channel == "landing":
        return
    body = HASHTAG.sub("", block).strip()
    _len_check(rep, name, "LEN-body", "Thân bài", body, lim["body_max"])
    first = next((ln for ln in body.splitlines() if ln.strip() and not ln.startswith("!")), "")
    if lim.get("hook") and len(first) > lim["hook"]:
        rep.add("LEN-hook", "MINOR", name,
                f"Câu mở {len(first)} ký tự > {lim['hook']} — phần hiện trước “Xem thêm” chưa chứa ý chính", first)
    if len(tags) > lim["tags"]:
        rep.add("TAG-count", "MINOR", name, f"{len(tags)} hashtag > {lim['tags']}")
    if not CTA.search(block):
        rep.add("CTA-missing", "MINOR", name, "Không có link hay lời mời hành động")


def lint(path: Path, channel: str) -> Report:
    text = path.read_text(encoding="utf-8")
    rep = Report(str(path), channel)
    hard, _hedge, _soft = ql.load_blacklist()
    forbidden = ql.load_forbidden_terms()
    variants = split_variants(text)
    rep.variants = len(variants)
    for name, block in variants:
        check_compliance(rep, name, block, channel)
        check_anti_ai(rep, name, block, hard, forbidden)
        check_format(rep, name, block, channel)
    return rep


def render(rep: Report) -> str:
    head = (f"mkt_lint · {rep.file} · kênh {rep.channel} · {rep.variants} biến thể\n"
            f"{'PASS' if rep.passed else 'FAIL'} — " + " ".join(f"{s}:{rep.count(s)}" for s in SEVERITIES))
    lines = [head]
    for sev in SEVERITIES:
        for i in (x for x in rep.issues if x.severity == sev):
            lines.append(f"  [{i.severity}] {i.rule} · {i.variant} · {i.msg}" + (f"\n      “{i.text}”" if i.text else ""))
    return "\n".join(lines)


def main(argv=None) -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--channel", required=True, choices=CHANNELS)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    rep = lint(Path(a.file), a.channel)
    if a.json:
        print(json.dumps({"file": rep.file, "channel": rep.channel, "passed": rep.passed, "variants": rep.variants,
                          "issues": [i.__dict__ for i in rep.issues]}, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    from activity_log import classify
    dom, target = classify(a.file) or (MKT_DOMAIN.get(a.channel, "social"), Path(a.file).stem)
    emit(dom, "qa", target, skill="mkt_lint", result="PASS" if rep.passed else f"FAIL ({len(rep.issues)} lỗi)",
         path=a.file, note=a.channel)
    return 0 if rep.passed else 1


if __name__ == "__main__":
    sys.exit(main())
