"""Images for thi-truong-so-cap-va-thu-cap-la-gi (DSC image design system, dsc_design.py).
Featured 1000x600, in-article 800x500. Run from repo root:
    python scripts/images/generate_so_cap_thu_cap_images.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (MARGIN, CANVAS, FEATURED, FEATURED_OUT, Canvas, inline_frame, tag)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "thi-truong-so-cap-va-thu-cap-la-gi"
W, H = CANVAS
R = W - MARGIN
BOTTOM = H - 58


def out(name):
    return os.path.join(OUT, f"{SLUG}-{name}.jpg")


def arrow(cv, x0, y, x1, color="green", width=3):
    # horizontal arrow from x0 to x1 at height y
    cv.line([(x0, y), (x1 - 8, y)], color, width)
    cv.d.polygon([((x1) * 3, y * 3), ((x1 - 12) * 3, (y - 7) * 3), ((x1 - 12) * 3, (y + 7) * 3)],
                 fill="#2AD03D" if color == "green" else "#B9C3BF")


def featured():
    cv = Canvas(FEATURED, "navy", out=FEATURED_OUT)
    cv.glow(640, 380, 260, "green", 70)
    cv.glow(780, 40, 150, "teal", 35)
    cv.paste_logo(MARGIN, 32, dark=True, height=22)

    s = "KIẾN THỨC NHẬP MÔN"
    w = cv.tlen(s, "eyebrow") + 1.2 * len(s) + 26
    cv.rect(MARGIN, 96, MARGIN + w, 122, "navy_800", r=13, outline="green_900", width=1)
    cv.text(MARGIN + 13, 109, s, "eyebrow", "bright", anchor="lm", tracking=1.2)

    cv.text(MARGIN, 136, "Thị trường", "display", "white")
    cv.text(MARGIN, 190, "sơ cấp và thứ cấp", "display", "white")
    cv.gradient_text(MARGIN, 244, "tiền về ai?", "display")

    stats = [("6", "điểm khác nhau"), ("T+2", "cổ phiếu về tài khoản"), ("30 tỷ", "vốn tối thiểu khi IPO")]
    for i, (big, small) in enumerate(stats):
        x = MARGIN + i * 150
        if i:
            cv.line([(x - 16, 350), (x - 16, 392)], "navy_700", 1)
        cv.text(x, 346, big, "num_m", "white")
        cv.text(x, 378, small, "caption", "ink_3")

    # two stacked cards: primary vs secondary
    cards = [(120, "SƠ CẤP", "Nhà đầu tư → Doanh nghiệp", "Tiền vào công ty"),
             (270, "THỨ CẤP", "Nhà đầu tư → Nhà đầu tư", "Tiền vào người bán")]
    for y, head, flow, note in cards:
        x0, x1 = 500, 760
        cv.shadow(x0, y, x1, y + 120, r=16, blur=16, alpha=90, dy=10)
        cv.rect(x0, y, x1, y + 120, "white", r=16)
        tag(cv, x0 + 18, y + 18, head)
        cv.text(x0 + 18, y + 58, flow, "h2", "navy")
        cv.text(x0 + 18, y + 86, note, "body_m", "green_700")
    cv.save(out("featured"))


def money_flow():
    cv, top = inline_frame("Tiền của nhà đầu tư đi về đâu",
                           "Ví dụ giả định: IPO 10 triệu cổ phiếu, sau đó đổi chủ 3 lần trên sàn",
                           eyebrow="Dòng tiền", source="Số liệu minh họa, chưa tính phí và thuế")
    gap = 16
    cw = (R - MARGIN - gap) / 2
    panels = [
        (MARGIN, "Thị trường sơ cấp", "Giá IPO 20.000 VNĐ", "200 tỷ VNĐ", "vào tài khoản công ty", "green",
         ["Nhà đầu tư", "Công ty phát hành"]),
        (MARGIN + cw + gap, "Thị trường thứ cấp", "Giá 25.000 VNĐ × 3 lần", "750 tỷ VNĐ",
         "vào tài khoản nhà đầu tư bán", "navy", ["Nhà đầu tư mua", "Nhà đầu tư bán"]),
    ]
    for x0, head, sub, big, note, col, nodes in panels:
        x1 = x0 + cw
        cv.card(x0, top, x1, BOTTOM)
        cv.text(x0 + 20, top + 18, head, "h2", "navy")
        cv.text(x0 + 20, top + 44, sub, "body", "ink_2")
        # flow nodes
        ny = top + 96
        nw = (cw - 40 - 50) / 2
        for i, lab in enumerate(nodes):
            nx = x0 + 20 + i * (nw + 50)
            cv.rect(nx, ny, nx + nw, ny + 44, "mint_100", r=10)
            cv.text(nx + nw / 2, ny + 22, lab, "caption", "green_700", anchor="mm")
        arrow(cv, x0 + 20 + nw + 6, ny + 22, x0 + 20 + nw + 44)
        cv.text(x0 + 20, ny + 84, big, "num_xl", "navy" if col == "navy" else "green_700")
        cv.text(x0 + 20, ny + 140, note, "body_m", "ink_2")
        done = "Công ty nhận thêm: 0 VNĐ" if col == "navy" else "Vốn mới cho doanh nghiệp"
        tag(cv, x0 + 20, BOTTOM - 36, done, fill="mint_100" if col != "navy" else "track",
            color="green_700" if col != "navy" else "navy")
    cv.save(out("dong-tien-ipo"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    featured()
    money_flow()
