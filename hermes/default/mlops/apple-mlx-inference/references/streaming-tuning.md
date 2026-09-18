# TurboQuant-MLX Expert Streaming Tuning

**Context**: Run MoE models larger than RAM by paging only router-selected experts from disk per token. Output is bit-identical to fully-resident model.

## Core Concept

- **Expert Cache**: LRU cache of expert weights in unified memory
- **Disk Reads**: `os.pread` + `F_NOCACHE` (bypass OS page cache) on macOS
- **Parallel Prefetch**: `--prefetch-workers` threads read next-layer experts while current layer computes
- **K-Reduction**: `--max-active-experts K` caps router top-k, cuts disk I/O ~2×

## Key Flags

| Flag | Default | Purpose | Tuning |
|------|---------|---------|--------|
| `--cache-budget-gb` | Required | Expert cache size in GB | **Primary lever** — larger = higher hit-rate = faster |
| `--prefetch-workers` | 8 | Parallel read threads | 8 for NVMe, 1 for USB; auto-disables if bandwidth-saturated |
| `--max-active-experts` | 0 (native) | K-reduction cap on router top-k | 4 = safe (2× less I/O), 2 = broken, 0 = native |
| `--use-page-cache` / `--no-page-cache` | Auto | OS page cache vs F_NOCACHE | Auto-enables when model < 0.6× RAM |
| `--prefetch-ahead` | 0 | Speculative next-layer prefetch | 1 on fast NVMe with headroom |
| `--pin-file` | None | Hot expert pinning (experimental) | Net-negative vs pure LRU in tests |

## Cache Budget Sweep (Qwen3.6-35B-A3B, 16GB M4 Mini)

| Cache Budget | Hit Rate | Disk Read/Token | Decode | Peak RSS |
|--------------|----------|-----------------|--------|----------|
| 2 GB | 60% | ~175 MB | 3.0 tok/s | 3.9 GB |
| **8 GB** | **91%** | **~41 MB** | **4.5 tok/s** | **9.4 GB** |
| 12 GB | 93% | ~35 MB | 4.7 tok/s | 13 GB |

> **Sweet spot on 16GB**: 8 GB cache → 91% hit-rate, ~9.4 GB peak (under Metal wired limit ~10.5 GB)

## Cache Budget Sweep (Qwen3.5-122B-A10B, 48GB M5 Pro)

| Cache Budget | Hit Rate | Decode | E2E | Peak Metal | Disk Read |
|--------------|----------|--------|-----|------------|-----------|
| 20 GB | 80.9% | 7.1 | 6.1 | 24.2 GB | 80.7 GB |
| **30 GB** | **90.3%** | **9.1** | **7.6** | **34.2 GB** | **40.9 GB** |
| 38 GB | 91.0% | 8.9 | 7.5 | 42.2 GB | 38.0 GB |

> **Sweet spot on 48GB**: 30 GB cache → 90%+ hit-rate, 14 GB headroom. Pushing to 38 GB peaks at wired limit with negligible gain.

## Prefetch Workers Impact (122B, 30 GB cache, 256 tokens)

| Workers | Gen tok/s | E2E tok/s | Disk Read | Hit Rate |
|---------|-----------|-----------|-----------|----------|
| 1 (serial) | 7.4 | 5.7 | 44.3 GB | 89.5% |
| **8 (parallel)** | **9.1** | **7.6** | **41.9 GB** | **90.1%** |
| Speedup | **1.23×** | **1.33×** | | |

## K-Reduction (Qwen3.6-35B-A3B, Native top-8)

| `--max-active-experts` | Disk Read/Token | Decode Speedup | Quality |
|------------------------|-----------------|----------------|---------|
| 0 (native top-8) | 1.0× | 1.0× | Reference |
| **4** | **~2.1× less** | **~1.4× faster** | **Byte-identical on 6-test harness** |
| 2 | ~3× less | ~1.8× faster | **Collapses (broken JSON)** |

> **Safe floor**: 4 experts. 2 breaks routing normalization.

## Page Cache vs F_NOCACHE

| Scenario | Mode | Decode Speed | Why |
|----------|------|--------------|-----|
| Model fits in free RAM (e.g., 35B on 64GB) | `--use-page-cache` (auto) | **2.44× faster** (7.58 → 18.5 tok/s) | Re-reads from warm RAM, not disk |
| Model > RAM (e.g., 122B on 16GB) | `--no-page-cache` (auto) | Baseline | Prevents OS page cache thrashing |

> **Auto-logic**: Enables page cache only when model files < 0.6× total RAM.

## 16GB M2 MacBook Pro Specifics

### Hardware Constraints
- **SSD**: ~2-3 GB/s sequential (internal), less on thermal throttle
- **Metal Wired Limit**: Default ~8 GB (50% of 16GB), raise to 12 GB via `iogpu.wired_limit_mb=12288`
- **Unified Memory**: Single pool for CPU + GPU + OS — expert cache competes with KV cache + OS

### Recommended Configs

```bash
# Qwen3.6-35B-A3B (best MoE for 16GB)
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3.6-35b-tq3-g32 \
  --cache-budget-gb 8 \
  --prefetch-workers 8 \
  --max-active-experts 4 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128

# Qwen3-235B ternary (article demo)
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3-235b-tq3a-tqTe-g64 \
  --cache-budget-gb 6 \
  --prefetch-workers 8 \
  --max-active-experts 4
```

### Expected Performance (M2 16GB)

| Model | Cache | Hit Rate | Disk/Token | Decode | Peak RAM |
|-------|-------|----------|------------|--------|----------|
| Qwen3.6-35B | 8 GB | ~91% | ~40 MB | **4.5 tok/s** | ~9.5 GB |
| Qwen3-235B ternary | 6 GB | ~38% | ~3.2 GB | **0.5 tok/s** | ~10.5 GB |
| Qwen3-235B ternary | 4 GB | ~30% | ~3.5 GB | **0.2 tok/s** | ~9 GB |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Metal out of memory` / watchdog panic | Peak > wired limit | Raise `iogpu.wired_limit_mb`, reduce `--cache-budget-gb`, close Chrome/Electron |
| 0.1 tok/s sustained | SSD saturated / USB drive | Use internal NVMe, increase `--cache-budget-gb`, check `iostat` |
| `--prefetch-workers 8` slower than 1 | Drive bandwidth saturated | Drop to 1 or 2; auto-disables if detected |
| Quality degrades with K-reduction | `--max-active-experts` too low | Keep ≥4; 2 breaks normalization |
| `KeyError: 'turboquant'` in server | mlx_lm.server doesn't know TurboQuant | Use `turboquant-serve` not `mlx_lm.server` |

## Calibration (Experimental)

```bash
# Generate routing trace → pin.json (hot experts) + perm.json (co-activation)
python -m turboquant_mlx.stream.calibrate_experts \
  --model ~/models/qwen3.6-35b-tq3-g32 \
  --prompt-file prompts.txt --num-tokens 2000 \
  --output-dir ./calibration

# Optional: Relayout experts on disk by co-activation (byte-identical)
python -m turboquant_mlx.stream.repack_experts \
  --model ~/models/qwen3.6-35b-tq3-g32 \
  --perm-file ./calibration/perm.json \
  --output-dir ./repacked
```

> **Note**: Pinning measured net-negative vs pure LRU on 122B (static costs adaptivity). For experimentation only.