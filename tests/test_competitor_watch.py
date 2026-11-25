"""competitor_watch.py filtering: hub scope, category pages, PR posts, baseline dating."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import competitor_watch as cw  # noqa: E402
from _common import unaccent  # noqa: E402

VPB = {"domain": "www.vpbanks.com.vn", "hub": "/trung-tam-kien-thuc/"}
ROOT_HUB = {"domain": "www.vfs.com.vn", "hub": "/", "exclude": ["/khuyen-mai-"]}


class FilterTest(unittest.TestCase):
    def test_hub_scope_and_category_pages(self):
        self.assertTrue(cw.in_hub("https://www.vpbanks.com.vn/trung-tam-kien-thuc/eps-la-gi", VPB))
        self.assertFalse(cw.in_hub("https://www.vpbanks.com.vn/trung-tam-kien-thuc/kien-thuc-chung", VPB))
        self.assertFalse(cw.in_hub("https://www.vpbanks.com.vn/san-pham/margin", VPB))

    def test_root_hub_needs_article_like_slug_and_honours_exclude(self):
        self.assertTrue(cw.in_hub("https://www.vfs.com.vn/phi-giao-dich-chung-khoan-phai-sinh", ROOT_HUB))
        self.assertFalse(cw.in_hub("https://www.vfs.com.vn/lien-he", ROOT_HUB))
        self.assertFalse(cw.in_hub("https://www.vfs.com.vn/khuyen-mai-mo-tai-khoan-thang-11", ROOT_HUB))

    def test_pr_titles(self):
        self.assertTrue(cw.PR_RX.match(unaccent("THÔNG BÁO NGƯNG CUNG CẤP DỊCH VỤ KÝ QUỸ")))
        self.assertFalse(cw.PR_RX.match(unaccent("Cổ phiếu ưu đãi là gì?")))

    def test_baseline_rows_without_published_date_are_not_new(self):
        self.assertEqual(cw.event_date({"baseline": "1", "first_seen": "2026-11-19", "published": ""}), "")
        self.assertEqual(cw.event_date({"baseline": "1", "first_seen": "2026-11-19", "published": "2026-09-27"}), "2026-09-27")
        self.assertEqual(cw.event_date({"baseline": "", "first_seen": "2026-11-19", "published": ""}), "2026-11-19")


if __name__ == "__main__":
    unittest.main()
