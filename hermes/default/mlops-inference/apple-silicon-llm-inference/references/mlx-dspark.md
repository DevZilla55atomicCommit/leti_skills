# mlx-dspark Reference

## Overview
`mlx-dspark` is a native MLX port of DeepSeek's DSpark and z-lab's DFlash speculative decoding. Runs entirely on Apple Metal — no CUDA, no server framework, pure Python + MLX.

## Key Characteristics
- **Lossless**: Every drafter token verified → output identical to baseline
- **OpenAI-compatible server** built on stdlib (uvicorn/fastapi optional)
- **Auto-draft resolution**: pass any HF repo ID; matching DSpark/DFlash checkpoint auto-selected
- **Three modes**: `baseline` (target only), `dspark` (semi-autoregressive), `dflash` (block diffusion), `lookup` (n-gram), `auto` (best available)
- **Metal-only**: requires MLX 0.32.0+ (multi-row 2-bit matmul kernels)

## Supported Models (July 2026)

| Target | Drafter Source | Quant | Notes |
|--------|----------------|-------|-------|
| Ornith-1.0-9B | DeepSeek (official) | 8-bit | Best speedup: 2.47x |
| Gemma-4-12B | DeepSeek (official) | 8-bit | 2.13x code, but tool protocol issues |
| Qwen3-14B | DeepSeek (official) | 8-bit | 1.92x |
| Qwen3-8B | DeepSeek (official) | 8-bit | 1.92x |
| Qwen3-4B | DeepSeek (official) | 8-bit | 1.64x |
| Qwen3.6-27B | Community (Aveseed) | 4-bit | 1.73x math |
| Ternary-Bonsai-27B | Community (Rahim) | **2-bit** | ~1.15x, acceptance 2.9 |

## CLI Reference
```bash
mlx-dspark serve [options]

Options:
  --model MODEL           HF repo ID or local path (required)
  --drafter DRAFTER       Override drafter repo (optional, auto-resolved)
  --mode {auto,dspark,dflash,lookup,baseline}  Default: auto
  --max-draft N           Max draft tokens per step (default: 8)
  --max-batch N           Continuous batching slots (default: 4)
  --kv-bits {0,4,8}       KV quantization (default: 8)
  --drafter-bits N        Drafter quantization (default: 0=auto)
  --no-thinking           Strip
```

## Tested: Ternary-Bonsai-27B (M4 Mac Mini, 16GB)

| Mode | Command | Result |
|------|---------|--------|
| **Baseline** (stable) | `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --no-thinking --host 0.0.0.0 --port 8081 --mode baseline` | ✅ Works — ~0.5 tok/s, identical output |
| **DSpark** (speculative) | `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --no-thinking --host 0.0.0.0 --port 8080 --mode auto` | ❌ GPU timeout (Metal command buffer execution failed) |

**Working server (baseline):**
```bash
mlx-dspark serve \
  --model prism-ml/Ternary-Bonsai-27B-mlx-2bit \
  --max-batch 1 \
  --no-thinking \
  --host 0.0.0.0 \
  --port 8081 \
  --mode baseline
```

**OpenAI-compatible endpoint:**
- `GET  http://localhost:8081/v1/models`
- `POST http://localhost:8081/v1/chat/completions` (stream: true/false)