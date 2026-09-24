---
title: Ollama Local vs Cloud Vision Analysis
date: 2026-07-28
session: Instagram→DaVinci pipeline vision batch (2c/2d)
tags: [ollama, vision, qwen3-vl, rate-limits, local-vs-cloud]
---

# Ollama Local vs Cloud Vision Analysis — Findings

## Summary

During Phase 2 (Vision Analysis) of the Instagram→DaVinci pipeline, we tested multiple approaches for running vision analysis on 2,818 video frames:

| Approach | Model | Speed | Reliability | Rate Limits | Context |
|----------|-------|-------|-------------|-------------|---------|
| **Local Ollama API** | qwen3-vl:8b | 30-60s/call | ❌ Frequent 180s timeouts | None | Mac Mini M4 16GB |
| **llama-server subprocess** | qwen3-vl:8b | Variable | ❌ Process crashes, port churn | None | Multiple ports (52317→53776→55618) |
| **Hermes `vision_analyze`** | NVIDIA/Google | 10-15s/call | ✅ Reliable | 20 RPM (6s delay) | Only works in agent context |
| **Ollama Cloud** (new) | qwen3-vl:8b, llama3.2-vision:11b, gemma3:27b | Untested | ? | ? | Added to config with user API key |

## Local Ollama (Port 11434)

**Endpoint**: `http://localhost:11434/api/generate`

**Working**: Direct API calls work correctly, return valid JSON with `<thinking>` tags.

**Problem**: Too slow on Mac Mini M4 16GB RAM:
- qwen3-vl:8b: 30-60 seconds per call typical
- 180-second timeout hit on ~40% of calls
- 2 parallel workers = ~2-4 calls/minute = 3-5 hours for 626 videos

**Worker**: `local_ollama_vision_worker.py` (proc_5f1e57cb0044) — running but slow.

## llama-server Subprocess (Abandoned)

**Symptoms**:
- Multiple `llama-server` processes spawned on random ports
- Each dies/restarts: 52317 → 53776 → 55618 → 11434...
- "Connection refused" and timeout errors cascade
- Scripts: `qwen_vision_worker.py`, `qwen_vision_worker_fixed.py`, `qwen_generate_worker.py` all failed

**Root cause**: llama-server instability when called as subprocess from Python workers.

## Hermes `vision_analyze` Tool (Cloud)

**Works perfectly**: ~10-15 seconds per call via Hermes gateway.

**Constraint**: 20 RPM hard limit (6s minimum between calls). 429 errors if exceeded.

**Critical limitation**: Only works **inside Hermes agent context**. Cannot call from standalone Python scripts (`from hermes_tools import vision_analyze` fails with `ModuleNotFoundError: hermes_tools`).

**Usage**: Manual calls during session, or via agent-driven batch.

**Best for**: Small batches, validation, when local fails.

## Ollama Cloud Provider (New)

Added to `config.yaml`:
```yaml
providers:
  ollama-cloud:
    api: https://ollama.com/api
    api_key: "139a698fca49456ba86a3c33b656644d.xo5iT9bvt8qYVfB4Y7gTT7Tr"
    default_model: qwen3-vl:8b
    models:
      - qwen3-vl:8b
      - llama3.2-vision:11b
      - gemma3:27b
      - qwen3:32b
    name: Ollama Cloud
```

**Untested** — should route vision requests through Ollama's cloud instead of NVIDIA.

## JSON Extraction Pattern (Both Workers)

```python
def extract_json(text):
    # Remove qwen3-vl thinking tags
    text = re.sub(r'', '', text, flags=re.DOTALL)
    # Try markdown code blocks
    for pattern in [r'```json\s*(.*?)\s*```', r'```\s*(.*?)\s*```']:
        matches = re.findall(pattern, text, re.DOTALL)
        for m in matches:
            try: return json.loads(m.strip())
            except: pass
    # Try direct JSON
    try: return json.loads(text.strip())
    except: pass
    # Find first complete JSON object
    try:
        start = text.index('{')
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i+1])
    except: pass
    raise ValueError(f"No valid JSON in: {text[:300]}")
```

Handles: `<thinking>` tags, markdown code blocks, partial responses.

## Recommended Strategy for Pipeline

**Current state** (2026-07-28):
- DaVinci Core: ✅ 445 complete (cloud vision_analyze)
- Cinematic/Shooting: 🔄 626 pending (local worker running)
- Remaining: ⏳ 688 pending

**Optimal path**:
1. **Let local worker finish** 626 pending (3-5 hours, no rate limits, background)
2. **Use cloud `vision_analyze`** for remaining 688 (rate limited to 20 RPM = ~30 min for 600)
3. **Test ollama-cloud** as fallback if NVIDIA rate limited

**For future runs**:
- Pre-extract frames for ALL videos first (blocker: 778 "Frame not found")
- Consider `gemma3:27b` on ollama-cloud for higher quality
- Local qwen3-vl:8b viable for overnight/background, not interactive