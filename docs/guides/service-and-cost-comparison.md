<!-- i18n: language-switcher -->
[English](service-and-cost-comparison.md) | [日本語](service-and-cost-comparison.ja.md)

# Service discovery and cost comparison

## Search by purpose

Do not assume that the reader already knows a product name. Start from the outcome, then compare candidates in all four clouds against:

1. Resource scope and isolation boundary.
2. Availability, replication, and failover.
3. Identity and private access.
4. Operator-owned patching, backup, scaling, and upgrades.
5. Billing meters and eligibility for free tiers or commitments.

The catalog narrows the search. Services in the same row are not guaranteed to be interchangeable.

## Levels of cost comparison

| Level | Normalized | Still different |
|---|---|---|
| Capacity match | vCPU, memory, running hours, instance count | CPU generation, burst model, network, and disk performance |
| Durability-intent match | Access tier, location, zone-failure intent, capacity | Durability figures, request units, transfer, and recovery features |
| Workload benchmark | Real data, common SLO, load test, operating procedure | Provider-specific implementation differences remain |

The public site supports the first two levels. A purchase decision requires the third.

## Formulas

### Linux VM baseline

```text
monthly compute = public hourly rate × instance count × running hours
```

The comparison uses public on-demand/pay-as-you-go prices for 2 vCPU and 8 GiB. It excludes disks, public IPv4, load balancers, networking, monitoring, and backup.

### Hot object-storage baseline

```text
monthly storage = public storage rate × stored GB/GiB-month
```

It excludes requests, retrieval, versioning, soft delete, replication, and egress. Azure uses ZRS rather than LRS to align the baseline with protection from a zone failure inside one location.

## Maintaining price data

- Store the reference date, currency, Region, SKU, formula, and official source in `site/data/cost-baselines.json`.
- Update the source and verification date with every price change.
- Never recommend the lowest list price without performance, SLO, operating work, existing skills, and data gravity.
- Keep contract discounts and private offers outside the public baseline and apply them in an organization-specific comparison.

## Final estimate

After the site estimate, enter the same requirements in each official calculator:

- [AWS Pricing Calculator](https://calculator.aws/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)
- [OCI Cost Estimator](https://www.oracle.com/cloud/costestimator.html)
