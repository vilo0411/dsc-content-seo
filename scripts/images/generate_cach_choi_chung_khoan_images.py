"""Images for cach-choi-chung-khoan, built on the DSC image design system (dsc_design.py).
Featured 1000x600, in-article images 800x500 (CMS standard). Run from repo root:
    python scripts/images/generate_cach_choi_chung_khoan_images.py
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (C, SS, MARGIN, CANVAS, FEATURED, FEATURED_OUT, Canvas, inline_frame, tag, hex_rgb)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "cach-choi-chung-khoan"
W, H = CANVAS
R = W - MARGIN          # right edge of content
BOTTOM = H - 58         # bottom of content area (footer line sits at H-42)


def out(name):
    return os.path.join(OUT, f"{SLUG}-{name}.jpg")


def area_fill(cv, pts, bottom, c="bright", a0=150):
    """Gradient area under a polyline, fading to transparent."""
    Wp, Hp = cv.img.size
    m = Image.new("L", (Wp, Hp), 0)
    poly = [(x * SS, y * SS) for x, y in pts] + [(pts[-1][0] * SS, bottom * SS), (pts[0][0] * SS, bottom * SS)]
    ImageDraw.Draw(m).polygon(poly, fill=255)
    top = min(y for _, y in pts)
    grad = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    rgb = hex_rgb(C[c])[:3]
    for yy in range(int(top * SS), int(bottom * SS)):
        t = (yy - top * SS) / max(1, (bottom - top) * SS)
        gd.line([(0, yy), (Wp, yy)], fill=rgb + (int(a0 * (1 - t)),))
    layer = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    layer.paste(grad, (0, 0), m)
    cv.img.alpha_composite(layer)
    cv.d = ImageDraw.Draw(cv.img)


def featured():
    cv = Canvas(FEATURED, "navy", out=FEATURED_OUT)
    cv.glow(660, 410, 260, "green", 75)
    cv.glow(790, 30, 150, "teal", 35)
    cv.paste_logo(MARGIN, 32, dark=True, height=22)

    s = "HƯỚNG DẪN CHO NGƯỜI MỚI"
    w = cv.tlen(s, "eyebrow") + 1.2 * len(s) + 26
    cv.rect(MARGIN, 96, MARGIN + w, 122, "navy_800", r=13, outline="green_900", width=1)
    cv.text(MARGIN + 13, 109, s, "eyebrow", "bright", anchor="lm", tracking=1.2)

    cv.text(MARGIN, 136, "Cách chơi", "display", "white")
    cv.text(MARGIN, 190, "chứng khoán", "display", "white")
    cv.gradient_text(MARGIN, 244, "cho người mới", "display")

    stats = [("5 bước", "đến lệnh bán đầu tiên"), ("0,3%", "phí mỗi lần mua bán"), ("T+2", "cổ phiếu về tài khoản")]
    for i, (big, small) in enumerate(stats):
        x = MARGIN + i * 150
        if i:
            cv.line([(x - 16, 350), (x - 16, 392)], "navy_700", 1)
        cv.text(x, 346, big, "num_m", "white")
        cv.text(x, 378, small, "caption", "ink_3")

    # phone
    px0, py0, px1, py1 = 560, 36, 740, 452
    cv.shadow(px0, py0, px1, py1, r=30, blur=20, alpha=90, dy=14)
    cv.rect(px0, py0, px1, py1, "navy_700", r=30)
    sx0, sy0, sx1, sy1 = px0 + 8, py0 + 8, px1 - 8, py1 - 8
    cv.rect(sx0, sy0, sx1, sy1, "#0F2133", r=24)
    cv.rect((px0 + px1) / 2 - 26, py0 + 16, (px0 + px1) / 2 + 26, py0 + 21, "navy_700", r=3)
    cv.text(sx0 + 14, sy0 + 40, "HPG", "h2", "white")
    cv.text(sx0 + 14, sy0 + 64, "HOSE · Cổ phiếu", "caption", "ink_3")
    cv.text(sx1 - 14, sy0 + 40, "20.900", "h2", "bright", anchor="ra")
    pts = [(sx0 + 12, 232), (sx0 + 34, 224), (sx0 + 54, 229), (sx0 + 76, 208), (sx0 + 96, 214),
           (sx0 + 118, 188), (sx0 + 136, 194), (sx1 - 12, 158)]
    area_fill(cv, pts, 268)
    cv.line(pts, "bright", 2)
    cv.ellipse(pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4, "bright")
    for i, (lab, val) in enumerate([("Giá", "20.900"), ("KL", "100")]):
        y = 284 + i * 38
        cv.rect(sx0 + 12, y, sx1 - 12, y + 30, "navy_800", r=8)
        cv.text(sx0 + 24, y + 15, lab, "caption", "ink_3", anchor="lm")
        cv.text(sx1 - 24, y + 15, val, "caption", "white", anchor="rm")
    mid = (sx0 + sx1) / 2
    cv.rect(sx0 + 12, 370, mid - 4, 404, "green", r=10)
    cv.text((sx0 + 12 + mid - 4) / 2, 387, "Mua", "body_m", "white", anchor="mm")
    cv.rect(mid + 4, 370, sx1 - 12, 404, "navy_700", r=10)
    cv.text((mid + 4 + sx1 - 12) / 2, 387, "Bán", "body_m", "ink_3", anchor="mm")

    # floating confirmation card
    fx0, fy0, fx1, fy1 = 452, 226, 652, 278
    cv.shadow(fx0, fy0, fx1, fy1, r=12, blur=14, alpha=110, dy=8)
    cv.rect(fx0, fy0, fx1, fy1, "white", r=12)
    cv.ellipse(fx0 + 12, fy0 + 12, fx0 + 40, fy0 + 40, "green")
    cv.line([(fx0 + 19, fy0 + 26), (fx0 + 24, fy0 + 31), (fx0 + 33, fy0 + 20)], "white", 3)
    cv.text(fx0 + 50, fy0 + 12, "Lệnh đã khớp", "body_m", "navy")
    cv.text(fx0 + 50, fy0 + 31, "Mua 100 HPG · 20.900", "caption", "ink_2")
    cv.save(out("featured"))


def steps():
    cv, top = inline_frame("5 bước chơi chứng khoán cho người mới",
                           "Từ mở tài khoản đến lệnh bán đầu tiên, nhanh nhất 3 ngày làm việc",
                           eyebrow="Hướng dẫn", source="Áp dụng tại mọi công ty chứng khoán")
    rows = [("Mở tài khoản eKYC", "CCCD gắn chip, số điện thoại, tài khoản ngân hàng chính chủ", "Online"),
            ("Nạp tiền", "Chuyển khoản tới số tài khoản định danh", "Chính chủ"),
            ("Chọn cổ phiếu hoặc ETF", "Thanh khoản cao, lãi đều 3 năm, P/E hợp lý", "VN30"),
            ("Đặt lệnh mua LO", "Trong giờ giao dịch, bội số 100 cổ phiếu", "Lệnh giới hạn"),
            ("Theo dõi và bán", "Đặt trước giá chốt lời và giá cắt lỗ", "T+2")]
    gap = 10
    cw = (R - MARGIN - gap * 4) / 5
    for i, (t, sub, tg) in enumerate(rows):
        x0 = MARGIN + i * (cw + gap)
        cv.card(x0, top, x0 + cw, BOTTOM)
        cv.rect(x0 + 12, top + 14, x0 + 44, top + 46, "green" if i < 4 else "navy", r=10)
        cv.text(x0 + 28, top + 30, str(i + 1), "num_m", "white", anchor="mm")
        y = cv.wrap(x0 + 12, top + 60, t, "h2", "navy", cw - 22, lh=1.25)
        cv.wrap(x0 + 12, y + 6, sub, "body", "ink_2", cw - 22, lh=1.4)
        tag(cv, x0 + 12, BOTTOM - 34, tg)
    cv.save(out("5-buoc"))


def cost():
    cv, top = inline_frame("Chi phí một lần mua bán cổ phiếu",
                           "Lệnh 10 triệu VNĐ: phí DSC từ 0,1% mỗi chiều, thuế 0,1% khi bán",
                           eyebrow="Chi phí giao dịch", source="Thuế: Điều 54 NĐ 253/2026/NĐ-CP · Phí: biểu phí DSC 11/2026")
    # left: one round trip
    lx0, lx1 = MARGIN, 392
    cv.card(lx0, top, lx1, BOTTOM)
    cv.text(lx0 + 20, top + 16, "Tổng chi phí một lần mua và bán", "caption", "ink_3")
    cv.text(lx0 + 20, top + 32, "30.000 VNĐ", "num_xl", "navy")
    by = top + 100
    seg = (lx1 - lx0 - 40 - 8) / 3
    parts = [("Phí mua 0,1%", "green"), ("Phí bán 0,1%", "green_700"), ("Thuế bán 0,1%", "navy")]
    for i, (lab, col) in enumerate(parts):
        x = lx0 + 20 + i * (seg + 4)
        cv.rect(x, by, x + seg, by + 12, col, r=6)
        ry = by + 30 + i * 24
        cv.ellipse(lx0 + 20, ry - 4, lx0 + 28, ry + 4, col)
        cv.text(lx0 + 36, ry, lab, "body", "ink_2", anchor="lm")
        cv.text(lx1 - 20, ry, "10.000 VNĐ", "body_m", "navy", anchor="rm")
    cv.line([(lx0 + 20, BOTTOM - 46), (lx1 - 20, BOTTOM - 46)], "line", 1)
    cv.text(lx0 + 20, BOTTOM - 23, "Hòa vốn khi giá tăng", "body_m", "ink_2", anchor="lm")
    cv.text(lx1 - 20, BOTTOM - 23, "≥ 0,3%", "num_m", "green_700", anchor="rm")

    # right: yearly cost by strategy
    rx0, rx1 = 408, R
    cv.card(rx0, top, rx1, BOTTOM)
    cv.text(rx0 + 20, top + 16, "Chi phí mỗi năm, vốn 10 triệu VNĐ", "h2", "navy")
    bars = [("Tích lũy định kỳ", 8, "0,1% · 10.000 đ", "green"),
            ("Nắm giữ dài hạn", 14, "0,3% · 30.000 đ", "green"),
            ("Lướt sóng 5 lần/tháng", None, "18% · 1,8 triệu đ", "navy")]
    for i, (lab, v, s, col) in enumerate(bars):
        y = top + 62 + i * 60
        cv.text(rx0 + 20, y, lab, "body_m", "navy", anchor="lm")
        cv.text(rx1 - 20, y, s, "body_m", "navy" if col == "navy" else "green_700", anchor="rm")
        cv.rect(rx0 + 20, y + 14, rx1 - 20, y + 26, "track", r=6)
        cv.rect(rx0 + 20, y + 14, rx1 - 20 if v is None else rx0 + 20 + v, y + 26, col, r=6)
    cv.save(out("chi-phi-hoa-von"))


def margin():
    cv, top = inline_frame("Vay margin 1:1 khuếch đại cả lãi lẫn lỗ",
                           "Vốn 50 triệu VNĐ, vay thêm 50 triệu với lãi 13,5%/năm, giữ 3 tháng",
                           eyebrow="Rủi ro margin", source="Chưa tính phí, thuế và rủi ro bị bán giải chấp")
    mid = W / 2
    scale = 3.3  # px per %
    panels = [
        (MARGIN, mid - 8, "Cổ phiếu tăng 20%", +1, [("Không vay", 20, "còn 60 triệu", "neutral"),
                                                  ("Vay 1:1", 37, "còn 68,31 triệu", "green")]),
        (mid + 8, R, "Cổ phiếu giảm 20%", -1, [("Không vay", 20, "còn 40 triệu", "neutral"),
                                               ("Vay 1:1", 43, "còn 28,31 triệu", "navy")]),
    ]
    for x0, x1, head, sign, bars in panels:
        cv.card(x0, top, x1, BOTTOM)
        cv.text(x0 + 18, top + 16, head, "h2", "navy")
        cx = (x0 + x1) / 2
        base = BOTTOM - 30 if sign > 0 else top + 66
        cv.line([(x0 + 18, base), (x1 - 18, base)], "line", 1)
        for i, (lab, v, note, col) in enumerate(bars):
            bc = cx + (-62 if i == 0 else 62)
            hgt = v * scale
            if sign > 0:
                cv.rect(bc - 40, base - hgt, bc + 40, base, col, r=6)
                cv.text(bc, base - hgt - 22, f"+{v}%", "num_l", "navy" if col == "neutral" else "green_700", anchor="ms")
                cv.text(bc, base - hgt - 7, note, "caption", "ink_3", anchor="ms")
                cv.text(bc, base + 18, lab, "body_m", "ink_2", anchor="ms")
            else:
                cv.rect(bc - 40, base, bc + 40, base + hgt, col, r=6)
                cv.text(bc, base - 8, lab, "body_m", "ink_2", anchor="ms")
                cv.text(bc, base + hgt + 27, f"−{v}%", "num_l", "navy", anchor="ms")
                cv.text(bc, base + hgt + 43, note, "caption", "ink_3", anchor="ms")
    cv.save(out("margin-2-chieu"))


def order_screen():
    """Real DSC Trading order screen (portrait) composed into the 800x500 frame."""
    cv, top = inline_frame("Đặt lệnh mua LO trên app", "Ví dụ màn hình đặt lệnh trên App DSC Trading",
                           eyebrow="Bước 4", source="Ảnh chụp App DSC Trading")
    shot = Image.open("knowledge/1-brand/assets/screens/dsc-trading-dat-lenh.jpg").convert("RGBA")
    cy0, cy1 = 230, 1340                       # crop: stock header -> volume field
    shot = shot.crop((0, cy0, shot.width, cy1))
    sh = BOTTOM - top
    sc = sh / shot.height
    sw = shot.width * sc
    x0 = R - sw - 20
    cv.shadow(x0 - 10, top - 4, x0 + sw + 10, BOTTOM + 4, r=16)
    cv.rect(x0 - 10, top - 4, x0 + sw + 10, BOTTOM + 4, "white", r=16, outline="line")
    img = shot.resize((int(sw * SS), int(sh * SS)), Image.Resampling.LANCZOS)
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=10 * SS, fill=255)
    cv.img.paste(img, (int(x0 * SS), int(top * SS)), m)
    cv.d = ImageDraw.Draw(cv.img)

    steps = [("Chọn mã cổ phiếu", "Gõ mã, ví dụ HPG, rồi kiểm tra sàn và giá tham chiếu", 300),
             ("Nhập giá", "Trong biên độ ±7% so với giá tham chiếu (HOSE)", 1163),
             ("Nhập khối lượng", "Bội số của 100 cổ phiếu, ví dụ 100", 1280),
             ("Chọn Lệnh mua và xác nhận", "Xác nhận OTP, rồi kiểm tra trạng thái trong sổ lệnh", 865)]
    for i, (t, sub, oy) in enumerate(steps):
        y = top + 8 + i * 72
        cv.rect(MARGIN, y, MARGIN + 28, y + 28, "green", r=8)
        cv.text(MARGIN + 14, y + 14, str(i + 1), "body_m", "white", anchor="mm")
        cv.text(MARGIN + 42, y + 3, t, "h2", "navy")
        cv.wrap(MARGIN + 42, y + 28, sub, "body", "ink_2", x0 - MARGIN - 80, lh=1.35)
        my = top + (oy - cy0) * sc              # marker on the screenshot
        cv.ellipse(x0 - 26, my - 11, x0 - 4, my + 11, "green")
        cv.text(x0 - 15, my, str(i + 1), "caption", "white", anchor="mm")
    cv.save(out("dat-lenh-lo"))


if __name__ == "__main__":
    featured()
    steps()
    cost()
    margin()
    order_screen()
