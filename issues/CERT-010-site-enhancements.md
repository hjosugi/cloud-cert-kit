# CERT-010: cloud-hub サイト基盤強化
Labels: site,enhancement,P3

## 背景
単なるフィード表示から、意味と行動を示す低コストな静的インテリジェンスへ強化した。

## 候補タスク
- [x] GitHub Pages で公開 — モバイルからの参照用
- [x] CORSプロキシ依存をGitHub Actionsのサーバー側取得で解消
- [x] 小型Naive Bayes + 明示ルールで重要度、意味、学習影響、次の行動を生成
- [x] 取得失敗時の前回データフォールバックを追加
- [ ] ネットワーク/IAMタブに「今日の1問」的なセルフクイズ (静的配列で十分)

## 完了条件
静的feed取得とPages基盤は完了。今後はmulti-cloud設計・運用比較として個別Issueへ分割する。
