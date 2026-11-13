"""Draft link_plan spec for C11 Vàng + C14 Bạc: each spoke -> cluster pillar + its branch sub-hub, by wrapping an
existing phrase (no new sentences). Pages with no fitting phrase go to the 'cần câu mới' list printed at the end."""
import csv, json, re, html as H
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LIVE = ROOT / "knowledge/raw/live"
reg = json.loads((ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").read_text(encoding="utf-8"))
audit = {r["slug"]: r for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-audit.csv", encoding="utf-8"))}
KT = "https://www.dsc.com.vn/kien-thuc/"

ctx = defaultdict(set)
for l in csv.DictReader(open(LIVE / "links.csv", encoding="utf-8-sig")):
    if l["kind"] == "contextual":
        ctx[l["from"]].add(l["to"].rstrip("/").rsplit("/", 1)[-1])

# target -> anchor phrases, most specific first
PHRASES = {
    "cach-dau-tu-vang": ["cách đầu tư vàng", "kênh đầu tư vàng", "đầu tư vàng hiệu quả", "đầu tư vàng"],
    "dau-tu-vang-nen-mua-loai-nao": ["nên mua loại vàng nào", "mua vàng loại nào", "loại vàng nào", "các loại vàng", "loại vàng"],
    "co-nen-dau-tu-vang-thoi-diem-nay": ["có nên đầu tư vàng", "có nên mua vàng", "thời điểm mua vàng", "mua vàng lúc này"],
    "dau-tu-bac-co-nen-khong": ["đầu tư bạc", "kênh đầu tư bạc", "mua bạc"],
}
STOP_H2 = re.compile(r"kết luận|câu hỏi|faq|mở tài khoản|tổng kết", re.I)

need = defaultdict(list)  # src -> [(target, role)]
for c in reg["clusters"]:
    if c["id"] not in ("c11-vang", "c14-bac"):
        continue
    for g in c["groups"]:
        sub_of = {s: b["subhub"] for b in g.get("branches", []) for s in b["spokes"] if b.get("subhub")}
        for s in ([g["hub"]] if g.get("hub") else []) + g["spokes"]:
            if c["pillar"] and c["pillar"] not in ctx[s] and s != c["pillar"]:
                need[s].append((c["pillar"], "pillar"))
            if s in sub_of and sub_of[s] not in ctx[s]:
                need[s].append((sub_of[s], "sub-hub"))
    for s in c.get("cross", []):  # bridge page links the other pillar too
        if c["pillar"] not in ctx[s] and s not in (c["pillar"],) and s in audit and audit[s]["cluster"] != "13":
            if s == "nen-dau-tu-vang-hay-bac" and c["id"] == "c14-bac":
                need[s].append((c["pillar"], "pillar cầu nối"))

def text(b):
    return H.unescape(re.sub(r"<[^>]+>", "", b))

import sys
sys.path.insert(0, str(ROOT / "scripts"))
from page_groups import unaccent  # noqa: E402

def own_keyword(src, t, m):
    """Anchor sits inside the article's own title phrase (e.g. «có nên đầu tư vàng thời điểm này» in that very article)."""
    words = lambda x: re.sub(r"[^a-z0-9]+", "-", unaccent(x.lower())).strip("-")
    a = words(m.group(0))
    before = words(t[:m.start()]).split("-")[-2:]
    after = words(t[m.end():]).split("-")[:2]
    return any(seg in src for seg in ("-".join(before[-1:] + [a]), "-".join([a] + after[:1]), "-".join([a] + after[:2])) if seg.count("-") >= a.count("-") + 1)

def unlinked(block, phrase):
    stripped = re.sub(r"(?is)<a\b.*?</a>", " ", block)
    return re.search(r"(?<![\wÀ-ỹ])" + re.escape(phrase) + r"(?![\wÀ-ỹ])", text(stripped), re.I)

REDIRECTED = {r["from"] for r in csv.DictReader(open(Path(__file__).with_name("2026-11-10-redirect-301.csv"), encoding="utf-8"))}
for s in REDIRECTED:
    need.pop(s, None)  # page will be 301'd — don't edit it
edits, missing = [], []
for src in sorted(need, key=lambda s: -float(audit.get(s, {}).get("clicks") or 0)):
    f = LIVE / "html" / f"{src}.html"
    blocks = f.read_text(encoding="utf-8").splitlines()
    texts = [text(x) for x in blocks]
    end = next((i for i, b in enumerate(blocks) if b.startswith("<h2") and STOP_H2.search(text(b)) and i > 3), len(blocks))
    used = set()
    for tgt, role in need[src]:
        best = None
        for ph in PHRASES[tgt]:
            for i, b in enumerate(blocks[:end]):
                if i in used or not b.startswith(("<p", "<li")) or "&gt;&gt;" in b or "Xem thêm" in b or len(texts[i]) < 60:
                    continue
                m = unlinked(b, ph)
                if m and not re.match(r"\s+(miếng|nhẫn|thỏi|SJC|9999|trang sức)", text(re.sub(r"(?is)<a.*?</a>", " ", b))[m.end():], re.I) and not own_keyword(src, text(re.sub(r"(?is)<a.*?</a>", " ", b)), m):
                    best = (i, m.group(0)); break
            if best:
                break
        if not best:
            missing.append((src, tgt, role)); continue
        i, anchor = best
        used.add(i)
        t = texts[i].strip(); pos = t.find(anchor)
        for w in (40, 70, 110, 160):
            find = t[max(0, pos - w):pos + len(anchor) + 30].strip()
            if sum(find in x for x in texts) == 1:
                break
        clicks = float(audit.get(src, {}).get("clicks") or 0)
        edits.append({"src": src, "op": "wrap", "find": find, "to": tgt, "anchor": anchor, "group": "cluster",
                      "pri": "P1" if clicks >= 20 else "P2", "why": f"{role} (block {i + 1}/{len(blocks)})"})
        if any(("&gt;&gt;" in b or "Xem thêm" in b) and tgt in b for b in blocks):
            edits.append({"src": src, "op": "remove", "old": KT + tgt, "group": "cluster", "pri": "P2",
                          "why": "Dòng Xem thêm trùng đích — link đã có trong câu"})

spec = {"title": "C11 Vàng + C14 Bạc — link bài về pillar & sub-hub (wrap cụm từ có sẵn)", "edits": edits}
out = Path(__file__).with_name("2026-11-10-c11-vang-bac.json")
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrap", sum(e["op"] == "wrap" for e in edits), "remove", sum(e["op"] == "remove" for e in edits), "missing", len(missing))
for e in edits:
    if e["op"] == "wrap":
        print(f"  {e['src'][:40]:40} → {e['to'][:32]:32} «{e['anchor']}» {e['why']}")
print("cần câu mới:")
for m in missing:
    print("  ", m)
