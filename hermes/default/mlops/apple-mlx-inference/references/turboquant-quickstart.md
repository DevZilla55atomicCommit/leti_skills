# TurboQuant-MLX Quickstart — 16GB M2 MacBook Pro Session

**Date**: 2026-07-10  
**User**: Alfred (M2 16GB MacBook Pro)  
**Goal**: Set up TurboQuant-MLX for extreme quantization + expert streaming on 16GB unified memory

## Install

```bash
pip install turboquant-mlx-full
# Verified: import turboquant_mlx works
```

## Model Downloads (Pre-converted from Hub)

```bash
# 1. Practical daily driver: Qwen3.6-27B dense coder (13 GB, 14 tok/s resident)
hf download manjunathshiva/Qwen3.6-27B-tq3-g32 \
  --local-dir ~/models/qwen3.6-27b-tq3-g32

# 2. Best streaming MoE: Qwen3.6-35B-A3B (16 GB, 4.5 tok/s on 16GB)
hf download manjunathshiva/Qwen3.6-35B-A3B-tq3-g32 \
  --local-dir ~/models/qwen3.6-35b-tq3-g32

# 3. Article replication: Qwen3-235B ternary experts (53 GB, 0.5 tok/s streaming)
hf download manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64 \
  --local-dir ~/models/qwen3-235b-tq3a-tqTe-g64

# 4. Tiny speed demon: Nemotron-3-Nano-4B (2.2 GB, 75 tok/s)
hf download manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3 \
  --local-dir ~/models/nemotron-3-nano-4b-tq3
```

## Memory Tuning (Required for Resident Models on 16GB)

```bash
# Raise Metal wired limit to 12GB (leaves 4GB for macOS)
sudo sysctl iogpu.wired_limit_mb=12288

# Make permanent
echo "iogpu.wired_limit_mb=12288" | sudo tee -a /etc/sysctl.conf
```

## Test Commands

### Resident Dense Model (Qwen3.6-27B)

```bash
turboquant-generate \
  --model ~/models/qwen3.6-27b-tq3-g32 \
  --prompt "Write a Python function that merges overlapping intervals. Include type hints and docstring." \
  --max-tokens 1024 --temp 0.7
```

### Streaming MoE (Qwen3.6-35B-A3B)

```bash
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3.6-35b-tq3-g32 \
  --prompt "Write a Python function that merges overlapping intervals." \
  --max-tokens 512 --cache-budget-gb 8 --prefetch-workers 8
```

### Article Replication (Qwen3-235B Ternary Streaming)

```bash
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3-235b-tq3a-tqTe-g64 \
  --prompt "Explain why the sky is blue." \
  --max-tokens 512 --cache-budget-gb 6 --prefetch-workers 8
```

### OpenAI-Compatible Server (for Cursor/VS Code)

```bash
# Resident model
turboquant-serve --model ~/models/qwen3.6-27b-tq3-g32 --port 8080

# Streaming MoE (single-user)
turboquant-serve \
  --model ~/models/qwen3.6-35b-tq3-g32 \
  --cache-budget-gb 8 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128 \
  --prompt-concurrency 1 --port 8080
```

### Client Usage

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "~/models/qwen3.6-27b-tq3-g32",
    "messages": [{"role": "user", "content": "Write a Python merge intervals function"}],
    "max_tokens": 1024,
    "temperature": 0.7
  }'
```

## Practical Alternative: Nemotron-3-Nano-4B via Ollama (Fastest Setup)

If TurboQuant-MLX compilation or model downloads are problematic, Ollama provides a pre-quantized GGUF version that runs instantly:

```bash
# Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh

# Pull and run Nemotron-3-Nano-4B (4B params, ~2.8 GB GGUF q4_k_m)
ollama pull nemotron-3-nano:4b
ollama run nemotron-3-nano:4b "Write a Python function that merges overlapping intervals."
```

| Aspect | Ollama Nemotron-3-Nano | TurboQuant-MLX Nemotron-3-Nano |
|--------|------------------------|--------------------------------|
| Download | ~2.8 GB | ~2.2 GB (safetensors) |
| Setup time | ~30 sec | ~5 min (pip install + download) |
| Speed | ~30-50 tok/s | **75 tok/s** |
| RAM | ~4 GB | ~4.3 GB |
| Quality | Good | Slightly better (TurboQuant 3-bit) |
| Use case | **Fastest path to working model** | Maximum performance |

Tested 2026-07-10: Nemotron-3-Nano-4B via Ollama produces clean, typed code with docstrings at ~35 tok/s on M2 16GB.

### Prisma-ML Bonsai-27B (M4 Mini 16GB Article Model)

**From: [MacOClock article](https://medium.com/macoclock/bonsai-27b-runs-on-a-16-gb-m4-mac-mini-with-4-2-gb-of-ram-1-bit-quantization-with-mlx-662a30587822)**

```bash
# Download (from Prisma-ML namespace)
hf download prism-ml/Ternary-Bonsai-27B-tq1 --local-dir ~/models/bonsai-27b-tq1

# Generate (~25 tok/s on M4 Pro, ~20-25 on M4 Mini, 4.2 GB RAM)
turboquant-generate \
  --model ~/models/bonsai-27b-tq1 \
  --prompt "Implement binary search in Python with type hints." \
  --max-tokens 512 --temp 0.7

# Serve OpenAI-compatible
turboquant-serve --model ~/models/bonsai-27b-tq1 --port 8080
```

**Specs**: 1.58-bit ternary (base-3 trit packing), ~8 GB disk, **4.2 GB peak RAM on M4 Mini 16GB**, lossless output, requires MLX 0.32.0+.

## Expected Performance (M2 16GB)

| Model | Mode | Peak RAM | Speed | Quality |
|-------|------|----------|-------|---------|
| Qwen3.6-27B | Resident | ~17.5 GB | **14 tok/s** | SWE-bench grade |
| Qwen3.6-35B-A3B | Streaming (cache=8GB) | ~9-10 GB | **4.5 tok/s** | Strong MoE coder |
| Qwen3-235B ternary | Streaming (cache=6GB) | ~10-11 GB | **0.5 tok/s** | Full 235B reasoning |
| Nemotron-3-Nano-4B | Resident | ~4.3 GB | **75 tok/s** | Limited (4B) |

## Key Flags Reference

| Flag | Purpose | Typical Value |
|------|---------|---------------|
| `--cache-budget-gb` | Expert cache size (streaming) | 4-8 (16GB), 30-40 (64GB) |
| `--prefetch-workers` | Parallel SSD reads | 8 (NVMe), 1 (USB) |
| `--max-active-experts` | K-reduction (fewer experts/token) | 4 (safe), 0 (native) |
| `--kv-k-bits / --kv-v-bits` | Mixed KV precision | 8 / 3 (recommended) |
| `--kv-min-tokens` | FP16 sink tokens | 128 |
| `--min-tokens` | Mask EOS for thinking models | 50 (Nemotron) |

## Conversion (If Needed)

```bash
# Dense model 3-bit
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3.6-27B \
  --mlx-path ./qwen3.6-27b-tq3-g32 \
  --bits 3 --group-size 32

# MoE with streaming (for 200B+)
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 \
  --mlx-path /Volumes/SSD/qwen3-235b-tq3a-tqTe-g64 \
  --bits 3 --group-size 64 --ternary-experts --streaming

# Hybrid 3-bit attn / 2-bit experts
python -m turboquant_mlx.convert \
  --hf-path nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 \
  --mlx-path ./nemotron-3-super-120b-tq3a-tq2e-g32 \
  --bits 2 --attn-bits 3 --mlp-bits 2 --group-size 32
```