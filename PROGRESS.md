# PROGRESS

最終更新: 2026-07-11

## 1. ステータス

| ID | 項目 | 状態 | 完了日/期限 |
|---|---|---|---|
| — | cloud-hubサイト基盤構築 + 一次情報検証 | 完了 | 2026-07-11 |
| HUB-001 | cloud-hubへrename・multi-cloud設計運用へ再定義 | 完了 | 2026-07-11 |
| HUB-002 | cloud-hub v2.0.0 Release | 完了 | 2026-07-11 |
| CERT-010 | 静的フィード分析 + GitHub Pages自動運用 | 完了 | 2026-07-11 |
| — | GitHub public repository作成、Issue #1〜#12登録 | 完了 | 2026-07-11 |
| CERT-013 | 間違い問題だけの復習導線 | 完了 | 2026-07-11 |
| CERT-014 | AIP-C01教材増補 (guide/cards/drills) | 完了 | 2026-07-11 |
| CERT-015 | v1.0.0 Release | 完了 | 2026-07-11 |
| — | PDE Domain1 (Design) 50問ノート | 完了 | 2026-07-11 |
| — | AIP-C01 模試#1 75問ノート | 完了 | 2026-07-11 |
| CERT-001 | AIP-C01 模試#2 ノート | **ブロック** (添付空×2) | — |
| CERT-002..005 | PDE Domain2〜5 ノート | 未着手 | — |
| CERT-006 | AIP-C01 公式教材消化 | 未着手 | 受験前 |
| CERT-007 | AIP-C01 受験予約判断 | 未着手 | Google面接(2026-08)後を想定 |
| CERT-008 | PDE 公式リソース+予約 | 未着手 | — |
| CERT-009 | 資格情報の月次定点観測 | 運用開始待ち | 毎月 |

## 2. 間違い復習

- AIP-C01: `wrong-answers/aip-c01.md` に誤答・迷った問題だけを追加
- GCP PDE: `wrong-answers/gcp-pde.md` に誤答・迷った問題だけを追加
- 総合点と正解問題は追跡しない
- 翌日・3日後・7日後に一行ルールを説明できたら定着済みへ移す

## 3. 検証済みファクト (2026-07-11 一次情報照合)

### AWS
- MLS-C01 (ML Specialty) は 2026-03-31 で廃止済み。後継: MLA-C01 (Associate) + AIP-C01 (Professional)
- AIP-C01 = Generative AI Developer Professional。GA。75問(採点65) / $300 / 合格750
- Security Specialty は SCS-C03 (登録開始 2025-11-18)
- SysOps → CloudOps Engineer Associate SOA-C03 (2025-09-30〜)
- 定点: https://aws.amazon.com/certification/coming-soon/

### Azure (2026年大再編中)
- 廃止済: DP-203 (2025-03-31 → DP-700) / SC-400 (2025-05-31 → SC-401)
- 廃止予定: AZ-204 (2026-07-31 → AI-200) / AZ-500 (2026-08 → SC-500) / DP-100 (→AI-300) / AI-102 (→AI-103) / AI-900 (→AI-901) / AZ-800・801 (→AZ-802)
- 定点: https://learn.microsoft.com/credentials/certifications/retired-certification-exams

### GCP
- 2026-02-22 に Kryterion → Pearson VUE 全面移行
- PMLE は 2026-06 改訂 (Gemini Enterprise Agent Platform 反映)。旧教材注意
- Next '26 発表を各試験ガイドに反映中 (カタログ上部に告知)
- 定点: https://cloud.google.com/learn/certification

### OCI
- 現行コードは -25 系 (1Z0-997-25 等)。年次で -26 へ更新。教材の年式を揃える
- 定点: https://education.oracle.com/certification

### フィード生存確認 (curl 200)
- AWS What's New / Azure Service Updates / GCP Release Notes / OCI Release Notes — 4/4 OK (AzureのみブラウザUA必須)
- 4フィードの日次取得、軽量分類、静的JSON/Markdown生成をGitHub Actions化。外部CORSプロキシ依存を解消

## 4. リスク・注意

- AIP-C01 と Google面接 (2026-08) の学習時間が競合。面接優先、AIP-C01は面接後に受験予約が現実的
- Udemy PDE模試は名称・仕様が一部古い (Data Studio旧称、CSR終了、Datastream×Teradata誤り、Spannerテーブル単位write設定は非実在)。ノートのセクション5参照
- 2024年改訂のPDE本番はDataform / BigLake / Icebergの比重増。Udemy模試では薄い
- フィード分類は読む順序を決める補助機能。採用判断は公式情報、対象inventory、実環境の検証結果で行う
- 対応表は機能の完全互換を意味しない。resource scope、failure behavior、IAM、SLAを必ず個別確認する
