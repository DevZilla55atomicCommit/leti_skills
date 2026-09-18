---
title: Apple Silicon TurboQuant Benchmarks
skill: turboquant-kv-cache
---

# Apple Silicon TurboQuant Benchmarks

## M4 Mini (16GB) — Gemma4 12B Q4_K_M

| Config | Prompt 512 | Decode (0 ctx) | Decode 8K ctx | Max Context | V Cache Size |
|--------|-----------|----------------|---------------|-------------|--------------|
| Q8_0 / Q8_0 | 415 t/s | 21.9 t/s | 15.5 t/s | ~8K | 100% |
| **Q8_0 / Turbo3** | 410 t/s | 20.2 t/s | **14.5 t/s** | **32K–131K** | **~20%** |
| Q8_0 / Turbo2 | 395 t/s | 18.8 t/s | 13.2 t/s | ~200K | ~16% |
| Q8_0 / Turbo4 | 412 t/s | 21.1 t/s | 15.0 t/s | ~16K | ~26% |

**Key findings:**
- M4 Mini is **compute-bound** — TurboQuant adds 5-20% decode overhead
- Memory win: Turbo3 V cache = 4.9× smaller → 4-16× longer context
- Compute-bound = speed similar, context window expands dramatically

## M5 Max (128GB) — Qwen3-4B Q8_0

| Config | Prompt 512 | Decode (0 ctx) | Decode 8K ctx | Decode 32K ctx | Max Context |
|--------|-----------|----------------|----------------|----------------|-------------|
| Q8_0 / Q8_0 | ~400 t/s | 54 t/s | 37 t/s | ~25 t/s | ~16K |
| **Q8_0 / Turbo3** | ~390 t/s | **54 t/s** | **54 t/s** | **54 t/s** | **>128K** |

**Key findings:**
- M5 Max is **memory-bound** — TurboQuant keeps decode FLAT at 54 t/s
- Q8_0 decodes slows 54→37→25 t/s as KV cache grows
- TurboQuant eliminates memory bandwidth bottleneck

## M4 Pro / M4 Max (Predicted)

| Model | M4 Pro (24GB) | M4 Max (48GB) |
|-------|--------------|---------------|
| 7B Q8_0 | 32K–64K ctx | 64K–128K ctx |
| 14B Q8_0 | 16K–32K ctx | 32K–64K ctx |
| 32B Q4_K_M | 8K–16K ctx | 16K–32K ctx |
| 70B Q4_K_M | ~4K ctx | 8K–16K ctx |

*Extrapolated from M4 Mini scaling; actual may vary.*

## Compute-Bound vs Memory-Bound

| Chip | Bound | TurboQuant Effect |
|------|-------|-------------------|
| **M4 Mini (16GB)** | Compute | Speed ~same, context 4-16× |
| **M4 Pro/Max** | Mixed | Speed slight hit, context 4-16× |
| **M5 Max (128GB)** | Memory | Speed **flat**, context 8-32× |

**Rule of thumb:** If decode slows as context grows → memory-bound → TurboQuant wins on speed. If decode flat → compute-bound → TurboQuant wins on context.

## GPU Offload Impact

| -ngl | Q8_0/Q8_0 | Q8_0/Turbo3 | Notes |
|------|-----------|-------------|-------|
| 0 (CPU) | 8 t/s | 6 t/s | Pure CPU, slow |
| 32 | 22 t/s | 19 t/s | Partial GPU |
| 99 (full) | 21.9 t/s | 20.2 t/s | Full Metal, best |

- TurboQuant Metal kernels optimized for full offload (-ngl 99)
- Partial offload adds CPU↔GPU copy overhead

## Test Methodology

```bash
# Standard benchmark
llama-bench -m model.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -n 128 -p 512 -d 8192

# Context scaling test
for ctx in 0 4096 8192 16384 32768 65536 131072; do
  llama-bench -m model.gguf \
    --cache-type-k q8_0 --cache-type-v turbo3 \
    -n 64 -p 256 -d $ctx
done
```

## Summary

| Scenario | Recommendation |
|----------|----------------|
| M4 Mini 16GB, need >8K context | **Turbo3 (Q8_0 K + Turbo3 V)** |
| M5 Max 128GB, any context | **Turbo3** (flat decode speed) |
| Max quality, short context (<4K) | Q8_0 / Q8_0 |
| Max context, quality secondary | Turbo2 (Q8_0 K + Turbo2 V) |
| Sliding window (SWA) models | Turbo3 + `TURBO_SPARSE_V=0` |