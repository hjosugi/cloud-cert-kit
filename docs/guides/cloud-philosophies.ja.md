<!-- i18n: language-switcher -->
[English](cloud-philosophies.md) | [日本語](cloud-philosophies.ja.md)

# 4クラウドの思想を比較する

これは優劣表ではない。各社の公式landing zone、resource hierarchy、Well-Architected guidanceから、設計時に現れやすい傾向を抽出したもの。個々のserviceは例外を持つため、最終判断はresource scopeとSLAを確認する。

## 一枚比較

| 観点 | AWS | Azure | Google Cloud | OCI |
|---|---|---|---|---|
| 出発点 | 小さいビルディングブロックを組み合わせる | エンタープライズコントロールプレーンへワークロードを載せる | グローバルインフラとマネージドプラットフォームを活用する | データベース・エンタープライズワークロードを明確な区画で動かす |
| 主要な隔離単位 | アカウント | サブスクリプション | プロジェクト | コンパートメント |
| 上位階層 | 組織→OU→アカウント | Entraテナント→管理グループ→サブスクリプション→リソースグループ | 組織→フォルダ→プロジェクト | テナンシー→ネストされたコンパートメント |
| 統制 | SCP、コントロールタワー、Config | Azure Policy、管理グループ、Landing Zone | 組織ポリシー、階層的ファイアウォール、IAM拒否 | IAMポリシー、セキュリティゾーン、クォータ |
| アイデンティティの癖 | リソースポリシーとアイデンティティポリシーの両面 | Entra IDとAzure RBACの二層 | プリンシパル＋ロールバインディング、リソース階層継承 | subjectが何をどこでできるかをpolicy文で表す |
| ネットワークの癖 | VPCはリージョナル、サブネットはAZ。サービスごとのエンドポイント設計 | VNetはリージョナル、ARM/Entra/Policyとのエンタープライズ統合 | グローバル／リージョナルリソースが混在。グローバルLBとプロジェクト設計が強い | VCNはリージョナル、DRG／コンパートメントとエンタープライズネットワークを構成 |
| 信頼性の癖 | フェイラー隔離をアカウント／AZ／リージョンへ明示的に組む | ゾーン／リージョンに加え中央プラットフォーム運用との整合 | SLO、エラーバジェット、グローバルトラフィック、マネージドデータを重視 | 可用性ドメイン／フォールトドメインとDBサービス特性を明示 |
| 運用の中心 | CloudWatch、CloudTrail、Config、Systems Manager | Azure Monitor、Activity Log、Policy、Defender | Cloud Monitoring／Logging／Trace、SREプラクティス | Monitoring、Logging、Audit、Cloud Guard |
| 設計者への問い | どのアカウント・リージョン・サービス責任境界に置くか | どのテナント／MG／サブスクリプションポリシーで統制するか | ユーザーエクスペリエンスのSLOとグローバル／リージョナルスコープは何か | どのコンパートメント・AD／FD・DB構成に置くか |

## AWS: composable primitivesとアカウント隔離

AWSはサービスごとの責任境界が明確で、IAM、ネットワーク、イベント、ストレージを組み合わせてアーキテクチャを作る傾向が強い。自由度が高いぶん、アカウントのベンディング、中央ログ収集、ガードレールを先に作らないと構成差が拡大する。

設計時の観点:

- プロダクション／ノンプロダクション、セキュリティ、ログアーカイブ、ネットワークをアカウントで分離する。
- OUは組織図ではなく、共通コントロールとセキュリティ／運用ニーズで作る。
- VPCエンドポイント、リソースポリシー、KMSキーのポリシーのようにデータパスと認可をサービスごとに確認する。
- マネージドサービスでもマルチAZ／マルチリージョンの責任範囲はサービスごとに違う。

公式: [AWSマルチアカウント設計原則](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/design-principles-for-your-multi-account-strategy.html)

## Azure:エンタープライズ階層とポリシードリブンガバナンス

AzureはMicrosoft Entraテナント、管理グループ、サブスクリプション、Azureリソースマネージャーを軸に、エンタープライズ全体のアイデンティティ・ポリシー・ハイブリッド環境を統制する思想が強い。サブスクリプションは請求だけでなく、ポリシー、クォータ、管理境界でもある。

設計時の観点:

- プラットフォームlanding zoneとアプリケーションlanding zoneを分ける。
- 管理グループ階層は組織図のコピーではなく、同じポリシーを必要とするワークロードタイプでまとめる。
- Azure Policyでガードレールを配りつつ、サブスクリプションのベンディングでワークロードチームへ自治を渡す。
- EntraディレクトリロールとAzure RBACロールを混同しない。

公式: [Azure landing zone設計原則](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-principles)

## Google Cloud:プロジェクト境界、グローバルプラットフォーム、SRE

Google CloudはプロジェクトをAPI、クォータ、請求、IAMの実務単位として扱い、Organization／Folderからポリシーを継承する。グローバルリソースとリージョナルリソースが混在し、データ／分析、Kubernetes、グローバルロードバランシング、SREの考え方がアーキテクチャへ入りやすい。

設計時の観点:

- プロジェクトを単なるリソースグループとして扱わず、ライフサイクル・クォータ・IAM・請求境界として設計する。
- リソースがゾーン／リージョン／グローバル／マルチリージョンのどれかを最初に確認する。
- 可用性ではサービス稼働だけでなく、ユーザーフェイシングのSLI/SLOとデータ正確性を定義する。
- 階層は組織図よりポリシー、環境、チームの自治から決める。

公式: [Google Cloudリソース階層](https://docs.cloud.google.com/architecture/landing-zones/decide-resource-hierarchy) / [信頼性の柱](https://docs.cloud.google.com/architecture/framework/reliability)

## OCI:コンパートメントガバナンスとデータベース中心のエンタープライズ

OCIはテナンシー内をネストされたコンパートメントで区画化し、IAMポリシー、クォータ、ネットワーク、セキュリティ、コストの運用境界を作る。Oracle Databaseや既存のエンタープライズシステムとの接続で、性能・ライセンス・データレジデンシーを明示的に扱いやすい。

設計時の観点:

- コンパートメントをフォルダではなく、IAM／運用／クォータ境界として扱う。
- ポリシーの動詞 (`inspect/read/use/manage`) とリソースタイプ、ロケーションを読む。
- リージョン、アベイラビリティドメイン、フォールトドメインの組み合わせを確認する。
- DBサービス固有のHA／バックアップ／DR責任とアプリケーション層を分けて考える。

公式: [OCIクラウド導入フレームワーク](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/home.htm) / [OCIコアランディングゾーン](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/oci-core-landing-zone.htm)

## 同等サービス比較で必ず見る5点

1. リソーススコープ：グローバル／リージョナル／ゾーン
2. 隔離境界：アカウント／サブスクリプション／プロジェクト／コンパートメント
3. コントロールの継承：上位ポリシーがどう継承・拒否されるか
4. データプレーンの障害：コントロールプレーン停止時も既存トラフィックが流れるか
5. オペレーター責任範囲：パッチ、バックアップ、スケーリング、フェイルオーバーのどこまで管理されているか

名前が似ていても、この5点が違えば移植時のアーキテクチャは同じにならない。