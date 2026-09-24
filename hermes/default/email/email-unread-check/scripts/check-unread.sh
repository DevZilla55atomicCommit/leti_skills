#!/usr/bin/env bash
# List unread counts per account
for acc in gmail icloud outlook; do
  echo "=== $acc ==="
  himalaya envelope list --account "$acc" --folder INBOX --output json
done