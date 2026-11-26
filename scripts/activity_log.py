#!/usr/bin/env python3
"""Activity log chung cho mọi kênh marketing: knowledge/logs/activity/YYYY-MM.jsonl (append-only, 1 dòng / việc).

Log chi tiết của từng việc vẫn ở chỗ cũ (revision-log, publish-ledger, qa-*-log, social ledger…);
file này chỉ là dòng thời gian chung để dashboard (tab "Hoạt động") và /mkt-status đọc.

Dùng:
    python scripts/activity_log.py add --domain social --skill social-post --action create \
        --target CMP-261124-mo-tai-khoan-tet-2027 --path knowledge/6-campaigns/.../social/fb-v1.md [--note "…"]
    python scripts/activity_log.py tail [--domain seo] [--days 7] [-n 30]
    python scripts/activity_log.py stats [--month 2026-11]
    python scripts/activity_log.py backfill [--dry-run]      # dựng lại lịch sử từ ledger/log/file có sẵn (idempotent)

domain: seo · ads-google · ads-meta · social · email · landing · creative · campaign · analytics · market · system
action: create · status · qa · approve · publish · revise · report · learn · sync · run · link · export

Trong script khác:  from activity_log import emit;  emit("seo", "status", slug, status_from=a, status_to=b, skill="approve")
emit() không bao giờ raise — ghi log lỗi thì script chính vẫn chạy tiếp.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import LOGS_DIR, ROOT, setup_utf8  # noqa: E402

ACTIVITY_DIR = Path(os.environ.get("DSC_ACTIVITY_DIR") or ROOT / "knowledge/logs/activity")
FIELDS = ("ts", "actor", "domain", "skill", "action", "target", "status_from", "status_to", "path", "result", "note", "src")
DOMAINS = ("seo", "ads-google", "ads-meta", "social", "email", "landing", "creative", "campaign", "analytics", "market", "system")
ACTIONS = ("create", "status", "qa", "approve", "publish", "revise", "report", "learn", "sync", "run", "link", "export")
DOMAIN_LABEL = {"seo": "SEO", "ads-google": "Google Ads", "ads-meta": "Meta Ads", "social": "Social", "email": "Email",
                "landing": "Landing", "creative": "Creative", "campaign": "Campaign", "analytics": "Analytics",
                "market": "Thị trường", "system": "Hệ thống"}
# Unit tests import scripts that call emit(); keep the real log clean unless a test opts in.
FORCE = False
_actor_cache: str | None = None


def _actor() -> str:
    global _actor_cache
    if _actor_cache is None:
        name = os.environ.get("DSC_ACTOR", "")
        if not name:
            try:
                name = subprocess.run(["git", "config", "user.name"], cwd=ROOT, capture_output=True, text=True,
                                      encoding="utf-8", timeout=5).stdout.strip()
            except Exception:
                name = ""
        _actor_cache = name or os.environ.get("USERNAME") or os.environ.get("USER") or "?"
    return _actor_cache


def _rel(path) -> str:
    if not path:
        return ""
    p = Path(path)
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return p.as_posix()


def _file_for(ts: str) -> Path:
    return ACTIVITY_DIR / f"{ts[:7]}.jsonl"


def emit(domain: str, action: str, target: str = "", *, skill: str = "", status_from: str = "", status_to: str = "",
         path="", result: str = "", note: str = "", ts: str = "", src: str = "", actor: str = "") -> dict | None:
    """Append one event. Never raises. Returns the record (or None when skipped / failed)."""
    if "unittest" in sys.modules and not FORCE:
        return None
    try:
        rec = {"ts": ts or datetime.now().isoformat(timespec="seconds"), "actor": actor or _actor(),
               "domain": domain, "skill": skill, "action": action, "target": str(target or ""),
               "status_from": status_from, "status_to": status_to, "path": _rel(path),
               "result": str(result or ""), "note": (note or "")[:300], "src": src}
        rec = {k: v for k, v in rec.items() if v != ""}
        f = _file_for(rec["ts"])
        f.parent.mkdir(parents=True, exist_ok=True)
        with f.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec
    except Exception as e:  # logging must never break the caller
        try:
            print(f"(activity_log: không ghi được — {e})", file=sys.stderr)
        except Exception:
            pass
        return None


def read_events(days: int | None = None, since: str | None = None) -> list[dict]:
    """All events (oldest first), optionally limited to the last N days / since YYYY-MM-DD."""
    if days is not None:
        since = (date.today() - timedelta(days=days)).isoformat()
    out = []
    if not ACTIVITY_DIR.is_dir():
        return out
    for f in sorted(ACTIVITY_DIR.glob("*.jsonl")):
        if since and f.stem < since[:7]:
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if since and e.get("ts", "") < since:
                continue
            out.append(e)
    out.sort(key=lambda e: e.get("ts", ""))
    return out


def recent_has(path, minutes: int = 10) -> bool:
    """True if an event for this path was logged in the last N minutes (de-dup for the Write hook)."""
    rel = _rel(path)
    cutoff = (datetime.now() - timedelta(minutes=minutes)).isoformat(timespec="seconds")
    return any(e.get("path") == rel and e.get("ts", "") >= cutoff for e in read_events(days=1))


# ─────────────────────────── path → domain ───────────────────────────

CAMPAIGN_RE = re.compile(r"knowledge/6-campaigns/(CMP-[^/]+)/(?:([^/]+)/)?")
CAMPAIGN_CH = {"social": "social", "ads": "ads-meta", "landing": "landing", "seo": "seo", "email": "email"}


def classify(path) -> tuple[str, str] | None:
    """(domain, target) for a file under a tracked output folder; None = not tracked."""
    rel = _rel(path)
    m = CAMPAIGN_RE.match(rel)
    if m:
        if "/creatives/" in rel:
            return "creative", m.group(1)
        return CAMPAIGN_CH.get(m.group(2) or "", "campaign"), m.group(1)
    stem = Path(rel).stem
    for prefix, dom in (("knowledge/4-channels/ads/", "ads-google"), ("knowledge/4-channels/email/", "email"),
                        ("knowledge/4-channels/landing/", "landing"), ("knowledge/4-channels/social/", "social"),
                        ("knowledge/5-analytics/", "analytics"), ("knowledge/2-market/", "market"),
                        ("knowledge/3-seo/content/", "seo")):
        if rel.startswith(prefix):
            if dom == "seo":
                stem = re.sub(r"^(Final|Draft|Outline|Optimize|Proposal|Rollback)-", "", stem)
            return dom, stem
    return None


# ─────────────────────────── backfill ───────────────────────────

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")
SKIP_NAMES = {"README.md", "index.html", "sync-baseline.json", "config.json"}
LEDGER_STAGES = (("outline", "approve", "Outline-Approved", "approve"), ("gate2", "approve", "Draft-Approved", "approve"),
                 ("final", "approve", "Finalized", "approve"), ("first_live", "publish", "Live", ""),
                 ("backfill_done", "link", "", "link"), ("gsc_checked", "report", "", "weekly"),
                 ("optimized", "approve", "Optimized", "optimize"), ("optimize_live", "publish", "Live", ""))


def _git_added() -> dict[str, str]:
    """repo path → date the file was first committed (one git call). Empty when git is unavailable."""
    try:
        out = subprocess.run(["git", "log", "--diff-filter=A", "--name-only", "--format=@%as", "--", "knowledge"],
                             cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60).stdout
    except Exception:
        return {}
    added, day = {}, ""
    for line in out.splitlines():
        if line.startswith("@"):
            day = line[1:]
        elif line.strip():
            added[line.strip()] = day  # log is newest first → keep overwriting to end at the oldest add
    return added


def _key(e: dict) -> tuple:
    return (e.get("ts", "")[:10], e.get("domain"), e.get("action"), e.get("target", ""), e.get("path", ""),
            e.get("status_to", ""))


def _backfill_events() -> list[dict]:
    ev: list[dict] = []
    add = lambda **k: ev.append({kk: vv for kk, vv in k.items() if vv})  # noqa: E731

    ledger = LOGS_DIR / "publish-ledger.csv"
    if ledger.exists():
        with ledger.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                for col, action, st, skill in LEDGER_STAGES:
                    v = (r.get(col) or "").strip()
                    if DATE_RE.match(v):
                        add(ts=v[:10] + "T00:00:00", domain="seo", action=action, target=r["slug"], status_to=st,
                            skill=skill, path="knowledge/3-seo/logs/publish-ledger.csv", note=f"ledger:{col}")

    for f in [LOGS_DIR / "revision-log.md", *sorted((LOGS_DIR / "revision-log").glob("*.md"))]:
        if f.exists():
            for d, slug in re.findall(r"(?m)^### \[(\d{4}-\d{2}-\d{2})\] - (\S+)", f.read_text(encoding="utf-8")):
                add(ts=d + "T00:00:00", domain="seo", action="revise", target=slug, skill="revise",
                    path=f"knowledge/3-seo/logs/{f.relative_to(LOGS_DIR).as_posix()}")

    qa = LOGS_DIR / "qa-score-log.csv"
    if qa.exists():
        with qa.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if DATE_RE.match(r.get("date") or ""):
                    add(ts=r["date"][:10] + "T00:00:00", domain="seo", action="qa", target=r.get("slug", ""),
                        skill="qa_lint", result=f"score {r.get('score', '')}", path="knowledge/3-seo/logs/qa-score-log.csv")

    camp = ROOT / "knowledge/6-campaigns"
    for log in camp.glob("CMP-*/**/creatives/generate-log.jsonl"):
        job = log.relative_to(camp).parts[0]
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                g = json.loads(line)
            except json.JSONDecodeError:
                continue
            if DATE_RE.match(str(g.get("at", ""))):
                add(ts=str(g["at"])[:19], domain="creative", action="create", target=job, skill="creative",
                    result=str(g.get("status", "")), note=f"generate {g.get('id', '')}", path=log)
    for design in camp.glob("CMP-*/**/creatives/design.json"):
        job = design.relative_to(camp).parts[0]
        try:
            d = json.loads(design.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for a in d.get("approved") or []:
            if DATE_RE.match(str(a.get("luc", ""))):
                add(ts=str(a["luc"])[:19], domain="creative", action="approve", target=job, skill="creative",
                    note=f"v{a.get('v', '')} {', '.join(map(str, a.get('ids') or []))}", path=design)

    # Output files with no log of their own: one "create" event at the file's Created:/mtime date.
    roots = [camp, ROOT / "knowledge/4-channels/ads", ROOT / "knowledge/4-channels/email",
             ROOT / "knowledge/4-channels/landing", ROOT / "knowledge/5-analytics", ROOT / "knowledge/2-market"]
    added = _git_added()
    for base in roots:
        for f in base.rglob("*.md"):
            if f.name in SKIP_NAMES or "/creatives/" in f.as_posix():
                continue
            hit = classify(f)
            if not hit:
                continue
            head = f.read_text(encoding="utf-8", errors="replace")[:800]
            m = re.search(r"(?m)^(?:Created|Date|Ngày):\s*(\d{4}-\d{2}-\d{2})", head)
            day = m.group(1) if m else added.get(_rel(f)) or date.fromtimestamp(f.stat().st_mtime).isoformat()
            dom, target = hit
            action = "report" if dom == "analytics" or f.name == "report.md" or "/watch/" in f.as_posix() else "create"
            add(ts=day + "T00:00:00", domain=dom, action=action, target=target, path=f)
    for e in ev:
        e["path"] = _rel(e.get("path", ""))
        e["src"] = "backfill"
        e.setdefault("actor", _actor())
    return ev


def backfill(dry_run: bool = False) -> int:
    have = {_key(e) for e in read_events()}
    new, seen = [], set()
    for e in _backfill_events():
        k = _key(e)
        if k in have or k in seen:
            continue
        seen.add(k)
        new.append(e)
    new.sort(key=lambda e: e["ts"])
    if not dry_run:
        by_file: dict[Path, list[str]] = {}
        for e in new:
            rec = {k: e[k] for k in FIELDS if e.get(k)}
            by_file.setdefault(_file_for(e["ts"]), []).append(json.dumps(rec, ensure_ascii=False))
        for f, lines in by_file.items():
            f.parent.mkdir(parents=True, exist_ok=True)
            with f.open("a", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lines) + "\n")
    c = Counter(e["domain"] for e in new)
    print(f"{'(dry-run) ' if dry_run else ''}backfill: {len(new)} sự kiện mới"
          + (" · " + " · ".join(f"{k} {v}" for k, v in c.most_common()) if c else ""))
    return 0


# ─────────────────────────── CLI ───────────────────────────

def fmt(e: dict) -> str:
    st = f" {e.get('status_from', '')}→{e['status_to']}" if e.get("status_to") else ""
    extra = " · ".join(x for x in (e.get("result"), e.get("note")) if x)
    return (f"{e.get('ts', '')[:16].replace('T', ' ')}  {e.get('domain', ''):<10} {e.get('action', ''):<8} "
            f"{e.get('target', '')}{st}" + (f"  [{e['skill']}]" if e.get("skill") else "") + (f"  — {extra}" if extra else ""))


def main(argv=None) -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add", help="ghi 1 sự kiện (skill do agent làm tay)")
    p.add_argument("--domain", required=True, choices=DOMAINS)
    p.add_argument("--action", required=True, choices=ACTIONS)
    p.add_argument("--target", default="")
    p.add_argument("--skill", default="")
    p.add_argument("--path", default="")
    p.add_argument("--status-from", default="")
    p.add_argument("--status-to", default="")
    p.add_argument("--result", default="")
    p.add_argument("--note", default="")
    p = sub.add_parser("tail")
    p.add_argument("--domain")
    p.add_argument("--days", type=int, default=14)
    p.add_argument("-n", type=int, default=30)
    p = sub.add_parser("stats")
    p.add_argument("--month", default=date.today().strftime("%Y-%m"))
    p = sub.add_parser("backfill")
    p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "add":
        rec = emit(a.domain, a.action, a.target, skill=a.skill, path=a.path, status_from=a.status_from,
                   status_to=a.status_to, result=a.result, note=a.note)
        if not rec:
            return 1
        print("activity: " + fmt(rec))
    elif a.cmd == "tail":
        ev = [e for e in read_events(days=a.days) if not a.domain or e.get("domain") == a.domain]
        for e in ev[-a.n:]:
            print(fmt(e))
        if not ev:
            print("(chưa có sự kiện)")
    elif a.cmd == "stats":
        ev = [e for e in read_events(since=a.month + "-01") if e.get("ts", "").startswith(a.month)]
        by = Counter((e.get("domain"), e.get("action")) for e in ev)
        print(f"# Hoạt động {a.month}: {len(ev)} sự kiện")
        for dom in DOMAINS:
            row = {act: n for (d, act), n in by.items() if d == dom}
            if row:
                print(f"{DOMAIN_LABEL[dom]:<11} {sum(row.values()):>4}  " + " · ".join(f"{k} {v}" for k, v in sorted(row.items())))
    elif a.cmd == "backfill":
        return backfill(a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
