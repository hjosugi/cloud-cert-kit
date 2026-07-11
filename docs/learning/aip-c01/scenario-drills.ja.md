<!-- i18n: language-switcher -->
[English](scenario-drills.md) | [日本語](scenario-drills.ja.md)

# AIP-C01 シナリオ演習

既存模試の転載ではないオリジナル演習。各問で「要件語→候補→消去理由」を声に出してから答えを開く。

## 1. RAGの版管理

複数部門が同じ規定の異なる版をS3へ保存している。質問には常に対象部門の最新承認版だけを使いたい。最小運用の改善は？

<details><summary>答え</summary>

`business_unit`、`approved`、`effective_at`をmetadataとして取込み、retrieval時にfilterする。embedding次元を増やしても版や承認状態は保証できない。
</details>

## 2. exact IDと症状

運用アシスタントは`DB-781`でも「接続が断続的に切れる」でも同じrunbookへ到達する必要がある。

<details><summary>答え</summary>

エラーコードフィールドのキーワード検索と本文のベクター検索を組み合わせたハイブリッド検索。必要に応じてトップ候補をリランキングする。
</details>

## 3. chunkの粒度

100ページの契約書で、例外条項は2文だが、回答には同じ節全体の条件が必要。

<details><summary>答え</summary>

階層的チャンク分割。小さい子チャンクで例外条項を検索し、大きい親チャンクをコンテキストとして返す。
</details>

## 4. 更新頻度

製品価格表が毎日更新される。最新価格を回答させるためにカスタムモデルを毎週ファインチューンする案が出た。

<details><summary>答え</summary>

ファインチューニングではなく、RAGまたは決定論的データツールを使用。更新情報をインデックスやデータベースに反映させ、価格は取得結果からのみ回答する。
</details>

## 5. webhook

パートナWebhookは2秒以内にACKが必要。生成した説明をCRM、通知、監査の3系統へ送り、将来のコンシューマ増加を見越す。

<details><summary>答え</summary>

API Gateway→Lambdaで署名検証→EventBridgeへパブリッシュしてACK。後段でBedrockを呼び出し、生成イベントをルールでファンアウトする。
</details>

## 6. burst

オンプレミス装置はHTTPSだけ使える。交代時間に数千件が集中し、Bedrock停止中も受信を失いたくない。

<details><summary>答え</summary>

API Gateway→SQSサービス連携→Lambdaコンシューマ→Bedrock。キューがバーストと一時停止を吸収する。
</details>

## 7. agent loop

外部API障害中、エージェントが同じツールを何度も要求してトークン費用が増える。

<details><summary>答え</summary>

Step Functionsでツール障害カウンターとChoiceによる停止条件を持つ。共有サーキットブレーカーをDynamoDB+TTLに置き、クールダウン中はフェイルファストする。
</details>

## 8. tool parameter

FMが`customerId`を文字列ではなく空配列でツールへ渡すことがある。

<details><summary>答え</summary>

型付きスキーマに加え、ツール側で厳格にバリデーションし、`INVALID_CUSTOMER_ID`のような構造化エラーを返す。リトライだけでは直らない。
</details>

## 9. 人手承認

生成した拒否通知は有資格者が編集・承認してから送信する。承認には数時間かかる。

<details><summary>答え</summary>

Step Functionsのコールバック/待機パターン、APIエンドポイントで承認/編集を受け付け、DynamoDBにドラフト・最終版・レビュアーフィードバックを保存する。
</details>

## 10. PII

カスタマーチャットの氏名と電話番号をFMへ送らず、同一人物の会話関係は維持したい。

<details><summary>答え</summary>

ComprehendでPIIを検出し、`<NAME_1>`等の一貫したプレースホルダーへ置換。Guardrailsの入力/出力マスキングを追加し、防御策とする。
</details>

## 11. policy validation

融資コミュニケーションポリシーとの論理矛盾を検出し、違反時は必ず送信を止めたい。

<details><summary>答え</summary>

自動推論チェックでポリシーとの整合性を検出。ただし検出モードなので、Lambda等がファインディングを検査してブロック/書き換え/フォールバックを決定する。
</details>

## 12. audit

監査人が「誰がAPIを呼んだか」と「どのソースでこの回答を作ったか」の両方を要求した。

<details><summary>答え</summary>

前者はCloudTrail。後者はアプリケーション決定ログにモデルID、プロンプトバージョン、取得したソースID、レスポンスメタデータを記録する。
</details>

## 13. private connectivity

プライベートサブネットのLambdaからBedrock、Athena、S3へパブリックインターネットを使わずに接続したい。

<details><summary>答え</summary>

Bedrock/AthenaインターフェースVPCエンドポイントとS3ゲートウェイエンドポイントを設定。NATゲートウェイ経由のパブリックエンドポイントはプライベートサービスパス要件を満たさない。
</details>

## 14. deterministic SQL

FMが生成する任意SQLをAthenaへ実行する案があるが、SELECT以外を絶対に禁止したい。

<details><summary>答え</summary>

意図を許可リスト化したパラメータ化されたSELECTテンプレートにマッピング。自由生成SQLを文字列検査だけにしない。
</details>

## 15. perceived latency

トラフィックはバーストしやすく専用キャパシティを買いたくないが、チャット離脱を減らしたい。

<details><summary>答え</summary>

ConverseStream等でトークンを逐次表示し、TTFT（Time To First Token）を下げる。プロビジョンドスループットは必須ではない。
</details>

## 16. nightly workload

50万件のトランスクリプトを毎晩要約し、朝までにS3へ結果を置く。同期呼び出しはスロットルされる。

<details><summary>答え</summary>

Bedrockバッチ推論を利用。入力/出力をS3に置き、オフラインジョブとして処理する。
</details>

## 17. predictable peak

平日9時から30分だけ同期リクエストが10倍になり、同一リージョン・同一モデルを使い続ける必要がある。

<details><summary>答え</summary>

予測RPM/TPMからプロビジョンドスループットを調整し、プロビジョンドモデルARNを呼び出す。
</details>

## 18. context overflow

全会話履歴とRAGチャンクを毎回送信し、コンテキスト上限を超える。

<details><summary>答え</summary>

CountTokensで事前予算を確認し、古いターンをランニングサマリーへ圧縮、最近のターンだけ残し、取得したチャンク数を制限する。
</details>

## 19. release gate

プロンプト変更後も文章は毎回少し異なる。以前の品質を保ったまま自動判定したい。

<details><summary>答え</summary>

固定プロンプトのデータセットでベースラインと候補をモデル評価または判定モデルにより比較し、品質閾値をCI/CDゲートに設定。正確な一致は使わない。
</details>

## 20. agent評価

エンドポイントは常にHTTP 200だが、エージェントが不要なツールを3回呼んでから回答する。

<details><summary>答え</summary>

目標達成度、ツール選択/パラメータの正確性をエージェント評価で測定し、トレースからツール呼び出し回数とループを分析する。HTTPの可用性だけでは不十分。
</details>