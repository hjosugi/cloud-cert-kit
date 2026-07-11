<!-- i18n: language-switcher -->
[English](domain-1-notes.en.md) | [日本語](domain-1-notes.md)

# PDE Domain 1: Design Data Processing Systems — 50問圧縮ノート

対象: Udemy模試 Domain 1 (Architecture & Planning) 50問
方針: 全問を「要件キーワード → 正解パターン」に還元。本番は要件語の即応で7割決まる。
基準日: 2026-07

---

## 0. 出題側の思考回路 (これだけで消去法が効く)

1. **Managed > self-managed**。Jenkins/Atlas/Hadoop/Vault を GKE/GCE に自前構築する選択肢はほぼ常に不正解。
2. **Native機能 > 自作**。Cloud Functions + Firestore で自作オーケストレーション/自作リネージ/自作削除ジョブは不正解。
3. **要件の数字が答えを固定する**。RPO=0 → active-active。帯域1Gbps+期限 → オフライン転送。50k writes/s → Bigtable/Spanner。
4. **「業務ユーザーが」「経験の浅いチームが」= 低運用負荷のマネージドを選べ**の合図。
5. 2択問題は「実装の柱」+「可視化/監査の柱」の組み合わせが多い (例: 検証パイプライン + ダッシュボード)。

---

## 1. 要件キーワード → 即応表

| 要件キーワード | 答え |
|---|---|
| グローバル + ACID + 99.999% + 即時可視 | Spanner multi-region (external consistency) |
| 大量書き込みKV/時系列 + 1桁ms + 強整合不要 + 低コスト | Bigtable (row key設計) |
| 単一リージョンでよいPostgreSQL強化 | AlloyDB (※グローバル要件が出たら即除外) |
| OLTP + リアルタイム分析を単一DBで | Spanner + change streams → BigQuery |
| 帯域不足 (1Gbps) + 数百TB + 期限 | Transfer Appliance (NFS/SMB対応) |
| DB移行 + ダウンタイム最小 (分単位) | Database Migration Service (継続CDC) |
| Teradata → BigQuery | BigQuery Data Transfer Service |
| 不良レコードの隔離 + リプレイ | Dataflow side outputs + エラーバケット/DLQ |
| exactly-once / 冪等 | BigQuery MERGE (一意キー) + Dataflow exactly-once sink |
| 複雑依存 + データ到着待ち + リトライ + リネージ | Cloud Composer (sensors + Dataplex Lineage) |
| 単純ワークフロー + 宣言的 + 低運用 | Cloud Workflows (YAML) |
| CI/CD | Cloud Build + テスト + 承認ゲート + Terraform |
| Googleが復号できないこと | Cloud EKM (外部鍵: Thales/Fortanix) |
| 即時失効 / 環境の暗号分離 | CMEK + 環境別 key ring + Audit Logs |
| データ持ち出し(exfiltration)防止 | VPC Service Controls perimeter (+access levelsで例外) |
| 公衆インターネット禁止 | Private Google Access + 外部IPなし + VPC-SC |
| PII自動検出・仮名化 | Cloud DLP (infoTypes / FPE de-identification) |
| 列単位のアクセス制御 | policy tags (column-level security) + Fine-Grained Reader |
| 再識別不能の数学的証明 | 差分プライバシー (ε, δ + privacy budget) |
| 統合ガバナンス + ドメイン所有 + 自動分類 | Dataplex (lakes/zones + DLP統合 + zone IAM) |
| 横断検索 + タグ + リネージ | Data Catalog (+ Lineage API) |
| 組織/プロジェクト間の統制されたデータ共有 | Analytics Hub / authorized views |
| コスト: 時系列テーブル | partitioning + clustering + partition expiration |
| コスト: ダッシュボード高頻度クエリ | BI Engine + materialized views |
| ワークロード分離 + 性能保証 | BigQuery Editions + 別reservation + priority |
| アクセス管理のスケール (数百人) | Google Groups + dataset-level role + HR連携自動化 |
| 保持期限後の自動削除 | GCS Lifecycle + BQ table/partition expiration |
| PITR + 本番影響なしバックアップ | Cloud SQL automated backups + binary logging |
| ロックイン回避 / マルチクラウド | open format (Parquet/Iceberg/Delta) + OSSエンジン (Spark/Trino) |
| データレイク + スキーマ進化 + in-place分析 | GCS (Parquet/Avro) + zones + Dataproc + BQ external tables |
| ストリーミングのスキーマ進化 | Schema Registry + Avro + BQ schema relaxation |
| residency (地域内保持) | dataset/bucket location + Org Policy (location制約) + VPC-SC |
| RPO=0 / RTO<60s | active-active (Pub/Sub複製 + 並行パイプライン + Spanner + dedup) |
| RTO 15分 / RPO 5分 + 低コスト | ウォームスタンバイ (テンプレ + IaC自動デプロイ + スナップショット) |
| DRの規制向け証跡 | 本番同等ステージング + 月次drill + Monitoring計測 |

---

## 2. 50問 一行要約

| # | シナリオ要点 | 正解 | 決め手 |
|---|---|---|---|
| 1 | Dataflow 50本のCI/CD (2択) | Terraform IaC+lint+テンプレ検証 / Cloud Build+単体・統合テスト+順次デプロイ+承認ゲート | IaCで構成をレビュー可能に、テストとゲートで本番事故防止 |
| 2 | RTO15分/RPO5分/低コスト | テンプレ+Terraform自動デプロイ+Pub/Sub複製+5分BQスナップショット | active-activeはコスト過剰、手動はRTO未達 → ウォーム |
| 3 | 配車: 残高=強整合、履歴=結果整合 | Spanner multi-region + クリティカルは強整合 + 非クリティカルはbounded staleness読み + リードレプリカ | 整合性要件をデータ種別ごとに使い分け |
| 4 | 50k TPS/グローバル/ACID/99.999% | Spanner multi-region | この4条件同時 = Spanner一択 |
| 5 | Cloud SQLデッドロック+分析24h遅延 | Spanner + interleaved + change streams → BQ | 単一DBでOLTP+リアルタイム分析 = change streams |
| 6 | 1000万件/日 品質検証+隔離+パートナー別レポート | Dataflow検証 → valid:BQ / invalid:GCS+理由 + Logging集計 + ダッシュボード | CFはタイムアウト、BQ制約はロード全体が失敗 |
| 7 | 複雑依存+到着待ち+リトライ+リネージ | Cloud Composer + sensors + Dataplex Lineage | sensorsとDAGが要件に直結 |
| 8 | 部門別共有+細粒度+監査 (2択) | Analytics Hub / authorized views + audit logs | 基表を隠して必要分だけ。エクスポート複製は不正解 |
| 9 | HIPAA (鍵管理+residency+監査) | CMEK + 単一リージョン + Audit Logs + VPC-SC + **BAA** | BAA締結が入っている選択肢を選ぶ |
| 10 | Google復号不可+90日ローテ+即時失効 (2択) | EKM / Cloud Audit Logs | 「Googleが技術的に触れない」= EKMのみ。CMEKでは不足 |
| 11 | 開発でPHIを使わずリアルなテストデータ | DLP de-identification + 別プロジェクト + VPC-SC | 参照整合性を保った匿名化。マスキングは本番アクセス自体が問題 |
| 12 | PB規模+カタログ+自動分類+ドメイン所有 | Dataplex (lakes/zones + DLP + zone IAM) | データを動かさず統合 |
| 13 | 500TB/1Gbps/3週間/NAS | Transfer Appliance | ネット経由は物理的に間に合わない |
| 14 | 3温度 (日次/月次/年次) + 10年保持 | Standard/Nearline/Archive + Lifecycle自動遷移 | アクセス頻度→クラス対応の教科書問題 |
| 15 | 5年分、直近90日中心のクエリ | date partitioning + clustering + partition expiration | 月次テーブル分割(シャーディング)はアンチパターン |
| 16 | EU/US residency + 越境分析は許可制 | location制御 + VPC-SC + IAM | 暗号化はresidencyを保証しない |
| 17 | $50k/月、混在ワークロード | partition + cluster + BI Engine + MV + reservations | フルコンボ選択肢が正解のパターン |
| 18 | Dataflow 5分以内検知 + PagerDuty (2択) | Monitoring alert policies (lag/freshness/worker) / log-based metrics → PagerDuty | 手動レビューと自作監視パイプは不正解 |
| 19 | Oracle 200台/50TB/30分ダウン/経験浅 | DMS 継続CDC → Cloud SQL/AlloyDB | dump/importは時間超過、Datastreamは分析向け |
| 20 | 3地域規制 + 中央可視性 + 地域自律 | Dataplex連邦ガバナンス + Policy Tags + Org Policyで地域固定 | 「集中管理せず統一可視化」= Dataplex |
| 21 | PHI持ち出し防止 (2択) | VPC-SC perimeter / access levels | DLPは検出であってブロックではない |
| 22 | Teradata 500TB/3ヶ月/1Gbps/増分 (2択) | Transfer Appliance+増分 / BQ DTS for Teradata | 初回=物理、増分=ネイティブ連携 |
| 23 | 決済の重複処理禁止 | MERGE on transaction_id + exactly-once sink | メモリ内dedupは耐久性なし、Pub/Sub dedupは処理冪等性でない |
| 24 | ダッシュボード遅い+$10k/月 (2択) | materialized views / BI Engine | 事前集計 + インメモリの複合 |
| 25 | 株式データ RPO=0/RTO<60s | Pub/Sub複製 + 両リージョン並行パイプライン + Spanner multi-region + dedup | スナップショット方式はRPO/RTO未達 |
| 26 | 500人/20部門/1時間以内付与 | Google Groups + dataset-level Viewer + HR連携 + audit logs | グループ=スケールする唯一の選択肢 |
| 27 | リアルタイム5秒 + 日次アトリビューション (2択) | 5s tumbling windowストリーミング / 日次バッチ | Lambda型の使い分け。24hセッションwindowは罠 |
| 28 | AWS併存 + ロックイン回避 | Delta Lake + Databricks + Fivetran | openフォーマット+統一プラットフォーム |
| 29 | 公衆インターネット禁止 | Private Google Access + 外部IPなし + VPC-SC | Interconnect/VPNはオンプレ接続用で無関係 |
| 30 | 単純+複雑ワークフロー混在 | Composer (複雑) + Workflows (単純) の併用 | 全部Composerはコスト・運用過剰 |
| 31 | IoT不正値の即時隔離+リプレイ | Dataflow side outputs + DLQ + alerting | Q49と同型 |
| 32 | アドホック高額クエリ統制+部門別コスト可視化 | reservations + custom quotas + partition/cluster + BI Engine + labels | 時間帯シフトはBQ価格に無意味 |
| 33 | データレイク (IoT+ERP+RDB) + スキーマ進化 | GCS (Parquet/Avro) + raw/curated zones + Data Catalog + Dataproc + BQ external tables | 全部BQネイティブ格納は高コスト、Bigtableは用途違い |
| 34 | Cloud SQL 30日PITR / RTO2h / 本番影響なし | automated backups + binary logging | pg_dumpは負荷+粒度不足 |
| 35 | 単一SA広範権限の是正 | パイプラインごとにSA + 最小の事前定義ロール | 「共有SA継続」系は全部不正解 |
| 36 | Q6の変形 (2択) | Dataflow検証+エラーバケット / Looker Studio可視化 | 実装の柱+可視化の柱 |
| 37 | イベントスキーマ進化で取込破壊 | Schema Registry + Avro検証 + Dataflow変換 + BQ relaxation | 発行前検証が肝。auto-detectは事後対応 |
| 38 | DRの規制証跡 | 本番同等ステージング + 月次drill + 合成データ + Monitoring計測 | 本番chaosは金融で不可、四半期は頻度不足 |
| 39 | 即時読取不能化 + dev/prod暗号分離 | CMEK + 環境別key ring + 自動ローテ + Audit Logs | 鍵destroy=即時無効化。ここではEKM不要 (要件が「Google不可」でない) |
| 40 | 集計は可・個人識別子は不可 (2択) | DLP de-identify (FPE) / policy tags列制御 | ビュー量産は保守不能 |
| 41 | マルチクラウド可搬性 (2択) | Dataproc Spark + Parquet + Iceberg + WIF / Delta・Hudi + Ranger + Trino | BQ Omni/Storage Write APIはGCP依存で罠 |
| 42 | BQ30 + GCS50 + SQL横断の発見+PII+リネージ | Dataplex + DLP + Data Catalog + Lineage | OSS自前構築は不正解の定番 |
| 43 | 50k writes/s KV時系列 強整合不要 低予算 | Bigtable | Firestore/Cloud SQLはスループット不足、Spannerは過剰 |
| 44 | 7年後に確実に自動削除 | GCS Lifecycle + BQ table expiration | 自作削除ジョブ系は全部不正解 |
| 45 | Datastream→Dataflow→BQ→dbt→Looker のE2Eリネージ | Data Catalog lineage + Dataflowリネージ有効化 + Lineage APIでdbt統合 | SQLパース自作/商用ツールは不正解 |
| 46 | 外部データ結合でも再識別不能の証明 | 差分プライバシー (ε=1.0, δ=1e-5) + 集計限定 + budget管理 | 秘匿化/k-匿名/合成データは保証が弱い |
| 47 | ダッシュボード vs data science 分離 | Enterprise edition + reservation分割 (70/30) + priority | on-demandクォータでは性能保証にならない |
| 48 | EU/US分離 + 集計のみ協業 | 別プロジェクト + 単一リージョン + Org Policy + VPC-SC | multi-region系は物理分離違反 |
| 49 | malformed JSONでパイプ全停止 | ParDoのtry-catch + side output → GCSエラーバケット | Pub/Sub DLQは「処理内失敗」を救えない |
| 50 | 数千テーブルの自動分類タグ付け | Data Catalog + DLP inspection templates + tag templates | 手動フォーム/regex自作は不正解 |

---

## 3. ひっかけ選択肢の型 (見た瞬間に切る)

- **自前運用**: Jenkins/Apache Atlas/Ranger/Hadoop/Vault/Great Expectations を GKE・GCE・Cloud Run に構築 → 運用負荷で不正解。
- **Cloud Functionsで重量処理**: タイムアウト(数分〜)と実行モデルが大規模データに不適。
- **存在しない機能**: Dataflowの「マルチリージョンモード」、BQの「同期クロスリージョンレプリケーション」、BQの「INSERT時に制約で行単位拒否」。
- **DLPの役割誤用**: DLPは検出・変換(de-identify)。転送のブロックや アクセス制御はしない (それはVPC-SC/IAM)。
- **Pub/Sub dedup ≠ 冪等性**: メッセージ重複配信の抑止であって、ack後の再処理は防げない。
- **external tables**: 低速。性能・SLA要件がある文脈では不正解。
- **手動プロセス**: spreadsheet管理、週次レビュー、承認委員会、手動リネージ → 「スケール」「1時間以内」等の要件と衝突。
- **テーブルシャーディング** (`table_202401`): アンチパターン。常にpartitioningへ。
- **時間帯シフトでBQコスト削減**: BQに時間帯料金はない。
- **k-匿名性/合成データで「証明」**: 背景知識攻撃・モデル記憶のリスク。数学的保証は差分プライバシーのみ。
- **暗号化でresidency**: 暗号化しても物理的な地域移動は防げない。
- **multi-region構成で「地域分離」**: multi-regionは複製が広がる方向。分離要件では逆効果。

---

## 4. 頻出判断軸の整理

### DB選定 (Q3,4,5,43)
- Spanner: グローバル / ACID / 99.999% / 水平スケール / external consistency。分析連携は change streams。
- Bigtable: 書き込みスループット特化・1桁ms・KV/wide-column・時系列。SQLなし、強整合の複雑トランザクションなし。
- AlloyDB: 高性能PostgreSQL。**単一リージョン**が試験上の除外条件。
- Cloud SQL: 中規模OLTP。グローバル・数万TPSで即除外。
- Firestore: モバイル/Webアプリ向けドキュメント。大規模スループット問題では除外される役回り。

### 暗号鍵の3段階 (Q9,10,39)
1. Google-managed: 顧客制御なし → 「制御」要件で即除外。
2. CMEK (Cloud KMS): 顧客が無効化/破棄=即時失効、key ringで環境分離、ローテ自動化、Audit Logs。
3. EKM: 鍵材はGoogle外。「Googleが復号できないこと」という文言が出たときだけこれ。

### DRの対応表 (Q2,25,38)
- RPO=0 & RTO秒 → active-active (両リージョン常時稼働 + dedup)。コスト2倍を許容する文言があるか確認。
- RTO分単位 & RPO分単位 & コスト重視 → ウォームスタンバイ (テンプレ+IaC+スナップショット/複製)。
- テスト → 本番同等ステージング+定期drill+自動化+メトリクス証跡。本番chaos・年数回・SLA頼みは不正解。

### ガバナンス製品の役割分担 (Q12,20,42,45,50)
- Dataplex: 組織化 (lakes/zones)、ドメイン所有、プロファイリング、品質、統合ガバナンス。
- Data Catalog: 検索、タグ(tag templates)、リネージ (現在はDataplexに統合)。
- DLP: PII検出 (infoTypes)、de-identify (FPE/tokenization)、リスク分析。
- Analytics Hub: 組織間・プロジェクト間の購読型データ共有。
- VPC-SC: 境界。Org Policy: 予防的ガードレール (location制約等)。

---

## 5. 問題集の記述 vs 2026年の現実 (本番でのズレ対策)

この模試は概念は正しいが、名称・仕様が古い箇所がある。本番・実務では以下で読み替える。

- **Data Studio → Looker Studio** (2022改名)。模試内の表記ゆれはすべてLooker Studio。
- **Cloud Source Repositories は新規受付終了** (2024)。CI/CDの文脈はGitHub/GitLab + Cloud Buildで読み替え。
- **Data Catalog は Dataplex Universal Catalog へ統合進行中**。本番では「Dataplex (Catalog)」として出る可能性。リネージもDataplex Lineage。
- **Firestoreの「10k writes/s上限」は撤廃済み** (2021)。ただし模試・本番とも「超高スループット=Bigtable」の解法自体は変わらない。
- **Q22のDatastream+Teradataは不正確**: Datastreamのソースは Oracle / MySQL / PostgreSQL / SQL Server 等で **Teradata非対応**。Teradata→BQ は BigQuery DTS が正。設問の正解2つのうちDTS側を信用する。
- **Q3の「テーブル単位のwrite region/整合性設定」はSpannerに存在しない**。実態: インスタンス構成 (リーダーリージョン、dual-region構成は日本などに存在) + **読み取り時に strong / bounded staleness をクライアントが指定**。概念(クリティカル=強整合読み、非クリティカル=stale読み)として理解しておく。
- **Q46の「Cloud DLPの差分プライバシーライブラリ」**: 実態は **BigQueryの差分プライバシー集計 (`SELECT WITH DIFFERENTIAL_PRIVACY`)** またはGoogleのOSS DPライブラリ。DLPが持つのはk-匿名性等の再識別リスク分析。
- **BQ料金**: flat-rate廃止済み、現行は **Editions (Standard/Enterprise/Enterprise Plus) + autoscaling slots** (Q47は現行仕様を正しく反映)。
- **Dataform / Datastream / BigLake / Iceberg対応**など2024年版試験ガイドで比重が上がった領域はこの模試では薄い。公式Exam Guideの差分を別途確認。

---

## 6. 復習の回し方

1. 本表の「決め手」列を隠して要件キーワードから正解を即答 (目標: 50問を15分)。
2. 間違えた行だけ設問本文に戻る。
3. セクション5のズレを頭に入れてから公式サンプル問題 (Cloud Skills Boost) で答え合わせ。
