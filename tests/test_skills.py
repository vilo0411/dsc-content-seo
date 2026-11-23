"""Guard the agent-facing instruction layer: skill frontmatter and path references.

Broken YAML makes agents silently fall back to the H1 title as the skill description,
and a stale path sends the agent on extra tool calls. Both are cheap to catch here.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
DOCS = [ROOT / "AGENTS.md", ROOT / ".agents" / "context.md", *SKILLS.glob("*/SKILL.md"),
        *(ROOT / ".agents" / "rules").glob("*.md")]
# Paths that are produced at runtime or gitignored - allowed to be missing.
OPTIONAL = {".agents/config/gsc-credentials.json", ".agents/config/gsc-token.json",
            ".agents/memory/instincts-archive.proposed.md", "knowledge/3-seo/cta-variants.md",
            "knowledge/raw/ga4/landing-pages.csv"}
PATH_RE = re.compile(r"`((?:\.agents|knowledge|scripts|tests)/[^`\s]+?)`")

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def frontmatter(text: str) -> str:
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    return m.group(1) if m else ""


class SkillFrontmatterTest(unittest.TestCase):
    @unittest.skipIf(yaml is None, "PyYAML not installed")
    def test_every_skill_has_valid_name_and_description(self):
        for f in sorted(SKILLS.glob("*/SKILL.md")):
            with self.subTest(skill=f.parent.name):
                data = yaml.safe_load(frontmatter(f.read_text(encoding="utf-8")))
                self.assertIsInstance(data, dict, "frontmatter is not a YAML mapping")
                self.assertEqual(data.get("name"), f.parent.name, "name must equal folder name")
                desc = data.get("description") or ""
                self.assertGreaterEqual(len(desc), 40, "description too short to route on")
                self.assertLessEqual(len(desc), 1024, "description over Agent Skills limit")


class PathReferenceTest(unittest.TestCase):
    def test_backticked_repo_paths_exist(self):
        missing = []
        for doc in DOCS:
            for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
                for raw in PATH_RE.findall(line):
                    p = raw.rstrip(".,:;)")
                    if re.search(r"[<>\[\]*{}]|YYYY|\.\.\.|…", p) or p in OPTIONAL:
                        continue
                    if not (ROOT / p).exists():
                        missing.append(f"{doc.relative_to(ROOT)}:{i}: {p}")
        self.assertEqual(missing, [], "\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
