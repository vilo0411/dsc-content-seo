"""Replacement images for do-lech-chuan-la-gi (DSC image design system, dsc_design.py).
Replaces the Google Docs formula crops and the ~60 single-key fx-570 / fx-580 crops.
In-article 800x500. Run from repo root:
    python scripts/images/generate_do_lech_chuan_images.py
"""
import os
import sys

from PIL import ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (MARGIN, CANVAS, SS, C, font, inline_frame, tag)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "do-lech-chuan-la-gi"
W, H = CANVAS
R = W - MARGIN
BOTTOM = H - 58

# Plus Jakarta Sans has no Greek glyphs; use Segoe UI for Σ σ μ only.
GREEK = "C:/Windows/Fonts/segoeuib.ttf"
GREEK_R = "C:/Windows/Fonts/segoeui.ttf"


def out(name):
    return os.path.join(OUT, f"{SLUG}-{name}.jpg")


def greek(size, bold=True):
    return ImageFont.truetype(GREEK if bold else GREEK_R, size * SS)


# ---- tiny math typesetter --------------------------------------------------------
# A run is a list of items: (text, kind) with kind in {"t" text, "g" greek, "sub", "sup", "bar" (x with overline)}
def _font_for(kind, size, weight):
    if kind == "g":
        return greek(size)
    if kind in ("sub", "sup"):
        return font(weight, int(size * 0.62))
    return font(weight, size)


def run_width(cv, items, size, weight="SemiBold"):
    w = 0
    for s, kind in items:
        w += cv.d.textlength(s, font=_font_for(kind, size, weight)) / SS
    return w


def draw_run(cv, x, y, items, size, color="navy", weight="SemiBold"):
    """Draw a math run with baseline at y (final px). Returns end x."""
    for s, kind in items:
        f = _font_for(kind, size, weight)
        dy = 0
        if kind == "sub":
            dy = size * 0.28
        elif kind == "sup":
            dy = -size * 0.42
        cv.d.text((x * SS, (y + dy) * SS), s, font=f, fill=C[color], anchor="ls")
        cv.track(cv.d.textbbox((x * SS, (y + dy) * SS), s, font=f, anchor="ls"), s)
        tw = cv.d.textlength(s, font=f) / SS
        if kind == "bar":
            top = y - size * 0.62
            cv.line([(x + 1, top), (x + tw - 1, top)], color, 2)
        x += tw
    return x


def fraction(cv, x, y_bar, num, den, size, color="navy", lead=None):
    """lead (run) is drawn left of the fraction on the bar axis. Returns end x."""
    if lead:
        x = draw_run(cv, x, y_bar + size * 0.35, lead, size, color) + 8
    nw, dw = run_width(cv, num, size), run_width(cv, den, size)
    fw = max(nw, dw) + 12
    draw_run(cv, x + (fw - nw) / 2, y_bar - 9, num, size, color)
    cv.line([(x, y_bar), (x + fw, y_bar)], color, 2)
    draw_run(cv, x + (fw - dw) / 2, y_bar + size + 6, den, size, color)
    return x + fw


def keycap(cv, x, y, s, dark=False):
    w = max(26, cv.tlen(s, "caption") + 14)
    cv.rect(x, y, x + w, y + 24, "navy" if dark else "white", r=6, outline=None if dark else "neutral")
    cv.text(x + w / 2, y + 12, s, "caption", "white" if dark else "navy", anchor="mm")
    return w


def keys_row(cv, x, y, keys, max_x):
    """Flow keycaps; '→' and plain words render as text. Returns bottom y."""
    x0, cy = x, y
    for k in keys:
        if k.startswith("~"):  # plain text token
            s = k[1:]
            tw = cv.tlen(s, "caption") + 6
            if cy and x + tw > max_x:
                x, cy = x0, cy + 30
            cv.text(x + 2, cy + 12, s, "caption", "ink_3", anchor="lm")
            x += tw
            continue
        w = max(26, cv.tlen(k, "caption") + 14)
        if x + w > max_x:
            x, cy = x0, cy + 30
        keycap(cv, x, cy, k, dark=k in ("SHIFT", "MODE", "MENU", "OPTN", "AC"))
        x += w + 5
    return cy + 24


def steps_card(cv, x0, y0, x1, y1, steps):
    cv.card(x0, y0, x1, y1)
    n = len(steps)
    row_h = (y1 - y0 - 20) / n
    for i, (label, keys) in enumerate(steps):
        ry = y0 + 12 + i * row_h
        last = i == n - 1
        cv.rect(x0 + 16, ry + 4, x0 + 40, ry + 28, "navy" if last else "green", r=8)
        cv.text(x0 + 28, ry + 16, str(i + 1), "caption", "white" if last else "navy", anchor="mm")
        cv.text(x0 + 52, ry + 16, label, "body_m", "navy", anchor="lm")
        keys_row(cv, x0 + 52, ry + 30, keys, x1 - 14)
        if not last:
            cv.line([(x0 + 52, ry + row_h - 2), (x1 - 16, ry + row_h - 2)], "track", 1)


def result_card(cv, x0, y0, x1, y1, head, rows):
    """Dark 'calculator screen' card. rows = [(label_run, value, highlight)]."""
    cv.shadow(x0, y0, x1, y1)
    cv.rect(x0, y0, x1, y1, "navy", r=14)
    cv.text(x0 + 18, y0 + 24, head, "eyebrow", "frosted_mint", anchor="lm", tracking=1.2)
    ry = y0 + 62
    step = (y1 - ry - 18) / len(rows)
    for lab, val, hi in rows:
        draw_run(cv, x0 + 18, ry + 14, lab, 17, "white" if not hi else "frosted_mint")
        cv.text(x1 - 18, ry + 14, val, "num_l" if hi else "num_m", "frosted_mint" if hi else "white", anchor="rs")
        ry += step


# ---- images ------------------------------------------------------------------------
X_BAR = [("x", "bar")]
XI = [("x", "t"), ("i", "sub")]


def formulas():
    cv, top = inline_frame("Công thức tính độ lệch chuẩn",
                           "Độ lệch chuẩn là căn bậc hai của phương sai. Mẫu chia cho n − 1, tổng thể chia cho N",
                           eyebrow="Công thức")
    gap = 16
    cw = (R - MARGIN - gap) / 2
    cards = [
        ("Mẫu", "Dùng khi chỉ có một phần dữ liệu", [("s", "t")], X_BAR, [("n − 1", "t")],
         [("Σ", "g")], X_BAR + [(": trung bình mẫu · n: số quan sát", "t")]),
        ("Tổng thể", "Dùng khi có toàn bộ dữ liệu", [("σ", "g")], [("μ", "g")], [("N", "t")],
         [("Σ", "g")], [("μ", "g"), (": trung bình tổng thể · N: số phần tử", "t")]),
    ]
    for i, (head, sub, sym, mean, den, sig, legend) in enumerate(cards):
        x0 = MARGIN + i * (cw + gap)
        x1 = x0 + cw
        cv.card(x0, top, x1, BOTTOM)
        tag(cv, x0 + 20, top + 18, head)
        cv.text(x0 + 20, top + 56, sub, "body", "ink_2")
        size = 24
        # variance: sym² = Σ(xi − mean)² / den
        lead = sym + [("2", "sup"), (" = ", "t")]
        num = sig + [("(", "t")] + XI + [(" − ", "t")] + mean + [(")", "t"), ("2", "sup")]
        fraction(cv, x0 + 24, top + 112, num, den, size, lead=lead)
        cv.text(x0 + 20, top + 162, "Phương sai", "caption", "ink_3")
        # std dev: sym = √sym²
        y = top + 220
        x = draw_run(cv, x0 + 24, y, sym + [(" = ", "t")], 30)
        x = draw_run(cv, x, y, [("√", "t")], 30, "green_700")
        top_y = y - 30
        x_end = draw_run(cv, x, y, sym + [("2", "sup")], 30)
        cv.line([(x - 1, top_y), (x_end + 2, top_y)], "green_700", 2)
        cv.text(x0 + 20, y + 12, "Độ lệch chuẩn", "caption", "ink_3")
        cv.line([(x0 + 20, BOTTOM - 42), (x1 - 20, BOTTOM - 42)], "line", 1)
        draw_run(cv, x0 + 20, BOTTOM - 18, legend, 13, "ink_2", weight="Medium")
    cv.save(out("cong-thuc"))


def fx570():
    cv, top = inline_frame("Tính độ lệch chuẩn bằng Casio fx-570ES PLUS",
                           "Dữ liệu x = {1, 2, 2, 3, 3, 3, 4, 4, 5}, nhập theo tần số",
                           eyebrow="Máy tính Casio")
    split = 500
    steps = [
        ("Bật cột tần số (FREQ)", ["SHIFT", "MODE", "▼", "4", "1", "~STAT → ON"]),
        ("Chọn thống kê 1 biến", ["MODE", "3", "1", "~STAT → 1-VAR"]),
        ("Nhập cột X rồi cột FREQ (mỗi số nhấn =)", ["~X:", "1", "2", "3", "4", "5", "~· FREQ:",
                                                     "1", "2", "3", "2", "1"]),
        ("Tính giá trị trung bình", ["AC", "SHIFT", "1", "4", "2", "="]),
        ("Tính độ lệch chuẩn tổng thể", ["AC", "SHIFT", "1", "4", "3", "="]),
    ]
    steps_card(cv, MARGIN, top, split, BOTTOM, steps)
    result_card(cv, split + 16, top, R, BOTTOM, "KẾT QUẢ", [
        (X_BAR + [("  trung bình", "t")], "3", False),
        ([("n", "t"), ("  số quan sát", "t")], "9", False),
        ([("σ", "g"), ("x", "t")], "1,1547", True),
    ])
    cv.save(out("fx-570es"))


def fx580():
    cv, top = inline_frame("Tính độ lệch chuẩn bằng Casio fx-580VN X",
                           "Năng suất lúa 25, 30, 35, 40, 45 với tần số 1, 1, 9, 5, 8 (tổng 24)",
                           eyebrow="Máy tính Casio")
    split = 500
    steps = [
        ("Vào chế độ thống kê", ["MENU", "6", "~Statistics"]),
        ("Chọn thống kê 1 biến", ["1", "~1-Variable"]),
        ("Nhập cột x (mỗi số nhấn =)", ["25", "30", "35", "40", "45"]),
        ("Lên ô đầu cột Freq, nhập tần số", ["1", "1", "9", "5", "8"]),
        ("Xem kết quả", ["OPTN", "3", "~1-Variable Calc"]),
    ]
    steps_card(cv, MARGIN, top, split, BOTTOM, steps)
    result_card(cv, split + 16, top, R, BOTTOM, "KẾT QUẢ", [
        (X_BAR + [("  trung bình", "t")], "38,75", False),
        ([("σ", "g"), ("²", "t"), ("x", "t"), ("  phương sai", "t")], "29,6875", False),
        ([("σ", "g"), ("x", "t")], "5,4486", True),
    ])
    cv.save(out("fx-580vn-x"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    formulas()
    fx570()
    fx580()
