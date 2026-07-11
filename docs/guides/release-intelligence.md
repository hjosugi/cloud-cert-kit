<!-- i18n: language-switcher -->
[English](release-intelligence.md) | [日本語](release-intelligence.ja.md)

# クラウドリリースを設計・運用の観点で読む

新機能の件数ではなく、既存architectureの前提が変わるreleaseを拾う。

## 8つの確認

1. Stage: Preview / GA / deprecation / retirement / security fix
2. Scope: global / Region / zone / account等
3. Existing resources: 自動適用かopt-inか、新規だけか
4. Data plane: traffic/data format/consistencyが変わるか
5. Control plane: API、IAM、policy、defaultが変わるか
6. Operations: metric、log、quota、runbook、backupが変わるか
7. Economics: pricing、commitment、egress、licenseが変わるか
8. Cross-cloud: 他cloudの同等機能と責任範囲はどう違うか

## stage別の行動

| Stage | 設計者 | 運用者 |
|---|---|---|
| Preview | architecture optionとして記録、production依存は避ける | sandbox検証、SLA/support/Regionを確認 |
| GA | 既存ADRの制約を再評価 | metric、quota、cost、runbookを検証 |
| default change | security/availability前提の差分を確認 | existing/new resourceの適用範囲をinventoryで特定 |
| deprecation | replacementとmigration architectureを決定 | deadline、owner、対象resource、rollbackをIssue化 |
| security | exposureとcompensating controlを評価 | patch/mitigation、evidence、完了確認 |

## cloudごとの読み方

### AWS

service単位のreleaseが多い。Region availability、IAM action、service quota、既存resourceへの適用、CloudFormation/API supportを確認する。

### Azure

Preview→GAだけでなく、Azure Policy、API version、SKU retirement、Entra/Defenderとの統合変更を見る。subscription/MGへ展開するpolicy影響を確認する。

### Google Cloud

product release notesは日単位に複数serviceがまとまる。launch stage、global/regional scope、quota、data/ML model version、deprecated APIを確認する。

### OCI

database version、Region/AD availability、shape、network、IAM policy例、console/API/CLI supportの差を見る。annual certification codeは実務releaseと分離する。

## release review record

```markdown
## <date> <release title>
- provider / service:
- stage / deadline:
- affected inventory:
- design impact:
- operations impact:
- cross-cloud equivalent and difference:
- action / owner / due date:
- official source:
```
