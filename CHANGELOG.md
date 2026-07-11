# Changelog

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
