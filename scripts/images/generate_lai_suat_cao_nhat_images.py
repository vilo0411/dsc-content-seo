"""Images for lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat (hub 10a), built on dsc_design.py.
In-article image 800x500. Run from repo root:
    python scripts/images/generate_lai_suat_cao_nhat_images.py
Numbers: VnExpress 26/11/2026 (listed ceiling, promotional offers and their conditions).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsc_design import (MARGIN, CANVAS, inline_frame)  # noqa: E402

OUT = "knowledge/3-seo/content/images"
SLUG = "lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat"
W, H = CANVAS
R = W - MARGIN
BOTTOM = H - 58


def out(name):
    return os.path.join(OUT, f"{SLUG}-{name}.jpg")


def listed_vs_promo():
    cv, top = inline_frame(
        "Lãi suất niêm yết và lãi suất ưu đãi tháng 11/2026",
        "Mức 9%/năm có thật, nhưng luôn đi kèm điều kiện",
        eyebrow="Đọc kỹ trước khi gửi",
        source="VnExpress 26/11/2026 · Mức niêm yết theo biểu công bố của từng ngân hàng",
    )
    # Left card: listed rates
    lx0, lx1 = MARGIN, 386
    cv.card(lx0, top, lx1, BOTTOM)
    cv.text(lx0 + 20, top + 16, "Lãi suất niêm yết", "h2", "navy")
    cv.text(lx0 + 20, top + 52, "7,9%/năm", "num_xl", "navy")
    cv.text(lx0 + 20, top + 112, "Cao nhất hệ thống: Saigonbank, 13 tháng", "caption", "ink_3")
    cv.line([(lx0 + 20, top + 140), (lx1 - 20, top + 140)], "line", 1)
    cv.text(lx0 + 20, top + 156, "≤ 7%/năm", "num_m", "green_700")
    cv.wrap(lx0 + 20, top + 194, "Khoản dưới 1 tỷ VNĐ, kỳ hạn 12 tháng", "caption", "ink_3",
            lx1 - lx0 - 40, lh=1.3)
    cv.wrap(lx0 + 20, top + 236, "Áp dụng cho mọi khách hàng, rút sớm theo biểu không kỳ hạn", "body",
            "ink_2", lx1 - lx0 - 40, lh=1.35)

    # Right card: promotional offers and conditions
    rx0, rx1 = 402, R
    cv.card(rx0, top, rx1, BOTTOM)
    cv.text(rx0 + 20, top + 16, "Lãi suất ưu đãi", "h2", "navy")
    cv.text(rx0 + 20, top + 52, "9–9,6%/năm", "num_xl", "green_700")
    conds = [
        "Tiền lãi trả trước bị phong tỏa",
        "Kèm quà tặng hoặc số tiền tối thiểu",
        "Rút sớm phải tất toán toàn bộ sổ",
    ]
    for i, c in enumerate(conds):
        y = top + 122 + i * 46
        cv.rect(rx0 + 20, y + 4, rx0 + 30, y + 14, "green", r=5)
        cv.wrap(rx0 + 40, y, c, "body", "ink_2", rx1 - rx0 - 60, lh=1.3)

    cv.save(out("niem-yet-va-uu-dai"))


if __name__ == "__main__":
    listed_vs_promo()
    print("saved", out("niem-yet-va-uu-dai"))
