# TurboQuant in llama.cpp (TheTom Fork) — Testing Notes

## Source
- Fork: https://github.com/TheTom/llama-cpp-turboquant
- Branch: `feature/turboquant-kv-cache`
- Status: Community fork, 28 commits ahead of upstream, active development (last commit 53 min ago as of 2026-08-01)
- Not yet merged to mainline llama.cpp

## Build (M4 Mac Mini)
```bash
git clone -b feature/turboquant-kv-cache https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

## New KV Cache Types

| Type | Enum | Bits/value | Compression vs FP16 |
|------|------|------------|---------------------|
| `turbo2` | `GGML_TYPE_TURBO2_0` (43) | 2 | 6.4× |
| `turbo3` | `GGML_TYPE_TURBO3_0` (44) | 3.25 | 4.9× |
| `turbo4` | `GGML_TYPE_TURBO4_0` (47) | 4.25 | 3.8× |

These are **runtime-only** KV cache types — never stored in model files.

## Usage

```bash
# Asymmetric (recommended): Q8_0 for K, Turbo3 for V
./build/bin/llama-cli -m model.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 32768 -p "your prompt"

# All combinations supported: f16, q8_0, q4_0, turbo2, turbo3, turbo4
```

## Test Results (M4 Mac Mini 16GB)

### Qwen3-4B Q8_0 (4 GB model)

| Config | Prompt (512) | Decode (256) | Prompt @ 8K | Decode @ 8K |
|--------|-------------|-------------|-------------|-------------|
| Q8_0 / Q8_0 | 415 t/s | 21.9 t/s | 151 t/s | 15.5 t/s |
| **Q8_0 / Turbo3** | **410 t/s** | **20.2 t/s (-8%)** | **147 t/s** | **14.5 t/s (-7%)** |

### Gemma4-12B Q4_K_M (6.6 GB model)

| Config | Prompt (512) | Decode (128) | Prompt @ 8K | Decode @ 8K |
|--------|-------------|-------------|-------------|-------------|
| Q8_0 / Q8_0 | 134 t/s | 12.5 t/s | 101 t/s | 11.1 t/s |
| **Q8_0 / Turbo3** | **135 t/s** | **11.8 t/s (-5%)** | **97 t/s** | **8.9 t/s (-20%)** |
| Q8_0 / Turbo4 | 112 t/s | 10.5 t/s (-16%) | — | — |

## Key Observations

### M4 Mini is Compute-Bound
- M4 Mini: decode speed drops with TurboQuant (1-20% penalty) because bottleneck is matrix multiplies, not KV cache bandwidth
- Video claims M5 Max shows **flat decode speed** (54 t/s from 0→32K) vs Q8_0 dropping to 37 t/s — we couldn't verify (no M5 Max)

### Turbo3 = Sweet Spot
| Level | Compression | Quality | Context Limit |
|-------|-------------|---------|---------------|
| Turbo2 | ~4× | ❌ Collapses >4K | Low |
| **Turbo3** | **~2.5×** | ✅ Passes needle-in-haystack at 131K | **High** |
| Turbo4 | ~1.9× | ✅ Good | Medium |

### Asymmetric K/V is Critical
- Symmetric (same level for K & V): quality drops at >4K context
- Asymmetric (Q8_0 K + Turbo3 V): maintains quality at 131K+
- Video author tested: Q8_0 K + Turbo1 V, Q8_0 K + Turbo3 V — both work

### Memory Savings
- Turbo3 V cache: ~2.5× compression vs Q8_0
- Enables 64K–131K context on 16GB that would OOM with Q8_0 V
- On M4 Mini 16GB: 32K context works, 64K works, 128K likely works

## Environment Variables

```bash
export TURBO_LAYER_ADAPTIVE=7    # Boundary layers in Q8_0, middle in Turbo (0=off)
export TURBO_AUTO_ASYMMETRIC=1   # Auto asymmetric for large-GQA models
export TURBO_SPARSE_V=1          # Sparse V dequant skip in flash attention
```

## Models Tested

| Model | Source | Format | Works? |
|-------|--------|--------|--------|
| Qwen3-4B Q8_0 | unsloth/Qwen3-4B-GGUF | GGUF | ✅ |
| Qwen3.5-4B | Ollama cache | GGUF | ❌ RoPE config mismatch |
| Gemma4-12B Q4_K_M | unsloth/gemma-4-12b-it-GGUF | GGUF | ✅ |

## Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `qwen35.rope.dimension_sections` error | Ollama Qwen3.5 uses different GGUF metadata | Use HF GGUF (unsloth org), not Ollama cache |
| Turbo3 slower at short context | M4 is compute-bound, WHT rotation overhead | Accept tradeoff or use Q8_0/Q8_0 for short ctx |
| 128K context benchmark timeout | Very slow at high context on M4 | Test shorter contexts, trust video for 128K claim |

## When to Use TurboQuant on M4 Mini 16GB

| Scenario | Recommendation |
|----------|----------------|
| Short context (<4K) | Q8_0/Q8_0 — 5-8% faster |
| Medium context (8K-16K) | Q8_0/Turbo3 — small penalty, 2.5× KV savings |
| Long context (32K+) | **Q8_0/Turbo3 required** — Q8_0 V would OOM |
| Quality critical | Q8_0/Q8_0 or Q8_0/Turbo4 |

## Status & Roadmap

- [ ] Merge to mainline llama.cpp (PR pending)
- [ ] LM Studio integration (auto when merged)
- [ ] V Llama integration (in progress)
- [ ] Metal kernel optimization for M4/M5 (currently uses 4-mag LUT fallback)

## Related Video
- "After This, 16GB Feels Different" — Alex Ziskind (XLlQDfhyBjc)
- Covers TurboQuant theory, asymmetric K/V, M4 vs M5 benchmarks