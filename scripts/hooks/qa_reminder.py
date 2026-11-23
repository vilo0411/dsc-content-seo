"""Claude Code PostToolUse hook (matcher: Edit|Write|MultiEdit) - remind the QA gate once per file.

After the first edit of an outline / draft / final file in a session, inject one line telling the
model which check to run before presenting it. Later edits of the same file stay silent, so the
reminder costs ~40 tokens per file instead of per edit.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = [
    (re.compile(r"^knowledge/3-seo/content/1-outlines/[^/]+\.md$"),
     "python scripts/outline_lint.py {rel}"),
    (re.compile(r"^knowledge/3-seo/content/(2-drafts|3-finalized)/[^/]+\.md$"),
     "python scripts/qa_gate.py {rel}  (vòng 2: --changed)"),
]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    raw = (data.get("tool_input") or {}).get("file_path") or ""
    if not raw:
        return 0
    path = Path(raw)
    if not path.is_absolute():
        path = Path(data.get("cwd") or ROOT) / path
    try:
        rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    except (ValueError, OSError):
        return 0
    cmd = next((c.format(rel=rel) for pat, c in RULES if pat.match(rel)), None)
    if not cmd:
        return 0

    session = re.sub(r"[^\w-]", "", str(data.get("session_id") or "nosession"))[:64]
    state = Path(tempfile.gettempdir()) / f"dsc-qa-reminder-{session}.txt"
    seen = set(state.read_text(encoding="utf-8").splitlines()) if state.exists() else set()
    if rel in seen:
        return 0
    with state.open("a", encoding="utf-8") as fh:
        fh.write(rel + "\n")

    msg = (f"Đã sửa {rel}. Trước khi trình bày cho user: chạy `{cmd}` (tối đa 2 vòng sửa; "
           f"sửa theo yêu cầu chat thì ghi revision_log.py add trước).")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": msg}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
