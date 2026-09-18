#!/usr/bin/env bash
# claude-check-tokens.sh — One-shot token/context check for a tmux session
# Usage: ./claude-check-tokens.sh <session-name>

set -euo pipefail

SESSION_NAME="${1:-}"

if [[ -z "$SESSION_NAME" ]]; then
    echo "Usage: $0 <session-name>"
    echo "Example: $0 mysession"
    exit 1
fi

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' not found"
    tmux list-sessions
    exit 1
fi

echo "=== Token/Context Check for '$SESSION_NAME' ==="

# Send /cost and /context, capture output
tmux send-keys -t "$SESSION_NAME" "/cost" Enter
sleep 2
tmux send-keys -t "$SESSION_NAME" "/context" Enter
sleep 2

# Capture and show recent output
OUTPUT=$(tmux capture-pane -t "$SESSION_NAME" -p -S -50 2>/dev/null || echo "Failed to capture")
echo "$OUTPUT"

echo "=== End Check ==="