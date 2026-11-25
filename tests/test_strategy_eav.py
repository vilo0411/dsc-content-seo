"""Strategy layer (taxonomy.json topics) + EAV: one source for cluster catalog, core/outer, attributes."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / ".agents/skills/web-serp/scripts"))
import outline_lint  # noqa: E402
import page_groups  # noqa: E402
import qa_lint  # noqa: E402
import registry  # noqa: E402
import serp_research  # noqa: E402


class TopicCatalogTest(unittest.TestCase):
    def test_page_groups_reads_catalog_from_taxonomy(self):
        topics = json.loads(registry.TAXONOMY.read_text(encoding="utf-8"))["topics"]
        self.assertEqual(page_groups.CLUSTERS, {c: t["name"] for c, t in topics.items()})
        self.assertIn("3b", page_groups.SUBGROUPS)

    def test_every_link_cluster_points_to_a_topic(self):
        data = json.loads(registry.TAXONOMY.read_text(encoding="utf-8"))
        self.assertTrue(all(c.get("topic") in data["topics"] for c in data["clusters"]))

    def test_topic_problems(self):
        data = {"topics": {"1": {"name": "A", "section": "core", "attributes": [{"name": "phí", "fact": "nope"}],
                                 "subgroups": {"1a": "Tài khoản"}},
                           "3": {"name": "B", "section": "outer", "bridge_to": ""},
                           "9": {"name": "C", "section": "middle"}},
                "clusters": [{"id": "x", "topic": "1", "groups": [{"name": "1a Tài khoản cũ"}]}]}
        out = " | ".join(registry.topic_problems(data, set(), {"trading_fee"}))
        self.assertIn("cụm 3 (outer): thiếu bridge_to", out)
        self.assertIn("section `middle`", out)
        self.assertIn("fact `nope`", out)
        self.assertIn("tên nhóm lệch", out)

    def test_suggest_section(self):
        self.assertEqual(registry.suggest_section(0.38, 0.07, 0.01, 5000), "core")   # big share of key events
        self.assertEqual(registry.suggest_section(0.02, 0.03, 0.01, 5000), "core")   # converts 3x site rate
        self.assertEqual(registry.suggest_section(0.02, 0.03, 0.01, 200), "outer")   # too little traffic to tell
        self.assertEqual(registry.suggest_section(0.01, 0.001, 0.01, 9000), "outer")

    def test_attribute_coverage_uses_aliases(self):
        rows = [{"slug": "t2", "title": "Chu kỳ T+2 là gì", "key_chinh": "", "key_phu": "", "keywords": ""}]
        self.assertEqual(registry.covered({"name": "chu kỳ thanh toán", "aliases": ["t+2"]}, rows), ["t2"])
        self.assertEqual(registry.covered({"name": "lô giao dịch"}, rows), [])


class ActionTest(unittest.TestCase):
    def row(self, **kw):
        base = dict(slug="a", cluster="3", labels="", priority="0", sessions=0, key_events=0)
        base.update(kw)
        return base

    def test_actions(self):
        rows = [self.row(slug="dead", labels="dead"),
                self.row(slug="drop", labels="rank-drop", priority="50"),
                self.row(slug="small", labels="striking", priority="5"),
                self.row(slug="bridge", labels="convert-low", sessions=300),
                self.row(slug="core", cluster="5", labels="convert-low", sessions=300)]
        page_groups.decide_actions(rows)
        got = {r["slug"]: r["action"] for r in rows}
        self.assertEqual(got, {"dead": "prune?", "drop": "refresh", "small": "keep", "bridge": "bridge", "core": "keep"})


def comp(domain, md):
    return {"url": "https://%s/x" % domain, "domain": domain, "content": md,
            "sections": serp_research.split_sections(md), "word_count": 900}


class EavTest(unittest.TestCase):
    def test_root_and_rare_attributes(self):
        body = "Nội dung giải thích chi tiết cho người mới. " * 30
        pages = [
            comp("a.vn", f"## 1. Biên độ dao động giá\nBiên độ trên HOSE là 7%. {body}\n## Phí giao dịch\n{body}"),
            comp("b.vn", f"## Biên độ dao động giá HOSE\nHOSE 7%, HNX 10%. {body}\n## Ví dụ tính giá trần\n{body}"),
            comp("c.vn", f"## II. Biên độ dao động giá các sàn\n{body}\n## Lịch sử\n{body}"),
        ]
        data = {"keyword": "giá trần là gì", "organic": [{"url": p["url"]} for p in pages], "competitors": pages}
        res = serp_research.eav_candidates(data)
        top = res["rows"][0]
        self.assertEqual((top["attribute"], top["type"], top["n"]), ("Biên độ dao động giá", "root", 3))
        self.assertTrue(any("7%" in v for _, v in top["values"]))
        self.assertTrue(all(r["type"] == "rare" for r in res["rows"][1:]))

    def test_outline_eav_parse_and_planned(self):
        yaml_raw = ('EAV:\n  - attribute: "biên độ dao động giá"\n    entity: "HOSE"\n    value: "±7%"\n'
                    '    source: "market_facts"\n    type: root\n    h2: "Biên độ"\nPersona: P2\n')
        items = outline_lint.parse_eav(yaml_raw)
        self.assertEqual(items[0]["value"], "±7%")
        self.assertTrue(outline_lint.attr_planned("Biên độ dao động giá HOSE", ["biên độ dao động giá"]))
        self.assertFalse(outline_lint.attr_planned("Phí giao dịch", ["biên độ dao động giá"]))

    def test_draft_must_carry_eav_values(self):
        outline = ROOT / "scratch" / "_test_eav_outline.md"
        outline.parent.mkdir(exist_ok=True)
        outline.write_text('---\nEAV:\n  - attribute: "phí"\n    value: "0,1%"\n    source: "brand-facts:trading_fee"\n'
                           '    type: unique\n  - attribute: "lô"\n    value: "100 cổ phiếu"\n    source: "market_facts"\n'
                           '    type: root\nPersona: P2\n---\n# x\n', encoding="utf-8")
        try:
            rep = qa_lint.Report("x")
            qa_lint.check_eav(rep, ["# Bài", "Phí giao dịch từ 0.1% mỗi lệnh."], 0, outline)
            msgs = [f for f in rep.findings if f.check == "EAV-value-missing"]
            self.assertEqual(len(msgs), 1)
            self.assertIn("100 cổ phiếu", msgs[0].message)
        finally:
            outline.unlink()


if __name__ == "__main__":
    unittest.main()


class FrontmatterDatesTest(unittest.TestCase):
    def run_stamp(self, text):
        import _common
        p = ROOT / "scratch" / "_test_stamp.md"
        p.parent.mkdir(exist_ok=True)
        p.write_text(text, encoding="utf-8")
        try:
            _common.stamp_frontmatter(p, Updated="2026-11-25")
            return p.read_text(encoding="utf-8")
        finally:
            p.unlink()

    def test_leading_yaml_updated_in_place(self):
        out = self.run_stamp("---\nStatus: Outline\nUpdated: 2026-01-01\n---\n# T\n")
        self.assertEqual(out, "---\nStatus: Outline\nUpdated: 2026-11-25\n---\n# T\n")

    def test_fenced_yaml_of_old_template(self):
        out = self.run_stamp("# T\n```yaml\n---\nStatus: Outline\n---\n```\nbody\n")
        self.assertIn("Status: Outline\nUpdated: 2026-11-25\n---\n```", out)

    def test_no_yaml_gets_a_block(self):
        self.assertTrue(self.run_stamp("# Proposal\n").startswith("---\nUpdated: 2026-11-25\n---\n\n# Proposal"))


class SiteLayerTest(unittest.TestCase):
    def test_every_folder_with_clicks_is_mapped(self):
        v = registry.site_sections()
        self.assertTrue(all(s["section"] in registry.SITE_SECTIONS for s in v["sections"]))
        self.assertEqual(v["unmapped"], [])
