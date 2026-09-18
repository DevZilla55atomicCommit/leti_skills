---
name: claude-code-statusline-customization
version: 1.0.0
author: Maddie
license: MIT
description: Use when customizing statusline with TPS colors and blink.
---

# Claude Code Statusline Customization Skill

**Use when:** Customizing the `~/.claude/statusline.sh` for TPS monitoring, color coding, blink animations, and custom colors.

## Prerequisites

- `~/.claude/statusline.sh` exists and is executable
- `jq` installed for JSON parsing
- Python 3 available for millisecond timestamps
- `~/.claude/settings.json` has `statusLine.command` set to `~/.claude/statusline.sh`

## Core Patterns

### 1. TPS Thresholds & Color Coding

```bash
TPS_LOW_THRESHOLD=15    # Below = orange
TPS_MID_THRESHOLD=35    # Below = green, above = custom blue
CUSTOM_BLUE='\033[38;2;72;202;228m'  # #48cae4
ELECTRIC_BLUE='\033[38;5;39m'
```

### 2. Color Variables

```bash
CUSTOM_BLUE='\033[38;2;72;202;228m'   # #48cae4
ELECTRIC_BLUE='\033[38;5;39m'
ORANGE='\033[38;5;208m'
GREEN='\033[32m'
BLUE='\033[34m'
RED='\033[31m'
YELLOW='\033[33m'
MAGENTA='\033[35m'
CYAN='\033[36m'
RESET='\033[0m'
BOLD='\033[1m'
BLINK_ON='\033[5m'
BLINK_OFF='\033[25m'
```

### 3. TPS Color Logic

```bash
TPS_ICON="⚡"
if [ "$TPS" -lt "$TPS_LOW_THRESHOLD" ]; then
    TPS_ICON_COLOR="$ORANGE"
elif [ "$TPS" -lt "$TPS_MID_THRESHOLD" ]; then
    TPS_ICON_COLOR="$GREEN"
else
    TPS_ICON_COLOR="$CUSTOM_BLUE"
fi
TPS_NUM_COLOR="$ELECTRIC_BLUE"
TPS_NUM_BLINK="$BLINK_ON"
```

### 4. Blink Animation

```bash
BLINK_ON='\033[5m'
BLINK_OFF='\033[25m'
TPS_NUM_BLINK="$BLINK_ON"
```

### 5. Output Formatting

```bash
TPS_NUM_COLOR="$ELECTRIC_BLUE"
TPS_NUM_BLINK="$BLINK_ON"
TPS_ICON="⚡"
LINE1="... | ${TPS_NUM_BLINK}${TPS_NUM_COLOR}${TPS_FMT}${RESET} ${TPS_ICON_COLOR}${TPS_ICON}${RESET}"
```

## Threshold Guidelines

| Model | LOW | MID |
|-------|-----|-----|
| qwen3.5-96k | 15 | 35 |
| qwen3.5-128k | 20 | 45 |
| qwen3.5-48k | 10 | 25 |

## Common Pitfalls

1. Blink not visible — Terminal must support ANSI blink (`\033[5m`). Enable in terminal settings.
2. Custom colors not rendering — Terminal must support 24-bit color (`\033[38;2;R;G;Bm`).
3. TPS cache not updating — Cache file uses `$SESSION_ID`. Ensure `SESSION_ID` is extracted.
4. TPS spikes on first render — Rolling average (70/30) smooths this.
5. Model name parsing — `LOCAL_MODEL_CONTEXT` auto-detection uses model name patterns.

## Settings Integration

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

Tilde expansion works; absolute paths do NOT.

## Related Skills
- [[claude-code-auto-compact]] — Auto-compact configuration for local models
- [[claude-code-settings-overview]] — Comprehensive settings guide