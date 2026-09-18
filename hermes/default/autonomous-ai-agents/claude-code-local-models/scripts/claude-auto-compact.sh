#!/usr/bin/env bash
# claude-auto-compact.sh — tmux wrapper for Claude Code with auto-compact for local models
# Usage: ./claude-auto-compact.sh <session-name> <compact-interval-turns> <project-dir> "<focus-topic>"

set -euo pipefail

SESSION_NAME="${1:-claude-work}"
COMPACT_INTERVAL="${2:-10}"
PROJECT_DIR="${3:-$(pwd)}"
FOCUS_TOPIC="${4:-current task}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate
if [[ -z "$SESSION_NAME" || -z "$COMPACT_INTERVAL" ]]; then
    echo "Usage: $0 <session-name> <compact-interval-turns> <project-dir> \"<focus-topic>\""
    echo "Example: $0 mysession 10 ~/project \"auth refactor\""
    exit 1
fi

# Create tmux session
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' already exists. Killing..."
    tmux kill-session -t "$SESSION_NAME"
fi

tmux new-session -d -s "$SESSION_NAME" -x 160 -y 50

# Launch Claude Code with auto-compact disabled
tmux send-keys -t "$SESSION_NAME" "cd '$PROJECT_DIR' && claude --dangerously-skip-permissions" Enter

# Handle trust dialog (Enter for default "Yes")
sleep 4
tmux send-keys -t "$SESSION_NAME" Enter

# Handle permissions dialog (Down then Enter for "Yes, I accept")
sleep 3
tmux send-keys -t "$SESSION_NAME" Down
sleep 0.3
tmux send-keys -t "$SESSION_NAME" Enter

# Wait for Claude to be ready
sleep 5

# Disable built-in auto-compact
tmux send-keys -t "$SESSION_NAME" "/config autoCompactEnabled=false" Enter
sleep 1

# Send initial task with focus topic
tmux send-keys -t "$SESSION_NAME" "Work on: $FOCUS_TOPIC. Keep context focused on this topic." Enter

# Start background monitor
cat <<'MONITOR_EOF' > "/tmp/claude-monitor-$SESSION_NAME.sh"
#!/usr/bin/env bash
SESSION="$1"
INTERVAL="$2"
FOCUS="$3"
COUNTER=0
LAST_COST_TURN=0
LAST_CONTEXT_TURN=0

while tmux has-session -t "$SESSION" 2>/dev/null; do
    sleep 2
    PANE=$(tmux capture-pane -t "$SESSION" -p -S -100 2>/dev/null || echo "")
    
    # Detect turn completion (❯ prompt at bottom)
    if echo "$PANE" | tail -5 | grep -q '^❯'; then
        COUNTER=$((COUNTER + 1))
        echo "[$(date +%H:%M:%S)] Turn $COUNTER completed"
        
        # Every 5 turns: show cost
        if (( COUNTER % 5 == 0 )) && (( COUNTER != LAST_COST_TURN )); then
            LAST_COST_TURN=$COUNTER
            tmux send-keys -t "$SESSION" "/cost" Enter
            sleep 2
        fi
        
        # Every 10 turns: show context
        if (( COUNTER % 10 == 0 )) && (( COUNTER != LAST_CONTEXT_TURN )); then
            LAST_CONTEXT_TURN=$COUNTER
            tmux send-keys -t "$SESSION" "/context" Enter
            sleep 2
        fi
        
        # Every N turns: auto-compact
        if (( COUNTER % INTERVAL == 0 )); then
            echo "[$(date +%H:%M:%S)] Auto-compacting at turn $COUNTER..."
            tmux send-keys -t "$SESSION" "/compact focus on $FOCUS" Enter
            sleep 3
        fi
    fi
    
    # Detect context exceeded error
    if echo "$PANE" | grep -qi "context.*exceed\|token.*limit\|context length"; then
        echo "[$(date +%H:%M:%S)] Context exceeded detected! Forcing compact..."
        tmux send-keys -t "$SESSION" "/compact focus on $FOCUS" Enter
        sleep 3
    fi
done
MONITOR_EOF

chmod +x "/tmp/claude-monitor-$SESSION_NAME.sh"
tmux split-window -t "$SESSION_NAME" -h -p 30 "/tmp/claude-monitor-$SESSION_NAME.sh '$SESSION_NAME' '$COMPACT_INTERVAL' '$FOCUS_TOPIC'"

echo "Claude Code session '$SESSION_NAME' started with auto-compact every $COMPACT_INTERVAL turns"
echo "Monitor pane running on right. Attach with: tmux attach -t $SESSION_NAME"
echo "Focus topic: $FOCUS_TOPIC"