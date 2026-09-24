# Custom Status Line Configuration for Claude Code

This document describes how to configure a custom status line for Claude Code that displays context window usage, cost, duration, git status, and warnings.

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

Or use inline command:
```json
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\(.model.display_name)] \\(.context_window.used_percentage // 0)%\"'"
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
| `workspace.added_dirs` | Additional directories added via `/add-dir` |
| `workspace.git_worktree` | Git worktree name |
| `workspace.repo.host/owner/name` | Git remote info |
| `cost.total_cost_usd` | Estimated session cost in USD |
| `cost.total_duration_ms` | Total wall-clock time |
| `cost.total_api_duration_ms` | Time waiting for API responses |
| `context_window.total_input_tokens` | Input tokens in context window |
| `context_window.total_output_tokens` | Output tokens in context window |
| `context_window.context_window_size` | Max context window size (200k or 1M) |
| `context_window.used_percentage` | Pre-calculated percentage of context used |
| `context_window.remaining_percentage` | Pre-calculated percentage remaining |
| `context_window.current_usage` | Per-component token breakdown |
| `exceeds_200k_tokens` | Whether total tokens > 200k |
| `fast_mode` | Whether fast mode is enabled |
| `effort.level` | Current reasoning effort level |
| `rate_limits.five_hour/seven_day` | Subscription rate limit usage |

## Our Custom Status Line Script

Located at: `~/.claude/statusline.sh` (copy from `scripts/statusline.sh`)

### Features

1. **Context window percentage** - Shows `used_percentage` on line 1
2. **Circular progress indicator** - 8-segment circle (12.5% per segment) using Unicode quadrant arcs:
   - ◷ (bottom-right), ◶ (bottom-left), ◵ (top-left), ◴ (top-right)
   - Fills clockwise from bottom-right
3. **Color thresholds** matching the linear progress bar:
   - Green (< 70%): ◷◶◵◴
   - Yellow (70-89%): ◷◶◵◴
   - Red (≥ 90%): ◷◶◵◴
4. **75% warning indicator** - ⚠ appears at 75%+ in matching color
5. **Git status** - Cached branch name, staged (+N), modified (~N)
6. **Cost tracking** - Session cost in USD (yellow)
7. **Duration** - Wall-clock time (stopwatch emoji)
8. **Local model context override** - Auto-detects context size from model name (`*32k*`→32K, `*64k*`/`*9b*`→64K, `*128k*`/`*coder*`→128K) or manual override via `LOCAL_MODEL_CONTEXT` env var. Recalculates true percentage against local model's actual context (not Anthropic's 200K). See `references/local-model-context-override.md`.
9. **Floating 3D robot pet** - Single-line inline pet using Unicode quadrant/half-block chars (`◤◢◣◢▀▄`) that cycles through states: IDLE (cyan), THINKING (yellow), SUCCESS (green), FAIL (red), TYPING (cyan) — advances frame on each status-line refresh (~1s). See `references/floating-3d-robot-pet.md`.
10. **RAM memory pressure** - Shows 🧠 XX% with color thresholds: Green <60%, Magenta 60-74%, Yellow 75-89%, Red ≥90%. Uses macOS `memory_pressure` (preferred) or `vm_stat` fallback. Calculates USED % = 100 - free %. See `references/ram-memory-pressure.md`.
11. **Tokens per second (TPS)** - Live ⚡ TPS rate calculated from token delta between status-line refreshes. Caches `tokens_used|timestamp` to `/tmp/statusline-tps-cache-$SESSION_ID`. Formats as `N/s` (<1K) or `Nk/s` (≥1K). See `references/tokens-per-second.md`.

### Color Thresholds

| Percentage | Bar Color | Circle Color | Warning |
|------------|-----------|--------------|---------|
| 0-69% | Green (32) | Green (32) | None |
| 70-74% | Yellow (33) | Yellow (33) | None |
| 75-89% | Yellow (33) | Yellow (33) | ⚠ 75% CONTEXT USED |
| 90%+ | Red (31) | Red (31) | ⚠ TOKEN LIMIT NEARING! |

### Example Output

```
[qwen3.5-32k:latest] 📁 Mission_Control_ALL-Agents | 🌿 main | 75% context ◷◶◵◴◷◶○○ 75% ⚠
▓▓▓▓▓▓▓░░░ 75% | $0.56 | ⏱️ 7m 15s | ⚠ 75% CONTEXT USED
```

## Script Files

- `scripts/statusline.sh` - Main status line script (copy to `~/.claude/statusline.sh` and make executable)
- `scripts/test-statusline.sh` - Test script with various percentage scenarios

## Installation

```bash
# Copy script to Claude config directory
cp scripts/statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh

# Add to settings.json
cat > ~/.claude/settings.json << 'EOF'
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  },
  "model": "qwen3.5-32k:latest",
  "effortLevel": "medium",
  "promptSuggestionEnabled": false,
  "theme": "dark",
  "verbose": false,
  "switchModelsOnFlag": true,
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "enabled": true
  }
}
EOF
```

## Testing

Run the test script to verify all color thresholds:

```bash
bash scripts/test-statusline.sh
```

This tests percentages: 13%, 25%, 50%, 69%, 70%, 75%, 89%, 90%, 100%