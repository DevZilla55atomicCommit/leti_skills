# TurboQuant-MLX Streaming MoE on 16GB Mac (Session Notes)

## Session Context
**Hardware**: MacBook Pro M2 16GB
**Models Tested**: Qwen3-235B-A22B (tq3a-tqTe-g64, 53 GB), Qwen3.6-35B-A3B (tq3-g32, 16 GB), Nemotron-3-Nano-4B (tq3, 2.2 GB)
**Date**: 2025-07-10

---

## Key Findings

### 1. Streaming MoE Works on 16GB — But Slow
- **Qwen3-235B (tq3a-tqTe-g64, 53 GB)**: ~0.2 tok/s cold, ~1-4 tok/s warm with `--cache-budget-gb 6`
- **Qwen3.6-35B-A3B (tq3-g32, 16 GB)**: ~4.5 tok/s with `--cache-budget-gb 8`
- **Nemotron-3-Nano-4B (tq3, 2.2 GB resident)**: 75 tok/s — best daily driver for 16GB

### 2. Required Configuration for 16GB
```bash
# Must raise Metal wired memory limit (requires sudo, resets on reboot)
sudo sysctl iogpu.wired_limit_mb=12288
echo "iogpu.wired_limit_mb=12288" | sudo tee -a /etc/sysctl.conf

# Close memory-heavy apps (Chrome, Slack, Docker, Xcode)
# Use internal SSD (Thunderbolt/NVMe external helps streaming)
```

### 3. Streaming Command Template
```bash
python -m turboquant_mlx.stream.stream_generate \
  --model /path/to/model \
  --prompt "Your prompt here" \
  --max-tokens 512 \
  --cache-budget-gb 6 \       # 4-8 GB sweet spot for 16GB
  --prefetch-workers 8 \      # Parallel SSD reads (default 8)
  --max-active-experts 4      # K-reduction: 8→4 cuts I/O ~2x, bit-identical
```

### 4. Model-Specific Results

| Model | Quant | Disk | Cache Budget | Speed | Notes |
|-------|-------|------|--------------|-------|-------|
| Qwen3-235B-A22B | tq3a-tqTe-g64 | 53 GB | 6 GB | 0.2-4 tok/s | Ternary experts, 5/6 stress pass |
| Qwen3.6-35B-A3B | tq3-g32 | 16 GB | 8 GB | 4.5 tok/s | Best practical MoE for 16GB |
| Nemotron-3-Nano-4B | tq3 | 2.2 GB | N/A (resident) | 75 tok/s | **Best daily driver** |
| Qwen3.6-27B (dense) | tq3-g32 | 13 GB | N/A (resident) | 14 tok/s | SWE-bench grade coder |

### 5. Download Commands (Hugging Face)
```bash
# Qwen3-235B ternary experts (article model)
hf download manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64 \
  --local-dir ~/models/qwen3-235b-tq3a-tqTe-g64

# Qwen3.6-35B-A3B streaming
hf download manjunathshiva/Qwen3.6-35B-A3B-tq3-g32 \
  --local-dir ~/models/qwen3.6-35b-tq3-g32

# Nemotron-3-Nano-4B (fast, resident)
hf download manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3 \
  --local-dir ~/models/nemotron-3-nano-4b-tq3
```

### 6. Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `METAL: Out of memory` / watchdog panic | `iogpu.wired_limit_mb` too low | Raise to 12288 (12GB) for 16GB machine |
| Generation freezes at 0 tok/s | Cache budget too small / slow SSD | Increase `--cache-budget-gb`, use faster drive |
| `OSError: [Errno 24] Too many open files` | 19 shards + experts open | `ulimit -n 65536` |
| Download stalls at 55% | Unauthenticated HF rate limit | `hf auth login` or set `HF_TOKEN` |
| Conversion OOM on 64GB | Full model materialized in RAM | Add `--streaming` flag (peak ~8-12 GB) |

### 7. Quality Notes
- **Ternary experts (1.58-bit)** work on 128-expert models (redundancy) but fail on 32-expert (GPT-OSS-20B)
- **Full 3-bit** passes 6/6 stress tests (exact recall); **ternary hybrid** passes 5/6 (fuzzy recall on needle-in-haystack)
- **Nemotron-3-Super-120B math accuracy** degrades with `--rep-penalty` (Phase 1 limitation)

---

## Practical Recommendation for 16GB M2

**Daily driver**: `Nemotron-3-Nano-4B-tq3` (75 tok/s, 4.3 GB RAM, resident)
**Heavy coding**: `Qwen3.6-27B-tq3-g32` (14 tok/s, 17.5 GB RAM — needs 48GB+ for comfort)
**MoE demo**: `Qwen3.6-35B-A3B-tq3-g32` streaming (4.5 tok/s, 10 GB peak)
**Extreme demo**: `Qwen3-235B-tq3a-tqTe-g64` streaming (0.5 tok/s, 11 GB peak)

**Skip on 16GB**: Full 3-bit 235B (103 GB), GPT-OSS-120B (48 GB), Nemotron-3-Super-120B (36+ GB)