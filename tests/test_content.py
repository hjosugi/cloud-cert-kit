import re
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REPOSITORY_LINK_RE = re.compile(
    r"https://github\.com/hjosugi/cloud-hub/blob/main/([^\"#?]+)"
)


class LearningContentTests(unittest.TestCase):
    def test_aip_flashcard_count(self):
        text = (ROOT / "docs/learning/aip-c01/flashcards.md").read_text(encoding="utf-8")
        self.assertEqual(50, len(re.findall(r"^### \d+$", text, re.MULTILINE)))

    def test_scenario_drill_count(self):
        text = (ROOT / "docs/learning/aip-c01/scenario-drills.md").read_text(encoding="utf-8")
        self.assertEqual(20, len(re.findall(r"^## \d+\.", text, re.MULTILINE)))

    def test_local_markdown_links_exist(self):
        files = [ROOT / "README.md"]
        files.extend((ROOT / "docs").rglob("*.md"))
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

    def test_site_repository_links_exist(self):
        html = (ROOT / "site/cloud-hub.html").read_text(encoding="utf-8")
        missing = [
            path
            for path in REPOSITORY_LINK_RE.findall(html)
            if not (ROOT / path).exists()
        ]
        self.assertEqual([], missing)

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
        canonical = {
            "cloud-philosophies.md",
            "multicloud-design.md",
            "operations-comparison.md",
            "release-intelligence.md",
            "service-and-cost-comparison.md",
        }
        localized = {name.removesuffix(".md") + ".ja.md" for name in canonical}
        actual = {path.name for path in (ROOT / "docs/guides").glob("*.md")}
        self.assertEqual(canonical | localized, actual)

    def test_purpose_catalog_has_four_clouds_and_official_links(self):
        data = json.loads((ROOT / "site/data/service-catalog.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["use_cases"]), 15)
        cost_ids = {item["id"] for item in json.loads((ROOT / "site/data/cost-baselines.json").read_text())["scenarios"]}
        for use_case in data["use_cases"]:
            self.assertEqual({"aws", "azure", "gcp", "oci"}, set(use_case["services"]))
            self.assertTrue(use_case["keywords"])
            self.assertTrue(use_case["questions"])
            for service in use_case["services"].values():
                self.assertTrue(service["url"].startswith("https://"))
            if "cost_scenario" in use_case:
                self.assertIn(use_case["cost_scenario"], cost_ids)

    def test_cost_baselines_are_traceable_and_calculable(self):
        data = json.loads((ROOT / "site/data/cost-baselines.json").read_text(encoding="utf-8"))
        self.assertRegex(data["checked_at"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual("USD", data["currency"])
        for scenario in data["scenarios"]:
            self.assertEqual({"aws", "azure", "gcp", "oci"}, set(scenario["providers"]))
            self.assertTrue(scenario["assumptions"])
            for provider in scenario["providers"].values():
                rate = provider.get("hourly_rate", provider.get("monthly_rate", 0))
                self.assertGreater(rate, 0)
                self.assertTrue(provider["source"].startswith("https://"))
        vm = next(item for item in data["scenarios"] if item["id"] == "linux-vm-2vcpu-8gb")
        self.assertAlmostEqual(60.955, vm["providers"]["aws"]["hourly_rate"] * 730, places=3)

    def test_site_exposes_purpose_search_and_cost_comparison(self):
        html = (ROOT / "site/cloud-hub.html").read_text(encoding="utf-8")
        for expected in ('id="service-search"', 'id="service-results"', 'id="cost-scenario"', 'id="cost-results"', "capacity-match"):
            self.assertIn(expected, html)


if __name__ == "__main__":
    unittest.main()
