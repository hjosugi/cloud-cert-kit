<!-- i18n: language-switcher -->
[English](feed-intelligence.en.md) | [日本語](feed-intelligence.md)

# Feed Intelligence Architecture

## Purpose

Not only to list official releases from 4Clouds, but also to create a static digest that allows quick judgment of design changes, operational changes, and comparisons with other clouds. This is done without relying on always-on services or paid inference APIs, and is completed entirely on GitHub.

## Processing Flow

```text
AWS / Azure / GCP / OCI Official RSS/Atom
                  |
          GitHub Actions (Daily)
                  |
     XML parsing, normalization, deduplication
                  |
 Small Naive Bayes classifier + explicit rules
                  |
 stage / design impact / operational impact / comparison basis / next actions
                  |
 site/data/feed-digest.{json,md}
                  |
         GitHub Pages (static delivery)
```

## Reasons for Choosing a Small ML Model

- For short text classification into 8 categories, there's no need to constantly invoke large language models.
- Training data consists of a small set of representative sentences in `config/training-data.json`. Retraining occurs every millisecond.
- Can return reasoning as `signals`. For deadlines, deprecations, GA, etc., explicit rules override probabilistic judgments.
- Uses only Python standard library, so no dependency vulnerabilities or usage fees.

The classifier is not a "meaning-understanding LLM" but a primary screener that determines reading order. Category-specific templates assist in ensuring no comparison perspective is missed, but do not confirm feature equivalence or impact. Always verify official links, target resources, regions, and existing configurations.

## Scoring

Priority scores from 0 to 100 are calculated based on the following signals:

- Category probability from the classifier
- Match of category-specific keywords
- Urgent terms like deprecation, discontinuation, vulnerabilities
- High-interest terms like GA, new features, generative AI
- Match with security, deprecation, or currently focused technical areas
- Days since publication

Display thresholds: `72 or above = check immediately`, `52 or above = check within this week`, below that = `record only`. Thresholds and vocabulary can be modified in `config/analysis-rules.json`.

## Cost Model

| Item | Typical Cost |
|---|---:|
| GitHub Pages (public repository) | $0 |
| Daily GitHub Actions (a few minutes of Python) | Within standard limits for public repositories |
| ML inference | $0 (local calculation within Actions) |
| DB / API / Always-on server | None |

Since Actions and Pages costs/conditions may change on GitHub's side, verify the official Billing page at the start of operation and monthly.

## During Failures

If a single official feed fails, but previous JSON data contains entries for that cloud, it remains cached. Even if all feeds fail, the site can still display previous data if available. `source_status` indicates `ok / cached / error`.

## Local Execution

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_feed_digest.py
python3 -m http.server -d site 8000
```

Open `http://localhost:8000/` in a browser. Accessing via `file://` may cause JSON retrieval failures due to browser restrictions.

## Output Schema v2

In addition to normal classification and priority, each item stores:

- `release_stage`: preview / ga / deprecation / retirement / security / update
- `comparison_category`: a subcategory for comparing targeted technical areas even in deprecation info
- `design_perspective`: points of view for resource scope and control boundaries
- `operations_perspective`: inventory, default values, region, quota, metrics, cost, rollback
- `cross_cloud_context`: a basis for comparison that does not assert equivalence

## Future Expansion Criteria

No paid LLM will be added until the following conditions are met:

- Misclassification rates are measured with labeled data and cannot be resolved by rules/small classifiers.
- Confirmed that full-text summarization actually shortens decision-making time.
- Defined boundaries for monthly limits, caching, and no personal data transmission.

Even if needed later, only the top-scoring items will be summarized weekly in batch, avoiding full inference on all items.