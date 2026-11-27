"""Replacements for blurry / low-res Google Docs images on live articles (audit 2026-11-27).
One function per image; output knowledge/3-seo/content/images/<slug>-<topic>.jpg (800x500).
Run from repo root:
    python scripts/images/generate_gdocs_replacements.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import MARGIN, CANVAS, SS, C, inline_frame, tag  # noqa: E402
from generate_do_lech_chuan_images import draw_run, fraction, greek, run_width  # noqa: E402

OUT = "knowledge/3-seo/content/images"
W, H = CANVAS
R = W - MARGIN
BOTTOM = H - 58


def out(slug, name):
    return os.path.join(OUT, f"{slug}-{name}.jpg")


def candle(cv, x, o, c, hi, lo, w=22, up="green", down="navy", hollow=False):
    """Draw one candle centred at x; o/c/hi/lo are y pixels (smaller = higher price)."""
    col = up if c <= o else down
    cv.line([(x, hi), (x, lo)], "navy", 2)
    top, bot = min(o, c), max(o, c)
    if bot - top < 3:
        cv.rect(x - w / 2, top - 1.5, x + w / 2, top + 1.5, "navy")
        return
    if hollow:
        cv.rect(x - w / 2, top, x + w / 2, bot, "white", outline="navy", width=2)
    else:
        cv.rect(x - w / 2, top, x + w / 2, bot, col, r=2)


def arrow(cv, pts, color="green", width=3):
    cv.line(pts, color, width)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    L = 11
    p1 = (x1 - L * math.cos(a - 0.45), y1 - L * math.sin(a - 0.45))
    p2 = (x1 - L * math.cos(a + 0.45), y1 - L * math.sin(a + 0.45))
    cv.d.polygon([(x1 * SS, y1 * SS), (p1[0] * SS, p1[1] * SS), (p2[0] * SS, p2[1] * SS)], fill=C[color])


def label_line(cv, x0, y, x1, text, right=True, color="ink_2"):
    """Thin leader line from candle edge to a label."""
    cv.line([(x0, y), (x1, y)], "neutral", 1)
    cv.text(x1 + (6 if right else -6), y, text, "caption", color, anchor="lm" if right else "rm")


def pill(cv, x0, y0, x1, y1, text, fill="mint_100", color="green_700", token="caption"):
    cv.rect(x0, y0, x1, y1, fill, r=8)
    lines = text.split("\n")
    lh = 15
    cy = (y0 + y1) / 2 - (len(lines) - 1) * lh / 2
    for i, ln in enumerate(lines):
        cv.text((x0 + x1) / 2, cy + i * lh, ln, token, color, anchor="mm")


# ---- rui-ro-tin-dung-la-gi ------------------------------------------------------------
def rui_ro_phan_loai():
    slug = "rui-ro-tin-dung-la-gi"
    cv, top = inline_frame("Phân loại rủi ro tín dụng",
                           "Theo nguyên nhân phát sinh và theo khả năng trả nợ của khách hàng",
                           eyebrow="Rủi ro tín dụng")
    split = 520
    # left: by cause
    cv.card(MARGIN, top, split, BOTTOM)
    tag(cv, MARGIN + 18, top + 16, "Theo nguyên nhân phát sinh")
    groups = [("Rủi ro\ngiao dịch", ["Rủi ro lựa chọn", "Rủi ro bảo đảm", "Rủi ro nghiệp vụ"]),
              ("Rủi ro\ntác nghiệp", []),
              ("Rủi ro\ndanh mục", ["Rủi ro nội tại", "Rủi ro tập trung"])]
    gw = (split - MARGIN - 36 - 2 * 10) / 3
    for i, (head, subs) in enumerate(groups):
        x0 = MARGIN + 18 + i * (gw + 10)
        pill(cv, x0, top + 56, x0 + gw, top + 100, head, fill="navy", color="white", token="body_m")
        for j, s in enumerate(subs):
            y = top + 120 + j * 46
            cv.line([(x0 + gw / 2, y - 20 + (0 if j else 0)), (x0 + gw / 2, y)], "neutral", 1)
            pill(cv, x0 + 6, y, x0 + gw - 6, y + 34, s)
    # right: by repayment ability
    x0 = split + 16
    cv.card(x0, top, R, BOTTOM)
    tag(cv, x0 + 18, top + 16, "Theo khả năng trả nợ")
    items = ["Rủi ro đọng vốn", "Rủi ro mất khả năng\nchi trả", "Rủi ro không giới hạn ở\nhoạt động cho vay"]
    for j, s in enumerate(items):
        y = top + 56 + j * 76
        pill(cv, x0 + 18, y, R - 18, y + 60, s, fill="mint_100", color="green_700", token="body_m")
    cv.save(out(slug, "phan-loai"))


def rui_ro_camels():
    slug = "rui-ro-tin-dung-la-gi"
    cv, top = inline_frame("Tiêu chí xếp hạng CAMELS với tổ chức tín dụng",
                           "6 nhóm tiêu chí, kết quả xếp từ hạng A (tốt) đến hạng E (yếu kém)",
                           eyebrow="Xếp hạng")
    split = 520
    crit = [("C", "Vốn", "Capital"), ("A", "Chất lượng tài sản", "Asset Quality"),
            ("M", "Quản trị điều hành", "Management"), ("E", "Kết quả kinh doanh", "Earnings"),
            ("L", "Khả năng thanh khoản", "Liquidity"), ("S", "Độ nhạy rủi ro thị trường", "Sensitivity")]
    cw = (split - MARGIN - 10) / 2
    ch = (BOTTOM - top - 2 * 10) / 3
    for i, (letter, vi, en) in enumerate(crit):
        x0 = MARGIN + (i % 2) * (cw + 10)
        y0 = top + (i // 2) * (ch + 10)
        cv.card(x0, y0, x0 + cw, y0 + ch)
        cv.rect(x0 + 14, y0 + ch / 2 - 18, x0 + 50, y0 + ch / 2 + 18, "green", r=10)
        cv.text(x0 + 32, y0 + ch / 2, letter, "num_m", "navy", anchor="mm")
        cv.text(x0 + 62, y0 + ch / 2 - 9, vi, "body_m", "navy", anchor="lm")
        cv.text(x0 + 62, y0 + ch / 2 + 11, en, "caption", "ink_3", anchor="lm")
    # right: rating ladder
    x0 = split + 16
    cv.card(x0, top, R, BOTTOM)
    cv.text(x0 + 18, top + 22, "Kết quả xếp hạng", "h2", "navy", anchor="lm")
    ranks = [("A", "Tốt", 1.0), ("B", "Khá", 0.8), ("C", "Trung bình", 0.6), ("D", "Yếu", 0.4), ("E", "Yếu kém", 0.2)]
    bw = R - 18 - (x0 + 52)
    for j, (r_, lab, f) in enumerate(ranks):
        y = top + 50 + j * 50
        cv.text(x0 + 30, y + 16, r_, "num_m", "navy", anchor="mm")
        cv.rect(x0 + 52, y + 22, x0 + 52 + bw, y + 32, "track", r=5)
        cv.rect(x0 + 52, y + 22, x0 + 52 + bw * f, y + 32, "green" if j < 2 else ("neutral" if j == 2 else "navy"), r=5)
        cv.text(x0 + 52, y + 8, lab, "caption", "ink_2", anchor="lm")
    cv.save(out(slug, "camels"))


# ---- chi-bao-atr-la-gi ----------------------------------------------------------------------
def atr_true_range():
    slug = "chi-bao-atr-la-gi"
    cv, top = inline_frame("3 trường hợp xác định True Range (TR)",
                           "TR là giá trị lớn nhất trong 3 cách tính. Nến trước tô đậm, nến hiện tại để rỗng",
                           eyebrow="Chỉ báo ATR")
    gap = 12
    cw = (R - MARGIN - 2 * gap) / 3
    cases = [
        ("A", "Mở gap tăng", "TR = |Cao hiện tại − Đóng trước|",
         dict(prev=(250, 290, 225, 320), cur=(180, 168, 150, 190), top_y=150, bot_y=290)),
        ("B", "Mở gap giảm", "TR = |Thấp hiện tại − Đóng trước|",
         dict(prev=(170, 205, 150, 235), cur=(275, 288, 262, 300), top_y=205, bot_y=300)),
        ("C", "Biên độ hiện tại nhỏ", "TR = |Cao hiện tại − Đóng trước|",
         dict(prev=(200, 240, 180, 270), cur=(222, 212, 196, 232), top_y=196, bot_y=240)),
    ]
    for i, (letter, head, formula, g) in enumerate(cases):
        x0 = MARGIN + i * (cw + gap)
        x1 = x0 + cw
        cv.card(x0, top, x1, BOTTOM)
        tag(cv, x0 + 16, top + 14, f"Ví dụ {letter}")
        cv.text(x0 + 16, top + 54, head, "h2", "navy", anchor="lm")
        ox = top + 84 - 150  # case coords start at y=150 -> place below the card heading
        px, cx = x0 + cw * 0.32, x0 + cw * 0.60
        o, c_, hi, lo = (v + ox for v in g["prev"])
        candle(cv, px, o, c_, hi, lo, w=20, down="navy")
        o2, c2, hi2, lo2 = (v + ox for v in g["cur"])
        candle(cv, cx, o2, c2, hi2, lo2, w=20, hollow=True)
        # TR bracket in lime
        bx = x0 + cw * 0.82
        ty, by = g["top_y"] + ox, g["bot_y"] + ox
        cv.line([(bx - 6, ty), (bx, ty), (bx, by), (bx - 6, by)], "green", 3)
        cv.text(bx + 8, (ty + by) / 2, "TR", "body_m", "green_700", anchor="lm")
        cv.line([(px + 12, by if letter != "B" else ty), (bx - 6, by if letter != "B" else ty)], "neutral", 1)
        cv.wrap(x0 + 16, BOTTOM - 46, formula, "caption", "ink_2", cw - 32)
    cv.save(out(slug, "true-range"))


# ---- mo-hinh-nen-hammer-la-gi --------------------------------------------------------------
def hammer_cau_tao():
    slug = "mo-hinh-nen-hammer-la-gi"
    cv, top = inline_frame("Cấu tạo nến Hammer",
                           "Thân nhỏ nằm sát giá cao nhất, bóng dưới dài ít nhất gấp 2 lần thân",
                           eyebrow="Mô hình nến")
    gap = 16
    cw = (R - MARGIN - gap) / 2
    variants = [("Hammer tăng giá", "Đóng cửa > mở cửa", "green", ("Đóng cửa", "Mở cửa")),
                ("Hammer giảm giá", "Đóng cửa < mở cửa, chờ phiên sau xác nhận", "navy", ("Mở cửa", "Đóng cửa"))]
    for i, (head, sub, col, (lab_top, lab_bot)) in enumerate(variants):
        x0 = MARGIN + i * (cw + gap)
        cv.card(x0, top, x0 + cw, BOTTOM)
        cv.text(x0 + 20, top + 22, head, "h2", "navy", anchor="lm")
        cv.text(x0 + 20, top + 44, sub, "caption", "ink_3", anchor="lm")
        cx = x0 + cw * 0.38
        hi, btop, bbot, lo = top + 84, top + 92, top + 132, top + 262
        cv.line([(cx, hi), (cx, lo)], "navy", 3)
        cv.rect(cx - 22, btop, cx + 22, bbot, col, r=3)
        # high sits just above the body: elbow its leader up so labels don't collide
        cv.line([(cx + 4, hi), (cx + 34, hi - 14), (cx + 60, hi - 14)], "neutral", 1)
        cv.text(cx + 66, hi - 14, "Giá cao nhất", "caption", "ink_2", anchor="lm")
        label_line(cv, cx + 24, btop + 4, cx + 60, lab_top)
        label_line(cv, cx + 24, bbot - 4, cx + 60, lab_bot)
        label_line(cv, cx + 4, lo, cx + 60, "Giá thấp nhất")
        # shadow length bracket
        bx = cx - 40
        cv.line([(bx + 6, bbot), (bx, bbot), (bx, lo), (bx + 6, lo)], "green", 2)
        cv.text(bx - 8, (bbot + lo) / 2 - 8, "Bóng dưới", "caption", "green_700", anchor="rm")
        cv.text(bx - 8, (bbot + lo) / 2 + 8, "≥ 2 lần thân", "caption", "green_700", anchor="rm")
    cv.save(out(slug, "cau-tao"))


# ---- mau-hinh-nen-bao-trum-la-gi -----------------------------------------------------------
def bao_trum():
    slug = "mau-hinh-nen-bao-trum-la-gi"
    cv, top = inline_frame("Mẫu hình nến bao trùm tăng và giảm",
                           "Thân nến thứ hai bao trọn thân nến trước, báo hiệu khả năng đảo chiều",
                           eyebrow="Mô hình nến")
    gap = 16
    cw = (R - MARGIN - gap) / 2
    # (o, c, hi, lo) relative y in 0..1 of the chart band
    bull = [(0.10, 0.28, 0.06, 0.32), (0.30, 0.48, 0.25, 0.53), (0.52, 0.66, 0.48, 0.72), (0.66, 0.74, 0.62, 0.80),
            (0.80, 0.50, 0.85, 0.46)]
    bear = [(0.90, 0.72, 0.94, 0.68), (0.70, 0.52, 0.75, 0.47), (0.48, 0.34, 0.52, 0.28), (0.34, 0.26, 0.38, 0.20),
            (0.20, 0.50, 0.15, 0.54)]
    panels = [("Bao trùm tăng (Bullish Engulfing)", "Xuất hiện cuối xu hướng giảm", bull, "up"),
              ("Bao trùm giảm (Bearish Engulfing)", "Xuất hiện cuối xu hướng tăng", bear, "down")]
    for i, (head, sub, cs, d) in enumerate(panels):
        x0 = MARGIN + i * (cw + gap)
        cv.card(x0, top, x0 + cw, BOTTOM)
        cv.text(x0 + 20, top + 22, head, "h2", "navy", anchor="lm")
        cv.text(x0 + 20, top + 44, sub, "caption", "ink_3", anchor="lm")
        y0, y1 = top + 70, BOTTOM - 30
        band = y1 - y0
        for k, (o, c_, hi, lo) in enumerate(cs):
            x = x0 + 40 + k * 46
            last = k == len(cs) - 1
            candle(cv, x, y0 + o * band, y0 + c_ * band, y0 + min(hi, lo) * band, y0 + max(hi, lo) * band,
                   w=30 if last else 20)
        # highlight the two-candle pattern
        hx0, hx1 = x0 + 40 + 3 * 46 - 18, x0 + 40 + 4 * 46 + 22
        cv.rect(hx0, y0 - 6, hx1, y1 + 4, None, r=10, outline="green", width=2)
        ax = x0 + cw - 50
        if d == "up":
            arrow(cv, [(ax - 20, y0 + band * 0.55), (ax + 14, y0 + band * 0.12)])
        else:
            arrow(cv, [(ax - 20, y0 + band * 0.45), (ax + 14, y0 + band * 0.88)], color="navy")
    cv.save(out(slug, "tang-giam"))


# ---- nen-doji-la-gi ---------------------------------------------------------------------------
def doji_4_loai():
    slug = "nen-doji-la-gi"
    cv, top = inline_frame("4 loại nến Doji phổ biến",
                           "Vạch xanh: giá mở cửa = giá đóng cửa. Các loại khác nhau ở độ dài bóng nến trên và dưới",
                           eyebrow="Mô hình nến")
    gap = 10
    cw = (R - MARGIN - 3 * gap) / 4
    # (high, body, low) as fractions of the drawing band
    types = [("Doji thông thường", "Common Doji", 0.25, 0.45, 0.65),
             ("Doji chân dài", "Long legged Doji", 0.02, 0.45, 0.90),
             ("Doji bia mộ", "Gravestone Doji", 0.02, 0.86, 0.86),
             ("Doji chuồn chuồn", "Dragonfly Doji", 0.06, 0.06, 0.90)]
    for i, (vi, en, hi, body, lo) in enumerate(types):
        x0 = MARGIN + i * (cw + gap)
        cv.card(x0, top, x0 + cw, BOTTOM)
        cv.text(x0 + cw / 2, top + 22, vi, "body_m", "navy", anchor="mm")
        cv.text(x0 + cw / 2, top + 42, en, "caption", "ink_3", anchor="mm")
        y0, y1 = top + 70, BOTTOM - 46
        band = y1 - y0
        cx = x0 + cw / 2
        cv.line([(cx, y0 + hi * band), (cx, y0 + lo * band)], "navy", 3)
        by = y0 + body * band
        # body bar only; the open = close legend lives in the subtitle (a side label overflowed the 172px card)
        cv.rect(cx - 24, by - 2, cx + 24, by + 2, "green", r=1)
    # one shared footnote line inside cards
    for i in range(4):
        x0 = MARGIN + i * (cw + gap)
        cv.line([(x0 + 14, BOTTOM - 34), (x0 + cw - 14, BOTTOM - 34)], "line", 1)
    notes = ["2 bóng ngắn", "2 bóng rất dài", "Chỉ có bóng trên", "Chỉ có bóng dưới"]
    for i, n in enumerate(notes):
        x0 = MARGIN + i * (cw + gap)
        cv.text(x0 + cw / 2, BOTTOM - 17, n, "caption", "ink_2", anchor="mm")
    cv.save(out(slug, "4-loai"))


# ---- npv-va-irr-la-gi --------------------------------------------------------------------------
def sigma_block(cv, x, y_bar, size, top_lim, bot_lim, color="navy"):
    """Big Σ with limits, vertically centred on the fraction bar. Returns end x."""
    f = greek(int(size * 1.5))
    sw = cv.d.textlength("Σ", font=f) / SS
    cv.d.text((x * SS, (y_bar + size * 0.55) * SS), "Σ", font=f, fill=C[color], anchor="ls")
    cv.track(cv.d.textbbox((x * SS, (y_bar + size * 0.55) * SS), "Σ", font=f, anchor="ls"), "Σ")
    lim = [(top_lim, "t")]
    tw = run_width(cv, lim, int(size * 0.55))
    draw_run(cv, x + (sw - tw) / 2, y_bar - size * 0.95, lim, int(size * 0.55), color)
    bw = run_width(cv, [(bot_lim, "t")], int(size * 0.55))
    draw_run(cv, x + (sw - bw) / 2, y_bar + size * 1.25, [(bot_lim, "t")], int(size * 0.55), color)
    return x + sw + 4


def npv_irr_formula():
    slug = "npv-va-irr-la-gi"
    cv, top = inline_frame("Công thức tính NPV và IRR",
                           "IRR là tỷ lệ chiết khấu khiến NPV của dự án bằng 0",
                           eyebrow="Thẩm định dự án")
    gap = 16
    cw = (R - MARGIN - gap) / 2
    size = 24
    CT = [("C", "t"), ("t", "sub")]
    for i, (head, rate, rhs) in enumerate([("NPV", [("r", "t")], None), ("IRR", [("IRR", "t")], "= 0")]):
        x0 = MARGIN + i * (cw + gap)
        cv.card(x0, top, x0 + cw, BOTTOM)
        tag(cv, x0 + 20, top + 18, "Giá trị hiện tại thuần" if i == 0 else "Tỷ suất hoàn vốn nội bộ")
        yb = top + 120
        x = x0 + 22
        if i == 0:
            x = draw_run(cv, x, yb + size * 0.35, [("NPV = ", "t")], size) + 2
        x = sigma_block(cv, x, yb, size, "n", "t=1")
        den = [("(1 + ", "t")] + rate + [(")", "t"), ("t", "sup")]
        x = fraction(cv, x, yb, CT, den, size) + 6
        x = draw_run(cv, x, yb + size * 0.35, [("− C", "t"), ("0", "sub")], size)
        if rhs:
            draw_run(cv, x + 4, yb + size * 0.35, [(" " + rhs, "t")], size, "green_700")
        cv.line([(x0 + 20, BOTTOM - 70), (x0 + cw - 20, BOTTOM - 70)], "line", 1)
        leg = [CT + [(": dòng tiền ròng năm t · ", "t")] + ([("r", "t")] if i == 0 else [("IRR", "t")]) +
               [(": tỷ lệ chiết khấu", "t")],
               [("C", "t"), ("0", "sub"), (": vốn đầu tư ban đầu · n: số năm", "t")]]
        for k, run in enumerate(leg):
            draw_run(cv, x0 + 20, BOTTOM - 46 + k * 22, run, 13, "ink_2", weight="Medium")
    cv.save(out(slug, "cong-thuc"))


# ---- tai-sao-nen-dau-tu-trai-phieu-... (replaces an HSC-branded diagram) ----------------
def chu_ky_dau_tu():
    import math
    slug = "tai-sao-nen-dau-tu-trai-phieu-trai-phieu-phu-hop-voi-nha-dau-tu-nao"
    cv, top = inline_frame("Chu kỳ đầu tư chứng khoán dài hạn",
                           "Luân chuyển giữa cổ phiếu và trái phiếu theo nhịp thị trường",
                           eyebrow="Ví dụ minh họa")
    cv.card(MARGIN, top, R, BOTTOM)
    x0, x1 = MARGIN + 30, R - 30
    mid, amp = top + 150, 60

    def curve(t):  # troughs at t=0.2 / 0.8, peak at t=0.5
        return x0 + t * (x1 - x0), mid + amp * math.cos(2 * math.pi * (t - 0.2) / 0.6)
    cv.line([curve(k / 120) for k in range(121)], "navy", 3)
    lo1, hi_, lo2 = curve(0.2), curve(0.5), curve(0.8)
    for (x, y), kind in ((lo1, "low"), (hi_, "high"), (lo2, "low")):
        cv.ellipse(x - 6, y - 6, x + 6, y + 6, "green" if kind == "low" else "navy")
        if kind == "low":
            pill(cv, x - 96, y + 16, x + 96, y + 58, "Thị trường giảm mạnh\nMua cổ phiếu · Bán trái phiếu")
        else:
            pill(cv, x - 96, y - 66, x + 96, y - 24, "Thị trường tăng mạnh\nBán cổ phiếu · Mua trái phiếu",
                 fill="navy", color="white")
    yb = BOTTOM - 32
    for xa, xb in ((lo1[0], hi_[0]), (hi_[0], lo2[0])):
        cv.line([(xa + 4, yb), (xb - 4, yb)], "neutral", 1)
        cv.text((xa + xb) / 2, yb + 13, "Nhiều quý đến nhiều năm", "caption", "ink_3", anchor="mm")
    for x in (lo1[0], hi_[0], lo2[0]):
        cv.line([(x, yb - 6), (x, yb + 6)], "neutral", 1)
    cv.save(out(slug, "chu-ky-dau-tu"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rui_ro_phan_loai()
    rui_ro_camels()
    atr_true_range()
    hammer_cau_tao()
    bao_trum()
    doji_4_loai()
    npv_irr_formula()
    chu_ky_dau_tu()
