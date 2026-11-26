"""Tests for scripts/activity_log.py.  Run: python -m unittest discover tests"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import activity_log as al  # noqa: E402


class ActivityLogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self._orig = (al.ACTIVITY_DIR, al.LOGS_DIR, al.ROOT, al.FORCE)
        al.ACTIVITY_DIR = root / "activity"
        al.LOGS_DIR = root / "logs"
        al.ROOT = root
        al.FORCE = True
        al.LOGS_DIR.mkdir()

    def tearDown(self):
        al.ACTIVITY_DIR, al.LOGS_DIR, al.ROOT, al.FORCE = self._orig
        self.tmp.cleanup()

    def test_emit_writes_monthly_jsonl_with_schema(self):
        rec = al.emit("seo", "status", "abc", status_from="Planned", status_to="Outlining", skill="topic_status",
                      ts="2026-11-02T10:00:00", actor="tester")
        self.assertEqual(rec["status_to"], "Outlining")
        lines = (al.ACTIVITY_DIR / "2026-11.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        e = json.loads(lines[0])
        self.assertTrue(set(e) <= set(al.FIELDS))
        self.assertNotIn("path", e)  # empty fields are dropped
        self.assertEqual(al.read_events(since="2026-11-01")[0]["target"], "abc")

    def test_emit_never_raises(self):
        al.ACTIVITY_DIR = Path(self.tmp.name) / "file-not-dir"
        al.ACTIVITY_DIR.write_text("x")
        with redirect_stdout(io.StringIO()):
            import contextlib
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertIsNone(al.emit("seo", "qa", "x"))

    def test_skipped_under_unittest_unless_forced(self):
        al.FORCE = False
        self.assertIsNone(al.emit("seo", "qa", "x"))
        self.assertFalse(al.ACTIVITY_DIR.exists())

    def test_recent_has_dedups_by_path(self):
        al.emit("social", "create", "CMP-1", path=Path(self.tmp.name) / "a.md")
        self.assertTrue(al.recent_has(Path(self.tmp.name) / "a.md"))
        self.assertFalse(al.recent_has(Path(self.tmp.name) / "b.md"))

    def test_classify_paths(self):
        r = al.ROOT
        self.assertEqual(al.classify(r / "knowledge/6-campaigns/CMP-261124-x/social/fb-v1.md"), ("social", "CMP-261124-x"))
        self.assertEqual(al.classify(r / "knowledge/6-campaigns/CMP-261124-x/ads/creatives/design.json"), ("creative", "CMP-261124-x"))
        self.assertEqual(al.classify(r / "knowledge/6-campaigns/CMP-261124-x/brief.md"), ("campaign", "CMP-261124-x"))
        self.assertEqual(al.classify(r / "knowledge/4-channels/ads/2026-11-01-audit.md"), ("ads-google", "2026-11-01-audit"))
        self.assertEqual(al.classify(r / "knowledge/3-seo/content/2-drafts/Draft-abc.md"), ("seo", "abc"))
        self.assertIsNone(al.classify(r / "scripts/x.py"))

    def test_backfill_is_idempotent(self):
        (al.LOGS_DIR / "publish-ledger.csv").write_text(
            "slug,outline,gate2,final,first_live\nabc,2026-10-01,2026-10-03,2026-10-05,seed\n", encoding="utf-8")
        (al.LOGS_DIR / "revision-log.md").write_text("### [2026-10-02] - abc\n- x\n", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            al.backfill()
            n1 = len(al.read_events())
            al.backfill()
        self.assertEqual(n1, 4)  # outline, gate2, final (seed is not a date), revise
        self.assertEqual(len(al.read_events()), n1)
        self.assertTrue(all(e["src"] == "backfill" for e in al.read_events()))


if __name__ == "__main__":
    unittest.main()
