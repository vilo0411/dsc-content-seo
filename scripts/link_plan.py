#!/usr/bin/env python3
"""Build a CMS edit plan (HTML) for internal-link fixes on published articles.

The live CMS is not connected to this project, so every change is applied by hand. This script turns
a small hand-written spec (JSON) into a page with, per article: the current block copied from the live
snapshot (`knowledge/raw/live/html/<slug>.html`), the replacement block, and a preview — ready to paste
into the CMS source view. Progress is kept in the browser (localStorage).

    python scripts/link_plan.py candidates                # print what needs fixing (input for the spec)
    python scripts/link_plan.py build <spec.json>         # -> <spec>.html next to the spec
    python scripts/link_plan.py verify <spec.json>        # after CMS edits + sync_live: which edits are live

Spec format (one object per edit, grouped by source article automatically):
    {"title": "...", "edits": [
      {"src": "slug", "op": "wrap|href|unlink|append|newp|newli", "find": "text inside the block",
       "to": "target-slug or full URL", "anchor": "phrase to wrap / anchor text",
       "sentence": "new sentence with [anchor] marked in brackets (append/newp only)",
       "old": "old href (href/unlink only)", "group": "fix|cluster|backfill", "pri": "P1|P2", "why": "...",
       "check_text": true  # replace only: verify requires the new wording verbatim (full-paragraph rewrites)
      }]}

ops (`find` is optional for href/unlink/remove — then every block linking to `old` is edited):
    wrap    — wrap the first unlinked occurrence of `anchor` inside the block that contains `find`
    replace — swap `old_text` (verbatim in the block HTML) for `sentence` ([anchor] becomes the link)
    href    — repoint every link to `old` inside the block (redirect / category / dead URL) to `to`
    unlink  — drop the <a> around `old`, keep the text
    remove  — delete the <p>/<li> holding the link to `old` (dead "Xem thêm" lines)
    append — add `sentence` at the end of the block (paragraph has <= 3 sentences)
    newp   — add `sentence` as a new <p> right after the block
    cut    — delete `old_text` (verbatim block HTML) — a sentence/link that does not fit; empty <p> is dropped
    newli  — add `sentence` as a new <li> after the <li> containing `find` (same list; may hold <strong>)
    append/newp are refused on a list lead-in ("...sau:" / block followed by <ul>/<ol>) — use newli or wrap.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, setup_utf8  # noqa: E402

LIVE = ROOT / "knowledge/raw/live"
LIVE_HTML = LIVE / "html"
CLUSTERS = ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json"
GSC_PAGES = ROOT / "knowledge/raw/gsc/pages.csv"
KB = "https://www.dsc.com.vn/kien-thuc/"
UA = "Mozilla/5.0 (compatible; DSC-content-snapshot/1.0)"


# ──────────────────────────── data ────────────────────────────

def slug_of(url: str) -> str:
    return url.split("?")[0].split("#")[0].rstrip("/").split("/")[-1]


def load_pages() -> dict[str, dict]:
    with (LIVE / "pages.csv").open(encoding="utf-8-sig", newline="") as f:
        return {r["slug"]: r for r in csv.DictReader(f)}


def load_links() -> list[dict]:
    with (LIVE / "links.csv").open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_clicks() -> dict[str, int]:
    if not GSC_PAGES.exists():
        return {}
    with GSC_PAGES.open(encoding="utf-8-sig", newline="") as f:
        return {slug_of(r["page"]): int(float(r["clicks"] or 0)) for r in csv.DictReader(f)}


def resolve(url: str) -> tuple[int, str, bool]:
    """(status, final URL, is_article). Category pages under /kien-thuc/ have no article body."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", "replace")
            return r.status, r.geturl().rstrip("/"), "COSVFIRFRK" in body
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", 0) or 0, url, False


# ──────────────────────────── candidates ────────────────────────────

def cmd_candidates(args) -> None:
    pages, links, clicks = load_pages(), load_links(), load_clicks()
    kt = [l for l in links if l["kind"] in ("contextual", "xem-them") and l["to"].startswith(KB)]

    print("## 1. Link trỏ tới URL không phải bài viết (danh mục / redirect / chết)\n")
    missing = Counter(slug_of(l["to"]) for l in kt if slug_of(l["to"]) not in pages)
    for s, n in missing.most_common():
        st, final, art = resolve(KB + s)
        kind = ("DANH MỤC" if not art and final.rstrip("/") == (KB + s).rstrip("/") else
                "CHẾT→/kien-thuc" if final.rstrip("/") + "/" == KB else
                "REDIRECT" if slug_of(final) != s else ("OK-ngoài-sitemap" if art else "?"))
        print(f"- {s} ×{n} [{kind}] {st} → {final}")
        for l in kt:
            if slug_of(l["to"]) == s:
                print(f"    {l['from']} | {l['kind']} | «{l['anchor']}» | {l['section'][:60]}")

    print("\n## 2. Bài trong cụm thiếu link pillar/hub\n")
    ctx = defaultdict(set)
    for l in links:
        if l["kind"] == "contextual":
            ctx[l["from"]].add(slug_of(l["to"]))
    for c in json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"]:
        for g in c["groups"]:
            for sp in ([g["hub"]] if g.get("hub") else []) + g["spokes"]:
                need = []
                if c.get("pillar") and not g.get("pillar_exempt") and c["pillar"] not in ctx[sp]:
                    need.append(("pillar", c["pillar"]))
                if g.get("hub") and sp != g["hub"] and g["hub"] not in ctx[sp]:
                    need.append(("hub", g["hub"]))
                for b in g.get("branches", []):
                    if sp in b["spokes"] and b.get("subhub") and b["subhub"] not in ctx[sp]:
                        need.append(("subhub", b["subhub"]))
                for role, t in need:
                    print(f"- {sp} → {role} {t}  (clicks {clicks.get(sp, 0)})")

    print("\n## 3. Bài traffic cao, 0 inlink ngữ cảnh (top 15 theo GSC clicks)\n")
    orphans = [(clicks.get(s, 0), s) for s, p in pages.items() if p["in_contextual"] == "0"]
    for c, s in sorted(orphans, reverse=True)[: args.top]:
        print(f"- {s}  clicks {c}  xem-them-in {pages[s]['in_kt']}")


# ──────────────────────────── block ops ────────────────────────────

A_OPEN = re.compile(r"<a\b[^>]*>", re.I)


def norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def find_block(lines: list[str], find: str) -> int:
    needle = norm_text(find).lower()
    hits = [i for i, ln in enumerate(lines) if needle in norm_text(ln).lower()]
    if len(hits) != 1:
        raise ValueError(f"find «{find[:50]}» khớp {len(hits)} block (cần đúng 1)")
    return hits[0]


def link_tag(url: str, text: str) -> str:
    return f'<a target="_blank" href="{url}">{text}</a>'


def wrap_phrase(block: str, phrase: str, url: str) -> str:
    """Wrap the first occurrence of `phrase` that is outside any <a>…</a> and outside tags."""
    out, i, depth = [], 0, 0
    for m in re.finditer(r"<[^>]+>", block):
        text = block[i:m.start()]
        if depth == 0:
            k = text.lower().find(phrase.lower())
            if k >= 0:
                hit = text[k:k + len(phrase)]
                return "".join(out) + text[:k] + link_tag(url, hit) + text[k + len(phrase):] + block[m.start():]
        out.append(text)
        tag = m.group()
        if re.match(r"<a\b", tag, re.I):
            depth += 1
        elif re.match(r"</a>", tag, re.I):
            depth -= 1
        out.append(tag)
        i = m.end()
    raise ValueError(f"không thấy cụm «{phrase}» chưa gắn link trong block")


def href_re(old: str) -> re.Pattern:
    return re.compile(r'href="' + re.escape(old.rstrip("/")) + r'/?"', re.I)


def sentence_html(sentence: str, url: str) -> str:
    m = re.search(r"\[(.+?)\]", sentence)
    if not m:
        raise ValueError(f"câu mới thiếu [anchor]: {sentence}")
    return sentence[:m.start()] + link_tag(url, m.group(1)) + sentence[m.end():]


def apply(block: str, e: dict, url: str) -> str:
    op = e["op"]
    if op == "wrap":
        return wrap_phrase(block, e["anchor"], url)
    if op == "href":
        new, n = href_re(e["old"]).subn(f'href="{url}"', block)
        if not n:
            raise ValueError(f"không thấy href {e['old']} trong block")
        return new
    if op == "remove":
        pat = re.compile(r'<(p|li)\b[^>]*>(?:(?!</\1>).)*?href="' + re.escape(e["old"].rstrip("/")) + r'/?".*?</\1>', re.I | re.S)
        new, n = pat.subn("", block, count=1)
        if not n:
            raise ValueError(f"không thấy <p>/<li> chứa {e['old']}")
        return new
    if op == "replace":
        if e["old_text"] not in block:
            raise ValueError(f"không thấy đoạn «{e['old_text'][:50]}» nguyên văn trong block")
        return block.replace(e["old_text"], sentence_html(e["sentence"], url), 1)
    if op == "cut":
        if e["old_text"] not in block:
            raise ValueError(f"không thấy đoạn «{e['old_text'][:50]}» nguyên văn trong block")
        new = block.replace(e["old_text"], "", 1)
        # A paragraph left empty is dropped entirely.
        return "" if not norm_text(new) else re.sub(r"\s+(</(p|li)>)", r"\1", new)
    if op == "unlink":
        pat = re.compile(r'<a\b[^>]*href="' + re.escape(e["old"].rstrip("/")) + r'/?"[^>]*>(.*?)</a>', re.I | re.S)
        new, n = pat.subn(r"\1", block)
        if not n:
            raise ValueError(f"không thấy link {e['old']} trong block")
        return new
    s = sentence_html(e["sentence"], url)
    if op == "append":
        m = re.search(r"</(p|li)>\s*$", block)
        if not m:
            raise ValueError("append chỉ dùng cho block <p>/<li>")
        return block[:m.start()].rstrip() + " " + s + block[m.start():]
    if op == "newp":
        return block + "\n<p>" + s + "</p>"
    if op == "newli":
        if not re.match(r"\s*<li\b", block):
            raise ValueError("newli: `find` phải nằm trong 1 <li> của list cần thêm")
        # The last <li> of a list carries the closing </ul>/</ol> on the same line in the snapshot.
        m = re.search(r"(</li>)(\s*</[uo]l>\s*)$", block)
        if m:
            return block[:m.end(1)] + "\n<li>" + s + "</li>" + m.group(2)
        return block + "\n<li>" + s + "</li>"
    raise ValueError(f"op lạ: {op}")


def already_live(lines: list[str], e: dict) -> bool:
    """The added sentence is already on the page (edit done, snapshot re-synced)."""
    want = norm_text(re.sub(r"<[^>]+>", "", e.get("sentence", "")).replace("[", "").replace("]", "")).lower()
    return bool(want) and want in norm_text(" ".join(lines)).lower()


def is_lead_in(lines: list[str], idx: int) -> bool:
    """A paragraph that introduces the list right below it ("...gồm:")."""
    nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
    return norm_text(lines[idx]).endswith(":") or bool(re.match(r"\s*<[uo]l\b", nxt))


def section_of(lines: list[str], idx: int) -> str:
    for ln in reversed(lines[:idx]):
        if re.match(r"<h[23]", ln):
            return norm_text(ln)
    return "Mở đầu bài"


def target_url(to: str) -> str:
    return to if to.startswith("http") else KB + to


# ──────────────────────────── build ────────────────────────────

def build_items(spec: dict, pages: dict, clicks: dict) -> tuple[list[dict], list[str]]:
    by_src: dict[str, list[dict]] = defaultdict(list)
    for e in spec["edits"]:
        by_src[e["src"]].append(e)
    arts, errors = [], []
    for src, edits in by_src.items():
        path = LIVE_HTML / f"{src}.html"
        if not path.exists():
            errors.append(f"{src}: không có snapshot live")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        # Edits on the same block are merged so each block is pasted once.
        blocks: dict[int, dict] = {}
        for e in edits:
            try:
                if e.get("find"):
                    idxs = [find_block(lines, e["find"])]
                elif e["op"] in ("href", "unlink", "remove"):
                    idxs = [i for i, ln in enumerate(lines) if href_re(e["old"]).search(ln)]
                    if not idxs:
                        raise ValueError(f"không block nào link tới {e['old']}")
                else:
                    raise ValueError(f"op {e['op']} cần 'find'")
                url = target_url(e["to"]) if e.get("to") else ""
                if url and url.startswith(KB) and slug_of(url) not in pages and not e.get("allow_missing"):
                    raise ValueError(f"đích {slug_of(url)} không có trong snapshot live")
                if e["op"] in ("append", "newp", "newli") and already_live(lines, e):
                    continue  # re-building after the CMS edit must not add the sentence twice
                for idx in idxs:
                    if e["op"] in ("append", "newp") and is_lead_in(lines, idx):
                        # A sentence glued after "...sau:" breaks the lead-in → list flow.
                        raise ValueError(f"{e['op']} vào câu dẫn list «{norm_text(lines[idx])[-50:]}» — "
                                         "dùng newli (thêm 1 dòng vào list) hoặc wrap cụm có sẵn")
                    after = apply(blocks.get(idx, {}).get("after", lines[idx]), e, url)
                    b = blocks.setdefault(idx, {"before": lines[idx], "after": lines[idx], "edits": []})
                    b["after"] = after
                    b["edits"].append({**e, "url": url})
            except ValueError as ex:
                errors.append(f"{src}: {ex}")
        if not blocks:
            continue
        items = []
        for idx in sorted(blocks):
            b = blocks[idx]
            items.append({"pos": section_of(lines, idx), "before": b["before"], "after": b["after"],
                          "links": [{"to": slug_of(x["url"]) if x["url"] else slug_of(x.get("old", "")),
                                     "url": x["url"], "anchor": x.get("anchor") or "",
                                     "op": x["op"], "group": x.get("group", "fix"),
                                     "pri": x.get("pri", "P2"), "why": x.get("why", "")} for x in b["edits"]],
                          "group": sorted({x.get("group", "fix") for x in b["edits"]}),
                          "pri": min(x.get("pri", "P2") for x in b["edits"])})
        p = pages.get(src, {})
        arts.append({"slug": src, "title": p.get("title", src), "url": KB + src, "clicks": clicks.get(src, 0),
                     "pri": min(i["pri"] for i in items), "group": sorted({g for i in items for g in i["group"]}),
                     "items": items})
    arts.sort(key=lambda a: (a["pri"], -a["clicks"], a["slug"]))
    return arts, errors


def cmd_build(args) -> None:
    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    pages, clicks = load_pages(), load_clicks()
    arts, errors = build_items(spec, pages, clicks)
    for e in errors:
        print("✗", e)
    meta = json.loads((LIVE / "_meta.json").read_text(encoding="utf-8"))
    out = spec_path.with_suffix(".html")
    page = TEMPLATE.replace("__TITLE__", html.escape(spec["title"])) \
                   .replace("__INTRO__", spec.get("intro", "")) \
                   .replace("__SYNC__", meta["last_run"][:16].replace("T", " ")) \
                   .replace("__KEY__", spec_path.stem) \
                   .replace("__DATA__", json.dumps({"arts": arts, "groups": spec.get("groups", {})},
                                                   ensure_ascii=False).replace("</", "<\\/"))
    out.write_text(page, encoding="utf-8")
    n = sum(len(a["items"]) for a in arts)
    print(f"✓ {out.resolve().relative_to(ROOT)} — {len(arts)} bài, {n} block, {sum(len(i['links']) for a in arts for i in a['items'])} thay đổi"
          + (f", {len(errors)} lỗi" if errors else ""))
    if errors:
        sys.exit(1)


# ──────────────────────────── verify ────────────────────────────

def cmd_verify(args) -> None:
    """After the CMS edits are synced back: which edits are now live."""
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    links = load_links()
    ctx = defaultdict(set)
    hrefs = defaultdict(set)
    anchors = defaultdict(set)  # (from, to) -> anchor texts, lowercased
    xemthem = defaultdict(set)  # from -> targets still linked from a ">> Xem thêm" line
    for l in links:
        hrefs[l["from"]].add(l["to"].rstrip("/"))
        anchors[(l["from"], l["to"].rstrip("/"))].add(norm_text(l["anchor"]).lower())
        if l["kind"] == "xem-them":
            xemthem[l["from"]].add(l["to"].rstrip("/"))
        if l["kind"] == "contextual":
            ctx[l["from"]].add(slug_of(l["to"]))
    done = todo = 0
    pending = defaultdict(list)
    for e in spec["edits"]:
        if e["op"] == "cut":
            p = LIVE_HTML / f"{e['src']}.html"
            ok = p.exists() and e["old_text"] not in p.read_text(encoding="utf-8")
            done += ok
            todo += not ok
            if not ok:
                pending[e["src"]].append("cut (đoạn cần gỡ vẫn còn trên live)")
            continue
        if e["op"] == "replace" and e.get("old_text"):
            # The anchor may have existed before the edit, so check the text itself.
            p = LIVE_HTML / f"{e['src']}.html"
            if p.exists():
                page = p.read_text(encoding="utf-8")
                new_txt = norm_text(e.get("sentence", "").replace("[", "").replace("]", "")).lower()
                # Exact new wording is only required for full-paragraph rewrites (`check_text`); for small
                # edits the editor often words it differently, so "old HTML gone" is enough there.
                note = ("đoạn cũ vẫn còn trên live" if e["old_text"] in page else
                        "chưa thấy đoạn mới trên live" if e.get("check_text") and new_txt
                        and new_txt not in norm_text(page).lower() else "")
                if note:
                    todo += 1
                    pending[e["src"]].append(f"{e['op']} → {e.get('to') or e.get('old')} ({note})")
                    continue
        if e["op"] in ("append", "newp", "newli") and e.get("check_text"):
            # Same anchor may already exist from an earlier (removed) sentence — require the new wording.
            p = LIVE_HTML / f"{e['src']}.html"
            want_txt = norm_text(re.sub(r"<[^>]+>", "", e.get("sentence", "")).replace("[", "").replace("]", "")).lower()
            if p.exists() and want_txt not in norm_text(p.read_text(encoding="utf-8")).lower():
                todo += 1
                pending[e["src"]].append(f"{e['op']} → {e.get('to')} (chưa thấy câu mới trên live)")
                continue
        if e["op"] == "remove":
            # Usually paired with a wrap to the same target, so only the "Xem thêm" copy must be gone.
            ok = html.unescape(e["old"]).split("?")[0].rstrip("/") not in xemthem[e["src"]]
        elif e["op"] in ("href", "unlink"):
            # links.csv stores URLs without the query string
            ok = html.unescape(e["old"]).split("?")[0].rstrip("/") not in hrefs[e["src"]]
        else:
            # Check the new anchor text on that target: a slug-only check is a false "done" when the
            # source already linked the target before (e.g. CTA /mo-tai-khoan, or an extra pillar link).
            m = re.search(r"\[(.+?)\]", e.get("sentence", ""))
            want = norm_text(m.group(1) if m else e.get("anchor", "")).lower()
            url = target_url(e["to"]).rstrip("/")
            live = anchors[(e["src"], url)]
            if not want:
                ok = slug_of(url) in ctx[e["src"]]
            elif url.startswith(KB):
                # editors sometimes shorten/extend the anchor on the CMS — accept containment
                ok = any(want in a or a in want for a in live if a)
            else:
                # CTA rename: the new text is usually contained in the old one, so match exactly —
                # or accept the editor's own wording as long as the old anchor is gone.
                old = norm_text(e.get("old_text", "")).lower()
                ok = want in live or bool(live and old and old not in live)
        done += ok
        todo += not ok
        if not ok:
            pending[e["src"]].append(f"{e['op']} → {e.get('to') or e.get('old')}")
    print(f"Đã lên live: {done}/{done + todo}")
    for s, xs in sorted(pending.items()):
        print(f"- {s}: " + "; ".join(xs))


TEMPLATE = r"""<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--ink:#172033;--muted:#5b6478;--line:#e3e7ef;--bg:#fff;--soft:#f6f8fa;--box:#fbfcfe;--acc:#2a78d6;--ok:#1f9d55}
@media(prefers-color-scheme:dark){:root{--ink:#e6e9ef;--muted:#9aa3b5;--line:#2c3342;--bg:#14181f;--soft:#1b212b;--box:#181d26;--acc:#3987e5}}
body{font:15px/1.55 Arial,sans-serif;max-width:1240px;margin:auto;padding:24px;color:var(--ink);background:var(--bg)}
h1{margin:0 0 6px;font-size:24px}h2{margin:0;font-size:18px}a{color:var(--acc)}code{background:var(--soft);padding:1px 5px;border-radius:4px}
.lead{color:var(--muted);margin:0 0 14px}
.toolbar{position:sticky;top:0;z-index:10;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px 14px;box-shadow:0 3px 14px #0002;display:flex;gap:12px;align-items:end;flex-wrap:wrap}
.toolbar label{display:grid;gap:4px;font-weight:600;font-size:13px}
.toolbar select,.toolbar input,button{padding:6px 9px;font:inherit;font-weight:400;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:6px;cursor:pointer}
.summary{margin-left:auto;font-weight:700;font-size:14px}
.progress{height:6px;background:var(--soft);border-radius:9px;overflow:hidden;width:100%}.progress i{display:block;height:100%;background:var(--ok);width:0}
details.box{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:14px 0;background:var(--box)}details.box summary{font-weight:700;cursor:pointer}
article{border-top:2px solid var(--line);margin-top:26px;padding-top:14px}
article.done,.chg.done{opacity:.4}article[hidden],.chg[hidden]{display:none}
.head{display:flex;justify-content:space-between;gap:16px;align-items:start}
.badge{display:inline-block;background:var(--soft);border-radius:999px;padding:2px 9px;font-size:12px;margin:4px 5px 0 0}
.badge.P1{background:#fde8e1;color:#9a2f10;font-weight:700}
.badge.g-fix{background:#fdeee6;color:#8a3d13}.badge.g-cluster{background:#e3eefc;color:#174f96}.badge.g-backfill{background:#e4f4ea;color:#1d6b3a}
.chg{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:12px 0;background:var(--bg)}
.chg-head{display:flex;justify-content:space-between;gap:12px;align-items:start}
.complete{white-space:nowrap;background:var(--soft);padding:6px 10px;border-radius:7px;font-size:13px;cursor:pointer}
.links{margin:6px 0 4px;padding-left:18px;font-size:13.5px}.links li{margin:3px 0}.why{color:var(--muted)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}.cols h3{font-size:13px;margin:6px 0;display:flex;justify-content:space-between;align-items:center}
pre{white-space:pre-wrap;word-break:break-word;background:var(--soft);padding:10px;font-size:12.5px;max-height:320px;overflow:auto;margin:0;border-radius:6px}
.preview{border:1px dashed var(--line);border-radius:8px;padding:8px 12px;font-size:14px;max-height:320px;overflow:auto}
.preview a.new{background:#d7f5e5;outline:2px solid var(--ok);border-radius:3px;color:#0b4a2a}
del.old{background:#fde2e2;color:#8a1c1c}
.copy.ok{background:var(--ok);color:#fff;border-color:var(--ok)}
@media(max-width:860px){.cols{grid-template-columns:1fr}.summary{width:100%;margin-left:0}.head,.chg-head{display:block}}
</style>
<h1>__TITLE__</h1>
<p class="lead">Snapshot live: __SYNC__. Mỗi bài gom mọi thay đổi trong 1 lần mở CMS. Cột <b>Sau</b> là block HTML thay thế: mở source view của CMS, tìm block <b>Trước</b>, dán đè bằng <b>Sau</b>. Link mới được tô <span style="background:#d7f5e5;outline:2px solid #1f9d55;color:#0b4a2a">xanh</span> trong bản xem trước.</p>
__INTRO__
<div class="toolbar">
<label>Nhóm việc<select id="fG"><option value="all">Tất cả</option></select></label>
<label>Ưu tiên<select id="fP"><option value="all">P1 + P2</option><option value="P1">Chỉ P1</option><option value="P2">Chỉ P2</option></select></label>
<label>Tìm bài<input id="fQ" placeholder="slug / tiêu đề" size="20"></label>
<label>Mục đã sửa<select id="fD"><option value="dim">Làm mờ</option><option value="hide">Ẩn</option></select></label>
<button type="button" id="exp">Copy danh sách slug đã sửa</button>
<span class="summary" id="sum"></span>
<div class="progress"><i id="bar"></i></div>
</div>
<div id="list"></div>
<script>
const DATA=__DATA__;const KEY="linkplan:__KEY__";
const st=JSON.parse(localStorage.getItem(KEY)||"{}");const save=()=>localStorage.setItem(KEY,JSON.stringify(st));
const esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const GN={fix:"Sửa link sai",cluster:"Link pillar/hub",backfill:"Link tới bài traffic cao",...DATA.groups};
const fG=document.getElementById("fG");for(const g of [...new Set(DATA.arts.flatMap(a=>a.group))])fG.add(new Option(GN[g]||g,g));
function preview(after,item){const d=document.createElement("div");d.innerHTML=after;
  const urls=new Set(item.links.filter(l=>l.op!=="unlink").map(l=>l.url));
  d.querySelectorAll("a").forEach(a=>{if(urls.has(a.getAttribute("href")))a.className="new";a.removeAttribute("target");a.onclick=e=>e.preventDefault()});
  d.querySelectorAll("img").forEach(i=>i.remove());return d.innerHTML}
function render(){const L=document.getElementById("list");L.innerHTML="";
 DATA.arts.forEach(a=>{const art=document.createElement("article");art.dataset.slug=a.slug;
  art.innerHTML=`<div class="head"><div><h2>${esc(a.title)}</h2><a href="${a.url}" target="_blank">${a.slug}</a>
   <div>${a.group.map(g=>`<span class="badge g-${g}">${GN[g]||g}</span>`).join("")}<span class="badge ${a.pri}">${a.pri}</span>
   <span class="badge">${a.clicks} clicks GSC</span><span class="badge">${a.items.length} block</span></div></div>
   <label class="complete"><input type="checkbox" data-art="${a.slug}"> Đã sửa xong bài này</label></div>`;
  a.items.forEach((it,k)=>{const id=a.slug+"#"+k;const c=document.createElement("div");c.className="chg";c.dataset.id=id;
   c.dataset.g=it.group.join(" ");c.dataset.p=it.pri;
   c.innerHTML=`<div class="chg-head"><div><b>${k+1}. ${esc(it.pos)}</b>
    <ul class="links">${it.links.map(l=>`<li><span class="badge g-${l.group}">${l.op}</span> ${l.op==="unlink"||l.op==="remove"||l.op==="cut"?`${l.op==="remove"?"xoá dòng":l.op==="cut"?"gỡ câu chứa link":"bỏ link"} <code>${l.to}</code>`:`→ <code>${l.to}</code> «${esc(l.anchor)}»`} <span class="why">— ${esc(l.why)}</span></li>`).join("")}</ul></div>
    <label class="complete"><input type="checkbox" data-id="${id}"> Xong</label></div>
    <div class="cols"><div><h3>Trước (tìm trong CMS) <button class="copy" data-t="b">Copy</button></h3><pre>${esc(it.before)}</pre></div>
    <div><h3>Sau (dán đè) <button class="copy" data-t="a">Copy</button></h3><pre>${it.after?esc(it.after):"(xoá cả block này)"}</pre></div></div>
    <h3 style="font-size:13px">Xem trước</h3><div class="preview">${preview(it.after,it)}</div>`;
   c.querySelectorAll(".copy").forEach(b=>b.onclick=()=>{navigator.clipboard.writeText(b.dataset.t==="a"?it.after:it.before);b.classList.add("ok");b.textContent="Đã copy";setTimeout(()=>{b.classList.remove("ok");b.textContent="Copy"},1200)});
   art.appendChild(c)});
  L.appendChild(art)});
 document.querySelectorAll("input[data-id]").forEach(x=>{x.checked=!!st[x.dataset.id];x.onchange=()=>{st[x.dataset.id]=x.checked;sync(x.closest("article"));save();apply()}});
 document.querySelectorAll("input[data-art]").forEach(x=>{x.onchange=()=>{x.closest("article").querySelectorAll("input[data-id]").forEach(y=>{y.checked=x.checked;st[y.dataset.id]=x.checked});save();apply()}});
 document.querySelectorAll("article").forEach(sync);apply()}
function sync(art){const ys=[...art.querySelectorAll("input[data-id]")];art.querySelector("input[data-art]").checked=ys.every(y=>y.checked)}
function apply(){const g=fG.value,p=document.getElementById("fP").value,q=document.getElementById("fQ").value.toLowerCase(),hide=document.getElementById("fD").value==="hide";
 let tot=0,dn=0;
 document.querySelectorAll("article").forEach(art=>{const a=DATA.arts.find(x=>x.slug===art.dataset.slug);let vis=0;
  art.querySelectorAll(".chg").forEach(c=>{const d=!!st[c.dataset.id];tot++;dn+=d;c.classList.toggle("done",d);
   const show=(g==="all"||c.dataset.g.split(" ").includes(g))&&(p==="all"||c.dataset.p===p)&&!(hide&&d);c.hidden=!show;vis+=show});
  const allDone=[...art.querySelectorAll(".chg")].every(c=>st[c.dataset.id]);art.classList.toggle("done",allDone);
  art.hidden=!vis||(q&&!(a.slug+" "+a.title).toLowerCase().includes(q))});
 document.getElementById("sum").textContent=`${dn}/${tot} block đã sửa · ${DATA.arts.length} bài`;document.getElementById("bar").style.width=(tot?100*dn/tot:0)+"%"}
["fG","fP","fQ","fD"].forEach(i=>document.getElementById(i).addEventListener("input",apply));
document.getElementById("exp").onclick=()=>{const s=DATA.arts.filter(a=>a.items.some((_,k)=>st[a.slug+"#"+k])).map(a=>a.slug);
 navigator.clipboard.writeText("python scripts/sync_live.py --only "+s.join(","));document.getElementById("exp").textContent="Đã copy lệnh sync ("+s.length+" bài)"};
render();
</script>
"""


def main() -> None:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("candidates")
    c.add_argument("--top", type=int, default=15)
    b = sub.add_parser("build")
    b.add_argument("spec")
    v = sub.add_parser("verify")
    v.add_argument("spec")
    args = ap.parse_args()
    {"candidates": cmd_candidates, "build": cmd_build, "verify": cmd_verify}[args.cmd](args)


if __name__ == "__main__":
    main()
