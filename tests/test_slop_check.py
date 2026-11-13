"""Regression tests for scripts/slop_check.py.  Run: python -m unittest discover tests"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import slop_check as sc  # noqa: E402


class FillerTest(unittest.TestCase):
    def test_flags_empty_short_sentences(self):
        for s in ["Đây là chỉ báo rất nhạy.", "Quy tắc này áp dụng nhất quán.",
                  "Đây là bước then chốt.", "Thao tác này rất nhanh.", "Con số này rất lớn."]:
            self.assertTrue(sc.is_filler(s), s)

    def test_keeps_short_sentences_that_say_something(self):
        for s in ["Hoàn toàn không.",                    # stance / direct answer
                  "Đây không phải chân lý.",             # negation = stance
                  "Lỗ 7% thì cắt ngay.",                 # number
                  "VCB tăng 12% trong quý.",             # ticker + number
                  "Đây là bẫy.",                         # < 4 words
                  "Đây là quy định của HOSE."]:          # named entity
            self.assertFalse(sc.is_filler(s), s)

    def test_long_sentence_is_never_filler(self):
        self.assertFalse(sc.is_filler("Đây là chỉ báo rất nhạy với biến động của lãi suất và dòng vốn ngoại."))


class AnchorTest(unittest.TestCase):
    def test_brand_mention_is_not_evidence(self):
        s = "Khi cần hỗ trợ, đội ngũ của DSC luôn đồng hành cùng bạn trong mọi quyết định."
        self.assertTrue(sc.is_unanchored(s))
        self.assertTrue(sc.is_unanchored(s.replace("DSC", "App DSC Trading")))

    def test_real_entity_still_anchors(self):
        self.assertFalse(sc.is_unanchored("Khi cần hỗ trợ, đội ngũ của DSC giải thích cơ chế ký quỹ theo quy định của UBCKNN."))
        self.assertFalse(sc.is_unanchored("Khi lãi suất tăng, dòng vốn ngoại rút khỏi nhóm cổ phiếu ngân hàng như VCB."))


def _write(dir_: Path, body: str) -> Path:
    p = dir_ / "Draft-x.md"
    p.write_text("---\nTitle: X\n---\n\n# X\n\n" + body, encoding="utf-8")
    return p


class MeasureTest(unittest.TestCase):
    def test_fillers_do_not_buy_rhythm(self):
        long = "Nhà đầu tư cần theo dõi diễn biến tỷ giá và lãi suất điều hành trước khi giải ngân vào cổ phiếu."
        clean = " ".join([long] * 6)
        padded = " ".join([long, "Đây là bước then chốt."] * 3)
        with tempfile.TemporaryDirectory() as d:
            m_clean = sc.measure(sc.Doc(_write(Path(d), clean + "\n")))
            m_padded = sc.measure(sc.Doc(_write(Path(d), padded + "\n")))
        self.assertEqual(m_padded["filler_n"], 3)
        self.assertEqual(m_padded["rhythm_gap"], m_clean["rhythm_gap"])
        self.assertEqual(m_padded["short_share"], 0.0)

    def test_judge_reports_filler(self):
        m = {k: 0 for k in ("burstiness", "uniform_run", "rhythm_gap", "evidence_per_100w",
                            "unanchored_ratio", "vague_per_1000w", "hedge_para_max", "synonym_variants",
                            "h2_def_open", "para_shape_sd", "inline_headers", "thin_tables")}
        m.update(burstiness=9, evidence_per_100w=5, para_shape_sd=1, filler_n=4)
        ids = {(c, s) for c, s, _ in sc.judge(m, (0.0, ""), sc.T)}
        self.assertIn(("SLOP-filler", "MAJOR"), ids)
        m["filler_n"] = 1
        self.assertNotIn("SLOP-filler", {c for c, _, _ in sc.judge(m, (0.0, ""), sc.T)})
        self.assertIn(("SLOP-filler", "MINOR"), {(c, s) for c, s, _ in sc.judge(m, (0.0, ""), sc.T_STRICT)})


class ModeTest(unittest.TestCase):
    def test_auto_mode_is_strict_only_for_drafts(self):
        self.assertEqual(sc.thresholds_for(sc.DRAFTS_DIR / "Draft-a.md", "auto")[1], "strict")
        self.assertEqual(sc.thresholds_for(sc.FINAL_DIR / "Final-a.md", "auto")[1], "relative")
        self.assertEqual(sc.thresholds_for(sc.FINAL_DIR / "Final-a.md", "strict")[1], "strict")

    def test_strict_is_never_looser_than_relative(self):
        low_is_bad = {"burstiness", "evidence", "para_shape"}
        for k, v in sc.T.items():
            s = sc.T_STRICT[k]
            if any(k.startswith(p) for p in low_is_bad):
                self.assertGreaterEqual(s, v, k)
            else:
                self.assertLessEqual(s, v, k)


if __name__ == "__main__":
    unittest.main()
