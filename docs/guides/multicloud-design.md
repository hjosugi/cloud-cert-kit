<!-- i18n: language-switcher -->
[English](multicloud-design.md) | [日本語](multicloud-design.ja.md)

# マルチクラウド設計判断ガイド

「全cloudで同じ構成」を目標にしない。business requirementを共通化し、各cloudではnativeな実装を選ぶ。

## 設計の順序

### 1. なぜ複数cloudか

| 理由 | 妥当な設計 | 危険な設計 |
|---|---|---|
| 規制・data residency | workload/dataを地域・provider境界で明示分割 | 全dataを常時相互複製 |
| M&A・既存投資 | identity、observability、governanceを段階統合 | 最初から全platformを共通化 |
| best-of-breed | capability単位でproviderを選びcontractを定義 | serviceごとに無秩序に分散 |
| outage risk | business processの代替経路を設計 | databaseを異種cloud間で同期すれば安全と考える |
| commercial leverage | portabilityの高い層を選別 | すべてを最低共通機能へ落とす |

「cloud障害対策」だけを理由にactive-active multi-cloudを選ぶと、通常はdata consistency、identity、network、test、operationの複雑性が可用性利益を上回る。

### 2. 共通化するもの

- business SLO / RTO / RPO
- data classificationとretention
- identity lifecycleとbreak-glass原則
- telemetry schema、incident severity、ownership
- IaC review、artifact provenance、release approval
- ADRのdecision criteria

### 3. cloud nativeに残すもの

- IAM policy language
- network topologyとprivate service access
- managed database HA/backup mechanism
- autoscaling signalとquota
- audit log category
- service-specific failover procedure

## 6つの設計軸

| 軸 | 共通質問 | AWS | Azure | GCP | OCI |
|---|---|---|---|---|---|
| Organization | 隔離・quota・billing単位は？ | account/OU | subscription/MG | project/folder | compartment |
| Identity | workload identityと人のaccessは？ | role/Identity Center | managed identity/Entra | service account/WIF | dynamic group/resource principal |
| Network | scopeとtransitive routingは？ | VPC/TGW | VNet/vWAN | VPC/NCC | VCN/DRG |
| Data | consistency、location、DRは？ | service別 | service別 | global managed dataが豊富 | Oracle DB選択肢が中心 |
| Operations | log、metric、change evidenceは？ | CloudWatch/CloudTrail/Config | Monitor/Activity Log/Policy | Operations suite/Cloud Audit Logs | Monitoring/Logging/Audit |
| Governance | 上位denyとexceptionは？ | SCP+resource policy | Policy+RBAC | Org Policy+IAM deny | IAM policy+Security Zones |

## ADR template

```markdown
# ADR-NNN: <decision>

## Business outcome
- user impact / compliance / deadline

## Measurable requirements
- SLO:
- RTO/RPO:
- data residency:
- expected load:
- cost ceiling:

## Cloud-specific facts
- resource scope:
- failure domains:
- identity boundary:
- data plane behavior during control plane failure:
- quota and regional availability:

## Options
| Option | Reliability | Security | Operations | Cost | Lock-in |

## Decision and consequences
- chosen option:
- accepted risks:
- validation test:
- exit criteria:
```

## portabilityの3段階

1. Operational portability: 同じSLO、dashboard、incident processで運用できる。
2. Deployment portability: IaC/module interfaceは共通だが、内部resourceはcloud native。
3. Runtime portability: container/VM/applicationが別cloudでも動く。

通常は1を最優先し、2を必要な範囲で行い、3は明確なexit requirementがあるworkloadだけに適用する。
