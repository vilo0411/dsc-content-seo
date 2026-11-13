"""Anchor keywords for every link target (pillar / hub / sub-hub) -> internal-links/anchor-keys.csv.

Priority (user rule 2026-11-10): key chính (1/bài) > key phụ > key ngữ nghĩa; vary key phụ / ngữ nghĩa across sources.
  key chính   = the GSC query (180 + 90 days, accented) closest to the page's own topic (title head / slug)
  key phụ     = other on-topic GSC queries (share the core words of key chính), by impressions
  ngữ nghĩa   = short core phrases: GSC queries of 1–3 words inside the topic + key chính stripped of question words
Pages with little GSC data fall back to the title / slug. MANUAL rows override everything (edit them, re-run).
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from page_groups import unaccent  # noqa: E402

Q = json.loads((ROOT / "knowledge/raw/audit/2026-11-10/anchor-gsc/queries-by-target.json").read_text(encoding="utf-8"))
title = {r["slug"]: r["title"] for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-groups.csv", encoding="utf-8-sig"))}
reg = json.loads((ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").read_text(encoding="utf-8"))
role = {}
for c in reg["clusters"]:
    for g in c["groups"]:
        for b in g.get("branches", []):
            if b.get("subhub"):
                role.setdefault(b["subhub"], "sub-hub")
    for g in c["groups"]:
        if g.get("hub"):
            role[g["hub"]] = "hub"
    if c.get("pillar"):
        role[c["pillar"]] = "pillar"

STOP = {"là", "gì", "ai", "nào", "nhất", "như", "thế", "nào", "có", "nên", "không", "cách", "các", "những", "của", "và", "trong",
        "cho", "người", "mới", "bắt", "đầu", "top", "hướng", "dẫn", "chi", "tiết", "hiệu", "quả", "tốt", "uy", "tín", "hôm", "nay",
        "ở", "đâu", "bao", "nhiêu", "vào", "thời", "điểm", "này", "lúc", "năm", "việt", "nam", "vn", "the", "là", "gi"}
QWORDS = r"\b(là gì|là ai|như thế nào|thế nào|ở đâu|có nên|nên|nào|cao nhất|tốt nhất|uy tín|hiệu quả|cho người mới( bắt đầu)?|chi tiết|hôm nay|cách|các|những|top \d+)\b"
BROAD = {"chứng khoán", "đầu tư", "đầu tư chứng khoán", "cổ phiếu", "thị trường chứng khoán", "ngân hàng", "tài chính", "kiến thức đầu tư",
         "biểu đồ", "chỉ báo", "chỉ số"}

# hand-fixed rows (target -> (key chính, [key phụ], [ngữ nghĩa])) — wins over the automatic pick
MANUAL = {
    "lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat": ("lãi suất gửi tiết kiệm ngân hàng nào cao nhất",
        ["gửi tiết kiệm ngân hàng nào cao nhất", "lãi suất gửi tiết kiệm online ngân hàng nào cao nhất", "ngân hàng nào có lãi suất tiết kiệm cao nhất"],
        ["lãi suất tiết kiệm các ngân hàng", "so sánh lãi suất tiết kiệm"]),
    "co-tien-nen-dau-tu-gi-luc-nay": ("có tiền nên đầu tư gì",
        ["nên đầu tư gì thời điểm này", "có tiền nên đầu tư vào đâu", "tiền nhàn rỗi nên đầu tư vào đâu"],
        ["đầu tư gì lúc này", "phân bổ tiền nhàn rỗi"]),
    "cac-thuat-ngu-trong-chung-khoan": ("thuật ngữ chứng khoán", ["các thuật ngữ trong chứng khoán", "thuật ngữ trong chứng khoán"],
        ["thuật ngữ đầu tư chứng khoán"]),
}


def clean(q):
    q = re.sub(r"\b(20\d\d|dsc|mới nhất|hiện nay|tphcm|update)\b", "", q.lower())
    return re.sub(r"\s+", " ", q).strip(" -:")


def toks(x):
    return {w for w in unaccent(x.lower()).split() if w not in {unaccent(s) for s in STOP}}


def accented_ok(q, t):
    """Reject queries typed without accents ('phan tich ky thuat') — they can't appear in Vietnamese prose."""
    if unaccent(q) != q:
        return True
    tw = set(title.get(t, "").lower().split())
    return all(w in tw or re.fullmatch(r"[a-z0-9&/.-]+", w) and unaccent(w) == w and w not in {unaccent(x) for x in tw if unaccent(x) != x}
               for w in q.split())


def head(t):
    h = re.split(r"[?:|]| – | - ", title.get(t, ""))[0]
    h = re.sub(r"^(top \d+|\d+)\s+", "", h, flags=re.I)
    return re.sub(r"\s+(\(\d{4}\)|\[\d{4}\]|năm \d{4}|\d{4})\s*$", "", h).strip().lower()


def strip_q(k):
    s = re.sub(QWORDS, " ", k)
    return re.sub(r"\s+", " ", s).strip()


rows = []
for t in sorted(role, key=lambda x: (["pillar", "hub", "sub-hub"].index(role[x]), x)):
    qs = []
    seen = set()
    for q, (c, i) in sorted(Q.get(t, {}).items(), key=lambda x: -x[1][1]):
        q2 = clean(q)
        if not q2 or len(q2.split()) > 9 or not accented_ok(q2, t):
            continue
        k = " ".join(sorted(unaccent(q2).split()))
        if k in seen:
            continue
        seen.add(k)
        qs.append((q2, i))
    h = head(t)
    core = toks(h) or toks(t.replace("-", " "))
    # typo filter: every word must occur in the title or in >= 2 of this page's queries ("chứng khoáng", "cố phiếu" drop out)
    vocab = {}
    for q, _ in qs:
        for w_ in set(q.split()):
            vocab[w_] = vocab.get(w_, 0) + 1
    tw = set(re.findall(r"[\wÀ-ỹ]+", title.get(t, "").lower()))
    qs = [(q, i) for q, i in qs if all(w_ in tw or vocab.get(w_, 0) >= 2 for w_ in q.split())]
    # a 3-letter ticker that is not this page's own -> another stock ("tiềm năng cổ phiếu csv" on the chemicals page)
    own = {w_ for w_ in t.split("-") if len(w_) == 3}
    qs = [(q, i) for q, i in qs if not any(len(w_) == 3 and re.fullmatch(r"[a-z]{3}", w_) and unaccent(w_) == w_
                                           and w_ not in own and w_ not in tw and w_ not in {"etf", "ipo", "roe", "eps", "bop", "atc", "ato", "gdp", "cpi"}
                                           for w_ in q.split())]
    on = [(q, i) for q, i in qs if toks(q) and len(toks(q) & core) / max(1, len(toks(q))) >= 0.5]
    src = "gsc" if on else "title"
    if t in MANUAL:
        main, sub, sem = MANUAL[t]
        src = "manual"
    else:
        # key chính: on-topic query covering most of the core words, ties -> impressions
        hq = [q for q, _ in on if unaccent(q) == unaccent(strip_q(h)) or unaccent(q) == unaccent(h)]
        main = hq[0] if hq else (max(on, key=lambda x: (len(toks(x[0]) & core) / len(core), x[1]))[0] if on else h)
        if len(toks(main) & core) < min(2, len(core)) and h:
            main = h
        sub = [q for q, _ in on if q != main and q not in BROAD and len(q.split()) >= 2][:5]
        sem = []
        for cand in [strip_q(main), strip_q(h)] + [q for q, _ in on if 1 <= len(q.split()) <= 3]:
            if cand and re.search(r"(và|các|của|trong|là|cho|với|tich|kỹ|kĩ)$", cand):
                continue  # fragment left after stripping question words
            if cand and len(cand.split()) > 6:
                continue
            if cand and cand not in sem and cand != main and cand not in sub and cand not in BROAD \
                    and (len(cand.split()) >= 2 or re.fullmatch(r"[a-z0-9&/.-]{2,}", unaccent(cand))):
                sem.append(cand)
        sem = sem[:4]
    rows.append({"target": t, "role": role[t], "title": title.get(t, ""), "source": src,
                 "key_chinh": main, "key_phu": " | ".join(sub), "ngu_nghia": " | ".join(sem),
                 "gsc_queries": len(qs)})

out = ROOT / "knowledge/3-pipeline/internal-links/anchor-keys.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(out.name, len(rows), {s: sum(r["source"] == s for r in rows) for s in ("gsc", "title", "manual")})
