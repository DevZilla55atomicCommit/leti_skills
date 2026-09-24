---
name: claude-code-local-models
description: "Configure and run Claude Code with local models (Ollama) including auto-compact workarounds for small context windows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Ollama, Local-LLM, Auto-Compact, Context-Management]
    related_skills: [claude-code, hermes-agent, custom-llm-providers]
---

# Claude Code with Local Models (Ollama) — Auto-Compact & Context Management

This skill covers the specific challenges and workarounds for running Claude Code with local models via Ollama, where context windows (32K-128K) are far smaller than Anthropic's 200K, making the built-in auto-compact ineffective or harmful.

## Prerequisites

- Ollama **v0.14.0+** (Jan 16, 2026) — native Anthropic Messages API at `/v1/messages`
- Model pulled: `ollama pull qwen3-coder` (or your preferred model)
- Claude Code installed: `npm install -g @anthropic-ai/claude-code`

## The Core Problem

Claude Code's auto-compact triggers at **~70-85% of Anthropic's 200K context** (~140K-170K tokens). Local models have much smaller contexts:

| Model | Context Window | Auto-Compact Triggers | Result |
|-------|---------------|----------------------|--------|
| Anthropic Sonnet/Opus | 200K | ~140K-170K | Works perfectly |
| qwen3.5:4b (default) | 32K-128K | ~140K-170K | **Fails — model limit hit first** |
| qwen3.5:9b | 128K | ~140K-170K | **Fails — same issue** |
| llama3.1:8b/70b | 128K | ~140K-170K | **Fails — same issue** |
| qwen3-coder | 128K | ~140K-170K | **Fails — same issue** |
| glm-4.7-flash | 128K | ~140K-170K | **Fails — same issue** |

**No configurable threshold exists** (`autoCompactThreshold` is not a setting).

## Key Breakthrough: Ollama v0.14.0+ Native Anthropic Compatibility

**Since January 16, 2026, Ollama speaks Anthropic Messages API natively.** No proxy, no LiteLLM, no translation layer needed.

- Endpoint: `http://localhost:11434/v1/messages`
- Full streaming, tools, vision, thinking, system prompts supported
- Only missing: prompt caching (per Ollama docs)
- See: https://ollama.com/blog/claude and https://docs.ollama.com/api/anthropic-compatibility

## Local vs Cloud: Both Work on Modern Ollama (v0.34 Verified)

**Local GGUF models pulled via `ollama pull` WORK with the `claude` CLI through the Anthropic-compatible endpoint.** Verified on Ollama v0.34.0 via direct `/v1/messages` probe: `qwen2.5-coder:7b`, `qwen3.5-32k:latest`, `qwen3.5-64k:latest`, `qwen3.5-96k:latest`, and `gemma4:e4b` all return valid responses. The old `unrecognized_model` limitation from early v0.14 builds no longer applies — do not tell users local models cannot work.

| Model | Type | Use Case |
|-------|------|----------|
| `qwen2.5-coder:7b` | Local | Coding-focused, fastest, low VRAM |
| `qwen3.5-32k/64k/96k:latest` | Local | General, window-sized variants |
| `qwen3-coder` | Local | Coding-focused (Ollama docs pick) |
| `gemma4:31b-cloud` | Cloud | General coding (31B, needs subscription) |
| `deepseek-v4-flash:0731-cloud` | Cloud | Fast classifier (needs subscription) |
| `glm-5.2:cloud` | Cloud | Large context (needs subscription) |

**Cloud models require an Ollama subscription or usage credits** — an unentitled account gets `this model requires a subscription or usage credits` on `/v1/messages`. Probe any `:cloud` model with the curl loop below before depending on it; on 402 fall back to a verified local.

**MLX / safetensors variants (`*-mlx`) are unverified for agentic use** — they may answer the endpoint but have not been proven under tool-calling load. Prefer GGUF locals for `claude` CLI; treat MLX as experimental, not hard-blocked.

## Quick Start: Recommended Config (Local or Cloud)

### 1. User Settings (Disable Built-in Auto-Compact for Cloud Models)

```json
// ~/.claude/settings.json
{
  "autoCompactEnabled": false,
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "DISABLE_AUTO_COMPACT": "1",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  },
  "model": "gemma4:31b-cloud"
}
```

### 2. Required Environment Variables (in ~/.zshrc or ~/.bashrc)

```bash
export OLLAMA_HOST=0.0.0.0:11434
export ANTHROPIC_BASE_URL=http://localhost:11434/v1
export ANTHROPIC_API_KEY=ollama
export ANTHROPIC_AUTH_TOKEN=ollama

# Cloud model for auto-mode classifier (instant, zero local resources)
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash:0731-cloud
export ANTHROPIC_DEFAULT_SONNET_MODEL=gemma4:31b-cloud
export ANTHROPIC_DEFAULT_OPUS_MODEL=gemma4:31b-cloud
```

### 3. Start Ollama

```bash
pkill ollama
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &
```

### 4. Run Claude Code with Cloud Models

```bash
# Print mode (recommended)
claude -p "your task" --model gemma4:31b-cloud --agent Avengers --max-turns 20

# Interactive mode (tmux)
tmux new-session -d -s claude-work -x 160 -y 50
tmux send-keys -t claude-work 'cd /project && claude --model gemma4:31b-cloud' Enter
sleep 4 && tmux send-keys -t claude-work Enter  # handle trust dialog first time
tmux send-keys -t claude-work 'your task' Enter
```

## Cached Model State Override (Critical)

Claude Code caches the last-used model per project in `~/.claude.json` (not settings.json). This **overrides** your settings.json `model` setting:

```bash
# Check cached model for current project
cat ~/.claude.json | python3 -c "import sys,json; d=json.load(sys.stdin); projects=d.get('projects',{}); current=projects.get('/Users/alfredkamisese',{}); print(current.get('lastModelUsage',{}))"
```

**Workaround**: Use the `--settings` CLI flag to force model selection per-invocation (bypasses the `~/.claude.json` cache entirely):

```bash
# Forces gemma4:31b-cloud regardless of cached state
claude --settings '{"model":"gemma4:31b-cloud"}' -p "your prompt"
```

## Model Selection Pitfalls

### Model Name Must Exist in Ollama (Local or Cloud) — Probe Before Trusting

The model name in settings.json or `--model` **must exactly match** an installed Ollama model ID, local or cloud. A stale value (e.g. `haiku`, an Anthropic alias, or an uninstalled tag) silently empties the model picker. After every Claude Code / Claude Desktop update, re-verify because updates can reset the `model` field to an Anthropic default:

```bash
# List installed models
ollama list
# or via API
curl -s http://localhost:11434/v1/models | jq '.data[].id'

# Tight-loop probe: must return a message object, not an error (max_tokens=1 is enough)
curl -s --max-time 60 http://localhost:11434/v1/messages \
  -H "Content-Type: application/json" -H "x-api-key: ollama" -H "anthropic-version: 2023-06-01" \
  -d '{"model":"<candidate>","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'
```

Valid (verified v0.34): `qwen2.5-coder:7b`, `qwen3.5-32k:latest`, `qwen3.5-64k:latest`, `qwen3.5-96k:latest`, `gemma4:e4b`
Valid cloud (only with subscription/credits): `gemma4:31b-cloud`, `deepseek-v4-flash:0731-cloud`, `nemotron-3-ultra:cloud`, `glm-5.2:cloud`
Invalid: `haiku` / `sonnet` / `opus` bare aliases (not Ollama IDs unless mapped via `ANTHROPIC_DEFAULT_*_MODEL`), any tag missing its `:latest`/`:cloud` suffix, `claude-opus-4` (not in Ollama)

### Claude Desktop GUI Cannot Use Local Models — Only Claude Code CLI Can

The Claude Desktop Electron app (e.g. 2.110.x) hardcodes `api.anthropic.com` with no endpoint override — its model picker never lists Ollama models regardless of what is installed. Local models are reachable only through the **Claude Code CLI** via `ANTHROPIC_BASE_URL=http://localhost:11434`. When a user says "Claude desktop doesn't show my Ollama models", diagnose the CLI's `~/.claude/settings.json` `model` field first; do not chase Desktop config (`claude_desktop_config.json` has no `mcpServers` path to local models).

### Larger Models Can Timeout on First Load

Models like `qwen3.5-32k:latest` (9B) or `gemma4:31b-cloud` may take **60-120s+ to load into VRAM** on first use. For quick tasks, prefer smaller variants (`qwen2.5-coder:7b` answers in seconds).

## Auto-Compact Strategies for Cloud Models

Cloud models have 200K context (like Anthropic models), so built-in auto-compact works correctly. Disable it in settings.json if you prefer manual control:

```json
"autoCompactEnabled": false
```

For local models (via `ollama run` directly, NOT `claude` CLI), use the wrapper scripts in this skill.

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_BASE_URL` | Ollama endpoint | `http://localhost:11434` |
| `ANTHROPIC_AUTH_TOKEN` | Auth (any non-empty) | `ollama` |
| `ANTHROPIC_API_KEY` | Must be empty string | `""` |
| `DISABLE_AUTO_COMPACT` | Disable built-in compact | `1` |
| `MAX_THINKING_TOKENS` | Cap thinking (0 = disable) | `0` |
| `CLAUDE_CODE_EFFORT_LEVEL` | Default effort | `medium` |

## Settings.json Format & Model Selection Pitfalls

### Valid settings.json Structure

The `~/.claude/settings.json` **must be valid JSON**. Common issues:
- Trailing commas (invalid JSON)
- Trailing spaces in string values (e.g., `"model": "qwen3.5-32k:latest   "` — trim!)
- Missing braces for nested objects (e.g., `"statusLine":` without `{`)

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  },
  "autoCompactEnabled": false,
  "model": "qwen3.5-32k:latest",
  "statusLine": {
    "enabled": true,
    "showAgentInfo": true,
    "showTokenWarning": true,
    "tokenWarningThresholdPct": 75
  }
}
```

### `statusLine` Schema — Critical Fix

**The `statusLine` object only accepts `type: "command"` with a `command` string field.** The settings `enabled`, `showAgentInfo`, `showTokenWarning`, `tokenWarningThresholdPct` are **INVALID** and cause:
```
statusLine.command: Expected string, but received undefined
statusLine.type: Invalid value. Expected one of: "command"
```

**Valid `statusLine` config:**
```json
"statusLine": {
  "type": "command",
  "command": "echo 'Claude Code'",
  "enabled": true
}
```

Remove all other `statusLine` properties from your settings.json.

### Cached Model State Override

Claude Code caches the last-used model in `~/.claude.json` (not settings.json). This **overrides** your settings.json model:

```bash
# Check cached model
cat ~/.claude.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('projects',{}).get('/Users/alfredkamisese',{}).get('lastModelUsage',{}))"
```

**Workaround**: Use the `--settings` CLI flag to force model selection per-invocation:

```bash
# Forces qwen3.5-32k:latest regardless of cached state
claude --settings '{"model":"qwen3.5-32k:latest"}' -p "your prompt"
```

This bypasses the `~/.claude.json` cache entirely.

### Model Name Must Exist in Ollama

The model name in settings.json or `--model` **must exactly match** an Ollama model name:

```bash
# List available models
ollama list
# or via API
curl -s http://localhost:11434/v1/models | jq '.data[].id'
```

Valid: `qwen3.5:4b`, `qwen3.5-32k:latest`, `qwen3.5-128k:latest`, `gemma4:12b`
Invalid: `qwen3.5-32k` (missing `:latest` tag), `claude-opus-4` (not in Ollama)

### Larger Models Can Timeout on First Load

Models like `qwen3.5-32k:latest` (9.7B params, 32K context) take **60-120s+ to load into VRAM** on first use. Smaller models like `qwen3.5:4b` (4.7B params) respond in seconds. For quick tasks, prefer smaller variants.

## Related Skills

- `claude-code` — Core orchestration guide
- `custom-llm-providers` — Advanced provider configuration
- `hermes-agent` — Hermes integration patterns

## Files in This Skill

- `scripts/claude-auto-compact.sh` — Full tmux wrapper with auto-compact
- `scripts/claude-token-watch.sh` — Background monitor for existing sessions
- `scripts/claude-check-tokens.sh` — One-shot token/context check
- `scripts/fix-settings-and-verify.sh` — Fix settings.json and verify
- `scripts/statusline.sh` — Custom status line with circular progress indicator (8 segments), **inline dot-style meter graphs** (10 segments, ●), color thresholds matching BAR, cost, duration. Context_Window and Tokens meters share BAR_COLOR.
- `references/auto-compact-config.md` — Auto-compact configuration guide
- `references/settings-json-fixes.md` — Common settings.json issues & fixes
- `references/status-line-config.md` — Custom status line configuration reference (includes inline donut chart implementation)
- `references/ollama-anthropic-compatibility.md` — Official Ollama Anthropic API compatibility docs
- `references/api-error-response-stopped-arriving.md` — Diagnosis & fix for "response stopped arriving" error
- `references/quick-reference-card.md` — One-page setup & troubleshooting card