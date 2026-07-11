# AIP-C01 ドメイン別判断ガイド

公式ブループリントは D1 31%、D2 26%、D3 20%、D4 12%、D5 11%。合格には全サービスの暗記より、要件語から設計パターンを固定する力が必要になる。

公式: [AWS Certified Generative AI Developer - Professional Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01.html)

## Domain 1: Foundation Model Integration, Data Management, and Compliance — 31%

### このドメインで問われること

- FMとembedding modelの選択
- RAGの取込、chunking、検索、reranking、metadata
- 構造化・非構造化・マルチモーダルデータの準備
- モデル、prompt、設定の外部化とライフサイクル
- Knowledge Bases、OpenSearch、Aurora pgvector等の統合

### RAGの判断順序

1. 情報は頻繁に変わるか。変わるならfine-tuningではなくRAG。
2. exact IDが重要か。重要ならvector-onlyではなくhybrid search。
3. 小さい条項と周辺文脈の両方が必要か。必要ならhierarchical chunking。
4. 最新版・部署・地域を限定するか。限定するならmetadata filtering。
5. 初期検索結果に正解が含まれるが順位が悪いか。含まれるならreranker。

### 検索方式の比較

| 方式 | 強み | 弱み | 合図 |
|---|---|---|---|
| keyword | ID、固有名詞、完全一致 | 言い換えに弱い | CVE、ERR-1042、型番 |
| vector | 意味、言い換え | exact IDを落とす | 自然文、類似症状 |
| hybrid | exact+意味 | index設計が必要 | IDと自然文が混在 |
| reranking | top-kの順位改善 | 追加遅延・費用 | 正解候補は取得済み |
| metadata filter | 版、部署、権限を限定 | metadata品質に依存 | latest、business unit |

### chunking

| 戦略 | 選ぶ条件 | 注意 |
|---|---|---|
| fixed | 安価、単純、文書構造が均一 | 境界で意味が切れる |
| semantic | 意味境界が重要 | 取込時にFM費用が増える |
| hierarchical | 小さい条項でヒットし、広い文脈を返す | childとparentの関係を理解する |
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
- Titan Text Embeddingsで画像は扱えない。画像とテキストを同一空間で比較するならmultimodal embeddings。
- Prompt Managementはprompt版管理。モデル版管理はModel Registryやモデル固有のライフサイクル。
- Knowledge BaseはRAGであり、会話の短期・長期memoryではない。

## Domain 2: Implementation and Integration — 26%

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
| Step Functions | 分岐、再試行、承認待ち、Parallel、監査履歴、agent loop上限 | 単純なfan-outだけ |
| EventBridge | 疎結合fan-out、content routing、消費者追加 | 状態を持つ順序制御 |
| SQS | バースト吸収、再処理、backpressure | 1メッセージを複数消費者へ同報 |
| Bedrock Flows | 非開発者がprompt chain・条件分岐を編集 | 厳密な長時間業務workflow |

### agent toolの安全境界

- tool schemaに型、必須項目、説明を定義する。
- Lambda側でも入力を再検証する。FMのtool callを信用しない。
- エラーは構造化して返し、agentが不足情報を質問できるようにする。
- tool execution roleは特定table、bucket、secretへresource-levelで限定する。
- tool失敗回数とloop回数はworkflow側で上限を持つ。
- cooldownを跨ぐcircuit breakerはDynamoDB等の共有状態へ置く。Lambdaのメモリ変数は使わない。

### 認証

- Bedrock Runtime APIはIAMとSigV4。ブラウザJWTを直接渡して認可しない。
- workforce SSOはIAM Identity Centerと外部IdPを連携し、短期credentialsを使う。
- inference-only roleは`InvokeModel`、`InvokeModelWithResponseStream`、`Converse`等の必要actionと対象modelに限定する。

## Domain 3: AI Safety, Security, and Governance — 20%

### Guardrailsの役割分担

| 部品 | 対象 | 試験での使い方 |
|---|---|---|
| content filter | harmful content、prompt attacks | 入出力をfilter/block |
| denied topics | 業務上禁止された話題 | topic単位でblock |
| word filter | 禁止語、固有表現 | exact phraseをblock |
| sensitive information filter | PII | blockまたはmask |
| contextual grounding check | sourceとのgrounding・query relevance | unsupported responseを検知 |
| Automated Reasoning checks | policy ruleとの論理整合 | findingを返し、アプリが判断 |

重要: Automated Reasoning checksは検証層であり、findingを返すdetect mode。自動的なblockではない。アプリケーションがserve、rewrite、clarification、fallbackを決める。またprompt injection防御やoff-topic検出の代替ではない。

公式: [Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)

### defense in depth

```text
WAF/API validation
      ↓
入力正規化・PII placeholder化
      ↓
Bedrock Guardrails
      ↓
FM / Knowledge Base / Agent tools
      ↓
決定的な出力schema検証・PII再確認
      ↓
安全なresponse contract
```

WAFはWeb攻撃、GuardrailsはGenAI内容、IAMはAWS resource、Lambda validationは決定的業務ルールを担当する。1つで全部を解こうとしない。

### deterministic data access

取引額、在庫、承認状態などの厳密値はFMの記憶や自由生成に任せない。

1. user intentをallowlistされたoperationへmapする。
2. parameterized read-only queryまたは型付きtoolを実行する。
3. 結果setだけをFMへ渡す。
4. source ID、query template version、model IDをdecision logへ残す。

### auditの違い

| 必要な証跡 | 選択 |
|---|---|
| 誰がAWS APIを呼んだか | CloudTrail |
| アプリのprompt/model/source/result | application logs / CloudWatch Logs |
| agentがどのKB/toolを使ったか | agent trace |
| モデルの用途・制限・版 | model card |
| データsource・変換 | Glue Catalog / lineage metadata |

## Domain 4: Operational Efficiency and Optimization — 12%

### まず最適化対象を特定する

| 症状 | 施策 |
|---|---|
| 画面が待たされる | streamingでTTFTを下げる |
| 同一の質問が大量 | deterministic fingerprint+edge cache |
| system promptが長い | prompt caching |
| simple requestに高価なmodel | intelligent prompt routing/model cascade |
| 夜間大量処理 | batch inference |
| 予測可能な同期ピーク | provisioned throughput |
| Region障害・quota spike | cross-Region inference profile |
| context window超過 | CountTokens、prune、summary、retrieved chunk制限 |
| Lambda接続setupが遅い | SDK client再利用、keep-alive |
| OpenSearch shard fan-out | fewer, appropriately sized shards |

### キャッシュを混同しない

- edge cache: FMを呼ばない。verbatimで決定的な応答向け。
- prompt caching: FMは呼ぶ。共通prefixのtoken処理を再利用。
- semantic cache: 類似promptを再利用。embedding費用と誤hit thresholdの責任が増える。

### throughputを混同しない

- retry/backoffは一時障害を吸収するがcapacityを増やさない。
- provisioned throughputは単一modelの予測可能なcapacity。
- cross-Region inferenceは利用可能Regionへrouteする。異なるmodel間の複雑度routingではない。
- batch inferenceはinteractive responseの答えにしない。

## Domain 5: Testing, Validation, and Troubleshooting — 11%

### 評価対象を分ける

| 対象 | 代表指標 |
|---|---|
| model response | correctness、helpfulness、fluency、robustness |
| retrieval | context relevance、coverage、precision |
| RAG generation | faithfulness/groundedness、answer relevance、citation quality |
| agent | goal attainment、tool selection、tool parameter accuracy、loop count |
| production API | latency、error、availability、token usage |

Amazon Bedrock evaluationsはmodelとKnowledge Base/RAGを自動評価またはjudge modelで評価できる。RAG評価ではpromptだけでなく期待するretrieved textやresponseを含むground truth datasetが必要になる。

公式: [Evaluate Amazon Bedrock resources](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html)

### release前後

```text
固定dataset
   ↓
baselineとcandidateをModel Evaluationsで比較
   ↓ quality threshold
CI/CD quality gate
   ↓
canary/linear rollout
   ↓ error・latency alarm
automatic rollback
   ↓
synthetic workflowで継続監視
```

### 見たら切る誤答

- exact string matchだけで生成品質を判定
- latency/token数をqualityとみなす
- RAG faithfulnessをcosine similarityだけで代用
- prompt変更を本番へ直接入れてログを人手確認
- agent評価をHTTP 200だけで済ませる

## 最後に覚える15行

1. 最新文書はRAG、挙動・形式はprompt、policyはGuardrails、専門styleは必要時だけcustomization。
2. exact ID+自然文はhybrid search。
3. child検索+parent文脈はhierarchical chunking。
4. metadataは本文へ混ぜずfilterする。
5. Step Functionsは状態、EventBridgeはfan-out、SQSはbuffer、Flowsはprompt workflow。
6. FMが作るtool引数はtool側で再検証する。
7. PII liveはComprehend/Guardrails、S3発見はMacie。
8. Automated Reasoningはdetect mode。アプリがfindingを処理する。
9. CloudTrailはAPI活動、agent traceはorchestration過程。
10. 厳密値はallowlist query/tool結果から返す。
11. streamingは体感遅延、provisionedはcapacity、batchはoffline。
12. edge cacheはFMを回避、prompt cacheはFMを呼ぶ。
13. CountTokensは呼出前budget、maxTokensは出力量上限。
14. quality gateは固定dataset+評価、運用監視はsynthetic+alarm。
15. fine-tuning、GPU hosting、自作pipelineは「必要性が明示されたときだけ」。
