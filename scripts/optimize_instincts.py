#!/usr/bin/env python3
"""Sync instincts-archive.md → compact instincts.md (+ per-scope files), and audit the archive.

Archive entry format (fields after Phạm vi are optional; old entries without them still work):

    ### [Tên ngắn gọn]
    - **ID:** I042                      stable id — /learn edits the rule in place, never re-numbers
    - **Trạng thái:** ACTIVE | DEPRECATED | ARTICLE   (ARTICLE = ghi chú riêng 1 bài: không load khi viết,
                                        tra bằng `grep -n "Nguồn:" archive | grep <slug>` khi /optimize đúng bài đó)
    - **Tag:** sapo                     topic of the rule; one ACTIVE rule per (tag, scope)
    - **Nguồn:** slug
    - **Phản hồi từ User:** "..."
    - **Bản năng:** 1–3 short points    (≤ MAX_CHARS — rules are written short, never truncated)
    - **Phạm vi:** Global | Chỉ topic: X
    - **Checklist:** qa_lint:CL2-softban, outline_lint:H2-conclusion   checks that enforce it
    - **Máy kiểm:** full | partial      full → listed in the "đã tự động hoá" table only
    - **Thay bởi:** I0xx                (DEPRECATED only)
    - **Cập nhật:** 2026-11-09

What the script does:
  1. Global rules → instincts.md (full text, no truncation), scoped rules → instincts-by-scope/<x>.md,
     machine-enforced rules → one-line table.
  2. Audits: LONG (rule > MAX_CHARS), TAG-DUP (≥2 ACTIVE rules share tag+scope), BUDGET (instincts.md
     > CORE_BUDGET), ORPHAN (an ACTIVE rule rendered nowhere), SUPERSEDE (DEPRECATED without valid
     "Thay bởi"), NO-ID. `--check` exits 1 when any audit fires.
  3. `--stats`: recurrence of each rule's checks in knowledge/3-pipeline/qa-check-log.csv
     (written by `qa_lint.py --log`) — a check that keeps firing after the rule was learned means the
     rule is not working; a rule whose check never fires for months is a pruning candidate.
  4. `--assign-ids`: one-time, writes `- **ID:** Ixxx` into archive entries that lack one (backup first).

Usage:  python scripts/optimize_instincts.py [--check] [--dry-run] [--stats] [--assign-ids] [--show ID|TAG|SLUG]
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / ".antigravity/memory/instincts-archive.md"
CORE = ROOT / ".antigravity/memory/instincts.md"
SCOPE_DIR = ROOT / ".antigravity/memory/instincts-by-scope"
CHECK_LOG = ROOT / "knowledge/3-pipeline/qa-check-log.csv"

DEDUPE_THRESHOLD = 0.5
MAX_CHARS = 450              # a rule longer than this is reported, never cut
CORE_BUDGET = 8000           # chars; instincts.md is loaded by every session

# Legacy: titles fully enforced by qa_lint.py (entries without a Checklist field).
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

FIELDS = {  # label in archive → key
    "ID": "id", "Trạng thái": "status", "Tag": "tag", "Nguồn": "source", "Phản hồi từ User": "user_feedback",
    "Phạm vi": "scope", "Checklist": "checklist", "Máy kiểm": "coverage", "Thay bởi": "superseded_by",
    "Cập nhật": "updated",
}
FIELD_RX = re.compile(r"^- \*\*(%s):\*\*\s*(.*)$" % "|".join(map(re.escape, FIELDS)))


# ─────────────────────────── Parsing ───────────────────────────

def parse_instincts_file(archive_path):
    with open(archive_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    instincts, current, in_fence = [], None, False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):          # format examples in the header are not rules
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("### "):
            title = line[4:].strip()
            if title == "[Tên ngắn gọn]" or not title:
                continue
            if current:
                instincts.append(current)
            current = {"title": title, "status": "", "source": "", "user_feedback": "", "instinct_lines": [],
                       "scope": "Global", "id": "", "tag": "", "checklist": "", "coverage": "",
                       "superseded_by": "", "updated": "", "parsing_instinct": False}
            continue
        if current is None:
            continue
        m = FIELD_RX.match(stripped)
        if m:
            current[FIELDS[m.group(1)]] = m.group(2).strip()
            current["parsing_instinct"] = False
        elif stripped.startswith("- **Bản năng:**"):
            current["parsing_instinct"] = True
            content = stripped.replace("- **Bản năng:**", "").strip()
            if content:
                current["instinct_lines"].append(content)
        elif current["parsing_instinct"]:
            if stripped.startswith("## ") or stripped == "---":
                current["parsing_instinct"] = False
            else:
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


def is_global(inst) -> bool:
    return inst["scope"].strip().lower() in ("", "global")


def label(inst) -> str:
    return f"[{inst['id']}] {inst['title']}" if inst["id"] else inst["title"]


def dedupe(instincts):
    """Legacy entries only (no Tag): drop earlier entries whose title overlaps ≥ threshold with a later one.
    Tagged entries are never dropped — duplicates among them are reported as TAG-DUP instead."""
    keep, merged = [], {}
    sigs = [toks(i["title"]) for i in instincts]
    for i in range(len(instincts)):
        dup_of = None
        if not instincts[i]["tag"]:
            for j in range(i + 1, len(instincts)):
                if instincts[j]["tag"]:
                    continue
                inter = len(sigs[i] & sigs[j])
                union = len(sigs[i] | sigs[j]) or 1
                if inter / union >= DEDUPE_THRESHOLD:
                    dup_of = j
                    break
        if dup_of is None:
            keep.append(instincts[i])
        else:
            chain = merged.pop(instincts[i]["title"], [])
            merged.setdefault(instincts[dup_of]["title"], []).extend(chain + [instincts[i]["title"]])
    return keep, merged


def lint_check_for(inst) -> str | None:
    """Check id(s) when the rule is fully machine-enforced, else None."""
    if inst["checklist"]:
        return inst["checklist"] if inst["coverage"].lower().startswith("full") else None
    clauses = [c for c in re.split(r"\s+(?:và|&|,)\s+", inst["title"].lower()) if c.strip()]
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


def check_ids(checklist: str) -> list[str]:
    """'qa_lint:CL2-softban, outline_lint:H2-x' / 'CL2-softban + FMT-hr' → ['CL2-softban', 'H2-x', ...]"""
    out = []
    for part in re.split(r"[,+]", checklist or ""):
        part = part.strip().strip("`")
        if part:
            out.append(part.split(":", 1)[-1].strip())
    return out


# ─────────────────────────── Rendering ───────────────────────────

def render_rule(inst) -> list[str]:
    head = f"### {label(inst)}"
    if inst["checklist"] and not inst["coverage"].lower().startswith("full"):
        head += " (lint)"   # check ids stay in the archive; core only flags it
    return [head, "- " + body_text(inst), ""]


def render_core(globals_, linted, merged, scoped_files) -> str:
    out = ["# Instincts", "",
           "> Đọc trước khi viết; rule ở đây là đầy đủ. Sinh từ `instincts-archive.md` bằng `scripts/optimize_instincts.py` "
           "— không sửa tay. `(lint)` = có check máy bắt một phần.",
           ""]
    if scoped_files:
        out.append("> Theo topic, load thêm 1 file trong `instincts-by-scope/`: "
                   + ", ".join(f"`{f}` ({lab})" for f, lab in scoped_files))
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
            lines = render_rule(inst)
            if inst["title"] in merged:
                lines[0] += f" *(gộp: {'; '.join(merged[inst['title']])})*"
            out += lines
    if linted:
        out += ["## ✅ Đã tự động hoá (vẫn phải tuân thủ khi viết)", "",
                "| Bản năng | Check |", "|---|---|"]
        for inst, check in linted:
            out.append(f"| {label(inst)} | `{check}` |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_scope(scope: str, items) -> str:
    out = [f"# Instincts — {scope}", "",
           f"> Chỉ load khi bài viết thuộc phạm vi **{scope}**. Sinh tự động từ instincts-archive.md.", ""]
    for inst in items:
        out += render_rule(inst)
    return "\n".join(out).rstrip() + "\n"


# ─────────────────────────── Audit ───────────────────────────

def audit(all_inst, active, core, scope_texts, max_chars) -> list[tuple[str, str]]:
    issues = []
    ids = {i["id"] for i in all_inst if i["id"]}
    active_ids = {i["id"] for i in active if i["id"]}
    for i in active:
        if not i["id"]:
            issues.append(("NO-ID", i["title"]))
        n = len(body_text(i))
        if n > max_chars:
            issues.append(("LONG", f"{label(i)} — {n} ký tự (> {max_chars}): tách / viết ngắn lại"))
    seen: dict[tuple[str, str], list[str]] = {}
    for i in active:
        if i["tag"]:
            seen.setdefault((i["tag"].split(",")[0].strip().lower(), scope_slug(i["scope"])), []).append(label(i))
    for (tag, scope), labs in seen.items():
        if len(labs) > 1:
            issues.append(("TAG-DUP", f"tag `{tag}` ({scope}) có {len(labs)} rule ACTIVE: " + " | ".join(labs)))
    if len(core) > CORE_BUDGET:
        issues.append(("BUDGET", f"instincts.md {len(core):,} ký tự > {CORE_BUDGET:,} — gộp theo tag, "
                                 "chuyển rule 1 chủ đề sang Chỉ topic, hoặc DEPRECATE"))
    rendered = core + "\n".join(scope_texts)
    for i in active:
        if i["title"] not in rendered and not (i["id"] and f"[{i['id']}]" in rendered):
            issues.append(("ORPHAN", f"{label(i)} không xuất hiện ở instincts.md / by-scope / bảng tự động hoá"))
    for i in all_inst:
        if i["status"].upper() == "DEPRECATED" and i["id"]:
            sup = i["superseded_by"]
            if sup and sup not in active_ids:
                issues.append(("SUPERSEDE", f"{label(i)} → `{sup}` không phải rule ACTIVE"))
    dup_ids = [x for x in ids if sum(1 for i in all_inst if i["id"] == x) > 1]
    for x in dup_ids:
        issues.append(("ID-DUP", f"ID {x} dùng cho nhiều rule"))
    return issues


# ─────────────────────────── Stats (recurrence) ───────────────────────────

def stats(active) -> int:
    if not CHECK_LOG.exists():
        print(f"Chưa có {CHECK_LOG.relative_to(ROOT)} — chạy `qa_lint.py <Final> --log` khi /approve để bắt đầu đo.")
        return 0
    rows = list(csv.DictReader(CHECK_LOG.open(encoding="utf-8")))
    articles = {(r["date"], r["slug"]) for r in rows}
    print(f"Log: {len(rows)} dòng, {len(articles)} lượt lint bài.\n")
    print("| Rule | Check | Bài lint sau khi học | Bài còn lỗi | Lần cuối |\n|---|---|---:|---:|---|")
    for i in active:
        checks = check_ids(i["checklist"]) or (check_ids(lint_check_for(i) or ""))
        if not checks:
            continue
        since = i["updated"] or "0000"
        lint_after = {(r["date"], r["slug"]) for r in rows if r["date"] >= since}
        hit = {(r["date"], r["slug"]) for r in rows if r["date"] >= since and r["check"] in checks}
        last = max((d for d, _ in hit), default="-")
        print(f"| {label(i)[:70]} | {', '.join(checks)} | {len(lint_after)} | {len(hit)} | {last} |")
    return 0


# ─────────────────────────── Lookup (token-cheap retrieval) ───────────────────────────

def show(query: str) -> int:
    """Print only the archive blocks matching an ID (I105), a tag (sapo) or an article slug (Nguồn).
    Agents use this instead of opening the 100 KB archive."""
    q = query.strip()
    qn = unaccent(q)
    hits = []
    for i in parse_instincts_file(str(ARCHIVE)):
        by_id = q.upper() == i["id"].upper()
        by_tag = bool(i["tag"]) and qn == unaccent(i["tag"].split(",")[0].strip())
        by_slug = len(qn) > 3 and qn in unaccent(i["source"])
        if by_id or by_tag or by_slug:
            hits.append(i)
    if not hits:
        print(f"Không có rule nào khớp “{q}” (ID / Tag / slug trong Nguồn).")
        return 1
    order = {"ACTIVE": 0, "ARTICLE": 1}
    for i in sorted(hits, key=lambda x: order.get(x["status"].upper(), 2)):
        extra = f" → thay bởi {i['superseded_by']}" if i["superseded_by"] else ""
        print(f"### {label(i)}  [{i['status']}{extra}] · {i['scope']}")
        if i["user_feedback"]:
            print(f"- Phản hồi gốc: {i['user_feedback'][:300]}")
        print(f"- {body_text(i)}\n")
    return 0


# ─────────────────────────── IDs ───────────────────────────

def assign_ids() -> int:
    text = ARCHIVE.read_text(encoding="utf-8")
    used = [int(x) for x in re.findall(r"^- \*\*ID:\*\*\s*I(\d+)", text, re.M)]
    nxt = max(used, default=0) + 1
    backup = ARCHIVE.with_name(f"instincts-archive.bak-{date.today().isoformat()}.md")
    if not backup.exists():
        shutil.copy2(ARCHIVE, backup)
    out, lines, i, added = [], text.split("\n"), 0, 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.startswith("### ") and line[4:].strip() not in ("", "[Tên ngắn gọn]"):
            block = lines[i + 1:i + 4]
            if any(b.strip().startswith("- **Trạng thái:**") for b in block) and \
                    not any(b.strip().startswith("- **ID:**") for b in block):
                out.append(f"- **ID:** I{nxt:03d}")
                nxt += 1
                added += 1
        i += 1
    ARCHIVE.write_text("\n".join(out), encoding="utf-8")
    print(f"Gán {added} ID mới (backup: {backup.name}).")
    return 0


# ─────────────────────────── Main ───────────────────────────

def run(max_chars: int, dry_run: bool, check: bool = False):
    if not ARCHIVE.exists():
        print(f"Error: {ARCHIVE} not found.")
        return 2
    all_inst = parse_instincts_file(str(ARCHIVE))
    active = [i for i in all_inst if i["status"].upper() == "ACTIVE"]
    print(f"Parsed {len(all_inst)} instincts ({len(active)} ACTIVE) from archive.")

    kept, merged = dedupe(active)
    for k, v in merged.items():
        print(f"  dedupe (legacy, theo tiêu đề): {v} → giữ '{k}'")
    merged_titles = {t for v in merged.values() for t in v}

    globals_, linted, scoped, scope_label = [], [], {}, {}
    for inst in kept:
        chk = lint_check_for(inst)
        if chk and is_global(inst):
            linted.append((inst, chk))
        elif not is_global(inst):
            slug = scope_slug(inst["scope"])
            scoped.setdefault(slug, []).append(inst)
            lab = re.sub(r"^chỉ topic:\s*", "", inst["scope"].strip(), flags=re.I)
            if lab != slug or slug not in scope_label:      # prefer a human label over the bare slug
                scope_label[slug] = lab
        else:
            globals_.append(inst)

    scoped_files = [(f"{slug}.md", scope_label[slug]) for slug in sorted(scoped)]
    core = render_core(globals_, linted, merged, scoped_files)
    scope_texts = {slug: render_scope(scope_label[slug], items) for slug, items in scoped.items()}
    print(f"instincts.md: {len(globals_)} full + {len(linted)} tự động hoá → {len(core):,} ký tự "
          f"({len(core.encode('utf-8')) / 1024:.1f} KB UTF-8)")
    for slug in sorted(scoped):
        print(f"instincts-by-scope/{slug}.md: {len(scoped[slug])} bản năng, {len(scope_texts[slug]):,} ký tự")

    # merged legacy titles are rendered via their keeper's "(gộp: …)" note → not orphans
    issues = audit(all_inst, [i for i in active if i["title"] not in merged_titles],
                   core, list(scope_texts.values()), max_chars)
    if issues:
        counts: dict[str, int] = {}
        for k, _ in issues:
            counts[k] = counts.get(k, 0) + 1
        print("\nAudit: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
        for k, msg in issues:
            if k != "NO-ID":
                print(f"  [{k}] {msg}")
        if counts.get("NO-ID"):
            print(f"  [NO-ID] {counts['NO-ID']} rule chưa có ID — chạy --assign-ids")
    else:
        print("\nAudit: sạch.")

    if not dry_run:
        CORE.write_text(core, encoding="utf-8")
        SCOPE_DIR.mkdir(exist_ok=True)
        for slug, text in scope_texts.items():
            (SCOPE_DIR / f"{slug}.md").write_text(text, encoding="utf-8")
        for stale in SCOPE_DIR.glob("*.md"):   # a scope that lost all its instincts must not linger
            if stale.stem not in scoped:
                stale.unlink()
                print(f"  removed stale instincts-by-scope/{stale.name}")
        print("Updated instincts.md successfully.")
    return 1 if (check and issues) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true", help="exit 1 if any audit issue (LONG/TAG-DUP/BUDGET/ORPHAN/…)")
    ap.add_argument("--stats", action="store_true", help="recurrence of each rule's checks in qa-check-log.csv")
    ap.add_argument("--assign-ids", action="store_true", help="write missing `ID:` fields into the archive")
    ap.add_argument("--show", metavar="ID|TAG|SLUG",
                    help="print only matching archive blocks (ID I105, tag sapo, or article slug) — use instead of reading the archive")
    ap.add_argument("--archive", help="read this archive instead (preview a proposed archive; implies --dry-run)")
    a = ap.parse_args()
    if a.archive:
        ARCHIVE = Path(a.archive)
        a.dry_run = True
    if a.assign_ids:
        sys.exit(assign_ids())
    if a.show:
        sys.exit(show(a.show))
    if a.stats:
        all_ = [i for i in parse_instincts_file(str(ARCHIVE)) if i["status"].upper() == "ACTIVE"]
        sys.exit(stats(all_))
    sys.exit(run(a.max_chars, a.dry_run, a.check))
