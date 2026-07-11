# AIP-C01 模試#1 (Kane/Maarek) — 75問圧縮ノート

対象: Full Practice Exam #1。ドメイン配分は本番と一致 (D1:23問31% / D2:20問27% / D3:15問20% / D4:9問12% / D5:8問11%)。
D1=FM統合・データ管理 / D2=実装・統合 / D3=安全・セキュリティ・ガバナンス / D4=運用効率・最適化 / D5=テスト・検証

---

## 0. この試験の思考回路

1. **Guardrailsが最頻出の正解部品** (単独 or 多層防御の柱)。機能名と要件語の対応を暗記: content/topic/word filter, PII masking (入出力両方), contextual grounding check (幻覚+根拠スコア), automated reasoning (ポリシー文書からのルール強制)。
2. **fine-tuning は罠**。「安全性/JSON形式/最新文書対応のためにfine-tune」はほぼ常に不正解 (コスト+ライフサイクル+決定的保証なし+文書更新に追随不可)。AIP-C01はモデル訓練を役割外と明言。
3. **「LEAST operational overhead」= マネージドGenAI部品を選ぶ**: Knowledge Bases > 自作RAG、Model Evaluations > 自作評価、Step Functions > 自前ループ、Data Automation > Textract+自作パース。
4. **DynamoDBでベクトル類似検索は常に不正解** (k-NNなし)。本試験で3回以上出る。
5. **決定性が要る回答 (金額・取引) はFMに生成させない**: text-to-SQL (allowlist・parameterized・SELECTのみ) の結果からのみ回答。

---

## 1. 要件キーワード → 即応表

### ネットワーク / セキュリティ (D3)
| 要件 | 答え |
|---|---|
| パブリックインターネット禁止 | interface VPC endpoint (Bedrock/Athena) + S3 gateway endpoint + 外部IPなしsubnet |
| Athena経由の列レベル制御 (PHI除外) | Lake Formation data filters |
| 有害入力/出力・PII・禁止トピック | Bedrock Guardrails (リアルタイム、入出力両方) |
| 幻覚検出+confidence signal | Guardrails contextual grounding check |
| ポリシー文書由来のルール強制 | Guardrails automated reasoning policy + Lambda最終チェック + model card |
| PII: 会話のリアルタイム | Comprehend (前処理placeholder置換) / Guardrails masking |
| PII: S3蓄積データの発見 | Macie (※リアルタイムマスキング不可) |
| SSO+短期クレデンシャル+推論のみ | IAM Identity Center + IdP連携 + InvokeModel/Converse限定policy |
| データはオンプレ残置 | Outposts でローカル前処理・de-identify + PrivateLinkでBedrock |
| 監査: 誰がどのモデル版・ソース | model cards + Glue Catalog lineage + CloudWatch Logs決定ログ (CloudTrailはAPI活動のみ) |
| agentの推論過程の監査 | Bedrock agent trace (+取得ドキュメントmetadata提示) |

### RAG / データ (D1)
| 要件 | 答え |
|---|---|
| S3ソースRAG最小運用 | Bedrock Knowledge Bases + RetrieveAndGenerate |
| Confluence / SharePoint | KBマネージドコネクタ |
| Salesforce→S3コピー必須 | AppFlow → S3 → KB |
| 文書更新の準リアルタイム同期 | S3イベント→EventBridge→Lambda→StartIngestionJob |
| 完全一致ID (CVE/エラーコード)+意味検索 | hybrid search (keyword+vector)。遅延許容ならreranker追加 |
| ベクトル検索の遅延/JVM圧 | fewer, larger shards + ドメイン別multi-index + 階層ルーティング |
| 精密ヒット+周辺文脈 | hierarchical chunking (child検索→parent返却) |
| 版・部署・著者の識別 | metadata schema分離 + metadata filtering (チャンク本文に混ぜない) |
| 画像+テキスト同一検索 | Titan Multimodal Embeddings |
| 検索層で埋め込み自動生成 | OpenSearch Neural plugin (ingest pipeline + neural query) |
| PDF+画像+音声→構造化JSON | Bedrock Data Automation (blueprints)。CSVはGlue |
| バッチ入力の品質検証+メトリクス | Glue Data Quality (DQDL) + quarantine + CloudWatch |
| embeddingコスト削減 | 次元削減(relevance検証付き) + バッチ生成 + モデルPoC比較 |
| vector store差し替え耐性/tool標準化 | MCP server (stateless契約)。軽量=Lambda、重量/native依存=ECS Fargate |
| モデル切替を再デプロイなし+段階rollout | AWS AppConfig (deployment strategy + CWアラームrollback) |
| リージョン障害+地理制約 (US内等) | geographic cross-Region inference profile |
| プロンプト集中管理+承認+版 | Bedrock Prompt Management (+Guardrails+CloudTrail) |
| 組織標準化 | Well-Architected Generative AI Lens + 再利用IaC |

### 実装・統合 (D2)
| 要件 | 答え |
|---|---|
| reasoning+acting ループ+監査+リトライ | Step Functions (InvokeModelタスク+Lambda+Choice, ReAct) |
| 複数成果物を並列生成→統合 | Step Functions Parallel state + Lambda合成 |
| 人手承認 (分〜時間待ち) | Step Functions待機 + API GWフィードバック + DynamoDB |
| ツール障害の暴走ループ停止 | ループカウンタ+Choice + DynamoDB TTL circuit breaker + 最小権限IAM |
| webhook 2秒ACK+将来のファンアウト | API GW→Lambda検証→EventBridge (ルール追加だけで消費者追加) |
| legacyバースト+疎結合 | API GW→SQS直接統合→Lambda→Bedrock |
| 同期+長時間非同期の両立 | API GW request validator + Lambda同期 / SQS+job ID非同期 |
| streaming+トークン予算+リトライ | API GW WebSocket + Lambda (CountTokens→ConverseStream) + SDK backoff |
| 非開発者がプロンプトワークフロー編集 | Bedrock Flows (Amplify+OpenAPI API GWと組む) |
| agent記憶 (セッション+長期) | AgentCore Runtime + AgentCore Memory |
| agent tool の不正パラメータ | 型付きツール定義 + Lambda厳格検証 + 構造化エラー返却 |
| CI/CD+自動rollback | CodePipeline+CodeBuild(テスト+セキュリティスキャン)+CodeDeploy canary (Lambda alias)+CWアラーム |
| LoRA版管理+承認+安全リリース | SageMaker Model Registry (approval) + deployment guardrails (canary+自動rollback) |
| 大型LLM endpoint起動失敗 (health check) | container startup health check timeout / model download timeout延長 |
| ConverseStreamのvalidation error | messages配列 (role/content) に整形。SageMakerは期待スキーマJSON+Content-Type。推論はbedrock-runtime |

### コスト / 性能 (D4)
| 要件 | 答え |
|---|---|
| routine vs complex 混在コスト | Intelligent Prompt Routing / model cascading |
| verbatim反復+決定的応答 | CloudFront edge cache (正規化fingerprintハッシュ) |
| 静的prefix (system prompt/few-shot) | prompt caching (※毎回FMは呼ばれる) |
| 体感遅延 (チャット) | streaming + latency-optimized inference + TTFT計測 |
| 夜間大量・非同期 | batch inference (S3 in/out) |
| 予測可能ピーク+同期+単一リージョン | provisioned throughput (provisioned model ARNで呼ぶ) |
| トークンコスト+context超過 | CountTokensで予算チェック + 履歴prune + chunk数削減 + 小型FMで履歴要約 + maxTokens |
| Lambda→OpenSearch/Bedrock接続遅延 | SDKクライアントをhandler外で再利用 + keep-alive |
| 表現ゆれ・投機的記述 (同一モデル) | temperature低下 + top-p/top-k調整 → Model Evaluationsで構成比較 |

### 評価・テスト (D5)
| 要件 | 答え |
|---|---|
| RAG評価 (faithfulness/citation) | Bedrock Model Evaluations RAG評価 (LLM-as-judge, S3 dataset) |
| デプロイ前回帰ゲート | Model Evaluations を CodePipeline stageに (閾値でfail) |
| デプロイ後の継続検知 | CloudWatch Synthetics canary + alarms |
| 段階導入+自動rollback | CodeDeploy canary (Lambda alias) |
| 多次元品質 (関連性/正確性/一貫性/流暢さ) | LLM-as-judge (ROUGE/BLEU単独・トークン数・遅延は品質指標にならない) |
| agentのタスク完了率+tool効率 | Agent evaluations + trace→CW Logs Insights (反復tool呼び出し計測) |
| 評価結果の定期レポート | S3 + Glue crawler + Athena + QuickSight |
| ユーザーフィードバック収集 | UI→API GW→Lambda→DynamoDB (model ID/prompt version付き) |
| 公平性A/B | Prompt Management variants + Flows + LLM-as-judge (balanced dataset) + CW |

---

## 2. 75問 一行要約 (D=ドメイン)

| # | D | シナリオ要点 | 正解の柱 |
|---|---|---|---|
| 1 | 3 | 医療: 非公開経路+列制御+監視 | PrivateLink (Bedrock/Athena) + S3 gateway EP + Lake Formation列フィルタ + CW Logs |
| 2 | 4 | CVE等の完全一致ミス+遅延増 | hybrid search + ID抽出前処理 + fewer larger shards (reranker/HNSW増は遅延増で×) |
| 3 | 1 | 写真/テキスト両方で商品検索 | Titan Multimodal Embeddings (同一ベクトル空間) |
| 4 | 2 | routine大半+一部高度 | model cascading / Intelligent Prompt Routing |
| 5 | 4 | verbatim反復+決定的設定 | CloudFront + fingerprintハッシュでedge cache (FM呼び出し自体を回避) |
| 6 | 3 | 融資: 禁止表現+免責必須+文書化 | Guardrails (automated reasoning) + Lambda最終チェック + model card |
| 7 | 2 | 複雑質問を段階推論+tool実行+監査 | Step Functions ReActループ (Choice+retry+実行履歴) |
| 8 | 3 | 監査: モデル版・ソース・不変記録 | model cards + Glue lineage/tag + CW Logs決定ログ |
| 9 | 4 | 出力を即表示+バーストで固定費回避 | streaming + latency-optimized inference + TTFT計測 |
| 10 | 1 | ノイズだらけチケットの入力整形 | Lambda前処理 + Comprehendエンティティ抽出 + Bedrockでテンプレ整形 |
| 11 | 3 | PIIをFMに送らない+utility維持 (2択) | Comprehend PII→placeholder / Guardrails PII masking (入出力) |
| 12 | 5 | RAG自動評価+ユーザーフィードバック (2択相当) | Model Evaluations RAG評価 (LLM-as-judge) + API GW+DynamoDB |
| 13 | 2 | webhook 2秒ACK+消費者追加自由 | Lambda署名検証→EventBridgeファンアウト |
| 14 | 1 | S3頻繁更新→KB同期 | S3イベント→EventBridge→Lambda StartIngestionJob |
| 15 | 1 | SharePoint/Confluence/Salesforce統合 (2択) | KBコネクタ / AppFlow→S3→KB |
| 16 | 1 | OpenSearchとpgvectorの統一IF | MCP server (vector_search tool契約) |
| 17 | 5 | 小型モデル+パラメタ変更の検証+段階導入 (2択) | Model Evaluations (token/latencyで費用対品質) / CodeDeploy canary+CWアラーム |
| 18 | 2 | UI速攻+API-first+非開発者編集 | Amplify + OpenAPI API GW + Bedrock Flows |
| 19 | 2 | 同期+長時間非同期+JSON検証 | request validator + Lambda同期 / SQS+job ID |
| 20 | 3 | 複数チームのプロンプト統制+監査 | Prompt Management + Guardrails + CloudTrail/CW Logs |
| 21 | 1 | S3のRAGを最小運用で | Knowledge Base + RetrieveAndGenerate |
| 22 | 3 | 悪罵対応+取引額の捏造禁止+決定的 | Guardrails + text-to-SQL (read-only parameterized) 結果のみで回答 |
| 23 | 2 | Okta SSO+短期クレデンシャル+推論のみ | IAM Identity Center + 最小権限permission set |
| 24 | 4 | p95遅延: 接続セットアップ+shard fan-out (2択) | クライアント再利用+keep-alive / fewer larger shards |
| 25 | 5 | 評価結果の週次レポート | S3+Glue crawler+Athena+QuickSight |
| 26 | 2 | Agent Squad+Strands: セッション+長期記憶 | AgentCore Runtime + AgentCore Memory |
| 27 | 4 | 夜間数十万件でスロットリング | batch inference (S3 in/out) |
| 28 | 1 | 夜間JSONの品質検証+pass/failメトリクス | Glue Data Quality (DQDL) + quarantine + CW |
| 29 | 3 | agent透明性: trace+ソース帰属+confidence | agent trace + 取得docメタデータ提示 + CW custom metric |
| 30 | 4 | トークンコスト+context超過 (2択) | 履歴要約圧縮+maxTokens / CountTokens予算+prune+CW計測 |
| 31 | 3 | prompt injection+PII 多層防御 | Comprehend前処理 + Guardrails + Lambda後処理 + API GW整形 |
| 32 | 1 | 最新版・部署の正確な選択 | metadataスキーマ分離 (business_unit/timestamp) + filtering |
| 33 | 1 | PDF+JPEG+MP3+CSV→JSON case packet | Bedrock Data Automation + Glue(CSV) + Lambda組立 |
| 34 | 1 | 狭い条項ヒット+文脈、取込コスト最小 | hierarchical chunking (semanticは取込時FMコストで×) |
| 35 | 1 | エラーコード完全一致+関連度 | hybrid search + Bedrock reranker |
| 36 | 2 | MCP: 軽量stateless vs CPU重・native依存 | Lambda MCP server / ECS Fargate MCP server |
| 37 | 2 | 2成果物を特化モデルで最速生成 | Step Functions Parallel + Lambda統合 |
| 38 | 5 | prompt/model更新の自動回帰ゲート | Model Evaluations (baseline比較) をリリースゲートに |
| 39 | 2 | 人手承認 (分〜時間)+評価記録 | Step Functions待機 + API GWフィードバック + DynamoDB |
| 40 | 3 | 患者向け: 有害入力+PIIをリアルタイム | Guardrails (topic/word + input PII masking) |
| 41 | 5 | 回帰テスト+継続検知 (2択) | Model EvaluationsをCodePipelineゲート / Synthetics canary+alarm |
| 42 | 2 | SDK不可のlegacy+バースト+即ACK | API GW→SQS直接統合→Lambda→Bedrock→DynamoDB |
| 43 | 1 | トピック別+検索層で埋め込み生成 | OpenSearch Neural plugin + トピック別index |
| 44 | 4 | simple/complex混在のコスト | Intelligent Prompt Routing + CWトークン監視 |
| 45 | 4 | 市場オープン10x/45分+単一リージョン | provisioned throughput (RPM/TPMサイジング) |
| 46 | 3 | 応答PII+監査バケットPII検出+90日削除 | Guardrails + Macie + S3 Lifecycle |
| 47 | 3 | injection実時間防御+自動敵対テスト | Guardrails + Lambda前処理 + Step Functionsで攻撃スイート再生+CW |
| 48 | 2 | 患者データはオンプレ残置 | Outposts (ローカルde-identify) + PrivateLinkでBedrock |
| 49 | 5 | 要約の多次元評価 (関連/正確/一貫/流暢) | LLM-as-judge + S3 dataset (ROUGE/BLEU単独×) |
| 50 | 5 | 応答ごとのrating+コメント収集 | UI→API GW→Lambda→DynamoDB (modelID/prompt version) |
| 51 | 3 | 有害出力+決定的read-only SQL | Guardrails + intent→allowlist parameterized SELECTテンプレ |
| 52 | 2 | 複雑度routing+throttling fallback+監査 | Step Functions (分類→Choice→retry→fallback、実行履歴) |
| 53 | 2 | クレームPDF/画像→構造化→CRM更新 | S3イベント→Step Functions→Data Automation (blueprints)→Lambda |
| 54 | 2 | agent toolが空orderIdで落ちる | 型付きシグネチャ + Lambda検証 + 構造化エラー (agentが聞き直す) |
| 55 | 1 | 複数チームの標準GenAIアーキ | Well-Architected Tool + GenAI Lens + 再利用IaC |
| 56 | 1 | 一貫role+固定JSON+PII/topic制御 | Prompt Management (parameterizedテンプレ) + Guardrails |
| 57 | 2 | 平日ピークthrottling、同一モデル継続 | provisioned throughput (provisioned model ARN) |
| 58 | 1 | LoRA版管理+承認+rollback (2択) | Model Registry (approval) / deployment guardrails (canary+CW自動rollback) |
| 59 | 2 | tool障害でループ暴走+最小権限 | ループカウンタ+Choice + DynamoDB TTL circuit breaker + scoped IAM |
| 60 | 1 | 2週間PoC+コスト/遅延計測 (2択) | KB+RetrieveAndGenerate / CountTokens+CWメトリクス |
| 61 | 2 | GenAIゲートウェイ CI/CD+自動rollback | API GW+Lambda + CodePipeline/Build/Deploy canary + CloudTrail/CW |
| 62 | 1 | 数百万chunkのembeddingコスト (2択) | 次元削減(検証付き)+バッチ生成 / 複数embeddingモデルPoC比較 |
| 63 | 2 | 大型LLMのendpoint health check失敗 | startup health check timeout + download timeout延長 |
| 64 | 2 | streaming+トークン予算+自動リトライ | WebSocket API + CountTokens→ConverseStream + SDK backoff |
| 65 | 1 | プロンプト承認+版+監査 | Prompt Management + S3 + CloudTrail + CW Logs |
| 66 | 5 | agentのループ検出+タスク完了検証 (2択) | Agent evaluations / trace→CW Logs Insights |
| 67 | 1 | リージョン障害+US内限定 | geographic cross-Region inference profile |
| 68 | 4 | 表現ゆれ+投機、同一モデルでデータ駆動 | temperature/top-p調整 + Model Evaluationsで構成比較 |
| 69 | 3 | 有害入力ブロック最簡 | Guardrails (topic+word filter) |
| 70 | 1 | ConverseStream検証エラー+SageMakerパースエラー | messages配列(role/content)整形 + InvokeEndpointに期待スキーマJSON |
| 71 | 3 | プロンプト変種の公平性A/B+追跡 | PM variants + Flows + LLM-as-judge (balanced) + CWダッシュボード |
| 72 | 1 | 数千万chunk・複数ドメイン・JVM圧 | ドメイン別multi-index + 階層ルーティング + fewer larger shards |
| 73 | 1 | モデル切替を再デプロイなし+段階+rollback | AppConfig (deployment strategy + CWアラームrollback) |
| 74 | 3 | 幻覚+insufficient evidence+固定JSON | KB retrieve-and-generate + contextual grounding check + JSON構造 |
| 75 | 1 | S3+Confluence頻繁更新、再学習回避 | Knowledge Base (コネクタ) + RetrieveAndGenerate + grounding check |

---

## 3. ひっかけ選択肢の型

- **fine-tuning万能論**: 安全・形式・最新文書対応をfine-tuneで解く選択肢 → ×。RAG/Guardrails/プロンプト統制が正。
- **WAF / API GWスキーマ検証をLLM安全対策に**: HTTP層の防御であり自然言語の安全性・injection・PIIは扱えない。
- **Macieをリアルタイム処理に**: S3蓄積データの発見用。ライブなプロンプト/応答はComprehend/Guardrails。
- **DynamoDBでk-NN / Scanでcosine類似**: 常に×。
- **CloudTrailで推論の中身を監査**: API活動のみ。reasoning traceやソース帰属は agent trace / アプリログ。
- **bedrock (control plane) で推論**: 推論は bedrock-runtime。
- **prompt cachingで「呼び出し削減」**: 毎回FMは呼ばれる。verbatim反復の呼び出し削減はedge cache。動的なRAGコンテキストをprefixに入れるのも×。
- **provisioned throughputで何でも解決**: 容量の話。呼び出し数削減・体感遅延・リージョン耐性は別手段。バースト+コスト回避の文脈では×。
- **cross-Region inference**: 単一リージョン要件と矛盾 / content-based routingの代替にならない。
- **全件人手レビュー (A2I / Ground Truth)**: 「automated」「LEAST overhead」で×。
- **exact string match / ROUGE・BLEU単独 / トークン数・遅延を品質指標に**: 生成系の品質評価としては×。LLM-as-judgeが正。
- **in-memory circuit breaker (Lambda変数)**: 実行環境間で共有されない。DynamoDB+TTLが正。
- **NAT gateway経由**: パブリックエンドポイントへの経路。private要件では×。
- **プロンプト指示だけで安全/形式を保証**: injectionで破られる前提で採点される。

---

## 4. 横断判断軸

### キャッシュ3層の使い分け (Q5, 24, 30)
- **CloudFront edge cache**: verbatim反復 + 決定的応答 → FM呼び出し自体を回避。キーは正規化プロンプト+モデル設定のハッシュ。
- **prompt caching**: 静的prefix (system prompt / few-shot) のトークン割引。動的コンテキストには効かない。
- **semantic cache (MemoryDB等)**: 意味的類似。embedding生成+閾値調整のコストがあるため「verbatim中心」なら過剰。

### スループット/遅延の手段マップ (Q9, 27, 45, 57, 67)
- 体感遅延 → streaming + latency-optimized inference (TTFTで計測)
- 定常・予測可能ピーク → provisioned throughput
- 夜間・非同期・大量 → batch inference
- リージョン障害耐性 → cross-Region inference (geographic profileで地域制限)
- SDK retry/backoff → 過渡障害用。容量は増えない

### チャンク戦略 (Q34ほか)
- fixed: 安い・単純 / semantic: 境界品質↑だが取込時FMコスト / **hierarchical: 精密(child)+文脈(parent)の両立** / メタデータは本文と分離してfiltering

### オーケストレーション使い分け (Q7, 13, 37, 39, 42, 52, 59)
- **Step Functions**: ReActループ、Parallel、人手承認待ち、circuit breaker、fallback routing、実行履歴=監査
- **EventBridge**: ファンアウト・疎結合・消費者追加自由
- **SQS**: バースト吸収・非同期バッファ (API GW直接統合可)
- **Bedrock Flows**: 非開発者のプロンプトワークフロー (分岐・再利用部品)

### 新世代トピック (旧教材にない、本番頻出見込み)
CountTokens API / Bedrock Data Automation / AgentCore (Runtime, Memory, Evaluations) / Strands Agents / Agent Squad / Intelligent Prompt Routing / latency-optimized inference / geographic inference profile / automated reasoning checks / S3 Vectors (低コスト・低性能側の選択肢として登場)。
※「Prompt Flows」は現行名 **Bedrock Flows**。模試内の旧称は読み替え。

---

## 5. 復習の回し方

1. セクション1の即応表を暗記 (特にGuardrails機能セットとキャッシュ/スループットのマップ)。
2. セクション2の表で正解列を隠して即答 → 75問20分。
3. 間違えた問題はドメイン列で集計し、弱いドメインだけ講義に戻る。
4. 模試#2を解いたら同形式で追記。
