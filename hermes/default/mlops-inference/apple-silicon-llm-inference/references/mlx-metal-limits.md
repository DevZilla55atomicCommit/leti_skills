# MLX Metal Wired Memory Limits

## The Problem

Apple Silicon unified memory has a **GPU wired memory limit** (`iogpu.wired_limit_mb`) that caps how much memory Metal can lock for GPU buffers. This is separate from total RAM.

| Mac Model | Total RAM | Default Wired Limit | Usable for Models |
|-----------|-----------|---------------------|-------------------|
| M1/M2/M3/M4 16GB | 16 GB | ~8 GB (50%) | ~7-8 GB |
| M1/M2/M3/M4 32GB | 32 GB | ~16 GB (50%) | ~15-16 GB |
| M1/M2/M3/M4 48GB | 48 GB | ~24 GB (50%) | ~22-23-24 GB |
| M1/M2/M3/M4 64GB | 64 GB | ~32 GB (50%) | ~30-32 GB |
| M1/M2/M3/M4 96GB | 96 GB | ~48 GB (50%) | ~46-48 GB |
| M1/M2/M3/M4 128GB | 128 GB | ~64 GB (50%) | ~62-64 GB |

## Checking Current Limit

```bash
sysctl iogpu.wired_limit_mb
```

## Raising the Limit

**Temporary (until reboot):**
```bash
# 48GB Mac → 43 GB for GPU (leave 5 GB for OS)
sudo sysctl iogpu.wired_limit_mb=43008

# 64GB Mac → 57 GB for GPU (leave 7 GB for OS)
sudo sysctl iogpu.wired_limit_mb=57344

# 96GB Mac → 85 GB for GPU
sudo sysctl iogpu.wired_limit_mb=86016
```

**Permanent (survives reboot):**
```bash
echo "iogpu.wired_limit_mb=57344" | sudo tee -a /etc/sysctl.conf
```

## Recommended Settings by RAM

| Total RAM | Wired Limit (MB) | Leave for OS |
|-----------|------------------|--------------|
| 16 GB | 12288 (12 GB) | 4 GB |
| 32 GB | 26624 (26 GB) | 6 GB |
| 48 GB | 40960 (40 GB) | 8 GB |
| 64 GB | 57344 (56 GB) | 8 GB |
| 96 GB | 86016 (84 GB) | 12 GB |
| 128 GB | 114688 (112 GB) | 16 GB |

## Formula

```
wired_limit_mb = (total_ram_gb - os_reserve_gb) * 1024
```

**OS Reserve Guidelines:**
- 16 GB: 4 GB
- 32 GB: 6 GB
- 48 GB: 8 GB
- 64 GB+: 8-12 GB

## When You Need This

| Scenario | Required |
|----------|----------|
| MLX model > default wired limit | ✅ Yes |
| TurboQuant streaming (cache-budget + KV) > wired | ✅ Yes |
| `turboquant-generate` METAL OOM / watchdog panic | ✅ Yes |
| `mlx_lm.generate` on 48GB+ models | ✅ Yes |
| Ollama/llama.cpp (CPU inference) | ❌ No (uses CPU memory) |

## Verification

```bash
# After setting, verify model loads
python -c "
import mlx.core as mx
import mlx_lm
model, tokenizer = mlx_lm.load('mlx-community/Qwen2.5-32B-4bit')
print('Model loaded successfully')
print(f'Peak memory: {mx.metal.get_peak_memory() / 1e9:.1f} GB')
"
```

## Common Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `METAL: Out of memory` | Exceeded wired limit | Raise `iogpu.wired_limit_mb` |
| `watchdogd panic` / GPU restart | Allocation rate too high near limit | Raise limit + close other apps |
| `malloc` failure in Metal | Fragmented wired memory | Reboot, then raise limit before loading |

## TurboQuant + Metal Limits

For TurboQuant streaming:
```
Peak Metal = model_weights_in_cache + KV_cache + expert_cache (--cache-budget-gb)
```

Example (235B hybrid on 16GB):
- `--cache-budget-gb 4` → ~4 GB expert cache
- KV cache (4K context) → ~1 GB
- Shared weights (attn + embeddings) → ~2 GB
- **Total ~7 GB** → Need wired_limit ≥ 8192 MB (8 GB)

Default 16GB wired limit = 8 GB → **works but tight**.

## References

- Apple Developer: [Metal Resource Heaps](https://developer.apple.com/metal/)
- MLX Issue #412: [Wired memory limit](https://github.com/ml-explore/mlx/issues/412)
- TurboQuant-MLX benchmarks: `benchmarks/bench_m5_pro.py`