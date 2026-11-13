"""Tests for scripts/article_snapshot.py.  Run: python -m unittest discover tests"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import article_snapshot as snap  # noqa: E402


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self._orig = (snap.ROOT, snap.CONTENT, snap.ARCHIVE, snap.LEDGER, snap.SOURCES)
        snap.ROOT = root
        snap.CONTENT = root / "knowledge/4-content"
        snap.ARCHIVE = snap.CONTENT / "archive"
        snap.LEDGER = root / "knowledge/3-pipeline/publish-ledger.csv"
        snap.SOURCES = {
            "outline": [snap.CONTENT / "1-outlines" / "{slug}.md"],
            "gate2": [snap.CONTENT / "2-drafts" / "Draft-{slug}.md"],
            "final": [snap.CONTENT / "3-finalized" / "Final-{slug}.md"],
        }
        for d in ("1-outlines", "2-drafts", "3-finalized"):
            (snap.CONTENT / d).mkdir(parents=True)

    def tearDown(self):
        snap.ROOT, snap.CONTENT, snap.ARCHIVE, snap.LEDGER, snap.SOURCES = self._orig
        self.tmp.cleanup()

    def _quiet(self, fn, *a):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = fn(*a)
        return code, buf.getvalue()

    def test_final_archives_outline_and_diff_shows_only_changes(self):
        (snap.CONTENT / "1-outlines/x.md").write_text("# Outline", encoding="utf-8")
        (snap.CONTENT / "2-drafts/Draft-x.md").write_text("Đoạn A.\n\nĐoạn B cũ.\n\nĐoạn C.", encoding="utf-8")
        self.assertEqual(self._quiet(snap.snapshot, "x", "outline")[0], 0)
        self.assertEqual(self._quiet(snap.snapshot, "x", "gate2")[0], 0)
        (snap.CONTENT / "3-finalized/Final-x.md").write_text("Đoạn A.\n\nĐoạn B mới hẳn.\n\nĐoạn C.", encoding="utf-8")
        self.assertEqual(self._quiet(snap.snapshot, "x", "final")[0], 0)

        self.assertFalse((snap.CONTENT / "1-outlines/x.md").exists())          # moved, not deleted
        self.assertTrue((snap.ARCHIVE / "x/outline.md").exists())
        code, out = self._quiet(snap.diff, "x", "gate2", "final")
        self.assertEqual(code, 0)
        self.assertIn("- Đoạn B cũ.", out)
        self.assertIn("+ Đoạn B mới hẳn.", out)
        self.assertNotIn("Đoạn A.", out.split("\n", 2)[2])                   # unchanged blocks not printed

        ledger = snap.read_ledger()["x"]
        self.assertTrue(ledger["outline"] and ledger["gate2"] and ledger["final"])

    def test_second_gate2_keeps_previous(self):
        draft = snap.CONTENT / "2-drafts/Draft-y.md"
        draft.write_text("v1", encoding="utf-8")
        self._quiet(snap.snapshot, "y", "gate2")
        draft.write_text("v2", encoding="utf-8")
        self._quiet(snap.snapshot, "y", "gate2")
        self.assertEqual((snap.ARCHIVE / "y/gate2.prev.md").read_text(encoding="utf-8"), "v1")
        self.assertEqual((snap.ARCHIVE / "y/gate2.md").read_text(encoding="utf-8"), "v2")


if __name__ == "__main__":
    unittest.main()
