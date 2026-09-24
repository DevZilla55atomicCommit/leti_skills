---
name: apple-silicon-llm-inference
description: Comprehensive guide for running LLMs on Apple Silicon (M1/M2/M3/M4) using MLX, Ollama, llama.cpp, and TurboQuant. Covers quantization, expert streaming for MoE models, provider configuration, and TTS integration.
category: mlops-inference
tags: [apple-silicon, mlx, ollama, llama.cpp, turboquant, quantization, moe-streaming, nvidia-nim, tts, elevenlabs, edge-tts]
---

# Apple Silicon LLM Inference

Unified skill for deploying and running LLMs on Apple Silicon Macs (M1/M2/M3/M4) across multiple inference engines, with focus on memory-constrained environments (16–48 GB unified memory).

## Inference Engines Comparison

| Engine | Format | Quantization | MoE Streaming | Best For |
|--------|--------|--------------|---------------|----------|
| **MLX (mlx-lm)** | `.safetensors` | TurboQuant (1.58–4 bit), k-bit | ✅ Expert streaming (TurboQuant-MLX) | Native Apple Silicon, research models, TurboQuant compression |
| **Ollama** | GGUF | k-quants (q4_k_m, q5_k_m, q8_0) | ❌ | Daily drivers, easy model switching, OpenAI API compat |
| **llama.cpp** | GGUF | k-quants, IQ quants | ❌ | Maximum control, custom builds, server mode |
| **TurboQuant-MLX** | `.safetensors` | **1.58-bit ternary**, 2–4 bit | ✅ Expert streaming | **Extreme compression** (235B→53GB), MoE on 16GB |

## Engine Selection Guide

```
Need easiest UX + model zoo?           → Ollama (`ollama pull qwen2.5:14b`)
Need Apple-native + TurboQuant?        → MLX (`mlx_lm.convert`, `turboquant-generate`)
Need extreme compression on 16GB?      → TurboQuant-MLX streaming (`--cache-budget-gb 4`)
Need maximum control/custom kernels?   → llama.cpp (`./llama-server -m model.gguf`)
Need NVIDIA NIM API (cloud)?           → Hermes native provider (not LiteLLM)
```

## TurboQuant-MLX (Critical for 16GB MoE)

**Installation:**
```bash
pip install turboquant-mlx-full
# or from source
git clone https://github.com/nathannorthcutt/turboquant-mlx
cd turboquant-mlx && pip install -e .
```

## TurboQuant in llama.cpp (TheTom Fork)

**Community fork implementing TurboQuant KV cache quantization for llama.cpp:**

```bash
# Clone the TurboQuant branch
git clone -b feature/turboquant-kv-cache https://github.com/TheTom/llama-cpp-turboquant.git
cd llama-cpp-turboquant

# Build with Metal (Apple Silicon)
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

**New KV Cache Types (runtime only, never stored in model files):**
| Type | Enum | Bits/value | Compression vs FP16 |
|------|------|------------|---------------------|
| `turbo2` | `GGML_TYPE_TURBO2_0` (43) | 2 | 6.4× |
| `turbo3` | `GGML_TYPE_TURBO3_0` (44) | 3.25 | 4.9× |
| `turbo4` | `GGML_TYPE_TURBO4_0` (47) | 4.25 | 3.8× |

**Usage (asymmetric K/V recommended):**
```bash
# Asymmetric: Q8_0 for K, Turbo3 for V (best quality/savings balance)
./build/bin/llama-cli -m model.gguf \
  --cache-type-k q8_0 --cache-type-v turbo3 \
  -c 32768 -p "your prompt"

# Available cache types: f16, q8_0, q4_0, turbo2, turbo3, turbo4
```

**Key Findings (M4 Mac Mini 16GB):**

| Model | Config | Short ctx decode | 8K ctx decode | Memory savings |
|-------|--------|------------------|---------------|----------------|
| Qwen3-4B Q8_0 | Q8_0/Q8_0 | 21.9 t/s | 15.5 t/s | baseline |
| Qwen3-4B Q8_0 | **Q8_0/Turbo3** | **20.2 t/s (-8%)** | **14.5 t/s (-7%)** | **~2.5× V cache** |
| Gemma4-12B Q4_K | Q8_0/Q8_0 | 12.5 t/s | 11.1 t/s | baseline |
| Gemma4-12B Q4_K | Q8_0/Turbo3 | 11.8 t/s (-5%) | 8.9 t/s (-20%) | ~2.5× V cache |

**Environment Knobs:**
```bash
export TURBO_LAYER_ADAPTIVE=7    # Boundary layers in Q8_0, middle in Turbo
export TURBO_AUTO_ASYMMETRIC=1   # Auto asymmetric for large-GQA models
export TURBO_SPARSE_V=1          # Sparse V dequant skip (enabled by default)
```

**Quality Notes:**
- **Turbo3 = sweet spot** — passes needle-in-haystack at 131K context (asymmetric)
- Turbo2: quality collapses at >4K context
- Turbo4: diminishing returns, less compression
- Asymmetric (Q8_0 K + Turbo3 V) strongly recommended over symmetric

**Status:** Community fork, not yet merged to mainline llama.cpp. V Llama also working on it. Once merged, LM Studio and other tools will inherit it.

## mlx-dspark (Speculative Decoding for Apple Silicon)

**Installation:**
```bash
pip install mlx-dspark  # Requires MLX >= 0.32.0
```

**Key Capability:** Lossless speculative decoding — runs DSpark/DFlash drafters natively on Metal, produces byte-identical output to baseline.

**Supported Models (auto-resolves drafter):**
| Target | Drafter | Quant | Speedup (M4 Pro) |
|--------|---------|-------|------------------|
| Ornith-1.0-9B | DeepSeek DSpark | 8-bit | **2.47x** |
| Gemma-4-12B | DeepSeek DSpark | 8-bit | 2.13x code / 1.76x chat |
| Qwen3-14B | DeepSeek DSpark | 8-bit | 1.92x |
| Qwen3-8B | DeepSeek DSpark | 8-bit | 1.92x |
| Qwen3-4B | DeepSeek DSpark | 8-bit | 1.64x |
| Qwen3.6-27B (4-bit) | Community DSpark | 4-bit | 1.73x math / 1.42x code |
| **Ternary-Bonsai-27B (2-bit)** | Community DSpark | **2-bit** | ~1.15x (acceptance ~2.9) |

**⚠️ Known Limitations (2026-07):**
- Bonsai-27B drafter: "not Macs yet" (CUDA path only) — community drafter works but acceptance lower (~2.1 vs ~2.9 at cap 2)
- Gemma-4: does not converge on Pi's tool protocol
- Prefix caching + batching: dense-target only
- GPU timeout on M4 with DSpark mode — use `--mode baseline` for stability

**CLI (OpenAI-compatible server):**
```bash
# Baseline (stable, no drafter)
mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --no-thinking --mode baseline --port 8081

# DSpark (speculative, may GPU timeout on M4)
mlx-dspark serve --model prism-ml/Ternary-Bonsai-27B-mlx-2bit --max-batch 1 --no-thinking --mode auto --port 8080

# Any HF repo with auto-draft resolution
mlx-dspark serve --model mlx-community/Qwen3-8B-8bit --mode auto --port 8080
```

**Python API:**
```python
from mlx_dspark import load_pair, speculative_generate

target, tok, draft, cfg = load_pair("mlx-community/Qwen3-8B-8bit")
res = speculative_generate(target, tok, draft, "Explain rainbows.")
print(res.text, res.mean_accept_len, res.tokens_per_sec)
```

**Hermes Integration (custom provider):**
```yaml
# ~/.hermes/config.yaml
providers:
  bonsai-baseline:
    base_url: "http://127.0.0.1:8081/v1"
    api_key: "not-needed"
    models: ["Ternary-Bonsai-27B-mlx-2bit"]
    format: "openai"
  bonsai-dspark:
    base_url: "http://127.0.0.1:8080/v1"
    api_key: "not-needed"
    models: ["Ternary-Bonsai-27B-mlx-2bit"]
    format: "openai"
```

**Convert + Stream 235B MoE on 16GB:**
```bash
# Convert (streaming = peak RAM ~8-12GB)
python -m turboquant_mlx.convert \
  --hf-path Qwen/Qwen3-235B-A22B-Instruct-2507 \
  --mlx-path ./qwen3-235b-tq3a-tqTe-g64 \
  --bits 3 --group-size 64 --ternary-experts --streaming

# Run (expert streaming, cache-budget = expert cache in GB)
python -m turboquant_mlx.stream.stream_generate \
  --model ./qwen3-235b-tq3a-tqTe-g64 \
  --prompt "Explain quantum entanglement" \
  --max-tokens 512 --cache-budget-gb 4
```

**Key Parameters:**
| Param | 16GB M2 | 48GB M2 Max | 64GB M4 Max |
|-------|---------|-------------|-------------|
| `--cache-budget-gb` | 4–6 | 30–38 | 40–50 |
| `--prefetch-workers` | 8 | 8 | 8 |
| `--max-active-experts` | 4 | 4 | 8 (native) |
| Expected speed | 0.2–4 tok/s | 5–15 tok/s | 4–6 tok/s (warm) |

**Quality Tiers (Qwen3-235B):**
- **Hybrid tq3a-tqTe** (3-bit attn + ternary experts): 53 GB, 5/6 quality probes pass
- **Full 3-bit** (tq3): 103 GB, 6/6 probes pass (exact recall)

## MLX Native (mlx-lm)

```bash
# Convert HF → MLX
python -m mlx_lm.convert --hf-path Qwen/Qwen2.5-14B --mlx-path ./qwen2.5-14b-4bit -q 4bit

# Generate
python -m mlx_lm.generate --model ./qwen2.5-14b-4bit --prompt "Hello" --max-tokens 256

# Serve (OpenAI-compatible)
python -m mlx_lm.server --model ./qwen2.5-14b-4bit --port 8080
```

**Metal Wired Limit (raise for >48GB models):**
```bash
sudo sysctl iogpu.wired_limit_mb=57344  # 64GB machine → 56GB GPU
echo "iogpu.wired_limit_mb=57344" | sudo tee -a /etc/sysctl.conf
```

## Ollama (Daily Driver)

```bash
# Pull models
ollama pull qwen2.5:14b          # 9 GB (q4_k_m)
ollama pull nemotron3:nano-4b    # 2.8 GB
ollama pull deepseek-coder:33b   # 19 GB

# Serve (OpenAI-compatible on 11434)
ollama serve

# Use with Hermes
# Provider: ollama-launch, api: http://localhost:11434/v1
```

**Quantized KV Cache in Ollama:** Ollama's Modelfile does NOT yet expose `cache_type_k` / `cache_type_v` parameters (Ollama wraps llama.cpp but the Modelfile schema is limited). To use quantized KV (q4_0 saves ~2 GB at 98k ctx):
- **Option A**: Use llama.cpp directly with `--cache-type-k q4_0 --cache-type-v q4_0` (best RAM savings)
- **Option B**: Keep Ollama for ease; accept f16 KV overhead (~2 GB more at 98k ctx)
- **Workaround**: Some Ollama builds accept `OLLAMA_KV_CACHE_TYPE=q8_0` env var (set via launchctl); verify with `launchctl getenv OLLAMA_KV_CACHE_TYPE`.

**MTP (Multi-Token Prediction) in Ollama:** Not plug-and-play. MTP models (e.g., `unsloth/Qwen3.5-9B-MTP-GGUF`) require:
1. Manual GGUF download from HuggingFace (6+ GB)
2. Modelfile pointing to local file path
3. Ollama built with MTP support (recent versions; check `ollama run --help` for `--spec-type`)
4. For now, use llama.cpp directly: `--spec-type draft-mtp --spec-draft-n-max 2`

**Qwen3.5-96k Streaming Bug:** The `qwen3.5-96k:latest` variant in Ollama returns empty NDJSON on streaming (`/v1/chat/completions` with `stream: true`). **Workaround**: force non-streaming via gateway proxy (litellm):
```yaml
model_list:
  - model_name: qwen3.5-96k
    litellm_params:
      model: ollama/qwen3.5-96k:latest
      api_base: http://localhost:11434
      stream: false
```
Non-streaming endpoint returns valid JSON; trade "typing" effect for stability on 16 GB.

**Model Size Cheatsheet (q4_k_m):**
| Params | Disk | RAM (active) |
|--------|------|--------------|
| 7B     | 4.5 GB | ~6 GB |
| 14B    | 9 GB   | ~11 GB |
| 32B    | 19 GB  | ~22 GB |
| 72B    | 41 GB  | ~48 GB |

## NVIDIA NIM API (Hermes Native Provider)

**Correct Config (Hermes native, NOT LiteLLM):**
```yaml
# ~/.hermes/config.yaml
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  provider: nvidia
  base_url: https://integrate.api.nvidia.com/v1

providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: nvapi-xxxxxxxxxxxxxxxxxxxxxxxx  # Bearer token format
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    name: NVIDIA
    concurrency_limit: 1      # Critical: prevents burst 429s
    rate_limit_rpm: 35        # Safety buffer (<40 actual)
    max_retries: 5
    retry_delay: 10
    retry_on: [429, 500, 502, 503, 504]
```

**❌ Don't use LiteLLM for NVIDIA** — causes dual-path conflicts, model switching, rate limit confusion.

**Verify API Key:**
```bash
curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models | grep nemotron
```

## TTS Integration

### ElevenLabs (Premium)
```yaml
# ~/.hermes/config.yaml
tts:
  provider: elevenlabs
  use_gateway: true
  elevenlabs:
    voice_id: pNInz6obpgDQGcFmaJgB   # Your chosen voice
    model_id: eleven_multilingual_v2

# ~/.hermes/.env
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx
```

### Edge TTS (Free, Local Voices)
```yaml
tts:
  provider: edge
  edge:
    voice: en-ZA-LeahNeural   # South African female
    # voice: en-AU-NatashaNeural  # Australian female
    # voice: en-GB-SoniaNeural    # British female (professional)
```

**Available Regional Voices:**
| Locale | Female | Male |
|--------|--------|------|
| en-ZA (South Africa) | LeahNeural | LukeNeural |
| en-AU (Australia) | NatashaNeural | WilliamNeural, AdamNeural |
| en-GB (UK) | SoniaNeural, LibbyNeural, MaisieNeural | RyanNeural, ThomasNeural |

## Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| "METAL: Out of memory" / watchdog panic | `iogpu.wired_limit_mb` too low | `sudo sysctl iogpu.wired_limit_mb=57344` |
| TurboQuant 235B: 0.01 tok/s | `--cache-budget-gb` too small | Increase to 6 (16GB) or 40 (64GB) |
| NVIDIA 429 errors | `concurrency_limit` missing | Set `concurrency_limit: 1` in provider |
| Model switches mid-session | LiteLLM + native both configured | Remove LiteLLM NVIDIA configs |
| ElevenLabs "401 Unauthorized" | `ELEVENLABS_API_KEY` not in `.env` | Add to `~/.hermes/.env` |
| Ollama model not found | Wrong model tag | `ollama list` → use exact name from list |

## Quick Reference: Model → Engine → RAM

| Model | Best Engine | Quant | Disk | RAM (16GB) | RAM (48GB) |
|-------|-------------|-------|------|------------|------------|
| Nemotron-3-Nano-4B | MLX/Ollama | 3-bit/4-bit | 2.2 GB | ✅ 4 GB | ✅ 4 GB |
| Qwen2.5-14B | Ollama/MLX | 4-bit | 9 GB | ✅ 11 GB | ✅ 11 GB |
| Nemotron-3-Ultra-550B | NVIDIA NIM (API) | — | — | ✅ (cloud) | ✅ (cloud) |
| Qwen3-235B-A22B | TurboQuant-MLX | tq3a-tqTe | 53 GB | ✅ Streaming | ✅ Resident |
| Qwen3.6-35B-A3B | TurboQuant-MLX | 3-bit gs32 | 16 GB | ✅ Streaming | ✅ Resident |
| DeepSeek-V3 (671B) | — | — | — | ❌ | ❌ (needs 96GB+) |

## References

- `references/turboquant-streaming.md` — TurboQuant-MLX expert streaming deep dive
- `references/turboquant-llama-cpp.md` — TurboQuant in llama.cpp (TheTom fork): build, usage, benchmarks on M4
- `references/mlx-metal-limits.md` — Metal wired limit tuning
- `references/nvidia-nim-config.md` — NVIDIA NIM provider config patterns
- `references/edge-tts-voices.md` — Complete Edge TTS voice catalog by locale
- `references/mlx-dspark.md` — mlx-dspark native MLX speculative decoding (DSpark/DFlash)

## See Also

- `serving-llms-vllm` — vLLM for Linux/NVIDIA (not Apple Silicon)
- `llama-cpp` — llama.cpp GGUF inference
- `custom-ai-providers` — Generic provider configuration patterns