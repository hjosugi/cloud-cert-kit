<!-- i18n: language-switcher -->
[English](service-and-cost-comparison.md) | [日本語](service-and-cost-comparison.ja.md)

# 用途検索と費用比較の方法

## 用途から探す

サービス名を知っていることを前提にしない。最初に「何を実現するか」を選び、4クラウドの候補と次の確認事項を表示する。

1. resource scopeとisolation boundary
2. 可用性、レプリケーション、フェイルオーバー
3. アイデンティティとプライベートアクセス
4. オペレーターが担当するパッチ、バックアップ、スケーリング、アップグレード
5. 課金メーターと無料枠・コミットメントの適用条件

カタログは候補を絞るための入口であり、セル内のサービスが完全互換という意味ではない。

## 費用比較のレベル

| レベル | 揃えるもの | 揃わないもの |
|---|---|---|
| capacity-match | vCPU、メモリ、稼働時間、台数 | CPU世代、バースト、ネットワーク、ディスク性能 |
| durability-intent-match | アクセス層、ロケーション、ゾーン障害への意図、容量 | 耐久性値、リクエストユニット、データ転送、復旧機能 |
| workload benchmark | 実データ、同じSLO、負荷テスト、運用手順 | プロバイダー固有の実装差は残る |

サイトの金額は最初の2段階まで。採用判断には3段階目のベンチマークが必要。

## 計算式

### Linux VM ベースライン

```text
月間コンピュート = 公開時間単価 × インスタンス数 × 稼働時間
```

2 vCPU・8 GiBの公開オンデマンド/従量課金単価を使用する。ディスク、パブリックIPv4、ロードバランサー、ネットワーク、監視、バックアップは含めない。

### ホットオブジェクトストレージ ベースライン

```text
月間ストレージ = 公開ストレージレート × 保存GB/GiB-月
```

リクエスト、リトリーブ、バージョニング、ソフトデリート、レプリケーション、イーグレスは含めない。AzureはLRSではなくZRSを使い、単一ロケーション内のゾーン障害を意識した比較に寄せる。

## 単価の管理

- 基準日、通貨、リージョン、SKU、計算式、公式ソースを`site/data/cost-baselines.json`へ保存する。
- 単価変更はソースと確認日を同時に更新する。
- 最安値を推奨理由にしない。性能、SLO、運用工数、既存スキル、データの重力を含める。
- 契約割引やプライベートオファーは公開単価と分け、組織固有の比較表で上書きする。

## 最終見積もり

サイトの概算後、各社公式計算ツールへ同じ要件を入力する。

- [AWS Pricing Calculator](https://calculator.aws/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)
- [OCI Cost Estimator](https://www.oracle.com/cloud/costestimator.html)