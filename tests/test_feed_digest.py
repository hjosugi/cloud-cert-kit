import argparse
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from scripts.build_feed_digest import FeedItem, TinyNaiveBayes, analyze, build_digest, parse_feed


ROOT = Path(__file__).resolve().parents[1]


class FeedDigestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.training = json.loads((ROOT / "config/training-data.json").read_text())["examples"]
        cls.rules = json.loads((ROOT / "config/analysis-rules.json").read_text())
        cls.model = TinyNaiveBayes(cls.training)

    def test_parses_rss_and_strips_markup(self):
        xml = (ROOT / "tests/fixtures/rss.xml").read_text()
        items = parse_feed(xml, "aws", "Fixture")
        self.assertEqual(2, len(items))
        self.assertEqual("2026-07-10T08:00:00Z", items[0].published_at)
        self.assertNotIn("CDATA", items[0].summary)

    def test_parses_atom_link(self):
        xml = (ROOT / "tests/fixtures/atom.xml").read_text()
        items = parse_feed(xml, "gcp", "Fixture")
        self.assertEqual("https://example.com/bigquery-governance", items[0].link)
        self.assertEqual("2026-07-10T08:00:00Z", items[0].published_at)

    def test_splits_gcp_day_entry_into_product_updates(self):
        xml = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <title>July 10, 2026</title><updated>2026-07-10T00:00:00Z</updated>
        <link rel="alternate" href="https://example.com/day"/>
        <content type="html">&lt;h2 class="release-note-product-title"&gt;BigQuery&lt;/h2&gt;
        &lt;h3&gt;Feature&lt;/h3&gt;&lt;p&gt;Hybrid vector search is generally available.&lt;/p&gt;
        &lt;h2 class="release-note-product-title"&gt;Cloud VPN&lt;/h2&gt;
        &lt;h3&gt;Change&lt;/h3&gt;&lt;p&gt;New network routing behavior.&lt;/p&gt;</content>
        </entry></feed>"""
        items = parse_feed(xml, "gcp", "Fixture")
        self.assertEqual(2, len(items))
        self.assertTrue(items[0].title.startswith("BigQuery — Feature"))
        self.assertTrue(items[1].title.startswith("Cloud VPN — Change"))

    def test_deadline_rule_overrides_probabilistic_category(self):
        item = FeedItem(
            "aws",
            "Fixture",
            "Generative AI legacy API reaches end of support",
            "https://example.com/item",
            "2026-07-10T08:00:00Z",
            "Customers must migrate before retirement.",
        )
        perspectives = json.loads((ROOT / "config/cloud-perspectives.json").read_text())
        result = analyze(item, self.model, self.rules, datetime(2026, 7, 11, tzinfo=timezone.utc), perspectives)
        self.assertEqual("deprecation", result["category"])
        self.assertEqual("今すぐ確認", result["priority"])
        self.assertIn("AIP-C01", result["study_impact"])
        self.assertEqual("retirement", result["release_stage"])
        self.assertEqual("genai", result["comparison_category"])
        self.assertIn("Amazon Bedrock", result["cross_cloud_context"])
        self.assertIn("resource scope", result["cross_cloud_context"])

    def test_perspectives_add_vendor_boundary_and_comparison_starting_point(self):
        perspectives = json.loads((ROOT / "config/cloud-perspectives.json").read_text())
        item = FeedItem(
            "gcp",
            "Fixture",
            "Cloud VPN routing update",
            "https://example.com/network",
            "2026-07-10T08:00:00Z",
            "New network routing behavior is generally available.",
        )
        result = analyze(item, self.model, self.rules, datetime(2026, 7, 11, tzinfo=timezone.utc), perspectives)
        self.assertEqual("ga", result["release_stage"])
        self.assertIn("Organization / Folder / Project", result["design_perspective"])
        self.assertIn("同等性を示す一覧ではありません", result["cross_cloud_context"])

    def test_cached_data_is_used_when_one_feed_fails(self):
        prior = {
            "items": [
                {
                    "id": "cached",
                    "vendor": "aws",
                    "source": "old",
                    "title": "Cached update",
                    "url": "https://example.com/cached",
                    "published_at": "2026-07-01T00:00:00Z",
                    "excerpt": "",
                    "category": "operations",
                    "category_label": "運用・信頼性",
                    "tags": ["operations"],
                    "priority": "記録のみ",
                    "score": 30,
                    "confidence": "中",
                    "signals": [],
                    "why_it_matters": "cached",
                    "study_impact": "cached",
                    "recommended_action": "cached",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            sources = temp / "sources.json"
            output = temp / "digest.json"
            sources.write_text(json.dumps({"sources": [{"vendor": "aws", "name": "bad", "url": "https://invalid.example/feed"}]}))
            output.write_text(json.dumps(prior))
            args = argparse.Namespace(
                sources=sources,
                training=ROOT / "config/training-data.json",
                rules=ROOT / "config/analysis-rules.json",
                perspectives=ROOT / "config/cloud-perspectives.json",
                output=output,
                per_source=10,
                timeout=1,
                strict=False,
            )
            with patch("scripts.build_feed_digest.fetch_text", side_effect=OSError("offline")):
                digest = build_digest(args)
            self.assertEqual("cached", digest["source_status"][0]["status"])
            self.assertEqual("Cached update", digest["items"][0]["title"])


if __name__ == "__main__":
    unittest.main()
