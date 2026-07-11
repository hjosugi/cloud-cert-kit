# cloud-cert-kit

AWS / Azure / Google Cloud / OCIの上位資格学習と実務リファレンスを、1つの静的サイトにまとめた低コスト運用キットです。公式リリースを並べるだけでなく、軽量MLで重要度と意味を分析します。

## できること

- 4クラウドの資格ロードマップ、サービス対応、ネットワーク、IAMの横断参照
- 公式RSS/Atomを毎日取得し、更新を8領域に自動分類
- 各更新へ「なぜ重要か」「学習への影響」「次の行動」を付与
- 廃止、期限、セキュリティ、GAを優先表示
- AIP-C01とGCP PDEの圧縮学習ノートを管理
- GitHub Issue草稿から学習タスクを一括登録

## 低コスト構成

```text
公式フィード → GitHub Actions (日次)
             → 小型Naive Bayes + ルール
             → 静的JSON / Markdown
             → GitHub Pages
```

常時サーバー、DB、有料AI API、公開CORSプロキシは使いません。分類器はPython標準ライブラリだけでActions上で実行されます。詳しくは [Feed intelligence architecture](docs/FEED-INTELLIGENCE.md) を参照してください。

## 構成

```text
cloud-cert-kit/
├── .github/workflows/site.yml      日次分析 + GitHub Pagesデプロイ
├── config/                         フィード、学習例、判定ルール
├── docs/FEED-INTELLIGENCE.md       設計・コスト・運用仕様
├── issues/                         GitHub Issue草稿
├── notes/                          試験問題の圧縮ノート
├── scripts/build_feed_digest.py    依存ゼロの収集・分析器
├── site/
│   ├── index.html                  Pages入口
│   ├── quad-cloud-ops.html         ダッシュボード
│   └── data/feed-digest.{json,md}  生成済み分析結果
├── tests/                          XML解析・分類・フォールバック試験
├── HANDOFF.md                      再開手順
└── PROGRESS.md                     学習・運用進捗
```

`ref/` は貼り付けた模試原文を含むため、著作権とリポジトリ容量の観点からGit管理対象外です。

## ローカル実行

Python 3.11以降だけで動作します。

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_feed_digest.py
python3 -m http.server -d site 8000
```

`http://localhost:8000/` を開きます。ブラウザでHTMLファイルを直接開くと、ローカルJSONの読込がブロックされる場合があります。

## 判定の調整

- 公式フィード: `config/feed-sources.json`
- 分類器の代表文: `config/training-data.json`
- 優先語、カテゴリ語、対象資格: `config/analysis-rules.json`
- 表示閾値と説明: `scripts/build_feed_digest.py`

軽量分類は読む順序を決める一次スクリーニングです。採用判断、移行期限、試験改定は必ずリンク先の公式情報で確認してください。

## Issue登録

```bash
REPO=hjosugi/cloud-cert-kit ./issues/create-issues.sh
```

同じ草稿を再実行すると重複Issueが作られるため、初回に1度だけ実行します。

## 現在の学習優先度

1. Google Japan SWE面接準備
2. AWS AIP-C01模試#2の圧縮ノート作成
3. GCP PDE Domain 2〜5の圧縮ノート作成
4. フィード分類器の月次校正

基準日: 2026-07-11。資格情報の最終判断は各社の公式ページを参照してください。
