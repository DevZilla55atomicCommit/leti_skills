---
name: llama-cpp-quantization
description: Quantize llama.cpp TurboQuant asymmetric KV on Apple Silicon
category: mlops
---

## Overview

This skill covers local LLM quantization workflows using `llama.cpp` and its forks on macOS (Apple Silicon). It includes standard quantization (Q4_K_M, Q8_0, etc.), community TurboQuant forks for KV cache compression, and asymmetric quantization strategies (different levels for K vs V).

## Prerequisites

- macOS on Apple Silicon (M1/M2/M3/M4/M5)
- Xcode Command Line Tools (`xcode-select --install`)
- CMake 3.22+ (`brew install cmake`)
- Git

## Standard llama.cpp Build

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DLLAMA_METAL=ON -DLLAMA_METAL_NDEBUG=ON
cmake --build build --config Release -j$(sysctl -n hw.ncpu)
```

## TurboQuant Setup (Community Fork)

**Repository**: `https://github.com/TheTom/llama-cpp-turboquant` (branch: `feature/turboquant-kv-cache`)

```bash
# Clone the TurboQuant branch
git clone -b feature/turboquant-kv-cache https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant

# Build with Metal (Apple Silicon)
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

Binary location: `./build/bin/llama-cli` and `./build/bin/llama-bench`

> ⚠️ **Status**: Community fork, not yet merged into mainline `llama.cpp`. V Llama also working on it. Once merged, LM Studio and other tools inherit it automatically.

## Quantization Levels Reference

| Method | Model Weights | KV Cache | Use Case |
|--------|--------------|----------|----------|
| Q4_K_M | 4-bit | FP16 | Default balanced |
| Q8_0 | 8-bit | FP16 | High quality, larger |
| Turbo 2 | FP16/Q8 | ~4× compressed | Max compression, quality drops at >4K context |
| Turbo 3 | FP16/Q8 | ~2.5× compressed | **Sweet spot** — 131K context on 16GB M4 Mini |
| Turbo 4 | FP16/Q8 | ~1.9× compressed | Conservative, minimal quality loss |

## Asymmetric Quantization (Recommended)

**Best configuration per testing:**

```bash
# Q8 for K (keys), Turbo 3 for V (values) — asymmetric
./llama-cli -m <model.gguf> \
  --cache-type-k q8_0 \
  --cache-type-v turbo3 \
  -c 131072 \
  -p "your prompt"
```

- **Symmetric** (same level for K & V) degrades quality significantly at >4K context
- **Asymmetric** preserves needle-in-haystack accuracy at 32K+ context
- Q8_0 for K is critical — K cache is more sensitive to quantization

## TurboQuant Types

| Type | Enum | Bits/Value | Compression vs f16 | Description |
|------|------|------------|--------------------|-------------|
| `turbo2` | `GGML_TYPE_TURBO2_0` (43) | 2 bits | 6.4× | Most aggressive |
| `turbo3` | `GGML_TYPE_TURBO3_0` (44) | 3.25 bits | 4.9× | **Sweet spot** |
| `turbo4` | `GGML_TYPE_TURBO4_0` (47) | 4.25 bits | 3.8× | Least aggressive |

These are **KV-cache-only types** — never stored in model files. Corresponding model-weight types: `TQ3_1S` (45) and `TQ4_1S` (46).

## Apple Silicon Hardware Results

| Machine | Bottleneck | TurboQuant Benefit |
|---------|------------|-------------------|
| **M4 Mac Mini (16GB)** | Compute-bound | Memory savings ✓, speed ~flat (1–8% slower at short context) |
| **M5 Max / M5 MBP (128GB)** | Memory-bound | **Huge speed win** — decode stays flat 54 tok/s (0→32K) vs Q8 dropping 54→37 |
| **M5 Mac Mini (future)** | Expected memory-bound | Predicted significant boost |

> **Key insight**: On memory-bound machines (high unified memory, many cores), TurboQuant keeps decode speed flat across context lengths because KV cache bandwidth is no longer the bottleneck. On compute-bound machines (M4 Mini), matrix mul is the bottleneck so TurboQuant only helps memory, not speed.

## M4 Mac Mini (16GB) Benchmarks — Qwen3-4B Q8_0

| Config | Prompt (512) | Decode (256) | Prompt @ 8K ctx | Decode @ 8K ctx |
|--------|-------------|-------------|-----------------|-----------------|
| Q8_0 / Q8_0 (baseline) | 415 t/s | 21.9 t/s | 151 t/s | 15.5 t/s |
| **Q8_0 / Turbo3 (asymmetric)** | **410 t/s** | **20.2 t/s** | **147 t/s** | **14.5 t/s** |

### M4 Mac Mini (16GB) Benchmarks — Gemma4-12B Q4_K_M

| Config | Prompt (512) | Decode (128) | Prompt @ 8K ctx | Decode @ 8K ctx |
|--------|-------------|-------------|-----------------|-----------------|
| Q8_0 / Q8_0 (baseline) | 134 t/s | 12.5 t/s | 101 t/s | 11.1 t/s |
| **Q8_0 / Turbo3 (asymmetric)** | **135 t/s** | **11.8 t/s (-5%)** | **97 t/s** | **8.9 t/s (-20%)** |
| Q8_0 / Turbo4 | 112 t/s | 10.5 t/s (-16%) | — | — |

### Memory Savings

- Turbo3 V cache = ~2.5× compression vs Q8_0
- Enables 2–4× longer context on same RAM
- 64K+ context works; 128K+ likely works on 16GB

## Models That Respond Well to TurboQuant

- **Qwen 3.5 series** (MoE and dense) — "respond really nicely to TurboQuant on Apple hardware"
- Qwen 2.5, Qwen 3 8B — tested, similar results
- MoE models (Qwen 3.5 35B) benefit most — KV cache dominates memory

## Environment Variables

| Variable | Default | Effect |
|----------|---------|--------|
| `TURBO_LAYER_ADAPTIVE` | `0` | Layer-adaptive KV precision; `7` = Boundary V (first/last layers in q8_0, middle in turbo) |
| `TURBO_AUTO_ASYMMETRIC` | `1` | Auto-select asymmetric K/V for large-GQA models (`0` disables) |
| `TURBO_SPARSE_V` | `1` | Sparse-V dequant skip in flash attention (`0` disables) |
| `LLAMA_ATTN_ROT_K_OVERRIDE` | off | Enable upstream attention rotation for K |
| `LLAMA_ATTN_ROT_V_OVERRIDE` | off | Enable upstream attention rotation for V |
| `LLAMA_ATTN_ROT_DISABLE` | `0` | Hard lock-out: force rotation off on both sides |

## Quality Validation

Needle-in-haystack test results (asymmetric Q8_0 K + Turbo3 V):
- ✅ 1K context: 3/3 secrets found
- ✅ 4K context: 3/3 secrets found  
- ✅ 8K context: 3/3 secrets found
- ✅ 16K context: 3/3 secrets found
- ✅ 32K context: 3/3 secrets found

Symmetric Turbo3 fails at >4K context (0/3 secrets at 8K/16K).

## Current Status

- **Upstream**: Not yet merged into `ggml-org/llama.cpp` (community fork only)
- **V Llama**: Working on integration
- **Future**: Once merged, LM Studio and other tools get it automatically

## Source

- GitHub: https://github.com/TheTom/llama-cpp-turboquant (branch: `feature/turboquant-kv-cache`)
- Docs: `docs/kv-cache-quantization.md` in the fork
- Video: "After This, 16GB Feels Different" by Alex Ziskind

## Quick Test Script

Save as `scripts/test-turboquant.sh`:

```bash
#!/bin/bash
# Test TurboQuant asymmetric config on a model
MODEL="${1:-qwen3.5-35b-Q8.gguf}"
CONTEXT="${2:-131072}"

./build/bin/llama-cli -m "$MODEL" \
  --cache-type-k q8_0 \
  --cache-type-v turbo3 \
  -c "$CONTEXT" \
  -p "The secret word is 'pineapple'. Remember this. Now repeat back the secret word." \
  --temp 0.1
```

## Pitfalls

- **TurboQuant not in mainline** — must build from fork; `llama.cpp` releases won't have it
- **Model-dependent** — some models (older Qwen 2.5) show similar degradation; Qwen 3.5 is the sweet spot
- **Symmetric = quality loss** — never apply same Turbo level to both K and V for long context
- **M4 Mini compute-bound** — don't expect speed improvements, only memory savings
- **Context length matters** — benefits amplify at 32K+ context; at 1-4K, standard Q8 is fine

## References

- `references/turboquant-notes.md` — Full transcript notes from Alex Ziskind video
- `references/quant-comparison.md` — Quantization level comparison table

## See Also

- `mlops/inference/serving-llms-vllm` — For vLLM serving with quantization
- `mlops/inference/llama-cpp` — Base llama.cpp inference skill