<!-- i18n: language-switcher -->
[English](operations-comparison.md) | [日本語](operations-comparison.ja.md)

# Comparing multi-cloud operating models

The most dangerous operating assumption is that the same word implies the same responsibility boundary. Decompose terms such as monitoring, HA, backup, and policy.

## Telemetry

| Type | AWS | Azure | Google Cloud | OCI | Compare |
|---|---|---|---|---|---|
| Metrics | CloudWatch Metrics | Azure Monitor Metrics | Cloud Monitoring | Monitoring | Retention, dimensions/cardinality, custom-metric charges |
| Logs | CloudWatch Logs | Log Analytics Workspace | Cloud Logging | Logging | Ingestion, exclusion, and archive paths |
| Audit | CloudTrail | Activity Log + Entra audit | Cloud Audit Logs | Audit | Control/data planes and default read-event coverage |
| Config/compliance | AWS Config | Azure Policy | Asset Inventory / Organization Policy | Cloud Guard / Security Zones | Detection versus prevention |
| Tracing/APM | X-Ray / ADOT | Application Insights | Cloud Trace / OpenTelemetry | APM | Sampling and vendor-neutral export |

## Alert design

Standardize the policy, not the tool.

- **Page:** a user SLO is currently violated and an operator must act.
- **Ticket:** future risk, capacity, certificate expiry, or policy drift.
- **Log only:** forensic evidence, successful events, and change history.

Do not page directly from provider defaults. Lead with symptom alerts and use cause alerts as supporting evidence.

## Reading availability claims

| Check | Question |
|---|---|
| Resource scope | Is it zonal, regional, or global? |
| Replication | Is it synchronous or asynchronous, and who configures it? |
| Failover | Is it automatic or manual; what is the RTO; does the endpoint change? |
| Backup | Is it independent of the HA replica; is cross-region copy available? |
| Control plane | Does the existing data plane continue while APIs are unavailable? |
| Quota | Is capacity and quota reserved in the failover location? |
| Test | When did a production-equivalent recovery test last succeed? |

## Change management

Classify a release before applying it:

1. Provider-managed change: the platform applies it automatically.
2. Opt-in feature: the operator must enable it.
3. Default change: determine whether it affects new resources, existing resources, or both.
4. API or version retirement: migration must finish before a deadline.
5. Regional rollout: confirm that it has reached every target Region.

## Cost operations

- A common billing warehouse is useful, but allocation must respect each cloud's hierarchy.
- Compare commitments, instance flexibility, transfer, and operating work—not discount percentages alone.
- Include data gravity and consumer location in architecture decisions intended to reduce egress.
- Review retention, snapshots, public IPs, NAT, and data-processing charges as well as idle compute.

## Operator handoff template

| Field | Content |
|---|---|
| Owner | Service, team, and on-call rotation |
| User SLO | Availability, latency, and freshness |
| Dashboard | Golden signals plus business signals |
| Dependencies | Identity, network, data, and external APIs |
| Failure domains | Zone, Region, and global services |
| Rollback | Artifact, configuration, and data rollback |
| Backup restore | Date and result of the latest test |
| Quota | Current use, headroom, and failover-Region capacity |
| Break glass | Credential location, approval, and audit path |
| Provider releases | Subscribed feeds and responsible reviewer |
