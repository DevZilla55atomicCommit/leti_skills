# Floating 3D Robot Pet — Single-Line Implementation

## Problem
CLI status lines have **zero vertical space** — only one line. Multi-line ASCII art (7-8 lines) breaks the status line layout.

## Solution
Use **Unicode quadrant/half-block characters** to simulate 3D depth on a single line, cycling frames on each refresh (~1s).

## Frame Set
```bash
ROBOT_PET_STATES=(
  "◤◢◣◢"  # idle - subtle breathing
  "◤▀◣◢"  # thinking - processing (top half shaded)
  "◤✓◣◢"  # success - checkmark
  "◤✗◣◢"  # fail - error
  "◤⌨◣◢"  # typing - keyboard
  "◤◢◣◢"  # idle variant
  "◤▄◣◢"  # idle variant (bottom half shaded)
)
```

## State Detection
```bash
if echo "$input" | grep -q '"thinking"'; then
    state="thinking"
elif echo "$input" | grep -qE '"result":"error"|"success":false|failed'; then
    state="fail"
elif echo "$input" | grep -qE '"id":|"result":.*true|completed'; then
    state="success"
elif echo "$input" | grep -q 'tool_runner\|tool_call'; then
    state="typing"
else
    state="idle"
fi
```

## Color Mapping
| State | ANSI Code | Color |
|-------|-----------|-------|
| success | `\033[92m` | Bright green |
| fail | `\033[91m` | Bright red |
| thinking | `\033[93m` | Bright yellow |
| typing | `\033[96m` | Bright cyan |
| idle | `\033[36m` | Cyan |

## Key Patterns
- **Indexed arrays** (`ARRAY=(...)`) — works on bash 3.2 (macOS default)
- **Frame advance** — `INDEX=$(( (INDEX + 1) % ${#FRAMES[@]} ))`
- **Direct frame output** — `echo -e "\033[COLORm${frame}\033[0m"` (not `${output}`)

## Unicode Characters Used
| Char | Name | Purpose |
|------|------|---------|
| `◤` | Quadrant upper-left | Top-left 3D corner |
| `◢` | Quadrant upper-right | Top-right 3D corner |
| `◣` | Quadrant lower-right | Bottom-right 3D corner |
| `◥` | Quadrant lower-left | Bottom-left 3D corner |
| `▀` | Upper half block | Top shading (thinking) |
| `▄` | Lower half block | Bottom shading (idle variant) |
| `✓` | Checkmark | Success state |
| `✗` | Cross mark | Fail state |
| `⌨` | Keyboard | Typing state |

## Testing
```bash
# Idle
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":50},"cost":{"total_cost_usd":0.1,"total_duration_ms":60000},"session_id":"test"}'

# Thinking
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":50},"cost":{"total_cost_usd":0.1,"total_duration_ms":60000},"session_id":"test","thinking":true}'

# Success
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":50},"cost":{"total_cost_usd":0.1,"total_duration_ms":60000},"session_id":"test","result":true,"success":true}'

# Fail
~/.claude/statusline.sh <<<'{"model":{"display_name":"test"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":50},"cost":{"total_cost_usd":0.1,"total_duration_ms":60000},"session_id":"test","result":"error"}'
```