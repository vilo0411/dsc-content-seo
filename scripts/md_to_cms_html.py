#!/usr/bin/env python3
"""Convert a Final-*.md article into HTML ready to paste into the DSC CMS (source mode).

Usage:
    python scripts/md_to_cms_html.py <slug | path/to/Final-slug.md> [--stdout]

Output: knowledge/3-seo/content/4-cms/<slug>.html (body only, no H1 — the CMS renders the
title itself). Title / Meta / H1 are printed to the console for the CMS fields.

Markup mirrors what the CMS stores on the live site (see knowledge/raw/live/html/):
  <h2><strong>…</strong></h2>, images wrapped in <p style="text-align:center;">,
  tables in <figure class="table"> with left-aligned cells, links with target="_blank".
Raw HTML blocks already in the article (CTA banners, <img> tags) pass through unchanged,
except image URLs on extgw.dsc.com.vn/eback/uploads/ are rewritten to relative /uploads/.
Stdlib only.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL_DIR = ROOT / "knowledge/3-seo/content/3-finalized"
OUT_DIR = ROOT / "knowledge/3-seo/content/4-cms"

BLOCK_TAGS = r"div|section|table|figure"
# Live pages render images from the extgw host, but the CMS source must use relative /uploads/.
UPLOADS_ABS = re.compile(r"https?://extgw\.dsc\.com\.vn/eback/uploads/", re.I)


def split_frontmatter(text: str) -> tuple[dict, list[str]]:
    lines = text.split("\n")
    fm: dict[str, str] = {}
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for ln in lines[1:i]:
                    if ":" in ln:
                        k, v = ln.split(":", 1)
                        fm[k.strip()] = v.strip()
                return fm, lines[i + 1:]
    return fm, lines


def inline(text: str) -> str:
    """Markdown inline -> HTML. Escapes text, keeps existing inline HTML tags out of scope."""
    out = html.escape(text, quote=False)
    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
                 lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">', out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                 lambda m: f'<a target="_blank" href="{m.group(2)}">{m.group(1)}</a>', out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


IMG_SIZES = {(800, 500), (1000, 600)}   # CMS standard: in-article 800x500, featured 1000x600
size_warnings: list[str] = []


def img_size(src: str) -> tuple[int, int] | None:
    """Width/height of a local JPEG/PNG (stdlib only); None if not a local file."""
    path = ROOT / src
    if src.startswith("http") or not path.is_file():
        return None
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker, seg = data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
        i += 2 + seg
    return None


def img_tag(src: str, alt: str) -> str:
    """Plain <img src alt>: no width/height/style (see strip_img_size)."""
    size = img_size(src)
    if size and size not in IMG_SIZES:
        w, h = size
        size_warnings.append(f"{src} = {w}x{h} (chuẩn: 800x500 trong bài, 1000x600 ảnh bìa)")
    return f'<img src="{src}" alt="{alt}">'


def strip_img_size(tag: str) -> str:
    """Drop width/height attrs and inline style from <img>.

    Site CSS caps img width (max-width:100%) but never sets height:auto, and the CMS editor
    strips any inline height:auto we add. With height="500" kept, mobile shows a 500px-tall box
    letterboxed by object-fit:contain (blank bands above/below). Without the attrs height is auto.
    """
    return re.sub(r'\s+(?:width|height|style)\s*=\s*"[^"]*"', "", tag, flags=re.I)


def center_img(tag: str) -> str:
    return f'<p style="text-align:center;">\n{strip_img_size(tag)}</p>'


def table_html(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    body = [c for c in cells if not all(re.fullmatch(r":?-{3,}:?", x) for x in c if x)]
    head, data = body[0], body[1:]
    td = 'style="text-align:left;"'
    out = ['<figure class="table">', "<table>", "<thead>",
           "<tr>" + "".join(f"<th {td}>{inline(c)}</th>" for c in head) + "</tr></thead>", "<tbody>"]
    out += ["<tr>" + "".join(f"<td {td}>{inline(c)}</td>" for c in r) + "</tr>" for r in data]
    out += ["</tbody>", "</table>", "</figure>"]
    return "\n".join(out)


def convert(lines: list[str]) -> tuple[str, str]:
    """Return (h1_text, body_html)."""
    out: list[str] = []
    h1 = ""
    i, n = 0, len(lines)
    para: list[str] = []

    def flush_para():
        if para:
            out.append(f"<p>{inline(' '.join(s.strip() for s in para))}</p>")
            para.clear()

    while i < n:
        raw = lines[i]
        s = raw.strip()
        if not s:
            flush_para()
            i += 1
            continue
        # Raw HTML block (banner): copy until the opening tags are closed.
        if re.match(rf"<({BLOCK_TAGS})\b", s, re.I):
            flush_para()
            depth = 0
            while i < n:
                t = lines[i]
                depth += len(re.findall(rf"<({BLOCK_TAGS})\b", t, re.I))
                depth -= len(re.findall(rf"</({BLOCK_TAGS})>", t, re.I))
                out.append(t.rstrip())
                i += 1
                if depth <= 0:
                    break
            continue
        # Standalone image: <img …> tag or markdown image on its own line.
        if re.fullmatch(r"<img\b[^>]*>", s, re.I):
            flush_para()
            out.append(center_img(s))
            i += 1
            continue
        m = re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)\)", s)
        if m:
            flush_para()
            out.append(center_img(img_tag(m.group(2), html.escape(m.group(1)))))
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush_para()
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                h1 = text
            else:
                text = re.sub(r"^\*\*(.*)\*\*$", r"\1", text)
                out.append(f"<h{level}><strong>{inline(text)}</strong></h{level}>")
            i += 1
            continue
        if s.startswith("|"):
            flush_para()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table_html(rows))
            continue
        if re.match(r"^([*-]|\d+[.)])\s+", s):
            flush_para()
            ordered = bool(re.match(r"^\d", s))
            tag = "ol" if ordered else "ul"
            items = []
            while i < n and re.match(r"^\s*([*-]|\d+[.)])\s+", lines[i]):
                items.append(re.sub(r"^\s*([*-]|\d+[.)])\s+", "", lines[i]).strip())
                i += 1
            out.append(f"<{tag}>\n" + "\n".join(f"<li>{inline(x)}</li>" for x in items) + f"\n</{tag}>")
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            flush_para()
            i += 1
            continue
        para.append(raw)
        i += 1
    flush_para()
    return h1, relativize_uploads("\n".join(out) + "\n")


def relativize_uploads(body: str) -> str:
    """CMS stores images as /uploads/<file>; absolute extgw URLs break on paste."""
    return UPLOADS_ABS.sub("/uploads/", body)


def resolve(arg: str) -> Path:
    p = Path(arg)
    if p.suffix == ".md" and p.exists():
        return p
    cand = FINAL_DIR / f"Final-{arg}.md"
    if cand.exists():
        return cand
    sys.exit(f"Không tìm thấy bài: {arg}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("article", help="slug hoặc đường dẫn file .md")
    ap.add_argument("--stdout", action="store_true", help="in HTML ra màn hình thay vì ghi file")
    args = ap.parse_args()

    path = resolve(args.article)
    fm, lines = split_frontmatter(path.read_text(encoding="utf-8").replace("\r\n", "\n"))
    slug = fm.get("Slug") or re.sub(r"^(Final|Draft|Optimize)-", "", path.stem)
    h1, body = convert(lines)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.stdout:
        print(body)
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{slug}.html"
    out.write_text(body, encoding="utf-8")
    from activity_log import emit
    emit("seo", "export", slug, skill="md_to_cms_html", path=out, note="CMS HTML")
    from build_content_index import build
    build()
    print(f"HTML  : {out.relative_to(ROOT)}  ({len(body):,} ký tự, không gồm H1)")
    print(f"Slug  : {slug}")
    print(f"Title : {fm.get('Title', '')}  ({len(fm.get('Title', ''))} ký tự)")
    print(f"Meta  : {fm.get('Meta_Description', '')}  ({len(fm.get('Meta_Description', ''))} ký tự)")
    print(f"H1    : {h1}")
    for src in sorted(set(re.findall(r'<img[^>]*src="([^"]+)"', body, re.I))):
        size = img_size(src)
        if size and size not in IMG_SIZES:
            size_warnings.append(f"{src} = {size[0]}x{size[1]} (chuẩn: 800x500 trong bài, 1000x600 ảnh bìa)")
    for w in sorted(set(size_warnings)):
        print(f"⚠️  Ảnh sai kích thước: {w}")
    leftover = sorted(set(re.findall(r'src="(https?://[^"]+)"', body, re.I)))
    if leftover:
        print(f"⚠️  {len(leftover)} ảnh còn URL tuyệt đối — CMS cần /uploads/ (tải ảnh lên CMS rồi sửa src):")
        for u in leftover:
            print(f"   {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
