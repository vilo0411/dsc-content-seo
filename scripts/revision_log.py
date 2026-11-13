#!/usr/bin/env python3
"""Append to / read revision-log.md without loading the ~95 KB file into the LLM.

    python scripts/revision_log.py add <slug> --fix "..." --pattern "..." --rule "..." [--scope Global] [--date YYYY-MM-DD]
    python scripts/revision_log.py brief [--since YYYY-MM-DD | --since-learn] [--slug TEXT] [--width 220]
    python scripts/revision_log.py mark-learn          # record today as the last /learn run

`add`   appends one entry in the standard 4-line format (each field capped, see FIELD_MAX) — replaces
        "Read revision-log.md + Edit" in /approve and /write.
`brief` prints one compact line per entry (date · slug · scope · rule) — input for `/learn` without a slug,
        instead of reading the whole log. Default window: entries since the last `mark-learn`
        (falls back to 30 days). Quarterly archives are not scanned (use grep for old history).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta

from _common import PIPELINE_DIR, REVISION_LOG, setup_utf8

STATE = PIPELINE_DIR / "learn-state.json"
ENTRY = re.compile(r"^### \[(\d{4}-\d{2}-\d{2})\]\s*-\s*(.+?)\s*$")
FIELD = re.compile(r"^- \*\*(Lỗi đã sửa|Pattern|Rule học được|Scope):\*\*\s*(.*)$")
FIELD_MAX = 400  # chars per field; the old 3 KB entries are what made the log 95 KB for 30 days


def parse(text: str):
    """Yield dicts {date, slug, fix, pattern, rule, scope} in file order."""
    cur = None
    for line in text.splitlines():
        m = ENTRY.match(line)
        if m:
            if cur and cur["date"] != "YYYY-MM-DD":
                yield cur
            cur = {"date": m.group(1), "slug": m.group(2), "fix": "", "pattern": "", "rule": "", "scope": ""}
            continue
        if cur is None:
            continue
        f = FIELD.match(line)
        if f:
            key = {"Lỗi đã sửa": "fix", "Pattern": "pattern", "Rule học được": "rule", "Scope": "scope"}[f.group(1)]
            cur[key] = f.group(2).strip()
    if cur:
        yield cur


def clip(s: str, n: int) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def last_learn() -> str | None:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8")).get("last_learn")
        except (ValueError, OSError):
            return None
    return None


def cmd_add(a) -> int:
    fields = {"Lỗi đã sửa": a.fix, "Pattern": a.pattern, "Rule học được": a.rule, "Scope": a.scope}
    long = [k for k, v in fields.items() if len(v) > FIELD_MAX]
    if long and not a.allow_long:
        print(f"FAIL: {', '.join(long)} > {FIELD_MAX} ký tự. Rút gọn (chi tiết bài nằm trong snapshot/diff), "
              f"hoặc --allow-long nếu thật sự cần.", file=sys.stderr)
        return 1
    slug = a.slug.strip("/").split("/")[-1]
    block = [f"### [{a.date}] - {slug}"] + [f"- **{k}:** {' '.join(v.split())}" for k, v in fields.items()]
    raw = REVISION_LOG.read_bytes() if REVISION_LOG.exists() else b""
    nl = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").rstrip()
    out = (text + nl + nl if text else "") + nl.join(block) + nl
    REVISION_LOG.write_bytes(out.encode("utf-8"))
    print(f"Đã ghi revision-log: [{a.date}] {slug} ({sum(len(v) for v in fields.values())} ký tự)")
    return 0


def cmd_brief(a) -> int:
    if not REVISION_LOG.exists():
        print("Chưa có revision-log.md", file=sys.stderr)
        return 2
    since = a.since
    label = f"từ {since}" if since else ""
    if not since and a.since_learn is not False:
        since = last_learn()
        label = f"từ lần /learn trước ({since})" if since else ""
    if not since and not a.slug:
        since = (date.today() - timedelta(days=30)).isoformat()
        label = f"30 ngày ({since})"
    rows = list(parse(REVISION_LOG.read_text(encoding="utf-8")))
    if since:
        rows = [r for r in rows if r["date"] > since or (a.since and r["date"] >= since)]
    if a.slug:
        rows = [r for r in rows if a.slug in r["slug"]]
    rows.sort(key=lambda r: r["date"])
    scopes: dict[str, int] = {}
    for r in rows:
        scopes[r["scope"] or "?"] = scopes.get(r["scope"] or "?", 0) + 1
    print(f"# {len(rows)} mục revision-log {label}".rstrip())
    if scopes:
        print("Scope: " + " · ".join(f"{k} {v}" for k, v in sorted(scopes.items(), key=lambda x: -x[1])))
    print()
    for r in rows:
        print(f"- {r['date']} · {r['slug']} · {r['scope'] or '?'} — {clip(r['rule'] or r['fix'], a.width)}")
    if rows:
        print("\nChi tiết 1 mục: grep -n -A4 \"<slug>\" knowledge/3-pipeline/revision-log.md")
    return 0


def cmd_mark(_a) -> int:
    today = date.today().isoformat()
    STATE.write_text(json.dumps({"last_learn": today}, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Đã lưu mốc /learn: {today}")
    return 0


def main() -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="append one entry")
    p.add_argument("slug")
    p.add_argument("--fix", required=True, help="Lỗi đã sửa")
    p.add_argument("--pattern", required=True, help="Câu/cụm bị xoá hoặc thay")
    p.add_argument("--rule", required=True, help="Rule học được")
    p.add_argument("--scope", default="Global")
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--allow-long", action="store_true")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("brief", help="one line per entry")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--since", metavar="YYYY-MM-DD")
    g.add_argument("--since-learn", action="store_true", default=None)
    p.add_argument("--slug", help="filter by slug substring (no date window unless --since)")
    p.add_argument("--width", type=int, default=220)
    p.set_defaults(fn=cmd_brief)

    p = sub.add_parser("mark-learn", help="record today as last /learn")
    p.set_defaults(fn=cmd_mark)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
