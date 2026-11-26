"""Images for so-sanh-lai-suat-tiet-kiem-ngan-hang, built on the DSC image design system (dsc_design.py).
Featured 1000x600, in-article images 800x500 (CMS standard). Run from repo root:
    python3 scripts/images/generate_so_sanh_lai_suat_images.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (C, SS, MARGIN, CANVAS, FEATURED, FEATURED_OUT, Canvas, inline_frame, tag)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "so-sanh-lai-suat-tiet-kiem-ngan-hang"
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

    s = "SO SÁNH LÃI SUẤT 2026"
    w = cv.tlen(s, "eyebrow") + 1.2 * len(s) + 26
    cv.rect(MARGIN, 96, MARGIN + w, 122, "navy_800", r=13, outline="green_900", width=1)
    cv.text(MARGIN + 13, 109, s, "eyebrow", "bright", anchor="lm", tracking=1.2)

    cv.text(MARGIN, 136, "So sánh lãi suất", "display", "white")
    cv.text(MARGIN, 190, "tiết kiệm ngân hàng", "display", "white")
    cv.gradient_text(MARGIN, 244, "Big 4 và TMCP", "display")

    stats = [
        ("5,2–7,5%", "lãi suất kỳ hạn 12 tháng"),
        ("11,5 triệu", "chênh lệch trên 500 triệu"),
        ("350 triệu", "hạn mức bảo hiểm tiền gửi"),
    ]
    for i, (big, small) in enumerate(stats):
        x = MARGIN + i * 155
        if i:
            cv.line([(x - 16, 350), (x - 16, 392)], "navy_700", 1)
        cv.text(x, 346, big, "num_m", "white")
        cv.text(x, 378, small, "caption", "ink_3")

    # Right card showing 12-month rate comparison
    px0, py0, px1, py1 = 508, 44, 764, 442
    cv.shadow(px0, py0, px1, py1, r=22, blur=20, alpha=90, dy=12)
    cv.rect(px0, py0, px1, py1, "navy_800", r=22, outline="navy_700", width=1)
    cv.text(px0 + 18, py0 + 22, "Lãi 12 tháng (500 triệu)", "h2", "white")
    cv.text(px0 + 18, py0 + 48, "Tiền lãi nhận cuối kỳ theo nhóm", "caption", "ink_3")

    rows = [
        ("Big 4 tại quầy", "5,20%/năm", "26,0 triệu VNĐ", 0.55, "neutral"),
        ("Big 4 online", "5,90–7,00%", "29,5–35,0 triệu VNĐ", 0.78, "emerald"),
        ("TMCP lớn online", "6,55–7,25%", "32,8–36,3 triệu VNĐ", 0.88, "emerald"),
        ("TMCP top online", "7,40–7,50%", "37,0–37,5 triệu VNĐ", 1.00, "green"),
    ]
    for i, (lab, rate, amt, ratio, col) in enumerate(rows):
        y = py0 + 86 + i * 74
        cv.text(px0 + 18, y, lab, "body_m", "white")
        cv.text(px1 - 18, y, rate, "body_m", "frosted_mint", anchor="ra")
        bar_w = (px1 - px0 - 36) * ratio
        cv.rect(px0 + 18, y + 24, px1 - 18, y + 36, "navy_700", r=6)
        cv.rect(px0 + 18, y + 24, px0 + 18 + bar_w, y + 36, col, r=6)
        cv.text(px0 + 18, y + 42, amt, "caption", "ink_3")

    cv.save(out("featured"))


def compare_500m():
    cv, top = inline_frame(
        "Chênh lệch tiền lãi 12 tháng với vốn 500 triệu VNĐ",
        "Đặt nhóm Big 4 tại quầy cạnh kênh online của nhóm TMCP lớn và TMCP dẫn đầu",
        eyebrow="Quy đổi tiền thật",
        source="Khảo sát biểu lãi suất niêm yết năm 2026 · Bảo hiểm tiền gửi: Thông tư 05/2026/TT-NHNN",
    )
    # Left card: Big highlight + 4 bars
    lx0, lx1 = MARGIN, 456
    cv.card(lx0, top, lx1, BOTTOM)
    cv.text(lx0 + 20, top + 16, "Khoảng chênh tiền lãi tối đa mỗi năm", "caption", "ink_3")
    cv.text(lx0 + 20, top + 34, "11.500.000 VNĐ", "num_xl", "navy")

    bars = [
        ("Big 4 tại quầy (5,20%)", 0.69, "26.000.000 VNĐ", "neutral"),
        ("ACB online (6,55%)", 0.87, "32.750.000 VNĐ", "navy"),
        ("Techcombank online (7,25%)", 0.96, "36.250.000 VNĐ", "navy"),
        ("MBV / LPBank (7,40–7,50%)", 1.00, "37.500.000 VNĐ", "green"),
    ]
    for i, (lab, ratio, val, col) in enumerate(bars):
        y = top + 108 + i * 50
        cv.text(lx0 + 20, y, lab, "body", "ink_2", anchor="lm")
        cv.text(lx1 - 20, y, val, "body_m", "green_700" if col == "green" else "navy", anchor="rm")
        cv.rect(lx0 + 20, y + 14, lx1 - 20, y + 26, "track", r=6)
        bw = (lx1 - lx0 - 40) * ratio
        cv.rect(lx0 + 20, y + 14, lx0 + 20 + bw, y + 26, col, r=6)

    # Right card: Deposit insurance split rule (350M)
    rx0, rx1 = 472, R
    cv.card(rx0, top, rx1, BOTTOM)
    cv.text(rx0 + 20, top + 16, "Quy tắc chia sổ dưới 350 triệu", "h2", "navy")
    cv.wrap(
        rx0 + 20,
        top + 42,
        "Từ 13/7/2026, hạn mức Bảo hiểm tiền gửi là 350 triệu VNĐ (gồm gốc và lãi) tại mỗi ngân hàng.",
        "body",
        "ink_2",
        rx1 - rx0 - 40,
        lh=1.35,
    )

    splits = [
        ("Sổ 1 · Ngân hàng A (250 triệu gốc)", "Gốc + lãi ~267 triệu ≤ 350 triệu", "navy"),
        ("Sổ 2 · Ngân hàng B (250 triệu gốc)", "Gốc + lãi ~268 triệu ≤ 350 triệu", "green_700"),
    ]
    for i, (head, sub, col) in enumerate(splits):
        y = top + 116 + i * 74
        cv.rect(rx0 + 20, y, rx1 - 20, y + 64, "mint_50", r=10, outline="line", width=1)
        cv.text(rx0 + 32, y + 12, head, "body_m", col)
        cv.text(rx0 + 32, y + 38, sub, "caption", "green_700")

    tag(cv, rx0 + 20, BOTTOM - 32, "Bảo vệ 100% gốc và lãi")
    cv.save(out("500-trieu"))


def allocation_80_20():
    cv, top = inline_frame(
        "Mô phỏng dòng tiền 500 triệu VNĐ sau 12 tháng",
        "So sánh giữ 100% tại quầy Big 4 với phương án 80% tiết kiệm online + 20% đầu tư tại DSC",
        eyebrow="Phân bổ 80 / 20",
        source="Mô phỏng dòng tiền 12 tháng · Phí giao dịch DSC từ 0,1% · Thuế bán 0,1%",
    )
    mid = W / 2
    panels = [
        (
            MARGIN,
            mid - 8,
            "Phương án 1: 100% quầy Big 4",
            "26.000.000 VNĐ",
            "Lãi bình quân: 2.166.667 VNĐ/tháng",
            [
                ("500 triệu tại quầy (5,20%)", "26,0 triệu đ", "neutral"),
                ("Lãi thực sau lạm phát 3,8%", "~7,0 triệu đ", "navy"),
            ],
            "An toàn gốc · Lãi thực mỏng",
        ),
        (
            mid + 8,
            R,
            "Phương án 2: 80% Tiết kiệm + 20% DSC",
            "31.900.000 VNĐ",
            "Kịch bản tăng trưởng 12%/năm: 38.900.000 VNĐ",
            [
                ("200 triệu Big 4 online (5,90%)", "11,8 triệu đ", "navy"),
                ("200 triệu TMCP online (7,00%)", "14,0 triệu đ", "green_700"),
                ("100 triệu cổ phiếu/ETF (6,1%)", "6,1 triệu đ", "green"),
            ],
            "2 sổ dưới 350 triệu · Tăng hiệu suất",
        ),
    ]
    for idx, (x0, x1, title, big_num, sub, items, tg) in enumerate(panels):
        cv.card(x0, top, x1, BOTTOM)
        cv.text(x0 + 20, top + 16, title, "h2", "navy")
        cv.text(x0 + 20, top + 46, big_num, "num_l", "green_700" if idx == 1 else "navy")
        cv.text(x0 + 20, top + 78, sub, "caption", "ink_3")
        cv.line([(x0 + 20, top + 102), (x1 - 20, top + 102)], "line", 1)
        for j, (ilab, ival, icol) in enumerate(items):
            ry = top + 122 + j * 44
            cv.ellipse(x0 + 20, ry + 4, x0 + 28, ry + 12, icol)
            cv.text(x0 + 36, ry, ilab, "body", "ink_2")
            cv.text(x1 - 20, ry, ival, "body_m", "navy", anchor="ra")
        tag(cv, x0 + 20, BOTTOM - 32, tg)

    cv.save(out("phan-bo-80-20"))


if __name__ == "__main__":
    featured()
    compare_500m()
    allocation_80_20()
    print("Generated 3 images successfully.")
