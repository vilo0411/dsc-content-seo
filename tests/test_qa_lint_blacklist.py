"""Regression tests for the blacklist rules qa_lint.py reads from anti-ai-rules-blacklist.md.
Run: python -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import qa_lint as ql  # noqa: E402


class _Rep:
    def __init__(self):
        self.items = []

    def add(self, check, _cat, sev, _line, _msg, _raw=""):
        self.items.append((check, sev))


def lint(text):
    hard, hedge, soft = ql.load_blacklist()
    rep = _Rep()
    ql.check_anti_ai(rep, text.splitlines(), 0, hard, hedge, soft, [])
    return {c for c, _ in rep.items}


class BlacklistTest(unittest.TestCase):
    def test_self_introducing_sapo_is_critical(self):
        for s in ["Bài viết này giúp bạn nắm rõ chỉ số DXY.",
                  "Bài viết này sẽ phân tích 50 triệu nên gửi đâu.",
                  "Bài viết dưới đây của DSC sẽ giải thích cách tính."]:
            self.assertIn("CL2-blacklist", lint(s), s)

    def test_disclaimer_is_not_flagged(self):
        self.assertNotIn("CL2-blacklist", lint("Thông tin trong bài viết này chỉ mang tính chất tham khảo."))

    def test_hype_words_are_soft_banned(self):
        for s in ["Siêu bảng so sánh 4 kênh sinh lời.", "Đây là yếu tố sống còn.", "5 chỉ số vàng cho F0."]:
            self.assertIn("CL2-softban", lint(s), s)

    def test_replacement_suggestions_are_not_banned(self):
        # right-hand side of "→" is advice, never a banned term
        _, _, soft = ql.load_blacklist()
        self.assertNotIn("cốt lõi", soft)
        self.assertNotIn("bảng so sánh", soft)


if __name__ == "__main__":
    unittest.main()
