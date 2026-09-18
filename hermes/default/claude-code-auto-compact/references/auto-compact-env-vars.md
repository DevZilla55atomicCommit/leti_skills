# Auto-Compact Environment Variables Reference

## Required Variables for Ollama/Local Models

| Variable | Value | Purpose |
|----------|-------|---------|
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | 75% of model context | Triggers auto-compact at ~80% of this value |
| `CLAUDE_CODE_MAX_CONTEXT_LENGTH` | 100% of model context | Hard stop / actual window size |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | Match MAX_OUTPUT_TOKENS | Compaction window alignment |
| `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT` | `1` | Disable 200k default assumption |
| `ANTHROPIC_BASE_URL` | `http://localhost:11434` | Ollama endpoint |
| `ANTHROPIC_AUTH_TOKEN` | `ollama` | Auth token |
| `ANTHROPIC_API_KEY` | `ollama` | API key |
| `OLLAMA_CONTEXT_LENGTH` | Model context (e.g., 131072) | Ollama native context |

## Model-Specific Values

| Model | Context | MAX_OUTPUT_TOKENS (75%) | MAX_CONTEXT_LENGTH | AUTO_COMPACT_WINDOW |
|-------|---------|------------------------|-------------------|---------------------|
| qwen3.5-32k:latest | 32768 | 24000 | 32768 | 24000 |
| qwen3.5-48k:latest | 49152 | 36000 | 49152 | 36000 |
| qwen3.5-64k:latest | 65536 | 48000 | 65536 | 48000 |
| qwen3.5-96k:latest | 98304 | 72000 | 98304 | 72000 |
| qwen3.5-128k:latest | 131072 | 96000 | 131072 | 96000 |
| qwen3.5:9b (128k ctx) | 131072 | 96000 | 131072 | 96000 |

## RAM Budget Guidance (16 GB Apple Silicon)

| Model | Context | Est. Resident | Free RAM | Verdict |
|-------|---------|--------------|----------|---------|
| qwen3.5-96k | 98304 | ~6 GB | ~35% | ✅ Stable daily driver |
| qwen3.5:9b | 131072 | ~9.4 GB | ~8% | ❌ Thrash / overload |
| qwen3.5-128k | 131072 | ~9–10 GB | ~8% | ❌ Thrash / overload |

**Rule:** anchor the default model + settings trio to the largest model that leaves ≥20% free RAM. Accept early compaction on larger models when switching via picker; do not size the trio to a model that starves the system.

## Key Rules

1. **MAX_OUTPUT_TOKENS = 75% of context** — Auto-compact triggers at ~80% of this (≈60% of actual context)
2. **MAX_CONTEXT_LENGTH = 100% of context** — The actual hard limit
3. **AUTO_COMPACT_WINDOW = MAX_OUTPUT_TOKENS** — Keep them aligned
4. **Never exceed actual context** — Values > actual context prevent auto-compact from triggering

## Auto-Compact Default (Recommended)

```json
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "16384",
    "CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT": "1",
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "ollama",
    "OLLAMA_CONTEXT_LENGTH": "98304"
  },
  "autoCompactEnabled": true,
  "model": "qwen3.5-96k:latest"
}
```

*Remove `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS` — let auto tune to loaded model.*