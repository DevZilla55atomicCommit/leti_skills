#!/bin/bash
# Read all stdin JSON
input=$(cat)

# Extract fields with fallbacks
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
DIR=$(echo "$input" | jq -r '.workspace.current_dir // "~"')
# Anthropic's reported percentage (assumes 200K context)
ANTHROPIC_PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

# Local model context override (in tokens)
# Set via: export LOCAL_MODEL_CONTEXT=32768 (or 65536, 131072)
# Or auto-detect from known model names
LOCAL_MODEL_CONTEXT="${LOCAL_MODEL_CONTEXT:-}"
if [ -z "$LOCAL_MODEL_CONTEXT" ]; then
    case "$MODEL" in
        *32k*|*4b*) LOCAL_MODEL_CONTEXT=32768 ;;
        *48k*|*64k*|*9b*) LOCAL_MODEL_CONTEXT=65536 ;;
        *128k*|*31b*|*coder*) LOCAL_MODEL_CONTEXT=131072 ;;
        *) LOCAL_MODEL_CONTEXT=200000 ;;  # Default to Anthropic's 200K
    esac
fi

# Calculate true tokens used from Anthropic's percentage (based on 200K)
# Then recalculate percentage against local model's actual context
if [ "$LOCAL_MODEL_CONTEXT" -ne 200000 ] && [ "$ANTHROPIC_PCT" -gt 0 ]; then
    # Anthropic reports % of 200K, so tokens_used = ANTHROPIC_PCT * 200000 / 100
    TOKENS_USED=$((ANTHROPIC_PCT * 200000 / 100))
    # True percentage = tokens_used / local_context * 100
    PCT=$((TOKENS_USED * 100 / LOCAL_MODEL_CONTEXT))
    [ "$PCT" -gt 100 ] && PCT=100
else
    PCT=$ANTHROPIC_PCT
    TOKENS_USED=$((ANTHROPIC_PCT * 200000 / 100))
fi

# Tokens per second calculation (live rate with rolling average)
# Cache previous values to compute delta
TPS_CACHE_FILE="/tmp/statusline-tps-cache-$SESSION_ID"
# Use python for millisecond timestamp (macOS date doesn't support %3N)
NOW=$(python3 -c 'import time; print(int(time.time() * 1000))')
if [ -f "$TPS_CACHE_FILE" ]; then
    IFS='|' read -r PREV_TOKENS PREV_TIME PREV_TPS < "$TPS_CACHE_FILE"
    DELTA_TOKENS=$((TOKENS_USED - PREV_TOKENS))
    DELTA_TIME=$((NOW - PREV_TIME))
    if [ "$DELTA_TIME" -gt 0 ] && [ "$DELTA_TOKENS" -ge 0 ]; then
        # New TPS calculation
        NEW_TPS=$((DELTA_TOKENS * 1000 / DELTA_TIME))
        # Rolling average: 70% old + 30% new (smooths out bursts)
        if [ "$PREV_TPS" -gt 0 ]; then
            TPS=$(( (PREV_TPS * 7 + NEW_TPS * 3) / 10 ))
        else
            TPS=$NEW_TPS
        fi
    else
        # No change - keep previous TPS (don't reset to 0)
        TPS=${PREV_TPS:-0}
    fi
else
    TPS=0
fi
echo "$TOKENS_USED|$NOW|$TPS" > "$TPS_CACHE_FILE"

# New: Operations counter (track file operations)
OPS=$(echo "$input" | jq -r '.operations.count // 0' 2>/dev/null || echo "0")

# New: Environment hint (worktree/remote indicators)
ENV_HINT=""
[ -d ".claude/worktrees/*" ] && ENV_HINT=" 🌳 worktree"
[ "$CLAUDE_CODE_ENVIRONMENT" = "remote" ] && ENV_HINT=" ☁️ remote"

# Colors
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
BLUE='\033[34m'
MAGENTA='\033[35m'
RESET='\033[0m'
BOLD='\033[1m'

# Get RAM usage (macOS)
get_ram_usage() {
    # Use memory_pressure for a quick percentage, fallback to vm_stat
    if command -v memory_pressure >/dev/null 2>&1; then
        # memory_pressure reports "System-wide memory free percentage: XX%"
        # We want USED percentage = 100 - free
        local free_pct=$(memory_pressure 2>/dev/null | grep -oE 'System-wide memory free percentage: [0-9]+%' | grep -oE '[0-9]+' || echo "50")
        echo $((100 - free_pct))
    else
        # Fallback: parse vm_stat
        local pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
        local pages_active=$(vm_stat | grep "Pages active" | awk '{print $3}' | tr -d '.')
        local pages_inactive=$(vm_stat | grep "Pages inactive" | awk '{print $3}' | tr -d '.')
        local pages_speculative=$(vm_stat | grep "Pages speculative" | awk '{print $3}' | tr -d '.')
        local pages_wired=$(vm_stat | grep "Pages wired down" | awk '{print $4}' | tr -d '.')
        local pages_compressed=$(vm_stat | grep "Pages occupied by compressor" | awk '{print $5}' | tr -d '.')
        
        local page_size=4096
        local total_pages=$((pages_free + pages_active + pages_inactive + pages_speculative + pages_wired + pages_compressed))
        local used_pages=$((pages_active + pages_inactive + pages_speculative + pages_wired + pages_compressed))
        
        if [ "$total_pages" -gt 0 ]; then
            echo $((used_pages * 100 / total_pages))
        else
            echo "0"
        fi
    fi
}

# Get RAM color based on pressure
get_ram_color() {
    local pct=$1
    if [ "$pct" -ge 90 ]; then
        echo "$RED"
    elif [ "$pct" -ge 75 ]; then
        echo "$YELLOW"
    elif [ "$pct" -ge 60 ]; then
        echo "$MAGENTA"
    else
        echo "$GREEN"
    fi
}

# Build circular progress indicator: 8 circles (● filled, ○ empty)
# Output: "●○○○○○○○"
build_circle_progress() {
    local pct=$1
    local color=$2
    local filled=$((pct * 8 / 100))  # 8 segments = 12.5% each
    [ $filled -gt 8 ] && filled=8
    [ $filled -lt 0 ] && filled=0
    
    local circle=""
    for i in $(seq 1 8); do
        if [ $i -le $filled ]; then
            circle="${circle}${color}●${RESET}"
        else
            circle="${circle}○"
        fi
    done
    echo "$circle"
}

# Build progress bar (10 chars)
BAR_WIDTH=10
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
[ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

# Pick color based on usage - WARNING at 75%
if [ "$PCT" -ge 90 ]; then
    BAR_COLOR="$RED"
    WARNING="${BOLD}${RED}⚠ TOKEN LIMIT NEARING!${RESET}"
elif [ "$PCT" -ge 75 ]; then
    BAR_COLOR="$YELLOW"
    WARNING="${BOLD}${YELLOW}⚠ 75% CONTEXT USED${RESET}"
elif [ "$PCT" -ge 70 ]; then
    BAR_COLOR="$YELLOW"
    WARNING=""
else
    BAR_COLOR="$GREEN"
    WARNING=""
fi

# Format cost
COST_FMT=$(printf '$%.2f' "$COST")

# Format TPS
TPS_FMT=$(printf '%dk/s' $((TPS / 1000)))
[ "$TPS" -lt 1000 ] && TPS_FMT="${TPS}/s"

# Format duration
DURATION_SEC=$((DURATION_MS / 1000))
MINS=$((DURATION_SEC / 60))
SECS=$((DURATION_SEC % 60))

# Git branch (cached for performance)
SESSION_ID=$(echo "$input" | jq -r '.session_id // "default"')
CACHE_FILE="/tmp/statusline-git-cache-$SESSION_ID"
CACHE_MAX_AGE=5

cache_is_stale() {
    [ ! -f "$CACHE_FILE" ] || \
    [ $(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
}

if cache_is_stale; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        BRANCH=$(git branch --show-current 2>/dev/null)
        STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
        MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
        echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
    else
        echo "||" > "$CACHE_FILE"
    fi
fi

IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

# Build git status
GIT_STATUS=""
[ -n "$BRANCH" ] && GIT_STATUS=" | 🌿 $BRANCH"
[ -n "$STAGED" ] && [ "$STAGED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${GREEN}+${STAGED}${RESET}"
[ -n "$MODIFIED" ] && [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${YELLOW}~${MODIFIED}${RESET}"

# Build complete first line (no pets)
DIR_NAME="${DIR##*/}"
CIRCLE=$(build_circle_progress "$PCT" "$BAR_COLOR")
# Add warning indicator at 75%+
WARNING_INDICATOR=""
[ "$PCT" -ge 75 ] && WARNING_INDICATOR=" ${BOLD}${BAR_COLOR}⚠${RESET}"

# Format operations counter (green if active)
OPS_ICON=""
[ "$OPS" -gt 0 ] && OPS_ICON="${GREEN}$OPS${RESET}"

# Get RAM usage
RAM_PCT=$(get_ram_usage)
RAM_COLOR=$(get_ram_color "$RAM_PCT")
RAM_ICON="🧠 ${RAM_COLOR}${RAM_PCT}%${RESET}"

LINE1="${CYAN}[$MODEL]${RESET} 📁 ${DIR_NAME}${GIT_STATUS}${ENV_HINT} | ${PCT}% context $CIRCLE${WARNING_INDICATOR} 💾 ${OPS_ICON} | ${RAM_ICON} | ⚡ ${TPS_FMT}"

echo -e "$LINE1"

# Output line 2: Progress bar, cost, duration, WARNING
LINE2="${BAR_COLOR}${BAR}${RESET} ${PCT}% | ${YELLOW}${COST_FMT}${RESET} | ⏱️ ${MINS}m ${SECS}s"
[ -n "$WARNING" ] && LINE2="${LINE2} | ${WARNING}"
echo -e "$LINE2"