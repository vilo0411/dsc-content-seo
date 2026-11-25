import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO


spec = importlib.util.spec_from_file_location(
    "snapshot_security", Path(__file__).resolve().parents[1] / "scripts/snapshot_security.py"
)
security = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security)


class SnapshotSecurityTests(unittest.TestCase):
    def test_redacts_repeated_keys_without_changing_map_markup(self):
        key = "AIza" + "a" * 35
        html = f'<script src="https://maps.googleapis.com/maps/api/js?key={key}&#038;ver=1"></script>{key}'
        clean = security.redact_google_api_keys(html)
        self.assertEqual(clean, html.replace(key, security.REDACTED))
        self.assertEqual(security.redact_google_api_keys(clean), clean)

    def test_check_fails_without_printing_secret(self):
        key = "AIza" + "b" * 35
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "snapshot.html").write_text(key)
            output = StringIO()
            with patch.object(subprocess, "check_output", return_value=b"snapshot.html\0"), redirect_stdout(output):
                self.assertEqual(security.check_tracked_files(root), 1)
            self.assertIn("snapshot.html", output.getvalue())
            self.assertNotIn(key, output.getvalue())
            (root / "snapshot.html").write_text(security.REDACTED)
            with patch.object(subprocess, "check_output", return_value=b"snapshot.html\0"), redirect_stdout(StringIO()):
                self.assertEqual(security.check_tracked_files(root), 0)


if __name__ == "__main__":
    unittest.main()
