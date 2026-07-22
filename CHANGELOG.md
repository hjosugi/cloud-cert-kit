# Changelog

## 2.2.0 — 2026-07-23

### Added

- 公開サイトのネイティブ英語版と、日本語・英語の相互言語切替
- browser言語、明示的な`?lang=`指定、保存済み選択に対応する入口
- 英語版のrelease intelligence、用途検索、費用比較、設計・IAM・運用・学習view
- repository内の主要README・guide・学習資料の日英ペアとリンク整合テスト

### Fixed

- 動的に生成するURL属性をHTML attributeとしてescapeし、表示文字列用escapeと分離
- browser storageが利用不能でも言語選択とinteractive viewを停止させないfallback
- GitHub Pages workflowの権限をbuildとdeployの必要範囲へ分離
- 日本語版と英語版のsection構造、repositoryリンク、主要interactive viewをCIで検証
- English document本文への日本語混入をCIで検知

## 2.1.1 — 2026-07-11

### Changed

- 設計・運用ガイドと学習コンテンツを`docs/`配下へ集約
- README、公開サイト、テスト、フィード生成文言を新しい構成へ更新
- 公開サイトから参照するrepository内リンクの検証を追加

### Removed

- 不要になった`HANDOFF.md`、`PROGRESS.md`
- repository内で重複管理していた`issues/`とissue作成script
- 分散していた`guide/`、`study/`、`notes/`、`wrong-answers/`の旧ディレクトリ

## 2.1.0 — 2026-07-11

### Added

- 日本語の用途・要件から探せる4クラウドサービスカタログ
- 2 vCPU・8 GiB Linux VMのcapacity-match費用比較
- zone障害を意識したHot object storageの概算比較
- SKU、region、基準日、算入・除外条件、公式価格sourceの表示
- 費用比較のlevelと最終benchmark手順

## 2.0.0 — 2026-07-11

### Changed

- projectとrepositoryを`cloud-hub`へrename
- 資格中心からマルチクラウド設計・運用者向けへ目的を再定義
- siteをCLOUD HUBブランドと比較中心navigationへ変更
- release digestを設計・運用・cross-cloudの3観点へ拡張

### Added

- 4クラウドの思想・resource hierarchy比較
- multi-cloud design decision guideとADR template
- telemetry、availability、alert、costの運用比較
- releaseをstage/scope/default/data plane/control planeで読むguide
- cloud perspective設定とschema v2 digest
- 旧`quad-cloud-ops.html`からの互換redirect

## 1.0.0 — 2026-07-11

### Added

- AIP-C01の5ドメイン判断ガイド
- 50枚の頻出比較フラッシュカード
- 20問のオリジナルシナリオ演習
- AIP-C01とGCP PDEの間違い問題専用ノート
- サイトのAIP-C01学習ハブ
- AIP-C01模試#1 75問圧縮ノートとGCP PDE Domain 1 50問圧縮ノート
- 4クラウド公式フィードの静的分析とGitHub Pages日次配信

### Changed

- スコア追跡を廃止し、間違えた問題だけを翌日・3日後・7日後に復習する方式へ統一
- Automated Reasoning checksをdetect modeとして明記し、application側のblock/rewrite判断を補足

### Operations

- Python標準ライブラリだけでテスト・フィード生成を実行
- 模試原文をGit管理対象外に設定
