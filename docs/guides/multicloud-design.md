<!-- i18n: language-switcher -->
[English](multicloud-design.md) | [日本語](multicloud-design.ja.md)

# Multi-cloud design decision guide

Do not aim for an identical topology in every cloud. Standardize business requirements, then choose a native implementation in each provider.

## Design sequence

### 1. Why use more than one cloud?

| Reason | Defensible design | Dangerous design |
|---|---|---|
| Regulation or data residency | Partition workloads and data explicitly by geography and provider | Replicate all data everywhere at all times |
| M&A or existing investment | Integrate identity, observability, and governance incrementally | Standardize every platform first |
| Best of breed | Select providers by bounded capability and define contracts | Scatter individual services without ownership boundaries |
| Outage risk | Design alternate paths for the business process | Assume cross-cloud database synchronization automatically creates safety |
| Commercial leverage | Identify the layers that genuinely need portability | Reduce everything to the lowest common feature set |

Active-active multi-cloud chosen only for “cloud outage protection” usually adds more consistency, identity, network, testing, and operating complexity than the availability benefit justifies.

### 2. Standardize these outcomes

- Business SLO, RTO, and RPO.
- Data classification and retention.
- Identity lifecycle and break-glass principles.
- Telemetry schema, incident severity, and ownership.
- IaC review, artifact provenance, and release approval.
- Decision criteria recorded in ADRs.

### 3. Keep these cloud-native

- IAM policy languages.
- Network topology and private service access.
- Managed-database HA and backup mechanisms.
- Autoscaling signals and quotas.
- Audit-log categories.
- Service-specific failover procedures.

## Six decision axes

| Axis | Common question | AWS | Azure | Google Cloud | OCI |
|---|---|---|---|---|---|
| Organization | What is the isolation, quota, and billing unit? | Account / OU | Subscription / management group | Project / folder | Compartment |
| Identity | How do humans and workloads authenticate? | Roles / IAM Identity Center | Managed identities / Entra | Service accounts / WIF | Dynamic groups / resource principals |
| Network | What is the scope and transit-routing model? | VPC / TGW | VNet / vWAN | VPC / NCC | VCN / DRG |
| Data | What are the consistency, location, and DR guarantees? | Service-specific | Service-specific | Broad global managed-data portfolio | Oracle Database-centered choices |
| Operations | Where are logs, metrics, and change evidence? | CloudWatch / CloudTrail / Config | Monitor / Activity Log / Policy | Operations suite / Cloud Audit Logs | Monitoring / Logging / Audit |
| Governance | How do inherited denies and exceptions work? | SCP + resource policies | Policy + RBAC | Organization Policy + IAM deny | IAM policies + Security Zones |

## ADR template

```markdown
# ADR-NNN: <decision>

## Business outcome
- User impact / compliance / deadline

## Measurable requirements
- SLO:
- RTO / RPO:
- Data residency:
- Expected load:
- Cost ceiling:

## Cloud-specific facts
- Resource scope:
- Failure domains:
- Identity boundary:
- Data-plane behavior during a control-plane outage:
- Quotas and regional availability:

## Options
| Option | Reliability | Security | Operations | Cost | Lock-in |

## Decision and consequences
- Selected option:
- Accepted risk:
- Validation test:
- Exit criteria:
```

## Three levels of portability

1. Operational portability: operate to the same SLO, dashboard vocabulary, and incident process.
2. Deployment portability: share IaC or module interfaces while keeping the internal resources cloud-native.
3. Runtime portability: run the same container, VM, or application in another cloud.

Prioritize level 1, apply level 2 where it pays for itself, and require level 3 only for workloads with a concrete exit requirement.
