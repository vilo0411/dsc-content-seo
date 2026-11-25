#!/usr/bin/env python3
"""Shared helpers for DSC pipeline scripts. Import only — do not run directly.

    from _common import ROOT, setup_utf8, unaccent, split_frontmatter, read_text, write_text
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Canonical project paths (single place to change if the layout moves)
CONTENT = ROOT / "knowledge/3-seo/content"
SOURCES_DIR = CONTENT / "0-sources"
OUTLINES_DIR = CONTENT / "1-outlines"
PROPOSALS_DIR = CONTENT / "1-outlines"  # Proposal-*.md live next to outlines (1-proposals/ merged 2026-11-03)
DRAFTS_DIR = CONTENT / "2-drafts"
FINAL_DIR = CONTENT / "3-finalized"
STRATEGY_DIR = ROOT / "knowledge/3-seo/strategy"
REGISTRY = STRATEGY_DIR / "pages.csv"  # one row per article URL (scripts/registry.py)
BACKLOG_FILE = STRATEGY_DIR / "sprint-backlog.md"
BRAND_DIR = ROOT / "knowledge/1-brand"
PIPELINE_DIR = ROOT / "knowledge/3-seo"  # all SEO: strategy/ content/ links/ logs/ (2026-11-19)
LOGS_DIR = PIPELINE_DIR / "logs"
REVISION_LOG = LOGS_DIR / "revision-log.md"
ANTI_AI_RULES = BRAND_DIR / "anti-ai-rules.md"
BLACKLIST_FILE = BRAND_DIR / "anti-ai-rules-blacklist.md"
GLOSSARY_FILE = BRAND_DIR / "glossary.md"
SITEMAP_CACHE = ROOT / ".agents/skills/link/scripts/sitemap-cache.json"
WORDCOUNT_DIR = ROOT / "scripts"
MEMORY_DIR = ROOT / ".agents/memory"

HOST = "https://www.dsc.com.vn"
OPEN_ACCOUNT_URL = f"{HOST}/mo-tai-khoan"


def setup_utf8() -> None:
    """Force UTF-8 on stdout/stderr (Windows consoles default to cp1252)."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def unaccent(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def slugify(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", unaccent(s))).strip("-")


def slug_from_path(p: Path | str) -> str:
    stem = Path(p).stem
    return re.sub(r"^(Final|Draft|Outline|Optimize|Proposal|Raw)-", "", stem)


def read_text(p: Path) -> tuple[str, str]:
    """Return (text with LF endings, original newline) so writers can preserve CRLF/LF."""
    raw = p.read_bytes()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8-sig").replace("\r\n", "\n"), nl  # utf-8-sig: legacy Finals carry a BOM


def write_text(p: Path, text: str, nl: str = "\n") -> None:
    p.write_bytes(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))


def split_frontmatter(text: str) -> tuple[dict, int, list[str]]:
    """Return (frontmatter dict, body_start_line_index, all_lines). Nested YAML values are kept raw."""
    lines = text.split("\n")
    fm: dict[str, str] = {}
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return fm, i + 1, lines
            m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", lines[i])
            if m:
                fm[m.group(1)] = m.group(2).strip()
    return fm, 0, lines


WORK_PREFIXES = ("Proposal-", "Optimize-", "Draft-", "")   # working files of one article (outline has no prefix)
DATE_FIELDS = ("Created", "Updated")                          # YYYY-MM-DD in the YAML of outline / proposal / draft


def working_files(slug: str) -> list[Path]:
    """Outline / Proposal / Draft / Optimize files of one article that are still in the working folders."""
    out = []
    for folder in (OUTLINES_DIR, DRAFTS_DIR):
        for prefix in WORK_PREFIXES:
            p = folder / f"{prefix}{slug}.md"
            if p.exists() and p not in out:
                out.append(p)
    return out


def stamp_frontmatter(p: Path, keep_mtime: bool = False, **fields: str) -> None:
    """Set top-level YAML keys (adds the `---` block if the file has none). Other lines stay untouched.
    keep_mtime: restore the file time (backfills must not look like edits to gate detection)."""
    import os
    st = p.stat()
    text, nl = read_text(p)
    lines = text.split("\n")
    # YAML block: leading `---` … `---`, or the old template's ```yaml / --- … --- / ``` fenced after the title
    start = 0 if lines and lines[0].strip() == "---" else next(
        (i + 1 for i in range(len(lines) - 1) if re.match(r"^```ya?ml\s*$", lines[i]) and lines[i + 1].strip() == "---"), None)
    if start is not None and "---" in (l.strip() for l in lines[start + 1:]):
        end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "---")
        for key, val in fields.items():
            hit = next((i for i in range(start + 1, end) if re.match(rf"^{key}\s*:", lines[i])), None)
            if hit is not None:
                lines[hit] = f"{key}: {val}"
            else:
                lines.insert(end, f"{key}: {val}")
                end += 1
    else:
        lines = ["---", *(f"{k}: {v}" for k, v in fields.items()), "---", ""] + lines
    write_text(p, "\n".join(lines), nl)
    if keep_mtime:
        os.utime(p, (st.st_atime, st.st_mtime))


def body_end(lines: list[str], start: int = 0) -> int:
    """Index of the Revision Log heading (content after it is not article body), or len(lines)."""
    for i in range(start, len(lines)):
        if re.match(r"^##\s+\**\s*(Revision Log|Nhật ký chỉnh sửa)", lines[i].strip(), re.I):
            return i
    return len(lines)
