---
name: claude-code-ollama-integration
description: Run Claude Code CLI with Ollama via Anthropic API.
---

# Claude Code + Ollama Integration

Guide for running Anthropic's Claude Code CLI with Ollama's Anthropic-compatible API endpoint.

## Critical Constraints

**Ollama Anthropic API only supports official registry models.** Local models pulled via `ollama pull` (e.g., `qwen3.5-128k:latest`, `qwen2.5-coder:7b`) return `unrecognized_model` error. **Local models CANNOT be used with the `claude` CLI at all** — they work with `ollama run` but not the Anthropic-compatible endpoint. Only official Ollama models work:

| Model | Type | Use Case |
|-------|------|----------|
| `gpt-oss:20b` | Cloud | General coding |
| `qwen3-coder` | Cloud | Coding-focused |
| `gemma4:31b-cloud` | Cloud | General coding (31B) |
| `deepseek-v4-flash:0731-cloud` | Cloud | Fast auto-mode classifier |
| `nemotron-3-ultra:cloud` | Cloud | Reasoning-heavy tasks |
| `glm-5.2:cloud` | Cloud | Large context |

**Local MLX/quantized models will NOT work** with the `claude` CLI, even if they run fine via `ollama run`.

## Required Environment Setup

```bash
# ~/.zshrc or ~/.bashrc
export OLLAMA_HOST=0.0.0.0:11434
export ANTHROPIC_BASE_URL=http://localhost:11434/v1
export ANTHROPIC_API_KEY=ollama
export ANTHROPIC_AUTH_TOKEN=ollama

# Auto-mode classifier (fast cloud model for safety checks)
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash:0731-cloud
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-flash:0731-cloud
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-flash:0731-cloud
```

## Starting Ollama

```bash
pkill ollama
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &
```

## Running Claude Code

### Print Mode (Recommended)
```bash
# Use cloud model for coding, fast cloud model for auto-mode
claude -p "your task" --model gemma4:31b-cloud --agent Avengers --max-turns 20
```

### Interactive Mode (tmux)
```bash
# Start tmux session
terminal(command="tmux new-session -d -s claude-work -x 160 -y 50")

# Launch Claude Code with cloud model
terminal(command="tmux send-keys -t claude-work 'cd /project && claude --model gemma4:31b-cloud' Enter")

# Handle trust dialog (first time only)
terminal(command="sleep 4 && tmux send-keys -t claude-work Enter")

# Send task
terminal(command="tmux send-keys -t claude-work 'your task' Enter")
```

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `unrecognized_model` | Using local model with `claude` CLI | Switch to official cloud model (gemma4:31b-cloud, deepseek-v4-flash:0731-cloud, etc.) |
| `unknown option '--task'` | `--task` flag doesn't exist | Use print mode: `claude -p "prompt" --model MODEL --agent AGENT` |
| Classifier timeout | Slow local model for auto-mode | Set `ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash:0731-cloud` |
| Connection refused | Ollama on localhost only | `export OLLAMA_HOST=0.0.0.0:11434` before `ollama serve` |
| Trust dialog blocks | First run in directory | Send `Enter` after 4s via tmux |

## Model Selection Guide

| Need | Coding Model | Classifier (Auto-Mode) |
|------|--------------|------------------------|
| General coding | `gemma4:31b-cloud` | `deepseek-v4-flash:0731-cloud` |
| Heavy reasoning | `nemotron-3-ultra:cloud` | `deepseek-v4-flash:0731-cloud` |
| Large context | `glm-5.2:cloud` | `deepseek-v4-flash:0731-cloud` |
| Fast/cheap | `deepseek-v4-flash:0731-cloud` | `gemma4:31b-cloud` |

## Verification

```bash
# Test model works with Anthropic API
curl -v http://localhost:11434/v1/messages \
  -H "x-api-key: ollama" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"gemma4:31b-cloud","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

Should return JSON response, not `unrecognized_model`.
