<!-- i18n: language-switcher -->
[English](service-and-cost-comparison.md) | [日本語](service-and-cost-comparison.ja.md)

# 用途検索と費用比較の方法

## 用途から探す

サービス名を知っていることを前提にしない。最初に「何を実現するか」を選び、4クラウドの候補と次の確認事項を表示する。

1. resource scopeとisolation boundary
2. availability、replication、failover
3. identityとprivate access
4. operatorが担当するpatch、backup、scaling、upgrade
5. 課金meterと無料枠・commitmentの適用条件

カタログは候補を絞るための入口であり、セル内のサービスが完全互換という意味ではない。

## 費用比較のレベル

| Level | 揃えるもの | 揃わないもの |
|---|---|---|
| capacity-match | vCPU、memory、稼働時間、台数 | CPU世代、burst、network、disk性能 |
| durability-intent-match | access tier、location、zone障害への意図、容量 | durability値、request unit、data transfer、復旧機能 |
| workload benchmark | 実データ、同じSLO、load test、運用手順 | provider固有の実装差は残る |

サイトの金額は最初の2段階まで。採用判断には3段階目のbenchmarkが必要。

## 計算式

### Linux VM baseline

```text
monthly compute = public hourly rate × instance count × running hours
```

2 vCPU・8 GiBの公開On-Demand/Pay-as-you-go単価を使用する。disk、public IPv4、load balancer、network、monitoring、backupは含めない。

### Hot object storage baseline

```text
monthly storage = public storage rate × stored GB/GiB-month
```

request、retrieval、versioning、soft delete、replication、egressは含めない。AzureはLRSではなくZRSを使い、単一location内のzone障害を意識した比較に寄せる。

## 単価の管理

- 基準日、currency、region、SKU、formula、公式sourceを`site/data/cost-baselines.json`へ保存する。
- 単価変更はsourceとchecked dateを同時に更新する。
- 最安値を推奨理由にしない。性能、SLO、運用工数、既存skill、data gravityを含める。
- 契約割引やprivate offerは公開単価と分け、組織固有の比較表で上書きする。

## 最終見積もり

サイトの概算後、各社公式calculatorへ同じ要件を入力する。

- [AWS Pricing Calculator](https://calculator.aws/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)
- [OCI Cost Estimator](https://www.oracle.com/cloud/costestimator.html)
