#!/usr/bin/env python3
"""One-command QA gate for a draft: tầng A (qa_lint) → tầng B (slop_check) → tầng dữ liệu (market_facts --verify).

    python scripts/qa_gate.py <Draft-slug.md> [--cta] [--fix] [--all] [--no-facts]
    python scripts/qa_gate.py <Draft-slug.md> --changed      # đoạn đã sửa kể từ lần Quality Guardian duyệt trước
    python scripts/qa_gate.py <Draft-slug.md> --mark-qg      # lưu mốc sau khi Quality Guardian duyệt

Why: the three scripts print long reports; the agent re-reads all of them every QA round. This prints
one line per tier + only CRITICAL/MAJOR findings (MINOR counted), stops at the first failing blocking
tier (fix that tier, re-run — earlier tiers are cheap and re-checked automatically), and lets Quality
Guardian round 2 review only the changed paragraphs (`--changed`) instead of the whole article.
Outline is found automatically: 1-outlines/<slug>.md, else knowledge/4-content/archive/<slug>/outline.md.
Exit 0 = all blocking tiers PASS.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CONTENT = ROOT / "knowledge/4-content"
MAX_SHOWN = 12
BLOCKING = ("CRITICAL", "MAJOR")


def slug_of(path: Path) -> str:
    return re.sub(r"^(Final|Draft|Optimize)-", "", path.stem)


def find_outline(slug: str) -> Path | None:
    for p in (CONTENT / "1-outlines" / f"{slug}.md", CONTENT / "1-outlines" / f"Proposal-{slug}.md",
              CONTENT / "2-drafts" / f"Proposal-{slug}.md", CONTENT / "archive" / slug / "outline.md"):
        if p.exists():
            return p
    return None


def run_json(args: list[str], timeout: int = 180) -> tuple[int, dict | None, str]:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        r = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return 3, None, "timeout"
    try:
        return r.returncode, json.loads(r.stdout), r.stderr.strip()
    except json.JSONDecodeError:
        return r.returncode, None, (r.stderr or r.stdout).strip()[-300:]


def show(findings: list[dict]) -> None:
    hard = sorted((f for f in findings if f.get("severity") in BLOCKING),
                  key=lambda f: (f["severity"] != "CRITICAL", f.get("line") or 0))
    minor = len(findings) - len(hard)
    for f in hard[:MAX_SHOWN]:
        line = f"L{f['line']} " if f.get("line") else ""
        ex = f" — “{f['excerpt'][:80]}”" if f.get("excerpt") else ""
        print(f"    [{f['severity']}] {f['check']} {line}{f['message']}{ex}")
    if len(hard) > MAX_SHOWN:
        print(f"    … +{len(hard) - MAX_SHOWN} lỗi CRITICAL/MAJOR nữa (chạy script riêng để xem đủ)")
    if minor:
        print(f"    ({minor} MINOR — không chặn)")


def tier_lint(draft: Path, outline: Path | None, cta: bool, fix: bool, original: str | None = None) -> bool:
    args = [str(SCRIPTS / "qa_lint.py"), str(draft), "--json"]
    if outline:
        args += ["--outline", str(outline)]
    if cta:
        args.append("--cta")
    if fix:
        args.append("--fix")
    if original:
        args += ["--original", original]
    code, d, err = run_json(args)
    if d is None:
        print(f"A · qa_lint: LỖI CHẠY ({err})")
        return False
    cats, st = d.get("categories", {}), d.get("stats", {})
    print(f"A · qa_lint: {'PASS' if d['pass'] else 'FAIL'} · score {d['score']}"
          f" · coverage {cats.get('coverage', '-')} · trust {cats.get('trust', '-')}"
          + (f" · auto-fix: {'; '.join(d['fixes'])}" if d.get("fixes") else ""))
    # Substance at a glance: what the form score cannot show.
    facts = [f"{label} {st[key]}" for key, label in (("entity_coverage", "thuật ngữ đối thủ"), ("information_gain", "information gain"),
                                                    ("source_links", "link nguồn gốc"), ("h2_answer_first", "H2 trả lời ngay"))
             if key in st]
    if facts:
        print("    " + " · ".join(facts))
    if not outline:
        print("    ⚠ Không có outline: Information_Gain / PAA / word count KHÔNG được kiểm. "
              "Outline phải nằm ở 1-outlines/ hoặc archive/<slug>/outline.md.")
    show(d["findings"])
    return bool(d["pass"])


def tier_slop(draft: Path) -> bool:
    code, d, err = run_json([str(SCRIPTS / "slop_check.py"), str(draft), "--json"])
    if d is None:
        print(f"B · slop_check: LỖI CHẠY ({err})")
        return False
    print(f"B · slop_check: {'PASS' if d['pass'] else 'FAIL'} · score {d['slop_score']} (≥ 80) · mode {d.get('mode')}")
    show(d["findings"])
    if not d["pass"]:
        print("    Cách sửa từng SLOP-*: knowledge/3-pipeline/anti-ai-rules.md §8.7 — sửa đúng chỗ báo, không viết lại cả bài.")
    return bool(d["pass"])


def tier_facts(draft: Path) -> bool:
    code, d, err = run_json([str(SCRIPTS / "market_facts.py"), "--verify", str(draft), "--json"], timeout=120)
    if code == 3 or d is None:
        print(f"F · market_facts: BỎ QUA (nguồn dữ liệu không truy cập được — không chặn) {err[:120]}")
        return True
    hard = [f for f in d["findings"] if f.get("severity") in BLOCKING]
    print(f"F · market_facts: {'FAIL' if hard else 'PASS'}"
          + (f" · cảnh báo nguồn: {'; '.join(d['soft_errors'])[:150]}" if d.get("soft_errors") else ""))
    show(d["findings"])
    return not hard


# ─────────────────────────── Quality Guardian snapshot ───────────────────────────

def qg_path(slug: str) -> Path:
    return CONTENT / "archive" / slug / "qg.md"


def blocks(text: str) -> list[str]:
    text = re.sub(r"^---\n[\s\S]*?\n---\n", "", text.replace("\r\n", "\n"))
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]


def changed(draft: Path) -> int:
    base = qg_path(slug_of(draft))
    if not base.exists():
        print("Chưa có mốc Quality Guardian (`--mark-qg`) — vòng này QG đọc cả bài.")
        return 1
    old, new = blocks(base.read_text(encoding="utf-8")), blocks(draft.read_text(encoding="utf-8"))
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    lines = draft.read_text(encoding="utf-8").split("\n")
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for b in new[j1:j2]:
            first = b.split("\n", 1)[0]
            ln = next((k + 1 for k, l in enumerate(lines) if l.strip() == first.strip()), "?")
            # the heading the block sits under gives QG enough context without re-reading the article
            head = next((lines[k] for k in range(int(ln) - 2, -1, -1) if lines[k].startswith("#")), "") if ln != "?" else ""
            print(f"## L{ln} · dưới “{head.lstrip('# ').strip()[:70]}”\n{b}\n")
            n += 1
        if tag == "delete":
            print(f"## đã xoá {i2 - i1} đoạn: “{old[i1][:80]}…”\n")
            n += 1
    print(f"— {n} cụm thay đổi kể từ lần QG trước.")
    return 0


def mark_qg(draft: Path) -> int:
    dest = qg_path(slug_of(draft))
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(draft, dest)
    print(f"Đã lưu mốc QG: {dest.relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--outline", help="mặc định tự tìm theo slug")
    ap.add_argument("--cta", action="store_true", help="bật check CTA-* của qa_lint")
    ap.add_argument("--fix", action="store_true", help="qa_lint --fix (sửa an toàn, idempotent)")
    ap.add_argument("--original", help="Final-<slug>.md gốc (bài /optimize) — qa_lint kiểm bảo toàn ảnh")
    ap.add_argument("--all", action="store_true", help="chạy đủ 3 tầng kể cả khi tầng trước FAIL")
    ap.add_argument("--no-facts", action="store_true")
    ap.add_argument("--changed", action="store_true")
    ap.add_argument("--mark-qg", action="store_true")
    a = ap.parse_args()
    draft = Path(a.draft)
    if not draft.exists():
        print(f"Không thấy {draft}")
        return 2
    if a.changed:
        return changed(draft)
    if a.mark_qg:
        return mark_qg(draft)
    outline = Path(a.outline) if a.outline else find_outline(slug_of(draft))
    print(f"# QA gate · {draft.name} · outline: {outline.relative_to(ROOT) if outline else '(không có)'}")
    ok = tier_lint(draft, outline, a.cta, a.fix, a.original)
    if ok or a.all:
        ok = tier_slop(draft) and ok
    if (ok or a.all) and not a.no_facts:
        ok = tier_facts(draft) and ok
    print("→ PASS: chuyển tầng C (Quality Guardian)" if ok else
          "→ FAIL: sửa đúng các dòng trên rồi chạy lại lệnh này (tối đa 2 vòng)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
