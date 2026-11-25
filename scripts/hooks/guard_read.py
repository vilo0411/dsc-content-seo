"""Claude Code PreToolUse hook (matcher: Read) - stop full reads of large index files.

Each of these files has a script that answers the question in a few hundred bytes. A full Read
costs 7k-70k tokens and the answer is usually one row. Reads with offset/limit pass through
(needed before an Edit, e.g. /learn adding a rule to instincts-archive.md).

Exit 2 + stderr = block the call and show the message to the model.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# repo-relative path -> what to use instead
GUARDED = {
    "knowledge/3-seo/strategy/pages.csv":
        'python scripts/topic_status.py <slug> | --find "<từ>" | --summary · links: find_links.py "<kw>" · '
        'one row: registry.py show <slug>',
    "knowledge/3-seo/logs/revision-log.md":
        'grep -rn "<slug>" knowledge/3-seo/logs/revision-log*  ·  python scripts/revision_log.py brief',
    ".agents/memory/instincts-archive.md":
        "python scripts/optimize_instincts.py --show <ID|tag|slug>",
    ".agents/skills/link/scripts/sitemap-cache.json":
        'python scripts/find_links.py "<keyword>"',
}
GENERIC_LIMIT = 150_000  # bytes; any other file this big needs grep / offset+limit


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool_input = data.get("tool_input") or {}
    if tool_input.get("offset") or tool_input.get("limit"):
        return 0
    raw = tool_input.get("file_path") or ""
    if not raw:
        return 0
    path = Path(raw)
    if not path.is_absolute():
        path = Path(data.get("cwd") or ROOT) / path
    try:
        rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    except (ValueError, OSError):
        return 0

    if rel in GUARDED or rel.startswith(".agents/memory/archive/"):
        alt = GUARDED.get(rel, "python scripts/optimize_instincts.py --show <ID|tag|slug>")
        size = os.path.getsize(path) // 1024 if path.exists() else 0
        print(f"Blocked full read of {rel} (~{size} KB). Use instead: {alt}. "
              f"Need to edit it? grep -n the spot, then Read with offset/limit.", file=sys.stderr)
        return 2
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ipynb"} \
            and path.exists() and path.stat().st_size > GENERIC_LIMIT:
        print(f"Blocked full read of {rel} ({path.stat().st_size // 1024} KB > "
              f"{GENERIC_LIMIT // 1000} KB). Use grep -n to find the part you need, then Read with "
              f"offset/limit, or a script from AGENTS.md §5.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
