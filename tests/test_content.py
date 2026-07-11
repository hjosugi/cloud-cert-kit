import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class LearningContentTests(unittest.TestCase):
    def test_aip_flashcard_count(self):
        text = (ROOT / "study/aip-c01/flashcards.md").read_text(encoding="utf-8")
        self.assertEqual(50, len(re.findall(r"^### \d+$", text, re.MULTILINE)))

    def test_scenario_drill_count(self):
        text = (ROOT / "study/aip-c01/scenario-drills.md").read_text(encoding="utf-8")
        self.assertEqual(20, len(re.findall(r"^## \d+\.", text, re.MULTILINE)))

    def test_local_markdown_links_exist(self):
        files = [ROOT / "README.md"]
        files.extend((ROOT / "study").rglob("*.md"))
        files.extend((ROOT / "wrong-answers").rglob("*.md"))
        missing = []
        for source in files:
            for target in LINK_RE.findall(source.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#")):
                    continue
                path_text = target.split("#", 1)[0]
                if path_text and not (source.parent / path_text).resolve().exists():
                    missing.append(f"{source.relative_to(ROOT)} -> {target}")
        self.assertEqual([], missing)

    def test_site_exposes_learning_hub(self):
        html = (ROOT / "site/cloud-hub.html").read_text(encoding="utf-8")
        self.assertIn('data-t="learn"', html)
        self.assertIn('id="learn"', html)
        self.assertIn("50フラッシュカード", html)

    def test_site_leads_with_design_operations_and_release_views(self):
        html = (ROOT / "site/cloud-hub.html").read_text(encoding="utf-8")
        for expected in (
            'id="philosophy"',
            'id="ops"',
            "同等サービス比較の5点",
            "DESIGN VIEW",
            "OPERATIONS VIEW",
            "CROSS-CLOUD",
        ):
            self.assertIn(expected, html)

    def test_multicloud_guides_exist(self):
        expected = (
            "cloud-philosophies.md",
            "multicloud-design.md",
            "operations-comparison.md",
            "release-intelligence.md",
        )
        self.assertEqual(expected, tuple(path.name for path in sorted((ROOT / "guide").glob("*.md")) if path.name != "README.md"))


if __name__ == "__main__":
    unittest.main()
