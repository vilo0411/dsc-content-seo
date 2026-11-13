"""Draft tier-3 (sub-hub) tree for every subgroup → topical-tree-proposal.md. MECE check: each article in exactly one leaf.

Leaf rules are ordered regexes on the slug (first match wins). Ticker subgroups (5a–5i, 5l–5n) are split per ticker
automatically: sub-hub = the ticker's "co-phieu-xxx-tong-quan…" page, members = cách mua / có nên mua of that ticker.
"""
import csv, json, re
from collections import defaultdict, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
rows = list(csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-audit.csv", encoding="utf-8")))
reg = json.loads((ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").read_text(encoding="utf-8"))
SUB = {}
exec((ROOT / "scripts/page_groups.py").read_text(encoding="utf-8").split("SUBGROUPS = ")[1].split("\n}\n")[0].join(["SUB.update(", "\n})"]))
HUB2 = {g["name"].split()[0]: g["hub"] for c in reg["clusters"] for g in c["groups"] if re.match(r"\d+[a-z] ", g["name"])}
HUB2.update({"1a": "cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam", "1b": "cac-quy-dinh-giao-dich-chung-khoan-quan-trong-ma-nguoi-moi-can-biet",
             "2a": "cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau", "2b": "cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau",
             "2d": "chi-so-chung-khoan-la-gi", "2f": None})
PILLAR = {"1": "cach-mo-tai-khoan-chung-khoan", "2": "cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau"}
for c in reg["clusters"]:
    m = re.match(r"c(\d+)-", c["id"])
    if m:
        PILLAR[m.group(1)] = c.get("pillar")

# (leaf id, name, sub-hub slug or None, regex)
T = {
 "1a": [("1a.4", "App, sàn ảo & chọn CTCK", "app-dau-tu-chung-khoan", r"app|chung-khoan-ao|nen-mo|san-dau-tu"),
        ("1a.2", "Phí & thuế giao dịch", "phi-giao-dich-chung-khoan", r"(^|-)phi(-|$)|thue"),
        ("1a.3", "Margin & đòn bẩy", "margin-la-gi", r"margin|force-sell|don-bay"),
        ("1a.1", "Mở & loại tài khoản", "cach-mo-tai-khoan-chung-khoan", r"tai-khoan|luu-ky")],
 "1b": [("1b.1", "Lệnh & khớp lệnh", "lenh-ato-atc-lo-mp-la-gi", r"lenh|stop-loss|thoa-thuan|lo-le"),
        ("1b.2", "Giờ, biên độ, giá & bảng giá", "cac-quy-dinh-giao-dich-chung-khoan-quan-trong-ma-nguoi-moi-can-biet", r".")],
 "2d": [("2d.1", "Chỉ số Việt Nam", "cac-chi-so-chung-khoan-viet-nam-hieu-ro-ve-vn-index-vn-30-hnx-index-va-nhieu-chi-so-khac", r"vn-|vn30|hnx|viet-nam"),
        ("2d.2", "Chỉ số thế giới", "cac-chi-so-chung-khoan-chau-a-noi-bat", r".")],
 "13a": [("13a.2", "Sách & giáo trình (link về pillar chủ đề: PTKT → C3, BCTC → C4)", "nhung-cuon-sach-hay-ve-dau-tu-chung-khoan", r"cuon-sach|^sach|giao-trinh"),
         ("13a.1", "Khoá học & nguồn học", "khoa-hoc-chung-khoan", r".")],
 "13b": [("13b.1", "Chứng chỉ", "chung-chi-tai-chinh", r"chung-chi|cfa|acca"),
         ("13b.2", "Nghề tư vấn, môi giới & thu nhập", "PEER", r".")],
 "2f": [("2f.1", "Thị trường tài chính & cấu trúc", "thi-truong-tai-chinh-la-gi", r"thi-truong-(tai-chinh|von|so-cap|bo)|nyse|sec-la|cong-cu-tai-chinh|nguon-goc|tieu-diem|phan-hoa"),
        ("2f.2", "Chủ thể & hành vi trên thị trường", None, r"tu-doanh|tao-lap|thao-tung|noi-gian|ban-khong|wash-out|giau-nhat"),
        ("2f.3", "Thuật ngữ giao dịch", "cac-thuat-ngu-trong-chung-khoan", r".")],
 "3a": [("3a.2", "MACD", "macd-la-gi", r"macd"),
        ("3a.1", "Đường trung bình động", "duong-ma-la-gi", r"ma|ema|wma|hull|dema|moving-average|trung-binh|golden-cross"),
        ("3a.3", "Chỉ báo sức mạnh/hướng xu hướng (ADX, DMI, Aroon, SAR, Ichimoku, Supertrend)", None, r".")],
 "3b": [("3b.1", "RSI & phân kỳ", "chi-so-rsi-la-gi", r"rsi|phan-ky|vung-qua"),
        ("3b.2", "Dao động khác (CCI, Momentum, ROC, Williams, RS)", None, r".")],
 "3f": [("3f.3", "Bẫy giá, breakout & gap", None, r"trap|bay-gia|break|gap"),
        ("3f.1", "Hỗ trợ – kháng cự & đỉnh đáy", "duong-ho-tro-va-khang-cu-la-gi", r"ho-tro|dinh|day|pivot"),
        ("3f.2", "Xu hướng & kênh giá", "giao-dich-theo-xu-huong-trend-following-la-gi", r".")],
 "3h": [("3h.1", "Lý thuyết giá (Dow, Elliott, Fibonacci, Wyckoff)", None, r"dow|elliott|fibonacci|wyckoff|ngau-nhien|phan-biet"),
        ("3h.2", "Biểu đồ & công cụ vẽ", "bieu-do-chung-khoan-la-gi-cach-xem-bieu-do-chung-khoan", r".")],
 "4a": [("4a.2", "Doanh thu, chi phí & lợi nhuận", "chi-tieu-loi-nhuan-cua-doanh-nghiep", r"chi-phi|capex|hoa-von|chi-tieu|doanh-thu|q-o-q|yoy"),
        ("4a.1", "Báo cáo tài chính & cách đọc", "huong-dan-cach-doc-bao-cao-tai-chinh-nhung-thong-tin-quan-trong", r".")],
 "4c": [("4c.2", "Định giá chiết khấu dòng tiền", "dcf-la-gi", r"dcf|wacc|npv|irr|gia-tri-doanh-nghiep|noi-tai|cagr|quy-tac-72"),
        ("4c.1", "Chỉ số định giá tương đối", None, r".")],
 "4d": [("4d.3", "Hiệu quả hoạt động (vòng quay)", None, r"vong-quay|so-ngay|thoi-gian-thu-hoi"),
        ("4d.2", "Đòn bẩy & cơ cấu nợ", "don-bay-tai-chinh-la-gi-uu-va-nhuoc-diem-cach-su-dung", r"don-bay|gearing|no-tren|dar|no-dai-han|co-cau-von"),
        ("4d.1", "Khả năng thanh toán", "he-so-thanh-toan-la-gi", r".")],
 "4e": [("4e.3", "IPO, niêm yết & M&A", "niem-yet-chung-khoan-ipo-la-gi-nhung-dieu-can-biet", r"ipo|niem-yet|m-a"),
        ("4e.2", "Loại cổ phần & sự kiện cổ phần", "so-sanh-co-phieu-thuong-va-co-phieu-uu-dai", r"co-phieu|chia-tach|pha-loang|free-float|mua-lai"),
        ("4e.1", "Vốn doanh nghiệp", "von-chu-so-huu-la-gi", r".")],
 "6b": [("6b.1", "Phong cách giao dịch theo thời gian", "trading-trong-chung-khoan-la-gi", r"day-?trading|swing|position|ngan-han|^trading"),
        ("6b.2", "Chiến lược & công cụ đầu tư", None, r".")],
 "6c": [("6c.3", "Kỷ luật giao dịch: chốt lời, cắt lỗ, R:R, drawdown", "ty-le-risk-reward-la-gi", r"take-profit|risk-reward|cat-lo|drawdown"),
        ("6c.2", "Lý thuyết danh mục: Markowitz, CAPM, beta, độ lệch chuẩn, tương quan", "danh-muc-dau-tu-hieu-qua-la-gi",
         r"danh-muc|markowitz|capm|tuong-quan|phan-bo|beta|do-lech-chuan|volatility"),
        ("6c.1", "Các loại rủi ro & khẩu vị", "rui-ro-la-gi", r".")],
 "7a": [("7a.2", "ETF", "etf-la-gi", r"etf"),
        ("7a.3", "Uỷ thác & NAV", None, r"uy-thac|nav-la-gi"),
        ("7a.1", "Quỹ mở & chứng chỉ quỹ", "quy-mo-la-gi-tong-quan-ve-quy-mo-tren-thi-truong-chung-khoan-viet-nam", r".")],
 "9a": [("9a.2", "Lạm phát & chỉ số giá", "lam-phat-la-gi", r"lam-phat|giam-phat|cpi|ppi|pce"),
        ("9a.3", "Chu kỳ & suy thoái", "chu-ky-kinh-te-la-gi-cach-van-dung-chu-ky-kinh-te-de-dau-tu-co-phieu-hieu-qua", r"chu-ky|suy-thoai"),
        ("9a.1", "Tăng trưởng & sản lượng", "gdp-la-gi", r".")],
 "9b": [("9b.3", "Lãi suất", "lai-suat-la-gi", r"lai-suat"),
        ("9b.2", "Chính sách tài khoá", "chinh-sach-tai-khoa-la-gi", r"tai-khoa|dau-tu-cong|no-chinh-phu|chinh-sach-cong"),
        ("9b.1", "Chính sách tiền tệ & ngân hàng trung ương", "chinh-sach-tien-te-la-gi", r".")],
 "9e": [("9e.1", "Cạnh tranh & cấu trúc thị trường", "canh-tranh-la-gi", r"canh-tranh|tro-choi|zero-sum|quan-ly-thi-truong"),
        ("9e.2", "Cung cầu, giá & chi phí", None, r".")],
 "10b": [("10b.1", "Vốn nhỏ (≤ 20 triệu, sinh viên)", "PEER", r"^co-(2|3|5|10|15|20)-trieu|sinh-vien"),
         ("10b.2", "Vốn vừa (30–200 triệu)", "PEER", r"^co-(30|40|50|70|150|200)-trieu|100-trieu"),
         ("10b.3", "Vốn lớn (≥ 300 triệu)", "PEER", r"^co-(300|400|600)-trieu|^co-1-ty"),
         ("10b.4", "So sánh kênh & nguyên tắc", None, r".")],
 "11a": [("11a.0", "Tài liệu & kênh gián tiếp", None, r"^sach|etf"),
         ("11a.3", "So sánh kênh (vàng vs tiết kiệm / chứng khoán / bạc)", "PEER", r"hay-gui|tiet-kiem|so-sanh|hay-bac"),
         ("11a.1", "Chọn loại vàng & nơi mua", "dau-tu-vang-nen-mua-loai-nao", r"nen-mua-vang|loai-nao|app|san-giao-dich"),
         ("11a.2", "Thời điểm & giá vàng", "co-nen-dau-tu-vang-thoi-diem-nay", r".")],
}
TICKER_SG = {"5a", "5b", "5c", "5d", "5e", "5f", "5g", "5h", "5i", "5l", "5m", "5n"}
sector = {r["ticker"]: r["subgroup"] for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/ticker-sector.csv", encoding="utf-8"))}
live = {r["slug"] for r in rows}

by = defaultdict(list)
for r in rows:
    by[r["subgroup"]].append(r)

ALIAS = {"novaland": "NVL", "vingroup": "VIC", "hoa-phat": "HPG", "vinamilk": "VNM", "techcombank": "TCB",
         "petrolimex": "PLX", "vietnam-airlines": "HVN", "vietcombank": "VCB"}
def ticker(slug):
    for k, v in ALIAS.items():
        if k in slug:
            return v
    for tok in slug.split("-"):
        if tok.upper() in sector and len(tok) == 3:
            return tok.upper()
    return None

out, problems, leaves, BR = [], [], {}, {}
EXEMPT = {g["name"].split()[0]: g["pillar_exempt"] for c in reg["clusters"] for g in c["groups"] if g.get("pillar_exempt")}
for cl in sorted({r["cluster"] for r in rows}, key=int):
    out.append(f"\n## C{cl} · pillar: `{PILLAR.get(cl) or ('— (không cần: link về pillar theo chủ đề)' if cl == '13' else 'CHƯA CÓ')}`\n")
    for sg in sorted({r["subgroup"] for r in rows if r["cluster"] == cl}, key=lambda s: (len(s), s)):
        members = by[sg]
        h2 = HUB2.get(sg)
        out.append(f"### {sg} {SUB.get(sg, '')} — {len(members)} bài · hub: `{h2 or '—'}`" + (f" · ⚠️ không bắt link pillar ({EXEMPT[sg]})" if sg in EXEMPT else ""))
        tree = OrderedDict()
        if sg in T:
            for s_ in members:
                if s_["slug"] in (h2, PILLAR.get(cl)):
                    continue
                for lid, name, hub, rx in T[sg]:
                    if re.search(rx, s_["slug"]):
                        tree.setdefault((lid, name, hub), []).append(s_)
                        break
        elif sg in TICKER_SG:
            for s_ in members:
                if s_["slug"] in (h2,):
                    continue
                tk = ticker(s_["slug"])
                key = (f"{sg}.{tk}", f"Mã {tk}", None) if tk else (f"{sg}.0", "Trang ngành / bài chung", None)
                tree.setdefault(key, []).append(s_)
            # sub-hub of a ticker = its overview page
            fixed = OrderedDict()
            for (lid, name, _), ms in tree.items():
                ov = next((m["slug"] for m in ms if re.match(r"co-phieu-[a-z0-9-]+-(tong-quan|danh-gia|dinh-gia|trien-vong|tiem-nang|phan-tich)", m["slug"])
                           or re.fullmatch(r"co-phieu-[a-z]{3}", m["slug"])), None)
                fixed[(lid, name, ov if len(ms) > 1 else None)] = ms
            # tickers with a single article are not a branch: they link straight to the subgroup hub
            tree = OrderedDict()
            for k, ms in fixed.items():
                tree.setdefault(k if len(ms) > 1 else (f"{sg}.0", "Mã chỉ có 1 bài + trang ngành (link thẳng hub nhóm)", None), []).extend(ms)
        else:
            out.append(f"- (không chia tầng 3 — {len(members)} bài link thẳng hub cấp 2)\n")
            continue
        merged = OrderedDict()
        for (lid, name, hub), ms in tree.items():
            key = next((k for k in merged if k[1] == name and k[0].rstrip("b") == lid.rstrip("b")), (lid.rstrip("b"), name, hub))
            merged.setdefault(key, []).extend(ms)
        BR[sg] = [(lid, name, hub, [m["slug"] for m in ms]) for (lid, name, hub), ms in sorted(merged.items(), key=lambda kv: kv[0][0])]
        for (lid, name, hub), ms in sorted(merged.items(), key=lambda kv: kv[0][0]):
            if hub and hub != "PEER" and hub not in live:
                problems.append(f"{lid}: sub-hub `{hub}` không có trên site")
            leaves[lid] = len(ms)
            hubtxt = "— link chéo các bài cùng nhánh + pillar/hub nhóm" if hub == "PEER" else f"`{hub}`" if hub else ("→ link thẳng hub nhóm" if lid.endswith(".0") else "**chưa có bài tổng quan**")
            rest = [m for m in ms if m["slug"] != hub]
            out.append(f"- **{lid} {name}** ({len(ms)}) · sub-hub {hubtxt}")
            out.append("  - " + " · ".join(f"{m['title'][:55]} ({m['clicks']})" for m in rest[:40]))
        out.append("")

seen = defaultdict(int)
total_leaf = sum(leaves.values())
hdr = ["# Đề xuất cây topical cluster 3 tầng (pillar → hub nhóm → sub-hub → bài)", "",
       f"Sinh bởi `{Path(__file__).name}` từ page-audit.csv · {len(rows)} bài · {len(leaves)} nhánh lá ở các nhóm có chia tầng 3.",
       "Quy tắc link: bài → sub-hub của nhánh; sub-hub → hub nhóm; hub nhóm → pillar; pillar link xuống hub nhóm, hub nhóm link xuống sub-hub.",
       "Nhóm cổ phiếu chia theo mã: trang tổng quan mã là sub-hub, bài 'cách mua' / 'có nên mua' cùng mã link về nó.", ""]
if problems:
    hdr += ["**Cảnh báo:** " + "; ".join(problems), ""]
(ROOT / "knowledge/3-pipeline/internal-links/topical-tree-proposal.md").write_text("\n".join(hdr + out) + "\n", encoding="utf-8")
# write tier 3 into the registry: group.branches = [{id, name, subhub|None, peer, spokes}]
nb = 0
for c in reg["clusters"]:
    for g in c["groups"]:
        m = re.match(r"(\d+[a-z]) ", g["name"])
        g.pop("branches", None)
        if not m or m.group(1) not in BR:
            continue
        mem = set(([g["hub"]] if g.get("hub") else []) + g["spokes"])
        brs = []
        for lid, name, hub, slugs in BR[m.group(1)]:
            sub = hub if hub and hub != "PEER" and hub != g.get("hub") and hub != c.get("pillar") and hub in live else None
            sp = [s for s in slugs if s in mem and s not in (sub, g.get("hub"))]
            if not sp:
                continue
            b = {"id": lid, "name": name, "subhub": sub, "spokes": sp}
            if hub == "PEER":
                b["peer"] = True
            brs.append(b); nb += 1
        if brs:
            g["branches"] = brs
reg["_doc"] = reg["_doc"].split(" Tầng 3:")[0] + (" Tầng 3: group.branches (sinh bởi plans/2026-11-10-tier3.gen.py — chạy lại sau gen-clusters): "
              "spoke trong branch link về subhub (LINK-subhub); peer=true = các bài cùng nhánh link chéo, không có subhub.")
(ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("leaves", len(leaves), "branches in registry", nb, "problems", problems)
