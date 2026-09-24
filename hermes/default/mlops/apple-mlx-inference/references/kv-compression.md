# TurboQuant KV Cache Compression

**Context**: Runtime compression of KV cache using same Hadamard + Lloyd-Max pipeline. Compressed cache dequantizes to FP16 for attention — compatible with sinks, sliding window, linear attention.

## Why KV Compression?

| Model | FP16 KV/token | TQ 3-bit KV/token | Savings | Decode Speed |
|-------|---------------|-------------------|---------|--------------|
| GPT-OSS-20B | 27.0 MB | 7.79 MB | 3.5× | **29.9 vs 90.6 tok/s (slower)** |
| GPT-OSS-120B | 45.0 MB | 11.83 MB | 3.8× | **8.7 vs 6.4 tok/s (FASTER)** |
| Qwen3.6-35B | 18 GB @ 63K | 17.5 GB @ 63K | ~0.5 GB | 45.7 vs 52 tok/s (slower) |
| Qwen3.5-122B | 161 MB | 150 MB | ~7% | 5.7 vs 5.4 tok/s (≈same) |

> **Key insight**: Speedup only when per-token KV is large (many heads × long context). On small-active MoEs, it's a memory win, not speed win. GPT-OSS-120B is unique — its KV geometry makes compression faster.

## v0.2 Mixed Precision (Required on TurboQuant Weights)

```python
from turboquant_mlx.layers import convert_cache_to_turboquant
from mlx_lm.models.cache import make_prompt_cache

cache = make_prompt_cache(model)
cache = convert_cache_to_turboquant(
    cache,
    k_bits=8,           # K precision critical (softmax amplifies error)
    v_bits=3,           # V tolerates 3-bit
    min_tokens_before_quant=128,  # Attention sink protection
    group_size=64,
)
```

### CLI Flags

```bash
turboquant-generate --model ./model-tq3 --prompt "..." \
  --kv-k-bits 8 --kv-v-bits 3 \
  --kv-min-tokens 128 --kv-group-size 64

turboquant-serve --model ./model-tq3 --port 8080 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128
```

## Bit-Width Selection Guide

| Base Weights | K bits | V bits | Sink | When |
|--------------|--------|--------|------|------|
| FP16/BF16 | 8 | 3 | 128 | **Default** — lossless quality, ~4× smaller |
| FP16/BF16 | 4 | 3 | 128 | More aggressive, small quality dip on dense attention |
| **TurboQuant (tq3)** | **8** | **3** | **128** | **Required** — symmetric K3 collapses on tq3 weights |
| Any | 8 | 4 | 128 | Highest fidelity TQ KV |

### Why K8 on TurboQuant Weights?

Stacking 3-bit K cache on top of 3-bit weight quantization compounds noise → generation collapses past ~1K tokens with K3/V3 on tq3 weights. K8/V3 is clean. Same K3/V3 is fine on stock FP16 weights.

## The "Speed Flip"

| Model | FP16 KV | TQ 3-bit KV | Winner | Why |
|-------|---------|-------------|--------|-----|
| GPT-OSS-20B | 90.6 | 29.9 | FP16 | Small per-token KV → dequant overhead > bandwidth savings |
| Qwen3.6-35B | 52.0 | 45.7 | FP16 | 3B active params → small KV |
| **GPT-OSS-120B** | **6.4** | **8.7** | **TQ** | **Large per-token KV → 4× bandwidth savings > dequant cost** |
| Qwen3.5-122B | 24-25 | ~24 | FP16 | Similar to 120B but different KV geometry |

> The flip is **model-specific**, not size-specific. GPT-OSS-120B's KV head count/geometry makes compression faster.

## Long-Context Behavior (Qwen3.6-35B, M5 Pro)

| Context | KV Config | Prompt tok/s | Decode tok/s | Peak Metal | Saved |
|---------|-----------|--------------|--------------|------------|-------|
| 65 tok | FP16 | 47.8 | 52.0 | 18.13 GB | — |
| 65 tok | K8/V3 | 76.1 | 45.7 | 18.12 GB | 0.01 GB |
| 2.5K | FP16 | 131.9 | 51.5 | 20.50 GB | — |
| 2.5K | K8/V3 | 133.4 | 38.2 | 20.55 GB | -0.05 GB |
| 14.5K | FP16 | 132.8 | 46.0 | 22.50 GB | — |
| 14.5K | K8/V3 | 132.6 | 16.7 | 21.94 GB | 0.56 GB |
| 63K | FP16 | 124.5 | 34.5 | 30.79 GB | — |
| 63K | K8/V3 (no sink) | 123.6 | 5.2 | 28.71 GB | 2.08 GB |

> **Decoding advantage widens with context** on small-KV models — FP16 pulls ahead. Use KV compression on small-active MoEs to **fit longer context**, not to go faster.

## Compatibility Matrix

| Feature | Supported | Notes |
|---------|-----------|-------|
| Attention sinks (GPT-OSS) | ✅ | Sink vectors flow through standard SDPA |
| Sliding window | ✅ | RotatingKVCache layers untouched |
| Linear attention (GatedDeltaNet) | ✅ | ArraysCache layers untouched |
| Hybrid architectures | ✅ | Per-layer cache type preserved |
| Prompt-first conversion | ✅ | Process prompt FP16, convert before generate |

## Programmatic Usage

```python
from turboquant_mlx.layers import convert_cache_to_turboquant, TurboQuantKVCache
from mlx_lm.models.cache import make_prompt_cache

# 1. Build cache (correct types for hybrid models)
cache = make_prompt_cache(model)

# 2. Convert to TurboQuant KV (v0.2 mixed K/V + sink)
cache = convert_cache_to_turboquant(
    cache,
    k_bits=8, v_bits=3,
    min_tokens_before_quant=128,
    group_size=64,
)

# 3. Generate
model(prompt_tokens, cache=cache)
for token in generate_loop(model, cache):
    ...
```

## v0.1 → v0.2 Migration

| v0.1 (Deprecated) | v0.2 (Current) |
|-------------------|----------------|
| `tq_bits=3` | `k_bits=8, v_bits=3` |
| Symmetric K=V=3 | Mixed K8/V3 |
| Works on FP16 weights | Required on tq3 weights |

Backward compatible: `tq_bits=3` still works (maps to symmetric K3/V3) but not recommended on TurboQuant weights.

## Server Note

Enabling any `--kv-*` flag forces **sequential request processing** (TurboQuant KV doesn't support cross-request cache merge). Correct trade-off for single-user; multi-client queues instead of batching.