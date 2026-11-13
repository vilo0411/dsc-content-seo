"""Append clusters C3–C11 (from page-groups.csv) to link-clusters.json. Existing clusters untouched."""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1])
MOVED_OUT = {"huong-dan-mo-tai-khoan-chung-chi-quy"}
F = ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json"
data = json.loads(F.read_text(encoding="utf-8"))
data["clusters"] = [c for c in data["clusters"] if not re.match(r"c\d+-", c["id"])]  # idempotent: drop previously generated
# moved to C7 (2026-11-10 decision): opening a fund account belongs to the fund cluster
for c in data["clusters"]:
    c["groups"] = [g_ for g_ in c["groups"] if not re.match(r"\d+[a-z] ", g_["name"])]  # drop previously appended C1/C2 leftovers
    for g_ in c["groups"]:
        g_["spokes"] = [s for s in g_["spokes"] if s not in MOVED_OUT]

registered = set()

for c in data["clusters"]:
    registered.add(c["pillar"])
    for g in c["groups"]:
        registered.update(([g["hub"]] if g.get("hub") else []) + g["spokes"])

rows = list(csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-groups.csv", encoding="utf-8")))
by_sg = defaultdict(list)
for r in rows:
    if r["slug"] not in registered:
        by_sg[r["subgroup"]].append(r)

# cluster -> (id, name, pillar or None, pillar_keyword, pillar_anchors, note)
CL = {
    "3": ("c3-phan-tich-ky-thuat", "Phân tích kỹ thuật & Chỉ báo", "phan-tich-ky-thuat-la-gi", "phân tích kỹ thuật là gì",
          ["phân tích kỹ thuật là gì"], "Pillar yếu (0 click, pos 16) — cần viết lại."),
    "4": ("c4-phan-tich-co-ban", "Phân tích cơ bản & Tài chính DN", "phan-tich-co-ban-la-gi", "phân tích cơ bản là gì",
          ["phân tích cơ bản là gì"], "Pillar chỉ 6% bài cụm link về — cần nâng cấp."),
    "5": ("c5-co-phieu-nganh", "Cổ phiếu cụ thể & Ngành", None, "", [],
          "CHƯA CÓ PILLAR — cần viết trang tổng cổ phiếu theo ngành. Hub = trang ngành / top ngành."),
    "6": ("c6-chien-luoc-rui-ro", "Chiến lược, Phương pháp & Quản trị rủi ro",
          "cac-chien-luoc-dau-tu-chung-khoan-pho-bien-tren-thi-truong", "các chiến lược đầu tư chứng khoán phổ biến",
          ["các chiến lược đầu tư chứng khoán phổ biến"], "Pillar tạm (pos 40) — cân nhắc viết bài phương pháp đầu tư."),
    "7": ("c7-quy-etf", "Quỹ & ETF", "chung-chi-quy-la-gi", "chứng chỉ quỹ là gì",
          ["chứng chỉ quỹ là gì"], "Pillar yếu (pos 41.8) — cần làm lại."),
    "8": ("c8-phai-sinh", "Phái sinh & Chứng quyền", "chung-khoan-phai-sinh-la-gi-huong-dan-dau-tu-cho-nguoi-moi-bat-dau",
          "chứng khoán phái sinh là gì", ["chứng khoán phái sinh là gì"], ""),
    "9": ("c9-vi-mo", "Vĩ mô & Chính sách", "phan-tich-vi-mo-trong-dau-tu-chung-khoan-la-gi", "phân tích vĩ mô trong đầu tư chứng khoán",
          ["phân tích vĩ mô trong đầu tư chứng khoán"], ""),
    "10": ("c10-tiet-kiem-kenh-dau-tu", "Tiết kiệm & Kênh đầu tư", "co-tien-nen-dau-tu-gi-luc-nay", "có tiền nên đầu tư gì",
           ["có tiền nên đầu tư gì"], "Pillar = bài kênh đầu tư tổng (109 clicks). 10d = ngoài phạm vi, không bắt link pillar."),
    "11": ("c11-vang", "Vàng", "cach-dau-tu-vang", "cách đầu tư vàng",
           ["cách đầu tư vàng"], "Pillar yếu (pos 19.6) — /optimize trước khi chèn link."),
    "12": ("c12-trai-phieu", "Trái phiếu", "trai-phieu-la-gi", "trái phiếu là gì", ["trái phiếu là gì"], ""),
    "13": ("c13-hoc-nghe", "Học & nghề tài chính", None, "", [],
           "Không có pillar bắt buộc: sách/khoá học link về pillar của chủ đề (PTKT → C3, BCTC → C4)."),
    "14": ("c14-bac", "Bạc", "dau-tu-bac-co-nen-khong", "đầu tư bạc", ["đầu tư bạc"],
           "Cầu nối với C11: nen-dau-tu-vang-hay-bac (thuộc C11, link cả 2 pillar)."),
}
HUB = {
    # hub = bài tổng quan bao trùm cả nhóm; không có bài như vậy -> không đặt hub (ghi vào danh sách cần viết)
    "3a": "cac-chi-bao-xac-dinh-xu-huong-dang-tin-cay-trong-phan-tich-ky-thuat",
    "3c": "phuong-phap-dau-tu-theo-dong-tien-hieu-qua",
    "3d": "tu-dien-30-mo-hinh-nen-pho-bien-tren-thi-truong-chung-khoan",
    "3e": "cac-mo-hinh-gia-trong-chung-khoan", "3g": "chi-bao-ky-thuat",
    "4a": "cach-phan-tich-bao-cao-tai-chinh", "4b": "cac-chi-so-phan-tich-bao-cao-tai-chinh",
    "4c": "cach-dinh-gia-co-phieu-cho-nguoi-moi-bat-dau", "4d": "cac-chi-so-phan-tich-bao-cao-tai-chinh",
    "4f": "co-tuc-la-gi", "4g": "cach-phan-tich-bao-cao-tai-chinh",
    "4h": "phan-tich-doanh-nghiep-trong-dau-tu-chung-khoan-la-gi",
    "5a": "top-5-co-phieu-ngan-hang-dinh-gia-hop-ly-tiem-nang-but-pha-manh",
    "5b": "top-5-co-phieu-bat-dong-san-co-the-buoc-vao-song-tang-giai-doan-cuoi-nam",
    "5c": "top-5-co-phieu-nganh-thep-co-co-ban-tot-sap-buoc-vao-chu-ky-tang-truong-moi",
    "5d": "co-phieu-nganh-nang-luong", "5e": "co-phieu-nganh-ban-le",
    "5f": "top-5-co-phieu-nganh-chung-khoan-dang-dau-tu-nhat", "5g": "top-co-phieu-cang-bien-nen-dau-tu",
    "5h": "co-phieu-nganh-nong-nghiep", "5i": "co-phieu-nganh-cong-nghe",
    "5j": "huong-dan-phan-tich-nganh-trong-dau-tu-chung-khoan",
    "5k": "co-phieu-la-gi-cac-loai-co-phieu-tren-thi-truong-chung-khoan-viet-nam",
    "5l": "top-co-phieu-hang-khong-nen-dau-tu", "5m": "co-phieu-nganh-hoa-chat", "5n": "co-phieu-nganh-det-may",
    "5o": "top-5-co-phieu-dang-dau-tu",
    "6c": "quan-tri-rui-ro-la-gi-2", "6d": "thien-kien-nhan-thuc-la-gi",
    "8b": "chung-quyen-la-gi-chung-quyen-co-bao-dam-la-gi-tim-hieu-chung-quyen-tai-viet-nam",
    "9b": "so-sanh-chinh-sach-tai-khoa-va-chinh-sach-tien-te", "9d": "can-can-thanh-toan-bop-la-gi",
    "9e": "kinh-te-hoc-vi-mo-la-gi-y-nghia-trong-dau-tu-chung-khoan",
    "9f": "khung-hoang-tai-chinh-la-gi-cac-giai-doan-cua-khung-hoang-tai-chinh",
    "10a": "lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat",
}
# groups whose members are not required to link the cluster pillar (off-topic for it)
PILLAR_EXEMPT = {"8b": "chứng quyền không thuộc phái sinh — link pillar chỉ khi đoạn văn so sánh",
                 "10d": "ngoài phạm vi chứng khoán/tiết kiệm"}
CROSS = {"14": ["nen-dau-tu-vang-hay-bac"], "11": ["dau-tu-bac-co-nen-khong"], "7": ["quy-trai-phieu-la-gi"], "12": ["quy-trai-phieu-la-gi"]}
sys.path.insert(0, str(ROOT / "scripts"))
from page_groups import SUBGROUPS  # noqa: E402

live = {r["slug"] for r in rows}
added = 0
# C1/C2 keep their October registry (mo-tai-khoan / cach-choi-chung-khoan); pages it missed are appended as extra groups
LEGACY = {"1a": "mo-tai-khoan"}  # everything else of C1/C2 -> cach-choi-chung-khoan (where Oct put lệnh & quy định)
LEGACY_HUB = {"1b": "lenh-ato-atc-lo-mp-la-gi", "2b": "cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau",
              "2d": "chi-so-chung-khoan-la-gi"}
LEGACY_EXEMPT = {"2d": "chỉ số thế giới lệch chủ đề pillar người mới — bài chỉ số VN link pillar khi hợp ngữ cảnh"}
byid = {c["id"]: c for c in data["clusters"]}
for sg in sorted(s for s in by_sg if re.match(r"\d+", s).group() in ("1", "2")):
    c = byid[LEGACY.get(sg, "cach-choi-chung-khoan")]
    hub = LEGACY_HUB.get(sg)
    grp = {"name": f"{sg} {SUBGROUPS[sg]}", "hub": hub,
           "spokes": sorted(r["slug"] for r in by_sg[sg] if r["slug"] not in (hub, c["pillar"]))}
    if sg in LEGACY_EXEMPT:
        grp["pillar_exempt"] = LEGACY_EXEMPT[sg]
    c["groups"].append(grp)
    added += len(by_sg[sg])
for cl, (cid, name, pillar, kw, anchors, note) in CL.items():
    if not any(re.match(r"\d+", s).group() == cl for s in by_sg):
        continue
    assert pillar is None or pillar in live, pillar
    groups = []
    for sg in sorted((s for s in by_sg if re.match(r"\d+", s).group() == cl), key=lambda s: s):
        hub = HUB.get(sg)
        assert hub is None or hub in live, hub
        spokes = sorted(r["slug"] for r in by_sg[sg] if r["slug"] not in (pillar, hub))
        grp = {"name": f"{sg} {SUBGROUPS[sg]}", "hub": hub, "spokes": spokes}
        if sg in PILLAR_EXEMPT:
            grp["pillar_exempt"] = PILLAR_EXEMPT[sg]
        groups.append(grp)
        added += len(spokes) + (1 if hub else 0)
    c = {"id": cid, "name": name, "pillar": pillar, "pillar_keyword": kw, "pillar_anchors": anchors,
         "cross": CROSS.get(cl, []), "groups": groups}
    if note:
        c["note"] = note
    data["clusters"].append(c)

data["_doc"] = (data["_doc"].split(" Cụm c3–c1")[0] +
                " Cụm c3–c14 (2026-11-10) sinh từ knowledge/3-pipeline/page-groups.csv (scripts/page_groups.py): group = nhóm con, "
                "hub = bài tổng của nhóm; pillar null = cụm chưa có bài pillar (qa_lint chỉ kiểm hub); "
                "group có pillar_exempt = bài lệch chủ đề với pillar, không bắt link pillar (chỉ kiểm hub). "
                "Bài đã thuộc cụm mo-tai-khoan / cach-choi-chung-khoan không lặp lại ở cụm khác.")
F.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("clusters", len(data["clusters"]), "slugs added", added)
