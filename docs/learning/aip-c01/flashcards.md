<!-- i18n: language-switcher -->
[English](flashcards.md) | [日本語](flashcards.ja.md)

# AIP-C01 頻出比較とフラッシュカード

答えを隠して1問10秒。説明できなかったカードだけを [間違い問題ノート](wrong-answers.md) へ追加する。

## RAG・データ

### 1

Q. CVE IDやエラーコードをvector searchが落とす。最初に変えるものは？

A. keywordとvectorを組み合わせるhybrid search。IDをkeyword clauseまたはmetadata filterへ抽出する。

### 2

Q. 正しいchunkはtop-k内にあるが順位が低い。何を追加する？

A. reranker。初期retrievalに正解がない場合はrerankerでは救えない。

### 3

Q. 小さい条項へ精密にhitし、回答には周辺文脈も必要。chunkingは？

A. hierarchical chunking。childをindex/searchし、対応するparentを返す。

### 4

Q. 「最新の人事規定」「欧州部門の規定」を正確に選ぶ方法は？

A. timestamp、business_unit、region等をmetadataとして保持し、filterする。

### 5

Q. metadataを全chunk本文へコピーする欠点は？

A. tokenとnoiseが増え、chunkingで断片化し、構造化filterを使えない。

### 6

Q. 写真queryとtext queryを同じ商品indexへ投げたい。modelは？

A. multimodal embedding model。text-only embeddingでは画像を表現できない。

### 7

Q. S3文書で最小運用のRAGは？

A. Bedrock Knowledge Base + embedding model + managed vector store + RetrieveAndGenerate。

### 8

Q. S3文書更新をnear real timeでKBへ反映するpatternは？

A. S3 event→EventBridge→Lambda→StartIngestionJob。

### 9

Q. conversation memoryとKnowledge Baseの違いは？

A. memoryはsession/actorの会話状態・嗜好、KBは共有document corpusのretrieval。

### 10

Q. PDF、画像、音声を構造化JSONへ抽出するmanaged serviceは？

A. Bedrock Data Automation。CSV等のtabular変換はGlueと組み合わせる。

## 実装・agent

### 11

Q. ReAct loop、分岐、retry、timeout、監査履歴を最小コードで実装するには？

A. Step Functions。

### 12

Q. webhookを即ACKし、後からconsumerを増やしたい。何を使う？

A. API Gateway/Lambdaで検証後、EventBridgeへpublish。rulesでfan-outする。

### 13

Q. burstをbufferし、1つのworker群で非同期処理するには？

A. SQS。

### 14

Q. 非開発者がprompt chainと条件分岐を変更したい。何を使う？

A. Bedrock Flows。

### 15

Q. 2つのFMで別成果物を最短時間で作り、最後に統合するには？

A. Step Functions Parallel state→Lambdaでdeterministic merge。

### 16

Q. agentが空のorderIdでtoolを呼ぶ。modelを大きくする前に何を直す？

A. typed tool schema、tool側validation、structured error。agentに不足情報を聞き直させる。

### 17

Q. Lambda内のin-memory circuit breakerが不適切な理由は？

A. concurrent execution environment間で共有されず、再利用も保証されない。DynamoDB+TTL等を使う。

### 18

Q. Bedrock Runtime APIへCognito JWTを直接送れるか？

A. 送れない。AWS credentialsでSigV4署名し、IAMで認可する。

### 19

Q. WorkforceがOkta SSOでlocal scriptからBedrockを使う安全な方法は？

A. IAM Identity Center federated with Okta→permission set→short-lived credentials。

### 20

Q. ConverseStreamの会話履歴の基本schemaは？

A. `messages` arrayに各turnの`role`と`content`を入れる。

## Safety・governance

### 21

Q. harmful topicとprofanityをリアルタイムでfilterするmanaged controlは？

A. Bedrock Guardrailsのcontent/topic/word filters。

### 22

Q. PIIを会話構造を壊さずFMの前で隠す方法は？

A. Comprehendで検出し、一貫したplaceholderへ置換。Guardrails maskingも重ねる。

### 23

Q. S3 audit bucketにPIIが残っていないか継続発見するserviceは？

A. Macie。

### 24

Q. Contextual grounding checkは何を測る？

A. responseがsourceにgroundedか、queryにrelevantか。PII filterやprompt injection防御とは別。

### 25

Q. Automated Reasoning checksは違反responseを自動blockするか？

A. しない。detect modeでfindingを返し、applicationがblock/rewrite/clarify/fallbackを決める。

### 26

Q. Automated Reasoning checksがprompt injection対策にならない理由は？

A. 与えられたcontentをpolicyに対して検証する機能で、悪意あるinstruction自体を検出・blockしない。

### 27

Q. CloudTrailだけで「どのsourceを使って回答したか」を再構成できるか？

A. 不十分。CloudTrailはAPI activity。source ID、prompt version、response metadataはapplication decision logへ残す。

### 28

Q. agentがどのKBとaction groupを使ったかを見るには？

A. agent trace。

### 29

Q. transaction amountをhallucinateさせない基本patternは？

A. allowlisted parameterized read-only query/toolを実行し、そのresult setだけから回答する。

### 30

Q. WAFとGuardrailsの役割の違いは？

A. WAFはHTTP/Web exploit、Guardrailsはnatural-language input/output safety。

## Cost・performance

### 31

Q. 同一質問・決定的応答でFM invocation自体を減らすには？

A. normalized prompt+model configのfingerprintをkeyにCloudFront edge cache。

### 32

Q. prompt cachingでFM invocationはなくなるか？

A. なくならない。共通prefixのtoken処理を再利用する。

### 33

Q. semantic cacheがverbatim cacheより難しい点は？

A. query embedding費用と誤hitを防ぐsimilarity threshold調整が必要。

### 34

Q. user perceived latencyを最も直接下げる方法は？

A. streamingでTTFTを下げる。full completion latencyとは分けて計測する。

### 35

Q. 夜間数十万件の要約を最も効率よく処理するには？

A. Bedrock batch inference、S3 input/output。

### 36

Q. 毎朝45分だけ予測可能な10倍同期traffic。単一Region。何を検討する？

A. Provisioned Throughput。必要RPM/TPMからsizeする。

### 37

Q. Region impairmentとquota spikeをUS内で吸収するには？

A. US geographic cross-Region inference profile。

### 38

Q. retry/backoffはthrottling capacityを増やすか？

A. 増やさない。一時障害を平滑化するだけ。

### 39

Q. context window超過を呼出前に防ぐには？

A. CountTokens→budget超過なら古いturn、retrieved chunkを減らす。必要なら履歴をsummary化。

### 40

Q. Lambdaから毎回TLS setupが発生する。修正は？

A. SDK/HTTP clientをhandler外で初期化し、connection pooling/keep-aliveを使う。

## Evaluation・release

### 41

Q. prompt/model変更のpre-deployment regression testは？

A. 固定prompt datasetでBedrock Model Evaluationsを実行し、baselineとの品質差をgateにする。

### 42

Q. 生成responseのexact string matchが不適切な理由は？

A. 正しい意味でも表現が変わるため。semanticな品質指標やjudge modelを使う。

### 43

Q. ROUGE/BLEUだけでfactualityを測れるか？

A. 測れない。文字列重複はhallucination、consistency、fluencyを十分評価しない。

### 44

Q. RAG evaluation datasetにprompt以外で必要なものは？

A. 期待retrieved textやreference response等のground truth。

### 45

Q. RAGのretrievalとgenerationで分けて見る指標は？

A. retrievalはcontext relevance/coverage、generationはfaithfulness/answer relevance/citation quality。

### 46

Q. agentのHTTP 200だけでtask successを判断できるか？

A. できない。goal attainment、tool selection、parameter accuracy、loop countを見る。

### 47

Q. rollout中にerror/latencyが悪化したら自動で戻す構成は？

A. canary/linear deployment + CloudWatch alarms + automatic rollback。

### 48

Q. productionの継続的な回帰検知は？

A. CloudWatch Syntheticsで代表workflowを定期実行し、alarmを設定する。

### 49

Q. model qualityとoperational performanceを混ぜない例は？

A. correctness/helpfulnessは品質、latency/error/token countは運用。両方測るが代替しない。

### 50

Q. fine-tuningを選ぶ前に確認することは？

A. RAG、prompt、Guardrails、deterministic validationで解けない恒常的なbehavior/style要件か。更新頻度とlifecycle費用も確認する。
