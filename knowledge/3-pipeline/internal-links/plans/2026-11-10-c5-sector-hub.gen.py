"""Draft link_plan spec for C5: each stock article -> its sector page via an existing phrase (wrap only)."""
import csv, json, re, html as H
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(r"E:\project\seo-writer-agent-main")
LIVE = ROOT / "knowledge/raw/live/html"
reg = json.loads((ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").read_text(encoding="utf-8"))
c5 = next(c for c in reg["clusters"] if c["id"] == "c5-co-phieu-nganh")
hub_of = {}
for g in c5["groups"]:
    for s in g["spokes"]:
        hub_of[s] = g["hub"]
hubs = {g["hub"] for g in c5["groups"] if g.get("hub")}
audit = {r["slug"]: r for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-audit.csv", encoding="utf-8"))}

# sector word (lowercase, accented) -> sector page
SECTOR = [
    ("ngân hàng", "top-5-co-phieu-ngan-hang-dinh-gia-hop-ly-tiem-nang-but-pha-manh"),
    ("bất động sản", "top-5-co-phieu-bat-dong-san-co-the-buoc-vao-song-tang-giai-doan-cuoi-nam"),
    ("bất động sản khu công nghiệp", "top-5-co-phieu-bat-dong-san-co-the-buoc-vao-song-tang-giai-doan-cuoi-nam"),
    ("khu công nghiệp", "top-5-co-phieu-bat-dong-san-co-the-buoc-vao-song-tang-giai-doan-cuoi-nam"),
    ("xây dựng", "co-phieu-nganh-xay-dung"),
    ("đầu tư công", "top-co-phieu-dau-tu-cong-nen-dau-tu"),
    ("thép", "top-5-co-phieu-nganh-thep-co-co-ban-tot-sap-buoc-vao-chu-ky-tang-truong-moi"),
    ("nhựa", "co-phieu-nganh-nhua"),
    ("năng lượng", "co-phieu-nganh-nang-luong"),
    ("dầu khí", "co-phieu-nganh-nang-luong"),
    ("điện", "top-co-phieu-dien-luc-nganh-dien"),
    ("điện lực", "top-co-phieu-dien-luc-nganh-dien"),
    ("than", "co-phieu-nganh-than"),
    ("bán lẻ", "co-phieu-nganh-ban-le"),
    ("thực phẩm", "co-phieu-nganh-thuc-pham"),
    ("ô tô", "co-phieu-nganh-o-to"),
    ("chứng khoán", "top-5-co-phieu-nganh-chung-khoan-dang-dau-tu-nhat"),
    ("bảo hiểm", "co-phieu-nganh-bao-hiem"),
    ("cảng biển", "top-co-phieu-cang-bien-nen-dau-tu"),
    ("hàng không", "top-co-phieu-hang-khong-nen-dau-tu"),
    ("cao su", "top-co-phieu-cao-su-nen-dau-tu"),
    ("hóa chất", "co-phieu-nganh-hoa-chat"),
    ("phân bón", "co-phieu-nganh-hoa-chat"),
    ("thủy sản", "co-phieu-nganh-thuy-san"),
    ("nông nghiệp", "co-phieu-nganh-nong-nghiep"),
    ("công nghệ", "co-phieu-nganh-cong-nghe"),
    ("công nghệ thông tin", "co-phieu-nganh-cong-nghe"),
    ("dệt may", "co-phieu-nganh-det-may"),
    ("du lịch", "co-phieu-nganh-du-lich"),
    ("y tế", "co-phieu-nganh-y-te"),
]
# expected sector page(s) per subgroup — only these targets are accepted for a spoke of that subgroup
OK = {
    "5a": {"top-5-co-phieu-ngan-hang-dinh-gia-hop-ly-tiem-nang-but-pha-manh"},
    "5b": {"top-5-co-phieu-bat-dong-san-co-the-buoc-vao-song-tang-giai-doan-cuoi-nam", "co-phieu-nganh-xay-dung", "top-co-phieu-dau-tu-cong-nen-dau-tu"},
    "5c": {"top-5-co-phieu-nganh-thep-co-co-ban-tot-sap-buoc-vao-chu-ky-tang-truong-moi", "co-phieu-nganh-nhua"},
    "5d": {"co-phieu-nganh-nang-luong", "top-co-phieu-dien-luc-nganh-dien", "co-phieu-nganh-than"},
    "5e": {"co-phieu-nganh-ban-le", "co-phieu-nganh-thuc-pham", "co-phieu-nganh-o-to"},
    "5f": {"top-5-co-phieu-nganh-chung-khoan-dang-dau-tu-nhat", "co-phieu-nganh-bao-hiem"},
    "5g": {"top-co-phieu-cang-bien-nen-dau-tu"},
    "5l": {"top-co-phieu-hang-khong-nen-dau-tu"},
    "5h": {"top-co-phieu-cao-su-nen-dau-tu", "co-phieu-nganh-thuy-san", "co-phieu-nganh-nong-nghiep"},
    "5m": {"co-phieu-nganh-hoa-chat"},
    "5n": {"co-phieu-nganh-det-may"},
    "5i": {"co-phieu-nganh-cong-nghe"},
}
STOP_H2 = re.compile(r"kết luận|câu hỏi|faq|mở tài khoản|lưu ý khi|hướng dẫn mua|cách mua", re.I)

def text(b):
    return H.unescape(re.sub(r"<[^>]+>", "", b))

def unlinked(block, phrase):
    """Phrase occurs in block text outside any <a>…</a>."""
    stripped = re.sub(r"(?is)<a\b.*?</a>", " ", block)
    return re.search(r"(?<![\wÀ-ỹ])" + re.escape(phrase) + r"(?![\wÀ-ỹ])", H.unescape(re.sub(r"<[^>]+>", "", stripped)), re.I)

edits, missing = [], []
for slug, hub in sorted(hub_of.items()):
    if slug in hubs:
        continue
    sg = audit.get(slug, {}).get("subgroup", "")
    if sg not in OK:
        continue
    f = LIVE / f"{slug}.html"
    if not f.exists():
        missing.append((slug, "no snapshot")); continue
    blocks = f.read_text(encoding="utf-8").splitlines()
    if any(any(t in b for t in OK[sg]) and "Xem thêm" not in b and "&gt;&gt;" not in b for b in blocks):
        continue  # already links a sector page in prose
    # candidate blocks: <p>/<li> in body, before a stop-heading, not Xem thêm lines
    body_end = next((i for i, b in enumerate(blocks) if b.startswith("<h2") and STOP_H2.search(text(b)) and i > 3), len(blocks))
    cand = [(i, b) for i, b in enumerate(blocks[:body_end]) if b.startswith(("<p", "<li")) and "&gt;&gt;" not in b and "Xem thêm" not in b]
    best = None
    # the article's own sector = the allowed sector page whose words it mentions most
    body = text("\n".join(blocks)).lower()
    score = Counter()
    for word, tgt in SECTOR:
        if tgt in OK[sg]:
            score[tgt] += len(re.findall(r"(?<![\wÀ-ỹ])" + re.escape(word) + r"(?![\wÀ-ỹ])", body))
    own = score.most_common(1)[0][0] if score and score.most_common(1)[0][1] else None
    for word, tgt in sorted(SECTOR, key=lambda x: -len(x[0])):
        if tgt != own or tgt == slug:
            continue
        for form in (f"cổ phiếu ngành {word}", f"ngành {word}", f"cổ phiếu {word}", f"nhóm cổ phiếu {word}", f"nhóm {word}", f"lĩnh vực {word}"):
            if form == "lĩnh vực chứng khoán":
                continue  # "giới đầu tư trong lĩnh vực chứng khoán" is about the market, not securities stocks
            for i, b in cand:
                if len(text(b).strip()) < 60:
                    continue  # bold pseudo-headings like "a. Kỳ vọng ngành ngân hàng"
                m = unlinked(b, form)
                if m:
                    if best is None or i < best[0]:
                        best = (i, b, m.group(0), tgt)
                    break
    if not best:
        missing.append((slug, sg)); continue
    i, b, anchor, tgt = best
    t = text(b).strip()
    pos = t.find(anchor)
    texts = [text(x) for x in blocks]
    for w in (40, 70, 110, 160):  # widen until the snippet identifies exactly one block
        find = t[max(0, pos - w):pos + len(anchor) + 30].strip()
        if sum(find in x for x in texts) == 1:
            break
    clicks = float(audit[slug]["clicks"] or 0)
    edits.append({"src": slug, "op": "wrap", "find": find, "to": tgt, "anchor": anchor, "group": "cluster",
                  "pri": "P1" if clicks >= 50 else "P2", "why": f"{sg}: bài mã CP → trang ngành (block {i + 1}/{len(blocks)})"})
    xem = [b for b in blocks if ("&gt;&gt;" in b or "Xem thêm" in b) and tgt in b]
    if xem:
        edits.append({"src": slug, "op": "remove", "old": "https://www.dsc.com.vn/kien-thuc/" + tgt, "group": "cluster", "pri": "P2",
                      "why": "Dòng Xem thêm trùng đích — link đã có trong câu"})

spec = {"title": "C5 Cổ phiếu & Ngành — link bài mã CP về trang ngành (wrap cụm từ có sẵn)", "edits": edits}
out = ROOT / "knowledge/3-pipeline/internal-links/plans/2026-11-10-c5-sector-hub.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrap", sum(e["op"] == "wrap" for e in edits), "remove", sum(e["op"] == "remove" for e in edits), "missing", len(missing))
print(Counter(e["to"][:40] for e in edits if e["op"] == "wrap").most_common())
miss = ROOT / "knowledge/3-pipeline/internal-links/plans/2026-11-10-c5-can-cau-moi.csv"
with miss.open("w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh); w.writerow(["slug", "subgroup", "hub_registry", "clicks_90d"])
    for sl, sg_ in sorted(missing, key=lambda x: -float(audit.get(x[0], {}).get("clicks") or 0)):
        w.writerow([sl, sg_, hub_of.get(sl, ""), audit.get(sl, {}).get("clicks", "")])
print("missing ->", miss.name)
for e in edits[:6]:
    print(e)
