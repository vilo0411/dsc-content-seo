"""Lint new link sentences, then turn them into a link_plan spec.

Input: newsent-*.out.json — list of {src, target, i, op: append|newp|skip, sentence: "… [anchor] …", reason?}
(i = block index from the .ctx.json). Checks each sentence with qa_lint's own rules (blacklist, hedges,
pointer phrases, quotes) plus: one [anchor], anchor taken from anchor-keys.csv, <= 30 words, append only on a
paragraph with <= 3 sentences, no DSC pitch, no date/number that is not already in the paragraph.

    python 2026-11-10-newsent.check.py newsent-cp-part*.out.json            # lint only
    python 2026-11-10-newsent.check.py newsent-cp-part*.out.json --spec newsent-co-phieu.json
"""
import argparse, csv, json, re, sys, html as H
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import qa_lint  # noqa: E402

HERE = Path(__file__).parent
LIVE = ROOT / "knowledge/raw/live/html"
audit = {r["slug"]: r for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-audit.csv", encoding="utf-8"))}
keys = {r["target"]: r for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/internal-links/anchor-keys.csv", encoding="utf-8"))}
HARD, HEDGE, SOFT = qa_lint.load_blacklist()
EXTRA_BAN = re.compile(r"tham khảo|xem thêm|đọc thêm|bài viết|chi tiết tại|tìm hiểu thêm|^(ngoài ra|bên cạnh đó|hơn nữa)\b", re.I)


def text(b):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", b))).strip()


def anchors_of(t):
    k = keys.get(t, {})
    return [a.strip().lower() for a in [k.get("key_chinh", "")] + (k.get("key_phu", "") + "|" + k.get("ngu_nghia", "")).split("|") if a.strip()]


def check(o, blocks):
    errs = []
    s = o.get("sentence", "")
    plain = s.replace("[", "").replace("]", "")
    m = re.findall(r"\[([^\]]+)\]", s)
    if len(m) != 1:
        return ["cần đúng 1 [anchor]"]
    a = m[0].lower()
    if not any(a == x or (x in a and len(a) - len(x) <= 12) for x in anchors_of(o["target"])):
        errs.append(f"anchor «{m[0]}» không thuộc anchor-keys của {o['target']}")
    if len(plain.split()) > 30:
        errs.append(f"{len(plain.split())} từ > 30")
    low = plain.lower()
    for p in HARD:
        if p and p.lower() in low:
            errs.append(f"blacklist «{p}»")
    for w in HEDGE:
        if re.search(r"(?<![\wÀ-ỹ])" + re.escape(w.lower()) + r"(?![\wÀ-ỹ])", low):
            errs.append(f"hedge «{w}»")
    if qa_lint.POINTER_PHRASE.search(plain) or EXTRA_BAN.search(plain):
        errs.append("câu trỏ đi / từ nối cấm")
    if re.search(r"[\"“”]", plain):
        errs.append("ngoặc kép")
    if "DSC" in plain:
        errs.append("nhắc DSC")
    b = blocks[o["i"]] if o["i"] < len(blocks) else ""
    if not b.startswith("<p"):
        errs.append("block không phải <p>")
    para = text(b)
    # digits inside the anchor are ticker names (PC1, NT2), not figures
    nums = re.findall(r"\d[\d.,]*", re.sub(r"\[[^\]]*\]", "", s))
    new_nums = [n for n in nums if n.rstrip(".,") not in para and n.rstrip(".,") not in o.get("src", "")]
    if new_nums:
        errs.append(f"số không có trong đoạn gốc: {new_nums} (kiểm nguồn)")
    if o["op"] == "append" and len(re.findall(r"[.!?](\s|$)", para)) > 3:
        errs.append("đoạn > 3 câu → dùng newp")
    if not plain.rstrip().endswith((".", "?", "!")):
        errs.append("thiếu dấu chấm câu")
    return errs


def unique_find(blocks, i):
    t = text(blocks[i])
    texts = [text(x) for x in blocks]
    for w in (60, 90, 140, 220, 400):
        f = t[-w:].strip()
        if sum(f in x for x in texts) == 1:
            return f
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--spec")
    a = ap.parse_args()
    edits, bad, skip = [], 0, []
    for f in a.files:
        for o in json.loads(Path(f).read_text(encoding="utf-8")):
            if o.get("op") == "skip":
                skip.append(o); continue
            blocks = (LIVE / f"{o['src']}.html").read_text(encoding="utf-8").splitlines()
            errs = check(o, blocks)
            if errs:
                bad += 1
                print(f"✗ {o['src'][:50]} → {o['target'][:40]}: {'; '.join(errs)}\n    {o['sentence']}")
                continue
            clicks = float(audit.get(o["src"], {}).get("clicks") or 0)
            edits.append({"src": o["src"], "op": o["op"], "find": unique_find(blocks, o["i"]), "to": o["target"],
                          "sentence": o["sentence"], "group": "cluster", "pri": "P1" if clicks >= 20 else "P2",
                          "check_text": True, "why": o.get("why", "câu mới dẫn về hub/pillar")})
    print(f"OK {len(edits)} · lỗi {bad} · bỏ qua {len(skip)}")
    if a.spec:
        Path(a.spec).write_text(json.dumps({"title": "Câu mới chứa link về hub/pillar", "edits": edits,
                                            "skipped": skip}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("→", a.spec)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
