# Tokens Per Second (TPS) — Live Rate Display

## Problem
Developers want to see real-time token consumption rate (tokens/second) to gauge model throughput and detect when context is filling rapidly.

## Solution
Calculate TPS from token delta between status-line refreshes (~1s interval).

## Implementation (Rolling Average — Fixes "Dead" 0/s Display)
```bash
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

# Format TPS
TPS_FMT=$(printf '%dk/s' $((TPS / 1000)))
[ "$TPS" -lt 1000 ] && TPS_FMT="${TPS}/s"
```

## Output Format
```
⚡ 919/s    # under 1K tokens/s
⚡ 1k/s     # 1000+ tokens/s
```
Prepended to line 1 after RAM indicator.

## How It Works
1. **TOKENS_USED** = calculated actual tokens (from local model context override)
2. **Cache** stores `tokens_used|timestamp_ms|prev_tps` per session
3. **Delta** = current - previous on each refresh
4. **Rate** = delta_tokens / delta_seconds
5. **Rolling average** = 70% previous + 30% new (prevents 0/s flicker when context static)
6. **Format** = human-readable (N/s or Nk/s)

## Key Fix: Rolling Average
**Before:** TPS reset to 0 when context unchanged (looked "dead")
**After:** TPS decays smoothly (1000 → 756 → 529 → 370) when context static

This works because:
- Context only updates when tokens added (after tool calls, user messages)
- Status line refreshes ~1s regardless
- Rolling average persists last meaningful rate

## Limitations
- **Only updates on status-line refresh** (~1s interval, controlled by Claude Code)
- **Shows input token rate** (what's sent to model), not generation speed
- **Sub-tasks invisible** — only tracks main conversation context
- **First call = 0/s** (no previous sample to compare)
- **Requires python3** for millisecond timestamp (macOS `date` lacks %3N)

## Cache File
- Location: `/tmp/statusline-tps-cache-{SESSION_ID}`
- Format: `TOKENS_USED|TIMESTAMP_MS|PREV_TPS`
- Auto-cleaned on session end (tmp)

## Testing
```bash
# First call (no cache) → 0/s
rm -f /tmp/statusline-tps-cache-test
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"context_window":{"used_percentage":10},"session_id":"test"}'

# Second call after 1s → shows rate
sleep 1
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"context_window":{"used_percentage":20},"session_id":"test"}'

# Third call with same context → shows decaying rate
sleep 1
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"context_window":{"used_percentage":20},"session_id":"test"}'
```