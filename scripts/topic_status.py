#!/usr/bin/env python3
"""Read or update one article's status in topic-clusters.md without loading the file into the LLM.

Usage:
  python scripts/topic_status.py <slug>                    → print the matching row(s)
  python scripts/topic_status.py <slug> --set "In Progress" → update the Trạng thái cell of that row
  python scripts/topic_status.py --find "từ khóa"           → search rows by keyword text
  python scripts/topic_status.py --list Optimizing          → list rows with a given status

Slug is matched against the URL column (`/kien-thuc/<slug>/`). Exactly one row must match for --set.
Statuses used in the pipeline: Planned · In Progress · Outline-Approved · Optimizing · Finalized
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
TOPIC_FILE = ROOT / "knowledge/4-content/topic-clusters.md"
VALID_STATUS = {"Planned", "In Progress", "Outline-Approved", "Optimizing", "Finalized"}


def unaccent(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def parse_rows(lines: list[str]):
    """Yield (line_index, cluster, url_slug, keyword, status, cells) for each data row."""
    cluster = ""
    for i, line in enumerate(lines):
        if line.startswith("## "):
            cluster = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0].startswith("URL") or set(cells[0]) <= set(":- "):
            continue
        url_cell = cells[0]
        m = re.search(r"/kien-thuc/([^/\)\]`\s]+)", url_cell)
        slug = m.group(1) if m else url_cell.strip("`")
        yield i, cluster, slug, cells[1], cells[-1], cells


def fmt(cluster, slug, keyword, status):
    return f"| {slug} | {keyword} | {status} | {cluster} |"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--set", metavar="STATUS", help="New status for the matched row")
    ap.add_argument("--find", metavar="TEXT", help="Search keyword column (accent-insensitive)")
    ap.add_argument("--list", metavar="STATUS", help="List all rows with this status")
    args = ap.parse_args()

    if not TOPIC_FILE.exists():
        print(f"Không tìm thấy {TOPIC_FILE}", file=sys.stderr)
        sys.exit(2)
    raw = TOPIC_FILE.read_bytes()
    nl = "\r\n" if b"\r\n" in raw else "\n"  # preserve the file's line endings on write
    text = raw.decode("utf-8")
    lines = text.split(nl)
    rows = list(parse_rows(lines))

    if args.list:
        hits = [r for r in rows if r[4].lower() == args.list.lower()]
        print(f"# {len(hits)} bài ở trạng thái {args.list}\n\n| Slug | Keyword | Trạng thái | Cluster |\n|---|---|---|---|")
        for _, cl, slug, kw, st, _ in hits:
            print(fmt(cl, slug, kw, st))
        return

    if args.find:
        q = unaccent(args.find)
        hits = [r for r in rows if q in unaccent(r[3]) or q in unaccent(r[2])]
        print(f"# {len(hits)} dòng khớp “{args.find}”\n\n| Slug | Keyword | Trạng thái | Cluster |\n|---|---|---|---|")
        for _, cl, slug, kw, st, _ in hits[:20]:
            print(fmt(cl, slug, kw, st))
        return

    if not args.slug:
        ap.error("cần <slug>, --find hoặc --list")

    slug = args.slug.strip("/").split("/")[-1]
    hits = [r for r in rows if r[2] == slug]
    if not hits:
        # fallback: substring match on slug
        hits = [r for r in rows if slug in r[2]]
    if not hits:
        print(f"Không có dòng nào cho slug '{slug}' trong topic-clusters.md. "
              f"Thêm dòng mới vào cluster phù hợp trước khi đổi trạng thái.", file=sys.stderr)
        sys.exit(1)

    if args.set is None:
        print("| Slug | Keyword | Trạng thái | Cluster |\n|---|---|---|---|")
        for _, cl, s, kw, st, _ in hits:
            print(fmt(cl, s, kw, st))
        return

    if len(hits) > 1:
        print(f"{len(hits)} dòng khớp '{slug}' — không thể --set. Dùng slug đầy đủ:", file=sys.stderr)
        for _, cl, s, kw, st, _ in hits:
            print(f"  {s}  ({st})", file=sys.stderr)
        sys.exit(1)

    new_status = args.set.strip()
    if new_status not in VALID_STATUS:
        print(f"Cảnh báo: '{new_status}' không nằm trong {sorted(VALID_STATUS)} — vẫn ghi.", file=sys.stderr)

    idx, cl, s, kw, old, cells = hits[0]
    if old == new_status:
        print(f"Không đổi: {s} đã ở trạng thái {old}")
        return
    line = lines[idx]
    # Replace only the last cell content, preserving original spacing style
    new_line = re.sub(r"\|\s*" + re.escape(old) + r"\s*\|\s*$", f"| {new_status} |", line)
    if new_line == line:
        print("Không thay được ô trạng thái (format dòng không chuẩn):\n" + line, file=sys.stderr)
        sys.exit(1)
    lines[idx] = new_line
    TOPIC_FILE.write_bytes(nl.join(lines).encode("utf-8"))
    print(f"Đã cập nhật {s}: {old} → {new_status} (dòng {idx + 1}, {cl})")


if __name__ == "__main__":
    main()
