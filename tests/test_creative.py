"""Tests for scripts/creative.py. Run: python -m unittest discover tests
The render test needs Playwright + Chromium; it is skipped when they are missing."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import creative as cv  # noqa: E402

COPY = """## V1 · Proof · P2
Primary text: Mở tài khoản chứng khoán DSC online trong khoảng 3 phút.
Headline: Mở tài khoản trong 3 phút
Creative: 1080×1350 · S01 · chữ trên ảnh: "Mở tài khoản 3 phút"

## V2 · Proof · P2
Primary text: Phí từ 0,1% theo biểu phí hiện hành.
Headline: Phí từ 0,1%
Creative: 1080×1080 · S03 · chữ trên ảnh: "Phí từ 0,1%"

## facebook · V3 · carousel
Hình: carousel 1080×1080 × 3 slide · S03 · slide 1 "3 điều nên so"
"""


def make_job(d: Path) -> Path:
    copy = d / "CMP-261124-test" / "ads" / "copy-v1.md"
    copy.parent.mkdir(parents=True)
    copy.write_text(COPY, encoding="utf-8")
    return copy


class InitTest(unittest.TestCase):
    def test_init_parses_sizes_styles_and_locks(self):
        with tempfile.TemporaryDirectory() as d:
            copy = make_job(Path(d))
            data = json.loads(cv.init(copy).read_text(encoding="utf-8"))
            byid = {c["id"]: c for c in data["creatives"]}
            self.assertEqual(byid["ads-v1"]["size"], "1080x1350")
            self.assertEqual(byid["ads-v1"]["layout"], "thesis")
            self.assertEqual(byid["ads-v2"]["theme"], "paper")
            self.assertIn("biểu phí", byid["ads-v2"]["text"]["note"])
            slides = [c for c in data["creatives"] if c.get("group") == "ads-v3"]
            self.assertEqual([s["layout"] for s in slides], ["thesis", "rows", "cta-end"])
            locks = cv.locked_texts(copy)
            self.assertEqual(locks["ads-v1"], "Mở tài khoản 3 phút")
            self.assertEqual(locks["ads-v3-01"], "3 điều nên so")
            with self.assertRaises(SystemExit):
                cv.init(copy)  # không ghi đè design.json


class LayoutTest(unittest.TestCase):
    def test_every_layout_has_all_aspects(self):
        for p in cv.LAYOUT_DIR.glob("*.json"):
            lay = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(set(lay["variants"]), set(cv.ASPECTS), p.name)
            for v in lay["variants"].values():
                for r in v["regions"].values():
                    x, y, w, h = r["box"]
                    self.assertTrue(0 <= x and 0 <= y and x + w <= 1.001 and y + h <= 1.001, p.name)

    def test_headline_grows_into_empty_slots(self):
        lay = cv.load_layout("thesis")
        regs = cv.effective_regions(lay["variants"]["4:5"]["regions"], {"text": {"headline": "x", "note": "n"}})
        head = regs["headline"]
        self.assertEqual(head["valign"], "center")
        self.assertGreater(head["box"][3], lay["variants"]["4:5"]["regions"]["headline"]["box"][3])
        self.assertLessEqual(head["box"][1] + head["box"][3], regs["note"]["box"][1] + 1e-6)

    def test_text_widens_without_image(self):
        lay = cv.load_layout("thesis")
        regs = cv.effective_regions(lay["variants"]["1.91:1"]["regions"], {"text": {"headline": "x"}})
        self.assertNotIn("image", regs)
        self.assertAlmostEqual(regs["headline"]["box"][2], 0.9)

    def test_contrast(self):
        self.assertGreater(cv.contrast("#FFFFFF", "#0D1B2A"), 15)
        self.assertLess(cv.contrast("#00AD14", "#E8F8F2"), 3)


class LockAndAdaptTest(unittest.TestCase):
    def test_keeps_locked_allows_labels_not_edits(self):
        self.assertTrue(cv.keeps_locked("Phí từ 0,1% • Môi giới 1:1", "Phí giao dịch từ 0,1% Có **môi giới 1:1** đi kèm"))
        self.assertFalse(cv.keeps_locked("Phí từ 0,1%", "Phí từ 0%"))
        self.assertFalse(cv.keeps_locked("Mở tài khoản 3 phút", "3 phút mở tài khoản"))

    def test_adapt_adds_sizes_once(self):
        with tempfile.TemporaryDirectory() as d:
            dj = cv.init(make_job(Path(d)))
            added = cv.adapt(dj, cv.CHANNEL_SIZES["meta-ads"], only=["ads-v1"])
            self.assertEqual(sorted(added), ["ads-v1-1080x1080", "ads-v1-1080x1920", "ads-v1-1200x628"])
            self.assertEqual(cv.adapt(dj, cv.CHANNEL_SIZES["meta-ads"], only=["ads-v1"]), [])


class KVTest(unittest.TestCase):
    def test_prompt_reserves_text_side_and_bans_text(self):
        cr = {"id": "x", "layout": "kv-right", "theme": "emerald", "size": "1080x1350",
              "kv": {"subject": "two golden cranes", "motifs": ["lotus"]}}
        pr = cv.kv_prompt(cr)
        self.assertIn("left side", pr)
        self.assertIn("right 45%", pr)
        self.assertIn("NO text", pr)
        self.assertIn("No red anywhere", pr)
        self.assertIn("lacquer red", cv.kv_prompt(dict(cr, allow_red=True)))

    def test_kv_layouts_keep_image_region(self):
        lay = cv.load_layout("kv-right")
        regs = cv.effective_regions(lay["variants"]["1:1"]["regions"], {"text": {"headline": "x"}}, keep_image=True)
        self.assertIn("image", regs)


class RenderTest(unittest.TestCase):
    def test_render_qa_and_approve(self):
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                p.chromium.launch().close()
        except Exception as e:  # noqa: BLE001
            self.skipTest(f"Playwright/Chromium không có: {e}")
        with tempfile.TemporaryDirectory() as d:
            copy = make_job(Path(d))
            dj = cv.init(copy)
            data = json.loads(dj.read_text(encoding="utf-8"))
            data["creatives"] = [c for c in data["creatives"] if not c.get("group")]
            data["creatives"][0]["text"]["headline"] = "Mở tài khoản **3 phút**"   # nhấn không phá khoá
            data["creatives"][1]["text"]["headline"] = "Phí 0%"                      # đổi chữ → TEXT-locked
            dj.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            out, qa = cv.render(dj)
            q1, q2 = qa["creatives"]["ads-v1"], qa["creatives"]["ads-v2"]
            self.assertTrue((out / "ads-v1.png").exists() and (out / "preview.html").exists())
            self.assertNotEqual(q1["status"], "Chưa đạt", q1["issues"])
            self.assertIn("TEXT-locked", {i["rule"] for i in q2["issues"]})
            with self.assertRaises(SystemExit):
                cv.approve(dj, ["ads-v2"], "ok")
            copied = cv.approve(dj, ["ads-v1"], "duyệt v1")
            self.assertTrue(copied[0].name.startswith("CMP-261124-test-ads-v1-v1"))
            with self.assertRaises(SystemExit):
                cv.render(dj)  # v1 đã duyệt → phải --bump
            _, qa2 = cv.render(dj, bump=True)
            self.assertEqual(qa2["version"], 2)


if __name__ == "__main__":
    unittest.main()
