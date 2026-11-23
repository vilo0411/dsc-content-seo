"""DSC article-image design system (tokens + components) for PIL.
Spec: knowledge/1-brand/image-design-system.md — keep both in sync.

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
C = {
    "green": "#00AD14",      # brand primary: data highlight, numbers that matter
    "green_700": "#00801A",  # text-safe green on light bg (AA on white)
    "green_900": "#0B4D2A",
    "bright": "#2BE841",     # gradient start, only on navy
    "teal": "#10E7B3",       # gradient end, only on navy
    "navy": "#0D1B2A",       # text, dark surfaces, "bad" data (no red)
    "navy_800": "#13263A",
    "navy_700": "#1C3348",
    "ink_2": "#425466",      # secondary text
    "ink_3": "#7A8A99",      # captions, axis
    "line": "#DCE7E1",       # borders, dividers
    "track": "#E6F0EA",      # chart tracks, empty bars
    "neutral": "#B6C2CC",    # baseline / comparison data
    "mint_50": "#F4FAF7",    # light canvas
    "mint_100": "#E8F8F2",   # tags, soft fills
    "white": "#FFFFFF",
}

# ---- type scale (final px, Be Vietnam Pro) --------------------------------
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
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, f"BeVietnamPro-{weight}.ttf"), size * SS)
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
            for ch in s:
                self.d.text((cx, y * SS), ch, font=f, fill=C.get(fill, fill), anchor="l" + anchor[1])
                cx += self.d.textlength(ch, font=f) + tracking * SS
            return
        self.d.text((x * SS, y * SS), s, font=f, fill=C.get(fill, fill), anchor=anchor)

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
