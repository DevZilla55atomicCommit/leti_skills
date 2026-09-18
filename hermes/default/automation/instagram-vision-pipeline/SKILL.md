---
name: instagram-vision-pipeline
description: "Batch vision analysis of IG Reels via local Ollama qwen3-vl."
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [Instagram, Vision, Ollama, Batch, Pipeline, DaVinci]
---

# Instagram Vision Pipeline

> **Class-level skill** for batch vision analysis of Instagram Reels frames using local Ollama or cloud providers. Handles rate limiting, parallel workers, progress tracking, and JSON extraction robustness.

---

## What This Does

```text
VISION_PROGRESS.json (frame paths + status)
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│  INSTAGRAM-VISION-PIPELINE                                      │
├─────────────────────────────────────────────────────────────────┤
│  1. Load progress checkpoint                                    │
│  2. Filter pending videos with existing frames                  │
│  3. Batch process (N parallel workers)                          │
│  4. Vision analysis via Ollama API / cloud provider             │
│  5. Robust JSON extraction (markdown blocks, thinking tags)     │
│  6. Atomic progress updates (file-locked)                       │
│  7. Resume from checkpoint on interruption                      │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
Updated VISION_PROGRESS.json + technique JSONs per video
```

---

## Quick Start

```bash
# Local Ollama (stable, no rate limits)
python local_ollama_vision_worker.py

# Or via Hermes background process
hermes terminal --background --notify -- python local_ollama_vision_worker.py
```

### Configuration (in worker script)

```python
MODEL = "qwen3-vl:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_WORKERS = 2
RATE_LIMIT_SECONDS = 3.0  # ~20 RPM
BATCH_SIZE = 10
```

---

## Worker Architecture

### `local_ollama_vision_worker.py` (Production)

**Key Features:**
- **ThreadPoolExecutor** with `MAX_WORKERS` parallel vision calls
- **Rate limiter** (shared across workers) — respects RPM limits
- **Ollama `/api/generate` endpoint** (not `/api/chat` — avoids llama-server)
- **Robust JSON extraction** — handles:
  - Markdown code blocks: ````json ... ````
  - Thinking tags: `<thinking>...</thinking>`
  - Partial/truncated responses
- **File-locked progress writes** — atomic temp-file + rename
- **Checkpoint resume** — skips completed, continues pending
- **Background process compatible** — `notify_on_complete=true`

### Why Not These Alternatives

| Approach | Failure Mode |
|----------|--------------|
| `vision_analyze` tool | 20 RPM cloud limit → 429 errors |
| `llama-server` (port 52317+) | Process churn: dies/restarts on random ports |
| Subprocess bridge to `vision_analyze` | Tool only works IN Hermes agent context |

---

## Ollama Server Stability

| Process | Port | Stability | Notes |
|---------|------|-----------|-------|
| `ollama serve` | 11434 | ✅ Stable | Single process, runs for days |
| `llama-server` | 52317+ | ❌ Unstable | Spawned per `/api/chat`, dies, restarts on new port (52317, 53776, 55618...) |

**Rule:** Use `/api/generate` (completion) for vision. Avoid `/api/chat` (triggers llama-server).

### Critical Finding: Local Models on 16GB M4

| Model | Size | Vision? | Viable? | Notes |
|-------|------|---------|---------|-------|
| qwen3-vl:8b | 6GB | ✅ | ❌ | 180s timeouts, llama-server churn |
| qwen3.5:4b | 3.39GB | ✅ | ❌ | Connection aborted, server crashes |
| qwen3.5-64k | 6.59GB | ✅ | ❌ | Timeouts, server instability |
| gemma4:12b | 7.5GB | ✅ | ⚠️ | Marginal, likely OOM/slow |
| **gemma4:31b-cloud** | **32GB** | ✅ | ❌ **Impossible** | Won't fit in 16GB RAM |

**Cloud vision is the only viable path on 16GB hardware.** Local Ollama vision models crash the server or timeout.

---

## NVIDIA vision_analyze Tool — PRIMARY VIABLE METHOD (2026-07-30)

The Hermes `vision_analyze` tool using NVIDIA's `google/diffusiongemma` (or `gemini-2.5-flash`) is the **only reliable vision method** on 16GB Mac Mini M4.

### Configuration

```yaml
# ~/.hermes/config.yaml
vision:
  provider: nvidia
  model: google/diffusiongemma-26b-a4b-it  # or gemini-2.5-flash
```

### Usage Pattern (Sequential in Main Agent)

```python
# Main agent loop - works because vision_analyze is native Hermes tool
for item in pending_items:
    result = vision_analyze(
        image_url=item['frame_path'],
        question=VISION_PROMPT.format(**item)
    )
    parse_and_store_result(result)
    time.sleep(3.2)  # 20 RPM limit
```

**DO NOT** use sub-agents for vision analysis — `vision_analyze` tool ONLY works in Hermes agent context.

### Performance Metrics (2026-07-29 Extended - 564 frames complete)

| Metric | Value |
|--------|-------|
| Total analyzed this session | 54 frames |
| Latency per frame | 3-5s (avg ~4s) |
| Rate limit | 20 RPM enforced via 3.2s sleep |
| Success rate | ~95% (5% non-Resolve marked error) |
| Non-Resolve content rate | ~11% (133/1146) |
| JSON parsing | Clean native output, no markdown stripping needed |
| Session throughput | ~15 frames/hour (manual sequential) |

### Non-DaVinci Content Handling (Confirmed Pattern)

When vision analysis returns content without DaVinci Resolve techniques:
1. **Mark status = "error"** in VISION_PROGRESS.json with reason: "Non-Resolve content (gimbal tutorial / lens comparison / pure cinematography)"
2. **Skip skill generation** — no Hermes skill created
3. **Skip vault update** — no Obsidian note created
3. **Error count**: 133 videos (11.6% of 1146) as of 2026-07-29

Examples from this session:
- `CxbBIniIbV_` — "2 easy gimbal moves" tutorial (pure camera technique)
- `C4aFM7DNW01` — Shopping cart / POV diagram (not Resolve)
- `C4Hm6kYvoMr` (first analysis) — Behind-the-scenes gimbal shot (no Resolve technique shown)

### Non-Resolve Skills Created (2026-07-30)

Rather than skipping non-Resolve content entirely, created dedicated skill categories:

**Cinematography Techniques** (`~/.hermes/skills/cinematography-techniques/`):
- `gimbal-movement-basics.md` — 7 core movements, stabilization best practices
- `camera-movement-transitions.md` — Whip pan, match cut, invisible cut, drone transitions

**Photography Techniques** (`~/.hermes/skills/photography-techniques/`):
- `architectural-photography-lighting.md` — Natural/artificial light, HDR, composition
- `lens-selection-cinematic-look.md` — Focal length effects, sensor crop, aperture choices
- `gimbal-camera-movements.md` — 7 core movements, composite moves, Resolve post-stabilization
- `split-screen-comparison-technique.md` — Edit/Fusion methods, layouts, sync/alignment
- `color-grading-theory-fundamentals.md` — Scopes, primary/secondary, creative looks, LUTs, HDR
- `motion-graphics-fundamentals-fusion.md` — Text animation, keyframing, tracking, particles, 3D, macros

**Camera Hardware** (`~/.hermes/skills/camera-hardware/`):
- `camera-gear-workflow.md` — Sensor formats, codecs, log profiles, lens mounts, accessories, media management

### Why This Works When Local Ollama Fails

| Aspect | Local Ollama (qwen3-vl:8b) | NVIDIA vision_analyze |
|--------|---------------------------|----------------------|
| Latency | 180s+ (often timeout) | 3-5s |
| Server stability | Crashes llama-server | N/A (cloud) |
| Memory | 6GB+ VRAM + system | 0 local |
| Rate limit | None (but unusable) | 20 RPM |
| JSON output | Needs `<thinking>` strip | Clean native JSON |
| Sub-agent compatible | No | No (both need main agent) |

---

## Progress File Format

`VISION_PROGRESS.json`:

```json
[
  {
    "video_id": "C-FvSX-piqT",
    "collection": "DaVinci Core",
    "frame_to_analyze": "/Volumes/.../frames/C-FvSX-piqT/frame_0001.jpg",
    "status": "pending|complete|error",
    "result": { "technique_name": "...", "resolve_page": "Color", ... },
    "error": null,
    "updated_at": "2026-07-28T10:07:22"
  }
]
```

### Reset Errored → Pending (when frames exist)

```python
for v in data:
    if v.get('status') == 'error':
        frame_path = v.get('frame_to_analyze')
        if frame_path and Path(frame_path).exists():
            v['status'] = 'pending'
            v['error'] = None
```

---

## Cloud Ollama Provider (Optional)

Add to `~/.hermes/config.yaml` for cloud fallback:

```yaml
providers:
  ollama-cloud:
    api: https://ollama.com/api
    api_key: "YOUR_KEY"
    default_model: qwen3-vl:8b
    models:
      - qwen3-vl:8b
      - llama3.2-vision:11b
      - gemma3:27b
      - qwen3:32b
    name: Ollama Cloud
```

**Critical Finding: Ollama Cloud has NO vision models** (tested via `/api/tags` — only text LLMs: mistral-large, gpt-oss, nemotron, etc.). Your API key only accesses text models.

**To use cloud vision with Hermes**, switch auxiliary vision provider to one that supports vision + batch:

```yaml
auxiliary:
  vision:
    provider: google-gemini      # or openrouter
    model: gemini-1.5-flash       # ~2-3s/img, batch 16
```

Then `vision_analyze` tool routes through that provider.

---

## Integration with Instagram → DaVinci Pipeline

### Phase 2 Output → Phase 3 Input

After vision completes per collection:

```python
# Cluster techniques by name/page/parameters
clusters = cluster_techniques(vision_results)

# For each cluster with ≥2 videos → generate Hermes skill
for cluster in clusters:
    skill_md = render_skill_template(cluster)
    write_skill(skill_md)
    hermes_skill_install(skill_path)
```

### Skill Template Fields (from vision result)

| Vision Field | Skill Template Field |
|--------------|---------------------|
| `technique_name` | `name`, `description` |
| `resolve_page` | `tags` (Color/Edit/Fusion/Fairlight) |
| `node_graph_type` | `node_structure` |
| `key_nodes` | `key_nodes` |
| `parameters` | `parameters` |
| `steps_to_reproduce` | `steps` |
| `difficulty` | `difficulty` |
| `tags` | `tags` |
| `frame_to_analyze` | `reference_frame` |
| `video_id` | `source_reel` |

---

## Troubleshooting

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| `HTTPConnectionPool... Max retries exceeded` | Ollama server down | `ollama serve` in background |
| `No valid JSON in: ...` | Model output malformed | Check extraction logic; `qwen3-vl` emits `<thinking>` |
| `Frame not found` | Phase 1 didn't extract | Re-run frame extraction for that video |
| Worker exits silently | OOM or timeout | Check logs; reduce `MAX_WORKERS` |
| 429 errors | Using cloud `vision_analyze` | Switch to local worker |

---

## File Structure

```
instagram-vision-pipeline/
├── SKILL.md
├── references/
│   ├── vision-analysis-protocol.md     # Phase 2 protocol (prompts, sampling, clustering)
│   ├── local-ollama-worker-pattern.md  # This worker pattern (extractable)
│   └── ollama-cloud-config.md          # Cloud provider setup
├── templates/
│   └── vision_prompt.json              # Standard vision analysis prompt
├── scripts/
│   ├── local_ollama_vision_worker.py   # Production worker
│   └── reset_progress_errors.py        # Reset errored→pending
└── assets/
```

---

## Dependencies

- Python: `requests`, `threading`, `json`, `pathlib`, `time`, `re`
- Ollama: `ollama serve` running, `qwen3-vl:8b` pulled
- Hermes: `vision_analyze` tool (for cloud fallback)
- Disk: ~50GB for frames + analysis JSONs

---

## Session History

| Session | Progress | Notes |
|---------|----------|-------|
| 20260728 | 659 pending → processing | Local worker `proc_95f01d68347d` running |
| 20260727 | 665 errors reset → pending | Frame-not-found: 45 left as error |
| 20260727 | 436 complete, 306 timeouts | llama-server instability |
| 20260726 | 235 quality results (DaVinci Core) | Cloud vision_analyze (20 RPM) |

---

## Related Skills

- `instagram-davinci-learning-pipeline` — upstream (URL parsing, frame extraction, skill generation)
- `instagram-reels-pipeline` — downstream (download, dedup)
- `batch-vision-analysis` — legacy (rate-limited cloud)
- `tag-aware-vision-extraction` — category-specific prompts