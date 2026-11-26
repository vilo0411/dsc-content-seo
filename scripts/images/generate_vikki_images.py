"""Images for lai-suat-ngan-hang-dong-a (Vikki Bank), built on the DSC image design system (dsc_design.py).
In-article image 800x500 (CMS standard). Run from repo root:
    python scripts/images/generate_vikki_images.py
Numbers: Vikki online rate table effective 02/06/2026, general VND table effective 03/11/2026 (vikkibank.vn).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (MARGIN, CANVAS, inline_frame)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "lai-suat-ngan-hang-dong-a"
W, H = CANVAS
R = W - MARGIN
BOTTOM = H - 58


def out(name):
    return os.path.join(OUT, f"{SLUG}-{name}.jpg")


def interest_12m():
    cv, top = inline_frame(
        "Tiền lãi gửi Vikki Bank 12 tháng theo số tiền gửi",
        "Trả lãi cuối kỳ: online 6,10%/năm so với biểu chung 6,00%/năm",
        eyebrow="Quy đổi tiền thật",
        source="Biểu lãi suất Vikki Digital Bank: online hiệu lực 02/06/2026, biểu chung hiệu lực 03/11/2026",
    )
    # Left card: interest amount per deposit size, online vs general table
    lx0, lx1 = MARGIN, 486
    cv.card(lx0, top, lx1, BOTTOM)
    cv.text(lx0 + 20, top + 16, "Tiền lãi nhận sau 12 tháng", "h2", "navy")

    rows = [
        ("100 triệu VNĐ", "6.100.000", "6.000.000", 0.10),
        ("500 triệu VNĐ", "30.500.000", "30.000.000", 0.50),
        ("1 tỷ VNĐ", "61.000.000", "60.000.000", 1.00),
    ]
    track_w = lx1 - lx0 - 40
    for i, (lab, online, general, ratio) in enumerate(rows):
        y = top + 58 + i * 78
        cv.text(lx0 + 20, y, lab, "body_m", "ink_2")
        # Online bar
        cv.rect(lx0 + 20, y + 24, lx1 - 20, y + 34, "track", r=5)
        cv.rect(lx0 + 20, y + 24, lx0 + 20 + max(track_w * ratio, 14), y + 34, "green", r=5)
        cv.text(lx1 - 20, y, "Online " + online, "body_m", "green_700", anchor="ra")
        # General table bar (scaled by 6,00/6,10)
        cv.rect(lx0 + 20, y + 40, lx1 - 20, y + 50, "track", r=5)
        cv.rect(lx0 + 20, y + 40, lx0 + 20 + max(track_w * ratio * 6.00 / 6.10, 14), y + 50, "neutral", r=5)
        cv.text(lx1 - 20, y + 54, "Biểu chung " + general, "caption", "ink_3", anchor="ra")

    # Right card: monthly payout option and online gap
    rx0, rx1 = 502, R
    cv.card(rx0, top, rx1, BOTTOM)
    cv.text(rx0 + 20, top + 16, "Lãi hàng tháng", "h2", "navy")
    cv.wrap(rx0 + 20, top + 44, "Gói An Tâm 12 tháng, 5,94%/năm, gửi 500 triệu VNĐ:", "body", "ink_2",
            rx1 - rx0 - 40, lh=1.35)
    cv.text(rx0 + 20, top + 96, "2.475.000", "num_m", "navy")
    cv.text(rx0 + 20, top + 132, "VNĐ mỗi tháng", "caption", "ink_3")

    cv.line([(rx0 + 20, top + 164), (rx1 - 20, top + 164)], "line", 1)
    cv.text(rx0 + 20, top + 180, "Online cao hơn biểu chung", "body_m", "ink_2")
    cv.text(rx0 + 20, top + 208, "+0,3 điểm %", "num_m", "green_700")
    cv.wrap(rx0 + 20, top + 246, "ở kỳ hạn 7–11 tháng và 15–36 tháng", "caption", "ink_3",
            rx1 - rx0 - 40, lh=1.3)

    cv.save(out("tien-lai-12-thang"))


if __name__ == "__main__":
    interest_12m()
    print("saved", out("tien-lai-12-thang"))
