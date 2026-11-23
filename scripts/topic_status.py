"""Read or update one article's pipeline status in the registry (strategy/pages.csv) without the LLM opening it.

Usage:
  python scripts/topic_status.py <slug>                    → print the matching row(s) (live slug or file slug)
  python scripts/topic_status.py <slug> --set "Outlining"  → update its status
  python scripts/topic_status.py --find "từ khóa"           → search main/secondary keywords, anchor, title
  python scripts/topic_status.py --list Optimizing          → list rows with a given status
  python scripts/topic_status.py --summary                  → cluster × status counts + every row in progress (/keyword-plan)
  python scripts/topic_status.py <slug> --add --keyword "từ khóa" --cluster "3b | tên nhóm" [--set Planned]
                                                            → add a planned article (cluster omitted → auto-classified)

Statuses: Planned · Outlining · Outline-Approved · Optimizing · Finalized · Merged · Live (published, never in this pipeline)
Registry module and columns: scripts/registry.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry  # noqa: E402
from _common import setup_utf8, unaccent  # noqa: E402

IN_PROGRESS = {"Planned", "Outlining", "Outline-Pending", "In Progress", "Outline-Approved", "Optimizing"}


def cl_label(r: dict) -> str:
    return f"{r['subgroup'] or r['cluster']} {r['subgroup_name'] or r['cluster_name']}".strip()


def table(rows: list[dict]) -> None:
    print("| Slug | File slug | Keyword | Trạng thái | Live | Cluster |\n|---|---|---|---|---|---|")
    for r in rows:
        fs = r["file_slug"] if r["file_slug"] and r["file_slug"] != r["slug"] else ""
        print(f"| {r['slug']} | {fs} | {r['key_chinh'] or r['anchor']} | {r['status']} | {r['live']} | {cl_label(r)} |")


def main() -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--set", metavar="STATUS", help="New status for the matched row")
    ap.add_argument("--find", metavar="TEXT", help="Search keywords / anchor / title (accent-insensitive)")
    ap.add_argument("--list", metavar="STATUS", help="List all rows with this status")
    ap.add_argument("--summary", action="store_true", help="Cluster × status counts + rows in progress")
    ap.add_argument("--add", action="store_true", help="Add a planned article <slug> (needs --keyword)")
    ap.add_argument("--keyword", help="Main keyword for --add")
    ap.add_argument("--cluster", help="Subgroup code (3b) or cluster/subgroup name for --add; omitted = auto")
    args = ap.parse_args()
    rows = registry.load()

    if args.summary:
        statuses = [s for s in registry.STATUSES if any(r["status"] == s for r in rows)]
        per: dict[str, dict[str, int]] = {}
        for r in rows:
            key = f"{r['cluster']} {r['cluster_name']}".strip() or "(chưa có cluster)"
            per.setdefault(key, {}).setdefault(r["status"], 0)
            per[key][r["status"]] += 1
        print(f"# {len(rows)} bài · {len(per)} cluster (Live = bài cũ chưa qua pipeline)\n")
        print("| Cluster | " + " | ".join(statuses) + " |\n|---|" + "---|" * len(statuses))
        for key in sorted(per, key=lambda k: registry._cluster_key(k.split(" ")[0])):
            print(f"| {key} | " + " | ".join(str(per[key].get(s, 0)) for s in statuses) + " |")
        todo = [r for r in rows if r["status"] in IN_PROGRESS]
        print(f"\n## {len(todo)} bài đang làm\n")
        table(todo)
        return 0

    if args.list:
        hits = [r for r in rows if r["status"].lower() == args.list.lower()]
        print(f"# {len(hits)} bài ở trạng thái {args.list}\n")
        table(hits)
        return 0

    if args.find:
        words = unaccent(args.find).split()
        def hay(r):
            return set(unaccent(registry.terms(r)).replace("|", " ").split()) | set(r["slug"].split("-"))
        hits = [r for r in rows if all(w in hay(r) for w in words)]
        print(f"# {len(hits)} dòng khớp “{args.find}”\n")
        table(hits[:20])
        return 0

    if not args.slug:
        ap.error("cần <slug>, --find, --list hoặc --summary")
    slug = args.slug.strip("/").split("/")[-1]

    if args.add:
        if registry.find(rows, slug) and any(slug in (r["slug"], r["file_slug"]) for r in rows):
            print(f"Đã có dòng cho '{slug}' — dùng --set để đổi trạng thái.", file=sys.stderr)
            return 1
        if not args.keyword:
            ap.error("--add cần --keyword")
        row = {k: "" for k in registry.FIELDS} | {"slug": slug, "file_slug": slug, "live": "no",
                                                   "status": (args.set or "Planned").strip(), "key_chinh": args.keyword}
        if args.cluster:
            hit = registry.match_cluster(rows, args.cluster)
            if not hit:
                names = sorted({f"{r['subgroup']} {r['subgroup_name']}" for r in rows if r["subgroup"]})
                print(f"--cluster '{args.cluster}' không khớp đúng 1 nhóm. Nhóm hiện có:\n  " + "\n  ".join(names), file=sys.stderr)
                return 1
            row["cluster"], row["cluster_name"], row["subgroup"], row["subgroup_name"] = hit
        else:
            row["cluster"], row["cluster_name"], row["subgroup"], row["subgroup_name"] = registry._classify(slug, args.keyword)
        rows.append(row)
        registry.save(rows)
        print(f"Đã thêm: {slug} · {args.keyword} · {row['status']} · {cl_label(row) or '(chưa có cluster — thêm --cluster)'}")
        return 0

    hits = registry.find(rows, slug)
    if not hits:
        print(f"Không có dòng nào cho '{slug}' trong registry. Bài mới: thêm --add --keyword \"…\".", file=sys.stderr)
        return 1
    if args.set is None:
        table(hits)
        return 0
    if len(hits) > 1:
        print(f"{len(hits)} dòng khớp '{slug}' — không thể --set. Dùng slug đầy đủ:", file=sys.stderr)
        for r in hits:
            print(f"  {r['slug']}  ({r['status']})", file=sys.stderr)
        return 1
    new = args.set.strip()
    if new not in registry.STATUSES:
        print(f"Cảnh báo: '{new}' không nằm trong {registry.STATUSES} — vẫn ghi.", file=sys.stderr)
    r = hits[0]
    if r["status"] == new:
        print(f"Không đổi: {r['slug']} đã ở trạng thái {new}")
        return 0
    old, r["status"] = r["status"], new
    registry.save(rows)
    print(f"Đã cập nhật {r['slug']}: {old} → {new} ({cl_label(r)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
