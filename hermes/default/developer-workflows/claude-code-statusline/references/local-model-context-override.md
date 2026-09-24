# Local Model Context Override — True Context Percentage for Ollama Models

## Problem
Claude Code's `context_window.used_percentage` is calculated against **Anthropic's 200K context window**. When using local models via Ollama (which have smaller contexts: 32K, 64K, 128K), the reported percentage is wildly inaccurate:

| Real Usage | Model Context | Anthropic Reports |
|------------|---------------|-------------------|
| 28K tokens | 32K (87%) | 14% (green, looks fine) |
| 100K tokens | 128K (78%) | 50% (green, looks fine) |
| 28K tokens | 32K (87%) | **Should show 87% yellow+warning** |

## Solution
Recalculate true percentage:
1. Extract Anthropic's percentage (assumes 200K base)
2. Calculate actual tokens used: `TOKENS_USED = ANTHROPIC_PCT * 200000 / 100`
3. Recalculate against local model's context: `TRUE_PCT = TOKENS_USED * 100 / LOCAL_CONTEXT`
4. Cap at 100%

## Auto-Detection from Model Name
```bash
case "$MODEL" in
    *32k*|*4b*) LOCAL_MODEL_CONTEXT=32768 ;;
    *48k*|*64k*|*9b*) LOCAL_MODEL_CONTEXT=65536 ;;
    *128k*|*31b*|*coder*) LOCAL_MODEL_CONTEXT=131072 ;;
    *) LOCAL_MODEL_CONTEXT=200000 ;;  # Default to Anthropic's 200K
else
```

## Manual Override (Highest Priority)
```bash
export LOCAL_MODEL_CONTEXT=32768   # 32K
export LOCAL_MODEL_CONTEXT=65536   # 64K
export LOCAL_MODEL_CONTEXT=131072  # 128K
export LOCAL_MODEL_CONTEXT=8192    # 8K (phi3, etc.)
export LOCAL_MODEL_CONTEXT=262144  # 256K (future)
claude
```

## Coverage Table
| Pattern | Context | Examples |
|---------|---------|----------|
| `*32k*` or `*4b*` | 32,768 | `qwen3.5-32k:latest`, `qwen3.5:4b-mlx`, `gemma2:4b` |
| `*48k*`, `*64k*`, `*9b*` | 65,536 | `qwen3.5-48k:latest`, `qwen3.5-64k:latest`, `qwen3.5:9b` |
| `*128k*`, `*31b*`, `*coder*` | 131,072 | `qwen3.5-128k:latest`, `gemma4:31b-cloud`, `qwen3-coder` |
| **Everything else** | 200,000 | Anthropic models, unknown names |

## Gaps in Auto-Detection
| Model | Issue |
|-------|-------|
| `qwen2.5:7b` (7B, 32K ctx) | Doesn't match `*4b*` or `*9b*` |
| `llama3.1:8b` (8B, 128K ctx) | Doesn't match patterns |
| `phi3:14b` (14B, 4K/8K ctx) | Unusual context size |
| New models with custom names | No pattern match |

**Recommendation**: Always set `export LOCAL_MODEL_CONTEXT=XXXXX` in shell config for certainty.

## Implementation Snippet
```bash
# Extract Anthropic's percentage
ANTHROPIC_PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Determine local context
LOCAL_MODEL_CONTEXT="${LOCAL_MODEL_CONTEXT:-}"
if [ -z "$LOCAL_MODEL_CONTEXT" ]; then
    case "$MODEL" in
        *32k*|*4b*) LOCAL_MODEL_CONTEXT=32768 ;;
        *48k*|*64k*|*9b*) LOCAL_MODEL_CONTEXT=65536 ;;
        *128k*|*31b*|*coder*) LOCAL_MODEL_CONTEXT=131072 ;;
        *) LOCAL_MODEL_CONTEXT=200000 ;;
    esac
fi

# Recalculate true percentage
if [ "$LOCAL_MODEL_CONTEXT" -ne 200000 ] && [ "$ANTHROPIC_PCT" -gt 0 ]; then
    TOKENS_USED=$((ANTHROPIC_PCT * 200000 / 100))
    PCT=$((TOKENS_USED * 100 / LOCAL_MODEL_CONTEXT))
    [ "$PCT" -gt 100 ] && PCT=100
else
    PCT=$ANTHROPIC_PCT
    TOKENS_USED=$((ANTHROPIC_PCT * 200000 / 100))
fi
```

## Testing
```bash
# Test 32K model with 14% Anthropic → 85% true
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"context_window":{"used_percentage":14}}' | ~/.claude/statusline.sh

# Test 128K model with 50% Anthropic → 76% true
echo '{"model":{"display_name":"qwen3.5-128k:latest"},"context_window":{"used_percentage":50}}' | ~/.claude/statusline.sh

# Test manual override 64K with 50% Anthropic → 100% true
LOCAL_MODEL_CONTEXT=65536 echo '{"model":{"display_name":"custom"},"context_window":{"used_percentage":50}}' | ~/.claude/statusline.sh
```