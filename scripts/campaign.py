#!/usr/bin/env python3
"""Job folder cho chiến dịch marketing đa kênh: knowledge/5-campaigns/CMP-YYMMDD-<slug>/

Dùng:
    python scripts/campaign.py new <slug> --title "…" [--channels seo,social,ads,landing] [--date 2026-11-24]
    python scripts/campaign.py status [--json]          # mọi job + trạng thái + số file mỗi kênh
    python scripts/campaign.py set <CMP-id|slug> --status "Chờ duyệt"
    python scripts/campaign.py path <CMP-id|slug>

Trạng thái hợp lệ: Brief · Đang làm · Chờ duyệt · Approved · Live · Đo kết quả · Đóng
Quy ước trong job: <kênh>/<tên>-v<n>.md là bản nháp; bản đã duyệt copy sang approved/ (không sửa bản trong approved/).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, setup_utf8, slugify  # noqa: E402

CAMPAIGNS_DIR = ROOT / "knowledge/5-campaigns"
TEMPLATE = ROOT / ".antigravity/domains/campaign/references/brief-template.md"
CHANNELS = ("seo", "social", "ads", "landing")
STATUSES = ("Brief", "Đang làm", "Chờ duyệt", "Approved", "Live", "Đo kết quả", "Đóng")
STATUS_RE = re.compile(r"(?m)^Status:\s*(.*)$")


def campaigns_dir() -> Path:
    return CAMPAIGNS_DIR


def find(ref: str, base: Path | None = None) -> Path:
    base = base or campaigns_dir()
    hits = [p for p in sorted(base.glob("CMP-*")) if p.is_dir() and (p.name == ref or p.name.endswith("-" + ref))]
    if len(hits) != 1:
        raise SystemExit(f"Không tìm thấy đúng 1 job cho “{ref}” (khớp {len(hits)})")
    return hits[0]


def new(slug: str, title: str, channels: list[str], day: date, base: Path | None = None) -> Path:
    base = base or campaigns_dir()
    slug = slugify(slug)
    prefix = f"CMP-{day:%y%m%d}"
    existing = [p for p in base.glob(f"{prefix}-*") if p.name.endswith("-" + slug)]
    if existing:
        raise SystemExit(f"Đã có job {existing[0].name}")
    job = base / f"{prefix}-{slug}"
    for ch in channels:
        (job / ch).mkdir(parents=True, exist_ok=True)
    (job / "approved").mkdir(parents=True, exist_ok=True)
    tpl = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.exists() else "# {title}\n"
    brief = (tpl.replace("{id}", job.name).replace("{title}", title).replace("{date}", day.isoformat())
             .replace("{channels}", ", ".join(channels)))
    (job / "brief.md").write_text(brief, encoding="utf-8")
    return job


def read_status(job: Path) -> str:
    brief = job / "brief.md"
    if not brief.exists():
        return "?"
    m = STATUS_RE.search(brief.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else "?"


def set_status(job: Path, status: str) -> None:
    if status not in STATUSES:
        raise SystemExit(f"Trạng thái không hợp lệ. Chọn: {', '.join(STATUSES)}")
    brief = job / "brief.md"
    text = brief.read_text(encoding="utf-8")
    text = STATUS_RE.sub(f"Status: {status}", text, count=1) if STATUS_RE.search(text) else f"Status: {status}\n" + text
    brief.write_text(text, encoding="utf-8")


def summary(base: Path | None = None) -> list[dict]:
    base = base or campaigns_dir()
    rows = []
    for job in sorted(base.glob("CMP-*")):
        if not job.is_dir():
            continue
        counts = {ch: len([f for f in (job / ch).glob("*") if f.is_file()]) for ch in CHANNELS if (job / ch).is_dir()}
        rows.append({"id": job.name, "status": read_status(job), "files": counts,
                     "approved": len([f for f in (job / "approved").glob("*") if f.is_file()]) if (job / "approved").is_dir() else 0,
                     "report": (job / "report.md").exists()})
    return rows


def main(argv=None) -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new")
    p.add_argument("slug")
    p.add_argument("--title", required=True)
    p.add_argument("--channels", default=",".join(CHANNELS))
    p.add_argument("--date")
    p = sub.add_parser("status")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("set")
    p.add_argument("ref")
    p.add_argument("--status", required=True)
    p = sub.add_parser("path")
    p.add_argument("ref")
    a = ap.parse_args(argv)

    if a.cmd == "new":
        chans = [c.strip() for c in a.channels.split(",") if c.strip()]
        bad = [c for c in chans if c not in CHANNELS]
        if bad:
            raise SystemExit(f"Kênh không hợp lệ: {bad}. Chọn trong {CHANNELS}")
        job = new(a.slug, a.title, chans, date.fromisoformat(a.date) if a.date else date.today())
        print(job.relative_to(ROOT))
    elif a.cmd == "status":
        rows = summary()
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        elif not rows:
            print("Chưa có job nào trong knowledge/5-campaigns/")
        else:
            for r in rows:
                files = " ".join(f"{k}:{v}" for k, v in r["files"].items())
                print(f"{r['id']:<40} {r['status']:<12} {files}  approved:{r['approved']}"
                      + ("  report✓" if r["report"] else ""))
    elif a.cmd == "set":
        job = find(a.ref)
        set_status(job, a.status)
        print(f"{job.name} → {a.status}")
    elif a.cmd == "path":
        print(find(a.ref).relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
