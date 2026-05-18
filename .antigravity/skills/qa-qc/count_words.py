#!/usr/bin/env python3
"""Section-level word count auditor for SEO content drafts.

Parses word count targets from outline (Target / Max word count per heading),
counts actual words per matching section in draft, and reports PASS or FAIL.

Usage:  python count_words.py <draft.md> <outline.md>
Exit:   0 = PASS, 1 = FAIL (section under target or over max), 2 = error
"""

import io
import re
import sys
import difflib
from dataclasses import dataclass
from typing import Optional

# Force UTF-8 output on Windows
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


@dataclass
class OutlineSection:
    level: int
    title: str
    target: Optional[int] = None    # minimum word count
    max_words: Optional[int] = None  # maximum word count


@dataclass
class DraftSection:
    level: int
    title: str
    words: int = 0
    body: str = ""


def normalize_title(t: str) -> str:
    return re.sub(r"[^\w\s]", "", t.lower()).strip()


def count_words(text: str) -> int:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # inline links
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)         # images
    text = re.sub(r"```[\s\S]*?```", "", text)               # code blocks
    text = re.sub(r"`[^`]+`", "", text)                      # inline code
    text = re.sub(r"[*_`#>|~\-]", " ", text)                # md syntax
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split()) if text else 0


def parse_outline(content: str) -> list[OutlineSection]:
    """Extract sections that have a Target or Max word count defined."""
    sections: list[OutlineSection] = []
    current: Optional[OutlineSection] = None

    for line in content.split("\n"):
        # Outline headings look like: ### H2: Title  or  #### H3: Title
        m = re.match(r"^(#{2,5})\s+H\d:\s*(.+)", line)
        if m:
            current = OutlineSection(level=len(m.group(1)), title=m.group(2).strip())
            sections.append(current)
            continue

        if current is None:
            continue

        m = re.search(r"\*\*Target:\*\*\s+(\d+)", line)
        if m:
            current.target = int(m.group(1))
            continue

        m = re.search(r"\*\*Max\s+word\s+count:\*\*\s+(\d+)", line)
        if m:
            current.max_words = int(m.group(1))
            continue

    return [s for s in sections if s.target is not None or s.max_words is not None]


def parse_draft(content: str) -> list[DraftSection]:
    """Split draft into sections by heading, count words per section body."""
    # Strip YAML frontmatter
    content = re.sub(r"^---\n[\s\S]*?\n---\n", "", content)

    sections: list[DraftSection] = []
    current: Optional[DraftSection] = None
    body_lines: list[str] = []

    for line in content.split("\n"):
        m = re.match(r"^(#{1,5})\s+(.+)", line)
        if m:
            if current is not None:
                current.body = "\n".join(body_lines)
                current.words = count_words(current.body)
                sections.append(current)
            current = DraftSection(level=len(m.group(1)), title=m.group(2).strip())
            body_lines = []
        else:
            body_lines.append(line)

    if current is not None:
        current.body = "\n".join(body_lines)
        current.words = count_words(current.body)
        sections.append(current)

    return sections


def find_best_match(
    outline_sec: OutlineSection, draft_sections: list[DraftSection]
) -> Optional[DraftSection]:
    """Match outline section to draft section by title similarity."""
    if not draft_sections:
        return None

    o_norm = normalize_title(outline_sec.title)
    best = max(
        draft_sections,
        key=lambda d: difflib.SequenceMatcher(
            None, o_norm, normalize_title(d.title)
        ).ratio(),
    )
    ratio = difflib.SequenceMatcher(
        None, o_norm, normalize_title(best.title)
    ).ratio()
    return best if ratio > 0.3 else None


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python count_words.py <draft.md> <outline.md>", file=sys.stderr)
        sys.exit(2)

    draft_path, outline_path = sys.argv[1], sys.argv[2]

    try:
        with open(draft_path, encoding="utf-8") as f:
            draft_content = f.read()
        with open(outline_path, encoding="utf-8") as f:
            outline_content = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    outline_sections = parse_outline(outline_content)
    draft_sections = parse_draft(draft_content)

    if not outline_sections:
        print("WARNING: No sections with word count targets found in outline.")
        sys.exit(0)

    fail_list: list[tuple[OutlineSection, Optional[DraftSection], int]] = []
    rows: list[tuple[str, int, str, str]] = []

    for o in outline_sections:
        d = find_best_match(o, draft_sections)
        actual = d.words if d else 0
        target_str = str(o.target) if o.target is not None else f"≤{o.max_words}"

        TOLERANCE = 0.10
        if o.target is not None and actual < o.target * (1 - TOLERANCE):
            status = f"FAIL  (thiếu {o.target - actual} từ, floor={int(o.target * (1 - TOLERANCE))})"
            fail_list.append((o, d, actual))
        elif o.max_words is not None and actual > o.max_words * (1 + TOLERANCE):
            status = f"OVER  (vượt {actual - o.max_words} từ, ceil={int(o.max_words * (1 + TOLERANCE))})"
            fail_list.append((o, d, actual))
        else:
            status = "OK"

        rows.append((o.title, actual, target_str, status))

    # ── Report ────────────────────────────────────────────────────────────────
    print("\n=== WORD COUNT AUDIT (per section) ===\n")
    print(f"  {'Section (Outline)':<46} {'Actual':>7}  {'Target':>8}  Status")
    print("  " + "─" * 76)

    for title, actual, target_str, status in rows:
        marker = "[OK]" if status == "OK" else "[!!]"
        short = (title[:43] + "...") if len(title) > 43 else title
        print(f"  {marker} {short:<45} {actual:>7}  {target_str:>8}  {status}")

    total = sum(s.words for s in draft_sections)
    print(f"\n  Tổng số từ toàn bài: {total}")

    if fail_list:
        print("\n=== KẾT QUẢ: FAIL ===\n")
        print("Các section cần bổ sung / rút ngắn:\n")
        for o, d, actual in fail_list:
            t_str = str(o.target) if o.target is not None else f"max {o.max_words}"
            if o.target is not None and actual < o.target:
                diff = o.target - actual
                action = f"Thêm ~{diff} từ"
            else:
                diff = actual - (o.max_words or 0)
                action = f"Rút ngắn ~{diff} từ"
            print(f"  → [{o.title}]")
            print(f"     Hiện tại: {actual} từ | Target: {t_str} | {action}\n")
        print("Chỉ sửa các section trên. Không thay đổi các section đã đạt target.")
        sys.exit(1)
    else:
        print("\n=== KẾT QUẢ: PASS ===")
        sys.exit(0)


if __name__ == "__main__":
    main()
