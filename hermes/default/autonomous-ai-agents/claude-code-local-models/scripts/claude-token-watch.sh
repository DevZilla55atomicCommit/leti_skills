#!/usr/bin/env bash
# claude-token-watch.sh — Background token monitor for existing Claude Code sessions
# Usage: ./claude-token-watch.sh <session-name> [interval-seconds]

set -euo pipefail

SESSION_NAME="${1:-}"
INTERVAL="${2:-15}"

if [[ -z "$SESSION_NAME" ]]; then
    echo "Usage: $0 <session-name> [interval-seconds]"
    echo "Example: $0 mysession 15"
    exit 1
fi

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' not found"
    tmux list-sessions
    exit 1
fi

echo "Monitoring session '$SESSION_NAME' every ${INTERVAL}s (Ctrl+C to stop)..."

while tmux has-session -t "$SESSION_NAME" 2>/dev/null; do
    sleep "$INTERVAL"
    PANE=$(tmux capture-pane -t "$SESSION_NAME" -p -S -200 2>/dev/null || echo "")
    
    # Check for context/token warnings
    if echo "$PANE" | grep -qi "context.*exceed\|token.*limit\|context length"; then
        echo "[$(date +%H:%M:%S)] ⚠️  Context limit warning detected!"
        tmux send-keys -t "$SESSION_NAME" "/compact focus on current task" Enter
        sleep 2
    fi
    
    # Check if waiting for input (❯ prompt)
    if echo "$PANE" | tail -3 | grep -q '^❯'; then
        # Could trigger /cost or /context here if desired
        :
    fi
done

echo "Session '$SESSION_NAME' ended"