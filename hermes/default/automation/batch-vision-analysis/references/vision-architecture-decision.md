# Vision Architecture Decision (2026-07-28)

## Executive Summary
**Local qwen3-vl:8b on Mac Mini M4 16GB is NOT viable** for vision analysis — 180s timeouts, unstable llama-server processes. **Cloud `vision_analyze` (NVIDIA provider) is the only working path** at ~10-15s/call sequential.

---

## What Was Tested

| Approach | Result | Notes |
|----------|--------|-------|
| Local qwen3-vl:8b via Ollama API (port 11434) | ❌ Failed | 180s timeouts, llama-server crashes/restarts on random ports |
| Local qwen3-vl:8b via llama-server (ports 52317→53776→55618) | ❌ Failed | Process churn, 0 successful calls |
| Hermes `vision_analyze` tool (NVIDIA provider) | ✅ Works | ~10-15s/call, sequential only |
| Ollama Cloud API (user API key) | ❌ No vision models | Only text LLMs (nemotron, gpt-oss, kimi, etc.) |
| Sub-agents calling `vision_analyze` | ❌ Impossible | Tool only works in main agent context |

---

## Why Local Model Failed

**Hardware constraint**: Mac Mini M4 16GB unified memory
- qwen3-vl:8b Q4_K_M = ~9GB model + system overhead
- llama-server spawns, allocates, OOMs/hangs, restarts on new port
- Each vision call needs full model in VRAM → swap thrashing

**Process instability**: 
- llama-server PID changes every few minutes (52317 → 53776 → 55618 → 62165)
- Worker scripts can't maintain stable connection
- 100% failure rate after first few calls

---

## Why Cloud `vision_analyze` Works

- NVIDIA Nemotron provider handles vision inference remotely
- Image attached to main conversation context → model analyzes pixels directly
- No local GPU/RAM pressure
- ~10-15s per call reliable

**Limitation**: Sequential only. `vision_analyze` binds to current agent context — cannot parallelize via sub-agents or background workers.

---

## Ollama Cloud API Reality Check

```bash
# Models available on ollama.com/api with API key:
curl -H "Authorization: Bearer $KEY" https://ollama.com/api/tags

# Returns: nemotron-3-ultra, gpt-oss:20b, gpt-oss:120b, kimi-k3, 
#          deepseek-v4-pro/flash, glm-5.1/5.2, minimax-m2.5/2.7/m3,
#          gemma4:31b, qwen3.5:397b, mistral-large-3:675b...

# NO vision models (qwen3-vl, llama3.2-vision, gemma3, etc.)
```

**Conclusion**: Ollama Cloud API is for **text inference only**. Cannot use for vision analysis.

---

## Architecture Implications

### Current Pipeline (Sequential)
```
Main Agent → vision_analyze(frame) → wait 10-15s → update JSON → repeat
```
**Throughput**: ~300-400 videos/hour

### Cannot Parallelize Because:
1. `vision_analyze` tool requires image attachment to **main context**
2. Sub-agents run in isolated processes with their own terminal sessions
3. Sub-agents inherit parent model but **cannot call tools requiring main context**

### Only Real Speedups
| Option | Speedup | Feasibility |
|--------|---------|-------------|
| Switch to Gemini/GPT-4o provider (if configured) | 2-3x (batch support) | Requires API keys + config |
| Reduce calls via smarter frame sampling | 5-10x fewer calls | Already at 1 key frame/video |
| Run skills/vault in parallel | N/A (vision bottleneck) | ✅ Do this instead |

---

## Recommendation

**Accept sequential vision (~8-10 hours for 2,370 remaining)** and parallelize everything else:
- Skill authoring from completed analyses
- Vault rebuild with new techniques
- Skill installation/validation

**Do NOT waste time on**:
- Local vision model optimization (hardware-limited)
- Ollama Cloud for vision (no models)
- Sub-agent vision workers (architectural impossibility)

---

## Related Skills
- `instagram-davinci-learning-pipeline` — Phase 2 vision analysis section
- `instagram-reels-pipeline` — Frame extraction complete, vision pending
- `hermes-agent` — `vision_analyze` tool behavior

---

*Generated from session 2026-07-28. Update when hardware/provider changes.*