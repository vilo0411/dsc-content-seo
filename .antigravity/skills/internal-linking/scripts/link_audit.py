#!/usr/bin/env python3
"""Internal-link audit across finalized articles.

Builds an in/out link matrix for knowledge/4-content/3-finalized/*.md using the
absolute https://www.dsc.com.vn/kien-thuc/<slug> URLs found in each article, classifies
inbound anchors against anchor-index.md (Exact / Partial / Generic) and writes
knowledge/3-pipeline/internal-link-dashboard.md.

Usage:  python .antigravity/skills/internal-linking/scripts/link_audit.py [--orphans]
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[4]
CONTENT_DIR = ROOT / "knowledge/4-content/3-finalized"
OUTPUT_FILE = ROOT / "knowledge/3-pipeline/internal-link-dashboard.md"
INDEX_FILE = ROOT / "knowledge/3-pipeline/anchor-index.md"

KB_URL = re.compile(r"\[([^\]]+)\]\((https://www\.dsc\.com\.vn/kien-thuc/([^)\s/?#]+))[^)]*\)")


def get_anchor_index() -> dict[str, dict]:
    """slug -> {exact: anchor text, partial: [related keywords]}"""
    index: dict[str, dict] = {}
    if not INDEX_FILE.exists():
        return index
    for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[1].startswith("http"):
            continue
        slug = cells[1].rstrip("/").rsplit("/", 1)[-1]
        index[slug] = {"exact": cells[0].lower(),
                       "partial": [p.strip().lower() for p in cells[2].split(",") if p.strip()]}
    return index


def classify_anchor(anchor: str, slug: str, index: dict) -> str:
    a = anchor.lower().strip()
    entry = index.get(slug, {})
    if a == entry.get("exact", ""):
        return "Exact"
    if any(a == p or a in p for p in entry.get("partial", [])):
        return "Partial"
    return "Generic"


def article_slug(path: Path, text: str) -> str:
    m = re.search(r"^Slug:\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip().strip("/")
    return re.sub(r"^(Final|Draft|Optimize)-", "", path.stem)


def audit(show_orphans: bool) -> None:
    index = get_anchor_index()
    if not CONTENT_DIR.exists():
        print(f"Content directory not found: {CONTENT_DIR}")
        return
    data: dict[str, dict] = {}
    for path in sorted(CONTENT_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        src = article_slug(path, text)
        data.setdefault(src, {"file": path.name, "out": [], "in": []})
        for anchor, url, dest in KB_URL.findall(text):
            if dest == src:
                continue
            data[src]["out"].append((anchor, dest))
            data.setdefault(dest, {"file": "", "out": [], "in": []})["in"].append((anchor, src))

    rows, orphans = [], []
    for slug in sorted(data):
        st = data[slug]
        if not st["file"]:
            continue  # link target that isn't a local finalized article (live-only URL)
        n_in, n_out = len(st["in"]), len(st["out"])
        kinds = [classify_anchor(a, slug, index) for a, _ in st["in"]]
        ex, pa = kinds.count("Exact"), kinds.count("Partial")
        ge = n_in - ex - pa
        dist = f"{ex}/{pa}/{ge}"
        if n_in == 0:
            health, orphans = "🔴 Orphan", orphans + [slug]
        elif n_in and ex / n_in > 0.6:
            health = "🟠 Over-exact"
        elif n_out < 3:
            health = "🟡 Few out-links"
        else:
            health = "🟢 OK"
        rows.append(f"| {slug} | {n_out} | {n_in} | {dist} | {health} |")

    report = ["# Internal Linking Dashboard",
              f"> Updated: {datetime.now():%Y-%m-%d %H:%M:%S} · {len(rows)} bài · {len(orphans)} orphan",
              "> Chỉ tính link giữa các file trong `3-finalized/` — inbound từ bài live cũ (không có file local) không được đếm.",
              "", "| Slug | Out | In | Anchor (Exact/Partial/Generic) | Health |", "| :--- | :---: | :---: | :--- | :--- |"]
    report += rows
    if orphans:
        report += ["", "## Orphan pages (0 inbound) — ưu tiên backfill", ""]
        report += [f"- `{s}` → `python scripts/find_links.py --backfill {s}`" for s in orphans]
    OUTPUT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Dashboard written: {OUTPUT_FILE} ({len(rows)} bài, {len(orphans)} orphan)")
    if show_orphans:
        print("\n".join(orphans))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orphans", action="store_true", help="Also print orphan slugs to stdout")
    audit(ap.parse_args().orphans)
