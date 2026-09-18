# Ollama Model Mapping for Claude Code

## Your Ollama Models (from `ollama list`)

| Ollama Model Name | Use Case | Notes |
|-------------------|----------|-------|
| `claude-sonet-4.6:latest` | General coding, best balance | Primary workhorse |
| `claude-opus-4.8:latest` | Complex reasoning, architecture | Slower, more capable |
| `qwen3.5:9b` | Fast coding, good quality | Good default |
| `qwen3.5:4b-mlx` | Very fast, lower quality | Quick tasks |
| `gemma4:12b-mlx` | Alternative | Apple Silicon optimized |
| `gemma4:e4b-mlx` | Efficient | |
| `qwen3.5-128k:latest` | Long context | 128k context window |
| `qwen3.5-64k:latest` | Long context | 64k context window |
| `qwen3.5-48k:latest` | Long context | 48k context window |
| `qwen3.5-32k:latest` | Long context | 32k context window |
| `nomic-embed-text:latest` | Embeddings only | Not for generation |

## Claude Code Aliases → Ollama Mapping (DOES NOT WORK AUTOMATICALLY)

| Claude Code Alias | What It Tries | Result with Ollama |
|-------------------|---------------|-------------------|
| `sonnet` | `claude-sonnet-4-6` (Anthropic) | ❌ 404 |
| `haiku` | `claude-haiku-4-5-20251001` (Anthropic) | ❌ 404 |
| `opus` | `claude-opus-4-8` (Anthropic) | ❌ 404 |
| `fable` | `claude-fable-5` (Anthropic) | ❌ 404 |

## Correct Usage in Delegation

```python
# ❌ WRONG - will hang/404
delegate_task(goal="...", context="--model sonnet")

# ✅ CORRECT - explicit Ollama name
delegate_task(goal="...", context="--model claude-sonet-4.6:latest")

# ✅ ALSO WORKS - faster model
delegate_task(goal="...", context="--model qwen3.5:9b")
```

## Recommended Defaults

```bash
# Best all-around
DEFAULT_MODEL="claude-sonet-4.6:latest"

# Fast/cheap
FAST_MODEL="qwen3.5:9b"

# Complex reasoning
REASONING_MODEL="claude-opus-4.8:latest"

# Long context
LONG_CONTEXT_MODEL="qwen3.5-128k:latest"
```

## Verify Models at Runtime

```bash
# List available
ollama list

# Or via API
curl -s http://localhost:11434/api/tags | jq -r '.models[].name'
```

## Add to ~/.claude/settings.json for Convenience

```json
{
  "model": "claude-sonet-4.6:latest",
  "available_models": [
    "claude-sonet-4.6:latest",
    "claude-opus-4.8:latest",
    "qwen3.5:9b",
    "qwen3.5-128k:latest",
    "gemma4:12b-mlx"
  ]
}
```