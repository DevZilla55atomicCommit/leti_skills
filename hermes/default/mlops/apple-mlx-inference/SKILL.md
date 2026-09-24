---
name: apple-mlx-inference
description: Apple MLX framework inference workflows for Apple Silicon. Covers MLX-LM, TurboQuant-MLX extreme quantization, model conversion, expert streaming for MoE, and OpenAI-compatible serving. Targets M1/M2/M3/M4 Macs with unified memory.
version: 1.0.0
author: Alfred Kamisese
license: MIT
tags: [apple-silicon, mlx, mlx-lm, turboquant, quantization, moe, expert-streaming, llm-inference, m1, m2, m3, m4]
metadata:
  hermes:
    tags: [apple-silicon, mlx, mlx-lm, turboquant, quantization, moe, expert-streaming, llm-inference, m1, m2, m3, m4]
---

# Apple MLX Inference

Complete workflow for running LLMs locally on Apple Silicon using the MLX framework. Includes standard MLX-LM usage, TurboQuant-MLX extreme quantization (1.58-bit ternary), expert streaming for MoE models beyond RAM, and OpenAI-compatible serving.

## When to Use

- Run LLMs on M1/M2/M3/M4 Macs with unified memory
- Quantize models to 2-4 bit with TurboQuant (beats standard affine/GPTQ)
- Stream MoE experts from disk to run 100B+ models on 16-64GB RAM
- Serve models via OpenAI-compatible API for Cursor/VS Code/Claude Code integration
- Benchmark and evaluate quantized model quality

## Prerequisites

- macOS 13+ (Ventura or later)
- Apple Silicon (M1/M2/M3/M4)
- Python 3.10+
- Unified memory: 16GB minimum, 48GB+ recommended for 20B+ models

## Installation

### Standard MLX-LM

```bash
pip install mlx-lm huggingface_hub
```

### TurboQuant-MLX (Extreme Quantization + Expert Streaming)

```bash
# From PyPI (stable)
pip install turboquant-mlx-full

# From source (latest streaming fixes)
git clone https://github.com/nathannorthcutt/turboquant-mlx
cd turboquant-mlx
pip install -e .
```

**Import name**: `import turboquant_mlx` (package is `turboquant-mlx-full` on PyPI)

## Core Commands

### MLX-LM (Standard)

```bash
# Convert HF model to MLX format
python -m mlx_lm.convert --hf-path Qwen/Qwen2.5-14B-Instruct --mlx-path ./qwen2.5-14b-mlx

# Quantize to 4-bit
python -m mlx_lm.convert --hf-path Qwen/Qwen2.5-14B-Instruct --mlx-path ./qwen2.5-14b-4bit -q --q-bits 4

# Generate
python -m mlx_lm.generate --model ./qwen2.5-14b-4bit --prompt "Hello" --max-tokens 256

# Serve OpenAI-compatible
python -m mlx_lm.server --model ./qwen2.5-14b-4bit --port 8080
```

### TurboQuant-MLX (Extreme Quantization)

```bash
# Convert dense model to TurboQuant 3-bit
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3.6-27B \
  --mlx-path ./qwen3.6-27b-tq3-g32 \
  --bits 3 --group-size 32

# Convert MoE model to TurboQuant 3-bit
python -m turboquant_mlx.convert \
  --hf-path openai/gpt-oss-20b \
  --mlx-path ./gpt-oss-20b-tq3 \
  --bits 3 --group-size 32

# Convert LARGE MoE with streaming (peak RAM ~8-12GB for 235B model)
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 \
  --mlx-path /Volumes/SSD/qwen3-235b-tq3a-tqTe-g64 \
  --bits 3 --group-size 64 --ternary-experts --streaming

# Hybrid quantization: 3-bit attention, 2-bit experts
python -m turboquant_mlx.convert \
  --hf-path nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 \
  --mlx-path ./nemotron-3-super-120b-tq3a-tq2e-g32 \
  --bits 2 --attn-bits 3 --mlp-bits 2 --group-size 32
```

### TurboQuant Generation

```bash
# Standard generation
turboquant-generate \
  --model ./gpt-oss-20b-tq3 \
  --prompt "Explain quantum entanglement." \
  --max-tokens 256

# With KV cache compression (mixed K8/V3 recommended)
turboquant-generate \
  --model ./gpt-oss-120b-tq3 \
  --prompt "Why is the sky blue?" \
  --max-tokens 1024 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128

# Nemotron-3 needs --min-tokens to enter thinking phase
turboquant-generate \
  --model ./nemotron-3-super-120b-tq3 \
  --prompt "Why is the sky blue?" \
  --max-tokens 4096 --min-tokens 50
```

### Expert Streaming (Run MoE Beyond RAM)

```bash
# Stream Qwen3.6-35B-A3B on 16GB Mac (~4.5 tok/s)
python -m turboquant_mlx.stream.stream_generate \
  --model manjunathshiva/Qwen3.6-35B-A3B-tq3-g32 \
  --prompt "Write a Python function merging intervals." \
  --max-tokens 512 --cache-budget-gb 8

# Stream Qwen3-235B-A22B on 16GB Mac (~0.2-4 tok/s)
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3-235b-tq3a-tqTe-g64 \
  --prompt "Explain why the sky is blue." \
  --max-tokens 512 --cache-budget-gb 6 --prefetch-workers 8

# Tune streaming performance
# --cache-budget-gb: expert cache in GB (4-8 for 16GB, 30-40 for 64GB)
# --prefetch-workers: parallel SSD reads (8 for NVMe, 1 for USB)
# --max-active-experts: K-reduction (4 = safe, cuts disk I/O ~2x)
# --use-page-cache: trust OS page cache (auto: on if model < 0.6x RAM)
```

### TurboQuant OpenAI-Compatible Server

```bash
# Serve standard TurboQuant model
turboquant-serve \
  --model ./qwen3.6-27b-tq3-g32 \
  --port 8080

# Serve with KV cache compression
turboquant-serve \
  --model ./gpt-oss-120b-tq3 \
  --port 8080 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128

# Serve streaming MoE (single-user, sequential requests)
turboquant-serve \
  --model manjunathshiva/qwen3.5-122b-tq3 \
  --cache-budget-gb 4 \
  --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128 \
  --prompt-concurrency 1 --port 8080

# Memory tuning near ceiling
sudo sysctl iogpu.wired_limit_mb=57344  # 64GB Mac: leave 7GB for OS
turboquant-serve \
  --model ./nemotron-3-super-120b-tq3 \
  --port 8080 \
  --prompt-cache-bytes 2147483648  # 2GB hard cap
```

## Model Recommendations by RAM

| RAM | Best Resident Model | Best Streaming MoE |
|-----|---------------------|-------------------|
| 16GB | **Nemotron-3-Nano-4B** (4.3GB, **75 tok/s**) — best daily driver | Qwen3.6-35B-A3B (cache=8GB, **4.5 tok/s**) |
| 16GB | Qwen3.6-27B (17.5GB, 14 tok/s) | Qwen3-235B ternary (cache=6GB, 0.5 tok/s) |
| 32GB | GPT-OSS-20B 3-bit (12GB, 73 tok/s) | Qwen3.5-122B (cache=8GB, ~3 tok/s) |
| 48GB | Nemotron-3-Super-120B hybrid (36GB, 27 tok/s) | Qwen3.5-122B (cache=30GB, 9 tok/s) |
| 64GB | GPT-OSS-120B 3-bit (52GB, 44 tok/s) | Qwen3-235B hybrid (cache=40GB, 4-6 tok/s) |
| 96GB+ | Nemotron-3-Super-120B full 3-bit (55GB, 18 tok/s) | Qwen3-235B full 3-bit (103GB, 1.3 tok/s) |
### Session-Tested Models (M2 16GB, 2025-07-10)

- **Nemotron-3-Nano-4B (tq3, resident)**: 75 tok/s, 4.3 GB peak — best daily driver for 16GB
- **Qwen3.6-35B-A3B (tq3-g32, streaming, cache=8GB)**: 4.5 tok/s, 9-10 GB peak — strong MoE coder
- **Qwen3-235B ternary (tq3a-tqTe-g64, streaming, cache=6GB)**: 0.2-4 tok/s, 10-11 GB peak — full 235B reasoning
- **Qwen3.6-27B (tq3-g32, resident)**: 14 tok/s, 17.5 GB peak — SWE-bench grade (needs 32GB+ for comfort)

### Prisma-ML Bonsai-27B (MacOClock Article Model)

**From: [MacOClock article](https://medium.com/macoclock/bonsai-27b-runs-on-a-16-gb-m4-mac-mini-with-4-2-gb-of-ram-1-bit-quantization-with-mlx-662a30587822)**

- **Model**: `prism-ml/Ternary-Bonsai-27B-tq1` (Prisma-ML's 1.7-bit ternary rebuild of Qwen3.6-27B)
- **HF Repos**: `prism-ml/Ternary-Bonsai-27B-mlx-2bit` (2-bit), `prism-ml/Bonsai-27B-mlx-1bit` (1-bit)
- **Size**: ~8 GB at 1.58-bit ternary quantization
- **RAM Usage**: **4.2 GB** on M4 Mac Mini 16GB (article claim)
- **Speed**: ~25 tok/s on M4 Pro (greedy, warm)
- **Key Feature**: Ships with DSpark draft for speculative decoding (CUDA path, not Mac yet)
- **Lossless**: Every token verified, byte-identical to normal decoding
- **Requires**: MLX 0.32.0+ (for multi-row 2-bit matmul kernels)
- **Conversion**: `python -m turboquant_mlx.convert --hf-path prism-ml/Ternary-Bonsai-27B --mlx-path ./bonsai-27b-tq1 --bits 1 --group-size 64 --ternary-experts`

This is the **first working speculative decoding for a 27B-class model on Apple Silicon**, making 27B viable on a 16GB M4 Mac Mini.

#### Practical Findings (Session 2025-07-22, M4 Mac Mini 16GB)

| Attempt | Command | Result |
|---------|---------|--------|
| `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --mode auto` | DSpark auto-detects draft, downloads weights | **GPU timeout** (`Command buffer execution failed`) — Metal kernel for 2-bit matmul times out under load |
| `mlx-dspark serve --model prism-ml/Bonsai-27B-mlx-1bit --mode auto` | 1-bit variant | Same GPU timeout |
| `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --mode baseline` | Baseline (no draft) | **Works** — ~20-25 tok/s, ~6-8 GB peak RAM |

**Current limitation**: mlx-dspark's speculative decoding path hits a Metal GPU watchdog timeout on Apple Silicon when the 2-bit ternary matmul kernel runs. The draft model (Rahim/Ternary-Bonsai-27B-dspark) loads but the fused kernel exceeds the default GPU watchdog limit.

**Workarounds**:
1. **Use `--mode baseline`** — runs target model without draft, stable at 20-25 tok/s
2. **Raise GPU watchdog limit** (requires sudo, resets on reboot):
   ```bash
   sudo sysctl -w debug.iosched.enable=0  # Not directly applicable
   # No clean Metal watchdog toggle; fallback is baseline mode
   ```
3. **Wait for MLX 0.33+ / mlx-dspark fix** — the 2-bit ternary kernels need a longer timeout or splitting

**Recommendation for 16GB M4**: Use baseline mode for now. The 2-bit model runs well at ~20 tok/s within 8 GB RAM. Speculative decoding will be faster once the GPU timeout is resolved upstream.

## Quantization Methods Comparison

| Method | Bits | Quality | Speed | MoE Support | Apple Silicon |
|--------|------|---------|-------|-------------|---------------|
| **TurboQuant** | 1.58-4 | Best | Fast (fused kernels) | ✅ Expert streaming | ✅ Native MLX |
| MLX-LM affine | 2-8 | Good | Fast | ❌ | ✅ Native MLX |
| llama.cpp/GGUF | 2-8 | Good | Fast (Metal) | ⚠️ Partial | ✅ Metal |
| GPTQ/AWQ | 3-4 | Good | Fast (CUDA) | ⚠️ | ❌ NVIDIA only |
| MXFP4 (GPT-OSS native) | 4 | Poor | Fast | ✅ | ❌ NVIDIA only |

**TurboQuant advantages on Apple Silicon:**
- Hadamard rotation + Lloyd-Max codebooks = near-lossless at 3-bit
- Fused Metal kernels for dequant+GEMM (PolarQuantizedLinear)
- 1.58-bit ternary experts (base-3 trit packing) for massive MoE compression
- Expert streaming = run 235B on 16GB
- KV cache compression (mixed K8/V3) = 4× smaller cache, sometimes faster

## Common Configurations

### 16GB M2 MacBook Pro (User's Machine)

```bash
# Option A: Fast coding model (resident)
hf download manjunathshiva/Qwen3.6-27B-tq3-g32 --local-dir ~/models/qwen3.6-27b-tq3-g32
turboquant-generate --model ~/models/qwen3.6-27b-tq3-g32 --prompt "..." --max-tokens 1024

# Option B: Largest MoE via streaming
hf download manjunathshiva/Qwen3.6-35B-A3B-tq3-g32 --local-dir ~/models/qwen3.6-35b-tq3-g32
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3.6-35b-tq3-g32 \
  --cache-budget-gb 8 --prefetch-workers 8

# Option C: Extreme compression demo (article model)
hf download manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64 --local-dir ~/models/qwen3-235b-tq3a-tqTe-g64
python -m turboquant_mlx.stream.stream_generate \
  --model ~/models/qwen3-235b-tq3a-tqTe-g64 \
  --cache-budget-gb 6
```

### Memory Tuning (Critical on 16-48GB)

```bash
# Raise Metal wired memory limit (requires sudo, resets on reboot)
# 16GB: 12288 MB (12GB) — leaves 4GB for OS
# 32GB: 26624 MB (26GB) — leaves 6GB for OS
# 48GB: 43008 MB (42GB) — leaves 6GB for OS
# 64GB: 57344 MB (56GB) — leaves 8GB for OS
sudo sysctl iogpu.wired_limit_mb=12288

# Make permanent
echo "iogpu.wired_limit_mb=12288" | sudo tee -a /etc/sysctl.conf

# Verify
sysctl iogpu.wired_limit_mb
```

```python
# In Python: cap prompt cache to prevent OOM on multi-turn
from turboquant_mlx.layers import convert_cache_to_turboquant
from mlx_lm.models.cache import make_prompt_cache

cache = make_prompt_cache(model)
cache = convert_cache_to_turboquant(cache, k_bits=8, v_bits=3, min_tokens_before_quant=128)
```

## Quality Evaluation

```bash
# Perplexity benchmark (TurboQuant vs affine vs QJL)
python -m turboquant_mlx.evaluate \
  --hf-path openai/gpt-oss-20b \
  --bits 3 \
  --no-affine --no-qjl \
  --num-samples 64 --seq-len 512

# KV cache roundtrip test
python -m turboquant_mlx.test_kv_cache \
  --model ./gpt-oss-20b-tq3 \
  --k-bits 8 --v-bits 3 --min-tokens 128
```

## Key Files & Structure

```
turboquant_mlx/
├── convert.py              # HF → TurboQuant MLX (with --streaming for huge models)
├── generate.py             # turboquant-generate CLI
├── evaluate.py             # Perplexity evaluation
├── demo_kv.py              # KV cache compression demo
├── test_kv_cache.py        # KV cache roundtrip tests
├── quantize_model.py       # Model traversal & layer replacement
├── config.py               # TurboQuantConfig
├── core/
│   ├── codebook.py         # Lloyd-Max codebooks (Gaussian optimal)
│   ├── rotation.py         # Randomized Hadamard rotation
│   ├── polar_quantize.py   # Rotate + codebook quantize
│   ├── packing.py          # Bit-packing (including base-3 trit packing)
│   └── qjl.py              # 1-bit QJL residual correction
├── layers/
│   ├── polar_linear.py           # PolarQuantizedLinear (dense)
│   ├── polar_switch_linear.py    # PolarQuantizedSwitchLinear (MoE)
│   └── polar_kv_cache.py         # TurboQuantKVCache (runtime KV compression)
├── kernels/
│   ├── polar_qmv.py              # Fused dense decode kernel
│   ├── polar_gather_qmv.py       # Fused MoE shared-input kernel
│   └── polar_multi_gather_qmv.py # Fused MoE per-expert kernel
├── integration/
│   └── rotation_configs.py       # Per-architecture rotation configs
└── stream/                       # Expert streaming (v0.4+)
    ├── safetensors_reader.py     # Per-expert os.pread + F_NOCACHE
    ├── streaming_switch.py       # StreamingSwitchLinear + LRU ExpertCache
    ├── loader.py                 # load_streaming(): swap experts post-load
    ├── stream_generate.py        # stream_generate CLI
    ├── calibrate_experts.py      # Routing trace → pin.json + perm.json
    └── repack_experts.py         # Optional on-disk co-activation relayout
```

## Pre-Converted Models (Hugging Face Hub)

| Model | HF Repo | Size | Notes |
|-------|---------|------|-------|
| Qwen3.6-27B (dense coder) | `manjunathshiva/Qwen3.6-27B-tq3-g32` | 13 GB | SWE-bench grade, 14 tok/s |
| Qwen3.6-35B-A3B | `manjunathshiva/Qwen3.6-35B-A3B-tq3-g32` | 16 GB | Streams on 16GB at 4.5 tok/s |
| Qwen3.5-122B-A10B | `manjunathshiva/qwen3.5-122b-tq3` | 50 GB | 256 experts, reasoning |
| Qwen3-235B-A22B (hybrid ternary) | `manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3a-tqTe-g64` | 53 GB | Article model, 5.6 tok/s resident |
| Qwen3-235B-A22B (full 3-bit) | `manjunathshiva/Qwen3-235B-A22B-Instruct-2507-tq3-g32` | 103 GB | 6/6 stress pass, 1.3 tok/s |
| GPT-OSS-20B | `manjunathshiva/gpt-oss-20b-tq3` | 9.3 GB | 73 tok/s, beats MXFP4 |
| GPT-OSS-120B | `manjunathshiva/gpt-oss-120b-tq3` | 48 GB | Only way on 64GB, 44 tok/s |
| Nemotron-3-Nano-4B | `manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3` | 2.2 GB | 75 tok/s, Mamba+attention |
| Nemotron-3-Super-120B | `manjunathshiva/Nemotron-3-Super-120B-A12B-tq3a-tq2e-g32` | 36 GB | Hybrid 3/2-bit, 27 tok/s |

## Ollama GGUF vs MLX selection

- Same base weights, different runtime: bare tag (`model:12b`) is GGUF/llama.cpp, `-mlx` tag is an Apple MLX build — verify with `ollama list` then `ollama show <tag>` (architecture, quantization, context length) before comparing, because pulling one tag does not pull the other.
- Default to `-mlx` on Apple-only machines when RAM headroom exists — unified-memory Metal kernels give better prefill and long-context throughput.
- Default to GGUF when under RAM pressure — mmap plus tunable `num_ctx` / partial GPU offload / single loaded model with short keep-alive shrinks the footprint, while MLX loads full weights resident with wired Metal buffers and has no partial-offload dial.
- Check pressure first with `vm_stat` (free pages) and `ollama ps`; close Chrome/Electron apps before running 10B+ locally, and drop to a 4B-class model when free memory stays near zero.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `KeyError: 'turboquant'` in mlx_lm.server | Use `turboquant-serve` instead — patches loader |
| `Metal out of memory` / watchdog panic | Raise `iogpu.wired_limit_mb`, close Chrome/Electron apps |
| `OSError: [Errno 12] Cannot allocate memory` | Reduce `--cache-budget-gb`, add `--prompt-cache-bytes` |
| Streaming too slow (0.1 tok/s) | Use faster SSD (Thunderbolt/NVMe), increase `--cache-budget-gb`, `--prefetch-workers 8` |
| Ternary experts fail (incoherent) | Need ≥64 experts for redundancy — 32-expert models collapse at 1.58-bit |
| Nemotron-3 math accuracy degrades | Omit `--rep-penalty` for math (Phase 1 limitation) |
| Conversion OOM on 64GB | Add `--streaming` flag — peak RAM drops to ~one shard |

## References

- **[turboquant-quickstart.md](references/turboquant-quickstart.md)** — Commands used in this session for 16GB M2
- **[model-catalog.md](references/model-catalog.md)** — Full pre-converted model table with Hub URLs
- **[streaming-tuning.md](references/streaming-tuning.md)** — Expert cache, prefetch, K-reduction deep dive
- **[kv-compression.md](references/kv-compression.md)** — Mixed K8/V3, sink protection, speed flip analysis
- **[memory-tuning.md](references/memory-tuning.md)** — `iogpu.wired_limit_mb`, prompt cache caps, watchdog avoidance
- **[small-models-4b.md](references/small-models-4b.md)** — 4B-class models (Qwen3.5-4B, Nemotron-3-Nano-4B, Bonsai-4B) with benchmarks
- **[quickstart-qwen3.5-4b.md](references/quickstart-qwen3.5-4b.md)** — 30-second setup for Qwen3.5-4B on Apple Silicon
- **[bonsai-27b-gpu-timeout.md](references/bonsai-27b-gpu-timeout.md)** — DSpark GPU watchdog timeout on M4, workarounds
- **[turboquant-streaming-moe.md](references/turboquant-streaming-moe.md)** — Expert streaming deep dive
## Resources

- **TurboQuant-MLX GitHub**: https://github.com/nathannorthcutt/turboquant-mlx
- **TurboQuant Paper** (Zandieh et al., 2025): Hadamard + Lloyd-Max for Gaussian-optimal quantization
- **MLX Framework**: https://github.com/ml-explore/mlx
- **MLX-LM**: https://github.com/ml-explore/mlx-lm
- **Hugging Face Local Apps (llama.cpp view)**: https://huggingface.co/docs/hub/main/local-apps