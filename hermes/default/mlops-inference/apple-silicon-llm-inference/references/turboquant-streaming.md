# TurboQuant-MLX Expert Streaming Deep Dive

## Overview

TurboQuant-MLX implements **expert streaming** for MoE (Mixture-of-Experts) models, allowing models whose total weights exceed RAM to run by paging only the router-selected experts from disk per token.

## How Expert Streaming Works

```
Token t → Router → Top-K Experts → Load K experts from disk → Compute → Next token
                     ↑
              LRU Expert Cache (--cache-budget-gb)
```

**Key insight:** Only ~8 of 128/256 experts active per token → stream those 8 from SSD.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TurboQuant-MLX Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│  1. CONVERT (--streaming)                                   │
│     HF → Quantized shards (1 shard/layer) → Disk           │
│     Peak RAM: ~1 shard + 1 layer (~5-8 GB)                 │
│                                                             │
│  2. LOAD (stream_generate)                                  │
│     - Memory-maps all shards                                │
│     - Builds expert index (layer → expert → file offset)   │
│     - Initializes LRU ExpertCache (--cache-budget-gb)      │
│                                                             │
│  3. GENERATE (per token)                                    │
│     a. Router logits → Top-K expert IDs                    │
│     b. Check cache → miss → async read from SSD            │
│     c. Prefetch next layer's predicted experts             │
│     d. Compute → update LRU                                │
└─────────────────────────────────────────────────────────────┘
```

## Critical Parameters

| Parameter | Purpose | 16GB M2 | 48GB M2 Max | 64GB M4 Max |
|-----------|---------|---------|-------------|-------------|
| `--cache-budget-gb` | Expert LRU cache size | 4–6 | 30–38 | 40–50 |
| `--prefetch-workers` | Parallel SSD reads | 8 | 8 | 8 |
| `--max-active-experts` | K-reduction (router top-k) | 4 | 4 | 8 |
| `--prefetch-ahead` | Speculative prefetch layers | 1 | 1 | 1 |

## Cache Budget Tuning

```bash
# 16GB Mac Mini - Qwen3-235B hybrid
# Cache = expert weights in Metal. KV cache separate.
# Target: peak Metal < wired_limit_mb (default ~8GB on 16GB)
python -m turboquant_mlx.stream.stream_generate \
  --model ./qwen3-235b-tq3a-tqTe-g64 \
  --cache-budget-gb 4 \
  --prefetch-workers 8 \
  --max-active-experts 4

# 64GB M4 Max - full 235B resident
sudo sysctl iogpu.wired_limit_mb=57344
python -m turboquant_mlx.stream.stream_generate \
  --model ./qwen3-235b-tq3-g32 \
  --cache-budget-gb 40 \
  --prefetch-workers 8
```

## Quality Tiers (Qwen3-235B-A22B)

| Build | Config | Size | Quality | 16GB Speed |
|-------|--------|------|---------|------------|
| **tq3a-tqTe** | 3-bit attn + **ternary experts** | 53 GB | 5/6 probes | ~0.5–4 tok/s |
| **tq3a-tq2e** | 3-bit attn + 2-bit experts | ~47 GB | 4/6 probes | ~1–5 tok/s |
| **tq3** | Full 3-bit | 103 GB | 6/6 probes | Streaming only |

**Ternary (1.58-bit) experts:** Uses base-3 trit packing (20 trits/uint32 = 1.58 bpw). Requires ≥128 experts for redundancy.

## Performance Optimization

### SSD Matters
| Drive | 235B tok/s (4GB cache) | 35B tok/s (8GB cache) |
|-------|------------------------|----------------------|
| Internal M2 SSD | 0.2–0.5 | 2–4 |
| Thunderbolt NVMe | 0.5–1.5 | 4–8 |
| USB 3.1 SSD | 0.1–0.3 | 1–2 |

### Prefetch Workers
```bash
# Serial (baseline)
--prefetch-workers 1

# Parallel (8 workers) → ~1.9x speedup on fast NVMe
--prefetch-workers 8
```

### K-Reduction (max-active-experts)
```bash
# Native router top-k (e.g., 8 for Qwen3-235B)
--max-active-experts 0

# Reduced to 4 → ~2x less disk I/O, bit-identical output on 128-expert models
--max-active-experts 4

# ⚠️ 2 breaks JSON formatting on 128-expert models
--max-active-experts 2
```

## Common Issues

| Error | Fix |
|-------|-----|
| `METAL: Out of memory` | Lower `--cache-budget-gb` or raise `iogpu.wired_limit_mb` |
| `OSError: [Errno 24] Too many open files` | `ulimit -n 65536` |
| Generation hangs at 0 tok/s | Cache budget too small → increase `--cache-budget-gb` |
| `KeyError: expert_proj_up` | Model uses different expert key prefix → check `loader.py` auto-detect |

## Benchmark Commands

```bash
# 35B on 16GB (resident if fits, else streaming)
python -m turboquant_mlx.stream.stream_generate \
  --model manjunathshiva/Qwen3.6-35B-A3B-tq3-g32 \
  --prompt "Explain transformer attention" \
  --max-tokens 512 --cache-budget-gb 8 --prefetch-workers 8

# 235B hybrid on 16GB
python -m turboquant_mlx.stream.stream_generate \
  --model manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64 \
  --prompt "Write a Python async HTTP client" \
  --max-tokens 512 --cache-budget-gb 4 --prefetch-workers 8
```

## Conversion from HF

```bash
# Hybrid ternary experts (recommended for 235B)
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 \
  --mlx-path ./qwen3-235b-tq3a-tqTe-g64 \
  --bits 3 --group-size 64 --ternary-experts --streaming

# Full 3-bit (quality-critical)
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 \
  --mlx-path ./qwen3-235b-tq3-g32 \
  --bits 3 --group-size 32 --streaming

# 35B MoE (Qwen3.6)
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3.6-35B-A3B \
  --mlx-path ./qwen3.6-35b-tq3-g32 \
  --bits 3 --group-size 32 --streaming
```

## References

- [TurboQuant Paper (Zandieh et al., 2025)](https://arxiv.org/abs/2501.xxxxx)
- [Flash-MoE: Apple LLM in a Flash](https://arxiv.org/abs/2312.xxxxx) — K-reduction & trust-OS
- [TurboQuant-MLX GitHub](https://github.com/nathannorthcutt/turboquant-mlx)