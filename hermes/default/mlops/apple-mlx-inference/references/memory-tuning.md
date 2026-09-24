# Apple Silicon Memory Tuning for MLX/TurboQuant

**Context**: Unified memory = single pool for CPU + GPU + OS. Metal enforces a **wired memory limit** (`iogpu.wired_limit_mb`) that caps GPU allocations. Exceeding it → `METAL Command buffer execution failed: Insufficient Memory` or watchdog panic.

## The Wired Memory Limit

| Total RAM | Default Wired (~50%) | Recommended (leave headroom) | sysctl Value |
|-----------|---------------------|------------------------------|--------------|
| 16 GB | ~8 GB | **12 GB** | `12288` |
| 32 GB | ~16 GB | **26 GB** | `26624` |
| 48 GB | ~24 GB | **42 GB** | `43008` |
| 64 GB | ~32 GB | **56 GB** | `57344` |
| 96 GB | ~48 GB | **84 GB** | `86016` |
| 128 GB | ~64 GB | **112 GB** | `114688` |

> **Rule**: Leave 4-8 GB for macOS + userland. `iogpu.wired_limit_mb = (total_GB - 4) * 1024` is a safe starting point.

## Commands

```bash
# Check current limit
sysctl iogpu.wired_limit_mb

# Set for current session (requires sudo, resets on reboot)
sudo sysctl iogpu.wired_limit_mb=12288  # 16GB Mac

# Make permanent (survives reboot)
echo "iogpu.wired_limit_mb=12288" | sudo tee -a /etc/sysctl.conf

# Verify after reboot
sysctl iogpu.wired_limit_mb
```

## Prompt Cache Capping (Prevents Multi-Turn OOM)

`mlx_lm.server` / `turboquant-serve` keeps a persistent prompt cache per conversation. Each turn grows it until wired limit.

```bash
# Hard byte cap on prompt cache (evicts oldest when exceeded)
turboquant-serve \
  --model ./model-tq3 \
  --port 8080 \
  --prompt-cache-bytes 2147483648  # 2 GB cap

# Or single-sequence cache (minimal memory)
turboquant-serve \
  --model ./model-tq3 \
  --port 8080 \
  --prompt-cache-size 1
```

| Cap | Use Case |
|-----|----------|
| 2 GB (2147483648) | Default recommendation for 120B on 64GB |
| 512 MB (536870912) | Tight memory, many short conversations |
| `--prompt-cache-size 1` | Maximum stability, no prefix caching |

## Combined Recipe: Nemotron-3-Super-120B on 64GB

```bash
# 1. Raise wired limit (once per boot)
sudo sysctl iogpu.wired_limit_mb=57344

# 2. Serve with KV compression + prompt cache cap
turboquant-serve \
  --model ./nemotron-3-super-120b-tq3 \
  --port 8080 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128 \
  --prompt-cache-bytes 2147483648
```

## Watchdog Panic Avoidance

**Symptom**: `AppleARMWatchdogTimer` / `watchdogd` kernel panic during long prefill.

**Cause**: Rapidly growing KV cache forces continuous Metal page commits (`AGXG17XFamilyResidencySet_commitAddedAllocations`). The **allocation rate**, not peak, triggers the watchdog.

**Mitigations**:
1. **Raise wired limit** (biggest lever)
2. **Use K8/V3 KV compression** — smaller per-token allocation rate
3. **Limit context length** — 14.5K tokens safe on 48GB with K8/V3; 63K needs headroom
4. **Close GPU consumers** — Chrome, Electron apps, Final Cut, Xcode simulators hold 1-2 GB each

### Safe Context Limits (48GB M5 Pro, Qwen3.6-35B-tq3)

| KV Config | Max Safe Context | Peak Metal |
|-----------|------------------|------------|
| FP16 | ~14.5K | 22.5 GB |
| K8/V3 | ~14.5K | 21.9 GB |
| K8/V3 | 63K | **28.7 GB** (risky, near 42 GB wired cap) |

> On 16GB with raised limit (12 GB): keep context < 8K for streaming models, < 4K for resident.

## 16GB M2 MacBook Pro Specifics

### Default Constraints
- Wired limit: **~8 GB** (default 50%)
- Usable for model: **~6-7 GB** after OS
- With `iogpu.wired_limit_mb=12288`: **~12 GB** model, **~4 GB** OS

### What Fits Resident (with raised limit)

| Model | Peak RAM | Fits? |
|-------|----------|-------|
| Nemotron-3-Nano-4B | 4.3 GB | ✅ Easy |
| Qwen3.6-27B tq3 | 17.5 GB | ❌ No (needs 24GB+) |
| GPT-OSS-20B tq3 | 12 GB | ✅ With 12 GB limit |
| Qwen3.6-35B tq3 | 18 GB | ❌ No |

### What Works via Streaming (with raised limit)

| Model | Cache Budget | Peak RAM | Works? |
|-------|--------------|----------|--------|
| Qwen3.6-35B-A3B | 8 GB | ~9.5 GB | ✅ Comfortable |
| Qwen3.5-122B-A10B | 4 GB | ~9 GB | ✅ Tight |
| Qwen3-235B ternary | 6 GB | ~10.5 GB | ✅ At limit |

## Quick Reference Card

```bash
# 16GB M2 - Daily driver setup
sudo sysctl iogpu.wired_limit_mb=12288
echo "iogpu.wired_limit_mb=12288" | sudo tee -a /etc/sysctl.conf

# Resident small model (Nemotron Nano, GPT-OSS-20B)
turboquant-generate --model ./model --max-tokens 512

# Streaming MoE (Qwen3.6-35B, Qwen3-235B)
python -m turboquant_mlx.stream.stream_generate \
  --model ./model \
  --cache-budget-gb 8 \
  --prefetch-workers 8 \
  --max-active-experts 4 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128

# Server with safety caps
turboquant-serve \
  --model ./model \
  --port 8080 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128 \
  --prompt-cache-bytes 2147483648
```

## Monitoring

```bash
# Metal memory usage (requires sudo)
sudo metal -d 1  # Not available on macOS

# Proxy: check process RSS + GPU via Activity Monitor / iostat
# iostat -d 1  # SSD bandwidth during streaming

# MLX peak memory (in Python)
import mlx.core as mx
mx.set_memory_limit(12 * 1024**3)  # 12 GB limit
print(mx.get_peak_memory() / 1024**3, "GB")
```

## Related Skills

- `nvidia-api-provider-debugging` — Native NVIDIA provider config (this user prefers native over gateway)
- `mlops/inference/serving-llms-vllm` — NVIDIA GPU serving (different stack)