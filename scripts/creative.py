#!/usr/bin/env python3
"""Dựng ảnh quảng cáo / post social từ file copy đã lint: design.json → HTML → PNG (Chromium qua Playwright) + QA máy.

Dùng:
    python scripts/creative.py init <copy.md>                   # đọc dòng Creative:/Hình: → <kênh>/creatives/design.json
    python scripts/creative.py render <design.json> [--only id,id] [--bump]
    python scripts/creative.py approve <design.json> --ids all|id,id --xac-nhan "<lời duyệt của user>" [--chap-nhan-loi]
    python scripts/creative.py layouts                          # liệt kê layout + tỉ lệ

Nguyên tắc (học từ design-agent-plugin):
- design.json là nguồn duy nhất; không sửa tay HTML/PNG. Chữ trên ảnh là chữ HTML thật (đúng dấu tiếng Việt), AI chỉ vẽ phần minh hoạ.
- Chữ trên ảnh bị KHOÁ theo file copy: khác chữ trong `chữ trên ảnh: "…"` → lỗi TEXT-locked. Sửa ở file copy, lint lại, rồi init lại.
- Chữ không vừa khung → trình duyệt thu nhỏ dần 4%/bước tới 60% cỡ gốc; vẫn tràn → lỗi, engine không tự cắt chữ.
- Bản đã duyệt không render đè: dùng --bump để ra v mới.

Output: <kênh>/creatives/v<N>/<id>.png, html/<id>.html, qa.json, preview.html (xem cả bộ + cỡ điện thoại).
QA: FONT-*, FIT-*, SAFE-zone, MOBILE-small, CONTRAST-*, RED-pixels, LOGO-missing, TEXT-locked, FIELD-placeholder, COMP-*/AI-* (dùng lại mkt_lint).
Exit 1 nếu còn lỗi (error).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, setup_utf8, unaccent  # noqa: E402
from activity_log import classify as _act_classify, emit  # noqa: E402
import mkt_lint as ml  # noqa: E402

LAYOUT_DIR = ROOT / ".agents/core/creative/layouts"
BRAND_FILE = ROOT / "knowledge/1-brand/brand.json"
STYLE_THEME = {"S01": "dark", "S02": "mint", "S03": "paper", "S04": "dark"}  # ảnh 1 dòng chữ: layout thesis + tông của style
SIZE_PRESET = {"xs": 0.026, "s": 0.034, "m": 0.045, "l": 0.06, "xl": 0.075, "xxl": 0.095, "mega": 0.24}
TEXT_SLOTS = ("badge", "eyebrow", "script", "big", "headline", "sub", "cta", "note")
LOCK_SLOTS = ("eyebrow", "script", "big", "headline")
# Khổ theo kênh (đề xuất biên tập — kiểm lại trên nền tảng khi đăng)
CHANNEL_SIZES = {
    "facebook": ["1080x1350", "1080x1080", "1200x628"],
    "instagram": ["1080x1350", "1080x1080", "1080x1920"],
    "meta-ads": ["1080x1350", "1080x1080", "1080x1920", "1200x628"],
    "linkedin": ["1080x1350", "1200x628"],
    "zalo": ["1280x720", "1080x1080"],
    "tiktok": ["1080x1920"],
    "youtube": ["1280x720"],
    "google-display": ["1200x628", "1200x1200"],
}
ASPECTS = {"4:5": 0.8, "1:1": 1.0, "9:16": 0.5625, "1.91:1": 1.91}
PHONE_W = 390
MIN_SCALE = 0.6
TODO = "TODO"
NOTE_FEE = "Theo biểu phí hiện hành của Chứng khoán DSC"


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s or "")


def plain(s: str) -> str:
    return re.sub(r"\s+", " ", nfc(s).replace("**", "")).strip()


# ─────────────────────────── brand / themes ───────────────────────────

def load_brand() -> dict:
    return json.loads(BRAND_FILE.read_text(encoding="utf-8"))


def themes(brand: dict) -> dict:
    """Theme = palette DESIGN.md v1.0 §2 (dark/pine/mint/paper); emerald/ivory = theme mùa vụ §7 (chỉ khi brief ghi Tết/lễ)."""
    c, d, se = brand["colors"], brand["colors"]["derived"], brand["colors"]["seasonal"]
    prim = brand["colors"]["gradients"]["primary"]
    return {
        "dark": {"bg": c["gunmetal"], "fg": c["white"], "sub": d["on_dark_sub"], "note": d["on_dark_note"],
                 "eyebrow": c["frosted_mint"], "grid": True, "accent": prim, "mark": c["emerald"],
                 "cta_bg": [c["lime"], c["lime"]], "cta_fg": c["gunmetal"],
                 "badge_bg": c["pine_teal"], "badge_fg": c["frosted_mint"], "logo": "dark_bg", "band": c["lime"], "glow": True},
        "pine": {"bg": c["pine_teal"], "fg": c["white"], "sub": d["on_dark_sub"], "note": d["on_dark_note"],
                 "eyebrow": c["frosted_mint"], "grid": False, "accent": [c["lime"], c["frosted_mint"]], "mark": c["emerald"],
                 "cta_bg": [c["lime"], c["lime"]], "cta_fg": c["gunmetal"],
                 "badge_bg": c["frosted_mint"], "badge_fg": c["gunmetal"], "logo": "dark_bg", "band": c["lime"], "glow": True},
        "mint": {"bg": d["mint_50"], "fg": c["gunmetal"], "sub": d["ink_2"], "note": d["ink_3"], "eyebrow": c["pine_teal"],
                 "grid": False, "accent": None, "mark": c["frosted_mint"], "cta_bg": [c["pine_teal"], c["pine_teal"]],
                 "cta_fg": c["white"], "badge_bg": c["frosted_mint"], "badge_fg": c["gunmetal"],
                 "logo": "light_bg", "band": c["lime"], "glow": False},
        "paper": {"bg": c["white"], "fg": c["gunmetal"], "sub": d["ink_2"], "note": d["ink_3"], "eyebrow": c["pine_teal"],
                  "grid": False, "accent": None, "mark": c["frosted_mint"], "cta_bg": [c["lime"], c["lime"]],
                  "cta_fg": c["gunmetal"], "badge_bg": c["pine_teal"], "badge_fg": c["white"],
                  "logo": "light_bg", "band": c["lime"], "glow": False},
        # seasonal (DESIGN.md §7)
        "emerald": {"bg": se["emerald_950"], "fg": "#FFFFFF", "sub": "#EDE6C8", "note": "#CFC8A9", "eyebrow": se["gold_200"],
                    "grid": False, "accent": None, "gold": se["gold_gradient"], "display_ref": se["gold_500"],
                    "script": se["gold_200"], "cta_bg": [se["gold_200"], se["gold_500"]], "cta_fg": se["emerald_950"],
                    "badge_bg": "#FFFFFF", "badge_fg": se["emerald_800"], "logo": "dark_bg", "band": se["gold_500"], "glow": False},
        "ivory": {"bg": se["ivory_50"], "fg": se["emerald_800"], "sub": "#3E4A3F", "note": "#5E665C", "eyebrow": se["emerald_600"],
                  "grid": False, "accent": None, "mark": se["gold_200"], "script": se["emerald_800"], "display_ref": se["emerald_800"],
                  "cta_bg": [se["emerald_800"], se["emerald_800"]], "cta_fg": "#FFFFFF",
                  "badge_bg": se["emerald_800"], "badge_fg": "#FFFFFF", "logo": "light_bg", "band": se["gold_700"], "glow": False},
    }


SEASONAL_THEMES = {"emerald", "ivory"}


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ─────────────────────────── layouts ───────────────────────────

def load_layout(name: str) -> dict:
    p = LAYOUT_DIR / f"{name}.json"
    if not p.exists():
        raise SystemExit(f"Không có layout “{name}”. Có: {', '.join(x.stem for x in sorted(LAYOUT_DIR.glob('*.json')))}")
    return json.loads(p.read_text(encoding="utf-8"))


def parse_size(size: str) -> tuple[int, int]:
    m = re.match(r"^\s*(\d{3,4})\s*[x×]\s*(\d{3,4})\s*$", size or "")
    if not m:
        raise SystemExit(f"Kích thước không hợp lệ: {size!r} (dạng 1080x1350)")
    return int(m.group(1)), int(m.group(2))


def pick_variant(layout: dict, w: int, h: int) -> tuple[str, dict]:
    ratio = w / h
    key = min((k for k in layout["variants"]), key=lambda k: abs(ASPECTS.get(k, 1) - ratio))
    return key, layout["variants"][key]


# ─────────────────────────── init: copy.md → design.json ───────────────────────────

SIZE_RE = re.compile(r"(\d{3,4})\s*[×x]\s*(\d{3,4})")
STYLE_RE = re.compile(r"\bS0([1-4])\b")
QUOTE_RE = re.compile(r"chữ trên ảnh:\s*[\"“]([^\"”]+)[\"”]", re.I)
SLIDE1_RE = re.compile(r"slide\s*1\s*[\"“]([^\"”]+)[\"”]", re.I)
SLIDES_RE = re.compile(r"[×x]\s*(\d+)\s*slide", re.I)
LINE_RE = re.compile(r"(?im)^\**\s*(creative|hình)\s*:?\**\s*:?\s*(.+)$")


def variant_id(channel_dir: str, heading: str) -> str:
    m = re.search(r"\bV(\d+)\b", heading)
    num = f"v{m.group(1)}" if m else re.sub(r"[^a-z0-9]+", "-", unaccent(heading).lower()).strip("-")[:20]
    if channel_dir == "social":
        first = re.split(r"[\s·]+", heading.strip())[0].lower()
        return f"{first}-{num}"
    return f"{channel_dir}-{num}"


def locked_texts(copy_path: Path) -> dict[str, str]:
    """id → chữ trên ảnh trong file copy (để khoá)."""
    channel_dir = copy_path.parent.name
    out = {}
    for heading, block in ml.split_variants(copy_path.read_text(encoding="utf-8")):
        m = LINE_RE.search(block)
        if not m:
            continue
        line = m.group(2)
        vid = variant_id(channel_dir, heading)
        q = QUOTE_RE.search(line)
        if q:
            out[vid] = plain(q.group(1))
        s1 = SLIDE1_RE.search(line)
        if s1:
            out[f"{vid}-01"] = plain(s1.group(1))
    return out


def init(copy_path: Path) -> Path:
    channel_dir = copy_path.parent.name
    out_dir = copy_path.parent / "creatives"
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "design.json"
    if dest.exists():
        raise SystemExit(f"Đã có {dest} — sửa file đó, hoặc xoá đi nếu muốn init lại từ copy")
    creatives = []
    for heading, block in ml.split_variants(copy_path.read_text(encoding="utf-8")):
        m = LINE_RE.search(block)
        if not m:
            continue
        line = m.group(2)
        if re.search(r"dùng ảnh (bài )?gốc", line, re.I):
            continue
        sz = SIZE_RE.search(line)
        size = f"{sz.group(1)}x{sz.group(2)}" if sz else "1080x1350"
        st = STYLE_RE.search(line)
        style = f"S0{st.group(1)}" if st else "S01"
        vid = variant_id(channel_dir, heading)
        slides = SLIDES_RE.search(line)
        if slides or style == "S04" or "carousel" in line.lower():
            n = int(slides.group(1)) if slides else 5
            s1 = SLIDE1_RE.search(line) or QUOTE_RE.search(line)
            group = []
            for i in range(1, n + 1):
                sid = f"{vid}-{i:02d}"
                if i == 1:
                    group.append({"id": sid, "group": vid, "layout": "thesis", "size": size,
                                  "text": {"headline": nfc(s1.group(1)) if s1 else TODO, "sub": "", "cta": "", "note": ""}})
                elif i == n:
                    group.append({"id": sid, "group": vid, "layout": "cta-end", "size": size,
                                  "text": {"headline": TODO, "sub": "", "cta": "Mở tài khoản ngay", "note": ""}})
                else:
                    group.append({"id": sid, "group": vid, "layout": "rows" if style == "S03" else "steps", "size": size,
                                  "text": {"headline": TODO, "items": [TODO, TODO, TODO], "note": ""}})
            for i, g_ in enumerate(group, 1):
                g_.update(page=i, pages=n)
            creatives.extend(group)
            continue
        q = QUOTE_RE.search(line)
        head = nfc(q.group(1)) if q else TODO
        text = {"headline": head, "sub": "", "cta": "", "note": NOTE_FEE if "%" in head else ""}
        creatives.append({"id": vid, "layout": "thesis", "theme": STYLE_THEME[style], "size": size, "text": text})
    if not creatives:
        raise SystemExit("Không thấy dòng `Creative:` / `Hình:` nào cần dựng ảnh mới trong file copy")
    job = copy_path.parent.parent.name
    data = {"job": job, "source": copy_path.name, "channel": channel_dir, "version": 1, "approved": [],
            "creatives": creatives}
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


# ─────────────────────────── compose: creative → HTML ───────────────────────────

def headline_html(text: str, theme: dict) -> str:
    out = []
    for i, part in enumerate(re.split(r"\*\*", html.escape(nfc(text)))):
        if i % 2 and part:
            cls = "accent" if theme.get("accent") else "mark"
            nw = " nw" if len(part.split()) <= 2 else ""
            out.append(f'<span class="{cls}{nw}">{part}</span>')
        else:
            out.append(part)
    return "".join(out).replace("\n", "<br>")


def effective_regions(regions: dict, cr: dict, keep_image: bool = False) -> dict:
    """Khung tự giãn: không có ảnh → chữ dàn hết bề ngang; slot ngay dưới tiêu đề bỏ trống → tiêu đề chiếm chỗ và căn giữa."""
    regs = {k: dict(v, box=list(v["box"])) for k, v in regions.items()}
    text = cr.get("text", {})

    def used(slot):
        if slot == "image":
            return bool(cr.get("image"))
        if slot == "items":
            return bool(text.get("items"))
        return bool((text.get(slot) or "").strip())

    if "image" in regs and not used("image") and not keep_image:
        img_x = regs.pop("image")["box"][0]
        for r in regs.values():
            x = r["box"][0]
            if x < img_x:
                r["box"][2] = max(r["box"][2], 1 - 2 * x)
    head = regs.get("headline")
    if head:
        hx, hy, hw, hh = head["box"]
        bottom, grown = hy + hh, False
        for slot, r in sorted(((s, r) for s, r in regs.items() if s != "headline" and r["box"][1] >= hy + hh - 0.01),
                              key=lambda kv: kv[1]["box"][1]):
            if used(slot):
                break
            bottom, grown = r["box"][1] + r["box"][3], True
        if grown:
            head["box"][3] = bottom - hy
            if head.get("valign", "end") != "start":
                head["valign"] = "center"
    return regs


def resolve_src(src: str) -> str:
    """`lib:<id>` → file trong thư viện asset (knowledge/1-brand/assets/library)."""
    if src and src.startswith("lib:"):
        import asset_lib
        p = asset_lib.path_of(src[4:])
        return str(p.relative_to(ROOT)) if p else f"missing-lib-asset/{src[4:]}"
    return src


def image_spec(cr: dict) -> dict | None:
    img = cr.get("image")
    if not img:
        return None
    spec = {"src": img} if isinstance(img, str) else dict(img)
    spec["src"] = resolve_src(spec["src"])
    spec.setdefault("focus", "50% 50%")
    return spec


def auto_theme(src: str) -> str:
    """Ảnh sáng → theme mint, ảnh tối → dark (để nền chữ liền với ảnh)."""
    try:
        from PIL import Image, ImageStat
        im = Image.open(ROOT / src).convert("L").resize((64, 64))
        return "mint" if ImageStat.Stat(im).mean[0] > 140 else "dark"
    except Exception:  # noqa: BLE001
        return "dark"


def compose(cr: dict, brand: dict) -> tuple[str, dict]:
    w, h = parse_size(cr["size"])
    layout = load_layout(cr["layout"])
    vkey, var = pick_variant(layout, w, h)
    img = image_spec(cr)
    th_name = cr.get("theme") or (auto_theme(img["src"]) if img and "image" in var["regions"] else None) \
        or layout.get("default_theme", "dark")
    theme = themes(brand)[th_name]
    base = min(w, h)
    align = layout.get("align", "left")
    fonts = brand["fonts"]
    fam, fb = fonts["family"], fonts.get("fallback", "Be Vietnam Pro")
    face_files = [(fonts.get(k), wt, st) for k, wt, st in (("regular", 400, "normal"), ("semibold", 600, "normal"),
                  ("bold", 700, "normal"), ("extrabold", 800, "normal"), ("italic", 400, "italic"))]
    faces_css = "".join(f'@font-face{{font-family:"{fam}";src:url("{(ROOT / f).as_uri()}");font-weight:{wt};font-style:{st}}}'
                        for f, wt, st in face_files if f and (ROOT / f).exists())
    faces_css += "".join(f'@font-face{{font-family:"{fb}";src:url("{(ROOT / f).as_uri()}");font-weight:{wt}}}'
                         for f, wt in zip(fonts.get("fallback_files", {}).values(), (400, 700)) if (ROOT / f).exists())
    font_stack = f'"{fam}","{fb}",sans-serif'
    # one brand typeface (DESIGN.md §4): old layout "type" values only change weight/caps, never the family
    typeface = cr.get("type") or layout.get("type") or "body"
    disp_family = font_stack
    disp_weight = 800 if typeface in ("serif", "serif_alt", "sans") else 700
    caps = cr.get("caps", typeface in ("serif", "serif_alt", "sans"))
    logo = ROOT / brand["logo"][theme["logo"]]
    logo_w = int(w * (0.14 if w / h > 1.3 else 0.17))
    logo_y = int(h * var.get("logo_y", 0.04))
    logo_h = int(logo_w * 0.3)
    try:
        from PIL import Image
        with Image.open(logo) as li:
            logo_h = int(logo_w * li.height / li.width)
    except Exception:  # noqa: BLE001
        pass
    g = int(base / 18)
    grid_css = (f"background-image:linear-gradient(#ffffff0b 1px,transparent 1px),linear-gradient(90deg,#ffffff0b 1px,transparent 1px);"
                f"background-size:{g}px {g}px;" if theme.get("grid") and layout.get("grid", True) else "")
    text = cr.get("text", {})
    acc = theme.get("accent") or [theme["fg"], theme["fg"]]
    cta_bg = theme["cta_bg"]
    css = f"""
{faces_css}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
body{{position:relative;background:{theme['bg']};color:{theme['fg']};font-family:{font_stack};{grid_css}
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
.r{{position:absolute;display:flex;flex-direction:column;overflow:hidden;text-align:{align}}}
.r.v-start{{justify-content:flex-start}} .r.v-center{{justify-content:center}} .r.v-end{{justify-content:flex-end}}
.t{{width:100%}}
.headline .t{{font-weight:700;line-height:1.25;text-wrap:balance}}
.sub .t{{line-height:1.45;color:{theme['sub']};text-wrap:pretty}}
.note .t{{line-height:1.4;color:{theme['note']}}}
.accent{{background:linear-gradient(90deg,{acc[0]},{acc[1]});-webkit-background-clip:text;background-clip:text;color:transparent}}
.nw{{white-space:nowrap}}
.mark{{background:linear-gradient(transparent 62%,{theme.get('mark', brand['colors']['frosted_mint'])}88 62%);padding:0 .05em}}
.cta .t{{display:flex;justify-content:{'center' if align == 'center' else 'flex-start'}}}
.cta .t span{{display:inline-block;font-weight:700;line-height:1;padding:.62em 1.3em;border-radius:.5em;
  background:linear-gradient(90deg,{cta_bg[0]},{cta_bg[1]});color:{theme['cta_fg']}}}
.items .t{{display:flex;flex-direction:column;gap:.7em}}
.items.rows .t{{border-left:.28em solid {theme['band']};padding-left:.9em}}
.items .it{{display:flex;gap:.7em;align-items:flex-start;line-height:1.35}}
.items .it span{{text-wrap:pretty}}
.items .it b{{flex:0 0 auto;min-width:1.7em;height:1.7em;border-radius:50%;display:inline-grid;place-items:center;
  font-size:.8em;background:{theme['fg']};color:{theme['bg']}}}
.items.rows .it{{padding-bottom:.55em;border-bottom:1px solid {theme['fg']}22}}
.items.rows .it b{{display:none}}
.image img{{width:100%;height:100%;object-fit:cover;display:block}}
.image::after{{content:"";position:absolute;inset:0;pointer-events:none}}
.image.fade-bottom::after{{background:linear-gradient(180deg,transparent 55%,{theme['bg']} 98%)}}
.image.fade-top-bottom::after{{background:linear-gradient(180deg,{theme['bg']} 0%,transparent 18%,transparent 70%,{theme['bg']} 99%)}}
.image.fade-left::after{{background:linear-gradient(90deg,{theme['bg']} 0%,transparent 35%)}}
.headline .t,.big .t{{font-variant-numeric:lining-nums}}
.big.gold3d .t{{isolation:isolate}}
.big.gold3d .t span{{position:relative;background:linear-gradient(180deg,#FFF6CF 0%,#F2D98A 35%,#C9A24A 62%,#9A7424 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}}
.big.gold3d .t span::before{{content:attr(data-t);position:absolute;left:0;top:0;z-index:-1;color:#6E5014;-webkit-text-fill-color:#6E5014;
  text-shadow:{','.join(f"{i * base * 0.0016:.1f}px {i * base * 0.0022:.1f}px 0 {'#7A5A18' if i < 6 else '#5A4110'}" for i in range(1, 9))},
  0 {base * 0.03:.0f}px {base * 0.05:.0f}px rgba(0,0,0,.55)}}
.headline .t{{font-family:{disp_family};font-weight:{disp_weight};{'text-transform:uppercase;line-height:1.1;' if caps else ''}
  filter:{'drop-shadow(0 4px 14px rgba(0,0,0,.45))' if theme.get('gold') else 'none'}}}
.gold{{background:linear-gradient(180deg,{','.join(theme.get('gold') or [theme['fg'], theme['fg']])});-webkit-background-clip:text;
  background-clip:text;color:transparent;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.gold .accent,.gold .mark{{background:none;-webkit-text-fill-color:#FFFFFF;color:#FFFFFF}}
.script .t{{font-family:{font_stack};font-style:italic;font-weight:400;line-height:1.15;color:{theme.get('script', theme['fg'])};
  filter:{'drop-shadow(0 3px 10px rgba(0,0,0,.45))' if theme.get('gold') else 'none'}}}
.badge .t{{display:flex;justify-content:{'center' if align == 'center' else ('flex-end' if align == 'right' else 'flex-start')}}}
.badge .t span{{display:inline-block;font-weight:700;text-transform:uppercase;letter-spacing:.06em;line-height:1;padding:.5em 1.1em;
  border-radius:999px;background:{theme.get('badge_bg', theme['fg'])};color:{theme.get('badge_fg', theme['bg'])}}}
.image.fade-scrim-right::after{{background:linear-gradient(270deg,{theme['bg']}F0 0%,{theme['bg']}B3 38%,transparent 72%)}}
.image.fade-scrim-left::after{{background:linear-gradient(90deg,{theme['bg']}F0 0%,{theme['bg']}B3 38%,transparent 72%)}}
.image.fade-scrim-top::after{{background:linear-gradient(180deg,{theme['bg']}F0 0%,{theme['bg']}A6 40%,transparent 68%)}}
.kv-missing{{position:absolute;inset:0;display:grid;place-items:center;color:{theme['note']};font-size:{base * 0.03:.0f}px;
  background:repeating-linear-gradient(45deg,{theme['bg']},{theme['bg']} 20px,{theme['fg']}10 20px,{theme['fg']}10 40px)}}
.logo.pos-right{{left:auto;right:{int(w * 0.04)}px}} .logo.pos-center{{left:50%;transform:translateX(-50%)}}
.eyebrow .t{{font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:{theme['eyebrow']};line-height:1.3}}
.big .t{{font-weight:700;line-height:1.02;white-space:nowrap}}
{'.big .t span{background:linear-gradient(90deg,' + acc[0] + ',' + acc[1] + ');-webkit-background-clip:text;background-clip:text;color:transparent}' if theme.get('accent') else ''}
.dots{{position:absolute;left:{int(w * 0.07)}px;bottom:{int(h * 0.045)}px;display:flex;gap:{base * 0.012:.0f}px}}
.dots i{{display:block;width:{base * 0.012:.0f}px;height:{base * 0.012:.0f}px;border-radius:50%;background:{theme['fg']}44}}
.dots i.on{{width:{base * 0.04:.0f}px;border-radius:{base * 0.01:.0f}px;background:{theme['eyebrow']}}}
.host{{position:absolute;right:{int(w * 0.04)}px;top:{logo_y}px;height:{logo_h}px;display:flex;align-items:center;
  font-size:{base * 0.022 * (1.25 if w / h > 1.6 else 1):.0f}px;letter-spacing:.04em;color:{theme['note']}}}
.logo{{position:absolute;left:{int(w * 0.04)}px;top:{logo_y}px;width:{logo_w}px}}
.glow{{position:absolute;right:-{int(base * .25)}px;bottom:-{int(base * .3)}px;width:{int(base * .9)}px;height:{int(base * .9)}px;
  border-radius:50%;background:radial-gradient(circle,{brand['colors']['emerald']}33,transparent 65%)}}
"""
    meta = {"w": w, "h": h, "aspect": vkey, "theme": th_name, "safe": var.get("safe"), "slots": {}}

    def layers_html() -> list[str]:
        """Lớp chồng lên nền, dưới chữ: motif tách nền (bóng đổ mềm) hoặc lớp ánh sáng (blend screen)."""
        out = []
        for lay in cr.get("layers", []):
            src = ROOT / resolve_src(lay["src"])
            if not src.exists():
                meta.setdefault("layer_missing", []).append(lay["src"])
                continue
            lx, ly, lw, lh = lay["box"]
            tf = " ".join(x for x in (f"rotate({lay['rotate']}deg)" if lay.get("rotate") else "",
                                      "scaleX(-1)" if lay.get("flip") else "") if x)
            fx = (f'mix-blend-mode:{lay["blend"]};' if lay.get("blend") else
                  f'filter:drop-shadow(0 {base * 0.02:.0f}px {base * 0.04:.0f}px rgba(0,0,0,.45));')
            fit = "cover" if lay.get("cover") else "contain"
            # "fade": "left"|"right"|"top"|"bottom" → that visual edge melts into the background (no hard seam)
            if lay.get("fade") in ("left", "right", "top", "bottom"):
                side = lay["fade"]
                if lay.get("flip") and side in ("left", "right"):
                    side = "right" if side == "left" else "left"  # mask lives in the element's (mirrored) space
                to = {"left": "to right", "right": "to left", "top": "to bottom", "bottom": "to top"}[side]
                stop = int(lay.get("fade_pct", 45))
                grad = f"linear-gradient({to},transparent 0%,#000 {stop}%)"
                fx += f"-webkit-mask-image:{grad};mask-image:{grad};"
            out.append(f'<img class="layer" src="{src.as_uri()}" style="position:absolute;left:{lx * w:.0f}px;top:{ly * h:.0f}px;'
                       f'width:{lw * w:.0f}px;height:{lh * h:.0f}px;object-fit:{fit};opacity:{lay.get("opacity", 1)};'
                       f'{"transform:" + tf + ";" if tf else ""}{fx}">')
        return out

    parts = []
    if theme.get("glow"):
        parts.append('<div class="glow"></div>')
    if "image" not in var["regions"]:  # layout không có vùng ảnh (bignum, rows…) → lớp nằm ngay trên nền
        parts.extend(layers_html())
    for slot, r in effective_regions(var["regions"], cr, bool(layout.get("needs_image"))).items():
        x, y, bw, bh = r["box"]
        style = f"left:{x * w:.0f}px;top:{y * h:.0f}px;width:{bw * w:.0f}px;height:{bh * h:.0f}px"
        size = SIZE_PRESET.get(r.get("size", "m"), 0.045) * base * (1.25 if w / h > 1.6 else 1)
        v = r.get("valign", "start")
        if slot == "image":
            if img and not (ROOT / img["src"]).exists():
                meta["kv_missing"] = img["src"]
                img = None
            if not img and layout.get("needs_image"):
                meta["kv_missing"] = meta.get("kv_missing") or "chưa gán ảnh"
                parts.append('<div class="kv-missing">KV chưa có — xem creatives/prompts.md</div>')
                continue
            if img:
                fade = img.get("fade", r.get("fade", "none"))
                parts.append(f'<div class="r image fade-{fade}" style="{style}"><img src="{(ROOT / img["src"]).as_uri()}" '
                             f'style="object-position:{img["focus"]}"></div>')
            parts.extend(layers_html())
            continue
        if slot == "items":
            items = text.get("items") or []
            if not items:
                continue
            rows = "".join(f'<div class="it"><b>{i}</b><span>{html.escape(nfc(t))}</span></div>' for i, t in enumerate(items, 1))
            cls = layout.get("items_style", "rows")
            parts.append(f'<div class="r items {cls} v-{v}" style="{style}"><div class="t" data-fit data-slot="items" '
                         f'data-size="{size:.1f}" data-max-lines="{r.get("max_lines", 2) * len(items)}" '
                         f'style="font-size:{size:.1f}px">{rows}</div></div>')
            meta["slots"]["items"] = {"fg": [theme["fg"]], "bg": [theme["bg"]]}
            continue
        val = (text.get(slot) or "").strip()
        if not val:
            continue
        inner = headline_html(val, theme) if slot == "headline" else html.escape(nfc(val))
        if (slot == "headline" or (slot == "big" and cr.get("big_style") != "gold3d")) and theme.get("gold"):
            inner = f'<span class="gold">{inner}</span>'
        if slot == "big" and cr.get("big_style") == "gold3d":
            inner = f'<span data-t="{html.escape(nfc(val))}">{inner}</span>'
        elif slot in ("cta", "badge") or (slot == "big" and theme.get("accent")):
            inner = f"<span>{inner}</span>"
        sty = " gold3d" if slot == "big" and cr.get("big_style") == "gold3d" else ""
        parts.append(f'<div class="r {slot}{sty} v-{v}" style="{style}"><div class="t" data-fit data-slot="{slot}" '
                     f'data-size="{size:.1f}" data-max-lines="{r.get("max_lines", 3)}" style="font-size:{size:.1f}px">'
                     f'{inner}</div></div>')
        fg = {"headline": theme.get("display_ref", theme["fg"]) if theme.get("gold") else theme["fg"], "sub": theme["sub"],
              "note": theme["note"], "cta": theme["cta_fg"], "eyebrow": theme["eyebrow"], "big": theme["fg"],
              "script": theme.get("script", theme["fg"]), "badge": theme.get("badge_fg", theme["bg"])}[slot]
        bgs = cta_bg if slot == "cta" else ([theme.get("badge_bg", theme["fg"])] if slot == "badge" else [theme["bg"]])
        fgs = ([fg] + (acc if (slot in ("headline", "big") and theme.get("accent") and ("**" in val or slot == "big")) else []))
        meta["slots"][slot] = {"fg": fgs, "bg": bgs}
    if logo.exists():
        parts.append(f'<img class="logo pos-{cr.get("logo_pos") or layout.get("logo", "left")}" src="{logo.as_uri()}" alt="Chứng khoán DSC">')
    if cr.get("group") and cr.get("page") and cr.get("pages"):
        dots = "".join(f'<i class="{"on" if i == cr["page"] else ""}"></i>' for i in range(1, cr["pages"] + 1))
        parts.append(f'<div class="dots">{dots}</div>')
    if layout.get("host", True) and not cr.get("hide_host"):
        parts.append(f'<div class="host">{html.escape(brand["host"].split("//")[-1].replace("www.", ""))}</div>')
    meta["logo"] = logo.exists()
    if img and "image" not in var["regions"]:
        meta["image_dropped"] = True
    doc = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{html.escape(cr["id"])}</title>'
           f"<style>{css}</style></head><body>{''.join(parts)}</body></html>")
    return doc, meta


# ─────────────────────────── render + QA ───────────────────────────

FIT_JS = """
async () => {
  const f700 = await document.fonts.load('700 40px "Plus Jakarta Sans"', 'Ắệờ');
  const f400 = await document.fonts.load('400 40px "Plus Jakarta Sans"', 'Ắệờ');
  await document.fonts.ready;
  const out = {fontLoaded: f700.length > 0 && f400.length > 0, slots: {}};
  const MIN = %s;
  for (const el of document.querySelectorAll('[data-fit]')) {
    const box = el.parentElement, start = parseFloat(el.dataset.size), maxLines = parseInt(el.dataset.maxLines || '99');
    let size = start;
    const lines = () => { const lh = parseFloat(getComputedStyle(el).lineHeight) || size * 1.3; return Math.round(el.scrollHeight / lh); };
    const over = () => el.scrollHeight > box.clientHeight + 1 || el.scrollWidth > box.clientWidth + 1 || (!['items', 'cta', 'badge'].includes(el.dataset.slot) && lines() > maxLines);
    while (over() && size > start * MIN) { size = Math.max(start * MIN, size - Math.max(1, size * 0.04)); el.style.fontSize = size + 'px'; }
    const r = el.getBoundingClientRect(), b = box.getBoundingClientRect();
    out.slots[el.dataset.slot] = {start, size, lines: lines(), overflow: over(),
      rect: [r.left, Math.max(r.top, b.top), r.width, Math.min(r.height, b.height)]};
  }
  return out;
}
"""


def qa_creative(cr: dict, meta: dict, m: dict, png: Path, locks: dict, channel: str) -> list[dict]:
    issues = []

    def add(rule, level, msg):
        issues.append({"rule": rule, "level": level, "msg": msg})

    w, h = meta["w"], meta["h"]
    if not m.get("fontLoaded"):
        add("FONT-not-loaded", "error", "Font Plus Jakarta Sans (có dấu tiếng Việt) chưa nạp — kiểm brand.json fonts")
    if not meta.get("logo"):
        add("LOGO-missing", "error", "Không tìm thấy file logo trong brand.json")
    if meta.get("layer_missing"):
        add("LAYER-missing", "error", f"Không thấy motif: {', '.join(meta['layer_missing'])}")
    if meta.get("kv_missing"):
        add("KV-missing", "error", f"Chưa có ảnh KV ({meta['kv_missing']}) — chạy `creative.py prompt`, tạo ảnh bằng Gemini, lưu vào creatives/assets/")
    if meta.get("image_dropped"):
        add("IMAGE-dropped", "warn", f"Layout {cr['layout']} khổ {meta['aspect']} không có chỗ cho ảnh minh hoạ — ảnh bị bỏ")
    texts = cr.get("text", {})
    all_text = " ".join([texts.get(s, "") for s in TEXT_SLOTS] + list(texts.get("items") or []))
    if TODO in all_text:
        add("FIELD-placeholder", "error", "Còn TODO trong design.json — điền chữ cho slide/hàng")
    if not plain(texts.get("headline", "")):
        add("FIELD-missing", "error", "Thiếu headline")
    for slot, s in m.get("slots", {}).items():
        if s["overflow"]:
            add("FIT-overflow", "error", f"{slot}: chữ vẫn tràn khung ở {MIN_SCALE:.0%} cỡ gốc — rút ngắn chữ")
        elif s["size"] < s["start"] * 0.85:
            add("FIT-shrunk", "warn", f"{slot}: phải thu chữ còn {s['size'] / s['start']:.0%} — cân nhắc rút gọn")
        x, y, rw, rh = s["rect"]
        if x < 0 or y < 0 or x + rw > w + 1 or y + rh > h + 1:
            add("FIT-off-canvas", "error", f"{slot}: ra ngoài khung ảnh")
        if meta.get("safe"):
            sx, sy, sw, sh = meta["safe"]
            if y < sy * h - 1 or y + rh > (sy + sh) * h + 1:
                add("SAFE-zone", "warn", f"{slot}: nằm ngoài vùng an toàn story/reel (giao diện app có thể che)")
        eff = s["size"] * PHONE_W / w
        if eff < 9.5:
            add("MOBILE-small", "warn", f"{slot}: chữ chỉ ~{eff:.1f}px khi xem trên điện thoại rộng {PHONE_W}px")
        colors = meta["slots"].get(slot, {})
        need = 3.0 if s["size"] * 1080 / w >= 40 else 4.5
        bare = None if slot in ("badge", "cta") else (m.get("bare") or {}).get(slot)
        if bare:  # nền thật dưới chữ (ảnh KV): đo phân vị 10/90 độ sáng
            fgs_ = colors.get("fg") if isinstance(colors.get("fg"), list) else [colors.get("fg")]
            worst = min(contrast(f, bg_) for f in fgs_ if f for bg_ in bare)
            if worst < need:
                add("CONTRAST-photo", "error" if worst < need - 0.8 else "warn",
                    f"{slot}: trên nền ảnh chỉ đạt {worst:.1f}:1 (< {need}:1) — tăng scrim, đổi focus ảnh hoặc đổi phía đặt chữ")
            continue
        for fg in (colors.get("fg") if isinstance(colors.get("fg"), list) else [colors.get("fg")]):
            for bg in colors.get("bg") or []:
                if fg and bg:
                    c = contrast(fg, bg)
                    if c < need:
                        add("CONTRAST-low", "error" if c < need - 0.5 else "warn",
                            f"{slot}: tương phản {c:.1f}:1 ({fg} trên {bg}) < {need}:1")
    # red pixels (brand: không dùng đỏ)
    try:
        from PIL import Image
        im = Image.open(png).convert("RGB").resize((240, max(1, int(240 * h / w))))
        px = list(im.getdata())
        red = sum(1 for r, g, b in px if r > 170 and g < 90 and b < 90) / len(px)
        if red > 0.003:
            if cr.get("allow_red"):
                add("RED-pixels", "warn", f"{red:.1%} điểm ảnh đỏ — được phép vì motif văn hoá (allow_red); kiểm không có chữ/số/biểu đồ đỏ")
            else:
                add("RED-pixels", "error", f"{red:.1%} điểm ảnh màu đỏ — chỉ được dùng đỏ cho motif văn hoá (đặt \"allow_red\": true) — DESIGN.md §2")
    except ImportError:
        add("RED-pixels", "warn", "Không có Pillow để kiểm màu đỏ")
    # locked text
    want = locks.get(cr.get("adapted_from") or cr["id"])
    shown = " ".join(texts.get(s, "") for s in LOCK_SLOTS)
    if want is not None and not keeps_locked(want, shown):
        add("TEXT-locked", "error", f"Chữ trên ảnh không giữ đủ, đúng thứ tự chữ của bản copy (“{want}”) — sửa ở file copy, lint lại, init lại")
    words = len(plain(texts.get("headline", "")).split())
    if channel == "ads" and words > 8:
        add("WORDS-on-image", "warn", f"Chữ trên ảnh quảng cáo {words} từ > 8")
    elif words > 14:
        add("WORDS-on-image", "warn", f"Tiêu đề trên ảnh {words} từ > 14")
    # compliance + blacklist on image text (reuse mkt_lint)
    rep = ml.Report(cr["id"], channel)
    ml.check_compliance(rep, cr["id"], plain(all_text), "meta-ad" if channel == "ads" else "facebook")
    hard, _h, _s = ml.ql.load_blacklist()
    ml.check_anti_ai(rep, cr["id"], plain(all_text), hard, ml.ql.load_forbidden_terms())
    for i in rep.issues:
        if i.rule == "FIELD-placeholder":
            continue
        lvl = "error" if i.severity in ("CRITICAL", "MAJOR") else ("warn" if i.severity == "MINOR" else None)
        if lvl:
            add(i.rule, lvl, i.msg + (f" — “{i.text}”" if i.text else ""))
    return issues


def _tokens(s: str) -> list[str]:
    out = []
    for tok in plain(s).lower().split():
        tok = tok.strip(".,:;!?…“”\"'()•·–-")
        if tok:
            out.append(tok)
    return out


def keeps_locked(locked: str, shown: str) -> bool:
    """Chữ khoá phải xuất hiện đủ và đúng thứ tự trong chữ hiển thị (eyebrow → big → headline); được thêm nhãn phụ."""
    it = iter(_tokens(shown))
    return all(any(tok == s for s in it) for tok in _tokens(locked))


def bare_colors(bare_png: Path, slots: dict) -> dict:
    """Màu nền tối/sáng (phân vị 10 và 90 theo độ sáng) dưới từng khối chữ, chụp khi đã ẩn chữ."""
    from PIL import Image
    im = Image.open(bare_png).convert("RGB")
    out = {}
    for slot, s in slots.items():
        x, y, w, h = [int(v) for v in s["rect"]]
        if w < 4 or h < 4:
            continue
        crop = im.crop((max(0, x), max(0, y), min(im.width, x + w), min(im.height, y + h))).resize((48, 24))
        px = sorted(crop.getdata(), key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
        out[slot] = ["#%02X%02X%02X" % px[int(len(px) * q)] for q in (0.1, 0.9)]
    return out


def status_of(issues: list[dict]) -> str:
    if any(i["level"] == "error" for i in issues):
        return "Chưa đạt"
    return "Đạt có lưu ý" if issues else "Đạt"


def _launch_browser(p):
    """Launch bundled Chromium; fall back to system Edge/Chrome when it is missing
    (company machines may block `playwright install`)."""
    try:
        return p.chromium.launch()
    except Exception as first_err:
        for channel in ("msedge", "chrome"):
            try:
                return p.chromium.launch(channel=channel)
            except Exception:
                continue
        raise first_err


def render(design_path: Path, only: list[str] | None = None, bump: bool = False) -> tuple[Path, dict]:
    data = json.loads(design_path.read_text(encoding="utf-8"))
    approved_versions = {a["v"] for a in data.get("approved", [])}
    if bump:
        data["version"] = int(data.get("version", 1)) + 1
        design_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    ver = int(data.get("version", 1))
    if ver in approved_versions:
        raise SystemExit(f"v{ver} đã được duyệt — dùng --bump để ra v{ver + 1}, không render đè bản đã duyệt")
    brand = load_brand()
    out = design_path.parent / f"v{ver}"
    (out / "html").mkdir(parents=True, exist_ok=True)
    src = design_path.parent.parent / data.get("source", "")
    locks = locked_texts(src) if src.is_file() else {}
    qa_path = out / "qa.json"
    qa = json.loads(qa_path.read_text(encoding="utf-8")) if qa_path.exists() else {}
    qa.update({"job": data.get("job"), "version": ver, "rendered_at": datetime.now().isoformat(timespec="seconds")})
    qa.setdefault("creatives", {})
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = _launch_browser(p)
        for cr in data["creatives"]:
            if only and cr["id"] not in only and cr.get("group") not in only:
                continue
            if not cr.get("image"):
                for ext in ("png", "jpg", "jpeg", "webp"):
                    cand = design_path.parent / "assets" / f"{cr.get('adapted_from') or cr['id']}.{ext}"
                    if cand.exists():
                        cr = dict(cr, image={"src": str(cand.relative_to(ROOT)), **(cr.get("kv_focus") and {"focus": cr["kv_focus"]} or {})})
                        break
            doc, meta = compose(cr, brand)
            hp = out / "html" / f"{cr['id']}.html"
            hp.write_text(doc, encoding="utf-8")
            page = browser.new_page(viewport={"width": meta["w"], "height": meta["h"]}, device_scale_factor=1)
            page.goto(hp.as_uri())
            m = page.evaluate(FIT_JS % MIN_SCALE)
            png = out / f"{cr['id']}.png"
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": meta["w"], "height": meta["h"]})
            if cr.get("image"):
                page.add_style_tag(content="[data-fit]{visibility:hidden!important} .logo,.host,.dots{visibility:hidden}")
                bare_png = out / "html" / f"{cr['id']}.bare.png"
                page.screenshot(path=str(bare_png), clip={"x": 0, "y": 0, "width": meta["w"], "height": meta["h"]})
                m["bare"] = bare_colors(bare_png, m.get("slots", {}))
            page.close()
            issues = qa_creative(cr, meta, m, png, locks, data.get("channel", ""))
            qa["creatives"][cr["id"]] = {"size": cr["size"], "layout": cr["layout"], "theme": meta["theme"],
                                         "group": cr.get("group"), "status": status_of(issues), "issues": issues,
                                         "fit": {k: round(v["size"] / v["start"], 2) for k, v in m.get("slots", {}).items()}}
        browser.close()
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
    write_preview(out, data, qa)
    return out, qa


def write_preview(out: Path, data: dict, qa: dict) -> None:
    color = {"Đạt": "#0B7A1C", "Đạt có lưu ý": "#8A6100", "Chưa đạt": "#B00020"}
    cards = []
    for cr in data["creatives"]:
        q = qa["creatives"].get(cr["id"])
        if not q:
            continue
        iss = "".join(f"<li class='{i['level']}'>{html.escape(i['rule'])} — {html.escape(i['msg'])}</li>" for i in q["issues"])
        cards.append(f"""<figure><div class="pair"><img class="full" src="{cr['id']}.png" alt="{cr['id']}">
<div class="phone"><span>cỡ điện thoại</span><img src="{cr['id']}.png" alt=""></div></div>
<figcaption><b>{html.escape(cr['id'])}</b> · {cr['size']} · {cr['layout']} · {q['theme']}
<span class="st" style="background:{color[q['status']]}">{q['status']}</span><ul>{iss}</ul></figcaption></figure>""")
    doc = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(str(data.get('job')))} · creatives v{qa['version']}</title><style>
body{{margin:0;padding:24px;background:#EEF1F0;color:#0D1B2A;font-family:system-ui,sans-serif}}
h1{{font-size:22px;margin:0 0 4px}} p.m{{margin:0 0 24px;color:#4A5866}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:24px}}
figure{{margin:0;background:#fff;border-radius:12px;padding:16px}}
.pair{{display:flex;gap:16px;align-items:flex-start}} .full{{width:260px;border:1px solid #DDE3E1}}
.phone{{font-size:11px;color:#4A5866}} .phone img{{display:block;width:120px;border:1px solid #DDE3E1;margin-top:4px}}
figcaption{{margin-top:12px;font-size:14px}} .st{{color:#fff;border-radius:4px;padding:2px 8px;margin-left:6px;font-size:12px}}
ul{{margin:8px 0 0;padding-left:18px;font-size:13px}} li.error{{color:#B00020}} li.warn{{color:#8A6100}}
</style></head><body><h1>{html.escape(str(data.get('job')))} — creatives v{qa['version']}</h1>
<p class="m">Nguồn chữ: {html.escape(data.get('source', ''))} · render {qa['rendered_at']} · ảnh bên phải = cỡ xem trên điện thoại</p>
<div class="grid">{''.join(cards)}</div></body></html>"""
    (out / "preview.html").write_text(doc, encoding="utf-8")


# ─────────────────────────── adapt: thêm khổ cho kênh khác ───────────────────────────

def adapt(design_path: Path, sizes: list[str], only: list[str] | None = None) -> list[str]:
    data = json.loads(design_path.read_text(encoding="utf-8"))
    have = {c["id"] for c in data["creatives"]}
    added = []
    for cr in list(data["creatives"]):
        if cr.get("adapted_from") or (only and cr["id"] not in only and cr.get("group") not in only):
            continue
        for size in sizes:
            parse_size(size)
            if size == cr["size"]:
                continue
            nid = f"{cr['id']}-{size}"
            if nid in have:
                continue
            new = json.loads(json.dumps(cr))
            new.update(id=nid, size=size, adapted_from=cr["id"])
            data["creatives"].append(new)
            have.add(nid)
            added.append(nid)
    design_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return added


# ─────────────────────────── prompt: KV cho Gemini / công cụ tạo ảnh ───────────────────────────

KV_STYLE = {  # DESIGN.md §5 (abstract, default) and §7 (seasonal)
    "dark": ("abstract 3D render, glossy translucent green glass ribbons and silk-like folds twisting in layers with thin dark edges, "
             "soft diagonal streaks of green light on a near-black gunmetal background (#272D2B), lime green (#2AD03D) and "
             "emerald (#1BBE72) highlights, subtle frosted mint (#8CFFCC) glow, cinematic depth, minimal and premium"),
    "pine": ("abstract 3D render, soft organic flowing blobs of lime green (#2AD03D) and emerald (#1BBE72) over a deep pine teal "
             "(#1D4130) background, smooth gradients, gentle volumetric light, calm and modern"),
    "mint": ("abstract 3D render, translucent green glass ribbons and wavy refracted green forms on a pale mint background, "
             "lime green (#2AD03D) to emerald (#1BBE72) tones, soft studio light, airy, lots of clean empty space"),
    "paper": ("abstract soft-focus ambient gradient, blurred green to grey-teal tones (#354D38, #2C7B50, #7D9E9F, #B6C7AF), "
              "a hint of glass ribbon, minimal and calm, lots of clean empty space"),
    "emerald": ("premium cinematic 3D render, deep emerald green (#0B331E to #226435) environment, polished metallic gold "
                "(#EFD786 to #A57D3F) details with fine engraved Vietnamese patterns, soft volumetric light, subtle glowing "
                "green light trails (#5BD681), floating light particles, shallow depth of field, luxurious and calm"),
    "ivory": ("elegant contemporary Vietnamese silk-and-watercolor painting, warm ivory paper background (#F9F4EB) with faint "
              "cream (#EBE1C1) Dong Son drum texture, jade green (#6CB298) layered mountains and leaves, thin gold (#C9A24A) "
              "linework, airy, refined, lots of soft empty space"),
}
SIDE_EN = {"kv-right": "right", "kv-left": "left", "kv-center": "top"}


def kv_prompt(cr: dict) -> str:
    kv = cr.get("kv") or {}
    theme = cr.get("theme") or load_layout(cr["layout"]).get("default_theme", "dark")
    w, h = parse_size(cr["size"])
    side = SIDE_EN.get(cr["layout"], "right")
    subject_side = {"right": "left", "left": "right", "top": "bottom"}[side]
    ratio = {0.8: "4:5", 1.0: "1:1", 0.5625: "9:16", 1.91: "1.91:1"}.get(round(w / h, 4) if round(w / h, 2) != 1.91 else 1.91, f"{w}:{h}")
    red = ("Touches of Vietnamese lacquer red (#BA382B) are allowed only on the flag, silk ribbon, lotus or lanterns. "
           if cr.get("allow_red") else "No red anywhere. ")
    parts = [
        f"Key visual for a social media post of Chung khoan DSC, a Vietnamese securities company. Subject: {kv.get('subject', 'TODO')}.",
        f"Motifs: {', '.join(kv.get('motifs', []))}." if kv.get("motifs") else "",
        f"Mood: {kv['mood']}." if kv.get("mood") else "",
        f"Style: {KV_STYLE.get(theme, KV_STYLE['dark'])}.",
        f"Composition: place the main subject on the {subject_side} side; keep the {side} {45 if side != 'top' else 40}% of the frame "
        f"calm, softly lit and uncluttered as negative space for a text overlay added later.",
        f"Aspect ratio {ratio}, {w}x{h}px, high detail, sharp focus on the subject.",
        red,
        "Absolutely NO text, NO letters, NO numbers, NO logos, NO watermarks, NO brand marks, NO real people's faces, "
        "NO coins, NO banknotes, NO stock price arrows or profit symbols.",
    ]
    return " ".join(x for x in parts if x)


def write_prompts(design_path: Path, only: list[str] | None = None) -> Path:
    data = json.loads(design_path.read_text(encoding="utf-8"))
    lines = [f"# Prompts KV — {data.get('job')}", "",
             "Dán từng prompt vào Gemini (hoặc công cụ tạo ảnh khác), chọn ảnh đẹp nhất, lưu đúng tên file bên dưới vào "
             f"`{(design_path.parent / 'assets').relative_to(ROOT)}/`, rồi `python scripts/creative.py render {design_path.relative_to(ROOT)}`.",
             "Quy tắc: DESIGN.md §5. Ảnh có chữ / logo / đồng xu → tạo lại.", ""]
    n = 0
    for cr in data["creatives"]:
        if cr.get("adapted_from") or not cr["layout"].startswith("kv") or (only and cr["id"] not in only):
            continue
        n += 1
        lines += [f"## {cr['id']} · {cr['size']} · {cr['layout']}", f"Lưu thành: `assets/{cr['id']}.png`", "", "```", kv_prompt(cr), "```", ""]
    out = design_path.parent / "prompts.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ─────────────────────────── generate: tạo KV tự động qua Codex CLI ───────────────────────────
# Học từ tabcom-designer-plugin: gọi `codex exec` (dùng tài khoản ChatGPT đã đăng nhập, không cần API key),
# sandbox read-only, prompt cấm chạy lệnh; ảnh lấy từ ~/.codex/generated_images; mỗi ảnh tạo 1 lần (--force để tạo lại).

CODEX_IMG_DIR = Path.home() / ".codex" / "generated_images"
CODEX_WRAP = ("Use your built-in image generation tool to create exactly ONE image from the brief below. "
              "Do not run any shell commands, do not read or write files, do not ask questions. "
              "After the image is generated, reply only with the word DONE.\n\nBRIEF:\n")


def lint_prompt(prompt: str) -> list[str]:
    errs = []
    if "TODO" in prompt:
        errs.append("subject còn TODO")
    for must in ("NO text", "NO logos", "negative space", "Aspect ratio"):
        if must not in prompt:
            errs.append(f"thiếu “{must}”")
    if re.search(r"[À-ỹ]", prompt.split("Subject:")[-1]):
        errs.append("prompt có chữ tiếng Việt có dấu — model dễ vẽ chữ ra ảnh; viết mô tả bằng tiếng Anh")
    return errs


def cover_crop(src: Path, dst: Path, w: int, h: int, focus: tuple[float, float] = (0.5, 0.5)) -> None:
    from PIL import Image
    im = Image.open(src).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x = round((im.width - w) * focus[0])
    y = round((im.height - h) * focus[1])
    im.crop((x, y, x + w, y + h)).save(dst)


def codex_generate(prompt: str, raw_out: Path, timeout: int = 420, cwd: Path | None = None) -> dict:
    """Gọi `codex exec` (read-only) tạo 1 ảnh; lấy PNG mới nhất trong ~/.codex/generated_images.
    Codex đôi khi treo sau khi đã tạo xong ảnh → hết timeout vẫn đi tìm ảnh mới (học từ tabcom)."""
    import subprocess
    import time
    before = set(CODEX_IMG_DIR.rglob("*.png")) if CODEX_IMG_DIR.exists() else set()
    t0 = time.time()
    exit_code, err = None, ""
    try:
        proc = subprocess.run(["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "-"],
                              input=CODEX_WRAP + prompt, text=True, capture_output=True, timeout=timeout,
                              cwd=str(cwd or raw_out.parent))
        exit_code, err = proc.returncode, proc.stderr[-800:]
    except subprocess.TimeoutExpired:
        exit_code, err = "timeout", f"hết {timeout}s — tìm ảnh đã tạo"
    new = sorted((p for p in CODEX_IMG_DIR.rglob("*.png") if p not in before and p.stat().st_mtime >= t0 - 5),
                 key=lambda p: p.stat().st_mtime) if CODEX_IMG_DIR.exists() else []
    res = {"seconds": round(time.time() - t0), "codex_exit": exit_code, "images_generated": len(new)}
    if new:
        raw_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(new[-1], raw_out)
        res["status"] = "ok" if len(new) == 1 else f"ok (Codex tạo {len(new)} ảnh, lấy ảnh cuối)"
    else:
        res["status"] = "Codex không trả ảnh"
        res["stderr"] = err
    return res


def generate(design_path: Path, only: list[str] | None = None, force: bool = False, dry_run: bool = False,
             timeout: int = 420) -> list[dict]:
    data = json.loads(design_path.read_text(encoding="utf-8"))
    assets = design_path.parent / "assets"
    assets.mkdir(exist_ok=True)
    log = design_path.parent / "generate-log.jsonl"
    results = []
    for cr in data["creatives"]:
        if cr.get("adapted_from") or not cr["layout"].startswith("kv") or (only and cr["id"] not in only):
            continue
        dst = assets / f"{cr['id']}.png"
        if dst.exists() and not force:
            results.append({"id": cr["id"], "status": "đã có ảnh — bỏ qua (--force để tạo lại)"})
            continue
        prompt = kv_prompt(cr)
        errs = lint_prompt(prompt)
        if errs:
            results.append({"id": cr["id"], "status": "prompt lỗi: " + "; ".join(errs)})
            continue
        if dry_run:
            results.append({"id": cr["id"], "status": "dry-run — prompt hợp lệ", "prompt": prompt})
            continue
        raw = assets / f"{cr['id']}.raw.png"
        entry = {"id": cr["id"], "at": datetime.now().isoformat(timespec="seconds"), "prompt": prompt,
                 **codex_generate(prompt, raw, timeout)}
        if entry["status"].startswith("ok"):
            w, h = parse_size(cr["size"])
            cover_crop(raw, dst, w, h)
            entry["raw"] = raw.name
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        results.append(entry)
    return results


# ─────────────────────────── pick: chọn nền từ thư viện asset ───────────────────────────

SIDE_OF_LAYOUT = {"kv-right": "right", "kv-left": "left", "kv-center": "top"}
FOCUS_OF_SIDE = {"right": "50% 50%", "left": "50% 50%", "top": "50% 60%", "center": "50% 50%"}


def aspect_of(size: str) -> str:
    w, h = parse_size(size)
    return min(ASPECTS, key=lambda k: abs(ASPECTS[k] - w / h))


def pick(design_path: Path, only: list[str] | None = None, season: str | None = None, dry: bool = False) -> list[tuple]:
    """Gán nền thư viện cho ảnh KV chưa có nền. Ưu tiên thẻ trùng `kv.tags`/`kv.motifs`, mùa, ít dùng."""
    import asset_lib
    data = json.loads(design_path.read_text(encoding="utf-8"))
    season = season or data.get("season")
    out = []
    used_now: set[str] = set()
    for cr in data["creatives"]:
        if not cr["layout"].startswith("kv") or cr.get("image") or (only and cr["id"] not in only):
            continue
        if (design_path.parent / "assets" / f"{cr['id']}.png").exists():
            continue
        kv = cr.get("kv") or {}
        tags = kv.get("tags") or [w for m in kv.get("motifs", []) for w in m.split()] + kv.get("subject", "").split()
        theme = cr.get("theme") or load_layout(cr["layout"]).get("default_theme")
        side = SIDE_OF_LAYOUT.get(cr["layout"], "right")
        cands = [c for c in asset_lib.find(theme, side, aspect_of(cr["size"]), tags, "bg", season, limit=8) if c[0] not in used_now]
        if not cands:
            out.append((cr["id"], None, "không có nền hợp — dùng `generate`"))
            continue
        aid = cands[0][0]
        used_now.add(aid)
        cr["image"] = {"src": f"lib:{aid}", "focus": FOCUS_OF_SIDE.get(side, "50% 50%")}
        out.append((cr["id"], aid, f"điểm {cands[0][2]}"))
        if not dry:
            asset_lib.record_use(aid, data.get("job", ""), cr["id"])
    if not dry:
        design_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


# ─────────────────────────── approve ───────────────────────────

def approve(design_path: Path, ids: list[str] | str, xac_nhan: str, accept_errors: bool = False) -> list[Path]:
    if not xac_nhan.strip():
        raise SystemExit("--xac-nhan phải là lời duyệt của user")
    data = json.loads(design_path.read_text(encoding="utf-8"))
    ver = int(data.get("version", 1))
    out = design_path.parent / f"v{ver}"
    qa = json.loads((out / "qa.json").read_text(encoding="utf-8"))
    want = list(qa["creatives"]) if ids == "all" else ids
    bad = [i for i in want if i not in qa["creatives"]]
    if bad:
        raise SystemExit(f"Chưa render: {bad}")
    errs = [i for i in want if qa["creatives"][i]["status"] == "Chưa đạt"]
    if errs and not accept_errors:
        raise SystemExit(f"Còn lỗi QA ở {errs} — sửa rồi render lại, hoặc --chap-nhan-loi nếu user chấp nhận")
    job_dir = design_path.parent.parent.parent
    dest_dir = job_dir / "approved"
    dest_dir.mkdir(exist_ok=True)
    copied = []
    for i in want:
        dst = dest_dir / f"{data.get('job')}-{i}-v{ver}.png"
        shutil.copy2(out / f"{i}.png", dst)
        copied.append(dst)
    data.setdefault("approved", []).append({"v": ver, "ids": want, "xac_nhan": xac_nhan,
                                            "luc": datetime.now().isoformat(timespec="seconds"),
                                            "chap_nhan_loi": bool(errs)})
    design_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return copied


def _job_of(design) -> str:
    hit = _act_classify(Path(design).resolve())
    return hit[1] if hit else Path(design).parent.parent.name


def main(argv=None) -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("copy")
    p = sub.add_parser("render")
    p.add_argument("design")
    p.add_argument("--only")
    p.add_argument("--bump", action="store_true")
    p = sub.add_parser("approve")
    p.add_argument("design")
    p.add_argument("--ids", required=True)
    p.add_argument("--xac-nhan", required=True)
    p.add_argument("--chap-nhan-loi", action="store_true")
    sub.add_parser("layouts")
    p = sub.add_parser("pick")
    p.add_argument("design")
    p.add_argument("--only")
    p.add_argument("--season")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("generate")
    p.add_argument("design")
    p.add_argument("--only")
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("prompt")
    p.add_argument("design")
    p.add_argument("--only")
    p = sub.add_parser("adapt")
    p.add_argument("design")
    p.add_argument("--channel", help=", ".join(CHANNEL_SIZES))
    p.add_argument("--sizes", help="vd. 1080x1920,1200x628")
    p.add_argument("--only")
    a = ap.parse_args(argv)
    if a.cmd == "init":
        d = init(Path(a.copy).resolve())
        n = len(json.loads(d.read_text(encoding="utf-8"))["creatives"])
        print(f"{d} — {n} ảnh. Điền TODO (nếu có) rồi: python scripts/creative.py render {d}")
    elif a.cmd == "render":
        out, qa = render(Path(a.design).resolve(), a.only.split(",") if a.only else None, a.bump)
        bad = 0
        for cid, q in qa["creatives"].items():
            print(f"{q['status']:<13} {cid:<22} {q['size']:<10} {q['layout']}")
            for i in q["issues"]:
                print(f"    [{i['level']}] {i['rule']} — {i['msg']}")
            bad += q["status"] == "Chưa đạt"
        print(f"→ {out / 'preview.html'}")
        emit("creative", "qa", _job_of(a.design), skill="creative render", path=out / "qa.json",
             result=f"{len(qa['creatives']) - bad}/{len(qa['creatives'])} đạt")
        return 1 if bad else 0
    elif a.cmd == "approve":
        for p_ in approve(Path(a.design).resolve(), "all" if a.ids == "all" else a.ids.split(","), a.xac_nhan, a.chap_nhan_loi):
            print(p_)
        emit("creative", "approve", _job_of(a.design), skill="creative approve", path=a.design,
             note=f"{a.ids} · {a.xac_nhan}"[:200])
    elif a.cmd == "pick":
        for cid, aid, note in pick(Path(a.design).resolve(), a.only.split(",") if a.only else None, a.season, a.dry_run):
            print(f"{cid:<18} → {aid or '—':<22} {note}")
    elif a.cmd == "generate":
        res = generate(Path(a.design).resolve(), a.only.split(",") if a.only else None, a.force, a.dry_run)
        for r_ in res:
            print(f"{r_['id']:<18} {r_['status']}" + (f"  ({r_['seconds']}s)" if "seconds" in r_ else ""))
        if not a.dry_run and res:
            emit("creative", "create", _job_of(a.design), skill="creative generate", path=a.design,
                 result=", ".join(f"{r_['id']} {r_['status']}" for r_ in res)[:200])
        return 1 if any(r_["status"].startswith(("prompt lỗi", "Codex")) for r_ in res) else 0
    elif a.cmd == "prompt":
        print(write_prompts(Path(a.design).resolve(), a.only.split(",") if a.only else None))
    elif a.cmd == "adapt":
        sizes = CHANNEL_SIZES.get(a.channel, []) if a.channel else []
        sizes += a.sizes.split(",") if a.sizes else []
        if not sizes:
            raise SystemExit(f"Cần --channel ({', '.join(CHANNEL_SIZES)}) hoặc --sizes")
        added = adapt(Path(a.design).resolve(), sizes, a.only.split(",") if a.only else None)
        print(f"Thêm {len(added)} ảnh: {', '.join(added) or '—'} → render lại để xem")
    elif a.cmd == "layouts":
        for p_ in sorted(LAYOUT_DIR.glob("*.json")):
            lay = json.loads(p_.read_text(encoding="utf-8"))
            print(f"{lay['name']:<9} {lay.get('style', ''):<4} {', '.join(lay['variants'])} — {lay.get('mo_ta', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
