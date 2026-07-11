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
        html = (ROOT / "site/quad-cloud-ops.html").read_text(encoding="utf-8")
        self.assertIn('data-t="learn"', html)
        self.assertIn('id="learn"', html)
        self.assertIn("50フラッシュカード", html)


if __name__ == "__main__":
    unittest.main()
