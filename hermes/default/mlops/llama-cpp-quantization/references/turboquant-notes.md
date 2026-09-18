# TurboQuant Notes — Alex Ziskind Video Transcript Summary

**Source**: YouTube "After This, 16GB Feels Different" (XLlQDfhyBjc) by Alex Ziskind
**Date**: 3 months ago (as of transcript extraction)

## Key Findings

### TurboQuant Overview
- **TurboQuant** = Google research paper technique for KV cache compression
- Works on **KV cache** (not model weights) — quantization solves model weights, TurboQuant solves KV cache
- Community fork: **The Tom / llama-cpp-turboquant** (branch: `feature/turboquant-kv-cache`)
- Not yet in mainline llama.cpp; V Llama also working on it

### Quantization Levels
| Level | Compression | Notes |
|-------|-------------|-------|
| Turbo 2 | ~4× | Most aggressive, quality drops at >4K context |
| Turbo 3 | ~2.5× | **Sweet spot** — 131K context on 16GB M4 Mini with 3.6GB spare |
| Turbo 4 | ~1.9× | Conservative, minimal quality loss |

### Asymmetric Quantization (Critical Finding)
- **Symmetric** (same level for K & V) = quality loss at >4K context
- **Asymmetric**: Q8 for K, Turbo 1/3 for V = preserves needle-in-haystack at 32K+
- K cache more sensitive to quantization — must keep at Q8
- Tom Turney (fork author) suggested this approach

### Hardware Results

#### M4 Mac Mini (16GB) — Compute Bound
- Matrix multiplication is bottleneck, not KV cache bandwidth
- TurboQuant: memory savings ✓, speed ~flat (1-4% slower at short context)
- No significant speed improvement because compute is the limit

#### M5 Max / M5 MacBook Pro (128GB) — Memory Bound
- **Huge speed win**: decode speed stays flat at 54 tok/s (0→32K context)
- Q8 baseline drops from 54→37 tok/s as context grows (0→8K)
- At 32K context, Q8 recovers to 44 tok/s but TurboQuant stays flat at 54
- KV cache bandwidth was the bottleneck; TurboQuant removes it

#### M5 Mac Mini (Future)
- Predicted: significant boost even with 16GB because M5 likely memory-bound
- Will benefit more from TurboQuant than M4 Mini

### Model Performance
- **Qwen 3.5 series** (MoE and dense): "behave really well and respond really nicely to TurboQuant on Apple hardware"
- Qwen 2.5, Qwen 3 8B: tested, similar results
- MoE models (Qwen 3.5 35B): benefit most — KV cache dominates memory
- Some models perform poorly; model-dependent

### Needle-in-Haystack Test Results
- **Symmetric Turbo**: 100% at 1K, drops to 0% at 8K/16K
- **Asymmetric (Q8_K + Turbo_V)**: 100% across all context lengths (1K→32K)

### Practical Commands Tested
```bash
# Q8 baseline with 131K context — CRASHES on M4 Mini
./llama-cli -m qwen3.5-35b-Q8.gguf -c 131072

# Turbo 3 asymmetric — WORKS with 3.6GB spare
./llama-cli -m qwen3.5-35b-Q8.gguf \
  --cache-type-k q8_0 \
  --cache-type-v turbo3 \
  -c 131072
```

### Build Notes
- Initial symmetric tests were "pretty bad" — prefill and decode speed suffered
- Asymmetric approach recovered speed AND quality
- Tested multiple context lengths: 32K, 65K, 131K — huge memory savings at each level
- M4 Mini: compute bound (matrix mul bottleneck)
- M5 Max: memory bound (KV cache bandwidth bottleneck)

### Integration Status
- Community effort only currently
- Wait for merge into llama.cpp → LM Studio, V Llama, other tools get it automatically
- Try fork now or wait for upstream integration

---

## Our Session Results (M4 Mac Mini 16GB)

### Build
```bash
git clone -b feature/turboquant-kv-cache https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

### Benchmarks: Qwen3-4B Q8_0

| Config | Prompt (512) | Decode (256) | Prompt @ 8K ctx | Decode @ 8K ctx |
|--------|-------------|-------------|-----------------|-----------------|
| Q8_0 / Q8_0 (baseline) | 415 t/s | 21.9 t/s | 151 t/s | 15.5 t/s |
| **Q8_0 / Turbo3 (asymmetric)** | **410 t/s** | **20.2 t/s** | **147 t/s** | **14.5 t/s** |

### Memory Savings
- Turbo3 V cache = ~2.5× compression vs Q8_0
- Enables 2–4× longer context on same RAM
- 64K+ context works; 128K+ likely works on 16GB

### Key Confirmations
- ✅ M4 Mini is compute-bound — no speed win, only memory
- ✅ Asymmetric Q8_0 K + Turbo3 V preserves quality
- ✅ Context scaling works — tested up to 64K context
- ✅ Model loading works with `--cache-type-k q8_0 --cache-type-v turbo3`

### Ready-to-Use Commands
```bash
# Asymmetric Turbo3 (best quality + memory savings)
./build/bin/llama-cli \
  -m ./models/qwen3-4b-q8.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 32768 -p "your prompt"

# Maximum context (64K+)
./build/bin/llama-cli \
  -m ./models/qwen3-4b-q8.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 65536 -p "your prompt"
```

### Environment Variables
```bash
export TURBO_LAYER_ADAPTIVE=7    # Boundary layers in Q8_0, middle in Turbo
export TURBO_AUTO_ASYMMETRIC=1   # Auto asymmetric for large-GQA models
export TURBO_SPARSE_V=1          # Sparse V dequant skip (enabled by default)
```