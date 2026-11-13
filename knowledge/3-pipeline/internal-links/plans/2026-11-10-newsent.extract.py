"""Context for writing new link sentences (links the wrap plan could not place).

For every (src, target) row of 2026-11-10-all-can-cau-moi.csv in one cluster, pick the 3 body paragraphs where a
sentence leading to the target fits best (after the first H2, before Kết luận/FAQ, heading shares words with the
target keys or talks about sector / outlook / peers). Output -> newsent-<cluster-id>.ctx.json, read by a human/LLM
who writes one sentence per row into newsent-<cluster-id>.json (link_plan spec, op append / newp).

    python 2026-11-10-newsent.extract.py "Cổ phiếu cụ thể"     # cluster name prefix
"""
import csv, json, re, sys, html as H
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from page_groups import unaccent  # noqa: E402

HERE = Path(__file__).parent
LIVE = ROOT / "knowledge/raw/live/html"
STOP_H2 = re.compile(r"kết luận|câu hỏi|faq|mở tài khoản|tổng kết|lời kết|cùng dsc|dsc", re.I)
TOPIC = re.compile(r"ngành|triển vọng|vị thế|tổng quan|so sánh|định giá|cạnh tranh|lĩnh vực|giới thiệu|hoạt động|tiềm năng|rủi ro", re.I)
BROAD = {unaccent(w) for w in "là gì các những của và trong cho với có nên top".split()}

keys = {r["target"]: r for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/internal-links/anchor-keys.csv", encoding="utf-8"))}
title = {r["slug"]: r["title"] for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-groups.csv", encoding="utf-8-sig"))}


def text(b):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", b))).strip()


def toks(x):
    return {w for w in unaccent(x.lower()).split() if len(w) > 1 and w not in BROAD}


def main(prefix, src_csv="2026-11-10-all-can-cau-moi.csv"):
    rows = [r for r in csv.DictReader(open(HERE / src_csv, encoding="utf-8"))
            if r["cluster"].startswith(prefix) and r["reason"] == "không có câu phù hợp"]
    out = []
    for r in rows:
        k = keys.get(r["target"], {})
        anchors = [k.get("key_chinh", "")] + [a.strip() for a in (k.get("key_phu", "") + "|" + k.get("ngu_nghia", "")).split("|") if a.strip()]
        tk = set().union(*(toks(a) for a in anchors if a)) | toks(title.get(r["target"], ""))
        blocks = (LIVE / f"{r['src']}.html").read_text(encoding="utf-8").splitlines()
        first = next((i for i, b in enumerate(blocks) if b.startswith("<h2")), len(blocks))
        end = next((i for i, b in enumerate(blocks) if b.startswith("<h2") and i > first and STOP_H2.search(text(b))), len(blocks))
        head, cands = "", []
        for i in range(first, end):
            b = blocks[i]
            if b.startswith(("<h2", "<h3", "<h4")):
                head = text(b); continue
            t = text(b)
            if STOP_H2.search(head) or re.search(r"DSC", t):
                continue  # CTA / product section: a knowledge link there reads as an add-on
            if not b.startswith("<p") or len(t) < 80 or "Xem thêm" in t or "&gt;&gt;" in b:
                continue
            nxt = blocks[i + 1] if i + 1 < len(blocks) else ""
            if t.rstrip().endswith(":") or nxt.startswith(("<ul", "<ol", "<table")):
                continue  # list lead-in: link_plan refuses append/newp here
            sc = 2 * len(toks(head) & tk) + len(toks(t) & tk) + (2 if TOPIC.search(head) else 0) - i / 200
            cands.append((sc, i, head, t))
        cands.sort(reverse=True)
        out.append({"src": r["src"], "src_title": title.get(r["src"], ""), "target": r["target"], "role": r["role"],
                    "target_title": title.get(r["target"], ""), "clicks": r["clicks_90d"], "anchors": anchors[:6],
                    "paras": [{"i": i, "h": h[:90], "n_sent": len(re.findall(r"[.!?](\s|$)", t)), "t": t[:700]}
                              for _, i, h, t in cands[:3]]})
    slug = re.sub(r"[^a-z0-9]+", "-", unaccent(prefix.lower())).strip("-")
    f = HERE / f"newsent-{slug}.ctx.json"
    f.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f.name, len(out), "rows", sum(not o["paras"] for o in out), "without a paragraph")


if __name__ == "__main__":
    main(*sys.argv[1:3])
