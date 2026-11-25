#!/usr/bin/env python3
"""Redact Google API keys from crawled snapshots; check tracked files before publishing.

Usage: python3 scripts/snapshot_security.py --check
The check reports paths only, never credential values.
"""
import argparse
from pathlib import Path
import re
import subprocess


GOOGLE_API_KEY = re.compile(r"AIza[0-9A-Za-z_-]{35}")
REDACTED = "[REDACTED_GOOGLE_API_KEY]"


def redact_google_api_keys(text: str) -> str:
    return GOOGLE_API_KEY.sub(REDACTED, text)


def check_tracked_files(root: Path) -> int:
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).split(b"\0")
    found = []
    for raw in paths:
        if not raw:
            continue
        path = Path(raw.decode("utf-8"))
        file = root / path
        if not file.is_file() or file.is_symlink():
            continue
        if GOOGLE_API_KEY.search(file.read_bytes().decode("utf-8", "replace")):
            found.append(path)
    for path in found:
        print(f"Google API key detected: {path}")
    if not found:
        print("No Google API keys found in tracked files.")
    return int(bool(found))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    raise SystemExit(check_tracked_files(Path(__file__).resolve().parents[1]))
