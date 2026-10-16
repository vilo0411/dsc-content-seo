#!/usr/bin/env python3
"""Cache SEO Dashboard MCP results so every agent (Claude Code, Antigravity, Cursor) shares the same GSC data.

The agent that has the `SEO Dashboard` MCP connected calls the tool, then pipes the raw JSON here.
Agents without MCP only read the cache (`report`, `status`). No network, no credentials.

    # save a tool result (JSON on stdin or --file)
    python scripts/dashboard_cache.py save page-queries <slug>   < result.json   # query_search_analytics dimensions=['query'], page filter
    python scripts/dashboard_cache.py save pages                  < result.json   # dimensions=['page']        -> also writes pages.csv
    python scripts/dashboard_cache.py save page-query             < result.json   # dimensions=['page','query'] -> also writes queries.csv
    python scripts/dashboard_cache.py save cannibalization        < result.json   # get_cannibalization

    # read
    python scripts/dashboard_cache.py report <slug>     # "📊 GSC Performance Context" block for the /optimize Proposal
    python scripts/dashboard_cache.py status            # what is cached and how old

Writing pages.csv / queries.csv in the sync_gsc.py schema means process_gsc.py, find_links.py --backfill
and /gsc-sync keep working without Google API credentials.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

from _common import ROOT, setup_utf8

GSC_DIR = ROOT / "knowledge/raw/gsc"
CACHE_DIR = GSC_DIR / "dashboard"
PAGES_CSV = GSC_DIR / "pages.csv"
QUERIES_CSV = GSC_DIR / "queries.csv"
META_FILE = GSC_DIR / "cache-meta.json"
SITE_URL = "https://www.dsc.com.vn/kien-thuc/"
TTL_DAYS = 7
KINDS = ("page-queries", "pages", "page-query", "cannibalization")


def cache_path(kind: str, slug: str | None) -> Path:
    return CACHE_DIR / (f"{kind}-{slug}.json" if slug else f"{kind}.json")


def load_payload(file: str | None) -> dict:
    raw = Path(file).read_text(encoding="utf-8") if file else sys.stdin.read()
    data = json.loads(raw)
    # MCP clients sometimes wrap the tool output as [{"type": "text", "text": "<json>"}]
    if isinstance(data, list) and data and isinstance(data[0], dict) and "text" in data[0]:
        data = json.loads(data[0]["text"])
    if not isinstance(data, dict) or "rows" not in data:
        sys.exit("[ERROR] Payload không phải output SEO Dashboard (thiếu key 'rows').")
    return data


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            # CSV schema (sync_gsc.py) stores CTR as a fraction; the dashboard returns a percentage
            w.writerow({k: (round(float(r.get("ctr", 0)) / 100, 4) if k == "ctr" else r.get(k, "")) for k in fields})
    print(f"[OK] {path.relative_to(ROOT)} ({len(rows)} rows)")


def update_meta(data: dict, rows_key: str):
    meta = json.loads(META_FILE.read_text(encoding="utf-8")) if META_FILE.exists() else {}
    m = data.get("meta", {})
    meta.update({
        "cached_at": datetime.now().isoformat(timespec="seconds"),
        "source": "seo-dashboard-mcp",
        "site": m.get("property_url", ""),
        "period": f"{m.get('start_date', '?')} → {m.get('end_date', '?')}",
        rows_key: len(data["rows"]),
    })
    META_FILE.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_save(a):
    if a.kind == "page-queries" and not a.slug:
        sys.exit("[ERROR] page-queries cần <slug>.")
    data = load_payload(a.file)
    data["_cached_at"] = datetime.now().isoformat(timespec="seconds")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out = cache_path(a.kind, a.slug if a.kind == "page-queries" else None)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {out.relative_to(ROOT)} ({len(data['rows'])} rows)")
    if a.kind == "pages":
        write_csv(PAGES_CSV, data["rows"], ["page", "clicks", "impressions", "ctr", "position"])
        update_meta(data, "page_rows")
    elif a.kind == "page-query":
        write_csv(QUERIES_CSV, data["rows"], ["page", "query", "clicks", "impressions", "ctr", "position"])
        update_meta(data, "query_rows")


def age_days(data: dict) -> float:
    try:
        return (datetime.now() - datetime.fromisoformat(data["_cached_at"])).total_seconds() / 86400
    except (KeyError, ValueError):
        return 999.0


def fmt_n(x) -> str:
    return f"{int(round(float(x))):,}".replace(",", ".")


def fmt_f(x, nd=1) -> str:
    return f"{float(x):.{nd}f}".replace(".", ",")


def cmd_report(a):
    path = cache_path("page-queries", a.slug)
    if not path.exists():
        print(f"[GSC] Chưa có cache cho {a.slug}. Agent có SEO Dashboard MCP: chạy query_search_analytics "
              f"(dimensions=['query'], page_value='/kien-thuc/{a.slug}', days=90, compare_mode='prev_period') "
              f"rồi `dashboard_cache.py save page-queries {a.slug}`. Không có MCP → bỏ qua Bước 2.3 Part A.")
        return 3
    data = json.loads(path.read_text(encoding="utf-8"))
    age = age_days(data)
    m, t = data.get("meta", {}), data.get("meta", {}).get("totals", {})
    if age > TTL_DAYS:
        print(f"⚠️ Cache {fmt_f(age, 0)} ngày tuổi (> {TTL_DAYS}) — nên fetch lại nếu có MCP.")

    lines = [f"📊 GSC Performance Context ({m.get('start_date', '?')} → {m.get('end_date', '?')}, nguồn: SEO Dashboard MCP):"]
    cur = f"- Clicks: {fmt_n(t.get('clicks', 0))} | Impressions: {fmt_n(t.get('impressions', 0))} | CTR: {fmt_f(t.get('ctr', 0), 2)}% | Position: {fmt_f(t.get('position', 0))}"
    if "prev_clicks" in t:
        pct = t.get("click_change_pct")
        cur += (f"  (kỳ trước: {fmt_n(t['prev_clicks'])} clicks, CTR {fmt_f(t.get('prev_ctr', 0), 2)}%, pos {fmt_f(t.get('prev_position', 0))}"
                + (f"; clicks {'+' if pct >= 0 else ''}{fmt_f(pct)}%" if pct is not None else "") + ")")
    lines.append(cur)
    lines.append(f"- Flag title rewrite: {'CÓ' if float(t.get('ctr', 0)) < 3 else 'KHÔNG'} (CTR {'<' if float(t.get('ctr', 0)) < 3 else '≥'} 3%)")

    rows = data["rows"]
    top = [r for r in rows if r.get("clicks", 0) >= 5 and r.get("position", 99) <= 20][:5]
    if top:
        lines.append("- Keyword đang mang click (clicks ≥ 5, pos ≤ 20) — kiểm tra có mặt trong sapo/H2/H3:")
        lines += [f"  → \"{r['query']}\" — {fmt_n(r['clicks'])} clicks, pos {fmt_f(r['position'])}, CTR {fmt_f(r['ctr'], 2)}%" for r in top]
    losers = sorted((r for r in rows if r.get("click_change", 0) <= -5), key=lambda r: r["click_change"])[:5]
    if losers:
        lines.append("- Query mất click nhiều nhất so với kỳ trước:")
        lines += [f"  → \"{r['query']}\" — {fmt_n(r['clicks'])} clicks (từ {fmt_n(r.get('prev_clicks', 0))}), "
                  f"pos {fmt_f(r['position'])} (từ {fmt_f(r.get('prev_position', 0))})" for r in losers]
    sleepers = sorted((r for r in rows if r.get("impressions", 0) >= 300 and float(r.get("ctr", 0)) < 1),
                      key=lambda r: -r["impressions"])[:5]
    if sleepers:
        lines.append("- Keyword ngủ quên (impr ≥ 300, CTR < 1%) — đề xuất H2/FAQ hoặc đưa vào title/meta:")
        lines += [f"  → \"{r['query']}\" — {fmt_n(r['impressions'])} impr, CTR {fmt_f(r['ctr'], 2)}%, pos {fmt_f(r['position'])}" for r in sleepers]

    can = cache_path("cannibalization", None)
    if can.exists():
        cdata = json.loads(can.read_text(encoding="utf-8"))
        hits = [r for r in cdata.get("rows", []) if a.slug in json.dumps(r, ensure_ascii=False)]
        if hits:
            lines.append(f"- Cannibalization: {len(hits)} query có nhiều URL DSC cùng cạnh tranh (xem cache cannibalization.json).")
    print("\n".join(lines))
    return 0


def cmd_status(a):
    if not CACHE_DIR.exists() or not any(CACHE_DIR.glob("*.json")):
        print("Chưa có cache SEO Dashboard.")
        return 0
    for p in sorted(CACHE_DIR.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        age = age_days(d)
        flag = " ⚠️ cũ" if age > TTL_DAYS else ""
        m = d.get("meta", {})
        print(f"{p.name:70} {len(d.get('rows', [])):>4} rows · {m.get('start_date', '?')}→{m.get('end_date', '?')} · {fmt_f(age)} ngày{flag}")
    return 0


def main():
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("save")
    s.add_argument("kind", choices=KINDS)
    s.add_argument("slug", nargs="?")
    s.add_argument("--file")
    r = sub.add_parser("report")
    r.add_argument("slug")
    sub.add_parser("status")
    a = ap.parse_args()
    return {"save": cmd_save, "report": cmd_report, "status": cmd_status}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
