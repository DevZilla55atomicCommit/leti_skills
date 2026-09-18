#!/usr/bin/env bash
# reproduce.sh - Automated research workflow for GitHub repo

set -euo pipefail

REPO_URL="https://github.com/earendil-works/pi"

echo "=== Step 1: Navigate to homepage ==="
printf 'Navigate to: %s\n' "$REPO_URL"

echo "=== Step 2: Capture AX tree (full snapshot) ==="
printf 'Run: browser_snapshot --full\n'

echo "=== Step 3: Extract package.json ==="
printf 'curl -s %s/raw/main/packages/coding-agent/package.json\n' "$REPO_URL"

echo "=== Step 4: Extract README.md ==="
printf 'curl -s %s/raw/main/README.md\n' "$REPO_URL"

echo "=== Step 5: Capture documentation site ==="
printf 'browser_navigate --url %s/docs\n' "$REPO_URL"
printf 'browser_snapshot --full\n'

echo "=== Step 6: Summarize findings ==="
printf 'Append summary to references/summary.md\n'

echo "=== Reproduction complete ==="