# Quick Start: Qwen3.5-4B on Apple Silicon (M4/M3/M2)

**Session**: 2026-07-22 | User: Alfred | Goal: 30-second setup for fast local Qwen3.5-4B

## Option 1: Ollama (Fastest to Working Model)

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull Nemotron-3-Nano-4B (best 4B for coding/reasoning)
ollama pull nemotron-3-nano:4b

# Run with large context
ollama run nemotron-3-nano:4b --context-size 32768

# For actual Qwen3.5-4B (multimodal):
ollama pull qwen2.5:4b  # Qwen2.5, not 3.5 (Qwen3.5-4B GGUF is vision)
```

---

## Option 2: llama.cpp Server (Best Performance/Control)

```bash
# Install
brew install llama.cpp

# Run Qwen3.5-4B Q4_K_M (best balance)
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
  --repeat-penalty 1.1 \
  --host 0.0.0.0 \
  --port 8080

# Test
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Write a Python async HTTP client"}],"max_tokens":512,"temperature":0.3}'
```

**Expected on M4 16GB**: 50-70 tok/s, ~3.5 GB RAM

---

## Option 3: TurboQuant-MLX (Fastest Inference)

```bash
# Install
pip install turboquant-mlx-full

# Download Nemotron-3-Nano-4B (75 tok/s!)
hf download manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3 \
  --local-dir ~/models/nemotron-3-nano-4b-tq3

# Generate
turboquant-generate \
  --model ~/models/nemotron-3-nano-4b-tq3 \
  --prompt "Implement binary search in Python" \
  --max-tokens 512 \
  --temp 0.7

# Serve API
turboquant-serve --model ~/models/nemotron-3-nano-4b-tq3 --port 8080
```

**Prereq**: `sudo sysctl iogpu.wired_limit_mb=12288` (16GB M4)

---

## Anti-Hallucination Settings (All Methods)

| Parameter | Value | Why |
|-----------|-------|-----|
| `temperature` | 0.3 | Low creativity = fewer fabrications |
| `top_p` | 0.9 | Nucleus sampling |
| `mirostat` | 2 | Adaptive entropy control |
| `mirostat_lr` | 0.1 | Learning rate for mirostat |
| `mirostat_ent` | 5.0 | Target entropy |
| `repeat_penalty` | 1.1 | Discourage loops |

**System prompt addendum:**
> "If uncertain, say 'I don't know' or 'I need to verify.' Do not fabricate APIs, functions, or facts. Cite provided context."

---

## Memory / Persistence (RAG)

Local models = **stateless**. For memory:

```python
# Your stack: Obsidian → Python → Chroma/LanceDB → nomic-embed-text → RAG → 32K context
# Inject top-k chunks into every prompt
```

---

## Quick Decision

| Need | Command |
|------|---------|
| Working in 30 sec | `ollama pull nemotron-3-nano:4b && ollama run nemotron-3-nano:4b` |
| Best Qwen3.5-4B text | `llama-server -hf unsloth/Qwen3.5-4B-GGUF:Q4_K_M -c 32768 -ngl 99 -fa` |
| Maximum speed | `pip install turboquant-mlx-full && hf download manjunathshiva/NVIDIA-Nemotron-3-Nano-4B-BF16-tq3` |
| Lowest RAM | TurboQuant Bonsai-4B (if available) ~2-3 GB |