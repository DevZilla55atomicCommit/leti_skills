---
title: Hermes Integration for TurboQuant
skill: turboquant-kv-cache
---

# Hermes Integration for TurboQuant

## Custom OpenAI Provider Configuration

Add to `~/.hermes/config.yaml` under `providers:`:

```yaml
providers:
  turboquant:
    api: http://localhost:8081/v1
    api_key: "not-needed"
    default_model: gemma4-12b-turbo
    models:
      - gemma4-12b-turbo
    name: "TurboQuant"
    context_length: 32768
```

**Critical fields:**
- `context_length: 32768` — Required! Without this, Hermes uses default (128-256) causing "Context length exceeded" errors
- `api_key: "not-needed"` — llama-server doesn't require auth
- `api: http://localhost:8081/v1` — Points to llama-server

## Provider Registration Steps

1. Edit `~/.hermes/config.yaml` (add provider under `providers:`)
2. **Restart Hermes completely** (Cmd+Q → reopen) — provider config cached at startup
3. In chat: Select "TurboQuant" from provider dropdown
4. Model should show: `gemma4-12b-turbo`

## Common Hermes Routing Conflicts

### Problem: "Context length exceeded (78 tokens)"

**Cause:** Hermes falls back to Ollama model with same/similar name.
- Ollama `gemma4:12b` defaults to ~128-256 token context
- Custom provider `gemma4-12b-turbo` has 32768 context
- Hermes merges models from all enabled providers; similar names cause fallback

### Fix: Disable Conflicting Ollama Models

**In Hermes Settings → Providers → Ollama:**
1. Find `gemma4:12b` (or any similar-named model)
2. Toggle **OFF** / remove from models list
3. Save

**Alternative:** Remove model from Ollama provider config in config.yaml:
```yaml
providers:
  ollama-launch:
    models:
      - qwen3.5:4b
      - gemma4:e4b
      # - gemma4:12b  # REMOVE THIS LINE
    ...
```

## Verification Checklist

After setup, verify:

| Check | Command | Expected |
|-------|---------|----------|
| Server running | `curl http://localhost:8081/v1/models` | Returns model list |
| Context length | `hermes config get providers.turboquant.context_length` | `32768` |
| Model visible | In Hermes chat dropdown | "TurboQuant" provider with `gemma4-12b-turbo` |
| Long context works | Chat: "Write 500 word story..." | Generates 500+ words without error |

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Provider not appearing | Hermes not restarted | Cmd+Q → reopen Hermes |
| "Model not found" | Model name mismatch | Ensure `default_model` matches `models[0]` exactly |
| Short context persists | Ollama fallback | Disable conflicting Ollama model; restart Hermes |
| Connection refused | Server not running | Start llama-server on port 8081 |
| Port 8081 busy | Old process | `lsof -ti:8081 \| xargs kill -9` |

## Server Management

### Start Server (background)
```bash
~/llama-cpp-turboquant/build/bin/llama-server \
  -m ~/models/gemma4-12b-q4.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 32768 --port 8081 --host 0.0.0.0 &
```

### Health Check
```bash
curl -s http://localhost:8081/health
curl -s http://localhost:8081/v1/models | jq .
```

### Stop Server
```bash
lsof -ti:8081 | xargs kill -9
```

## Environment Variables for Server

```bash
# Optional: tune TurboQuant behavior
export TURBO_LAYER_ADAPTIVE=7
export TURBO_AUTO_ASYMMETRIC=1
export TURBO_SPARSE_V=1

# Metal/GPU
export GGML_METAL_LOG_LEVEL=0
export GGML_METAL_NDEBUG=1
```