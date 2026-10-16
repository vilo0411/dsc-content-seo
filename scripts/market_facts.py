#!/usr/bin/env python3
"""Live VN market data for SEO articles: fetch anchors, verify claims.

Why this exists: `slop_check.py` can tell that a sentence has no verifiable anchor,
but it cannot tell whether an anchor is TRUE or STALE. This script closes that gap.
It is the only networked script in the writing pipeline - `qa_lint.py` and
`slop_check.py` stay offline and deterministic.

Usage:
    python scripts/market_facts.py --brief [--tickers VCB,HPG] [--days 60]
    python scripts/market_facts.py --ticker VCB [--days 120]
    python scripts/market_facts.py --index VNINDEX [--years 2022,2026]
    python scripts/market_facts.py --verify <file.md> [--json]
    python scripts/market_facts.py --refresh        # bust the 24h cache

Data source: dchart-api.vndirect.com.vn (unofficial public endpoint, no key).
            iboard-query.ssi.com.vn for the listed-symbol list.
Both are best-effort: on failure the script exits 3 and callers must continue
without market data rather than block the pipeline.

Exit:   0 = OK / no claim errors   1 = claim mismatch found   2 = usage
        3 = data source unreachable (soft failure, do not block)
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, setup_utf8, read_text  # noqa: E402

setup_utf8()

CACHE = ROOT / "scripts/market-cache.json"
CACHE_TTL = 24 * 3600
SYMBOL_TTL = 7 * 24 * 3600
TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "vi,en;q=0.9",
    "Referer": "https://dchart.vndirect.com.vn/",
    "Origin": "https://dchart.vndirect.com.vn",
}
HIST_URL = "https://dchart-api.vndirect.com.vn/dchart/history?symbol={sym}&resolution=D&from={frm}&to={to}"
BOARD_URL = "https://iboard-query.ssi.com.vn/stock/exchange/{ex}"

INDEXES = {"VNINDEX", "VN30", "HNX", "HNXINDEX", "UPCOM", "VN100"}
# Static market structure - true regardless of date, safe for evergreen copy.
STRUCTURAL = [
    "Biên độ dao động mỗi phiên: HOSE 7%, HNX 10%, UPCoM 15%",
    "Chu kỳ thanh toán T+2",
    "Lô giao dịch tối thiểu trên HOSE: 100 cổ phiếu",
    "Phiên khớp lệnh định kỳ: ATO 9h00-9h15, ATC 14h30-14h45 (HOSE)",
]

# Tolerance when checking a rounded claim ("vùng 1.500 điểm") against real data.
ROUND_TOLERANCE = 0.04
STALE_MONTHS = 18


# --------------------------- cache ---------------------------
def load_cache() -> dict:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"hist": {}, "symbols": {}}


def save_cache(c: dict) -> None:
    CACHE.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")


def fresh(entry: dict, ttl: int) -> bool:
    return bool(entry) and (time.time() - entry.get("_at", 0)) < ttl


# --------------------------- fetch ---------------------------
class SourceDown(Exception):
    pass


def _get(url: str) -> bytes:
    socket.setdefaulttimeout(TIMEOUT)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) as r:
            return r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, socket.error, OSError) as e:
        raise SourceDown(f"{type(e).__name__}: {e}") from e


def history(sym: str, days: int = 60, cache: dict | None = None, refresh: bool = False) -> dict:
    """Daily OHLCV for a symbol or index. Returns {t,o,h,l,c,v} lists."""
    cache = cache if cache is not None else load_cache()
    key = f"{sym.upper()}:{days}"
    hit = cache["hist"].get(key)
    if not refresh and fresh(hit, CACHE_TTL):
        return hit["data"]
    to = int(time.time())
    frm = to - 86400 * max(days, 7)
    raw = json.loads(_get(HIST_URL.format(sym=sym.upper(), frm=frm, to=to)))
    if not raw.get("t"):
        raise SourceDown(f"không có dữ liệu cho {sym}")
    cache["hist"][key] = {"_at": time.time(), "data": raw}
    save_cache(cache)
    return raw


def history_range(sym: str, y0: int, y1: int) -> dict:
    """Daily OHLCV between 1/1/y0 and 1/1/y1 (dchart rejects very long spans)."""
    frm = int(datetime(y0, 1, 1, tzinfo=timezone.utc).timestamp())
    to = int(datetime(y1, 1, 1, tzinfo=timezone.utc).timestamp())
    raw = json.loads(_get(HIST_URL.format(sym=sym.upper(), frm=frm, to=to)))
    if not raw.get("t"):
        raise SourceDown(f"không có dữ liệu {sym} {y0}-{y1}")
    return raw


def listed_symbols(cache: dict | None = None, refresh: bool = False) -> set[str]:
    """All symbols currently on HOSE/HNX/UPCOM (for spotting invented tickers)."""
    cache = cache if cache is not None else load_cache()
    hit = cache["symbols"]
    if not refresh and fresh(hit, SYMBOL_TTL):
        return set(hit["data"])
    out: set[str] = set()
    for ex in ("hose", "hnx", "upcom"):
        try:
            raw = json.loads(_get(BOARD_URL.format(ex=ex)))
        except SourceDown:
            continue
        for row in raw.get("data", []):
            s = (row.get("ss") or row.get("stockSymbol") or row.get("symbol") or "").strip().upper()
            if re.fullmatch(r"[A-Z0-9]{3}", s):
                out.add(s)
    if not out:
        raise SourceDown("không lấy được danh sách mã niêm yết")
    cache["symbols"] = {"_at": time.time(), "data": sorted(out)}
    save_cache(cache)
    return out


# --------------------------- summarise ---------------------------
def d(ts: int) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%d/%m/%Y")


def month_of(ts: int) -> tuple[int, int]:
    x = datetime.fromtimestamp(ts, timezone.utc)
    return x.month, x.year


def summarise(sym: str, raw: dict) -> dict:
    c, h, l, v, t = raw["c"], raw["h"], raw["l"], raw["v"], raw["t"]
    n = len(c)
    hi = max(range(n), key=lambda i: h[i])
    lo = min(range(n), key=lambda i: l[i])
    return {
        "symbol": sym.upper(),
        "sessions": n,
        "from": d(t[0]),
        "to": d(t[-1]),
        "last_close": c[-1],
        "change_pct": (c[-1] / c[0] - 1) * 100 if c[0] else 0.0,
        "high": h[hi], "high_date": d(t[hi]),
        "low": l[lo], "low_date": d(t[lo]),
        "last_volume": v[-1],
        "avg_volume_20": sum(v[-20:]) / len(v[-20:]) if v else 0,
    }


def fmt_summary(s: dict) -> str:
    return (f"{s['symbol']:9} {s['sessions']:>3} phiên {s['from']}→{s['to']} · "
            f"đóng cửa {s['last_close']:,.2f} ({s['change_pct']:+.1f}%) · "
            f"cao {s['high']:,.2f} ({s['high_date']}) · thấp {s['low']:,.2f} ({s['low_date']}) · "
            f"KLGD phiên cuối {s['last_volume']:,.0f}, bình quân 20 phiên {s['avg_volume_20']:,.0f}")


# --------------------------- claim verification ---------------------------
INDEX_ALIAS = {"vn-index": "VNINDEX", "vnindex": "VNINDEX", "vn index": "VNINDEX",
               "vn30": "VN30", "hnx-index": "HNX", "hnxindex": "HNX"}
# "VN-Index ... 1.500 điểm ... tháng 1/2022"  /  "... năm 2022"
CLAIM_INDEX = re.compile(
    r"(VN-?Index|VN30|HNX-?Index)[^.!?]{0,120}?([\d][\d.,]{2,7})\s*điểm[^.!?]{0,80}?"
    r"(?:ngày\s*\d{1,2}/(\d{1,2})/(20\d{2})"          # ngày DD/MM/YYYY - dạng chính xác nhất
    r"|tháng\s*(\d{1,2})/(20\d{2})"
    r"|năm\s*(20\d{2}))", re.I)
# A 3-letter upper-case token is only a ticker when context says so: in brackets right
# after a proper noun, or right after "mã" / "cổ phiếu". Vietnamese prose also uses the
# bracket form to gloss an English term ("biên lãi ròng (NIM)", "đường lũy thừa (EMA)"),
# so the word before the bracket must start with an explicit upper-case letter (the range
# À-Ỹ would also cover lower-case accented letters) - without that guard every indicator
# acronym in the corpus is reported as an invented ticker. The ticker group stays
# case-SENSITIVE (a global re.I would match "hôm nay" as ticker NAY); only the Vietnamese
# context words are matched case-insensitively.
TICKER = re.compile(
    r"[A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][\wÀ-ỹ]*\s*\(([A-Z]{3})\)"
    r"|(?i:mã|cổ phiếu|ticker)\s+(?:[a-zà-ỹ]+\s+){0,2}([A-Z]{3})\b")
TICKER_STOP = {"VND", "USD", "CEO", "CFO", "GDP", "CPI", "IPO", "NAV", "ROE", "ROA",
               "EPS", "ETF", "FDI", "VAT", "ATO", "ATC", "FAQ", "SEO", "CTA", "API", "PDF",
               "KPI", "VIP", "AND", "THE", "FOR", "OHLC", "RSI", "MACD", "MUA", "BAN", "LC",
               "FA", "TA", "BCTC", "HOSE", "HNX", "VSD", "SSC", "D1", "W1", "CFA", "CPA",
               "AEO", "LTD", "JSC", "PAS", "MNA",
               # technical indicators the corpus glosses in brackets
               "ADX", "EMA", "SMA", "WMA", "OBV", "ATR", "CCI", "MFI", "ROC", "BOP", "DMI",
               "SAR", "CMF", "MDI", "PDI", "VSA", "PSA",
               # accounting / banking metrics
               "NIM", "NPL", "NPM", "EBT", "IRR", "NPV", "CFF", "CFI", "FCF", "COE", "DPS",
               "TER", "AUM", "NCI", "CIR", "LDR", "CAR", "GPM", "OPM", "DSO", "DPO", "SGA",
               "VAS", "IAS", "BEP", "DOL", "DFL", "DTL",
               "NWC", "MOM", "CMO", "PPO", "ROI",
               # foreign exchanges, indices and regulators (not VN-listed by definition)
               "LSE", "TSE", "ASX", "BSE", "SSE", "NSE", "KRX", "SGX", "HKX", "SEC", "FED",
               "FCA", "BLS", "DXY", "SPX", "DJI", "IXC", "MYM", "MES", "MNQ", "CME", "CBO",
               # products, platforms, crypto, misc acronyms used as glosses
               "CCQ", "DCA", "PIN", "OTP", "SMS", "APP", "VFM", "SIP", "PIT", "HSC", "AFL",
               "BTC", "ETH", "XRP", "NFT", "DEX", "CEX", "UPC", "CIC", "PDT", "SOP", "XYZ"}
TEMPORAL = re.compile(r"(?:tháng\s*(\d{1,2})/(20\d{2})|quý\s*([1-4])/(20\d{2}))", re.I)


def parse_num(s: str) -> float:
    """Vietnamese number formatting: 1.500,25 -> 1500.25 ; 1.500 -> 1500."""
    s = s.strip()
    if "," in s:
        return float(s.replace(".", "").replace(",", "."))
    if s.count(".") >= 1 and len(s.split(".")[-1]) == 3:
        return float(s.replace(".", ""))
    return float(s)


def month_window(raw: dict, month: int | None, year: int) -> tuple[float, float] | None:
    """(low, high) of the index inside a month, or inside the whole year."""
    idx = [i for i, ts in enumerate(raw["t"])
           if (month_of(ts)[1] == year and (month is None or month_of(ts)[0] == month))]
    if not idx:
        return None
    return min(raw["l"][i] for i in idx), max(raw["h"][i] for i in idx)


def verify_file(path: Path, as_json: bool) -> int:
    text, _ = read_text(path)
    findings: list[dict] = []
    soft: list[str] = []

    # 1. Index level claims tied to a date
    claims = list(CLAIM_INDEX.finditer(text))
    ranges: dict[tuple[str, int], dict] = {}
    for m in claims:
        sym = INDEX_ALIAS.get(m.group(1).lower().replace(" ", ""), "VNINDEX")
        val = parse_num(m.group(2))
        # groups: 3,4 = ngày DD/MM/YYYY · 5,6 = tháng M/YYYY · 7 = năm YYYY
        month = int(m.group(3) or m.group(5)) if (m.group(3) or m.group(5)) else None
        year = int(m.group(4) or m.group(6) or m.group(7))
        key = (sym, year)
        if key not in ranges:
            try:
                ranges[key] = history_range(sym, year, year + 1)
            except SourceDown as e:
                soft.append(f"không kiểm chứng được {sym} {year}: {e}")
                ranges[key] = {}
        raw = ranges[key]
        if not raw:
            continue
        win = month_window(raw, month, year)
        when = f"tháng {month}/{year}" if month else f"năm {year}"
        if win is None:
            findings.append({"check": "FACT-index-nodata", "severity": "MINOR",
                             "message": f"Không có dữ liệu {sym} {when} để kiểm chứng mốc {val:,.0f} điểm"})
            continue
        lo, hi = win
        if not (lo * (1 - ROUND_TOLERANCE) <= val <= hi * (1 + ROUND_TOLERANCE)):
            findings.append({"check": "FACT-index-wrong", "severity": "CRITICAL",
                             "message": (f"{sym} {when} dao động {lo:,.0f}–{hi:,.0f} điểm, "
                                         f"bài viết nêu {val:,.0f} điểm"),
                             "excerpt": m.group(0)[:110]})

    # 2. Ticker sanity - a 3-letter code that is not listed anywhere
    try:
        listed = listed_symbols()
    except SourceDown as e:
        listed = set()
        soft.append(f"không lấy được danh sách mã niêm yết: {e}")
    if listed:
        seen = {g.upper() for m in TICKER.finditer(text) for g in m.groups()
                if g and g.upper() not in TICKER_STOP}
        for t in sorted(seen - listed):
            findings.append({"check": "FACT-ticker", "severity": "MAJOR",
                             "message": f"Mã “{t}” không có trong danh sách niêm yết HOSE/HNX/UPCoM"})

    # 3. Staleness - a dated figure older than STALE_MONTHS needs a current counterpart
    now = datetime.now(timezone.utc)
    newest = None
    olds = []
    for m in TEMPORAL.finditer(text):
        mo = int(m.group(1) or ((int(m.group(3)) - 1) * 3 + 1))
        yr = int(m.group(2) or m.group(4))
        when = datetime(yr, max(1, min(12, mo)), 1, tzinfo=timezone.utc)
        newest = when if newest is None or when > newest else newest
        if (now - when) > timedelta(days=30 * STALE_MONTHS):
            olds.append(f"{mo}/{yr}")
    if olds and (newest is None or (now - newest) > timedelta(days=30 * STALE_MONTHS)):
        findings.append({"check": "FACT-stale", "severity": "MAJOR",
                         "message": (f"Mọi mốc số liệu đều cũ hơn {STALE_MONTHS} tháng ({', '.join(sorted(set(olds))[:4])}) "
                                     f"— bổ sung 1 mốc hiện tại để bài không bị đọc là lỗi thời")})

    if as_json:
        print(json.dumps({"file": str(path), "findings": findings, "soft_errors": soft},
                         ensure_ascii=False, indent=2))
    else:
        print(f"\nFACT CHECK — {path.name}")
        print(f"{len(claims)} mốc chỉ số có ngày · {len(findings)} vấn đề")
        print("-" * 78)
        for f in findings:
            print(f"[{f['severity']:<8}] {f['check']:<18} {f['message']}")
            if f.get("excerpt"):
                print(f"{'':12}“{f['excerpt']}”")
        if not findings:
            print("Không phát hiện số liệu sai hoặc lỗi thời.")
        for s in soft:
            print(f"[soft]     {s}")
    return 1 if any(f["severity"] in ("CRITICAL", "MAJOR") for f in findings) else 0


# --------------------------- brief ---------------------------
def brief(tickers: list[str], days: int, refresh: bool) -> int:
    cache = load_cache()
    print(f"# Data pack — {datetime.now().strftime('%d/%m/%Y')}")
    print("Mọi số liệu dưới đây PHẢI đi kèm mốc thời gian khi đưa vào bài.\n")
    print("## Cấu trúc thị trường (không hết hạn)")
    for s in STRUCTURAL:
        print(f"- {s}")
    print("\n## Dữ liệu phiên gần nhất")
    down = []
    for sym in tickers:
        try:
            print("- " + fmt_summary(summarise(sym, history(sym, days, cache, refresh))))
        except SourceDown as e:
            down.append(f"{sym}: {e}")
    for x in down:
        print(f"- [không lấy được] {x}")
    if down and len(down) == len(tickers):
        print("\nNguồn dữ liệu không truy cập được — viết bài bằng dữ kiện cấu trúc, đừng chặn pipeline.")
        return 3
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--tickers", default="VNINDEX,VN30")
    ap.add_argument("--ticker")
    ap.add_argument("--index")
    ap.add_argument("--years", help="vd 2022,2026 — in đỉnh/đáy từng năm")
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--verify")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    try:
        if a.verify:
            p = Path(a.verify)
            if not p.exists():
                print(f"Không tìm thấy {p}", file=sys.stderr)
                return 2
            return verify_file(p, a.json)
        if a.ticker or a.index:
            sym = (a.ticker or a.index).upper()
            if a.years:
                y0, y1 = (int(x) for x in a.years.split(","))
                for y in range(y0, y1 + 1):
                    try:
                        raw = history_range(sym, y, y + 1)
                    except SourceDown as e:
                        print(f"{y}: {e}")
                        continue
                    # Report BOTH measures: an index peak quoted from closing prices differs
                    # from the intraday peak (2022: 1.529 vs 1.536). Articles should cite the
                    # closing figure and say so; mixing the two silently is a factual slip.
                    c, t, h, l = raw["c"], raw["t"], raw["h"], raw["l"]
                    chi = max(range(len(c)), key=lambda i: c[i])
                    clo = min(range(len(c)), key=lambda i: c[i])
                    print(f"{y}: {len(t):3} phiên")
                    print(f"      đóng cửa : đỉnh {c[chi]:>9,.0f} ({d(t[chi])}) · đáy {c[clo]:>9,.0f} ({d(t[clo])}) · cuối kỳ {c[-1]:,.0f}")
                    print(f"      intraday : đỉnh {max(h):>9,.0f} · đáy {min(l):>9,.0f}")
                return 0
            s = summarise(sym, history(sym, a.days, refresh=a.refresh))
            print(json.dumps(s, ensure_ascii=False, indent=2) if a.json else fmt_summary(s))
            return 0
        if a.refresh and not a.brief:
            if CACHE.exists():
                CACHE.unlink()
            print("Đã xóa cache market-cache.json")
            return 0
        return brief([x.strip() for x in a.tickers.split(",") if x.strip()], a.days, a.refresh)
    except SourceDown as e:
        print(f"Nguồn dữ liệu không truy cập được: {e}", file=sys.stderr)
        print("Pipeline KHÔNG bị chặn — viết bài bằng dữ kiện cấu trúc thị trường.", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
