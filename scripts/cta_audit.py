#!/usr/bin/env python3
"""Audit the conversion layer (CTA banners, product bridge, open-account links) of content files.

Usage:
  python scripts/cta_audit.py <file.md>              → detail for one article
  python scripts/cta_audit.py --all                  → table over knowledge/4-content/3-finalized/
  python scripts/cta_audit.py --all --ga4 <csv>      → same, ranked by real GA4 landing-page traffic
  python scripts/cta_audit.py --all --json           → machine-readable output

Rules audited here mirror .antigravity/rules/cta-conversion.md. This script never writes to
content files — inserting a banner requires writing prose (product bridge), which goes through
the /cro skill with an approval gate.

GA4 csv: any export with a landing-page column and a sessions/users column; headers are matched
loosely. Place it at knowledge/raw/ga4/landing-pages.csv.

Exit: 0 = every audited file passes, 1 = at least one issue, 2 = error
"""

from __future__ import annotations

import argparse
import csv
import html as html_module
import io
import json
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
FINALIZED_DIR = ROOT / "knowledge/4-content/3-finalized"
PAGE_CACHE = ROOT / "knowledge/raw/pages"
USER_AGENT = "Mozilla/5.0 (compatible; DSC-CRO-audit/1.0)"

DSC_HOST = "https://www.dsc.com.vn"
OPEN_ACCOUNT_URL = f"{DSC_HOST}/mo-tai-khoan"

# Palette from knowledge/1-brand/visual-brand-guidelines.md
BRAND_HEX = {"#00ad14", "#2be841", "#10e7b3", "#0d1b2a", "#e8f8f2", "#ffffff", "#fff", "#0a3d2e"}
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")

GENERIC_BUTTON = {"xem thêm", "tại đây", "click vào đây", "ở đây", "tìm hiểu", "chi tiết", "link"}

MAX_BANNERS = 2
EARLY_ZONE = 0.25       # no banner inside the first 25% of the body
MIN_BANNER_GAP = 300    # words between two banners
BRIDGE_LOOKBACK = 6     # lines above a banner to search for its lead-in paragraph


@dataclass
class Article:
    path: Path
    slug: str
    persona: str = "?"
    words: int = 0
    banners: list = field(default_factory=list)   # list of dict
    md_open_links: int = 0
    issues: list = field(default_factory=list)
    source: str = "local"   # "local" = file in repo, "live" = fetched from the site

    @property
    def has_bridge(self) -> bool:
        return all(b["bridge"] for b in self.banners) if self.banners else False

    def score(self) -> int:
        """0-100. Starts at 100, each issue costs by severity."""
        cost = {"CRITICAL": 30, "MAJOR": 12, "MINOR": 4}
        return max(0, 100 - sum(cost[sev] for _, sev, _, _ in self.issues))

    def passed(self) -> bool:
        """Same bar as qa_lint.Report.passed(): no CRITICAL and no MAJOR."""
        return not any(sev in ("CRITICAL", "MAJOR") for _, sev, _, _ in self.issues)


def split_frontmatter(text: str) -> tuple[dict, list[str], int]:
    """Return (frontmatter dict, all lines, index where the body starts)."""
    lines = text.split("\n")
    fm: dict = {}
    if not lines or lines[0].strip() != "---":
        return fm, lines, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            for raw in lines[1:i]:
                if ":" in raw:
                    k, v = raw.split(":", 1)
                    fm[k.strip()] = v.strip().strip("\"'")
            return fm, lines, i + 1
    return fm, lines, 0


def count_words(text: str) -> int:
    """Word count with markdown syntax and raw HTML blocks removed."""
    text = strip_html(text)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"[*_`#>|~\-]", " ", text)
    return len(re.sub(r"\s+", " ", text).strip().split()) if text.strip() else 0


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def find_banners(lines: list[str], start: int) -> list[dict]:
    """Locate CTA banner blocks: a <div> containing an href to the open-account page.

    Returns one dict per banner with line, end_line, href, button text and bridge flag.
    """
    banners = []
    i = start
    while i < len(lines):
        if "<div" not in lines[i]:
            i += 1
            continue
        # Accumulate until the div block closes (depth counting handles nested divs).
        depth, block, end = 0, [], i
        for j in range(i, len(lines)):
            depth += len(re.findall(r"<div\b", lines[j])) - len(re.findall(r"</div>", lines[j]))
            block.append(lines[j])
            end = j
            if depth <= 0:
                break
        html = "\n".join(block)
        # Only the conversion URL counts — article URLs like /kien-thuc/cach-mo-tai-khoan-... do not.
        m = re.search(r'href=["\']((?:' + re.escape(OPEN_ACCOUNT_URL) + r'|/mo-tai-khoan)[^"\']*)["\']', html)
        # A banner is a *styled* block, not any wrapper div that happens to contain the link.
        # Live pages (Next.js) nest dozens of layout divs around ordinary text links.
        styled = re.search(r'<div\b[^>]*style=["\'][^"\']*(background|border-left)', block[0], re.I)
        if m and styled:
            anchor = re.search(r"<a\b[^>]*>(.*?)</a>", html, re.S)
            banners.append({
                "line": i + 1,
                "end_line": end + 1,
                "href": m.group(1),
                "button": strip_html(anchor.group(1)).strip() if anchor else "",
                "html": html,
                "bridge": has_lead_in(lines, i),
            })
        i = end + 1
    return banners


def has_lead_in(lines: list[str], banner_start: int) -> bool:
    """True if a prose paragraph sits just above the banner (not a heading, list or other block)."""
    for k in range(banner_start - 1, max(-1, banner_start - 1 - BRIDGE_LOOKBACK), -1):
        s = lines[k].strip()
        if not s:
            continue
        if s.startswith(("#", ">", "-", "*", "|", "```")) or s.startswith("<") or s.endswith(">"):
            return False
        return count_words(s) >= 10
    return False


# ──────────────────── Live pages (own site — no scraping API needed) ────────────────────

def fetch_live(url: str, refresh: bool = False) -> str:
    """Fetch one page off our own site and cache it. Plain stdlib urllib, ~0.6s.

    Deliberately NOT the web-serp scraper: Firecrawl/Jina exist to get through competitors'
    bot protection and cost money per call. dsc.com.vn serves us its own HTML directly.
    """
    slug = url.rstrip("/").split("/")[-1]
    cache = PAGE_CACHE / f"{slug}.html"
    if cache.exists() and not refresh:
        return cache.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode("utf-8", "replace")
    PAGE_CACHE.mkdir(parents=True, exist_ok=True)
    cache.write_text(html, encoding="utf-8")
    return html


def html_to_markdown(html: str) -> str:
    """Reduce a rendered article page to markdown-ish text for CTA auditing.

    Only the <main> region is kept, so header/footer conversion links are not miscounted as
    in-article CTAs. Styled CTA blocks are preserved verbatim so find_banners() still sees them.
    """
    m = re.search(r"(?is)<main[^>]*>(.*)</main>", html)
    body = m.group(1) if m else html
    body = re.sub(r"(?is)<(script|style|svg|noscript|form)[^>]*>.*?</\1>", " ", body)

    # Protect styled CTA blocks before the generic tag strip below touches them.
    kept: list[str] = []

    def stash(mo: re.Match) -> str:
        kept.append(mo.group(0))
        return f"\n\n@@CTA{len(kept) - 1}@@\n\n"

    body = re.sub(
        r'(?is)<div\b[^>]*style="[^"]*(?:background|border-left)[^"]*"[^>]*>'
        r'(?:(?!<div\b).)*?href="[^"]*mo-tai-khoan[^"]*".*?</div>',
        stash, body)

    body = re.sub(r"(?is)<h([1-6])[^>]*>(.*?)</h\1>",
                  lambda mo: "\n\n" + "#" * int(mo.group(1)) + " " + re.sub(r"<[^>]+>", "", mo.group(2)).strip() + "\n",
                  body)
    body = re.sub(r'(?is)<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
                  lambda mo: f"[{re.sub(r'<[^>]+>', '', mo.group(2)).strip()}]({mo.group(1)})", body)
    body = re.sub(r"(?is)<li[^>]*>", "\n- ", body)
    body = re.sub(r"(?is)</(p|div|tr|ul|ol|li|table|blockquote)>", "\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html_module.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n\s*\n+", "\n\n", body)

    for i, block in enumerate(kept):
        body = body.replace(f"@@CTA{i}@@", block)
    return body.strip()


def resolve_target(arg: str, refresh: bool = False) -> tuple[str, Path, str, str]:
    """Turn a URL / slug / path into (text, path_label, slug, source).

    A local file always wins: it is the editable source of truth. Only when the article has no
    local copy (732 of 824 live URLs at last count) do we go to the network.
    """
    p = Path(arg)
    if p.suffix == ".md" and p.exists():
        slug = re.sub(r"^(Final|Draft|Optimize)-", "", p.stem)
        return p.read_text(encoding="utf-8"), p, slug, "local"

    slug = arg.rstrip("/").split("/")[-1] if arg.startswith("http") else arg
    local = FINALIZED_DIR / f"Final-{slug}.md"
    if local.exists():
        return local.read_text(encoding="utf-8"), local, slug, "local"

    url = arg if arg.startswith("http") else f"{DSC_HOST}/kien-thuc/{slug}"
    return html_to_markdown(fetch_live(url, refresh)), Path(url), slug, "live"


def audit(path: Path) -> Article:
    slug = path.stem
    for prefix in ("Final-", "Draft-", "Optimize-"):
        slug = slug[len(prefix):] if slug.startswith(prefix) else slug
    return audit_text(path.read_text(encoding="utf-8"), path, slug)


def audit_text(text: str, path: Path, slug: str, source: str = "local") -> Article:
    text = text.replace("\r\n", "\n")
    fm, lines, start = split_frontmatter(text)

    art = Article(path=path, slug=slug, words=count_words("\n".join(lines[start:])), source=source)
    for key in ("Primary_Persona", "Persona", "persona", "Target_Persona"):
        if fm.get(key):
            art.persona = fm[key]
            break

    body = "\n".join(lines[start:])
    art.md_open_links = len(re.findall(r"\]\(" + re.escape(OPEN_ACCOUNT_URL), body))
    art.banners = find_banners(lines, start)

    add = art.issues.append
    # Reader progress is measured in words, not lines: a banner is 8 lines of HTML but 0 words
    # of reading, so a line-based ratio would push every banner artificially far down the page.
    total_words = max(1, art.words)

    if not art.banners:
        add(("CTA-missing-banner", "CRITICAL", 1, "Không có banner CTA"))
    if art.md_open_links == 0 and not art.banners:
        add(("CTA-no-link", "CRITICAL", 1, f"Không có bất kỳ link nào tới {OPEN_ACCOUNT_URL}"))
    if len(art.banners) > MAX_BANNERS:
        add(("CTA-count", "MINOR", 1, f"{len(art.banners)} banner (tối đa {MAX_BANNERS})"))

    for b in art.banners:
        pos = count_words("\n".join(lines[start:b["line"] - 1])) / total_words
        b["pos"] = pos
        if pos < EARLY_ZONE:
            add(("CTA-position", "MAJOR", b["line"], f"Banner nằm trong {int(EARLY_ZONE * 100)}% đầu bài ({int(pos * 100)}%)"))
        if not b["bridge"]:
            add(("CTA-orphan", "MAJOR", b["line"], "Banner mồ côi — không có đoạn dẫn phía trên"))
        if b["button"].lower() in GENERIC_BUTTON:
            add(("CTA-copy", "MINOR", b["line"], f"Text nút chung chung “{b['button']}”"))
        if "{{" in b["html"]:
            add(("CTA-placeholder", "CRITICAL", b["line"], "Còn placeholder {{...}} chưa thay"))
        off = {h.lower() for h in HEX_RE.findall(b["html"])} - BRAND_HEX
        if off:
            add(("CTA-palette", "MINOR", b["line"], f"Màu ngoài brand palette: {', '.join(sorted(off))}"))

    if len(art.banners) == 2:
        between = count_words("\n".join(lines[art.banners[0]["end_line"]:art.banners[1]["line"] - 1]))
        if between < MIN_BANNER_GAP:
            add(("CTA-gap", "MINOR", art.banners[1]["line"], f"Hai banner chỉ cách nhau {between} từ (cần ≥ {MIN_BANNER_GAP})"))

    return art


def load_ga4(csv_path: Path) -> dict[str, int]:
    """Map slug → sessions from a GA4 landing-page export. Headers matched loosely."""
    traffic: dict[str, int] = {}
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header_idx = next(
        (i for i, r in enumerate(rows)
         if any(re.search(r"landing\s*page|trang đích|page path", c, re.I) for c in r)),
        None,
    )
    if header_idx is None:
        raise ValueError("Không tìm thấy cột landing page trong CSV")
    header = rows[header_idx]
    page_col = next(i for i, c in enumerate(header) if re.search(r"landing\s*page|trang đích|page path", c, re.I))
    num_col = next(
        (i for i, c in enumerate(header) if re.search(r"session|phiên|users|người dùng|clicks", c, re.I)),
        None,
    )
    for r in rows[header_idx + 1:]:
        if len(r) <= page_col or not r[page_col].strip():
            continue
        slug = r[page_col].strip().strip("/").split("/")[-1]
        try:
            n = int(float(re.sub(r"[^\d.]", "", r[num_col]) or 0)) if num_col is not None else 0
        except (ValueError, IndexError):
            n = 0
        traffic[slug] = traffic.get(slug, 0) + n
    return traffic


def print_detail(art: Article) -> None:
    print(f"\n=== CTA AUDIT: {art.path.name} ===\n")
    if art.source == "live":
        print("  Nguồn          : TRANG LIVE (chưa có bản local) — chỉ audit được, "
              "không ghi file.\n                   Banner phải dán tay vào CMS.")
    print(f"  Persona        : {art.persona}")
    print(f"  Số từ          : {art.words}")
    print(f"  Banner         : {len(art.banners)}")
    print(f"  Link text mở TK: {art.md_open_links}")
    for b in art.banners:
        print(f"    · dòng {b['line']}–{b['end_line']} | vị trí {int(b.get('pos', 0) * 100)}% thân bài | "
              f"nút: “{b['button']}” | đoạn dẫn: {'có' if b['bridge'] else 'KHÔNG'}")
    if art.issues:
        print(f"\n  Vấn đề ({len(art.issues)}):")
        for cid, sev, line, msg in art.issues:
            print(f"    [{sev:<8}] {cid:<20} dòng {line}: {msg}")
    else:
        print("\n  Không có vấn đề.")
    print(f"\n  CRO score: {art.score()}/100 — {'PASS' if art.passed() else 'FAIL'}\n")


def print_table(arts: list[Article], traffic: dict[str, int] | None) -> None:
    if traffic is not None:
        arts.sort(key=lambda a: (-traffic.get(a.slug, 0), a.score()))
        head = f"  {'Slug':<48} {'Traffic':>8} {'Bn':>3} {'Br':>3} {'Lnk':>4} {'Score':>6}"
    else:
        arts.sort(key=lambda a: (a.score(), a.slug))
        head = f"  {'Slug':<48} {'Words':>8} {'Bn':>3} {'Br':>3} {'Lnk':>4} {'Score':>6}"

    print(f"\n=== CTA AUDIT — {len(arts)} bài ===\n")
    print(head)
    print("  " + "─" * 76)
    for a in arts:
        slug = (a.slug[:45] + "...") if len(a.slug) > 48 else a.slug
        metric = traffic.get(a.slug, 0) if traffic is not None else a.words
        bridge = "✓" if a.has_bridge else ("–" if not a.banners else "✗")
        print(f"  {slug:<48} {metric:>8} {len(a.banners):>3} {bridge:>3} {a.md_open_links:>4} {a.score():>6}")

    no_banner = [a for a in arts if not a.banners]
    no_link = [a for a in arts if not a.banners and a.md_open_links == 0]
    print("\n  " + "─" * 76)
    print(f"  Thiếu banner CTA       : {len(no_banner)}/{len(arts)}")
    print(f"  Không có link mở TK nào: {len(no_link)}/{len(arts)}")
    print(f"  Điểm trung bình        : {sum(a.score() for a in arts) // max(1, len(arts))}/100")
    if traffic is not None and no_banner:
        print(f"\n  Ưu tiên vá trước (traffic cao, chưa có banner):")
        for a in no_banner[:10]:
            print(f"    · {a.slug}  ({traffic.get(a.slug, 0)} sessions)")
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="File .md, slug, hoặc URL bài trên dsc.com.vn")
    ap.add_argument("--refresh", action="store_true", help="Bỏ qua cache, fetch lại trang live")
    ap.add_argument("--all", action="store_true", help=f"Quét toàn bộ {FINALIZED_DIR.relative_to(ROOT)}")
    ap.add_argument("--ga4", help="CSV export GA4 landing page để xếp hạng theo traffic thực")
    ap.add_argument("--json", action="store_true", help="Xuất JSON")
    args = ap.parse_args()

    if not args.all and not args.file:
        ap.error("cần <file> hoặc --all")

    single: Article | None = None
    if not args.all:
        try:
            text, label, slug, source = resolve_target(args.file, args.refresh)
        except OSError as e:
            print(f"Không lấy được bài: {e}", file=sys.stderr)
            return 2
        single = audit_text(text, label, slug, source)
        paths: list[Path] = []
    else:
        paths = sorted(FINALIZED_DIR.glob("*.md"))
        if not paths:
            print(f"Không tìm thấy file nào trong {FINALIZED_DIR}", file=sys.stderr)
            return 2

    traffic = None
    if args.ga4:
        try:
            traffic = load_ga4(Path(args.ga4))
        except (OSError, ValueError, StopIteration) as e:
            print(f"Lỗi đọc GA4 CSV: {e}", file=sys.stderr)
            return 2

    try:
        arts = [single] if single else [audit(p) for p in paths]
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([{
            "slug": a.slug, "file": str(a.path), "persona": a.persona, "words": a.words,
            "banners": len(a.banners), "has_bridge": a.has_bridge,
            "open_account_links": a.md_open_links, "score": a.score(),
            "issues": [{"check": c, "severity": s, "line": l, "message": m} for c, s, l, m in a.issues],
        } for a in arts], ensure_ascii=False, indent=2))
    elif args.all:
        print_table(arts, traffic)
    else:
        print_detail(arts[0])

    return 1 if any(a.issues for a in arts) else 0


if __name__ == "__main__":
    sys.exit(main())
