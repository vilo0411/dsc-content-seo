"""Registry (strategy/pages.csv) is the single source for links + article status."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import registry  # noqa: E402

ROWS = [
    {**{k: "" for k in registry.FIELDS}, "slug": "rsi-la-gi-cach-dung", "file_slug": "rsi-la-gi", "live": "yes",
     "status": "Finalized", "cluster": "3", "cluster_name": "Phân tích kỹ thuật", "subgroup": "3b",
     "subgroup_name": "Chỉ báo động lượng", "key_chinh": "rsi là gì"},
    {**{k: "" for k in registry.FIELDS}, "slug": "vang-sjc", "live": "yes", "status": "Live", "cluster": "11",
     "cluster_name": "Vàng", "subgroup": "13b", "subgroup_name": "Nghề tài chính"},
]


class RegistryTest(unittest.TestCase):
    def test_find_by_live_or_file_slug(self):
        self.assertEqual(registry.find(ROWS, "rsi-la-gi")[0]["slug"], "rsi-la-gi-cach-dung")
        self.assertEqual(registry.find(ROWS, "https://www.dsc.com.vn/kien-thuc/vang-sjc/")[0]["slug"], "vang-sjc")

    def test_exact_subgroup_code_beats_substring(self):
        self.assertEqual(registry.match_cluster(ROWS, "3b")[2], "3b")   # not 13b
        self.assertEqual(registry.match_cluster(ROWS, "nghe tai chinh")[2], "13b")

    def test_live_mapping_prefers_unique_prefix(self):
        live = {"chi-so-rsi": "", "rsi-la-gi-cach-dung": "RSI là gì"}
        self.assertEqual(registry._map_to_live("rsi-la-gi", "", live), "rsi-la-gi-cach-dung")

    def test_real_registry_loads(self):
        if registry.REGISTRY.exists():
            rows = registry.load()
            self.assertTrue(rows and all(r["slug"] for r in rows))
            self.assertEqual(len({r["slug"] for r in rows}), len(rows), "slug must be unique")


if __name__ == "__main__":
    unittest.main()
