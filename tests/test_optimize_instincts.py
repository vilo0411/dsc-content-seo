"""Regression tests for scripts/optimize_instincts.py.  Run: python -m unittest discover tests"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import optimize_instincts as oi  # noqa: E402

ENTRY = """### {title}
- **Trạng thái:** ACTIVE
- **Nguồn:** test
- **Phản hồi từ User:** "ok"
- **Bản năng:** {body}
- **Phạm vi:** {scope}

"""


class ScopeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self._orig = (oi.ARCHIVE, oi.CORE, oi.SCOPE_DIR)
        oi.ARCHIVE, oi.CORE, oi.SCOPE_DIR = d / "archive.md", d / "instincts.md", d / "by-scope"

    def tearDown(self):
        oi.ARCHIVE, oi.CORE, oi.SCOPE_DIR = self._orig
        self.tmp.cleanup()

    def _run(self, entries):
        oi.ARCHIVE.write_text("## Bản năng Active\n\n" + "".join(ENTRY.format(**e) for e in entries), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(oi.run(450, False), 0)

    def test_slug_and_label_scopes_share_one_file(self):
        # "vi-mo" and "Chỉ topic: Vĩ mô" used to overwrite each other on disk.
        self._run([
            {"title": "Alpha GRDP tỉnh", "body": "Quy tắc A.", "scope": "vi-mo"},
            {"title": "Beta DXY tỷ giá", "body": "Quy tắc B.", "scope": "Chỉ topic: Vĩ mô"},
            {"title": "Gamma toàn cục", "body": "Quy tắc C.", "scope": "Global"},
        ])
        files = sorted(p.name for p in oi.SCOPE_DIR.glob("*.md"))
        self.assertEqual(files, ["vi-mo.md"])
        scoped = (oi.SCOPE_DIR / "vi-mo.md").read_text(encoding="utf-8")
        self.assertIn("Alpha GRDP tỉnh", scoped)
        self.assertIn("Beta DXY tỷ giá", scoped)
        self.assertIn("# Instincts — Vĩ mô", scoped)              # human label wins over slug
        core = oi.CORE.read_text(encoding="utf-8")
        self.assertEqual(core.count("`vi-mo.md`"), 1)
        self.assertIn("Gamma toàn cục", core)
        self.assertNotIn("Alpha GRDP tỉnh", core)

    def test_stale_scope_file_is_removed(self):
        self._run([{"title": "Alpha GRDP tỉnh", "body": "A.", "scope": "Chỉ topic: Vĩ mô"}])
        self.assertTrue((oi.SCOPE_DIR / "vi-mo.md").exists())
        self._run([{"title": "Alpha GRDP tỉnh", "body": "A.", "scope": "Chỉ topic: Phái sinh"}])
        self.assertFalse((oi.SCOPE_DIR / "vi-mo.md").exists())
        self.assertTrue((oi.SCOPE_DIR / "phai-sinh.md").exists())


TAGGED = """### {title}
- **ID:** {id}
- **Trạng thái:** {status}
- **Tag:** {tag}
- **Phạm vi:** {scope}
- **Bản năng:** {body}

"""


class AuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self._orig = (oi.ARCHIVE, oi.CORE, oi.SCOPE_DIR)
        oi.ARCHIVE, oi.CORE, oi.SCOPE_DIR = d / "archive.md", d / "instincts.md", d / "by-scope"

    def tearDown(self):
        oi.ARCHIVE, oi.CORE, oi.SCOPE_DIR = self._orig
        self.tmp.cleanup()

    def _run(self, entries, check=True):
        oi.ARCHIVE.write_text("".join(TAGGED.format(**e) for e in entries), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = oi.run(450, False, check)
        return code, buf.getvalue()

    def test_long_rule_is_reported_not_truncated(self):
        body = "Câu dài. " * 80
        code, out = self._run([{"title": "Dài", "id": "I001", "status": "ACTIVE", "tag": "a", "scope": "Global", "body": body}])
        self.assertEqual(code, 1)
        self.assertIn("[LONG]", out)
        self.assertIn(body.strip(), oi.CORE.read_text(encoding="utf-8"))   # full text, no "(…xem archive)"

    def test_article_and_deprecated_are_not_rendered(self):
        code, out = self._run([
            {"title": "Chuẩn", "id": "I003", "status": "ACTIVE", "tag": "a", "scope": "Global", "body": "Rule chuẩn."},
            {"title": "Ghi chú bài X", "id": "I001", "status": "ARTICLE", "tag": "a", "scope": "Global", "body": "Riêng bài X."},
            {"title": "Cũ", "id": "I002", "status": "DEPRECATED", "tag": "a", "scope": "Global", "body": "Cũ."},
        ])
        core = oi.CORE.read_text(encoding="utf-8")
        self.assertEqual(code, 0, out)
        self.assertIn("[I003] Chuẩn", core)
        self.assertNotIn("Riêng bài X", core)
        self.assertNotIn("Cũ.", core)

    def test_two_active_rules_with_same_tag_fail_check(self):
        code, out = self._run([
            {"title": "A", "id": "I001", "status": "ACTIVE", "tag": "sapo", "scope": "Global", "body": "A."},
            {"title": "B", "id": "I002", "status": "ACTIVE", "tag": "sapo", "scope": "Global", "body": "B."},
        ])
        self.assertEqual(code, 1)
        self.assertIn("TAG-DUP", out)


if __name__ == "__main__":
    unittest.main()
