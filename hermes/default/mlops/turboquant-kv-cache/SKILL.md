---
name: turboquant-kv-cache
description: "TurboQuant KV cache quantization for llama.cpp"
version: 1.0.0
author: Nous Research / TheTom (fork)
license: MIT
platforms: [macos]
tags: [llama.cpp, quantization, kv-cache, apple-silicon, turboquant, inference]
metadata:
  hermes:
    tags: [llama.cpp, quantization, kv-cache, apple-silicon, turboquant]
    related_skills: [llama-cpp-quantization, apple-silicon-llm-inference, hermes-agent]
---

# TurboQuant KV Cache Quantization

TurboQuant is a **KV-cache-only** quantization technique for llama.cpp that compresses the key/value cache far beyond standard `q8_0` while preserving decode quality via a fixed 128×128 Walsh-Hadamard rotation (WHT) that Gaussianizes cache vectors before quantization.

## Key Properties

| Type | Enum | Bits/value | Compression vs f16 | Best For |
|------|------|------------|-------------------|----------|
| `turbo2` | `GGML_TYPE_TURBO2_0` (43) | 2.0 | 6.4× | Max compression, low context |
| `turbo3` | `GGML_TYPE_TURBO3_0` (44) | 3.25 | 4.9× | **Sweet spot** — 131K context on 16GB M4 |
| `turbo4` | `GGML_TYPE_TURBO4_0` (47) | 4.25 | 3.8× | Conservative, near-Q8 quality |

**These are runtime-only types** — never stored in model files. Corresponding weight types are `TQ3_1S` (45) and `TQ4_1S` (46) for model-weight quantization.

## Asymmetric K/V Configuration (Recommended)

```bash
# Best quality + memory savings
--cache-type-k q8_0 --cache-type-v turbo3

# More aggressive
--cache-type-k q8_0 --cache-type-v turbo2
```

- **K (keys)**: Keep at `q8_0` — keys are more sensitive to quantization
- **V (values)**: Apply TurboQuant — values tolerate more compression
- Symmetric (same level for K & V) degrades quality at >4K context

## Building the Fork

```bash
git clone -b feature/turboquant-kv-cache https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

## Usage

```bash
# CLI with asymmetric Turbo3
~/llama-cpp-turboquant/build/bin/llama-cli \
  -m model.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 32768 -p "prompt"

# Server for Hermes/OpenAI-compatible API
~/llama-cpp-turboquant/build/bin/llama-server \
  -m model.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 32768 --port 8081 --host 0.0.0.0
```

## Environment Knobs

| Variable | Default | Effect |
|----------|---------|--------|
| `TURBO_LAYER_ADAPTIVE` | `0` | `7` = Boundary V (first/last layers q8_0, middle turbo) |
| `TURBO_AUTO_ASYMMETRIC` | `1` | Auto asymmetric for large-GQA models (`0` disables) |
| `TURBO_SPARSE_V` | `1` | Sparse-V dequant skip in flash attention (`0` disables) |
| `LLAMA_ATTN_ROT_DISABLE` | `0` | Hard lock-out: force rotation off (`1` disables) |

## Apple Silicon Performance (M4 Mini 16GB)

| Config | Prompt (512) | Decode (short ctx) | Decode (8K ctx) | Max Context |
|--------|-------------|-------------------|-----------------|-------------|
| Q8_0 / Q8_0 | 415 t/s | 21.9 t/s | 15.5 t/s | ~8K |
| **Q8_0 / Turbo3** | 410 t/s | 20.2 t/s | **14.5 t/s** | **32K–131K** |

- **M4 Mini is compute-bound** — TurboQuant adds ~5–20% decode overhead (WHT rotation)
- **Win is memory** — Turbo3 V cache ≈ 2.5× smaller, enabling 4–16× longer context
- On M5 Max (memory-bound), TurboQuant keeps decode FLAT at 54 t/s from 0→32K vs Q8_0 dropping 54→37 t/s

## Hermes Integration

### Custom OpenAI Provider

```yaml
# ~/.hermes/config.yaml
providers:
  turboquant:
    api: http://localhost:8081/v1
    api_key: "not-needed"
    default_model: my-model-turbo
    models:
      - my-model-turbo
    name: "TurboQuant"
    context_length: 32768  # CRITICAL — prevents fallback to default (128-256)
```

### Critical: Disable Conflicting Ollama Models

If Ollama has a similar model (e.g., `gemma4:12b` vs `gemma4-12b-turbo`), **disable the Ollama model** in Hermes Settings → Providers → Ollama, or Hermes will fall back to Ollama's tiny default context (128–256 tokens), causing "Context length exceeded (78 tokens)" errors.

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Context length exceeded (78 tokens)" | Hermes using Ollama model instead of custom provider | Disable conflicting Ollama model; set `context_length` on custom provider |
| TurboQuant not loading | Wrong fork/branch | Use `feature/turboquant-kv-cache` branch from TheTom/llama-cpp-turboquant |
| Quality degradation at high context | Symmetric K/V Turbo | Use asymmetric: `--cache-type-k q8_0 --cache-type-v turbo3` |
| Server won't start | Port conflict | Kill old process: `lsof -ti:8081 \| xargs kill -9` |
| Model not found in Hermes | Provider not restarted | Restart Hermes (Cmd+Q → reopen) after config changes |

## Model Compatibility

| Model Family | Works Well | Notes |
|--------------|------------|-------|
| Qwen 3 / 3.5 | ✅ | MoE and dense |
| Gemma 4 | ✅ | Tested on 12B Q4_K_M |
| Llama 3 / 3.1 | ✅ | Standard dense |
| Models with sliding window | ⚠️ | SWA cache may need `TURBO_SPARSE_V=0` |

## References

- `references/turboquant-technical.md` — WHT rotation math, quantization pipeline
- `references/hermes-integration.md` — Full Hermes provider setup, routing conflicts
- `references/apple-silicon-benchmarks.md` — M4/M5 performance tables
- `references/troubleshooting.md` — Common errors and fixes

## Templates

- `templates/hermes-provider.yaml` — Ready-to-paste provider config
- `templates/llama-server-turbo3.sh` — Server startup script with Turbo3
- `templates/llama-cli-turbo3.sh` — CLI command with asymmetric Turbo3