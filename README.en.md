<!-- i18n: language-switcher -->
[English](README.en.md) | [日本語](README.md)

# cloud-hub

A multi-cloud design and operation site to understand AWS / Azure / Google Cloud / OCI not by service names, but by differences in **philosophy, resource boundaries, failure domains, and operator responsibilities**.

- Public site: https://hjosugi.github.io/cloud-hub/ (selects Japanese / English from the browser language)
- Japanese: https://hjosugi.github.io/cloud-hub/cloud-hub.html
- English: https://hjosugi.github.io/cloud-hub/cloud-hub.en.html
- Latest Release: https://github.com/hjosugi/cloud-hub/releases/latest
- Repository: https://github.com/hjosugi/cloud-hub

## What can you understand

- What each cloud primarily isolates and controls
- How global/regional scope, IAM, high availability, and operational responsibilities differ even for equivalent services
- How to compare organization, network, identity, data, observability, disaster recovery, and costs
- How to find candidate clouds based on purpose and requirements without knowing service names
- How to compare published prices under the same capacity, uptime, and redundancy conditions
- What architecture, runbook, quota, and migration aspects are emphasized in official releases
- How to connect knowledge gained from certifications to real-world design decisions

## Design and operational guides

1. [Philosophies of the 4 clouds](docs/guides/cloud-philosophies.md)
2. [Multi-cloud design decision-making](docs/guides/multicloud-design.md)
3. [Operational model comparison](docs/guides/operations-comparison.md)
4. [How to read releases](docs/guides/release-intelligence.md)
5. [Purpose search and cost comparison](docs/guides/service-and-cost-comparison.md)

## Site information architecture

| Section | Purpose |
|---|---|
| Release Observation | Read official updates with design, operation, and cross-cloud perspectives |
| Cloud Philosophies | Compare boundary, control, and reliability philosophies of the 4 providers |
| Service Comparison | Map not only feature names but also purposes and responsibility scopes |
| Cost Comparison | Check published baseline prices and excluded items under the same input conditions |
| Network / IAM | Compare scopes, inheritance, and routing that are often confused |
| Operation Comparison | Standardize telemetry, audit, availability, and alerting language |
| Certifications & Learning | Supplement practical understanding with AIP-C01/PDE training materials |

## Release and intelligence

Official RSS/Atom feeds from the 4 clouds are fetched daily via GitHub Actions, and a lightweight Naive Bayes classifier with explicit rules assigns:

- Stage such as Preview / GA / Retirement / Security
- Impact on design
- Impact on operations
- Notes on areas covered by other clouds and points to watch during comparison
- Next steps for migration and verification

```text
Official feed
    ↓
GitHub Actions
    ↓
Classification / Stage determination / Cloud perspective
    ↓
Static JSON / Markdown
    ↓
GitHub Pages
```

No always-on servers, databases, paid AI APIs, or public CORS proxies are used. For details, see [Feed intelligence architecture](docs/feed-intelligence.en.md).

## Certifications and learning as an auxiliary layer

- [AIP-C01 Domain Guide](docs/learning/aip-c01/domain-guide.md)
- [AIP-C01 Flashcards](docs/learning/aip-c01/flashcards.md)
- [AIP-C01 Scenario Exercises](docs/learning/aip-c01/scenario-drills.md)
- [GCP PDE Domain 1 condensed notes](docs/learning/gcp-pde/domain-1-notes.en.md)
- [Review only incorrect questions](docs/learning/README.en.md)

Don’t just stop at obtaining certifications—connect the judgment criteria of each question to the design and operations guides.

## Structure

```text
cloud-hub/
├── docs/
│   ├── guides/                    Multi-cloud design and operation comparison
│   ├── learning/                  Certification materials, mock exam notes, mistake records
│   └── feed-intelligence.md       Release analysis design
├── site/index.html                 Automatic language-selection entry point
├── site/cloud-hub.html             Japanese GitHub Pages site
├── site/cloud-hub.en.html          English GitHub Pages site
├── site/data/service-catalog.json  Purpose-based candidate clouds
├── site/data/cost-baselines.json   Configuration, unit prices, formulas, official sources
├── config/cloud-perspectives.json  Cloud philosophies and corresponding domains
├── scripts/build_feed_digest.py    Official release analysis
└── tests/                          Feed and content verification
```

## Local setup

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_feed_digest.py
python3 -m http.server -d site 8000
```

Open `http://localhost:8000/`.

Reference date: 2026-07-23. Final judgments on specifications and SLAs should be based on each cloud’s official documentation.
