#!/usr/bin/env bash
# GitHub issue一括登録
# Usage: REPO=hjosugi/cloud-hub ./create-issues.sh
# 前提: gh auth login 済み。ラベルは存在しなければ自動作成する。
set -euo pipefail
REPO="${REPO:?Set REPO=owner/name}"
cd "$(dirname "$0")"

# ラベル作成 (存在すればスキップ)
for l in notes study ops site decision enhancement recurring blocked aip-c01 gcp-pde architecture reliability release hub P1 P2 P3; do
  gh label create "$l" --repo "$REPO" 2>/dev/null || true
done

for f in CERT-*.md HUB-*.md; do
  title=$(head -n1 "$f" | sed 's/^# //')
  labels=$(sed -n '2s/^Labels: //p' "$f")
  if gh issue list --repo "$REPO" --state all --search "in:title \"$title\"" --json title --jq '.[].title' | grep -Fxq "$title"; then
    echo "Skipping existing: $title"
    continue
  fi
  echo "Creating: $title"
  gh issue create --repo "$REPO" --title "$title" --label "$labels" --body-file "$f"
done
