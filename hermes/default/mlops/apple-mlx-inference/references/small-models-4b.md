# 4B-Class Models on Apple Silicon (M4/M3/M2)

**Session**: 2026-07-22 | User: Alfred (M4 Mini 16GB) | Goal: Fast, memory-efficient, low-hallucination 4B model

## Qwen3.5-4B (GGUF via llama.cpp)

**Repo**: `unsloth/Qwen3.5-4B-GGUF` (multimodal: image-text-to-text)

| Quant | Size | RAM (est.) | Speed (M4) | Quality | Best For |
|-------|------|------------|------------|---------|----------|
| Q3_K_M | 2.2 GB | ~3 GB | 60-80 tok/s | Good | Tight RAM |
| **Q4_K_M** | **2.7 GB** | **~3.5 GB** | **50-70 tok/s** | **Best balance** | **Daily driver** |
| Q5_K_M | 3.1 GB | ~4 GB | 40-60 tok/s | Better | Quality priority |
| Q6_K | 3.5 GB | ~4.5 GB | 35-50 tok/s | High | Max quality |
| Q8_0 | 4.5 GB | ~5.5 GB | 30-45 tok/s | Near-FP16 | Benchmarking |

**llama.cpp server command:**
```bash
llama-server \
  -hf unsloth/Qwen3.5-4B-GGUF:Q4_K_M \
  -c 32768 \
  -ngl 99 \
  -fa \
  -t 8 \
  --temp 0.3 \
  --top-p 0.9 \
  --mirostat 2 \
  --mirostat-lr 0.1 \
  --mirostat-ent 5.0 \
  --host 0.0.0.0 \
  --port 8080
```

> ⚠️ Qwen3.5-4B is **multimodal** (vision). For text-only, Nemotron-3-Nano-4B or Bonsai-4B are better optimized.

---

## Nemotron-3-Nano-4B (TurboQuant-MLX)

**Repo**: `manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3`

| Format | Size | RAM | Speed | Notes |
|--------|------|-----|-------|-------|
| TurboQuant 3-bit | 2.2 GB | 4.3 GB | **75 tok/s** | Fastest 4B on Apple Silicon |
| GGUF Q4_K_M (Ollama) | ~2.8 GB | ~4 GB | 35-50 tok/s | Easiest setup |

**Best for**: Coding, reasoning traces, speed-critical tasks.

**Commands:**
```bash
# TurboQuant (fastest)
hf download manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3 --local-dir ~/models/nemotron-3-nano-4b-tq3
turboquant-generate --model ~/models/nemotron-3-nano-4b-tq3 --prompt "..." --max-tokens 1024

# Ollama (easiest)
ollama pull nemotron-3-nano:4b
ollama run nemotron-3-nano:4b --context-size 32768
```

---

## Prisma-ML Bonsai-4B (Ternary 1.58-bit)

**Status**: Referenced in MacOClock article for 27B, 4B variant **likely exists** under `prism-ml/Ternary-Bonsai-4B-tq1` (not verified in session).

**Projected specs (extrapolated from 27B):**
- Size: ~1.5-2 GB
- RAM: ~2-3 GB
- Speed: ~25-30 tok/s on M4
- Quality: Near-lossless (ternary experts with Hadamard rotation)

**If available:**
```bash
hf download prism-ml/Ternary-Bonsai-4B-tq1 --local-dir ~/models/bonsai-4b-tq1
turboquant-generate --model ~/models/bonsai-4b-tq1 --prompt "..." --max-tokens 512
```

> **Note**: Requires MLX 0.32.0+ for 2-bit matmul kernels.

---

## Comparison Summary (M4 Mini 16GB)

| Model | Engine | RAM | Speed | Quality | Setup | Best For |
|-------|--------|-----|-------|---------|-------|----------|
| **Nemotron-3-Nano-4B** | TurboQuant | 4.3 GB | **75 tok/s** | ⭐⭐⭐⭐ | Medium | Speed demon |
| **Nemotron-3-Nano-4B** | Ollama (GGUF) | 4 GB | 35-50 tok/s | ⭐⭐⭐⭐ | **Easy** | Quick start |
| **Qwen3.5-4B Q4_K_M** | llama.cpp | 3.5 GB | 50-70 tok/s | ⭐⭐⭐⭐ | Easy | Multimodal/text |
| **Bonsai-4B (proj.)** | TurboQuant | 2-3 GB | 25-30 tok/s | ⭐⭐⭐⭐⭐ | Medium | RAM-constrained |

---

## Anti-Hallucination Config (All Models)

```bash
# llama.cpp
--temp 0.3 --top-p 0.9 --mirostat 2 --mirostat-lr 0.1 --mirostat-ent 5.0 --repeat-penalty 1.1

# TurboQuant-MLX
--temp 0.3 --top-p 0.9 --min-p 0.05

# System prompt addition:
# "If uncertain, say 'I don't know' or 'I need to verify.' Do not fabricate APIs, functions, or facts. Cite provided context."
```

---

## Memory / Persistence (RAG)

Local models have **no persistent memory**. Required stack:

```
Obsidian Vault → Python Extraction → Chroma/LanceDB → Embedding (nomic-embed-text) → 
  Retrieval → Context Injection (32K window) → Local LLM
```

**Context window**: All 4B GGUFs support 32K-262K tokens. Use `-c 32768` for RAG.

---

## Verification Checklist

- [ ] `sysctl iogpu.wired_limit_mb=12288` set (16GB M4)
- [ ] Model loads without OOM
- [ ] Generation > 30 tok/s
- [ ] Temperature 0.3 + mirostat 2 reduces hallucination
- [ ] RAG pipeline injects relevant context
- [ ] KV cache compression enabled (K8/V3) for long contexts