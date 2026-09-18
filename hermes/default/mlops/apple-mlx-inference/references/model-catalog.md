# TurboQuant-MLX Pre-Converted Model Catalog

**Source**: Hugging Face Hub `manjunathshiva` namespace  
**Format**: MLX safetensors shards + `config.json` with `quantization.mode = "turboquant"`

## Dense Models

| Model | Repo | Size | Bits | Group | Speed (M4 Max) | Use Case |
|-------|------|------|------|-------|----------------|----------|
| Qwen3.6-27B | `manjunathshiva/Qwen3.6-27B-tq3-g32` | 13 GB | 3 | 32 | 14 tok/s | **Best coding on 48GB** |
| Nemotron-3-Nano-4B | `manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3` | 2.2 GB | 3 | 64 | 75 tok/s | Fast chat, reasoning trace |

## Mixture-of-Experts Models

| Model | Repo | Size | Bits | Group | Active | Experts | Speed (M4 Max) | Use Case |
|-------|------|------|------|-------|---------|----------------|----------|
| GPT-OSS-20B | `manjunathshiva/gpt-oss-20b-tq3` | 9.3 GB | 3 | 32 | 32 (top-?) | 73 tok/s | Beats MXFP4 |
| GPT-OSS-120B | `manjunathshiva/gpt-oss-120b-tq3` | 48 GB | 3 | 64 | 128 (top-?) | 44 tok/s | **Only 120B on 64GB** |
| Qwen3.6-35B-A3B | `manjunathshiva/Qwen3.6-35B-A3B-tq3-g32` | 16 GB | 3 | 32 | 256 (top-8) | 60 tok/s (res) / 4.5 tok/s (stream 16GB) | Hybrid linear-attn + MoE |
| Qwen3.5-122B-A10B | `manjunathshiva/qwen3.5-122b-tq3` | 50 GB | 3 | 64 | 256 (top-8) | 26.5 tok/s (64GB) | Reasoning, 256 experts |
| Nemotron-3-Super-120B | `manjunathshiva/Nemotron-3-Super-120B-A12B-tq3a-tq2e-g32` | 36 GB | 3/2 hybrid | 32 | 512 (latent) | 27 tok/s | Mamba+attention hybrid |
| Nemotron-3-Super-120B (full 3-bit) | `manjunathshiva/NVIDIA-Nemotron-3-Super-120B-A12B-BF16-tq3` | 50 GB | 3 | 64 | 512 | 18.7 tok/s | Math/numeric accuracy |

## Qwen3-235B-A22B Variants (Largest Open MoE)

| Variant | Repo | Size | Config | Stress Pass | Speed (64GB) | Notes |
|---------|------|------|--------|-------------|--------------|-------|
| **Hybrid ternary (article)** | `manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64` | **53 GB** | 3-bit attn + 1.58-bit ternary experts | 5/6 | 5.6 tok/s (res) / 0.2-4 tok/s (stream) | **Article model** |
| Full 3-bit (recall-critical) | `manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3-g32` | 103 GB | 3-bit everything | 6/6 | 1.3 tok/s (stream) | Exact literal recall |

## Prisma-ML Bonsai Models (Ternary Rebuilds of Qwen)

| Model | Repo | Size | Bits | Group | Active/Experts | Speed (M4 Pro) | Notes |
|-------|------|------|------|-------|----------------|----------------|-------|
| **Bonsai-27B (ternary)** | `prism-ml/Ternary-Bonsai-27B-tq1` | ~8 GB | **1.58-bit** ternary | 64 | 27B dense | **~25 tok/s (M4 Pro)** | **Runs on 16GB M4 Mini (4.2 GB RAM article)** |
| Bonsai-27B DSpark draft | `prism-ml/Ternary-Bonsai-27B-DSpark` | ~2 GB | 3-bit | 32 | — | Speculative | CUDA draft, not Mac yet |

### Bonsai-27B Article Details (macoclock Medium)

**Source**: "Bonsai-27B Runs on a 16 GB M4 Mac Mini with 4.2 GB of RAM: 1-bit Quantization with MLX" (macoclock, 2026)

- **Architecture**: Prisma-ML's 1.7-bit ternary rebuild of Qwen3.6-27B — full 27B-class reasoning model in ~8 GB
- **Quantization**: 1.58-bit ternary (base-3 trit packing) via TurboQuant-MLX
- **RAM on M4 Mini 16GB**: 4.2 GB peak (article measurement) — fits comfortably on 16GB unified memory
- **Speed**: ~25 tok/s on M4 Pro, ~20-25 tok/s on M4 Mini
- **Quality**: Lossless output (byte-identical to unquantized); DSpark draft accelerates CUDA path only (not Mac yet)
- **MLX Version Required**: 0.32.0+ (multi-row 2-bit matmul kernels for verification)
- **Key Innovation**: Hadamard rotation + Lloyd-Max codebooks = near-lossless at 1.58-bit; fused Metal kernels for dequant+GEMM

### Usage on 16GB M4 Mini

```bash
# Download (from Prisma-ML namespace, not manjunathshiva)
hf download prism-ml/Ternary-Bonsai-27B-tq1 --local-dir ~/models/bonsai-27b-tq1

# Generate
turboquant-generate \
  --model ~/models/bonsai-27b-tq1 \
  --prompt "Implement binary search in Python with type hints." \
  --max-tokens 512 --temp 0.7

# Serve OpenAI-compatible
turboquant-serve --model ~/models/bonsai-27b-tq1 --port 8080
```

### Comparison: Bonsai-27B vs Qwen3.6-27B (TurboQuant 3-bit)

| Aspect | Bonsai-27B (1.58-bit ternary) | Qwen3.6-27B (3-bit TurboQuant) |
|--------|-------------------------------|--------------------------------|
| Size | ~8 GB | ~13 GB |
| Peak RAM (M4 Mini 16GB) | **4.2 GB** | ~17.5 GB (needs 32GB+) |
| Speed (M4 Pro) | ~25 tok/s | ~14 tok/s |
| Quality | Near-lossless (ternary experts) | Lossless at 3-bit |
| DSpark Draft | Published (CUDA only) | Not yet |
| Best For | **16GB Macs, edge deployment** | 32GB+ Macs, maximum quality |

## Diffusion / VLM (Requires `turboquant-mlx-full[vlm]`)

| Model | Repo | Size | Bits | Notes |
|-------|------|------|------|-------|
| DiffusionGemma-26B-A4B | `manjunathshiva/diffusiongemma-26B-A4B-it-tq3-g32` | ~10 GB | 3 | Block-diffusion, 128 experts |

## Download Commands

```bash
# Dense coder (best daily driver for 48GB+)
hf download manjunathshiva/Qwen3.6-27B-tq3-g32 --local-dir ~/models/qwen3.6-27b-tq3-g32

# Streaming MoE for 16GB
hf download manjunathshiva/Qwen3.6-35B-A3B-tq3-g32 --local-dir ~/models/qwen3.6-35b-tq3-g32

# Article replication
hf download manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64 --local-dir ~/models/qwen3-235b-tq3a-tqTe-g64

# Fast small model
hf download manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3 --local-dir ~/models/nemotron-3-nano-4b-tq3

# 120B on 64GB
hf download manjunathshiva/gpt-oss-120b-tq3 --local-dir ~/models/gpt-oss-120b-tq3
hf download manjunathshiva/Nemotron-3-Super-120B-A12B-tq3a-tq2e-g32 --local-dir ~/models/nemotron-3-super-120b-tq3a-tq2e-g32
```

## Selection Guide for 16GB M2

| Priority | Model | Command |
|----------|-------|---------|
| **Daily coding** | Qwen3.6-27B resident | `turboquant-generate --model ~/models/qwen3.6-27b-tq3-g32` |
| **MoE on 16GB** | Qwen3.6-35B-A3B streaming | `stream_generate --cache-budget-gb 8` |
| **Article demo** | Qwen3-235B ternary streaming | `stream_generate --cache-budget-gb 6` |
| **Fastest chat** | Nemotron-3-Nano-4B | `turboquant-generate --model ~/models/nemotron-3-nano-4b-tq3` |

## Conversion Recipes

```bash
# Dense 3-bit (group-size 32 for <32K context, 64 for >32K)
python -m turboquant_mlx.convert --hf-path Qwen/Qwen3.6-27B --mlx-path ./out --bits 3 --group-size 32

# MoE 3-bit (GPT-OSS uses 32, Qwen uses 64)
python -m turboquant_mlx.convert --hf-path openai/gpt-oss-20b --mlx-path ./out --bits 3 --group-size 32

# Ternary experts (1.58-bit) — needs 128+ experts
python -m turboquant_mlx.convert --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 --mlx-path ./out --bits 3 --group-size 64 --ternary-experts --streaming

# Hybrid 3-bit attn / 2-bit experts (Nemotron Super)
python -m turboquant_mlx.convert --hf-path nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 --mlx-path ./out --bits 2 --attn-bits 3 --mlp-bits 2 --group-size 32

# Streaming for >100B models (peak RAM ~5-12 GB)
python -m turboquant_mlx.convert --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 --mlx-path /Volumes/SSD/out --bits 3 --group-size 64 --ternary-experts --streaming
```

## Quality Notes

- **Ternary (1.58-bit) experts**: Only works with ≥64 experts (128 for Qwen3-235B). 32-expert models (GPT-OSS-20B) collapse at <2-bit.
- **Nemotron-3-Super hybrid**: Math accuracy degrades with `--rep-penalty`. Omit for numeric work.
- **GPT-OSS-120B**: TurboQuant 3-bit is the ONLY way to run on 64GB (MXFP4 = 63.5 GB, affine 4-bit = 65.8 GB).
- **KV compression**: Mixed K8/V3 is lossless on FP16 weights, REQUIRED on TurboQuant weights (K3 collapses).