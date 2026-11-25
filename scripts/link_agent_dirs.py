"""Expose .agents/skills to agents that look elsewhere (Claude Code reads .claude/skills).

Run once after cloning:  python scripts/link_agent_dirs.py
Windows: directory junction (no admin rights needed). macOS/Linux: symlink.
Falls back to copying when a link cannot be created (re-run after editing skills).
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
TARGETS = [ROOT / ".claude" / "skills"]


def is_link_to(path: Path, src: Path) -> bool:
    try:
        return path.exists() and path.resolve() == src.resolve() and path.resolve() != path.absolute()
    except OSError:
        return False


def make_link(dst: Path, src: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)], capture_output=True, text=True)
        if r.returncode == 0:
            return "junction"
    else:
        try:
            dst.symlink_to(os.path.relpath(src, dst.parent), target_is_directory=True)
            return "symlink"
        except OSError:
            pass
    shutil.copytree(src, dst)
    return "copy"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="replace an existing non-link directory (e.g. an old copy)")
    args = ap.parse_args()

    for dst in TARGETS:
        rel = dst.relative_to(ROOT).as_posix()
        if is_link_to(dst, SOURCE):
            print(f"ok      {rel} -> .agents/skills")
            continue
        if dst.exists():
            if not args.force:
                print(f"skip    {rel} exists and is not a link (use --force to replace)")
                continue
            shutil.rmtree(dst)
        kind = make_link(dst, SOURCE)
        print(f"{kind:<7} {rel} -> .agents/skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
