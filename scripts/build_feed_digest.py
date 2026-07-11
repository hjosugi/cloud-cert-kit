#!/usr/bin/env python3
"""Build a static, interpreted cloud release digest from official feeds.

The analyzer intentionally uses only the Python standard library.  A tiny
multinomial Naive Bayes classifier is trained from curated seed examples on
every run, then deterministic safety/urgency rules add explainable signals.
No article content or user data is sent to an external model.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "cloud-hub/2.0 (+https://github.com/hjosugi/cloud-hub)"
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9.+#/-]*", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")

CATEGORY_LABELS = {
    "genai": "生成AI",
    "security": "セキュリティ",
    "data": "データ",
    "network": "ネットワーク",
    "operations": "運用・信頼性",
    "cost": "コスト",
    "certification": "資格・学習",
    "deprecation": "廃止・移行",
}

IMPLICATIONS = {
    "genai": {
        "meaning": "生成AIの設計選択肢、モデル連携、RAGまたはエージェント構成に影響する更新です。",
        "study": "生成AI系試験では、機能名だけでなく既存方式との使い分けと運用上の制約を確認します。",
        "action": "成熟度、対応リージョン、データ境界、評価方法、料金を確認し、採用ADRと運用手順への影響を記録します。",
    },
    "security": {
        "meaning": "権限境界、データ保護、プライベート接続または監査設計を変える可能性があります。",
        "study": "IAM・暗号化・ネットワーク境界のどの層で効く統制かを整理すると、横断的な設計問題に効きます。",
        "action": "既存構成への適用範囲、既定値、監査証跡を確認し、必要なら統制と例外手順を更新します。",
    },
    "data": {
        "meaning": "保存、処理、検索、移行の選択肢または性能・運用特性に関わる更新です。",
        "study": "データ系試験では、整合性・レイテンシ・スケーリング・運用負荷のトレードオフとして整理します。",
        "action": "対象ワークロード、整合性、上限、互換性、移行と復旧方法を確認し、データ設計の差分をADRへ反映します。",
    },
    "network": {
        "meaning": "接続経路、到達性、負荷分散、名前解決またはハイブリッド接続に関わる更新です。",
        "study": "L4/L7、公開/非公開、リージョナル/グローバルの軸で既存サービスとの違いを整理します。",
        "action": "通信経路、名前解決、到達性、障害ドメインを図にし、同等機能との差と切戻し方法を更新します。",
    },
    "operations": {
        "meaning": "可観測性、自動化、デプロイ、復旧またはスケーリングの運用負荷に影響する更新です。",
        "study": "最小運用負荷、監査可能性、再試行・ロールバックの要件語と結び付けます。",
        "action": "SLI、ログ、失敗時動作、quota、料金を確認し、監視とランブックの変更要否を記録します。",
    },
    "cost": {
        "meaning": "継続費用または価格性能比を変える可能性がある更新です。",
        "study": "オンデマンド、予約・コミット、バッチ、サーバーレスの利用率別トレードオフを整理します。",
        "action": "料金表、commitment、データ転送、運用工数を確認し、代表ワークロードで総費用差を試算します。",
    },
    "certification": {
        "meaning": "試験範囲、受験期限、教材の鮮度または資格ロードマップに直接影響する更新です。",
        "study": "現行の試験ガイドと教材の差分を確認し、廃止日や改定日から逆算して学習順を調整します。",
        "action": "公式試験ページを開き、コード、変更日、登録期限をPROGRESS.mdへ反映します。",
    },
    "deprecation": {
        "meaning": "互換性喪失や期限付き移行につながるため、通常の新機能より優先度が高い更新です。",
        "study": "旧名称・旧方式を正解として覚えないよう、後継サービスと期限を対で記録します。",
        "action": "終了日、影響inventory、代替手段、移行検証、rollbackを公式情報で確認し、ownerと期限付きIssueを作成します。",
    },
}


@dataclass(frozen=True)
class FeedItem:
    vendor: str
    source: str
    title: str
    link: str
    published_at: str
    summary: str


class TinyNaiveBayes:
    """Small multinomial NB classifier suitable for short release-note text."""

    def __init__(self, examples: list[dict[str, str]]) -> None:
        self.labels = sorted({item["label"] for item in examples})
        self.docs: Counter[str] = Counter()
        self.words: dict[str, Counter[str]] = defaultdict(Counter)
        self.totals: Counter[str] = Counter()
        vocabulary: set[str] = set()
        for item in examples:
            label = item["label"]
            tokens = tokenize(item["text"])
            self.docs[label] += 1
            self.words[label].update(tokens)
            self.totals[label] += len(tokens)
            vocabulary.update(tokens)
        self.vocab_size = max(1, len(vocabulary))
        self.doc_count = sum(self.docs.values())

    def probabilities(self, text: str) -> dict[str, float]:
        tokens = tokenize(text)
        log_scores: dict[str, float] = {}
        for label in self.labels:
            prior = (self.docs[label] + 1) / (self.doc_count + len(self.labels))
            score = math.log(prior)
            denominator = self.totals[label] + self.vocab_size
            for token in tokens:
                score += math.log((self.words[label][token] + 1) / denominator)
            log_scores[label] = score
        peak = max(log_scores.values())
        exps = {label: math.exp(score - peak) for label, score in log_scores.items()}
        total = sum(exps.values())
        return {label: value / total for label, value in exps.items()}


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def clean_text(value: str | None, limit: int = 600) -> str:
    if not value:
        return ""
    value = html.unescape(TAG_RE.sub(" ", value))
    value = SPACE_RE.sub(" ", value).strip()
    return value[:limit]


def normalize_url(value: str) -> str:
    if not value:
        return ""
    parts = urlsplit(value.strip())
    if parts.scheme not in {"http", "https"}:
        return ""
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def normalized_date(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip()
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def first_text(node: ET.Element, local_names: Iterable[str]) -> str:
    wanted = set(local_names)
    for child in node.iter():
        if child.tag.rsplit("}", 1)[-1] in wanted and child.text:
            return child.text.strip()
    return ""


def atom_link(node: ET.Element) -> str:
    for child in node.iter():
        if child.tag.rsplit("}", 1)[-1] == "link":
            href = child.attrib.get("href", "")
            rel = child.attrib.get("rel", "alternate")
            if href and rel in {"alternate", ""}:
                return href
    return ""


def split_gcp_daily_entry(
    vendor: str,
    source: str,
    raw_content: str,
    link: str,
    published_at: str,
) -> list[FeedItem]:
    """Turn Google's day-level Atom entries into product-level updates."""
    pattern = re.compile(
        r'<h2[^>]*class=["\'][^"\']*release-note-product-title[^"\']*["\'][^>]*>'
        r"(.*?)</h2>(.*?)(?=<h2[^>]*class=[\"\'][^\"\']*release-note-product-title|$)",
        re.IGNORECASE | re.DOTALL,
    )
    output: list[FeedItem] = []
    for product_html, body_html in pattern.findall(raw_content):
        product = clean_text(product_html, 120)
        body = clean_text(body_html, 600)
        if not product or not body:
            continue
        status_match = re.search(r"<h3[^>]*>(.*?)</h3>", body_html, re.IGNORECASE | re.DOTALL)
        status = clean_text(status_match.group(1), 50) if status_match else "Update"
        lead_match = re.search(r"<(?:strong|p)[^>]*>(.*?)</(?:strong|p)>", body_html, re.IGNORECASE | re.DOTALL)
        lead = clean_text(lead_match.group(1), 140) if lead_match else ""
        title = f"{product} — {status}"
        if lead and lead.lower() not in body.lower()[:20]:
            title += f": {lead}"
        output.append(FeedItem(vendor, source, title[:240], link, published_at, body))
    return output


def parse_feed(xml_text: str, vendor: str, source: str) -> list[FeedItem]:
    root = ET.fromstring(xml_text)
    nodes = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "item"]
    is_atom = not nodes
    if is_atom:
        nodes = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "entry"]

    items: list[FeedItem] = []
    seen: set[str] = set()
    for node in nodes:
        title = clean_text(first_text(node, ["title"]), 240)
        link = atom_link(node) if is_atom else first_text(node, ["link"])
        link = normalize_url(link)
        date = first_text(node, ["pubDate", "published", "updated", "date"])
        raw_summary = first_text(node, ["description", "summary", "content"])
        summary = clean_text(raw_summary, 600)
        if vendor == "gcp" and is_atom and "release-note-product-title" in raw_summary:
            split_items = split_gcp_daily_entry(vendor, source, raw_summary, link, normalized_date(date))
            for split_item in split_items:
                key = (split_item.link + split_item.title).lower()
                if key not in seen:
                    seen.add(key)
                    items.append(split_item)
            continue
        key = (link or title).lower()
        if not title or not key or key in seen:
            continue
        seen.add(key)
        items.append(FeedItem(vendor, source, title, link, normalized_date(date), summary))
    return items


def fetch_text(url: str, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def phrases_in(text: str, phrases: Iterable[str]) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in phrases if phrase.lower() in lowered]


def category_scores(text: str, model: TinyNaiveBayes, rules: dict[str, Any]) -> dict[str, float]:
    probabilities = model.probabilities(text)
    scores = {label: probability * 40 for label, probability in probabilities.items()}
    for label, terms in rules["category_terms"].items():
        hits = phrases_in(text, terms)
        scores[label] = scores.get(label, 0) + min(48, 12 * len(hits))
    return scores


def analyze(
    item: FeedItem,
    model: TinyNaiveBayes,
    rules: dict[str, Any],
    now: datetime,
    perspectives: dict[str, Any] | None = None,
) -> dict[str, Any]:
    text = f"{item.title} {item.summary}"
    scores = category_scores(text, model, rules)
    ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))
    category = ranked[0][0]

    # Explicit deadline and exam signals are safer than a probabilistic choice.
    if phrases_in(text, rules["category_terms"]["deprecation"]):
        category = "deprecation"
    elif phrases_in(text, rules["category_terms"]["certification"]):
        category = "certification"

    matched = {
        label: phrases_in(text, terms)
        for label, terms in rules["category_terms"].items()
    }
    tags = [label for label, hits in matched.items() if hits]
    if category not in tags:
        tags.insert(0, category)
    tags = sorted(set(tags), key=lambda label: (-scores.get(label, 0), label))[:3]

    critical_hits = phrases_in(text, rules["priority_terms"]["critical"])
    title_critical_hits = phrases_in(item.title, rules["priority_terms"]["critical"])
    high_hits = phrases_in(text, rules["priority_terms"]["high"])
    low_hits = phrases_in(text, rules["priority_terms"]["low"])
    focus = rules["focus"].get(item.vendor, {"exams": [], "boost_categories": []})

    score = 18 + min(22, int(scores.get(category, 0) / 3))
    # A deadline mentioned in the title is actionable; a term buried in a long
    # changelog is still relevant but should not flood the urgent queue.
    score += 28 if title_critical_hits else min(14, 7 * len(critical_hits))
    score += min(12, 4 * len(high_hits))
    score += 6 if category in focus["boost_categories"] else 0
    score -= 5 if low_hits and not high_hits and not critical_hits else 0

    if item.published_at:
        try:
            published = datetime.fromisoformat(item.published_at.replace("Z", "+00:00"))
            age_days = max(0, (now - published).days)
            score += 8 if age_days <= 3 else 5 if age_days <= 14 else 2 if age_days <= 45 else 0
        except ValueError:
            pass
    score = max(0, min(100, score))
    priority = "今すぐ確認" if score >= 72 else "今週確認" if score >= 52 else "記録のみ"

    evidence = (critical_hits + high_hits + matched.get(category, []))[:4]
    confidence = "高" if len(evidence) >= 2 or scores.get(category, 0) >= 55 else "中" if evidence else "低"
    implications = IMPLICATIONS[category]
    signal_text = "、".join(dict.fromkeys(evidence))
    why = implications["meaning"]
    if signal_text:
        why = f"「{signal_text}」が検出されました。{why}"

    title_lower = item.title.lower()
    text_lower = text.lower()
    if any(term in text_lower for term in ("retirement", "retire", "end of support", "sunset", "shut down")):
        release_stage = "retirement"
    elif any(term in text_lower for term in ("deprecation", "deprecated", "deprecate")):
        release_stage = "deprecation"
    elif any(term in text_lower for term in ("security advisory", "vulnerability", "cve-")):
        release_stage = "security"
    elif any(term in text_lower for term in ("generally available", "general availability", "now available")):
        release_stage = "ga"
    elif any(term in text_lower for term in ("preview", "beta", "alpha")):
        release_stage = "preview"
    else:
        release_stage = "update"

    perspective_data = perspectives or {}
    platform = perspective_data.get("vendors", {}).get(item.vendor, {})
    comparison_category = next(
        (label for label, _score in ranked if label not in {"deprecation", "certification"}),
        category,
    )
    equivalents = perspective_data.get("category_equivalents", {}).get(comparison_category, {})
    boundary = platform.get("boundary", "resource scopeとfailure domain")
    operations = platform.get("operations", "metric、log、quota、runbookへの影響を確認")
    philosophy = platform.get("philosophy", "cloud固有の責任境界から設計する")
    equivalent_text = " / ".join(f"{vendor.upper()}: {service}" for vendor, service in equivalents.items())
    design_perspective = f"{why} {item.vendor.upper()}では「{philosophy}」前提で、{boundary}のどこが変わるかを確認します。"
    operations_perspective = f"{operations}。既存resourceへの適用、既定値、Region、quota、metric、料金、rollbackを確認します。"
    cross_cloud_context = (
        f"{CATEGORY_LABELS[comparison_category]}領域の比較起点: {equivalent_text}。同等性を示す一覧ではありません。resource scope、IAM、HA、運用者責任を個別に比較します。"
        if equivalent_text else "他cloudの同領域とresource scope、IAM、HA、運用者責任を比較します。"
    )

    # Some official feeds (notably GCP) publish many product updates under one
    # day-level URL, so the title is part of the stable identity.
    uid_source = f"{item.vendor}:{item.link}:{item.title}"
    return {
        "id": hashlib.sha256(uid_source.encode("utf-8")).hexdigest()[:16],
        "vendor": item.vendor,
        "source": item.source,
        "title": item.title,
        "url": item.link,
        "published_at": item.published_at,
        "excerpt": item.summary[:280],
        "category": category,
        "category_label": CATEGORY_LABELS[category],
        "tags": tags,
        "priority": priority,
        "release_stage": release_stage,
        "comparison_category": comparison_category,
        "score": score,
        "confidence": confidence,
        "signals": list(dict.fromkeys(evidence)),
        "why_it_matters": why,
        "design_perspective": design_perspective,
        "operations_perspective": operations_perspective,
        "cross_cloud_context": cross_cloud_context,
        "study_impact": f"対象: {', '.join(focus['exams']) or '共通基礎'}。{implications['study']}",
        "recommended_action": implications["action"],
    }


def load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def summarize(items: list[dict[str, Any]], source_status: list[dict[str, Any]]) -> dict[str, Any]:
    priorities = Counter(item["priority"] for item in items)
    categories = Counter(item["category"] for item in items)
    vendors = Counter(item["vendor"] for item in items)
    stages = Counter(item.get("release_stage", "update") for item in items)
    urgent = [item for item in items if item["priority"] == "今すぐ確認"][:5]
    return {
        "total_items": len(items),
        "source_success": sum(1 for source in source_status if source["status"] == "ok"),
        "source_total": len(source_status),
        "priorities": dict(priorities),
        "categories": dict(categories.most_common()),
        "vendors": dict(vendors),
        "stages": dict(stages),
        "top_actions": [
            {"id": item["id"], "vendor": item["vendor"], "title": item["title"], "action": item["recommended_action"]}
            for item in urgent
        ],
    }


def build_digest(args: argparse.Namespace) -> dict[str, Any]:
    sources = json.loads(args.sources.read_text(encoding="utf-8"))["sources"]
    training = json.loads(args.training.read_text(encoding="utf-8"))["examples"]
    rules = json.loads(args.rules.read_text(encoding="utf-8"))
    perspectives = json.loads(args.perspectives.read_text(encoding="utf-8"))
    previous = load_previous(args.output)
    model = TinyNaiveBayes(training)
    now = datetime.now(timezone.utc)
    analyzed: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []

    for source in sources:
        vendor = source["vendor"]
        try:
            xml_text = fetch_text(source["url"], args.timeout)
            parsed = parse_feed(xml_text, vendor, source["name"])
            if not parsed:
                raise ValueError("feed contained no entries")
            candidates = [analyze(item, model, rules, now, perspectives) for item in parsed[:120]]
            candidates = sorted(candidates, key=lambda item: item["published_at"] or "", reverse=True)
            candidates = sorted(candidates, key=lambda item: item["score"], reverse=True)
            vendor_items = candidates[: args.per_source]
            analyzed.extend(vendor_items)
            statuses.append({"vendor": vendor, "status": "ok", "items": len(vendor_items), "message": ""})
        except Exception as exc:  # feed availability must not break the whole dashboard
            cached = [item for item in previous.get("items", []) if item.get("vendor") == vendor]
            analyzed.extend(cached[: args.per_source])
            statuses.append({
                "vendor": vendor,
                "status": "cached" if cached else "error",
                "items": min(len(cached), args.per_source),
                "message": f"{type(exc).__name__}: {str(exc)[:180]}",
            })
            print(f"warning: {vendor}: {exc}", file=sys.stderr)

    # Deduplicate cross-posts and favor the newest/highest-priority entries.
    deduped: dict[str, dict[str, Any]] = {}
    for item in analyzed:
        deduped.setdefault(item["id"], item)
    items = sorted(
        deduped.values(),
        key=lambda item: (-item["score"], item["published_at"] or "", item["vendor"], item["title"]),
        reverse=False,
    )
    # The score key above is descending; within equal scores newest should be first.
    items = sorted(items, key=lambda item: item["published_at"] or "", reverse=True)
    items = sorted(items, key=lambda item: item["score"], reverse=True)

    if args.strict and any(status["status"] != "ok" for status in statuses):
        failed = ", ".join(status["vendor"] for status in statuses if status["status"] != "ok")
        raise RuntimeError(f"strict mode: feed failures: {failed}")
    if not items:
        raise RuntimeError("no feed items available and no cached digest found")

    return {
        "schema_version": 2,
        "generated_at": now.isoformat().replace("+00:00", "Z"),
        "analyzer": {
            "name": "tiny-naive-bayes-plus-rules",
            "version": "2.0",
            "privacy": "公式フィードのタイトルと概要だけをローカル処理。外部AI APIへの送信なし。",
        },
        "source_status": statuses,
        "summary": summarize(items, statuses),
        "items": items,
    }


def to_markdown(digest: dict[str, Any]) -> str:
    summary = digest["summary"]
    lines = [
        "# Cloud Hub release intelligence",
        "",
        f"生成日時: {digest['generated_at']}",
        f"取得元: {summary['source_success']}/{summary['source_total']}、分析件数: {summary['total_items']}",
        "",
        "## 優先項目",
        "",
    ]
    for item in digest["items"]:
        if item["priority"] == "記録のみ":
            continue
        title = item["title"].replace("|", "\\|")
        link = f"[{title}]({item['url']})" if item["url"] else title
        date = item["published_at"][:10] if item["published_at"] else "—"
        lines.extend([
            f"### {item['priority']} ({item['score']}) — {item['vendor'].upper()} / {item['category_label']} / {item.get('release_stage', 'update')}",
            "",
            f"{date} {link}",
            "",
            f"- 設計観点: {item['design_perspective']}",
            f"- 運用観点: {item['operations_perspective']}",
            f"- Cross-cloud: {item['cross_cloud_context']}",
            f"- 次の行動: {item['recommended_action']}",
            "",
        ])
    lines.extend([
        "## 判定方式",
        "",
        "小型Naive Bayes分類器と期限・GA・セキュリティ等の明示ルールを併用し、設計・運用・cross-cloudの観点を付与する。最終判断はリンク先の公式情報で確認する。",
        "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=ROOT / "config/feed-sources.json")
    parser.add_argument("--training", type=Path, default=ROOT / "config/training-data.json")
    parser.add_argument("--rules", type=Path, default=ROOT / "config/analysis-rules.json")
    parser.add_argument("--perspectives", type=Path, default=ROOT / "config/cloud-perspectives.json")
    parser.add_argument("--output", type=Path, default=ROOT / "site/data/feed-digest.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "site/data/feed-digest.md")
    parser.add_argument("--per-source", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    digest = build_digest(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(digest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(to_markdown(digest), encoding="utf-8")
    print(
        f"wrote {len(digest['items'])} items from "
        f"{digest['summary']['source_success']}/{digest['summary']['source_total']} sources"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
