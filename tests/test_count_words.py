"""qa_lint / outline_lint import scripts/count_words.py for per-section word budgets."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import count_words as cw  # noqa: E402

OUTLINE = """### H2: Chứng khoán là gì
**Target:** 120 từ

### H2: Cách mở tài khoản
**Target:** 200 từ
"""
DRAFT = """## Chứng khoán là gì
Chứng khoán là tài sản tài chính có thể mua bán trên thị trường.

## Cách mở tài khoản
Nhà đầu tư mở tài khoản online bằng eKYC trong vài phút.
"""


class CountWordsApiTest(unittest.TestCase):
    def test_outline_and_draft_sections_match(self):
        outline = cw.parse_outline(OUTLINE)
        draft = cw.parse_draft(DRAFT)
        self.assertEqual([s.target for s in outline], [120, 200])
        match = cw.find_best_match(outline[1], draft)
        self.assertIsNotNone(match)
        self.assertGreater(match.words, 5)


if __name__ == "__main__":
    unittest.main()
