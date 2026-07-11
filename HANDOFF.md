# HANDOFF — cloud-cert-kit

次セッション (または別のAI/人間) がこの作業を継続するための引き継ぎ文書。
最終更新: 2026-07-11

## 1. プロジェクト目的

1. AWS / Azure / GCP / OCI の上位資格 (Professional / Expert / Specialty) を最小努力で取得する。
2. 4クラウドのサービス・ネットワーク・IAMを実務で混同せず使う (変換表の常備)。
3. 各クラウドの最新リリース・試験改定・イベントを自動追従する。

保有資格 (2026-07時点): AWS SAA / AWS Security Specialty (旧版) / AZ-104 / AZ-400 / SnowPro Core。
制約: Google Japan SWE面接 (2026-08目標) が最優先。資格学習はその隙間で回す。

## 2. 成果物と状態

| 成果物 | 状態 | 備考 |
|---|---|---|
| site/quad-cloud-ops.html | 完成 | GitHub Pages対応。分析済み静的JSONを表示 |
| scripts/build_feed_digest.py | 完成 | 公式4フィードを依存ゼロの小型ML+ルールで日次分析 |
| .github/workflows/site.yml | 完成 | テスト、データ更新、Pages配信を自動化 |
| notes/pde-domain1-design-notes.md | 完成 | Udemy PDE模試 Domain1 (50問) |
| notes/aip-c01-exam1-notes.md | 完成 | Kane/Maarek AIP-C01 模試#1 (75問) |
| AIP-C01 模試#2 ノート | **ブロック中** | 添付アップロードが2回連続で空 (0バイト)。本文のチャット直貼りで解除 |
| PDE Domain2〜5 ノート | 未着手 | 模試を解き次第、同形式で圧縮 |

## 3. サイトとフィード分析の技術メモ

- 静的HTML。localStorage、トラッキング、クライアントからの外部フィード取得なし。
- GitHub Actionsが毎日フィードを取得し、`site/data/feed-digest.json` と `.md` を生成する。
- 分析は小型Multinomial Naive Bayes + 明示ルール。外部AI APIと常時サーバーは不要。
- 1フィード失敗時は前回JSONの該当クラウドを保持する。
- フィードURL (2026-07-11 curl 200確認済み):
  - AWS: https://aws.amazon.com/about-aws/whats-new/recent/feed/
  - Azure: https://www.microsoft.com/releasecommunications/api/v2/azure/rss (要ブラウザUA)
  - GCP: https://cloud.google.com/feeds/gcp-release-notes.xml (Atom)
  - OCI: https://docs.oracle.com/en-us/iaas/releasenotes/feed/
- 資格データを更新する場合は「資格ロードマップ」セクションのtable行を直接編集。状態タグ: st.now / st.new / st.sunset / st.have。
- 詳細仕様と校正方針: `docs/FEED-INTELLIGENCE.md`。

## 4. 模試→圧縮ノートの仕様 (再現用テンプレ)

入力: 模試の全問テキスト (設問+正解+解説)。
出力: notes/<exam>-notes.md。以下の構成を厳守:

```
0. 出題側の思考回路      … 消去法の原則を5項目以内
1. 要件キーワード→即応表  … 「要件語 → 正解サービス/パターン」の表
2. 全問一行要約表        … # / ドメイン / シナリオ要点 / 正解の柱 (1問1行)
3. ひっかけ選択肢の型     … 見た瞬間に切れる誤答パターン
4. 横断判断軸           … 複数問にまたがる使い分けマップ
5. 教材と現実のズレ      … 一次情報 (公式doc/リリースノート) で検証できた項目のみ記載
```

制約: 日本語 / raw markdown / 絵文字なし / UTF-8 LF / 設問の逐語転載はせず要件キーワードに還元する。
根拠のない補正は書かない (recencyルール: 2024以降に変わりうる仕様は検索で確認)。

## 5. 再開手順

1. AIP-C01 模試#2: 本文をチャットに直貼り (長ければ前半/後半の2分割)。→ 上記仕様でノート化し notes/ に追加。
2. PDE Domain2〜5: 各50問の結果ページを貼る → 同上。
3. 月次: issues/CERT-009 の定点観測URLを巡回し、サイトの資格表とPROGRESS.mdを更新。
4. ノート追加時は README.md の構成ツリーと PROGRESS.md の表も更新する。
5. フィード分析の月次校正は CERT-012 に従い、上位20件の誤分類と緊急項目の見逃しを記録する。

## 6. 検証済みファクトの一次情報

PROGRESS.md の「検証済みファクト」節を参照。すべて2026-07-11に公式ページ/公式発表と照合済み。
