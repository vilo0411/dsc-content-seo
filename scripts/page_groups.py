#!/usr/bin/env python3
"""Group every live /kien-thuc article into cluster → subgroup, then join GSC + GA4 data per group for audits.

    python scripts/page_groups.py build                 # -> knowledge/3-pipeline/page-groups.csv (all live slugs)
    python scripts/page_groups.py build --show 3d       # list slugs of one subgroup / cluster ("3") / "unassigned"
    python scripts/page_groups.py taxonomy              # print the cluster/subgroup tree with counts
    python scripts/page_groups.py report [--dir D]      # join audit data -> page-audit.csv + group-performance.md

Assignment priority (first hit wins):
  1. knowledge/3-pipeline/page-groups-overrides.csv   (slug,subgroup,note) — manual decisions, survive rebuilds
  2. link-clusters.json groups                        (internal-link hub/spoke registry)
  3. ticker pages -> ticker-sector.csv                (co-phieu-xxx, co-nen-mua-co-phieu-xxx)
  4. ordered slug rules in RULES below
  5. title rules (same RULES, run on the unaccented title) — confidence "title"
  6. otherwise "unassigned"

Audit data (report) is read from knowledge/raw/audit/<date>/ (newest by default); see AUDIT_FILES.
Stdlib only, no network.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from _common import PIPELINE_DIR, ROOT, TOPIC_FILE, setup_utf8, unaccent

LIVE_PAGES = ROOT / "knowledge/raw/live/pages.csv"
LINK_CLUSTERS = PIPELINE_DIR / "internal-links/link-clusters.json"
TICKER_SECTOR = PIPELINE_DIR / "ticker-sector.csv"
OVERRIDES = PIPELINE_DIR / "page-groups-overrides.csv"
OUT_GROUPS = PIPELINE_DIR / "page-groups.csv"
AUDIT_DIR = ROOT / "knowledge/raw/audit"
OUT_AUDIT = PIPELINE_DIR / "page-audit.csv"
OUT_REPORT = PIPELINE_DIR / "group-performance.md"

CLUSTERS = {
    "1": "Mở TK & Giao dịch cơ bản",
    "2": "Nhập môn & Thị trường chứng khoán",
    "3": "Phân tích kỹ thuật & Chỉ báo",
    "4": "Phân tích cơ bản & Tài chính DN",
    "5": "Cổ phiếu cụ thể & Ngành",
    "6": "Chiến lược, Phương pháp & Quản trị rủi ro",
    "7": "Quỹ & ETF",
    "8": "Phái sinh & Chứng quyền",
    "9": "Vĩ mô & Chính sách",
    "10": "Tiết kiệm & Kênh đầu tư",
    "11": "Vàng",
    "12": "Trái phiếu",
    "13": "Học & nghề tài chính",
    "14": "Bạc",
}

SUBGROUPS = {
    "1a": "Tài khoản, app, phí & margin", "1b": "Lệnh, quy định & phiên giao dịch",
    "2a": "Nền tảng, kinh nghiệm & rủi ro cho người mới", "2b": "Thao tác mua/bán",
    "2d": "Chỉ số chứng khoán VN & thế giới",
    "2f": "Thị trường, chủ thể & thuật ngữ",
    "3a": "Chỉ báo xu hướng (MA, MACD, ADX…)", "3b": "Chỉ báo động lượng/dao động (RSI, Stoch…)",
    "3c": "Khối lượng & dòng tiền", "3d": "Mô hình nến", "3e": "Mô hình giá",
    "3f": "Hỗ trợ–kháng cự, xu hướng, trap, gap", "3g": "Chỉ báo khác (ATR, Bollinger, Keltner…)",
    "3h": "Lý thuyết, phương pháp & công cụ PTKT",
    "4a": "BCTC, kế toán & chi phí", "4b": "Chỉ số sinh lời", "4c": "Định giá cổ phiếu & doanh nghiệp",
    "4d": "Thanh khoản, đòn bẩy, hiệu quả hoạt động", "4e": "Vốn, cổ phần & niêm yết", "4f": "Cổ tức & quyền cổ đông",
    "4g": "Phân tích BCTC doanh nghiệp cụ thể", "4h": "Phân tích định tính doanh nghiệp",
    "5a": "CP Ngân hàng", "5b": "CP BĐS, KCN, xây dựng", "5c": "CP Thép, VLXD, nhựa", "5d": "CP Dầu khí, điện, năng lượng",
    "5e": "CP Bán lẻ, tiêu dùng", "5f": "CP Chứng khoán, bảo hiểm", "5g": "CP Cảng biển & logistics",
    "5h": "CP Nông nghiệp, thuỷ sản, cao su", "5i": "CP Công nghệ & truyền thông",
    "5j": "Chuỗi giá trị & phân tích ngành", "5k": "Loại cổ phiếu & cách chọn", "5l": "CP Hàng không", "5m": "CP Hoá chất, phân bón", "5n": "CP Dệt may",
    "5o": "Danh sách cổ phiếu tiềm năng", "5p": "Chỉ số phân tích ngân hàng (NIM, CASA, LDR…)",
    "6a": "Trường phái & nhà đầu tư nổi tiếng", "6b": "Chiến lược giao dịch", "6c": "Quản trị rủi ro & danh mục",
    "6d": "Tâm lý & hành vi",
    "7a": "Chứng chỉ quỹ, quỹ mở & ETF",
    "8a": "Phái sinh", "8b": "Chứng quyền",
    "9a": "Chỉ số kinh tế", "9b": "Chính sách tiền tệ, tài khoá & lãi suất",
    "9d": "Tỷ giá, thương mại, dòng vốn ngoại", "9e": "Khái niệm kinh tế học", "9f": "Khủng hoảng & sự kiện",
    "10a": "Lãi suất tiết kiệm & so sánh ngân hàng", "10b": "Kênh đầu tư & phân bổ tiền nhàn rỗi",
    "10d": "Ngoài phạm vi: tiền số, forex, tài chính cá nhân",
    "11a": "Vàng", "12a": "Trái phiếu & lợi suất",
    "13a": "Khoá học & sách", "13b": "Chứng chỉ & nghề nghiệp", "14a": "Bạc",
}

# link-clusters.json group name -> subgroup
LINK_GROUP_MAP = {
    "Chọn nơi mở & công cụ": "1a", "Chi phí": "1a", "Thủ tục & loại tài khoản": "1a",
    "Nền tảng & quyết định": "2a", "Thao tác mua / bán": "2b", "Quy định & bảng giá": "1b",
    "Rủi ro & kinh nghiệm": "2a", "Chọn cổ phiếu": "5k",
}

SECTOR_WORDS = {  # "co-phieu-nganh-<x>", "top-co-phieu-<x>" -> subgroup
    "5a": ["ngan-hang"],
    "5b": ["bat-dong-san", "bds", "khu-cong-nghiep", "xay-dung", "dau-tu-cong"],
    "5c": ["thep", "vat-lieu", "nhua", "xi-mang"],
    "5d": ["dau-khi", "nang-luong", "dien", "dien-luc", "than"],
    "5e": ["ban-le", "tieu-dung", "thuc-pham", "o-to"],
    "5f": ["chung-khoan", "bao-hiem"],
    "5g": ["cang-bien", "logistics", "van-tai", "xuat-nhap-khau"],
    "5l": ["hang-khong"],
    "5m": ["phan-bon", "hoa-chat"],
    "5h": ["thuy-san", "cao-su", "nong-nghiep"],
    "5n": ["det-may"],
    "5i": ["cong-nghe", "truyen-thong"],
    "5o": ["du-lich", "y-te", "duoc"],
}


def t(*words: str) -> str:
    """Regex matching any of the hyphen-token sequences as whole tokens inside a slug."""
    return r"(?:^|-)(?:" + "|".join(words) + r")(?:-|$)"


def sector_rx(words: list[str]) -> str:
    w = "|".join(words)
    return rf"(?:co-phieu-(?:nganh-)?(?:{w})(?:-|$)|^top-.*co-phieu-(?:nganh-)?(?:{w})(?:-|$)|(?:^|-)nganh-(?:{w})(?:-|$))"


# Ordered: first match wins. Patterns run on the slug (and later on the slugified title).
RULES: list[tuple[str, str]] = [
    # --- disambiguation: specific phrases that contain a broader token used later
    ("4b", t("bien-loi-nhuan")),
    ("6c", t("mo-hinh-capm", "mo-hinh-markowitz")),
    ("4h", t("mo-hinh-kinh-doanh", "con-hao-kinh-te", "loi-the-canh-tranh", "phan-tich-doanh-nghiep",
             "phuong-phap-top-down", "due-diligence")),
    ("9f", t("khung-hoang", "brexit", "bong-bong", "thien-nga-den", "rua-tien")),
    ("4c", t("quy-tac-72")),
    ("4a", t("goodwill", "capex", "chi-phi-von-capex")),
    ("10a", t("lai-suat-gui-tiet-kiem")),
    ("9e", t("canh-tranh", "canh-tranh-khong-hoan-hao", "do-co-gian", "ly-thuyet-tro-choi", "quy-luat-gia-tri", "zero-sum-game",
             "noi-dia-hoa", "kinh-te-hoc-vi-mo")),
    ("9d", t("can-can-thanh-toan", "can-can-thuong-mai", "von-fpi", "von-fdi", "von-oda")),
    ("4d", t("thanh-toan-lai-vay", "no-dai-han", "chi-so-dar")),
    ("4e", t("co-phieu-quy")),
    ("12a", t("duong-cong-loi-suat", "tin-phieu-kho-bac")),
    ("6b", t("copy-trading", "daytrading", "day-trading", "qua-cau-tuyet", "market-timing")),
    ("6d", t("hieu-ung-dam-dong", "kiem-soat-tam-ly", "lo-kep")),
    ("3b", t("chi-so-rs", "vung-qua-mua", "vung-qua-ban")),
    ("3c", t("mcdx", "dong-tien-nong", "vsa", "theo-dong-tien")),
    ("3d", t("nen-sao-mai", "mau-hinh-nen", "heikin-ashi", "chang-linh", "con-qua", "bieu-do-nen")),
    ("3h", t("ly-thuyet-dow", "kenh-hoi-quy", "duong-zigzag", "quadrant-line")),
    ("4a", t("diem-hoa-von")),
    ("10d", t("tien-ao", "tien-dien-tu", "tieu-san")),
    ("10b", t("lai-kep")),
    ("2d", t("hnx-index", "hnx-30", "vn-index", "vnindex", "vn30", "vn-30", "vn-diamond", "chi-so-dow-jones")),
    ("9a", t("pce", "q-o-q", "yoy", "iip", "nffi", "chi-so-san-xuat")),
    ("1a", t("thue-chuyen-nhuong", "thue-khi-ban", "spread")),
    ("5o", r"^top-\d*-?co-phieu-(dang|sieu|tich-san)|^top-co-phieu-nganh-duoc"),
    # --- product / asset classes
    ("5j", t("chuoi-gia-tri-nganh", "phan-tich-nganh")),
    ("8b", t("chung-quyen-co-bao-dam", "chung-quyen")),
    ("8a", t("phai-sinh", "hop-dong-tuong-lai", "chung-quyen", "quyen-chon", "future", "futures")),
    *[(sg, sector_rx(w)) for sg, w in SECTOR_WORDS.items()],
    ("14a", t("dau-tu-bac", "mua-bac", "gia-bac")),
    ("11a", t("vang", "sjc", "9999", "gia-dau", "hang-hoa", "kim-loai")),
    ("7a", t("etf", "quy-etf", "chung-chi-quy", "ccq", "quy-mo", "quy-dau-tu", "quy-dong", "quy-trai-phieu",
             "quy-tuong-ho", "quy-dragon-capital", "quy-dau-tu-mao-hiem")),
    ("12a", t("trai-phieu", "bond", "bond-yield")),
    # --- stock types & top lists without a sector
    ("5o", r"^top-.*co-phieu"),
    ("5k", t("co-phieu-blue-chip", "blue-chip", "bluechip", "midcap", "penny", "co-phieu-penny",
                                   "co-phieu-phong-thu", "co-phieu-tru", "trang-ben-mua", "sap-but-pha", "chon-co-phieu",
                                   "co-phieu-tiem-nang", "co-phieu-tot")),
    # --- savings / banking
    ("10b", t("gui-tiet-kiem-hay", "tiet-kiem-hay", "nen-gui-tiet-kiem", "tien-nhan-roi", "dau-tu-gi", "kenh-dau-tu")),
    ("10a", t("lai-suat-gui-tiet-kiem", "lai-suat-tiet-kiem", "gui-tiet-kiem", "gui-ngan-hang", "lai-bao-nhieu",
              "so-tiet-kiem", "ngan-hang-nao", "lai-suat-ngan-hang", "lai-suat-huy-dong")),
    ("5p", t("casa", "cir", "nim", "ldr", "no-xau", "bao-phu-no-xau", "room-tin-dung")),
    # --- account & trading basics
    ("1a", t("margin", "ky-quy", "call-margin", "cat-margin", "force-sell", "tai-khoan", "mo-tai-khoan", "luu-ky",
             "ekyc", "app", "nen-mo", "phi-giao-dich", "phi-luu-ky", "bieu-phi", "mat-phi", "san-dau-tu-chung-khoan-ao",
             "chung-khoan-ao", "ung-truoc")),
    ("1b", t("lenh", "khop-lenh", "ato", "atc", "giao-dich-thoa-thuan", "lo-le", "gio-giao-dich", "bien-do",
             "gia-tham-chieu", "gia-tran", "gia-san", "bang-gia", "quy-dinh", "hose", "hnx", "upcom", "krx",
             "san-giao-dich", "mau-trong-chung-khoan", "du-mua", "du-ban")),
    # --- technical analysis
    ("3d", t("doji", "hammer", "marubozu", "engulfing", "harami", "shooting-star", "morning-star", "evening-star",
             "piercing", "dark-cloud", "tweezer", "hanging-man", "inverted-hammer", "mo-hinh-nen", "pin-bar", "inside-bar")),
    ("3e", t("mo-hinh", "vai-dau-vai", "coc-tay-cam", "tam-giac", "lap-gap")),
    ("3a", t("duong-trung-binh", "duong-ma", "ma200", "sma", "ema", "wma", "macd", "adx", "dmi", "ichimoku", "parabolic",
             "moving-average", "golden-cross", "death-cross", "supertrend", "dai-trung-binh-dong", "aroon")),
    ("3b", t("rsi", "stochastic", "momentum", "cci", "williams", "phan-ky", "roc")),
    ("3c", t("khoi-luong", "volume", "obv", "vwap", "mfi", "chaikin", "a-d", "dong-tien")),
    ("3f", t("ho-tro", "khang-cu", "xu-huong", "trendline", "kenh-gia", "gap", "khoang-trong", "bull-trap", "bear-trap",
             "sideway", "breakout", "break-out", "pullback", "pivot", "bullish", "bearish", "uptrend", "downtrend",
             "phan-phoi-dinh", "vung-dinh", "dinh-va-day", "dao-chieu", "vung-bay-gia")),
    ("3g", t("chi-bao", "bollinger", "atr", "keltner", "envelope")),
    ("3h", t("elliott", "wyckoff", "fibonacci", "gann", "phan-tich-ky-thuat", "do-thi-ky-thuat", "bieu-do", "amibroker",
             "tradingview", "price-action")),
    # --- fundamentals
    ("4g", r"^phan-tich-bao-cao-tai-chinh-(?!la-gi)[a-z]"),
    ("4b", t("roe", "roa", "roce", "roic", "ros", "eps", "ebit", "ebitda", "dupont", "phan-tich-dupont",
             "loi-nhuan-rong", "loi-nhuan-sau-thue")),
    ("4c", t("p-e", "p-b", "p-s", "peg", "dinh-gia-co-phieu", "gia-tri-so-sach", "gia-tri-noi-tai", "thi-gia",
             "dcf", "wacc", "npv", "irr", "cagr", "gia-tri-doanh-nghiep", "dinh-gia-doanh-nghiep")),
    ("4d", t("thanh-toan", "current-ratio", "don-bay", "gearing", "no-tren", "von-luu-dong", "vong-quay",
             "thoi-gian-thu-hoi", "he-so-thanh-toan")),
    ("4e", t("von-dieu-le", "von-co-phan", "von-chu-so-huu", "thang-du", "von-phap-dinh", "co-phieu-thuong",
             "co-phieu-uu-dai", "chia-tach", "free-float", "von-hoa", "pha-loang", "mua-lai-co-phieu",
             "ipo", "niem-yet", "huy-niem-yet", "m-a", "due-diligence")),
    ("4f", t("co-tuc", "ngay-giao-dich-khong-huong-quyen", "esop", "chot-quyen")),
    ("4a", t("bao-cao", "ke-toan", "can-doi", "thuong-nien", "chi-tieu", "phan-tich-co-ban", "no-phai-tra",
             "chi-phi", "co-cau-von", "phan-tich-doanh-nghiep")),
    # --- strategy / risk / psychology
    ("6a", t("dau-tu-gia-tri", "dau-tu-tang-truong", "warren", "buffett", "canslim", "richard", "phuong-phap-top-down",
             "top-down")),
    ("6b", t("dca", "swing", "swing-trading", "position-trading", "chien-luoc", "buy-the-dips", "trading", "quantitative",
             "backtest", "dau-tu-dai-han", "dau-co", "tich-san", "dau-tu-thu-dong")),
    ("6c", t("rui-ro", "cat-lo", "take-profit", "ty-le-risk-reward", "quan-ly-von", "da-dang-hoa", "danh-muc",
             "quan-tri-rui-ro", "do-lech-chuan", "volatility", "beta", "he-so-tuong-quan", "khau-vi-rui-ro", "drawdown")),
    ("6d", t("tam-ly", "fomo", "thien-kien", "lac-quan")),
    # --- macro
    ("9b", t("chinh-sach-tien-te", "lai-suat-dieu-hanh", "nghiep-vu-thi-truong-mo", "cung-tien", "cau-tien", "bom-tien",
             "ty-le-du-tru", "ngan-hang-trung-uong", "fed", "ecb", "lai-suat", "tai-khoa", "chinh-sach-cong",
             "dau-tu-cong", "no-chinh-phu", "thi-truong-tien-te")),
    ("9a", t("gdp", "grdp", "gnp", "cpi", "ppi", "pmi", "gpi", "lam-phat", "giam-phat", "icor", "tang-truong-kinh-te",
             "chu-ky-kinh-te", "suy-thoai", "vi-mo", "chu-ky")),
    ("9d", t("ty-gia", "ngoai-hoi", "du-tru-ngoai-hoi", "xuat-sieu", "dxy", "imf", "khoi-ngoai", "noi-dia-hoa")),
    ("9e", t("khung-hoang", "brexit", "bong-bong", "kinh-te", "rua-tien", "gio-hang", "quan-ly-thi-truong",
             "co-hoi-thi-truong")),
    # --- beginner track (broad, last)
    ("13b", t("chung-chi", "cfa", "acca", "chuyen-vien", "tu-van", "moi-gioi", "muc-luong")),
    ("13a", t("khoa-hoc", "cuon-sach", "sach", "giao-trinh", "hoc", "dien-dan", "kenh-tik-tok")),
    ("2d", t("chi-so-chung-khoan", "chi-so")),
    ("2b", t("mua-co-phieu", "ban-co-phieu", "cach-mua", "cach-ban", "tren-dien-thoai")),
    ("2a", t("kinh-nghiem", "sai-lam", "lua-dao", "doi-lai", "chay-tai-khoan", "f0")),
    ("2f", t("thanh-khoan", "thi-truong", "nha-tao-lap", "tu-doanh", "thao-tung", "noi-gian", "nyse", "sec", "repo",
             "ban-khong", "wash-out", "ce", "diem", "target", "nav", "uy-thac", "hieu-ung-thang-gieng", "sell-in-may",
             "giao-dich-chung-khoan", "cong-cu-tai-chinh")),
    ("2a", t("chung-khoan", "co-phieu", "nguoi-moi", "dau-tu", "thuat-ngu", "bao-nhieu-tien", "von-nho", "nha-dau-tu",
             "tai-chinh")),
]
COMPILED = [(sg, re.compile(p)) for sg, p in RULES]

INTENT_RULES = [
    ("ma-cp", None),  # set when a ticker is detected
    ("so-sanh", re.compile(t("so-sanh", "phan-biet", "hay", "vs", "khac-nhau", "va"))),
    ("co-nen", re.compile(r"(?:^|-)(co-nen|nen-mua|nen-gui|nen-chon|nen-dau-tu|co-nen-mua)(?:-|$)")),
    ("list", re.compile(r"(^|-)(top|danh-sach)(-|$)|^\d+-|(^|-)(cac|nhung)-")),
    ("huong-dan", re.compile(t("cach", "huong-dan", "bi-quyet", "quy-trinh", "cac-buoc", "lam-sao", "lam-the-nao"))),
    ("dinh-nghia", re.compile(t("la-gi", "la-ai", "y-nghia", "khai-niem"))),
]

FIELDS = ["slug", "title", "cluster", "cluster_name", "subgroup", "subgroup_name", "intent", "confidence",
          "rule", "old_cluster", "words", "in_contextual", "last_changed"]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_symbols() -> set[str]:
    cache = ROOT / "scripts/market-cache.json"
    try:
        return set(json.loads(cache.read_text(encoding="utf-8"))["symbols"]["data"])
    except (OSError, KeyError, ValueError):
        return set()


def ticker_in(slug: str, sector: dict[str, str]) -> str | None:
    """First token that is a ticker with a known sector, only on stock-type slugs."""
    if not re.search(r"(^|-)(co-phieu|ma)(-|$)", slug):
        return None
    for tok in slug.split("-"):
        if len(tok) == 3 and tok.upper() in sector:
            return tok.upper()
    return None


def old_clusters() -> dict[str, str]:
    out = {}
    if not TOPIC_FILE.exists():
        return out
    cluster = ""
    for line in TOPIC_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            cluster = line[3:].strip()
        m = re.search(r"/kien-thuc/([a-z0-9-]+)", line)
        if m and line.startswith("|"):
            out[m.group(1)] = cluster.split(":")[0]
    return out


def link_groups() -> dict[str, str]:
    out = {}
    data = json.loads(LINK_CLUSTERS.read_text(encoding="utf-8"))
    for c in data["clusters"]:
        for g in c["groups"]:
            # c3–c11 groups are named "<subgroup> <name>" (generated from this script's output) — skip, rules already cover them
            sg = LINK_GROUP_MAP.get(g.get("name", ""))
            if not sg:
                continue
            for s in ([g["hub"]] if g.get("hub") else []) + g.get("spokes", []):
                out.setdefault(s, sg)
    return out


def intent_of(slug: str, has_ticker: bool) -> str:
    if has_ticker:
        return "ma-cp"
    for name, rx in INTENT_RULES[1:]:
        if rx.search(slug):
            return name
    return "khac"


def classify(slug: str, title: str, overrides, links, sector) -> tuple[str, str, str, bool]:
    """Return (subgroup, confidence, rule, has_ticker)."""
    tk = ticker_in(slug, sector)
    if slug in overrides:
        return overrides[slug], "override", "overrides.csv", bool(tk)
    if slug in links:
        return links[slug], "registry", "link-clusters.json", bool(tk)
    if tk:
        return sector[tk], "ticker", tk, True
    for sg, rx in COMPILED:
        m = rx.search(slug)
        if m:
            return sg, "rule", m.group(0).strip("-"), False
    tslug = re.sub(r"[^a-z0-9]+", "-", unaccent(title)).strip("-")
    for sg, rx in COMPILED:
        m = rx.search(tslug)
        if m:
            return sg, "title", m.group(0).strip("-"), False
    return "", "unassigned", "", False


def build_rows() -> list[dict]:
    pages = read_csv(LIVE_PAGES)
    overrides = {r["slug"].strip(): r["subgroup"].strip() for r in read_csv(OVERRIDES)} if OVERRIDES.exists() else {}
    sector = {r["ticker"].upper(): r["subgroup"] for r in read_csv(TICKER_SECTOR)}
    links = link_groups()
    olds = old_clusters()
    rows = []
    for p in pages:
        slug = p["slug"]
        sg, conf, rule, tk = classify(slug, p.get("title", ""), overrides, links, sector)
        cl = re.match(r"\d+", sg).group(0) if sg else ""
        rows.append({
            "slug": slug, "title": p.get("title", ""), "cluster": cl, "cluster_name": CLUSTERS.get(cl, ""),
            "subgroup": sg, "subgroup_name": SUBGROUPS.get(sg, ""), "intent": intent_of(slug, tk),
            "confidence": conf, "rule": rule, "old_cluster": olds.get(slug, ""),
            "words": p.get("words", ""), "in_contextual": p.get("in_contextual", ""), "last_changed": p.get("last_changed", ""),
        })
    rows.sort(key=lambda r: (sg_key(r["subgroup"]), r["slug"]))
    return rows


def sg_key(sg: str):
    m = re.match(r"(\d+)([a-z]?)", sg or "")
    return (int(m.group(1)), m.group(2)) if m else (99, "")


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def cmd_build(a):
    rows = build_rows()
    if a.show:
        key = a.show
        sel = [r for r in rows if (r["subgroup"] == key or r["cluster"] == key or (key == "unassigned" and not r["subgroup"]))]
        for r in sel:
            print(f"{r['subgroup']:4} {r['confidence']:9} {r['rule'][:22]:22} {r['slug']}")
        print(f"-- {len(sel)} bài")
        return 0
    write_csv(OUT_GROUPS, rows, FIELDS)
    print(f"[OK] {OUT_GROUPS.relative_to(ROOT)} ({len(rows)} bài)")
    print_taxonomy(rows)
    return 0


def print_taxonomy(rows: list[dict]):
    by_sg = Counter(r["subgroup"] for r in rows)
    conf = Counter(r["confidence"] for r in rows)
    for cl, name in CLUSTERS.items():
        sgs = [s for s in SUBGROUPS if re.match(rf"{cl}[a-z]$", s)]
        print(f"\n{cl}. {name} — {sum(by_sg[s] for s in sgs)} bài")
        for s in sgs:
            n = by_sg[s]
            flag = "  ⚠️ <8" if n < 8 else ("  ⚠️ >35" if n > 35 else "")
            print(f"   {s:4} {SUBGROUPS[s]:45} {n:>4}{flag}")
    print(f"\nunassigned: {by_sg['']} · confidence: " + ", ".join(f"{k} {v}" for k, v in conf.most_common()))


def cmd_taxonomy(a):
    rows = read_csv(OUT_GROUPS) if OUT_GROUPS.exists() else build_rows()
    print_taxonomy(rows)
    return 0


# ---------------------------------------------------------------- report

def slug_of(url: str) -> str:
    """Slug of a canonical /kien-thuc/<slug> URL; '' for /en/, nested or other paths."""
    path = re.sub(r"^https?://[^/]+", "", (url or "").strip()).split("?")[0].split("#")[0].rstrip("/")
    m = re.fullmatch(r"/kien-thuc/([a-z0-9-]+)", path)
    return m.group(1) if m else ""


def duration_s(x) -> float:
    """GA4 durations come as seconds ('65.2') or '1m 05s' / '00:01:05'."""
    s = str(x).strip()
    if m := re.fullmatch(r"(?:(\d+)h\s*)?(?:(\d+)m\s*)?(?:(\d+(?:\.\d+)?)s)?", s):
        if any(m.groups()):
            return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + float(m.group(3) or 0)
    if re.fullmatch(r"\d+:\d{2}(:\d{2})?", s):
        parts = [int(p) for p in s.split(":")]
        return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
    return num(s)


def ratio(x) -> float:
    """Rates as 0–1 whether the source wrote 0.65, 65 or '65%'."""
    v = num(x)
    return v / 100 if v > 1 else v


def num(x) -> float:
    try:
        return float(re.sub(r"[^\d.\-]", "", str(x).replace(",", "")) or 0)
    except ValueError:
        return 0.0


def load_mcp(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list) and data and isinstance(data[0], dict) and "text" in data[0]:
        data = json.loads(data[0]["text"])
    rows = data.get("rows", []) if isinstance(data, dict) else []
    return collapse_device(rows) if rows and "device" in rows[0] else rows


def collapse_device(rows: list[dict]) -> list[dict]:
    """Sum rows split by device back to page (or page×query); position = impression-weighted mean.
    (Pulls add the device dimension only so large MCP results get saved to a file instead of inline.)"""
    acc: dict[tuple, dict] = {}
    for r in rows:
        key = (r.get("page"), r.get("query"))
        a = acc.setdefault(key, {"page": r.get("page"), **({"query": r["query"]} if "query" in r else {}),
                                 "clicks": 0, "impressions": 0, "prev_clicks": 0, "prev_impressions": 0,
                                 "_pw": 0.0, "_ppw": 0.0})
        for k in ("clicks", "impressions", "prev_clicks", "prev_impressions"):
            a[k] += r.get(k, 0) or 0
        a["_pw"] += (r.get("position") or 0) * (r.get("impressions") or 0)
        a["_ppw"] += (r.get("prev_position") or 0) * (r.get("prev_impressions") or 0)
    out = []
    for a in acc.values():
        pw, ppw = a.pop("_pw"), a.pop("_ppw")
        a["position"] = pw / a["impressions"] if a["impressions"] else None
        if a["prev_impressions"]:
            a["prev_position"] = ppw / a["prev_impressions"]
        a["ctr"] = a["clicks"] / a["impressions"] * 100 if a["impressions"] else 0
        a["click_change"] = a["clicks"] - a["prev_clicks"]
        if a["position"] is not None and a.get("prev_position"):
            a["position_change"] = a["position"] - a["prev_position"]
        out.append(a)
    return out


GA4_COLS = {  # canonical -> regex on header (GA4 EN/VI exports)
    "sessions": r"^(sessions|phiên)$",
    "engaged_sessions": r"engaged sessions|phiên tương tác",
    "engagement_rate": r"engagement rate|tỷ lệ tương tác",
    "avg_engagement_time": r"average engagement time|thời gian tương tác trung bình",
    "views_per_session": r"views per session|số lượt xem.*phiên",
    "key_events": r"^(key events|sự kiện chính|conversions|lượt chuyển đổi)$",
    "key_event_rate": r"key event rate|tỷ lệ sự kiện chính|conversion rate",
    "event_count": r"event count|số lượng sự kiện",
}


def load_ga4_csv(path: Path) -> dict[str, dict]:
    """GA4 Explore/Report CSV (comment lines '#', header with Landing page) -> slug -> metrics (summed)."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].startswith("#")]
    hi = next((i for i, r in enumerate(rows) if any(re.search(r"landing\s*page|trang đích|page path", c, re.I) for c in r)), None)
    if hi is None:
        sys.exit(f"[ERROR] {path.name}: không thấy cột Landing page")
    head = [c.strip() for c in rows[hi]]
    pcol = next(i for i, c in enumerate(head) if re.search(r"landing\s*page|trang đích|page path", c, re.I))
    cols = {k: next((i for i, c in enumerate(head) if re.search(rx, c, re.I)), None) for k, rx in GA4_COLS.items()}
    out: dict[str, dict] = defaultdict(lambda: defaultdict(float))
    for r in rows[hi + 1:]:
        if len(r) <= pcol:
            continue
        s = slug_of("/" + r[pcol].lstrip("/")) if "/kien-thuc/" in r[pcol] else ""
        if not s:
            continue
        sess = num(r[cols["sessions"]]) if cols["sessions"] is not None else 0
        for k, i in cols.items():
            if i is None or i >= len(r):
                continue
            v = (duration_s(r[i]) if k == "avg_engagement_time"
                 else ratio(r[i]) if k in ("engagement_rate", "key_event_rate") else num(r[i]))
            if k in ("engagement_rate", "avg_engagement_time", "views_per_session", "key_event_rate"):
                out[s]["_w_" + k] += v * sess  # session-weighted average when a slug appears on several rows
            else:
                out[s][k] += v
    for s, d in out.items():
        sess = d.get("sessions", 0) or 1
        for k in ("engagement_rate", "avg_engagement_time", "views_per_session", "key_event_rate"):
            if "_w_" + k in d:
                d[k] = d.pop("_w_" + k) / sess
    return out


AUDIT_FILES = """Files in knowledge/raw/audit/<YYYY-MM-DD>/ (all optional; missing = column left blank):
  gsc-pages.json         MCP query_search_analytics dims=['page'], page_value='/kien-thuc/', days=90, compare_mode='prev_period', limit=500 (+ gsc-pages-2.json … if split)
  gsc-pages-ly.json      same, compare_mode='same_period_ly'
  gsc-pq-<sg>.json       MCP query_search_analytics dims=['page','query'], page_match='regex' on the subgroup's slugs, days=90, compare_mode='prev_period', limit=500
  ga4-landing.csv        GA4 Explore export: Landing page × Sessions, Engaged sessions, Engagement rate, Avg engagement time/session, Views/session, Key events, Session key event rate (Organic Search)
  ga4-scroll.csv         GA4 Explore export: Landing page × Event count, filter Event name = scroll
  ga4-matrix.json        MCP get_content_matrix limit=500 (fallback when ga4-landing.csv is missing)"""


def latest_audit_dir() -> Path | None:
    dirs = sorted(p for p in AUDIT_DIR.glob("20*") if p.is_dir()) if AUDIT_DIR.exists() else []
    return dirs[-1] if dirs else None


def median(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else 0


def cmd_report(a):
    d = Path(a.dir) if a.dir else latest_audit_dir()
    if not d or not d.exists():
        print("Chưa có dữ liệu audit.\n" + AUDIT_FILES)
        return 3
    groups = {r["slug"]: r for r in (read_csv(OUT_GROUPS) if OUT_GROUPS.exists() else build_rows())}

    # GSC per page
    gsc: dict[str, dict] = {}
    for f in sorted(d.glob("gsc-pages*.json")):
        if "-ly" in f.name:
            continue
        for r in load_mcp(f):
            s = slug_of(r.get("page", ""))
            if s and r.get("impressions", 0) >= gsc.get(s, {}).get("impressions", -1):
                gsc[s] = r
    ly = {slug_of(r.get("page", "")): r for f in d.glob("gsc-pages-ly*.json") for r in load_mcp(f)}
    ly.pop("", None)

    # Query-level ranking per page
    q: dict[str, list[dict]] = defaultdict(list)
    for f in d.glob("gsc-pq-*.json"):
        for r in load_mcp(f):
            s = slug_of(r.get("page", ""))
            if s:
                q[s].append(r)

    ga4 = load_ga4_csv(d / "ga4-landing.csv")
    scroll = load_ga4_csv(d / "ga4-scroll.csv")
    ga4_src = "ga4-landing.csv"
    if not ga4:
        ga4_src = "ga4-matrix.json (MCP, thiếu scroll/avg time)"
        for r in load_mcp(d / "ga4-matrix.json"):
            s = slug_of(r.get("page", ""))
            if s:
                ga4[s] = {"sessions": r.get("ga4_sessions", 0), "engagement_rate": ratio(r.get("ga4_engagement_rate", 0)),
                          "key_events": r.get("ga4_conversions", 0)}

    rows = []
    for s, g in groups.items():
        r = dict(g)
        p = gsc.get(s, {})
        r.update({
            "clicks": p.get("clicks", 0), "impressions": p.get("impressions", 0), "ctr": p.get("ctr", 0),
            "position": p.get("position", ""), "prev_clicks": p.get("prev_clicks", ""),
            "click_change": p.get("click_change", ""), "position_change": p.get("position_change", ""),
            "ly_clicks": ly.get(s, {}).get("prev_clicks", ""),
        })
        qs = q.get(s, [])
        if qs:
            top = max(qs, key=lambda x: x.get("clicks", 0) or 0)
            r.update({
                "queries": len(qs),
                "top_query": top.get("query", ""), "top_query_pos": round(top.get("position") or 0, 1),
                "q_top3": sum(1 for x in qs if (x.get("position") or 99) <= 3),
                "q_top10": sum(1 for x in qs if (x.get("position") or 99) <= 10),
                "q_11_20": sum(1 for x in qs if 10 < (x.get("position") or 99) <= 20),
                "q_striking": sum(1 for x in qs if 4 <= (x.get("position") or 99) <= 15 and x.get("impressions", 0) >= 20),
                "q_lost_top10": sum(1 for x in qs if (x.get("prev_position") or 99) <= 10 < (x.get("position") or 99)),
            })
        ga = ga4.get(s, {})
        sess = ga.get("sessions", 0) or 0
        r.update({
            "sessions": round(sess), "engaged_sessions": round(ga.get("engaged_sessions", 0) or 0),
            "engagement_rate": round(ga.get("engagement_rate", 0) or 0, 3),
            "avg_engagement_time": round(ga.get("avg_engagement_time", 0) or 0, 1),
            "views_per_session": round(ga.get("views_per_session", 0) or 0, 2),
            "key_events": round(ga.get("key_events", 0) or 0),
            "scroll_rate": round((scroll.get(s, {}).get("event_count", 0) or 0) / sess, 3) if sess else "",
        })
        rows.append(r)

    label_rows(rows)

    fields = FIELDS + ["clicks", "impressions", "ctr", "position", "prev_clicks", "click_change", "position_change",
                       "ly_clicks", "queries", "top_query", "top_query_pos", "q_top3", "q_top10", "q_11_20",
                       "q_striking", "q_lost_top10", "sessions", "engaged_sessions", "engagement_rate",
                       "avg_engagement_time", "views_per_session", "scroll_rate", "key_events", "labels", "priority"]
    rows.sort(key=lambda r: (sg_key(r["subgroup"]), -float(r["priority"])))
    write_csv(OUT_AUDIT, rows, fields)
    print(f"[OK] {OUT_AUDIT.relative_to(ROOT)} ({len(rows)} bài)")
    OUT_REPORT.write_text(render_report(rows, d, ga4_src, bool(q), bool(scroll)), encoding="utf-8")
    print(f"[OK] {OUT_REPORT.relative_to(ROOT)}")
    # URLs Google still shows that are not live articles: renamed/deleted slugs (typo variants with ~1 impr are noise)
    orphans = sorted(((s, r) for s, r in gsc.items() if s not in groups
                      and max(r.get("impressions", 0), r.get("prev_impressions", 0)) >= 50),
                     key=lambda x: -max(x[1].get("impressions", 0), x[1].get("prev_impressions", 0)))
    if orphans:
        with OUT_REPORT.open("a", encoding="utf-8") as f:
            f.write(f"\n## URL có impression nhưng không còn trong snapshot live ({len(orphans)}) — kiểm tra redirect / đổi slug\n\n"
                    "| URL | Clicks | Impr | Clicks kỳ trước | Impr kỳ trước |\n|---|---:|---:|---:|---:|\n")
            for s, r in orphans:
                f.write(f"| `{s}` | {r.get('clicks', 0)} | {r.get('impressions', 0)} | {r.get('prev_clicks', 0)} | {r.get('prev_impressions', 0)} |\n")
        print(f"ℹ️ {len(orphans)} URL có impression nhưng không có trong snapshot live — xem cuối {OUT_REPORT.name}")
    return 0


def label_rows(rows: list[dict]):
    """Diagnostic labels; CTR/engagement thresholds are relative to the subgroup median."""
    by_sg = defaultdict(list)
    for r in rows:
        by_sg[r["subgroup"]].append(r)
    for sg, rs in by_sg.items():
        ctr_med = median([float(r["ctr"]) for r in rs if float(r["impressions"] or 0) >= 100])
        eng_med = median([float(r["avg_engagement_time"]) for r in rs if (r["sessions"] or 0) >= 30])
        er_med = median([float(r["engagement_rate"]) for r in rs if (r["sessions"] or 0) >= 30])
        for r in rs:
            lab = []
            impr, clicks = float(r["impressions"] or 0), float(r["clicks"] or 0)
            pos = float(r["position"] or 99)
            cc = float(r["click_change"] or 0)
            if impr == 0:
                lab.append("dead")
            if cc <= -10 and r["prev_clicks"] and cc / max(float(r["prev_clicks"]), 1) <= -0.2 or (r.get("q_lost_top10") or 0) >= 3:
                lab.append("rank-drop")
            if impr >= 300 and pos <= 8 and ctr_med and float(r["ctr"]) < 0.7 * ctr_med:
                lab.append("ctr-low")
            if (r.get("q_striking") or 0) >= 5 or (not r.get("queries") and 4 <= pos <= 15 and impr >= 300):
                lab.append("striking")
            sess = r["sessions"] or 0
            if sess >= 30 and ((eng_med and r["avg_engagement_time"] and r["avg_engagement_time"] < 0.7 * eng_med)
                               or (er_med and r["engagement_rate"] < 0.85 * er_med)):
                lab.append("engage-low")
            if sess >= 100 and r["engagement_rate"] >= (er_med or 0) and not r["key_events"]:
                lab.append("convert-low")
            r["labels"] = " ".join(lab)
            lost = max(-cc, 0)
            potential = impr * max(ctr_med / 100 if ctr_med else 0, 0) - clicks if "ctr-low" in lab or "striking" in lab else 0
            r["priority"] = round(lost + max(potential, 0) + (r.get("q_striking") or 0), 1)


def render_report(rows: list[dict], d: Path, ga4_src: str, has_q: bool, has_scroll: bool) -> str:
    def agg(rs):
        clicks = sum(float(r["clicks"] or 0) for r in rs)
        impr = sum(float(r["impressions"] or 0) for r in rs)
        prev = sum(float(r["prev_clicks"] or 0) for r in rs)
        sess = sum(r["sessions"] or 0 for r in rs)
        w = lambda k: (sum((r[k] or 0) * (r["sessions"] or 0) for r in rs) / sess) if sess else 0
        pos_w = (sum(float(r["position"] or 0) * float(r["impressions"] or 0) for r in rs) / impr) if impr else 0
        lab = Counter(x for r in rs for x in r["labels"].split())
        return {
            "n": len(rs), "clicks": clicks, "impr": impr, "ctr": clicks / impr * 100 if impr else 0, "pos": pos_w,
            "delta": (clicks - prev) / prev * 100 if prev else 0, "zero": sum(1 for r in rs if not float(r["clicks"] or 0)),
            "top10": sum(r.get("q_top10") or 0 for r in rs), "striking": sum(r.get("q_striking") or 0 for r in rs),
            "sess": sess, "er": w("engagement_rate"), "time": w("avg_engagement_time"),
            "scroll": w("scroll_rate") if has_scroll else None, "ke": sum(r["key_events"] or 0 for r in rs),
            "inlink": statistics.mean(float(r["in_contextual"] or 0) for r in rs), "lab": lab,
            "prio": sum(float(r["priority"]) for r in rs),
        }

    def pct(x):
        return f"{x:+.0f}%" if x else "–"

    by_sg = defaultdict(list)
    for r in rows:
        by_sg[r["subgroup"] or "–"].append(r)
    L = [f"# Performance theo nhóm bài /kien-thuc",
         f"",
         f"Nguồn: `{d.relative_to(ROOT)}` · GA4: {ga4_src} · ranking query: {'có' if has_q else 'chưa có (thiếu gsc-pq-*.json)'} · "
         f"sinh bởi `python scripts/page_groups.py report`. Chi tiết từng bài: `knowledge/3-pipeline/page-audit.csv`.",
         "",
         "Lưu ý số liệu: GSC 90 ngày so 90 ngày trước. Chỉ số query (top 10, striking) tính trên tối đa 500 cặp page×query "
         "nhiều impression nhất của mỗi nhóm con — đủ cho query chính, thiếu đuôi dài. "
         + ("GA4 lấy từ MCP Content Matrix: mọi kênh (không riêng Organic), không có thời gian tương tác/scroll — "
            "export GA4 theo spec trong `page_groups.py` (AUDIT_FILES) để có đủ." if ga4_src.startswith("ga4-matrix") else
            "GA4: export Organic Search từ GA4 Explore."),
         "",
         "Bản đồ cụm + link pillar/hub: [`internal-links/topical-map.html`](internal-links/topical-map.html) (bấm tên nhóm con bên dưới để mở đúng nhóm).",
         "",
         "Nhãn: `rank-drop` mất clicks/top 10 · `ctr-low` pos ≤ 8 nhưng CTR < 70% trung vị nhóm · `striking` ≥ 5 query pos 4–15 · "
         "`engage-low` thời gian/tỷ lệ tương tác dưới trung vị nhóm · `convert-low` đọc tốt nhưng 0 key event · `dead` 0 impression.",
         "",
         "## Theo cluster", "",
         "| Cluster | Bài | Clicks | Δ kỳ trước | Impr | CTR | Pos | Sessions | Eng. rate | Time (s) | Key events |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for cl, name in CLUSTERS.items():
        rs = [r for r in rows if r["cluster"] == cl]
        if not rs:
            continue
        g = agg(rs)
        L.append(f"| {cl}. {name} | {g['n']} | {g['clicks']:,.0f} | {pct(g['delta'])} | {g['impr']:,.0f} | {g['ctr']:.2f}% | "
                 f"{g['pos']:.1f} | {g['sess']:,} | {g['er']:.0%} | {g['time']:.0f} | {g['ke']} |")
    L += ["", "## Theo nhóm con (thứ tự audit = điểm ưu tiên giảm dần)", "",
          "| Nhóm | Bài | Clicks | Δ | CTR | Pos | 0 click | Query top10 | Striking | Sessions | Eng. | Time (s) | Scroll | KE | Inlink TB | Nhãn | Ưu tiên |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|"]
    stats = sorted(((sg, agg(rs)) for sg, rs in by_sg.items()), key=lambda x: -x[1]["prio"])
    for sg, g in stats:
        lab = ", ".join(f"{k} {v}" for k, v in g["lab"].most_common(4))
        sc = f"{g['scroll']:.0%}" if g["scroll"] is not None else "–"
        L.append(f"| [{sg} {SUBGROUPS.get(sg, 'unassigned')}](internal-links/topical-map.html#{sg}) | {g['n']} | {g['clicks']:,.0f} | {pct(g['delta'])} | {g['ctr']:.2f}% | "
                 f"{g['pos']:.1f} | {g['zero']} | {g['top10']} | {g['striking']} | {g['sess']:,} | {g['er']:.0%} | "
                 f"{g['time']:.0f} | {sc} | {g['ke']} | {g['inlink']:.1f} | {lab} | {g['prio']:,.0f} |")
    L += ["", "## Theo dạng bài (intent)", "", "| Intent | Bài | Clicks | CTR | Pos | Eng. | Time (s) |", "|---|---:|---:|---:|---:|---:|---:|"]
    by_int = defaultdict(list)
    for r in rows:
        by_int[r["intent"]].append(r)
    for it, rs in sorted(by_int.items(), key=lambda x: -len(x[1])):
        g = agg(rs)
        L.append(f"| {it} | {g['n']} | {g['clicks']:,.0f} | {g['ctr']:.2f}% | {g['pos']:.1f} | {g['er']:.0%} | {g['time']:.0f} |")
    dead = [r["slug"] for r in rows if "dead" in r["labels"]]
    L += ["", f"## Bài 0 impression ({len(dead)}) — xem xét prune/merge", "", ", ".join(f"`{s}`" for s in dead) or "–", ""]
    return "\n".join(L)


def main():
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--show", help="Subgroup (3d), cluster (3) hoặc 'unassigned' — chỉ in, không ghi file")
    sub.add_parser("taxonomy")
    r = sub.add_parser("report")
    r.add_argument("--dir", help="Thư mục audit (mặc định: mới nhất trong knowledge/raw/audit/)")
    a = ap.parse_args()
    return {"build": cmd_build, "taxonomy": cmd_taxonomy, "report": cmd_report}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
