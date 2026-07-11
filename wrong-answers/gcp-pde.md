# GCP PDE 間違い問題

参照: [Domain 1 50問圧縮ノート](../notes/pde-domain1-design-notes.md)

## 未定着

| 問題 | Domain | 原因 | 見落とした要件語 | 誤答→正解 | 次回の一行ルール | 復習日 | 状態 |
|---|---|---|---|---|---|---|---|
| 例: D1-25 | Design | R | RPO=0/RTO<60秒 | warm standby→active-active | RPO=0は両系常時処理+共有整合DB+dedup | 翌日/3日/7日 | 未定着 |

## 定着済み

| 問題 | 一行ルール | 定着日 |
|---|---|---|
