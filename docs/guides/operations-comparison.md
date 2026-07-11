<!-- i18n: language-switcher -->
[English](operations-comparison.md) | [日本語](operations-comparison.ja.md)

# マルチクラウド運用モデル比較

運用で最も危険なのは、同じ単語を同じ責任範囲だと思うこと。`monitoring`、`HA`、`backup`、`policy`の中身を分解する。

## telemetry

| 種別 | AWS | Azure | GCP | OCI | 比較時の注意 |
|---|---|---|---|---|---|
| metrics | CloudWatch Metrics | Azure Monitor Metrics | Cloud Monitoring | Monitoring | retention、dimension/cardinality、custom metric料金 |
| logs | CloudWatch Logs | Log Analytics Workspace | Cloud Logging | Logging | ingestion/exclusion/archive経路 |
| audit | CloudTrail | Activity Log + Entra audit | Cloud Audit Logs | Audit | control/data plane、read eventのdefault |
| config/compliance | AWS Config | Azure Policy | Asset Inventory/Org Policy | Cloud Guard/Security Zones | detectとdenyを区別 |
| trace/APM | X-Ray / ADOT | Application Insights | Cloud Trace/OpenTelemetry | APM | trace samplingとvendor-neutral export |

## alert設計

共通化するのはtoolではなくalert policy。

- page: user SLOを現在侵害しており、operator actionが必要
- ticket: 将来risk、capacity、certificate expiry、policy drift
- log only: forensic evidence、成功event、変更履歴

provider default alertをそのままpageへ送らない。症状alertを主、原因alertを補助にする。

## availabilityを読む

| 確認項目 | 質問 |
|---|---|
| resource scope | zonal/regional/globalのどれか |
| replication | sync/async、誰が構成するか |
| failover | automatic/manual、RTO、endpoint変化 |
| backup | HA replicaと独立しているか、cross-region copyはあるか |
| control plane | API停止中にexisting data planeは継続するか |
| quota | failover先にcapacity/quotaがあるか |
| test | production相当のrecovery testをいつ実行したか |

## change management

releaseを適用する前に次を分ける。

1. provider-managed change: platform側で自動適用
2. opt-in feature: operatorが有効化
3. default change: 新規resourceだけか既存resourceも変わるか
4. API/version retirement: deadlineまでにmigrationが必要
5. regional rollout: target Regionへ到達済みか

## cost operations

- billing exportを共通warehouseへ集めても、allocation unitは各cloudのhierarchyに合わせる。
- discount modelを単純比較しない。commitment term、instance flexibility、data transfer、managed operationを含める。
- egress削減のためにdata gravityとconsumer locationをarchitecture decisionへ含める。
- idle resource削除だけでなく、log retention、snapshot、public IP、NAT/data processing chargeを確認する。

## operator handoff template

| 項目 | 内容 |
|---|---|
| owner | service/team/on-call |
| user SLO | availability/latency/freshness |
| dashboard | golden signals + business signal |
| dependencies | identity/network/data/external API |
| failure domains | zone/region/global service |
| rollback | artifact/config/data rollback |
| backup restore | last tested date and result |
| quota | current/headroom/failover Region |
| break glass | credential location, approval, audit |
| provider release | subscribed feeds and review owner |
