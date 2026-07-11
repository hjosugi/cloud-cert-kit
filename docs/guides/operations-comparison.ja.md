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

共通化するのはツールではなくアラートポリシー。

- page: ユーザーSLOを現在侵害しており、オペレーターの対応が必要
- ticket: 将来リスク、容量、証明書期限、ポリシードリフト
- log only: フォレンジック証拠、成功イベント、変更履歴

プロバイダーのデフォルトアラートをそのままページへ送らない。症状アラートを主、原因アラートを補助にする。

## availabilityを読む

| 確認項目 | 質問 |
|---|---|
| resource scope | ゾーン/リージョン/グローバルのどれか |
| replication | 同期/非同期、誰が構成するか |
| failover | 自動/手動、RTO、エンドポイント変化 |
| backup | HAレプリカと独立しているか、クロスリージョンコピーはあるか |
| control plane | API停止中に既存データプレーンは継続するか |
| quota | フェイルオーバー先に容量/クォータがあるか |
| test | 本番相当のリカバリテストをいつ実行したか |

## change management

リリース適用前に次を分ける。

1. provider-managed change: プラットフォーム側で自動適用
2. opt-in feature: オペレーターが有効化
3. default change: 新規リソースだけか既存リソースも変わるか
4. API/バージョン廃止: デッドラインまでにマイグレーションが必要
5. regional rollout: 対象リージョンへ到達済みか

## cost operations

- 請求エクスポートを共通の倉庫へ集めても、割当単位は各クラウドの階層に合わせる。
- 割引モデルを単純比較しない。コミットメント期間、インスタンスの柔軟性、データ転送、管理運用を含める。
- egress削減のためにデータの重力とコンシューマーの場所をアーキテクチャの決定に含める。
- アイドルリソースの削除だけでなく、ログ保持、スナップショット、パブリックIP、NAT/データ処理料金も確認する。

## operator handoff template

| 項目 | 内容 |
|---|---|
| owner | サービス/チーム/オンコール |
| user SLO | 可用性/レイテンシ/新鮮さ |
| dashboard | ゴールデンシグナル + ビジネスシグナル |
| dependencies | アイデンティティ/ネットワーク/データ/外部API |
| failure domains | ゾーン/リージョン/グローバルサービス |
| rollback | アーティファクト/設定/データのロールバック |
| backup restore | 最終テスト日と結果 |
| quota | 現在/余裕/フェイルオーバーリージョン |
| break glass | 認証情報の場所、承認、監査 |
| provider release | 購読フィードとレビュー担当者 |