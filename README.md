# cloud-hub

AWS / Azure / Google Cloud / OCIを、サービス名の対応ではなく、**思想・resource boundary・failure domain・operator responsibility**の違いから理解するためのマルチクラウド設計・運用サイトです。

- 公開サイト: https://hjosugi.github.io/cloud-hub/
- 最新Release: https://github.com/hjosugi/cloud-hub/releases/latest
- Repository: https://github.com/hjosugi/cloud-hub

## 何が分かるか

- 各cloudが何を主要な隔離・統制単位としているか
- 同等serviceでもglobal/regional scope、IAM、HA、運用責任がどう違うか
- organization、network、identity、data、observability、DR、costをどう比較するか
- 公式releaseがarchitecture、runbook、quota、migrationへ何を変えるか
- 資格で得た知識を本番の設計判断へどう接続するか

## 設計・運用ガイド

1. [4クラウドの思想](guide/cloud-philosophies.md)
2. [マルチクラウド設計判断](guide/multicloud-design.md)
3. [運用モデル比較](guide/operations-comparison.md)
4. [リリースの読み方](guide/release-intelligence.md)

## サイトの情報設計

| セクション | 目的 |
|---|---|
| リリース観測 | 設計・運用・cross-cloud観点付きで公式更新を読む |
| クラウド思想 | 4社のboundary、control、reliability思想を比較 |
| サービス比較 | 機能名だけでなく用途と責任範囲を対応付ける |
| Network / IAM | 混同しやすいscope、継承、routingを比較 |
| 運用比較 | telemetry、audit、availability、alertを共通言語化 |
| 資格・学習 | 実務理解を補強するAIP-C01/PDE教材 |

## リリース・インテリジェンス

4クラウドの公式RSS/AtomをGitHub Actionsで毎日取得し、小型Naive Bayes分類器と明示ルールで次を付与します。

- Preview / GA / retirement / security等のstage
- 設計への影響
- 運用への影響
- 他cloudの対応領域と比較時の注意
- 移行・確認の次の行動

```text
公式フィード
    ↓
GitHub Actions
    ↓
分類・stage判定・cloud別perspective
    ↓
静的JSON / Markdown
    ↓
GitHub Pages
```

常時サーバー、DB、有料AI API、公開CORS proxyは使いません。詳細は [Feed intelligence architecture](docs/FEED-INTELLIGENCE.md) を参照してください。

## 資格学習は補助レイヤ

- [AIP-C01ドメインガイド](study/aip-c01/domain-guide.md)
- [AIP-C01フラッシュカード](study/aip-c01/flashcards.md)
- [AIP-C01シナリオ演習](study/aip-c01/scenario-drills.md)
- [GCP PDE Domain 1圧縮ノート](notes/pde-domain1-design-notes.md)
- [間違い問題だけの復習](wrong-answers/README.md)

資格取得で終わらせず、各問題の判断軸をdesign/operations guideへ接続します。

## 構成

```text
cloud-hub/
├── guide/                          マルチクラウド設計・運用比較
├── site/cloud-hub.html             GitHub Pages本体
├── config/cloud-perspectives.json  cloud思想と対応領域
├── scripts/build_feed_digest.py    公式release分析
├── docs/                           運用仕様
├── study/                          資格学習コンテンツ
├── wrong-answers/                  間違い問題だけの復習
├── notes/                          模試圧縮ノート
└── tests/                          feed・content検証
```

## ローカル確認

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_feed_digest.py
python3 -m http.server -d site 8000
```

`http://localhost:8000/` を開きます。

基準日: 2026-07-11。仕様とSLAの最終判断は各cloudの公式documentationを参照してください。
