---
name: claude-code-statusline
description: Custom status line configuration for Claude Code with context window progress, git status, cost tracking, and warnings
tags: [claude-code, statusline, shell, bash, customization]
related_skills: [claude-code, developer-workflows]
---

# Claude Code Custom Status Line

Configure a custom status line for Claude Code that displays context window usage with a circular progress indicator, git status, cost tracking, and warning thresholds.

## Overview

The status line is a customizable bar at the bottom of Claude Code that runs a shell script you configure. It receives JSON session data on stdin and displays whatever your script prints.

**Official Documentation:** https://docs.anthropic.com/en/docs/claude-code/customize-status-line

## Configuration

Add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "enabled": true
  }
}
```

## Available Data Fields

Claude Code sends these JSON fields to your script via stdin:

| Field | Description |
|-------|-------------|
| `model.id`, `model.display_name` | Current model identifier and display name |
| `cwd`, `workspace.current_dir` | Current working directory |
| `workspace.project_dir` | Project root directory |
| `cost.total_cost_usd` | Estimated session cost in USD |
| `cost.total_duration_ms` | Total wall-clock time |
| `context_window.used_percentage` | Pre-calculated percentage of context used |
| `context_window.remaining_percentage` | Pre-calculated percentage remaining |
| `rate_limits.five_hour/seven_day` | Subscription rate limit usage |

## Our Custom Status Line Script

Located at: `~/.claude/statusline.sh`

### Features

1. **Context window percentage** - Shows `used_percentage` on line 1
2. **Circular progress indicator** - 8-segment circle (12.5% per segment) using Unicode quadrant arcs
3. **Color thresholds** matching the linear progress bar:
   - Green (< 70%): ●○○○○○○○
   - Yellow (70-89%): ●●●●●●○○
   - Red (≥ 90%): ●●●●●●●○
4. **75% warning indicator** - ⚠ appears at 75%+ in matching color
5. **Git status** - Cached branch name, staged (+N), modified (~N)
6. **Cost tracking** - Session cost in USD (yellow)
7. **Duration** - Wall-clock time (stopwatch emoji)
8. **Local model context override** - Auto-detects context size from model name (`*32k*`→32K, `*64k*`/`*9b*`→64K, `*128k*`/`*coder*`→128K) or manual override via `LOCAL_MODEL_CONTEXT` env var. Recalculates true percentage against local model's actual context (not Anthropic's 200K).
9. **RAM memory pressure** - Shows 🧠 XX% with color thresholds: Green <60%, Magenta 60-74%, Yellow 75-89%, Red ≥90%. Uses macOS `memory_pressure` (preferred) or `vm_stat` fallback. Calculates USED % = 100 - free %.
10. **Tokens per second (TPS)** - Live ⚡ TPS rate calculated from token delta between status-line refreshes. Caches `tokens_used|timestamp|prev_tps` to `/tmp/statusline-tps-cache-$SESSION_ID`. Formats as `N/s` (<1K) or `Nk/s` (≥1K). Uses **rolling average (70% old + 30% new)** so TPS smoothly decays when context is static instead of flickering to 0/s.

**Note:** Floating 3D robot pet and cloud emoji were removed per user preference (cleaner status line). See `references/floating-3d-robot-pet.md` for the implementation if needed later.

### Color Thresholds

| Percentage | Bar Color | Circle Color | Warning |
|------------|-----------|--------------|---------|
| 0-69% | Green (32) | Green (32) | None |
| 70-74% | Yellow (33) | Yellow (33) | None |
| 75-89% | Yellow (33) | Yellow (33) | ⚠ 75% CONTEXT USED |
| 90%+ | Red (31) | Red (31) | ⚠ TOKEN LIMIT NEARING! |

### Example Output

```
[qwen3.5-32k:latest] 📁 Mission_Control_ALL-Agents | 🌿 main | 75% context ●●●●●●○○ 75% ⚠
▓▓▓▓▓▓▓░░░ 75% | $0.56 | ⏱️ 7m 15s | ⚠ 75% CONTEXT USED
```

### Script Structure

```bash
#!/bin/bash
# Read JSON from stdin
input=$(cat)

# Extract fields with fallbacks
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
DIR=$(echo "$input" | jq -r '.workspace.current_dir // "~"')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

# Build circular progress (8 segments = 12.5% each)
build_circle_progress() {
    local pct=$1
    local color=$2
    local filled=$((pct * 8 / 100))
    # ... segment logic
}

# Color logic
if [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"; ...
elif [ "$PCT" -ge 75 ]; then BAR_COLOR="$YELLOW"; ...

# Git caching (5s TTL per session)
# ... cache to /tmp/statusline-git-cache-$SESSION_ID

# Output two lines
echo -e "Line 1: model, dir, git, percentage, circle, warning"
echo -e "Line 2: bar, percentage, cost, duration, warning"
```

## Key Implementation Details

### Git Caching
- Cache file: `/tmp/statusline-git-cache-$SESSION_ID`
- TTL: 5 seconds
- Uses `stat -c %Y` (Linux) or `stat -f %m` (macOS) for mtime
- Avoids `git status` on every refresh (performance)

### Unicode Characters
- Circle segments: ● (filled), ○ (empty)
- Progress bar: ▓ (filled), ░ (empty)
- Icons: 📁 (folder), 🌿 (git branch), ⏱️ (stopwatch), ⚠ (warning)

### Color Codes
```bash
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'
BOLD='\033[1m'
```

## Testing the Script

```bash
# Mock 75% usage
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"workspace":{"current_dir":"/Users/alfredkamisese/Projects/test"},"context_window":{"used_percentage":75},"cost":{"total_cost_usd":0.56,"total_duration_ms":435000},"session_id":"test-123"}' | ~/.claude/statusline.sh

# Test different percentages
for p in 13 25 50 75 90 100; do
  echo "{\"model\":{\"display_name\":\"test\"},\"workspace\":{\"current_dir\":\"/test\"},\"context_window\":{\"used_percentage\":$p},\"cost\":{\"total_cost_usd\":0.10,\"total_duration_ms\":60000},\"session_id\":\"test\"}" | ~/.claude/statusline.sh
done
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Status line not appearing | Run `chmod +x ~/.claude/statusline.sh` |
| Colors not showing | Terminal must support ANSI escape codes |
| Unicode chars show as boxes | Use a font with good Unicode coverage (JetBrains Mono, Fira Code, etc.) |
| Script errors | Run with `claude --debug` to see stderr |
| Git status slow | Check cache TTL and cache file permissions |
| **Pet renders as multi-line ASCII art** | Status line is single-line only — replace multi-line `cat <<'EOF'` blocks with single-line Unicode frames (quadrant/half-block chars) |
| **`declare -A` invalid option** | macOS ships bash 3.2; associative arrays require bash 4+. Use indexed arrays (`ARRAY=(...)`) instead |
| **Pet doesn't animate** | Ensure frame index advances on each call: `INDEX=$(( (INDEX + 1) % ${#FRAMES[@]} ))` |
| **Empty color variable** | Function uses `${output}` but never sets it — use `${frame}` directly

## Related Configuration Options

### settings.json Format (Critical - must match exactly)

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "enabled": true
  }
}
```

**Important:** The `statusLine` object requires:
- `type`: Must be `"command"` (not "script" or "inline")
- `command`: Path to executable script (supports `~` expansion)
- `enabled`: `true` to activate (optional, defaults to true)

**Invalid config** (causes "Files with errors are skipped entirely" error):
```json
{
  "statusLine": {
    "enabled": true,
    "showAgentInfo": true,
    "showTokenWarning": true,
    "tokenWarningThresholdPct": 75
  }
}
```
These fields (`enabled`, `showAgentInfo`, etc.) are NOT valid for `statusLine` - they belong to other config sections.

### Optional Fields
- `padding`: Extra horizontal spacing (default 0)
- `refreshInterval`: Minimum 1 second, re-runs script on timer
- `hideVimModeIndicator`: Hide built-in `-- INSERT --` indicator

## Git Cache Pattern

The script caches git status to `/tmp/statusline-git-cache-{SESSION_ID}` with 5-second TTL. The `session_id` comes from the JSON input, ensuring each Claude Code session has its own cache file. This prevents:
- Cross-session cache pollution
- Stale git status when switching projects
- Excessive `git status` calls (performance)

Cache format: `branch|staged_count|modified_count` (e.g., `main|2|3`)