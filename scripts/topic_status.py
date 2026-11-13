#!/usr/bin/env python3
"""Read or update one article's status in topic-clusters.md without loading the file into the LLM.

Usage:
  python scripts/topic_status.py <slug>                    → print the matching row(s)
  python scripts/topic_status.py <slug> --set "In Progress" → update the Trạng thái cell of that row
  python scripts/topic_status.py --find "từ khóa"           → search rows by keyword text
  python scripts/topic_status.py --list Optimizing          → list rows with a given status
  python scripts/topic_status.py --summary                  → counts per cluster + rows not Finalized (/keyword-plan)
  python scripts/topic_status.py <slug> --add --keyword "từ khóa" --cluster "tên cluster" [--set Outlining]
                                                            → append a new row to that cluster (no file read by the LLM)

Slug is matched against the URL column (`/kien-thuc/<slug>/`). Exactly one row must match for --set.
Statuses used in the pipeline: Planned · Outlining · Outline-Approved · Optimizing · Finalized
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
VALID_STATUS = {"Planned", "Outlining", "In Progress", "Outline-Approved", "Optimizing", "Finalized"}


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
    ap.add_argument("--summary", action="store_true",
                    help="Counts per cluster × status + every row not yet Finalized (input for /keyword-plan)")
    ap.add_argument("--add", action="store_true", help="Append a new row for <slug> (needs --keyword and --cluster)")
    ap.add_argument("--keyword", help="Keyword / topic text for --add")
    ap.add_argument("--cluster", help="Cluster heading to add under (accent-insensitive substring) for --add")
    args = ap.parse_args()

    if not TOPIC_FILE.exists():
        print(f"Không tìm thấy {TOPIC_FILE}", file=sys.stderr)
        sys.exit(2)
    raw = TOPIC_FILE.read_bytes()
    nl = "\r\n" if b"\r\n" in raw else "\n"  # preserve the file's line endings on write
    text = raw.decode("utf-8")
    lines = text.split(nl)
    rows = list(parse_rows(lines))

    if args.summary:
        statuses = sorted({r[4] for r in rows}, key=lambda s: (s != "Finalized", s))
        per: dict[str, dict[str, int]] = {}
        for _, cl, _, _, st, _ in rows:
            per.setdefault(cl, {}).setdefault(st, 0)
            per[cl][st] += 1
        print(f"# {len(rows)} bài · {len(per)} cluster\n")
        print("| Cluster | " + " | ".join(statuses) + " |\n|---|" + "---|" * len(statuses))
        for cl, cnt in per.items():
            print(f"| {cl} | " + " | ".join(str(cnt.get(s, 0)) for s in statuses) + " |")
        todo = [r for r in rows if r[4] != "Finalized"]
        print(f"\n## {len(todo)} bài chưa Finalized (cột Volume nếu có)\n\n| Slug | Keyword | Volume | Trạng thái | Cluster |\n|---|---|---|---|---|")
        for _, cl, slug, kw, st, cells in todo:
            vol = cells[2] if len(cells) >= 4 else "-"
            print(f"| {slug} | {kw} | {vol} | {st} | {cl} |")
        return

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
    if args.add:
        if any(r[2] == slug for r in rows):
            print(f"Đã có dòng cho '{slug}' — dùng --set để đổi trạng thái.", file=sys.stderr)
            sys.exit(1)
        if not args.keyword or not args.cluster:
            ap.error("--add cần --keyword và --cluster")
        heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
        match = [(i, h) for i, h in heads if unaccent(args.cluster) in unaccent(h)]
        if len(match) != 1:
            print(f"--cluster '{args.cluster}' khớp {len(match)} cluster. Các cluster hiện có:", file=sys.stderr)
            for _, h in heads:
                print("  " + h, file=sys.stderr)
            sys.exit(1)
        head_idx = match[0][0]
        in_cluster = [r[0] for r in rows if head_idx < r[0] and not any(head_idx < i <= r[0] for i, _ in heads if i != head_idx)]
        if not in_cluster:
            print(f"Cluster '{match[0][1]}' chưa có bảng — thêm tay 1 lần.", file=sys.stderr)
            sys.exit(1)
        status = (args.set or "Planned").strip()
        lines.insert(max(in_cluster) + 1, f"| `/kien-thuc/{slug}/` | {args.keyword} | - | {status} |")
        TOPIC_FILE.write_bytes(nl.join(lines).encode("utf-8"))
        print(f"Đã thêm: {slug} · {args.keyword} · {status} · {match[0][1]}")
        return
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
