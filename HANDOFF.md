# HANDOFF — cloud-hub

最終更新: 2026-07-11

- Repository: https://github.com/hjosugi/cloud-hub
- Site: https://hjosugi.github.io/cloud-hub/
- Release: https://github.com/hjosugi/cloud-hub/releases/latest

## 目的

AWS / Azure / Google Cloud / OCIを比較し、設計者・運用者がservice名ではなく、思想・scope・failure behavior・responsibilityから選択できるようにする。

資格教材は実務理解を補助する一部であり、project全体の目的ではない。

## 中核成果物

| 成果物 | 役割 |
|---|---|
| `site/cloud-hub.html` | 比較・release intelligenceの公開UI |
| `guide/cloud-philosophies.md` | 4cloudの思想とboundary |
| `guide/multicloud-design.md` | 設計軸、ADR、portability判断 |
| `guide/operations-comparison.md` | telemetry、availability、alert比較 |
| `guide/release-intelligence.md` | releaseを8観点で読む方法 |
| `config/cloud-perspectives.json` | feedへ付与するcloud別perspective |
| `scripts/build_feed_digest.py` | 公式feed→静的intelligence |

## Release分析の仕様

各itemへ次を付与する。

- `release_stage`
- `design_perspective`
- `operations_perspective`
- `cross_cloud_context`
- priority / category / evidence

外部AI APIは使わない。1 feed失敗時は前回itemを保持する。

## 更新規則

1. 名前対応だけの比較を追加しない。scope、IAM、HA、operator責任を書く。
2. cloud思想は公式landing zone / Well-Architected guidanceを根拠にする。
3. releaseはPreview/GAだけでなくexisting resource、default、Region、quota、metric、cost、rollbackを見る。
4. 資格noteの新論点は、可能なら`guide/`の実務判断へ昇格する。
5. 模試全文や有料教材の逐語転載はしない。

## 互換性

- 旧repository名 `cloud-cert-kit` はGitHub redirect対象。
- 旧site path `quad-cloud-ops.html` は`cloud-hub.html`へredirectする。
- v1.0.0は旧名称のhistorical releaseとして保持する。
