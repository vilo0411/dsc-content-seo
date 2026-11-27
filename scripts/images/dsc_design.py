"""DSC article-image design system (tokens + components) for PIL.
Spec: .agents/skills/image/references/image-design-system.md — keep both in sync.

Everything is drawn at SS x scale and downsampled (anti-aliasing PIL lacks).
Coordinates passed to Canvas methods are in final pixels.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_DIR = os.path.join(ROOT, "knowledge/1-brand/assets/fonts")
LOGO_DIR = os.path.join(ROOT, "knowledge/1-brand/assets/logos")
SS = 3

# ---- colour tokens -------------------------------------------------------
# Brand guideline v1.0 (knowledge/1-brand/DESIGN.md, brand.json). Old token names
# (green/navy/bright/teal) are kept as aliases so per-article generate_*.py still run.
C = {
    "gunmetal": "#272D2B",
    "pine_teal": "#1D4130",
    "lime": "#2AD03D",
    "emerald": "#1BBE72",
    "frosted_mint": "#8CFFCC",
    "green": "#2AD03D",      # = lime: data highlight, bars, lines (never text on white; text on it = gunmetal)
    "green_700": "#1D4130",  # = pine_teal: text-safe green on light bg
    "green_900": "#1D4130",
    "bright": "#61CC6C",     # primary gradient start
    "teal": "#14A46E",       # primary gradient end
    "navy": "#272D2B",       # = gunmetal: text, dark surfaces, "bad" data (no red)
    "navy_800": "#1D4130",   # = pine_teal: surface on dark bg
    "navy_700": "#34403C",
    "ink_2": "#4A524F",      # secondary text
    "ink_3": "#666F6C",      # captions, axis (AA on white)
    "line": "#DCE5E0",       # borders, dividers
    "track": "#E8F0EC",      # chart tracks, empty bars
    "neutral": "#B9C3BF",    # baseline / comparison data
    "mint_50": "#F2FBF6",    # light canvas
    "mint_100": "#DDF7EA",   # tags, soft fills
    "white": "#FFFFFF",
}

# ---- type scale (final px, Plus Jakarta Sans) ------------------------------
TYPE = {  # for the 800x500 canvas
    "display": ("ExtraBold", 46), "h1": ("Bold", 26), "h2": ("SemiBold", 17),
    "body": ("Regular", 14), "body_m": ("Medium", 14), "caption": ("Medium", 12),
    "eyebrow": ("SemiBold", 11), "num_xl": ("ExtraBold", 46), "num_l": ("ExtraBold", 26),
    "num_m": ("Bold", 19),
}

# ---- layout tokens -----------------------------------------------------------
CANVAS = (800, 500)       # CMS standard for in-article images, 16:10
INLINE = CANVAS
FEATURED = (800, 480)     # featured/cover: drawn on 800x480 (5:3) with the same type scale...
FEATURED_OUT = (1000, 600)  # ...and exported at 1000x600
MARGIN = 40               # outer margin
RADIUS = 14               # cards
GAP = 12                  # base spacing unit = 4

_font_cache = {}


def font(weight, size):
    key = (weight, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, f"PlusJakartaSans-{weight}.ttf"), size * SS)
    return _font_cache[key]


def tfont(token):
    w, s = TYPE[token]
    return font(w, s)


def hex_rgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


class Canvas:
    def __init__(self, size, bg, out=None):
        self.w, self.h = size
        self.out = out or size
        self.img = Image.new("RGBA", (self.w * SS, self.h * SS), hex_rgb(C.get(bg, bg)))
        self.d = ImageDraw.Draw(self.img)
        self.cards = []   # card boxes, final px — used by check_layout()
        self.texts = []   # (bbox final px, string) of every drawn text

    # -- layout QA: text must stay inside its card and inside the canvas --
    def track(self, bbox_ss, s):
        """Register a text bbox given in SS pixels. Call this when drawing with self.d.text directly."""
        self.texts.append((tuple(v / SS for v in bbox_ss), s))

    def check_layout(self, pad=2):
        """Return overflow problems: text crossing the edge of the card it sits in, or leaving the canvas."""
        issues = []
        for (x0, y0, x1, y1), s in self.texts:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            home = [c for c in self.cards if c[0] <= cx <= c[2] and c[1] <= cy <= c[3]]
            if home:
                c = min(home, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))  # innermost card
                if x0 < c[0] + pad or x1 > c[2] - pad or y0 < c[1] + pad or y1 > c[3] - pad:
                    issues.append(f'"{s}" tràn khỏi card ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) '
                                  f'vs card ({c[0]:.0f},{c[1]:.0f})-({c[2]:.0f},{c[3]:.0f})')
            elif x0 < pad or y0 < pad or x1 > self.w - pad or y1 > self.h - pad:
                issues.append(f'"{s}" tràn khỏi khung ảnh ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})')
        return issues

    # -- primitives (final-pixel coords) --
    def _s(self, *v):
        return [x * SS for x in v]

    def rect(self, x0, y0, x1, y1, fill, r=0, outline=None, width=1):
        self.d.rounded_rectangle(self._s(x0, y0, x1, y1), radius=r * SS, fill=C.get(fill, fill),
                                 outline=C.get(outline, outline) if outline else None, width=width * SS)

    def shadow(self, x0, y0, x1, y1, r=RADIUS, blur=12, alpha=26, dy=5):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle(self._s(x0, y0 + dy, x1, y1 + dy), radius=r * SS,
                                                fill=(13, 27, 42, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(blur * SS))
        self.img.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.img)

    def card(self, x0, y0, x1, y1, fill="white", r=RADIUS, border="line", shadow=True):
        if shadow:
            self.shadow(x0, y0, x1, y1, r)
        self.rect(x0, y0, x1, y1, fill, r, outline=border, width=1 if border else 1)
        self.cards.append((x0, y0, x1, y1))

    def ellipse(self, x0, y0, x1, y1, fill):
        self.d.ellipse(self._s(x0, y0, x1, y1), fill=C.get(fill, fill))

    def line(self, pts, fill, width=2):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=C.get(fill, fill), width=width * SS, joint="curve")

    def text(self, x, y, s, token, fill, anchor="la", tracking=0):
        f = tfont(token) if token in TYPE else token
        if tracking:
            cx = x * SS
            if anchor[0] != "l":
                total = sum(self.d.textlength(ch, font=f) + tracking * SS for ch in s) - tracking * SS
                cx -= total if anchor[0] == "r" else total / 2
            start = cx
            for ch in s:
                self.d.text((cx, y * SS), ch, font=f, fill=C.get(fill, fill), anchor="l" + anchor[1])
                cx += self.d.textlength(ch, font=f) + tracking * SS
            bb = self.d.textbbox((start, y * SS), s, font=f, anchor="l" + anchor[1])
            self.track((start, bb[1], cx, bb[3]), s)
            return
        self.d.text((x * SS, y * SS), s, font=f, fill=C.get(fill, fill), anchor=anchor)
        self.track(self.d.textbbox((x * SS, y * SS), s, font=f, anchor=anchor), s)

    def tlen(self, s, token):
        f = tfont(token) if token in TYPE else token
        return self.d.textlength(s, font=f) / SS

    def wrap(self, x, y, s, token, fill, max_w, lh=1.3):
        words, line, lines = s.split(), "", []
        for w_ in words:
            t = (line + " " + w_).strip()
            if self.tlen(t, token) > max_w and line:
                lines.append(line)
                line = w_
            else:
                line = t
        lines.append(line)
        size = TYPE[token][1]
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * lh, ln, token, fill)
        return y + len(lines) * size * lh

    def gradient_rect(self, x0, y0, x1, y1, c0="bright", c1="teal", r=0, vertical=False, mask_alpha=255):
        W, H = int((x1 - x0) * SS), int((y1 - y0) * SS)
        a, b = hex_rgb(C.get(c0, c0)), hex_rgb(C.get(c1, c1))
        grad = Image.new("RGBA", (W, H))
        gd = ImageDraw.Draw(grad)
        n = H if vertical else W
        for i in range(n):
            t = i / max(1, n - 1)
            col = tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3)) + (mask_alpha,)
            gd.line([(0, i), (W, i)] if vertical else [(i, 0), (i, H)], fill=col)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), radius=r * SS, fill=255)
        self.img.paste(grad, (int(x0 * SS), int(y0 * SS)), m)
        self.d = ImageDraw.Draw(self.img)

    def gradient_text(self, x, y, s, token, c0="bright", c1="teal"):
        f = tfont(token)
        bbox = self.d.textbbox((x * SS, y * SS), s, font=f)
        W, H = bbox[2] - bbox[0], bbox[3] - bbox[1]
        m = Image.new("L", self.img.size, 0)
        ImageDraw.Draw(m).text((x * SS, y * SS), s, font=f, fill=255)
        grad = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(grad)
        a, b = hex_rgb(C[c0]), hex_rgb(C[c1])
        for i in range(W):
            t = i / max(1, W - 1)
            gd.line([(bbox[0] + i, bbox[1]), (bbox[0] + i, bbox[3])],
                    fill=tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3)) + (255,))
        self.img.paste(grad, (0, 0), m)
        self.d = ImageDraw.Draw(self.img)

    def glow(self, cx, cy, r, color="green", alpha=90):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(self._s(cx - r, cy - r, cx + r, cy + r), fill=hex_rgb(C[color], alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(r * SS * 0.45))
        self.img.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.img)

    def paste_logo(self, x, y, dark, height=30):
        lg = Image.open(os.path.join(LOGO_DIR, "logo-for-dark-bg.png" if dark else "logo-for-light-bg.png")).convert("RGBA")
        hh = height * SS
        lg = lg.resize((int(lg.width * hh / lg.height), hh), Image.Resampling.LANCZOS)
        self.img.alpha_composite(lg, (int(x * SS), int(y * SS)))

    def save(self, path, quality=90):
        # Refuse to write an image whose text overflows a card / the canvas (set DSC_ALLOW_OVERFLOW=1 to bypass).
        issues = self.check_layout()
        if issues and not os.environ.get("DSC_ALLOW_OVERFLOW"):
            raise ValueError(f"{os.path.basename(path)}: chữ tràn layout, chưa lưu ảnh:\n  " + "\n  ".join(issues))
        out = self.img.resize(self.out, Image.Resampling.LANCZOS).convert("RGB")
        out.save(path, quality=quality, optimize=True, subsampling=0)
        print(path, out.size)


# ---- components -----------------------------------------------------------------
def inline_frame(title, subtitle=None, eyebrow=None, source=None):
    """Light 4:3 frame: logo top-left, eyebrow, title, optional subtitle, footer. Returns (canvas, content_top)."""
    cv = Canvas(INLINE, "mint_50")
    cv.paste_logo(MARGIN, 30, dark=False, height=20)
    if eyebrow:
        cv.text(INLINE[0] - MARGIN, 40, eyebrow.upper(), "eyebrow", "green_700", anchor="rm", tracking=1.2)
    y = cv.wrap(MARGIN, 66, title, "h1", "navy", INLINE[0] - 2 * MARGIN, lh=1.25)
    if subtitle:
        y = cv.wrap(MARGIN, y + 2, subtitle, "body", "ink_2", INLINE[0] - 2 * MARGIN)
    fy = INLINE[1] - 26
    cv.line([(MARGIN, fy - 16), (INLINE[0] - MARGIN, fy - 16)], "line", 1)
    if source:
        cv.text(MARGIN, fy, source, "caption", "ink_3", anchor="lm")
    cv.text(INLINE[0] - MARGIN, fy, "dsc.com.vn", "caption", "green_700", anchor="rm")
    return cv, y + 16


def tag(cv, x, y, s, anchor_right=False, fill="mint_100", color="green_700"):
    w = cv.tlen(s, "caption") + 18
    x0 = x - w if anchor_right else x
    cv.rect(x0, y, x0 + w, y + 22, fill, r=11)
    cv.text(x0 + w / 2, y + 11, s, "caption", color, anchor="mm")
    return w
