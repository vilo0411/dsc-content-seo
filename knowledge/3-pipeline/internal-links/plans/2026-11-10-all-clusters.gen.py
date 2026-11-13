"""One CMS link plan for every registry cluster (v2, 2026-11-10 — after user review of v1 anchors).

Each pillar / hub / sub-hub link a page is missing is placed by wrapping a phrase already in the article.
Anchors come only from internal-links/anchor-keys.csv (key chính > key phụ > ngữ nghĩa; least-used first inside a tier
so anchors vary across the site). Placement rules (internal-linking SKILL §Quy tắc đặt link + user review):
  1. never in the sapo / intro (before the first H2), never in a sentence introducing the article itself
     ("Bài viết này…", "DSC sẽ…", "cùng tìm hiểu…"), never in Kết luận / FAQ / CTA / Xem thêm
  2. scope: the anchor must not be narrowed by what follows (proper name, ticker, bank, "tại quầy", "online của…")
     nor sit inside the article's own keyword; no cutting a compound ("vàng | miếng")
  3. section: prefer the H2/H3 whose heading shares words with the target keys; ngữ nghĩa anchors require that match
  4. one new link per block; a target already linked in prose is skipped
Pages with no fitting place -> 2026-11-10-all-can-cau-moi.csv (need a new sentence; content edit with QA).
"""
import csv, json, re, sys, html as H
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from page_groups import unaccent  # noqa: E402

LIVE = ROOT / "knowledge/raw/live"
KT = "https://www.dsc.com.vn/kien-thuc/"
HERE = Path(__file__).parent
reg = json.loads((ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").read_text(encoding="utf-8"))
audit = {r["slug"]: r for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-audit.csv", encoding="utf-8"))}
REDIRECTED = {r["from"] for r in csv.DictReader(open(HERE / "2026-11-10-redirect-301.csv", encoding="utf-8"))}

KEYS = {}
for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/internal-links/anchor-keys.csv", encoding="utf-8")):
    split = lambda x: [a.strip() for a in x.split("|") if a.strip()]
    KEYS[r["target"]] = [(r["key_chinh"], "chính")] + [(a, "phụ") for a in split(r["key_phu"])] + [(a, "ngữ nghĩa") for a in split(r["ngu_nghia"])]

ctx = defaultdict(set)
for l in csv.DictReader(open(LIVE / "links.csv", encoding="utf-8-sig")):
    if l["kind"] == "contextual":
        ctx[l["from"]].add(l["to"].rstrip("/").rsplit("/", 1)[-1])

STOP_H2 = re.compile(r"kết luận|câu hỏi|faq|mở tài khoản|tổng kết|lời kết|đầu tư .*cùng dsc|dsc", re.I)
SELF_INTRO = re.compile(r"bài viết|dsc sẽ|dsc giúp|cùng (dsc )?tìm hiểu|hãy cùng|dưới đây|trong bài", re.I)
SPLIT = re.compile(r"\s+(miếng|nhẫn|thỏi|SJC|9999|trang sức|là gì|tín dụng|thanh khoản|hệ thống)\b", re.I)
# what follows the anchor narrows it to one entity / channel -> the general target page is broader than the sentence
NARROW_NEXT = re.compile(r"^\s*(([\wÀ-ỹ]+\s+){0,2}(của|tại|ở)?\s*([A-ZĐ][\wÀ-ỹ]*[A-Z][\wÀ-ỹ]*|[A-Z]{2,5}\b)|online|tại quầy|danh nghĩa|thực\b|kỳ hạn|(ở |nêu )?(trên|dưới đây)\b)", re.U)
BROAD_WORDS = {unaccent(w) for w in "là gì các những của và trong cho với chứng khoán đầu tư cổ phiếu thị trường".split()}


def text(b):
    return H.unescape(re.sub(r"<[^>]+>", "", b))


def words(x):
    return re.sub(r"[^a-z0-9]+", "-", unaccent(x.lower())).strip("-")


def toks(x):
    return {w for w in unaccent(x.lower()).split() if len(w) > 1 and w not in BROAD_WORDS}


def own_keyword(src, t, m):
    a = words(m.group(0))
    before = words(t[:m.start()]).split("-")[-1:]
    after = words(t[m.end():]).split("-")[:2]
    segs = ["-".join(before + [a]), "-".join([a] + after[:1]), "-".join([a] + after[:2])]
    return any(s in src for s in segs if s.strip("-") and s.count("-") > a.count("-"))


# what each article needs (pillar -> hub -> sub-hub)
need, cluster_of = defaultdict(list), {}
for c in reg["clusters"]:
    for g in c["groups"]:
        sub_of = {s: b["subhub"] for b in g.get("branches", []) for s in b["spokes"] if b.get("subhub")}
        for s in ([g["hub"]] if g.get("hub") else []) + g["spokes"]:
            cluster_of.setdefault(s, c["name"])
            if s in REDIRECTED:
                continue
            req = []
            if c.get("pillar") and not g.get("pillar_exempt") and s != c["pillar"]:
                req.append((c["pillar"], "pillar"))
            if g.get("hub") and s != g["hub"]:
                req.append((g["hub"], "hub"))
            if s in sub_of:
                req.append((sub_of[s], "sub-hub"))
            for t, role in req:
                if t not in ctx[s] and t != s and t not in [x for x, _ in need[s]]:
                    need[s].append((t, role))

used_anchor = Counter()
edits, missing = [], []
for src in sorted(need, key=lambda s: -float(audit.get(s, {}).get("clicks") or 0)):
    f = LIVE / "html" / f"{src}.html"
    if not f.exists():
        missing += [(src, t, r, "không có snapshot") for t, r in need[src]]
        continue
    blocks = f.read_text(encoding="utf-8").splitlines()
    texts = [text(x) for x in blocks]
    plain = [text(re.sub(r"(?is)<a\b.*?</a>", " ", b)) for b in blocks]
    first_h2 = next((i for i, b in enumerate(blocks) if b.startswith("<h2")), len(blocks))
    end = next((i for i, b in enumerate(blocks) if b.startswith("<h2") and STOP_H2.search(text(b)) and i > first_h2), len(blocks))
    heading_of, cur = {}, ""
    for i, b in enumerate(blocks):
        if b.startswith(("<h2", "<h3")):
            cur = texts[i]
        heading_of[i] = cur
    used = set()
    for tgt, role in need[src]:
        keys = KEYS.get(tgt)
        if not keys:
            missing.append((src, tgt, role, "bài đích chưa có anchor-keys")); continue
        tkeys = set().union(*(toks(k) for k, _ in keys))
        best = None  # (tier, -section_score, uses, i, anchor, kind)
        for tier, (ph, kind) in enumerate(keys):
            rx = re.compile(r"(?<![\wÀ-ỹ])" + re.escape(ph) + r"(?![\wÀ-ỹ])", re.I)
            for i in range(first_h2 + 1, end):
                b = blocks[i]
                if i in used or not b.startswith(("<p", "<li")) or "&gt;&gt;" in b or "Xem thêm" in b or len(texts[i]) < 60:
                    continue
                m = rx.search(plain[i])
                if not m:
                    continue
                before, after = plain[i][:m.start()], plain[i][m.end():]
                sent = re.split(r"(?<=[.!?])\s+", before)[-1] + m.group(0) + re.split(r"(?<=[.!?])\s", after)[0]
                # "Tại MBBank, lãi suất tiết kiệm…" / "chỉ báo Stochastic": a brand next to the anchor narrows it
                brand_near = re.search(r"([A-ZĐ][\wÀ-ỹ]*[A-Z][\wÀ-ỹ]*|\b[A-Z]{2,5}\b)[\s,]*(\S+\s*){0,2}$", before[-30:]) \
                    or re.match(r"^\s+[A-ZĐ][a-zà-ỹ]+", after)
                if kind == "ngữ nghĩa" and re.search(r"[A-ZĐ][\wÀ-ỹ]*[A-Z]|\b[A-Z]{3}\b|\b(Agribank|Vietcombank|Techcombank|Sacombank|Vietinbank)\b", heading_of[i] + " " + sent):
                    continue  # section about one bank / ticker: a loose phrase there is narrower than the general target
                if SELF_INTRO.search(sent) or SPLIT.match(after) or NARROW_NEXT.match(after) or brand_near or own_keyword(src, plain[i], m):
                    continue
                if m.group(0)[0].isupper() and before.strip() and not re.search(r"[.:!?]\s*$", before):
                    continue  # capitalised mid-sentence = part of a proper name
                if re.search(r"(báo cáo|miễn phí|dịch vụ)\s*$", before, re.I):
                    continue
                score = len(toks(heading_of[i]) & tkeys)
                if kind == "ngữ nghĩa" and score == 0:
                    continue  # a loose semantic phrase only counts inside the section about the target
                tier_rank = {"chính": 0, "phụ": 1, "ngữ nghĩa": 2}[kind]
                cand = (tier_rank, -score, used_anchor[(tgt, ph)], i, m.group(0), kind)
                if best is None or cand < best:
                    best = cand
        if not best:
            missing.append((src, tgt, role, "không có câu phù hợp")); continue
        _, negscore, _, i, anchor, kind = best
        used.add(i)
        used_anchor[(tgt, anchor.lower())] += 1
        t = texts[i].strip()
        pos = t.find(anchor)
        for w in (40, 70, 110, 160):
            find = t[max(0, pos - w):pos + len(anchor) + 30].strip()
            if sum(find in x for x in texts) == 1:
                break
        if sum(find in x for x in texts) != 1:
            missing.append((src, tgt, role, "câu trùng lặp trong bài")); continue
        clicks = float(audit.get(src, {}).get("clicks") or 0)
        edits.append({"src": src, "op": "wrap", "find": find, "to": tgt, "anchor": anchor, "group": "cluster",
                      "pri": "P1" if clicks >= 20 else "P2",
                      "why": f"{cluster_of.get(src, '')} · {role} · key {kind} · mục «{heading_of[i][:50]}»"})
        if any(("&gt;&gt;" in b or "Xem thêm" in b) and (KT + tgt) in b for b in blocks):
            edits.append({"src": src, "op": "remove", "old": KT + tgt, "group": "cluster", "pri": "P2",
                          "why": "Dòng Xem thêm trùng đích — link đã có trong câu"})

seen, dedup = set(), []
for e in edits:
    k = (e["src"], e["op"], e.get("old") or e.get("find"), e.get("to"))
    if k not in seen:
        seen.add(k); dedup.append(e)
edits = dedup
spec = {"title": "Toàn bộ cụm — link về pillar / hub / sub-hub (v2: anchor theo key chính/phụ/ngữ nghĩa, không đặt ở sapo)",
        "edits": edits}
(HERE / "2026-11-10-all-clusters.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
with open(HERE / "2026-11-10-all-can-cau-moi.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["src", "cluster", "target", "role", "reason", "clicks_90d"])
    for s, t, r, why in sorted(missing, key=lambda x: -float(audit.get(x[0], {}).get("clicks") or 0)):
        w.writerow([s, cluster_of.get(s, ""), t, r, why, audit.get(s, {}).get("clicks", "")])
wr = [e for e in edits if e["op"] == "wrap"]
print("articles", len(need), "wrap", len(wr), "remove", len(edits) - len(wr), "missing", len(missing))
print(Counter(e["why"].split(" · ")[2] for e in wr))
