"""Claude Code hooks for the shared activity log (knowledge/logs/activity/).

PostToolUse (matcher: Write|Edit|MultiEdit)  →  python scripts/hooks/activity_hook.py
    Safety net for skills that write output files by hand (social, ads, email, landing, analytics, market…):
    - a NEW file in a tracked output folder → one "create" event
    - the first edit of an existing tracked file in a session → one "revise" event
    Skipped when the same path was logged in the last 10 minutes (the skill's own `activity_log.py add`).

Stop  →  python scripts/hooks/activity_hook.py --stop
    If the activity log is newer than knowledge/0-dashboard/index.html, rebuild the dashboard
    (build_content_index.py) so it always shows the latest work without a manual step.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

SKIP = re.compile(r"(/creatives/v\d+/|/assets/|/archive/|README\.md$|\.(png|jpe?g|webp|gif|svg)$)", re.I)


def on_write(data: dict) -> int:
    import activity_log as al
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
    hit = al.classify(path)
    if not hit or SKIP.search(rel):
        return 0
    resp = data.get("tool_response") or {}
    created = data.get("tool_name") == "Write" and (resp.get("type") == "create" if isinstance(resp, dict) and resp.get("type")
                                                     else not any(e.get("path") == rel for e in al.read_events(days=90)))
    if not created:
        # one "revise" per file per session — edits come in bursts
        session = re.sub(r"[^\w-]", "", str(data.get("session_id") or "nosession"))[:64]
        state = Path(tempfile.gettempdir()) / f"dsc-activity-{session}.txt"
        seen = set(state.read_text(encoding="utf-8").splitlines()) if state.exists() else set()
        if rel in seen:
            return 0
        with state.open("a", encoding="utf-8") as fh:
            fh.write(rel + "\n")
    if al.recent_has(path, minutes=10):
        return 0
    dom, target = hit
    al.emit(dom, "create" if created else "revise", target, path=path, skill="hook", src="hook")
    return 0


def on_stop() -> int:
    import activity_log as al
    logs = list(al.ACTIVITY_DIR.glob("*.jsonl")) if al.ACTIVITY_DIR.is_dir() else []
    index = ROOT / "knowledge/0-dashboard/index.html"
    if not logs or (index.exists() and index.stat().st_mtime >= max(f.stat().st_mtime for f in logs)):
        return 0
    # ~15 s: run detached so the session does not wait for the dashboard
    flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP) if sys.platform == "win32" else 0
    subprocess.Popen([sys.executable, str(ROOT / "scripts/build_content_index.py")], cwd=ROOT,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     creationflags=flags, start_new_session=sys.platform != "win32")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        if "--stop" in sys.argv:
            return on_stop()
        try:
            data = json.load(sys.stdin)
        except (json.JSONDecodeError, ValueError):
            return 0
        return on_write(data)
    except Exception:
        return 0  # a logging hook must never block the session


if __name__ == "__main__":
    sys.exit(main())
