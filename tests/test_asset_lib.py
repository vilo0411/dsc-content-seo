"""Tests for scripts/asset_lib.py (không gọi Codex/Unsplash). Run: python -m unittest discover tests"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import asset_lib as al  # noqa: E402


class ChromaKeyTest(unittest.TestCase):
    def test_magenta_removed_object_kept(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "m.png", Path(d) / "o.png"
            im = Image.new("RGB", (400, 400), (255, 0, 255))
            ImageDraw.Draw(im).ellipse((120, 120, 280, 280), fill=(212, 170, 60))
            im.save(src)
            w, h = al.chroma_key(src, dst, pad=10)
            out = Image.open(dst)
            self.assertEqual(out.mode, "RGBA")
            self.assertLess(w, 400)                       # cắt sát vật
            self.assertEqual(out.getpixel((0, 0))[3], 0)  # góc trong suốt
            r, g, b, a = out.getpixel((w // 2, h // 2))
            self.assertEqual(a, 255)
            self.assertLess(abs(r - 212) + abs(g - 170) + abs(b - 60), 10)


class FindTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._index = al.INDEX
        al.INDEX = Path(self.tmp.name) / "index.json"
        base = {"kind": "bg", "theme": "emerald", "side": "right", "master": "tall", "file": "x", "status": "active", "used": []}
        al.INDEX.write_text(json.dumps({"assets": {
            "a-tet": dict(base, season="tet", tags=["Tết", "hoa mai"]),
            "a-all": dict(base, season="all", tags=["núi"]),
            "a-used": dict(base, season="tet", tags=["Tết", "hoa mai"], used=[{"date": "2026-11-01"}] * 3),
            "a-left": dict(base, side="left", season="all", tags=["Tết"]),
            "a-wide": dict(base, master="wide", season="all", tags=["Tết"]),
            "a-rej": dict(base, status="rejected", season="tet", tags=["Tết", "hoa mai"]),
        }}), encoding="utf-8")

    def tearDown(self):
        al.INDEX = self._index
        self.tmp.cleanup()

    def test_rank_by_tags_season_and_usage(self):
        ids = [r[0] for r in al.find("emerald", "right", "4:5", ["Tết", "hoa mai"], "bg", "tet")]
        self.assertEqual(ids[0], "a-tet")
        self.assertLess(ids.index("a-tet"), ids.index("a-used"))
        self.assertNotIn("a-left", ids)   # sai phía chừa chữ
        self.assertNotIn("a-wide", ids)   # sai khổ (4:5 cần bản dọc)
        self.assertNotIn("a-rej", ids)    # đã loại

    def test_wide_for_landscape(self):
        self.assertEqual([r[0] for r in al.find("emerald", "right", "1.91:1", [], "bg")], ["a-wide"])


class PromptTest(unittest.TestCase):
    def test_motif_prompt_uses_magenta_and_bans_text(self):
        p = al.prompt_for({"kind": "motif", "theme": "emerald", "master": "square", "subject": "a golden crane"})
        self.assertIn("#FF00FF", p)
        self.assertIn("NO text", p)

    def test_bg_prompt_reserves_side(self):
        p = al.prompt_for({"kind": "bg", "theme": "ivory", "master": "tall", "side": "top", "subject": "mountains"})
        self.assertIn("top 45%", p)
        self.assertIn("9:16", p)


if __name__ == "__main__":
    unittest.main()
