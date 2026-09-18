# Bonsai-27B GPU Timeout on Apple Silicon (Session 2025-07-22 / Updated 2026-07-22)

## Problem
Running `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --mode auto` on M4 Mac Mini 16GB triggers a Metal GPU timeout:

```
RuntimeError: [METAL] Command buffer execution failed: Caused GPU Timeout Error (00000002:***).
```

This occurs when the 2-bit ternary matmul kernel (used by the DSpark draft) runs long enough to hit the GPU watchdog.

## Test Environment
- **Hardware**: M4 Mac Mini 16GB (70GB free on Samsung SSD)
- **MLX**: 0.32.0 (multi-row 2-bit matmul kernels)
- **mlx-dspark**: 0.5.0
- **Model**: `prism-ml/Ternary-Bonsai-27B-mlx-2bit` + draft `Rahim/Ternary-Bonsai-27B-dspark`

## What We Tried

| Attempt | Command | Result |
|---------|---------|--------|
| 1 | `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --kv-bits 8 --port 8080 --mode auto` | Error: `--kv-bits unsupported for hybrid linear-attention targets` |
| 2 | `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --port 8080 --mode auto` | GPU timeout during draft load |
| 3 | `mlx-dspark serve --model prism-ml/Bonsai-27B-mlx-1bit --max-batch 1 --port 8080 --mode auto` | Error: 1-bit not supported by MLX |
| 4 | `mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --no-thinking --port 8081 --mode baseline` | **Works** — ~20-25 tok/s, ~6-8 GB RAM |

## Root Cause
The DSpark draft model uses 2-bit ternary quantization with fused Metal kernels (`polar_qmv.py`). These kernels execute long enough to exceed the default GPU watchdog timeout (~2s on macOS). The watchdog kills the command buffer, returning `0x2` (IOGPUCommandBufferCallbackErrorTimeout).

## Current Workaround
Use **baseline mode** (no draft):
```bash
mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit \
  --max-batch 1 --no-thinking --host 0.0.0.0 --port 8081 --mode baseline
```

This runs the target model without speculative decoding at ~20-25 tok/s within 8 GB RAM on 16GB M4.

## Upstream Fix Needed
Either:
1. **MLX kernel split** — break 2-bit ternary matmul into smaller dispatches under watchdog limit
2. **Watchdog extension** — add `MTLCommandBuffer` timeout override (requires MLX Metal device config)
3. **mlx-dspark flag** — `--no-gpu-timeout` or similar to use slower but safe kernel path

Track: https://github.com/ml-explore/mlx/issues (search "watchdog" / "timeout")

## Session Log Excerpt (2025-07-22)
```
proc_61a3f5596caa: "mlx-dspark server · mode=dspark · model=Ternary-Bonsai-27B-mlx-2bit
  target : prism-ml/Ternary-Bonsai-27B-mlx-2bit
  drafter: Rahim/Ternary-Bonsai-27B-dspark
  ...
  listening on http://0.0.0.0:8080
curl /v1/chat/completions → GPU timeout error
proc_7a1fcfbf7297: Same GPU timeout on startup
proc_5255f35a7a86: 1-bit model rejected by MLX loader
```

---

## Update: Session 2026-07-22 (User: Alfred, M4 Mini 16GB)

### Additional Context
- Bonsai-27B is a **Prisma-ML ternary rebuild of Qwen3.6-27B** (~8 GB at 1.58-bit)
- Article claim: "Runs on 16GB M4 Mini with 4.2 GB RAM" — refers to **baseline mode only**
- The DSpark draft model (`Rahim/Ternary-Bonsai-27B-dspark`) is CUDA-optimized, not Apple Silicon
- On Mac, DSpark speculative decoding **does not work** due to the Metal watchdog

### Confirmed Working Config (2026-07-22)
```bash
# TurboQuant-MLX path (alternative to mlx-dspark)
hf download prism-ml/Ternary-Bonsai-27B-tq1 --local-dir ~/models/bonsai-27b-tq1
turboquant-serve --model ~/models/bonsai-27b-tq1 --port 8080
# ~25 tok/s on M4 Pro, ~20-25 on M4 Mini, 4.2 GB RAM
```

### Comparison
| Engine | Mode | Speed (M4 Mini) | RAM | Speculative Decoding |
|--------|------|-----------------|-----|---------------------|
| mlx-dspark | auto (draft) | **FAIL** (GPU timeout) | N/A | ✅ Intended |
| mlx-dspark | baseline | ~20-25 tok/s | 6-8 GB | ❌ Disabled |
| TurboQuant-MLX | N/A | ~20-25 tok/s | 4.2 GB | ❌ Not implemented yet |

### Recommendation for 16GB M4
**Use TurboQuant-MLX** (`turboquant-serve`) for Bonsai-27B. It runs the ternary model natively without the DSpark draft path, avoiding the Metal watchdog entirely. Performance matches mlx-dspark baseline with half the RAM.