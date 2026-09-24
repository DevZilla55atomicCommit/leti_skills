---
name: vision-skill-authoring
description: Run vision analysis on frames to author DaVinci skills.
category: automation
tags: [vision-analysis, skill-authoring, da-vinci-resolve, batch-processing, subagent-delegation]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-26
---

# Vision Analysis → Skill Authoring Pipeline

Run vision analysis on video frames at scale and author Hermes skills from results.

## Pipeline Stages

### Stage 1: Prepare Analysis Queue

```python
# Load VISION_PROGRESS.json
# Filter for pending DaVinci Core videos
# Select top N (e.g., 20) for batch
# Build queue entries with frame_path, context, prompt
# Save to vision_batch_queue.json
```

**Queue entry format**:
```json
{
  "video_id": "Cvzl4_zN5jm",
  "collection": "Color_grading",
  "frame_path": "/Volumes/.../frames/Cvzl4_zN5jm/frame_0010.jpg",
  "caption": "How to make your photos moody...",
  "techniques": ["color-grading", "curves"],
  "transcript": "Use S-curve for contrast..."
}
```

### Stage 2: Dispatch Subagent

```python
delegate_task(
    goal="Process vision_batch_queue.json (20 videos) using vision_analyze with 20 RPM rate limiting. Update VISION_PROGRESS.json with results.",
    context="Queue file: /Users/alfredkamisese/vision_batch_queue.json\nProgress file: /Volumes/Samsung LED/.../VISION_PROGRESS.json\nRate limit: 3.2s between calls"
)
```

**Subagent responsibilities**:
- Read queue and progress files
- For each pending video: call `vision_analyze` with frame + prompt
- Parse JSON from vision result
- Update `VISION_PROGRESS.json` via `terminal` + Python heredoc
- Sleep 3.2s between calls (20 RPM)
- On 429: sleep 10s → 30s → 60s, retry up to 3x
- Report completion summary

### Stage 3: Monitor & Iterate

```bash
# Check progress
python3 -c "
import json
with open('.../VISION_PROGRESS.json') as f:
    d = json.load(f)
print(f'Complete: {sum(1 for v in d if v.get(\"status\")==\"complete\")}')
print(f'Pending: {sum(1 for v in d if v.get(\"status\")==\"pending\")}')
"

# Tail subagent log
tail -f ~/.hermes/cache/delegation/live/{delegation_id}/task-0.log
```

### Stage 4: Author Skills from Analyses

**For each `status="complete"` entry with valid technique**:

```python
# Template → SKILL.md
skill_data = {
    "name": f"davinci-{technique_slug}",
    "category": "davinci-resolve",
    "tags": ["color-grading", page.lower(), node_graph.lower(), ...],
    "source_video": video_id,
    "source_url": f"https://www.instagram.com/reel/{video_id}/",
    "technique": technique_name,
    "resolve_page": resolve_page,
    "node_graph": node_graph,
    "key_nodes": key_nodes,
    "parameters": parameters,
    "steps": steps,
    "frame_refs": frame_list,
    "gif_path": f"CONTENT_PROCESSING/gifs/{video_id}.gif"
}
```

**Output**: `~/.hermes/skills/davinci-resolve/davinci-{technique-slug}.md`

### Stage 5: Validate & Install

```bash
# Validate each skill
hermes skill validate davinci-{technique-slug}

# Install all
for skill in ~/.hermes/skills/davinci-resolve/*.md; do
    hermes skill install "$(basename $skill .md)" --profile default
done
```

## Rate Limiting & Error Handling

| Scenario | Handling |
|----------|----------|
| **20 RPM limit** | 3.2s sleep between `vision_analyze` calls |
| **HTTP 429** | Exponential backoff: 10s → 30s → 60s, max 3 retries |
| **Invalid JSON** | Mark "failed", log raw response, continue |
| **"N/A" technique** | Mark complete, technique="N/A", skip skill creation |
| **Subagent timeout** | Re-dispatch remaining queue with new subagent |

## Vision Analysis: Cloud-Only Strategy (UPDATED 2026-07-28)

### Cloud Vision (Hermes `vision_analyze` tool) — PRIMARY
| Parameter | Value |
|-----------|-------|
| Rate Limit | 20 RPM (3s minimum between calls) |
| Latency | ~3-5s/call (NVIDIA DiffusionGemma) |
| Quality | High (native vision model) |
## Vision Analysis: NVIDIA `vision_analyze` Only Strategy (UPDATED 2026-07-29)

### NVIDIA `vision_analyze` Tool — PRIMARY VIABLE METHOD (2026-07-29)

The Hermes `vision_analyze` tool using NVIDIA's `google/diffusiongemma` (or `gemini-2.5-flash`) is the **only reliable vision method** on 16GB Mac Mini M4.

| Parameter | Value |
|-----------|-------|
| Rate Limit | 20 RPM (3s minimum between calls) |
| Latency | ~3-5s/call (NVIDIA DiffusionGemma / Gemini) |
| Quality | High (native vision model) |
| Use For | ALL vision analysis |
| Tool | `vision_analyze(image_url, question)` — ONLY works in Hermes agent context |

**Failure Pattern**: Subprocess wrapping `vision_analyze` fails because tool only works in Hermes agent context, not standalone Python.

### Local Ollama Vision Models — NOT VIABLE on 16GB Mac Mini M4

| Model | Size | Vision? | Status |
|-------|------|---------|--------|
| qwen3-vl:8b | 6GB | ✅ | ❌ 180s timeouts, llama-server churn |
| qwen3.5:4b | 3.39GB | ✅ | ❌ Connection aborted, server crashes |
| qwen3.5-64k | 6.59GB | ✅ | ❌ Timeouts, server instability |
| gemma4:12b | 7.5GB | ✅ | ⚠️ Marginal, likely OOM |
| gemma4:31b-cloud | 32GB | ✅ | ❌ **Impossible** — won't fit in RAM |

**TESTED & FAILED on 16GB Mac Mini M4**: qwen3-vl:8b times out at 180s+ per call; qwen3.5:4b connection aborted; llama-server process crashes/restarts on random ports. 16GB RAM insufficient for vision model + OS + other workloads. **USE CLOUD `vision_analyze` TOOL EXCLUSIVELY**.

### Critical Hardware Constraint (2026-07-29 Finding)

| Model | Size | Vision? | Viable on 16GB M4? |
|-------|------|---------|---------------------|
| qwen3-vl:8b | 6GB | ✅ | ❌ 180s timeouts, llama-server churn |
| qwen3.5:4b | 3.39GB | ✅ | ❌ Connection aborted, server crashes |
| gemma4:12b | 7.5GB | ✅ | ⚠️ Marginal, likely OOM |
| gemma4:31b-cloud | 32GB | ✅ | ❌ **Impossible** — won't fit in RAM |
| Ollama Cloud API | N/A | ❌ | N/A — text-only models |

**Conclusion:** Local vision on 16GB M4 is NOT viable for batch processing. Only cloud `vision_analyze` works reliably.

### Sequential Processing Pattern (CRITICAL)

Since `vision_analyze` only works in Hermes agent context (not subprocesses), process sequentially in main agent:

```python
# Main agent loop - works because vision_analyze is native tool
for item in pending_items:
    result = vision_analyze(
        image_url=item['frame_path'],
        question=VISION_PROMPT.format(**item)
    )
    parse_and_store_result(result)
    time.sleep(3.2)  # 20 RPM limit
```

**Do NOT** use sub-agents for vision analysis — they cannot call `vision_analyze` tool.

### Performance Metrics (2026-07-29 Session)

| Metric | Value |
|--------|-------|
| Latency per frame | 3-5s |
| Rate limit | 20 RPM (3.2s minimum) |
| Success rate | ~100% |
| JSON parsing | Reliable (native vision model) |
| Session throughput | ~15-20 frames |

### Why This Works When Local Ollama Fails

| Aspect | Local Ollama (qwen3-vl:8b) | NVIDIA vision_analyze |
|--------|---------------------------|----------------------|
| Latency | 180s+ (often timeout) | 3-5s |
| Server stability | Crashes llama-server | N/A (cloud) |
| Memory | 6GB+ VRAM + system | 0 local |
| Rate limit | None (but unusable) | 20 RPM |
| JSON output | Needs `<thinking>` strip | Clean native JSON |
| Sub-agent compatible | No | No (both need main agent) |

## References

- [vision-prompt.md](references/vision-prompt.md) — Full prompt template
- [rate-limiting.md](references/rate-limiting.md) — 20 RPM + backoff details
- [subagent-pattern.md](references/subagent-pattern.md) — Delegation + monitoring guide
- [skill-template.md](templates/davinci-skill.template.md) — Skill template
- [session-20260728-vision-pipeline-execution.md](references/session-20260728-vision-pipeline-execution.md) — Full session learnings, metrics, config fixes