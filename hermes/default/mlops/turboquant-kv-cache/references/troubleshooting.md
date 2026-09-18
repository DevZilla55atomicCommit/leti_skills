---
title: TurboQuant Troubleshooting
skill: turboquant-kv-cache
---

# TurboQuant Troubleshooting

## Server Issues

### "Couldn't bind HTTP server socket, port 8081"

**Cause:** Another process on port 8081 (stale llama-server)

**Fix:**
```bash
lsof -ti:8081 | xargs kill -9
# Or use different port:
--port 8082
```

### Server starts but exits immediately

**Cause:** Model file not found / wrong path

**Fix:**
```bash
# Verify model exists
ls -la ~/models/gemma4-12b-q4.gguf

# Use absolute path
-m /Users/alfredkamisese/models/gemma4-12b-q4.gguf
```

### Server loads but responses are empty

**Cause:** `max_tokens` too low / Gemma 4 outputs reasoning_content

**Fix:**
```bash
# Increase max_tokens
curl ... -d '{"max_tokens": 500, ...}'

# Gemma 4 puts answer in reasoning_content, not content
jq -r '.choices[0].message.reasoning_content'
```

## Model Loading Errors

### "Wrong array length" / "Invalid GGUF"

**Cause:** Ollama model format incompatible with llama.cpp fork

**Fix:**
```bash
# Download HF GGUF instead
curl -L -o model.gguf "https://huggingface.co/unsloth/gemma-4-12b-it-GGUF/resolve/main/gemma-4-12b-Q4_K_M.gguf"
```

### "TurboQuant not found" / "Unknown cache type"

**Cause:** Wrong fork / branch / outdated build

**Fix:**
```bash
# Use correct fork and branch
git clone -b feature/turboquant-kv-cache https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

## Quality Issues

### Degraded quality at high context (>8K)

**Cause:** Symmetric K/V Turbo (both at Turbo3)

**Fix:** Use asymmetric — K at q8_0, V at Turbo3
```bash
--cache-type-k q8_0 --cache-type-v turbo3
```

### Repetitive / looping output

**Cause:** Turbo level too aggressive for model

**Fix:** Reduce Turbo level
```bash
# Less aggressive
--cache-type-k q8_0 --cache-type-v turbo4

# Or layer-adaptive
export TURBO_LAYER_ADAPTIVE=7
```

## Hermes Integration Issues

### "Context length exceeded (78 tokens)"

**Cause:** Hermes using Ollama model instead of TurboQuant provider

**Fix:**
1. Settings → Providers → Ollama → Disable `gemma4:12b`
2. Restart Hermes (Cmd+Q → reopen)
3. Select "TurboQuant" provider in chat

### Custom provider not appearing in dropdown

**Cause:** Hermes not restarted after config change

**Fix:**
```bash
# Full restart
pkill -f "hermes"; open -a Hermes
```

### Model shows but context still short

**Cause:** Missing `context_length` in provider config

**Fix:** Add to config.yaml:
```yaml
providers:
  turboquant:
    context_length: 32768  # REQUIRED
```

## Performance Issues

### Decode slower than expected

**Cause:** Partial GPU offload / not using Metal

**Fix:**
```bash
# Full GPU offload
-ngl 99

# Verify Metal active in logs
# "ggml_metal_device_init: GPU name: MTL0"
```

### Server uses high CPU, low GPU

**Cause:** Partial offload (-ngl < 99) causes CPU↔GPU copies

**Fix:**
```bash
-ngl 99  # Full offload
```

## Build Issues

### CMake: "Metal framework not found"

**Fix:**
```bash
xcode-select --install
# Or ensure Xcode command line tools installed
```

### "ARM -march/-mcpu not found"

**Fix:** Use native build (default on Apple Silicon)
```bash
cmake -B build -DGGML_METAL=ON
# Don't set -DCMAKE_C_FLAGS manually
```

## Quick Diagnostic Commands

```bash
# Check server health
curl -s http://localhost:8081/health

# List models
curl -s http://localhost:8081/v1/models | jq .

# Test generation
curl -s http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma4-12b-turbo","messages":[{"role":"user","content":"hi"}],"max_tokens":20}' | jq .

# Check port usage
lsof -ti:8081

# Kill all llama-server
pkill -f llama-server
```

## Getting Help

If issue persists, collect:
1. Server startup logs (full)
2. `llama-server --version`
3. Model info: `llama-cli -m model.gguf --help`
4. Exact command that fails
5. Hardware: `sysctl -n machdep.cpu.brand_string` + `sysctl hw.memsize`