"""Tests for scripts/mkt_lint.py and scripts/campaign.py.
Run: python -m unittest discover tests"""
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import campaign  # noqa: E402
import mkt_lint as ml  # noqa: E402


def run(text, channel):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.md"
        p.write_text(text, encoding="utf-8")
        rep = ml.lint(p, channel)
    return rep, {i.rule for i in rep.issues}


CLEAN_FB = """## facebook · V1 · giáo dục
Mua cổ phiếu lần đầu, nhiều F0 đặt lệnh thị trường lúc 9h15 và khớp giá cao hơn dự tính.
Lệnh giới hạn giúp bạn chọn đúng mức giá muốn mua. Đọc hướng dẫn đặt lệnh: https://www.dsc.com.vn/kien-thuc/lenh-gioi-han
#DSC #F0
"""

CLEAN_AD = """## V1 · Proof · P2
Primary text: Mở tài khoản chứng khoán online trong khoảng 3 phút với eKYC.
Headline: Mở tài khoản DSC online
Description: eKYC 100% online

## Ghi chú
Primary text: bỏ qua mục này chắc chắn lãi
"""


class MktLintTest(unittest.TestCase):
    def test_clean_facebook_passes(self):
        rep, rules = run(CLEAN_FB, "facebook")
        self.assertTrue(rep.passed, rules)

    def test_profit_promise_is_critical(self):
        rep, rules = run("Đầu tư cùng DSC, cam kết lợi nhuận 2%/tháng. Mở tài khoản ngay.", "facebook")
        self.assertIn("COMP-promise", rules)
        self.assertFalse(rep.passed)

    def test_ticker_advice_is_critical_on_ads(self):
        _, rules = run("Primary text: Nên mua HPG vùng 25.000.\nHeadline: Cơ hội HPG", "meta-ad")
        self.assertIn("COMP-advice", rules)

    def test_margin_needs_risk(self):
        _, rules = run("Lãi suất margin chỉ 10% áp dụng từ ngày 1/12. Mở tài khoản.", "facebook")
        self.assertIn("COMP-leverage-risk", rules)
        _, rules = run("Lãi suất margin chỉ 10% áp dụng từ ngày 1/12, lưu ý rủi ro call margin. Mở tài khoản.", "facebook")
        self.assertNotIn("COMP-leverage-risk", rules)

    def test_rate_without_condition(self):
        _, rules = run("Phí giao dịch chỉ 0,1%. Mở tài khoản.", "facebook")
        self.assertIn("COMP-rate-condition", rules)

    def test_ad_fields_and_skip_notes(self):
        rep, rules = run(CLEAN_AD, "meta-ad")
        self.assertEqual(rep.variants, 1)
        self.assertTrue(rep.passed, rules)
        _, rules = run("## V1\nHeadline: Mở tài khoản", "meta-ad")
        self.assertIn("FIELD-missing", rules)

    def test_ad_length(self):
        long = "Primary text: " + "a" * 130 + "\nHeadline: " + "b" * 50
        _, rules = run(long, "meta-ad")
        self.assertIn("LEN-primary", rules)
        self.assertIn("LEN-headline", rules)

    def test_competitor_negative_is_major(self):
        rep, rules = run("Phí DSC rẻ, VPS thì đắt hơn nhiều. Mở tài khoản.", "facebook")
        self.assertIn("COMP-competitor", rules)
        self.assertFalse(rep.passed)

    def test_blacklist_phrase(self):
        _, rules = run("Bạn có bao giờ tự hỏi vì sao F0 hay mua đỉnh? Đọc thêm tại link.", "facebook")
        self.assertIn("AI-blacklist", rules)


class CampaignTest(unittest.TestCase):
    def test_new_status_set(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            job = campaign.new("Mở tài khoản Tết", "Tết 2027", ["social", "ads"], date(2026, 11, 24), base)
            self.assertEqual(job.name, "CMP-261124-mo-tai-khoan-tet")
            self.assertTrue((job / "approved").is_dir() and (job / "ads").is_dir())
            self.assertEqual(campaign.read_status(job), "Brief")
            campaign.set_status(campaign.find("mo-tai-khoan-tet", base), "Chờ duyệt")
            rows = campaign.summary(base)
            self.assertEqual(rows[0]["status"], "Chờ duyệt")
            with self.assertRaises(SystemExit):
                campaign.set_status(job, "abc")


if __name__ == "__main__":
    unittest.main()
