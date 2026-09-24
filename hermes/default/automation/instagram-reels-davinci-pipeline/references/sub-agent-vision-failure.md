# Sub-Agent Vision Analysis Failure — Root Cause & Resolution

**Date:** 2026-07-30
**Session:** 20260730
**User Correction:** "Never run a delegate tasks like that using a local ollama model as it hit OOM and crash my Mac mini"

---

## CRITICAL ROOT CAUSE DISCOVERED (2026-07-30)

**THE FUNDAMENTAL MISCONCEPTION:** `vision_analyze` tool uses the **parent assistant's built-in NVIDIA vision model (Gemini)**, NOT local Ollama models. Sub-agents CANNOT access the parent's vision model — they only inherit the text LLM configuration.

### What This Means

| Configuration | Vision Model Used | Works? |
|---------------|-------------------|--------|
| Sub-agent with `ollama-launch` | Local Ollama (text only) | ❌ Cannot proxy NVIDIA vision calls |
| Sub-agent with `ollama-cloud` | Cloud text LLM | ❌ Cannot access parent's vision tool |
| **Main session (manual)** | **Parent's NVIDIA (Gemini)** | ✅ **ONLY WORKING PATH** |

**The vision tool is a built-in capability of the main assistant model, not a configurable provider.** Even with `ollama-cloud`, sub-agents would inherit the cloud **text** LLM but **cannot access the parent's vision_analyze tool**.

---

## What Happened

### Dispatch
```python
delegate_task(
    tasks=[
        {"goal": "Process vision analysis for Batch 1 (37 videos)", ...},
        {"goal": "Process vision analysis for Batch 2 (37 videos)", ...},
        # ... 6 batches total, 221 videos
    ]
)
```

### Result
All 6 sub-agents **timed out at 600s** with only **1 API call completed each**.

```
Task 1: status=timeout, api_calls=1, 600.6s
Task 2: status=timeout, api_calls=1, 600.51s
Task 3: status=timeout, api_calls=1, 600.5s
Task 4: status=timeout, api_calls=1, 600.64s
Task 5: status=timeout, api_calls=1, 600.63s
Task 6: status=timeout, api_calls=1, 600.6s
```

### Root Cause Chain
1. Sub-agents used `provider: ollama-launch` (local Ollama)
2. Each sub-agent runs inference on Mac Mini M4 16GB
3. 6 concurrent × 3-4GB RAM = 18-24GB needed > 16GB available
4. Immediate OOM → llama-server crashes → sub-agent hangs → 600s timeout
5. **EVEN IF local worked:** vision_analyze uses parent's NVIDIA model, not sub-agent's Ollama

### User's Explicit Correction
> "Never run a delegate tasks like that using a local ollama model as it hit OOM and crash my Mac mini"

---

## Correct Configuration (config.yaml)

```yaml
delegation:
  provider: ollama-cloud           # Cloud - no local RAM pressure
  model: qwen3.5-64k               # Or other cloud model
  base_url: https://api.ollama.com/v1
  api_key: ${OLLAMA_CLOUD_API_KEY} # Required
  child_timeout_seconds: 300        # Reduced from 600
  max_concurrent_children: 3        # Reduced from 6
```

---

## Why Cloud Works, Local Fails

| Factor | Local (ollama-launch) | Cloud (ollama-cloud) |
|--------|----------------------|---------------------|
| Inference runs on | Mac Mini M4 16GB | Ollama Cloud servers |
| RAM per sub-agent | 3-4GB | 0GB local |
| 6 concurrent RAM | 18-24GB (OOM) | ~100MB orchestration |
| GPU pressure | High | None |
| llama-server crashes | Yes (OOM) | No |

---

## Batch Size Recommendations

| Approach | Batch Size | Concurrent | Timeout | Notes |
|----------|------------|------------|---------|-------|
| **Cloud sub-agents** | 10-15 videos | 3-4 | 300s | Recommended for Phase 2c/2d |
| **Manual sequential** | 1 video | 1 | N/A | ~1 min/video, 100% reliable |
| **Local sub-agents** | NEVER | NEVER | NEVER | **Hard blocked — OOM guaranteed** |

---

## Manual Workaround (Proven)

This session: **236 videos processed manually** (722 → 958) with 100% success rate, ~1 min/video, no timeouts.

```python
# Per video:
result = vision_analyze(frame_path, prompt)
update_vision_progress(video_id, result)
```

---

## Config Must-Never-Do (Burned into Skill)

```yaml
# NEVER USE - CAUSES MAC MINI CRASH
delegation:
  provider: ollama-launch
  model: qwen3.5-64k
  base_url: http://127.0.0.1:11434/v1
  max_concurrent_children: 6
  child_timeout_seconds: 600
```

**If you see this config in any delegation task for vision analysis — STOP. It will crash the Mac Mini.**