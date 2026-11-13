"""Build / verify the copy-paste edit pack for the stale-content refresh audit.

Usage:
  python scripts/stale_refresh.py build    # validate every spec vs live snapshot, inject EDITS into audit HTML
  python scripts/stale_refresh.py check    # validate only (no write) — for agents writing specs
  python scripts/stale_refresh.py verify   # after CMS edit + sync_live: report which body edits are live

Specs: knowledge/4-content/audits/edits/*.json
  {"group": "rule|rate|stock|data|legal", "priority": "P0|P1|P2", "issue": "...",
   "edits": [{"slug", "find", "replace", "note"?, "sources"?: [url], "priority"?, "issue"?, "field"?}]}
Body edits: find/replace are raw HTML; find must match exactly once in knowledge/raw/live/html/<slug>.html.
Field edits ("field": "title" | "meta"): CMS fields outside the body. title.find must equal the live title
from pages.csv; meta has no snapshot, so find may be "" (replace = full new meta description).
"""
import csv
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "knowledge/raw/live/html"
FINAL = ROOT / "knowledge/4-content/3-finalized"
AUDITS = ROOT / "knowledge/4-content/audits"
SPECS = AUDITS / "edits"
AUDIT_HTML = AUDITS / "stale-content-refresh-2026-11-04.html"
INNER_TAGS = ("td", "th", "li", "p", "h2", "h3", "h4")
MARK_A, MARK_B = "/*EDITS:BEGIN*/", "/*EDITS:END*/"
FIELD_LABEL = {"title": "Title (thẻ tiêu đề SEO / H1)", "meta": "Meta description"}


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("  ", " ").strip()


def enclosing_block(doc, start, end):
    """(b0, b1, tag) of the innermost td/th/li/p/h* fully containing doc[start:end]; else the match itself."""
    for m in reversed(list(re.finditer(r"<(%s)\b[^>]*>" % "|".join(INNER_TAGS), doc[:start]))):
        tag = m.group(1)
        if f"</{tag}>" in doc[m.end():start]:
            continue
        close = doc.find(f"</{tag}>", end)
        if close != -1:
            return m.start(), close + len(tag) + 3, tag
    return start, end, None


def heading_before(doc, pos):
    hs = list(re.finditer(r"<h[1-4][^>]*>(.*?)</h[1-4]>", doc[:pos], re.S))
    return strip(hs[-1].group(1)) if hs else "(đầu bài)"


def titles():
    with open(ROOT / "knowledge/raw/live/pages.csv", encoding="utf-8-sig") as f:
        return {r["slug"]: r["title"] for r in csv.DictReader(f)}


def specs():
    for p in sorted(SPECS.glob("*.json")):
        yield p, json.loads(p.read_text(encoding="utf-8"))


def collect():
    T = titles()
    out, errors = {}, []
    for path, spec in specs():
        for k, e in enumerate(spec.get("edits", [])):
            tag = f"{path.name}#{k} {e.get('slug')}"
            slug = e.get("slug", "")
            if slug not in T:
                errors.append(f"{tag}: slug không có trên live")
                continue
            final = FINAL / f"Final-{slug}.md"
            card = out.setdefault(slug, {
                "title": T[slug], "final": final.name if final.exists() else None,
                "g": spec.get("group", "data"), "p": spec.get("priority", "P1"),
                "issue": spec.get("issue", ""), "items": []})
            if e.get("priority") and e["priority"] < card["p"]:
                card["p"] = e["priority"]
            if e.get("issue"):
                card["issue"] = e["issue"]
            field = e.get("field")
            if field:
                if field not in FIELD_LABEL:
                    errors.append(f"{tag}: field phải là title/meta")
                    continue
                if field == "title" and e["find"] != T[slug]:
                    errors.append(f"{tag}: title.find khác title live «{T[slug]}»")
                    continue
                card["items"].append({
                    "heading": FIELD_LABEL[field], "field": field,
                    "before": html.escape(e["find"]) if e["find"] else "<i>(snapshot không lưu meta — xem trên CMS)</i>",
                    "after": f"<ins>{html.escape(e['replace'])}</ins>",
                    "html": html.escape(e["replace"]), "text": e["replace"],
                    "note": e.get("note", ""), "sources": e.get("sources", [])})
                continue
            doc = (LIVE / f"{slug}.html").read_text(encoding="utf-8")
            n = doc.count(e["find"]) if e["find"] else 0
            if n != 1:
                errors.append(f"{tag}: find khớp {n} lần — {e['find'][:70]!r}")
                continue
            s = doc.index(e["find"])
            b0, b1, btag = enclosing_block(doc, s, s + len(e["find"]))
            block = doc[b0:b1]
            if btag:  # inner HTML only: user selects the old text inside the cell/paragraph and pastes over it
                block = re.sub(r"^<[^>]+>|</[a-z0-9]+>$", "", block)
            new_block = block.replace(e["find"], e["replace"], 1)
            card["items"].append({
                "heading": heading_before(doc, s),
                "before": block.replace(e["find"], f"<del>{e['find']}</del>", 1),
                "after": new_block.replace(e["replace"], f"<ins>{e['replace']}</ins>", 1),
                "html": new_block, "text": strip(new_block),
                "note": e.get("note", ""), "sources": e.get("sources", [])})
    return out, errors


def build(write=True):
    out, errors = collect()
    if errors:
        print("LỖI — sửa spec:\n  " + "\n  ".join(errors))
        return 1
    n = sum(len(v["items"]) for v in out.values())
    if not write:
        print(f"OK: {n} chỗ sửa / {len(out)} bài hợp lệ")
        return 0
    page = AUDIT_HTML.read_text(encoding="utf-8")
    payload = json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = re.sub(re.escape(MARK_A) + r".*?" + re.escape(MARK_B),
                  lambda _: f"{MARK_A}const EDITS={payload};{MARK_B}", page, flags=re.S)
    AUDIT_HTML.write_text(page, encoding="utf-8")
    print(f"OK: {n} chỗ sửa / {len(out)} bài -> {AUDIT_HTML.relative_to(ROOT)}")
    return 0


def verify():
    done = todo = 0
    for path, spec in specs():
        for e in spec.get("edits", []):
            if e.get("field"):
                continue
            doc = (LIVE / f"{e['slug']}.html").read_text(encoding="utf-8")
            if e["replace"] in doc and e["find"] not in doc:
                done += 1
            else:
                todo += 1
                print(f"  CHƯA: {e['slug']} — {strip(e['find'])[:70]}")
    print(f"Đã lên live {done}/{done + todo} (không tính title/meta)")
    return 0 if todo == 0 else 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    sys.exit({"build": lambda: build(True), "check": lambda: build(False), "verify": verify}[cmd]())
