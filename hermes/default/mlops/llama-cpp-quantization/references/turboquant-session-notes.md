# TurboQuant Session Notes (August 2025)

## Session Summary
Testing TurboQuant asymmetric KV cache quantization on M4 Mac Mini (16GB) using TheTom's llama-cpp-turboquant fork (branch: feature/turboquant-kv-cache).

## Models Tested

### 1. Qwen3-4B Q8_0 (4 GB)
- Source: unsloth/Qwen3-4B-GGUF (Hugging Face)
- Works natively with TurboQuant fork
- Benchmarks completed at multiple context lengths

### 2. Gemma4-12B Q4_K_M (6.6 GB)
- Source: unsloth/gemma-4-12b-it-GGUF (Hugging Face)
- Required --allow-requantize for Ollama import
- Tested with Turbo3 and Turbo4

### 3. Qwen3.5-4B (Ollama) — FAILED
- Format mismatch: `qwen35.rope.dimension_sections` array length
- Ollama's GGUF differs from HF/unsloth GGUF

## Benchmark Results

### Qwen3-4B Q8_0 on M4 Mini 16GB

| Config | Prompt (512) | Decode (256) | Prompt @ 8K | Decode @ 8K |
|--------|-------------|-------------|-------------|-------------|
| Q8_0 / Q8_0 | 415 t/s | 21.9 t/s | 151 t/s | 15.5 t/s |
| Q8_0 / Turbo3 | 410 t/s | 20.2 t/s | 147 t/s | 14.5 t/s |

### Gemma4-12B Q4_K_M on M4 Mini 16GB

| Config | Prompt (512) | Decode (128) | Prompt @ 8K | Decode @ 8K |
|--------|-------------|-------------|-------------|-------------|
| Q8_0 / Q8_0 | 134 t/s | 12.5 t/s | 101 t/s | 11.1 t/s |
| Q8_0 / Turbo3 | 135 t/s | 11.8 t/s (-5%) | 97 t/s | 8.9 t/s (-20%) |
| Q8_0 / Turbo4 | 112 t/s | 10.5 t/s (-16%) | — | — |

## Key Findings

1. **M4 Mini is compute-bound** — TurboQuant gives memory savings, not speed wins
2. **Turbo3 is the sweet spot** — Turbo2 degrades quality, Turbo4 saves less memory
3. **Asymmetric (Q8_0 K + Turbo3 V) works** — symmetric fails at >4K context
4. **Gemma4 penalizes more at high context** — 20% decode drop vs 7% for Qwen3
5. **Ollama integration possible** but needs --allow-requantize and disk space

## Ollama Integration Notes

```bash
# Convert for Ollama (strict validator)
./build/bin/llama-quantize --allow-requantize \
  ./models/gemma4-12b-q4.gguf \
  /tmp/gemma4-12b-ollama.gguf \
  Q4_K_M

# Modelfile
FROM /tmp/gemma4-12b-ollama.gguf
TEMPLATE "{{ .Prompt }}"
PARAMETER num_ctx 8192
PARAMETER num_gpu 99

# Create (needs ~7GB free disk space)
ollama create gemma4-turbo-q4k -f ~/Modelfile.gemma4-turbo
```

**Important**: Ollama uses standard KV cache, NOT TurboQuant KV. TurboQuant KV only works with fork's llama-cli.

## Disk Space Requirements

- Ollama copies GGUF to ~/.ollama/models/blobs/ — need ~7GB free for 6-7GB models
- Clean space before `ollama create`

## Next Steps

- Test on M5 Max when available (expected huge speed win at high context)
- Try TurboQuant with MoE models (Qwen 3.5 35B)
- Wait for upstream merge into ggml-org/llama.cpp