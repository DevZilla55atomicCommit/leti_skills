# Error: "API Error: The response stopped arriving" — Diagnosis & Fix

**Context:** User encountered this error in Claude Code while using `qwen3.5-128k:latest` via Ollama after ~9 minutes of execution.

## Root Cause: Context Window Overflow

| Component | Limit |
|-----------|-------|
| Model (`qwen3.5-128k`) | 128K tokens (131,072) |
| Claude Code auto-compact trigger | ~140K-170K tokens (70-85% of Anthropic's 200K) |
| **Result** | Model hits hard limit **before** auto-compact runs → stream cuts off mid-response |

## Why 9 Minutes?

The session accumulated context over many turns. Each turn adds ~2-3K tokens. At ~35-40 turns, the 128K limit is reached. The model cannot generate more tokens, so the streaming response terminates abruptly.

## Evidence

- Error: `API Error: The response stopped arriving. The response above may be incomplete.`
- Task ran for 9m 25s (many turns)
- Model: `qwen3.5-128k:latest` (128K context)
- No proxy involved — direct Ollama Anthropic endpoint

## Fix (Applied in Session)

### 1. Disable Built-in Auto-Compact

```json
// ~/.claude/settings.json
{
  "autoCompactEnabled": false,
  "env": {
    "DISABLE_AUTO_COMPACT": "1"
  }
}
```

### 2. Set Ollama Context Length Explicitly

```bash
export OLLAMA_CONTEXT_LENGTH=131072  # 128K for qwen3.5-128k
```

### 3. Manual Compact Schedule

| Model Context | Compact Every N Turns |
|---------------|----------------------|
| 32K | 8-10 |
| 64K | 20-25 |
| 128K | **35-40** |

```bash
# In session:
/compact focus on current task
```

### 4. Verify Context Before Session

```bash
ollama show qwen3.5-128k:latest --parameters | grep num_ctx
# Should output: 131072
```

## Prevention Checklist

- [ ] `OLLAMA_CONTEXT_LENGTH` set in shell profile / settings.json
- [ ] `autoCompactEnabled: false` in settings.json
- [ ] `DISABLE_AUTO_COMPACT=1` in env
- [ ] Model name matches `ollama list` exactly (including `:latest` tag)
- [ ] Manual `/compact` every ~35 turns for 128K models
- [ ] Monitor with `/context` and `/cost` commands

## Related Files

- `references/ollama-anthropic-compatibility.md` — Official Ollama Anthropic API docs
- `references/auto-compact-config.md` — Auto-compact configuration guide
- `scripts/claude-auto-compact.sh` — Tmux wrapper for automated compacting
- `scripts/claude-token-watch.sh` — Background token monitor