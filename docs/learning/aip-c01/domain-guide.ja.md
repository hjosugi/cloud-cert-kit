<!-- i18n: language-switcher -->
[English](domain-guide.md) | [日本語](domain-guide.ja.md)

# AIP-C01 ドメイン別判断ガイド

公式ブループリントは D1 31%、D2 26%、D3 20%、D4 12%、D5 11%。合格には全サービスの暗記より、要件語から設計パターンを固定する力が必要になる。

公式: [AWS Certified Generative AI Developer - Professional Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01.html)

## ドメイン1: 基盤モデルの統合、データ管理、コンプライアンス — 31%

### このドメインで問われること

- FMとembedding modelの選択
- RAGの取込、chunking、検索、reranking、metadata
- 構造化・非構造化・マルチモーダルデータの準備
- モデル、prompt、設定の外部化とライフサイクル
- ナレッジベース、OpenSearch、Aurora pgvector等の統合

### RAGの判断順序

1. 情報は頻繁に変わるか。変わるならfine-tuningではなくRAG。
2. 正確なIDが重要か。重要ならvector-onlyではなくハイブリッド検索。
3. 小さな条項と周辺文脈の両方が必要か。必要なら階層的chunking。
4. 最新版・部署・地域を限定するか。限定するならmetadata filtering。
5. 初期検索結果に正解が含まれるが順位が悪いか。含まれるならreranker。

### 検索方式の比較

| 方式 | 強み | 弱み | 合図 |
|---|---|---|---|
| keyword | ID、固有名詞、完全一致 | 言い換えに弱い | CVE、ERR-1042、型番 |
| vector | 意味、言い換え | 正確なIDを落とす | 自然文、類似症状 |
| hybrid | 正確+意味 | index設計が必要 | IDと自然文が混在 |
| reranking | top-kの順位改善 | 追加遅延・費用 | 正解候補は取得済み |
| metadata filter | 版、部署、権限を限定 | metadata品質に依存 | latest、business unit |

### chunking

| 戦略 | 選ぶ条件 | 注意 |
|---|---|---|
| fixed | 安価、単純、文書構造が均一 | 境界で意味が切れる |
| semantic | 意味境界が重要 | 取込時にFM費用が増える |
| hierarchical | 小さな条項でヒットし、広い文脈を返す | childとparentの関係を理解する |
| no chunking | 文書単位検索が本当に必要 | 長文・多トピックでは精度低下 |

### データ処理のサービス選択

| 入力 | 最小運用の選択 |
|---|---|
| S3文書をRAG | Bedrock Knowledge Base |
| SharePoint / Confluence | Knowledge Baseの対応コネクタ |
| SalesforceをS3にも保管 | AppFlow→S3→Knowledge Base |
| PDF・画像・音声の構造化 | Bedrock Data Automation |
| CSVの正規化 | AWS Glue |
| PIIのリアルタイム検出 | Comprehend / Guardrails |
| S3蓄積データのPII発見 | Macie |

### 間違いやすい境界

- DynamoDBは一般的なk-NN vector searchの答えにしない。
- Titan Text Embeddingsで画像は扱えない。画像とテキストを同一空間で比較するならマルチモーダルembeddings。
- Prompt Managementはprompt版管理。モデル版管理はModel Registryやモデル固有のライフサイクル。
- Knowledge BaseはRAGであり、会話の短期・長期memoryではない。

## ドメイン2: 実装と統合 — 26%

### 同期・非同期・イベント駆動

| 要件 | パターン |
|---|---|
| 即時応答 | API Gateway→Lambda→Bedrock Runtime |
| token streaming | WebSocket/SSE→ConverseStream |
| 長時間処理、結果は後でよい | API→SQS→worker→結果store+job ID |
| 夜間大量 | Bedrock batch inference、S3 input/output |
| webhookを即ACK | API Gateway→検証→EventBridgeまたはSQS |
| 複数消費者へfan-out | EventBridge rules |

### オーケストレーターの選択

| サービス | 使う場面 | 使わない場面 |
|---|---|---|
| Step Functions | 分岐、再試行、承認待ち、Parallel、監査履歴、エージェントループ上限 | 単純なfan-outだけ |
| EventBridge | 疎結合fan-out、コンテンツルーティング、消費者追加 | 状態を持つ順序制御 |
| SQS | バースト吸収、再処理、バックプレッシャー | 1メッセージを複数消費者へ同報 |
| Bedrock Flows | 非開発者がprompt chain・条件分岐を編集 | 厳密な長時間業務workflow |

### エージェントツールの安全境界

- tool schemaに型、必須項目、説明を定義する。
- Lambda側でも入力を再検証する。FMのtool callを信用しない。
- エラーは構造化して返し、エージェントが不足情報を質問できるようにする。
- tool execution roleは特定table、bucket、secretへリソースレベルで限定する。
- tool失敗回数とループ回数はworkflow側で上限を持つ。
- cooldownを跨ぐサーキットブレーカーはDynamoDB等の共有状態へ置く。Lambdaのメモリ変数は使わない。

### 認証

- Bedrock Runtime APIはIAMとSigV4。ブラウザJWTを直接渡して認可しない。
- workforce SSOはIAM Identity Centerと外部IdPを連携し、短期credentialsを使う。
- inference-only roleは`InvokeModel`、`InvokeModelWithResponseStream`、`Converse`等の必要アクションと対象モデルに限定する。

## ドメイン3: AIの安全性、セキュリティ、ガバナンス — 20%

### Guardrailsの役割分担

| 部品 | 対象 | 試験での使い方 |
|---|---|---|
| content filter | 有害なコンテンツ、prompt攻撃 | 入出力をfilter/block |
| denied topics | 業務上禁止された話題 | topic単位でblock |
| word filter | 禁止語、固有表現 | 正確なフレーズをblock |
| sensitive information filter | PII | blockまたはmask |
| contextual grounding check | sourceとのgrounding・クエリの関連性 | サポートされていない応答を検知 |
| Automated Reasoning checks | ポリシールールとの論理整合 | ファインディングを返し、アプリが判断 |

重要: Automated Reasoning checksは検証層であり、findingを返すdetect mode。自動的なblockではない。アプリケーションがserve、rewrite、clarification、fallbackを決める。またprompt injection防御やオフトピック検出の代替ではない。

公式: [Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

### 深層防御

```text
WAF/API validation
      ↓
入力正規化・PIIプレースホルダー化
      ↓
Bedrock Guardrails
      ↓
FM / ナレッジベース / エージェントツール
      ↓
決定的な出力schema検証・PII再確認
      ↓
安全なレスポンス契約
```

WAFはWeb攻撃、GuardrailsはGenAI内容、IAMはAWSリソース、Lambda validationは決定的な業務ルールを担当する。1つですべてを解こうとしない。

### 決定的なデータアクセス

取引額、在庫、承認状態などの厳密値はFMの記憶や自由生成に任せない。

1. ユーザー意図を許可リストされた操作へマップする。
2. パラメータ化された読み取り専用クエリまたは型付きツールを実行する。
3. 結果セットだけをFMへ渡す。
4. source ID、クエリテンプレートのバージョン、モデルIDを決定ログへ残す。

### 監査の違い

| 必要な証跡 | 選択 |
|---|---|
| 誰がAWS APIを呼んだか | CloudTrail |
| アプリのprompt/model/source/result | アプリケーションログ / CloudWatch Logs |
| エージェントがどのKB/toolを使ったか | agent trace |
| モデルの用途・制限・バージョン | model card |
| データソース・変換 | Glue Catalog / lineage metadata |

## ドメイン4: 運用効率と最適化 — 12%

### まず最適化対象を特定する

| 症状 | 施策 |
|---|---|
| 画面が待たされる | ストリーミングでTTFTを下げる |
| 同一の質問が大量 | 決定的フィンガープリント+エッジキャッシュ |
| system promptが長い | prompt caching |
| シンプルリクエストに高価なモデル | インテリジェントpromptルーティング/モデルカスケード |
| 夜間大量処理 | バッチ推論 |
| 予測可能な同期ピーク | プロビジョンドスループット |
| Region障害・クォータスパイク | クロスリージョン推論プロファイル |
| コンテキストウィンドウ超過 | CountTokens、prune、summary、retrieved chunk制限 |
| Lambda接続設定が遅い | SDKクライアント再利用、keep-alive |
| OpenSearchシャードfan-out | 少なく、適切なサイズのシャード |

### キャッシュを混同しない

- edge cache: FMを呼ばない。verbatimで決定的な応答向け。
- prompt caching: FMは呼ぶ。共通prefixのトークン処理を再利用。
- semantic cache: 類似promptを再利用。embedding費用と誤hit閾値の責任が増える。

### throughputを混同しない

- retry/backoffは一時障害を吸収するが容量を増やさない。
- provisioned throughputは単一モデルの予測可能な容量。
- クロスリージョン推論は利用可能リージョンへルーティング。異なるモデル間の複雑なルーティングではない。
- バッチ推論はインタラクティブ応答の答えにしない。

## ドメイン5: テスト、検証、トラブルシューティング — 11%

### 評価対象を分ける

| 対象 | 代表指標 |
|---|---|
| モデル応答 | 正確さ、有用性、流暢さ、堅牢性 |
| 検索 | コンテキストの関連性、カバレッジ、精度 |
| RAG生成 | 信頼性/グラウンディング、回答の関連性、引用品質 |
| エージェント | 目標達成、ツール選択、ツールパラメータの正確さ、ループ回数 |
| 本番API | レイテンシ、エラー、可用性、トークン使用量 |

Amazon Bedrockの評価はモデルとナレッジベース/RAGを自動評価またはjudge modelで評価できる。RAG評価ではpromptだけでなく、期待するretrieved textやresponseを含むground truth datasetが必要になる。

公式: [Amazon Bedrockリソースの評価](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html)

### リリース前後

```text
固定データセット
   ↓
ベースラインと候補をModel Evaluationsで比較
   ↓ 品質閾値
CI/CD品質ゲート
   ↓
カナリア/リニアロールアウト
   ↓ エラー・レイテンシアラーム
自動ロールバック
   ↓
合成ワークフローで継続監視
```

### 切るべき誤答例

- 正確な文字列一致だけで生成品質を判定
- レイテンシやトークン数を品質とみなす
- RAGのfaithfulnessをコサイン類似度だけで代用
- prompt変更を本番に直接入れてログを人手で確認
- agent評価をHTTP 200だけで済ませる

## 最後に覚える15行

1. 最新文書はRAG、挙動・形式はprompt、policyはGuardrails、専門スタイルは必要時だけカスタマイズ。
2. exact ID+自然文はハイブリッド検索。
3. child検索+parent文脈はhierarchical chunking。
4. metadataは本文へ混ぜずfilterする。
5. Step Functionsは状態、EventBridgeはfan-out、SQSはバッファ、Flowsはpromptワークフロー。
6. FMが作るツール引数はツール側で再検証。
7. PII liveはComprehend/Guardrails、S3発見はMacie。
8. Automated Reasoningはdetect mode。アプリがfindingを処理。
9. CloudTrailはAPI活動、agent traceはオーケストレーション過程。
10. 厳密値は許可リストクエリ/ツール結果から返す。
11. streamingは体感遅延、provisionedは容量、batchはオフライン。
12. edge cacheはFMを回避、prompt cacheはFMを呼ぶ。
13. CountTokensは呼出前予算、maxTokensは出力量上限。
14. quality gateは固定データセット+評価、運用監視は合成+アラーム。
15. ファインチューニング、GPUホスティング、自作パイプラインは「必要性が明示されたときだけ」。