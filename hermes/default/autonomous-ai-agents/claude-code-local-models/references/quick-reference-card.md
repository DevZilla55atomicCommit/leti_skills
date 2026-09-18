# Quick Reference Card — Claude Code + Ollama (2026)

## One-Command Setup

```bash
# Ollama v0.14.5+
ollama launch claude --model qwen3-coder
```

## Manual Env Vars (Session)

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export OLLAMA_CONTEXT_LENGTH=65536  # or 131072 for 128K models

claude --model qwen3-coder
```

## Persistent Settings (~/.claude/settings.json)

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "OLLAMA_CONTEXT_LENGTH": "131072",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_AUTO_COMPACT": "1"
  },
  "autoCompactEnabled": false,
  "model": "qwen3.5-128k:latest"
}
```

## Model Quick-Pick

| Need | Model | VRAM | Context |
|------|-------|------|---------|
| **Best coding** | `qwen3-coder` | 24 GB | 128K |
| **Fast + balanced** | `glm-4.7-flash` | 8 GB | 128K |
| **General purpose** | `gpt-oss:20b` | 13 GB | 128K |
| **Low VRAM** | `qwen2.5-coder:7b` | 4 GB | 32K |
| **No GPU** | `glm-4.7:cloud` | 0 GB | 128K |

## Auto-Compact Schedule (Manual)

| Context | Compact Every |
|---------|---------------|
| 32K | 8-10 turns |
| 64K | 20-25 turns |
| 128K | **35-40 turns** |

```bash
# In session:
/compact focus on current task

# Check status:
/context
/cost
```

## Verification Commands

```bash
ollama version                          # Must be 0.14.0+
curl -s http://localhost:11434/v1/models | jq '.data[].id'
ollama show <model> --parameters | grep num_ctx
claude --model <model>                  # Then run /status in session
```

## Common Fixes

| Error | Fix |
|-------|-----|
| Connection refused | `ollama serve` |
| Model not found | Exact name from `ollama list` (include `:latest`) |
| Context exceeded | Set `OLLAMA_CONTEXT_LENGTH`, disable auto-compact |
| Response stopped arriving | Context overflow — see above |
| Settings ignored | Use `claude --settings '{"model":"..."}'` to bypass cache |

---
**Sources:** Ollama Blog (Jan 16 2026), Ollama API Docs, Anthropic Claude Code Docs