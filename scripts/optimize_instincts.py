#!/usr/bin/env python3
"""Sync instincts-archive.md → compact instincts.md (+ per-scope files).

Reads every ACTIVE instinct from the archive, then:
  1. Dedupes near-identical entries (title token Jaccard ≥ 0.5) — keeps the most recent.
  2. Moves instincts that qa_lint.py now enforces mechanically into a one-line
     "đã tự động hoá" list instead of repeating the full rule text.
  3. Trims each remaining rule to ~MAX_CHARS at a sentence boundary.
  4. Writes Global instincts to .antigravity/memory/instincts.md (mục tiêu ≤ 8.000 ký tự) and
     scoped instincts ("Chỉ topic: X") to .antigravity/memory/instincts-by-scope/<x>.md.

Usage:  python scripts/optimize_instincts.py [--max-chars 450] [--dry-run]
The archive is never modified.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / ".antigravity/memory/instincts-archive.md"
CORE = ROOT / ".antigravity/memory/instincts.md"
SCOPE_DIR = ROOT / ".antigravity/memory/instincts-by-scope"

DEDUPE_THRESHOLD = 0.5
MAX_CHARS = 450

# Instincts whose title matches one of these patterns are fully enforced by scripts/qa_lint.py.
# They are listed (not expanded) in instincts.md so the model knows the rule exists and who checks it.
LINT_COVERED = [
    (r"latex", "FMT-latex"),
    (r"code block|ascii", "FMT-codeblock"),
    (r"callout", "FMT-callout"),
    (r"đường kẻ ngang", "FMT-hr"),
    (r"nhãn in đậm|dấu hai chấm", "FMT-bold-label"),
    (r"tiêu đề seo|59 ký tự", "CL1-title"),
    (r"đường dẫn tuyệt đối|absolute url|absolute path", "LINK-relative / LINK-local"),
    (r"sitemap live", "LINK-sitemap"),
    (r"mở tài khoản chứng khoán dsc", "LINK-cta"),
    (r"ngoặc kép nhấn mạnh|emphatic quotes", "CL2-quotes"),
    (r"ngoặc kép trong yaml", "FM-quotes"),
    (r"cơ chế truyền dẫn|chiến lược thay cho thủ thuật|xương máu", "CL2-softban"),
    (r"thời gian đăng ký ekyc", "CL5-fact"),
    (r"list-item chứa nhiều câu|đếm câu list-item", "CL6-list-item"),
    (r"từ trigger", "CL2-softban"),
    (r"danh sách liên tiếp", "CL6-lists"),
    (r"mở bài vĩ mô", "CL2-blacklist"),
    (r"không dùng \"?xem thêm", "LINK-anchor"),
]

STOP = set("la gi va cua cho cac nhung co khong duoc trong khi voi de mot nay nao nhu the cach nen hay ve tu den "
           "theo tai bi se da dang hon nhat can phai bai viet su dung hoac bang bat buoc tuyet doi luon".split())

CATEGORIES = [
    ("Văn phong & Ngôn từ (Style & Tone)",
     ["vĩ mô", "ngoặc kép", "thuật ngữ", "từ ", "giọng", "xưng hô", "mở bài", "kết bài", "intent", "persona"]),
    ("Cấu trúc & Định dạng (Structure & Formatting)",
     ["heading", "đoạn", "list", "bảng", "table", "sapo", "dấu câu", "định dạng", "faq", "h2", "word count", "visual",
      "ma trận", "so sánh"]),
    ("SEO & Liên kết (SEO & Internal Links)",
     ["link", "sitemap", "đường dẫn", "seo", "title", "url", "anchor"]),
    ("Sản phẩm & Thương hiệu (Products & Brand Context)", []),
]


# ─────────────────────────── Parsing (unchanged format) ───────────────────────────

def parse_instincts_file(archive_path):
    with open(archive_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    instincts, current = [], None
    for line in lines:
        stripped = line.strip()
        if line.startswith("### "):
            title = line[4:].strip()
            if title == "[Tên ngắn gọn]" or not title:
                continue
            if current:
                instincts.append(current)
            current = {"title": title, "status": "", "source": "", "user_feedback": "",
                       "instinct_lines": [], "scope": "Global", "parsing_instinct": False}
            continue
        if current is None:
            continue
        if stripped.startswith("- **Trạng thái:**"):
            current["status"] = stripped.replace("- **Trạng thái:**", "").strip()
            current["parsing_instinct"] = False
        elif stripped.startswith("- **Nguồn:**"):
            current["source"] = stripped.replace("- **Nguồn:**", "").strip()
            current["parsing_instinct"] = False
        elif stripped.startswith("- **Phản hồi từ User:**"):
            current["user_feedback"] = stripped.replace("- **Phản hồi từ User:**", "").strip()
            current["parsing_instinct"] = False
        elif stripped.startswith("- **Bản năng:**"):
            current["parsing_instinct"] = True
            content = stripped.replace("- **Bản năng:**", "").strip()
            if content:
                current["instinct_lines"].append(content)
        elif stripped.startswith("- **Phạm vi:**"):
            current["scope"] = stripped.replace("- **Phạm vi:**", "").strip()
            current["parsing_instinct"] = False
        elif current["parsing_instinct"]:
            current["instinct_lines"].append(line.rstrip("\r\n"))
    if current:
        instincts.append(current)
    return instincts


# ─────────────────────────── Helpers ───────────────────────────

def unaccent(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def toks(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", unaccent(s)) if len(t) > 2 and t not in STOP}


def body_text(inst) -> str:
    return re.sub(r"\s+", " ", " ".join(l.strip() for l in inst["instinct_lines"])).strip()


def trim(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    m = max(cut.rfind(". "), cut.rfind("; "))
    if m > limit * 0.5:
        return cut[: m + 1] + " (…xem archive)"
    return cut.rstrip() + "… (xem archive)"


def dedupe(instincts):
    """Drop earlier entries whose title overlaps ≥ threshold with a later one."""
    keep, merged = [], {}
    sigs = [toks(i["title"]) for i in instincts]
    for i in range(len(instincts)):
        dup_of = None
        for j in range(i + 1, len(instincts)):
            inter = len(sigs[i] & sigs[j])
            union = len(sigs[i] | sigs[j]) or 1
            if inter / union >= DEDUPE_THRESHOLD:
                dup_of = j
                break
        if dup_of is None:
            keep.append(instincts[i])
        else:
            # carry over anything already merged into i (chains: a→b→c)
            chain = merged.pop(instincts[i]["title"], [])
            merged.setdefault(instincts[dup_of]["title"], []).extend(chain + [instincts[i]["title"]])
    return keep, merged


def lint_check_for(title: str) -> str | None:
    """Return the qa_lint check id(s) if EVERY clause of the title is machine-checked."""
    clauses = [c for c in re.split(r"\s+(?:và|&|,)\s+", title.lower()) if c.strip()]
    checks = []
    for c in clauses:
        hit = next((check for pat, check in LINT_COVERED if re.search(pat, c)), None)
        if hit is None:
            return None
        if hit not in checks:
            checks.append(hit)
    return " + ".join(checks) if checks else None


def categorize(inst) -> str:
    hay = (inst["title"] + " " + body_text(inst)).lower()
    for name, kws in CATEGORIES[:-1]:
        if any(k in hay for k in kws):
            return name
    return CATEGORIES[-1][0]


def scope_slug(scope: str) -> str:
    s = re.sub(r"^chỉ topic:\s*", "", scope.strip(), flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", unaccent(s)).strip("-") or "other"


# ─────────────────────────── Rendering ───────────────────────────

def render_core(globals_, linted, merged, scoped_files, max_chars) -> str:
    out = ["# Continuous Learning: Instincts (Bản năng rút gọn)", "",
           "> **Bắt buộc:** Mọi agent/skill đọc file này trước khi viết. Bản đầy đủ (nguồn, feedback gốc) ở "
           "`.antigravity/memory/instincts-archive.md`.",
           "> **Sinh tự động** bởi `scripts/optimize_instincts.py` — không sửa tay. Sau `/learn`, ghi vào archive rồi chạy lại script.",
           ""]
    if scoped_files:
        out.append("> **Bản năng theo topic:** " + ", ".join(f"`instincts-by-scope/{f}`" for f in scoped_files)
                   + " — chỉ load khi bài thuộc topic đó.")
        out.append("")
    cats: dict[str, list] = {}
    for inst in globals_:
        cats.setdefault(categorize(inst), []).append(inst)
    for name, _ in CATEGORIES:
        items = cats.get(name)
        if not items:
            continue
        out += [f"## {name}", ""]
        for inst in items:
            title = inst["title"]
            if title in merged:
                title += f" *(gộp: {'; '.join(merged[title])})*"
            out.append(f"### {title}")
            out.append("- " + trim(body_text(inst), max_chars))
            out.append("")
    if linted:
        out += ["## ✅ Đã tự động hoá bởi `scripts/qa_lint.py` (vẫn phải tuân thủ khi viết)", "",
                "| Bản năng | Check |", "|---|---|"]
        for inst, check in linted:
            out.append(f"| {inst['title']} | `{check}` |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_scope(scope: str, items, max_chars) -> str:
    out = [f"# Instincts — {scope}", "",
           f"> Chỉ load khi bài viết thuộc phạm vi **{scope}**. Sinh tự động từ instincts-archive.md.", ""]
    for inst in items:
        out += [f"### {inst['title']}", "- " + trim(body_text(inst), max_chars), ""]
    return "\n".join(out).rstrip() + "\n"


def run(max_chars: int, dry_run: bool):
    if not ARCHIVE.exists():
        print(f"Error: {ARCHIVE} not found.")
        return 2
    all_inst = parse_instincts_file(str(ARCHIVE))
    active = [i for i in all_inst if i["status"].upper() == "ACTIVE"]
    print(f"Parsed {len(all_inst)} instincts ({len(active)} ACTIVE) from archive.")

    active, merged = dedupe(active)
    for k, v in merged.items():
        print(f"  dedupe: {v} → giữ '{k}'")

    globals_, linted, scoped = [], [], {}
    for inst in active:
        if inst["scope"] != "Global":
            scoped.setdefault(inst["scope"], []).append(inst)
            continue
        check = lint_check_for(inst["title"])
        if check:
            linted.append((inst, check))
        else:
            globals_.append(inst)

    scoped_files = [f"{scope_slug(s)}.md" for s in scoped]
    core = render_core(globals_, linted, merged, scoped_files, max_chars)
    size, chars = len(core.encode("utf-8")), len(core)
    print(f"instincts.md: {len(globals_)} full + {len(linted)} lint-covered → {chars:,} ký tự ({size / 1024:.1f} KB UTF-8)"
          + ("  ⚠ > 8.000 ký tự, giảm --max-chars hoặc DEPRECATE bớt trong archive" if chars > 8000 else ""))
    for s, items in scoped.items():
        print(f"instincts-by-scope/{scope_slug(s)}.md: {len(items)} bản năng")
    if dry_run:
        return 0
    CORE.write_text(core, encoding="utf-8")
    if scoped:
        SCOPE_DIR.mkdir(exist_ok=True)
        for s, items in scoped.items():
            (SCOPE_DIR / f"{scope_slug(s)}.md").write_text(render_scope(s, items, max_chars), encoding="utf-8")
    print("Updated instincts.md successfully.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.exit(run(a.max_chars, a.dry_run))
