"""Images for dong-tien-tu-do-la-gi, built on the DSC image design system (dsc_design.py).
Featured 1000x600, in-article images 800x500 (CMS standard). Run from repo root:
    python scripts/images/generate_dong_tien_tu_do_images.py
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (C, SS, MARGIN, CANVAS, FEATURED, FEATURED_OUT, Canvas, inline_frame, tag, hex_rgb)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "dong-tien-tu-do-la-gi"
W, H = CANVAS
R = W - MARGIN
BOTTOM = H - 58


def out(name):
    return os.path.join(OUT, f"{SLUG}-{name}.jpg")


def featured():
    cv = Canvas(FEATURED, "navy", out=FEATURED_OUT)
    cv.glow(660, 410, 260, "green", 75)
    cv.glow(790, 30, 150, "teal", 35)
    cv.paste_logo(MARGIN, 32, dark=True, height=22)

    s = "PHÂN TÍCH BCTC · DÒNG TIỀN"
    w = cv.tlen(s, "eyebrow") + 1.2 * len(s) + 26
    cv.rect(MARGIN, 96, MARGIN + w, 122, "navy_800", r=13, outline="green_900", width=1)
    cv.text(MARGIN + 13, 109, s, "eyebrow", "bright", anchor="lm", tracking=1.2)

    cv.text(MARGIN, 136, "Dòng tiền tự do", "display", "white")
    cv.text(MARGIN, 190, "là gì?", "display", "white")
    cv.gradient_text(MARGIN, 244, "Cách tính FCF 2025", "display")

    stats = [("84,5%", "VNM: FCF/LNST 2025"), ("44,9%", "FPT: FCF/LNST 2025"), ("−8.382 tỷ", "HPG: FCF năm 2025")]
    for i, (big, small) in enumerate(stats):
        x = MARGIN + i * 155
        if i:
            cv.line([(x - 14, 350), (x - 14, 392)], "navy_700", 1)
        cv.text(x, 346, big, "num_m", "white")
        cv.text(x, 378, small, "caption", "ink_3")

    # Phone mockup on the right
    px0, py0, px1, py1 = 556, 36, 744, 452
    cv.shadow(px0, py0, px1, py1, r=30, blur=20, alpha=90, dy=14)
    cv.rect(px0, py0, px1, py1, "navy_700", r=30)
    sx0, sy0, sx1, sy1 = px0 + 8, py0 + 8, px1 - 8, py1 - 8
    cv.rect(sx0, sy0, sx1, sy1, "#0F2133", r=24)
    cv.rect((px0 + px1) / 2 - 26, py0 + 16, (px0 + px1) / 2 + 26, py0 + 21, "navy_700", r=3)

    cv.text(sx0 + 14, sy0 + 40, "Mẫu B03-DN", "h2", "white")
    cv.text(sx0 + 14, sy0 + 64, "TT 200/2014/TT-BTC", "caption", "ink_3")

    rows = [
        ("Mã 20 · CFO", "+8.949 tỷ VNĐ", "bright"),
        ("Mã 21 · CapEx", "−1.762 tỷ VNĐ", "white"),
        ("FCF (VNM 2025)", "7.187 tỷ VNĐ", "bright"),
    ]
    for i, (lab, val, col) in enumerate(rows):
        y = 144 + i * 58
        cv.rect(sx0 + 12, y, sx1 - 12, y + 48, "navy_800", r=10)
        cv.text(sx0 + 22, y + 8, lab, "caption", "ink_3")
        cv.text(sx0 + 22, y + 25, val, "body_m", col)

    # Floating formula card
    fx0, fy0, fx1, fy1 = 468, 336, 706, 392
    cv.shadow(fx0, fy0, fx1, fy1, r=12, blur=14, alpha=110, dy=8)
    cv.rect(fx0, fy0, fx1, fy1, "white", r=12)
    cv.ellipse(fx0 + 12, fy0 + 14, fx0 + 40, fy0 + 42, "green")
    cv.line([(fx0 + 19, fy0 + 28), (fx0 + 24, fy0 + 33), (fx0 + 33, fy0 + 22)], "navy", 3)
    cv.text(fx0 + 50, fy0 + 12, "FCF = CFO − CapEx", "body_m", "navy")
    cv.text(fx0 + 50, fy0 + 32, "Lấy số từ mã 20 và mã 21", "caption", "ink_2")

    cv.save(out("featured"))


def formula_b03():
    cv, top = inline_frame(
        "Công thức tính FCF trên mẫu B03-DN",
        "Lấy trực tiếp từ Báo cáo lưu chuyển tiền tệ theo Thông tư 200/2014/TT-BTC",
        eyebrow="CÔNG THỨC",
        source="Thông tư 200/2014/TT-BTC (BCTC 2026 đối chiếu theo TT 99/2025)",
    )
    cards = [
        ("Mã số 20", "Lưu chuyển tiền thuần từ HĐKD (CFO)", "Tiền thật thu về từ bán hàng, cung cấp dịch vụ sau chi phí vận hành.", "Cộng (+)", "green"),
        ("Mã số 21", "Tiền chi mua sắm, xây dựng TSCĐ (CapEx)", "Trên B03-DN thường ghi âm trong ngoặc đơn, ví dụ (1.762,01).", "Trừ (−)", "navy"),
        ("FCF", "Dòng tiền tự do = Mã 20 + Mã 21", "Cộng thêm Mã số 22 (thu thanh lý TSCĐ) nếu tính FCF ròng.", "Kết quả", "green_700"),
    ]
    gap = 14
    cw = (R - MARGIN - gap * 2) / 3
    for i, (code, title, desc, tg, accent) in enumerate(cards):
        x0 = MARGIN + i * (cw + gap)
        cv.card(x0, top, x0 + cw, BOTTOM)
        chip_text_col = "navy" if accent == "green" else "white"
        cv.rect(x0 + 16, top + 18, x0 + 116, top + 50, accent, r=10)
        cv.text(x0 + 66, top + 34, code, "h2", chip_text_col, anchor="mm")
        y = cv.wrap(x0 + 16, top + 68, title, "h2", "navy", cw - 32, lh=1.25)
        cv.wrap(x0 + 16, y + 10, desc, "body", "ink_2", cw - 32, lh=1.45)
        tag(cv, x0 + 16, BOTTOM - 38, tg)

    cv.save(out("cong-thuc-b03-dn"))


def comparison_2025():
    cv, top = inline_frame(
        "FCF năm 2025 của VNM, FPT và HPG",
        "Đơn vị: tỷ VNĐ · So sánh FCF với lợi nhuận sau thuế (LNST) để thấy chất lượng tiền",
        eyebrow="BCTC KIỂM TOÁN 2025",
        source="BCTC hợp nhất kiểm toán 2025 của HPG, VNM, FPT",
    )
    rows = [
        ("VNM", "Vinamilk", "7.186,87 tỷ", "84,5% LNST", 0.85, "green", "CFO 8.948,88 · CapEx 1.762,01 · LNST 8.505,22"),
        ("FPT", "FPT Corp", "5.038,12 tỷ", "44,9% LNST", 0.59, "neutral", "CFO 10.136,04 · CapEx 5.097,92 · LNST 11.232,34"),
        ("HPG", "Hòa Phát", "−8.382,46 tỷ", "−54,0% LNST", 1.00, "navy", "CFO 17.365,86 · CapEx 25.748,32 · LNST 15.514,93"),
    ]
    ch = (BOTTOM - top - 24) / 3
    for i, (ticker, name, fcf_str, ratio_str, bar_w, col, sub) in enumerate(rows):
        y0 = top + i * (ch + 12)
        y1 = y0 + ch
        cv.card(MARGIN, y0, R, y1)
        cv.rect(MARGIN + 16, y0 + 16, MARGIN + 82, y0 + 50, col if col != "neutral" else "track", r=10)
        tcol = "navy" if col in ("green", "neutral") else "white"
        cv.text(MARGIN + 49, y0 + 33, ticker, "h2", tcol, anchor="mm")
        cv.text(MARGIN + 98, y0 + 18, name, "h2", "navy")
        cv.text(MARGIN + 98, y0 + 42, sub, "caption", "ink_3")

        cv.text(R - 16, y0 + 18, fcf_str, "num_m", "green_700" if col == "green" else "navy", anchor="ra")
        cv.text(R - 16, y0 + 42, ratio_str, "caption", "ink_2", anchor="ra")

        bx0, bx1 = MARGIN + 16, R - 16
        by0, by1 = y1 - 24, y1 - 12
        cv.rect(bx0, by0, bx1, by1, "track", r=6)
        cv.rect(bx0, by0, bx0 + (bx1 - bx0) * bar_w, by1, col, r=6)

    cv.save(out("vi-du-2025"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    featured()
    formula_b03()
    comparison_2025()
    print("Generated 3 images in", OUT)
