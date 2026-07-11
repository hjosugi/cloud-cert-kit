# cloud-cert-kit

AWS / Azure / Google Cloud / OCIの上位資格を、間違えた問題だけ復習しながら学ぶ静的学習キットです。公式リリースの低コスト分析と、AIP-C01/PDEの判断軸教材をGitHub Pagesで公開します。

- 公開サイト: https://hjosugi.github.io/cloud-cert-kit/
- 学習コンテンツ: [study/](study/README.md)
- 間違い復習: [wrong-answers/](wrong-answers/README.md)
- 進捗Issue: https://github.com/hjosugi/cloud-cert-kit/issues

## 学習方法

1. 模試を解く。
2. 誤答、勘で正解、2択までしか絞れなかった問題だけを `wrong-answers/` へ記録する。
3. 見落とした要件語と「次回の一行ルール」を作る。
4. 対応するドメインガイド、比較表、フラッシュカードだけを復習する。
5. 翌日・3日後・7日後に説明できたら定着済みへ移す。

総合点の追跡や、正解した問題の再学習は行いません。

## 収録コンテンツ

### AWS AIP-C01

- [ドメイン別判断ガイド](study/aip-c01/domain-guide.md)
- [50フラッシュカード](study/aip-c01/flashcards.md)
- [20シナリオ演習](study/aip-c01/scenario-drills.md)
- [模試#1 75問圧縮ノート](notes/aip-c01-exam1-notes.md)
- [間違い問題ノート](wrong-answers/aip-c01.md)

### GCP Professional Data Engineer

- [Domain 1 50問圧縮ノート](notes/pde-domain1-design-notes.md)
- [間違い問題ノート](wrong-answers/gcp-pde.md)

## サイトとフィード

4クラウドの公式RSS/AtomをGitHub Actionsで毎日取得し、小型Naive Bayes分類器と明示ルールで重要度、資格への影響、次の行動を静的JSONへ変換します。

```text
公式フィード → GitHub Actions → 軽量分類 → 静的JSON → GitHub Pages
```

常時サーバー、DB、有料AI API、公開CORSプロキシは使いません。詳細は [Feed intelligence architecture](docs/FEED-INTELLIGENCE.md) を参照してください。

## 構成

```text
cloud-cert-kit/
├── .github/workflows/site.yml      テスト、日次分析、Pages配信
├── config/                         フィードと分析ルール
├── docs/                           技術・運用仕様
├── issues/                         GitHub Issue草稿
├── notes/                          模試圧縮ノート
├── study/                          ドメインガイド、カード、演習
├── wrong-answers/                  間違い問題だけの復習ノート
├── scripts/build_feed_digest.py    依存ゼロのフィード分析器
├── site/                           GitHub Pages静的サイト
├── tests/                          XML解析・分類・fallback試験
├── CHANGELOG.md
├── HANDOFF.md
└── PROGRESS.md
```

`ref/` は貼り付けた模試原文を含むため、著作権と容量の観点からGit管理対象外です。

## ローカル確認

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_feed_digest.py
python3 -m http.server -d site 8000
```

`http://localhost:8000/` を開きます。

## Issue登録

```bash
REPO=hjosugi/cloud-cert-kit ./issues/create-issues.sh
```

スクリプトは同じタイトルの既存Issueをスキップします。

基準日: 2026-07-11。資格・サービス仕様の最終判断は各社公式情報を参照してください。
