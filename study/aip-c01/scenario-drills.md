# AIP-C01 シナリオ演習

既存模試の転載ではないオリジナル演習。各問で「要件語→候補→消去理由」を声に出してから答えを開く。

## 1. RAGの版管理

複数部門が同じ規定の異なる版をS3へ保存している。質問には常に対象部門の最新承認版だけを使いたい。最小運用の改善は？

<details><summary>答え</summary>

`business_unit`、`approved`、`effective_at`をmetadataとして取込み、retrieval時にfilterする。embedding次元を増やしても版や承認状態は保証できない。
</details>

## 2. exact IDと症状

運用assistantは`DB-781`でも「接続が断続的に切れる」でも同じrunbookへ到達する必要がある。

<details><summary>答え</summary>

error code fieldのkeyword searchと本文のvector searchを組み合わせるhybrid search。必要に応じてtop candidatesをrerankする。
</details>

## 3. chunkの粒度

100ページの契約書で、例外条項は2文だが、回答には同じ節全体の条件が必要。

<details><summary>答え</summary>

hierarchical chunking。小さいchildで例外条項を検索し、大きいparentをcontextとして返す。
</details>

## 4. 更新頻度

製品価格表が毎日更新される。最新価格を回答させるためにcustom modelを毎週fine-tuneする案が出た。

<details><summary>答え</summary>

fine-tuningではなくRAGまたはdeterministic data tool。更新をindex/databaseへ反映し、価格は取得結果からのみ回答する。
</details>

## 5. webhook

partner webhookは2秒以内にACKが必要。生成した説明をCRM、通知、監査の3系統へ送り、将来consumerを増やす。

<details><summary>答え</summary>

API Gateway→Lambdaで署名検証→EventBridgeへpublishしてACK。後段でBedrockを呼び、生成eventをrulesでfan-outする。
</details>

## 6. burst

on-premises装置はHTTPSだけ使える。交代時間に数千件が集中し、Bedrock停止中も受信を失いたくない。

<details><summary>答え</summary>

API Gateway→SQS service integration→Lambda consumer→Bedrock。queueがburstと一時停止を吸収する。
</details>

## 7. agent loop

外部API障害中、agentが同じtoolを何度も要求してtoken費用が増える。

<details><summary>答え</summary>

Step Functionsでtool failure counterとChoiceによる停止条件を持つ。共有circuit breakerをDynamoDB+TTLへ置き、cooldown中はfail fastする。
</details>

## 8. tool parameter

FMが`customerId`を文字列ではなく空配列でtoolへ渡すことがある。

<details><summary>答え</summary>

typed schemaに加えtool側で厳格にvalidationし、`INVALID_CUSTOMER_ID`のような構造化errorを返す。retryだけでは直らない。
</details>

## 9. 人手承認

生成した拒否通知は有資格者が編集・承認してから送信する。承認は数時間かかる。

<details><summary>答え</summary>

Step Functions callback/wait pattern、API endpointでapproval/editを受け、DynamoDBへdraft・final・reviewer feedbackを保存する。
</details>

## 10. PII

customer chatの氏名と電話番号をFMへ送らず、同一人物の会話関係は維持したい。

<details><summary>答え</summary>

ComprehendでPIIを検出し、`<NAME_1>`等の一貫したplaceholderへ置換。Guardrailsのinput/output maskingを追加防御にする。
</details>

## 11. policy validation

融資communication policyとの論理矛盾を検出し、違反時は必ず送信を止めたい。

<details><summary>答え</summary>

Automated Reasoning checksでpolicyとの整合findingを得る。ただしdetect modeなので、Lambda等がfindingを検査してblock/rewrite/fallbackを決定する。
</details>

## 12. audit

監査人が「誰がAPIを呼んだか」と「どのsourceでこの回答を作ったか」の両方を要求した。

<details><summary>答え</summary>

前者はCloudTrail。後者はapplication decision logにmodel ID、prompt version、retrieved source IDs、response metadataを記録する。
</details>

## 13. private connectivity

private subnetのLambdaからBedrock、Athena、S3へpublic Internetを使わず接続したい。

<details><summary>答え</summary>

Bedrock/Athena interface VPC endpointsとS3 gateway endpoint。NAT Gateway経由のpublic endpointはprivate service path要件を満たさない。
</details>

## 14. deterministic SQL

FMが生成する任意SQLをAthenaへ実行する案があるが、SELECT以外を絶対に禁止したい。

<details><summary>答え</summary>

intentをallowlisted parameterized SELECT templateへmapする。自由生成SQLを文字列検査するだけにしない。
</details>

## 15. perceived latency

trafficはburstyで専用capacityを買いたくないが、chat離脱を減らしたい。

<details><summary>答え</summary>

ConverseStream等でtokenを逐次表示しTTFTを下げる。Provisioned Throughputは必須ではない。
</details>

## 16. nightly workload

50万件のtranscriptを毎晩要約し、朝までにS3へ結果を置く。同期invocationはthrottleされる。

<details><summary>答え</summary>

Bedrock batch inference。input/outputをS3に置き、offline jobとして処理する。
</details>

## 17. predictable peak

平日9時から30分だけ同期requestが10倍になり、同一Region・同一modelを使い続ける必要がある。

<details><summary>答え</summary>

予測RPM/TPMからProvisioned Throughputをsizeし、provisioned model ARNをinvokeする。
</details>

## 18. context overflow

全会話履歴とRAG chunkを毎回送ってcontext上限を超える。

<details><summary>答え</summary>

CountTokensで事前budgetを確認し、古いturnをrunning summaryへ圧縮、recent turnsだけ残し、retrieved chunk数を制限する。
</details>

## 19. release gate

prompt変更後も文章は毎回少し異なる。以前の品質を保ったまま自動判定したい。

<details><summary>答え</summary>

固定prompt datasetでbaseline/candidateをModel Evaluationsまたはjudge modelにより比較し、quality thresholdをCI/CD gateにする。exact matchは使わない。
</details>

## 20. agent評価

endpointは常にHTTP 200だが、agentが不要なtoolを3回呼んでから回答する。

<details><summary>答え</summary>

goal attainment、tool selection/parameter accuracyをagent evaluationで測り、traceからtool countとloopを分析する。HTTP availabilityだけでは不十分。
</details>
