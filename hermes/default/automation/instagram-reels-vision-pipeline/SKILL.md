---
name: instagram-reels-vision-pipeline
description: "Process IG Reels frames via vision_analyze → DaVinci skills."
category: automation
tags: [instagram, reels, vision, davinci-resolve, nvidia, automation]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-29
---

# Instagram Reels Vision Analysis Pipeline

End-to-end pipeline for converting Instagram Reels into searchable DaVinci Resolve technique skills via NVIDIA vision analysis.

## Overview

| Component | Tool | Purpose |
|-----------|------|---------|
| **Vision Analysis** | NVIDIA `vision_analyze` | Only viable method on 16GB M4 Mac Mini |
| **Frame Extraction** | ffmpeg | 8 frames at [0, 14, 28, 42, 57, 71, 86, 99.9]% |
| **Technique JSON** | vision_analyze prompt | DaVinci Resolve serial node graphs with parameters |
| **Hermes Skills** | Python → SKILL.md | Searchable technique references |
| **Obsidian Vault** | Markdown | Organized by discipline with frame tables |

## Prerequisites

- Hermes Agent with `vision_analyze` tool (NVIDIA API)
- Frame directories at `/Volumes/Samsung LED/Instagram Downloads/.../frames/{video_id}/frame_*.jpg`
- Progress tracking JSON at `VISION_PROGRESS.json`
- Config: `vision` provider = `google-gemini`, model = `gemini-2.5-flash`

## Workflow

### 1. Load Progress & Queue
```python
with open('VISION_PROGRESS.json') as f:
    progress = json.load(f)

pending = [v for v in progress if v.get('status') == 'pending']
```

### 2. Process Each Video
```python
for item in pending:
    frame_path = f"/Volumes/Samsung LED/.../frames/{item['video_id']}/frame_0001.jpg"
    result = vision_analyze(
        image_url=frame_path,
        question=VISION_PROMPT.format(video_id=item['video_id'])
    )
    # Parse JSON, update progress, write file
    time.sleep(3.2)  # 20 RPM limit
```

### 3. Vision Prompt Template
```text
Analyze this cinematic shot from Instagram Reel {video_id}. Describe the visual technique (composition, lighting, color grading style) and return ONLY valid JSON for a DaVinci Resolve technique that would recreate this look:
{
  "technique_name": "Descriptive name",
  "resolve_page": "Color|Edit|Fusion|Fairlight",
  "node_graph_type": "serial|parallel|layer_mixer|compound",
  "key_nodes": ["node1", "node2"],
  "parameters": {"param1": "value1"},
  "steps_to_reproduce": ["step1", "step2"],
  "difficulty": "beginner|intermediate|advanced",
  "tags": ["tag1", "tag2"]
}
```

### 4. Create Hermes Skill
```python
skill_dir = Path(f"~/.hermes/skills/davinci-resolve-techniques/reel_{video_id}")
skill_dir.mkdir(parents=True, exist_ok=True)

skill_md = f"""---
name: reel_{video_id}
description: DaVinci Resolve technique from Instagram Reel {video_id}
category: davinci-resolve
tags: {result['tags']}
---

# {result['technique_name']}

**Page:** {result['resolve_page']}  
**Node Graph:** {result['node_graph_type']}  
**Key Nodes:** {', '.join(result['key_nodes'])}

## Parameters
```json
{json.dumps(result['parameters'], indent=2)}
```

## Steps to Reproduce
{chr(10).join(f'{i}. {s}' for i, s in enumerate(result['steps_to_reproduce'], 1))}

## Difficulty
{result['difficulty']}

## Source
Instagram Reel: {video_id}
"""

(skill_dir / "SKILL.md").write_text(skill_md)
```

## Frame Extraction Spec (Validated 2026-07-29)

| Issue | Fix |
|-------|-----|
| Frame at 100% = black on short clips | Extract at **99.9%** instead of 100% |
| Require all 8 frames | Accept **≥7 frames** (tolerate missing last frame) |
| Frame percentages hardcoded | Use: `[0, 14, 28, 42, 57, 71, 86, 99.9]` |

```bash
ffmpeg -i input.mp4 -vf "select='gte(t,{pct/100*duration})'" -vframes 1 frame_{idx:02d}.jpg
```

## Progress Tracking Schema

```json
{
  "video_id": "string",
  "status": "complete|pending|error",
  "collection": "string",
  "result": { /* technique JSON */ },
  "error": "string (if error)",
  "updated_at": "ISO timestamp"
}
```

**Deduplication:** After each session, remove stale `pending` entries for videos that now have `complete` entries.

## Hardware Constraints (Critical)

| Model | Size | Vision? | Viable on 16GB M4? |
|-------|------|---------|---------------------|
| qwen3-vl:8b | 6GB | ✅ | ❌ 180s timeouts, llama-server churn |
| qwen3.5:4b | 3.39GB | ✅ | ❌ Connection aborted, server crashes |
| gemma4:12b | 7.5GB | ✅ | ⚠️ Marginal, likely OOM |
| gemma4:31b-cloud | 32GB | ✅ | ❌ **Impossible** — won't fit in RAM |
| Ollama Cloud API | N/A | ❌ | N/A — text-only models |
| **llava:7b (local Ollama)** | **8.5 GB** | ✅ | ✅ **WORKS** — ~10 sec/frame, no rate limits |

**UPDATED 2026-07-31:** Local vision IS viable with `llava:7b` (8.5 GB) on 16GB M4. Uses ~9 GB RAM, leaves room for text model. ~35-50 sec/video (3 frames), no rate limits, fully autonomous.

## Root Cause: vision_analyze Uses Parent's NVIDIA Model, NOT Local Ollama (CRITICAL — 2026-07-30)

**THE FUNDAMENTAL MISCONCEPTION:** `vision_analyze` tool uses the **assistant's built-in NVIDIA vision model (Gemini)**, NOT local Ollama models. Sub-agents CANNOT access the parent's vision model — they only inherit the text LLM configuration.

### Failed Architecture (caused 6× 600s timeouts with 1 API call each)
```yaml
# WRONG: Local Ollama for sub-agents
delegation:
  provider: ollama-launch    # Spawns local llama-server → OOM on 16GB M4
  model: qwen3.5-64k
  base_url: http://127.0.0.1:11434/v1
  child_timeout_seconds: 600
  max_concurrent_children: 6  # 6 × 3-4GB = 18-24GB > 16GB RAM
```

**Result:** 6 parallel sub-agents launched, all timed out at 600s with only 1 API call completed. Local Ollama cannot proxy NVIDIA vision_analyze calls in sub-contexts.

### Correct Architecture Options

| Approach | Vision Model Used | Works? | Notes |
|----------|-------------------|--------|-------|
| **Manual main session** | Parent's NVIDIA (Gemini) | ✅ 100% reliable | ~1 min/video, 20 RPM limit |
| **Sub-agents with ollama-cloud** | Parent's NVIDIA* | ❌ UNTESTED | Sub-agents inherit text config only |
| **Sub-agents with ollama-launch** | Local Ollama (text only) | ❌ HARD BLOCKED | Cannot proxy NVIDIA vision calls |

**Critical:** Even with `ollama-cloud`, sub-agents would inherit the cloud text LLM but **cannot access the parent's vision_analyze tool**. The vision tool is a built-in capability of the main assistant model, not a configurable provider.

### User Correction (2026-07-30)
> "Never run delegate tasks like that using a local ollama model as it hit OOM and crash my Mac mini"

**This applies to ALL local model sub-agents for vision tasks.** The only working path is **manual sequential processing in the main session**.

## Current Working Architecture (Manual Only)

```python
# Main session loop (only reliable path)
for video in pending_videos:
    frame = f"/Volumes/.../frames/{video}/frame_0001.jpg"
    result = vision_analyze(image_url=frame, question=VISION_PROMPT)
    # Parse JSON, update progress, write skill + vault note
    time.sleep(3.2)  # 20 RPM NVIDIA limit
```

### Hardware Constraints (Validated 2026-07-30)
| Model | Size | Vision? | Viable on 16GB M4? |
|-------|------|---------|---------------------|
| qwen3-vl:8b | 6GB | ✅ | ❌ 180s timeouts, llama-server churn |
| qwen3.5:4b | 3.39GB | ✅ | ❌ Connection aborted, server crashes |
| gemma4:12b | 7.5GB | ✅ | ⚠️ Marginal, likely OOM |
| gemma4:31b-cloud | 32GB | ✅ | ❌ Impossible — won't fit in RAM |
| Ollama Cloud API | N/A | ❌ | N/A — text-only models |
| **NVIDIA vision_analyze (main)** | Cloud | ✅ | ✅ **Only working path** |

**Conclusion:** Local vision on 16GB M4 is NOT viable for batch processing. Only main session `vision_analyze` works reliably.

## Phase 2c Progress (2026-07-30 Session)

| Metric | Value |
|--------|-------|
| Phase 2c total | 1,146 Cinematic/Shooting videos |
| Previous complete | 722 |
| **This session complete** | **236** (722 → 958) |
| **Phase 2c progress** | **83.6%** (958/1,146) |
| Pending | 47 |
| Errors | 142 |
| Session throughput | ~15-20 videos |

### Downstream Pipeline Status
- ✅ Skills generated: 1,449 in `~/.hermes/skills/davinci-resolve-techniques/`
- ✅ Vault notes: 958+ technique notes with GIFs
- ✅ Scripts ready: `generate_skills.py`, `build_vault.py` for incremental updates

## Sub-Agent Batch Processing: Local Vision Overcomes Blocker (2026-07-31)

**Previous conclusion (2026-07-30):** Local vision on 16GB M4 was NOT viable. Sub-agents with local Ollama were hard blocked (OOM, cannot proxy NVIDIA vision_analyze).

**NEW 2026-07-31:** `llava:7b` (8.5 GB) works locally! This changes the architecture:

| Approach | Vision Model | Works? | Notes |
|----------|--------------|--------|-------|
| **Main session + local llava:7b** | Local Ollama | ✅ **WORKS** | ~35-50 sec/video, no rate limits |
| **Parallel background terminals + llava:7b** | Local Ollama | ✅ **WORKS** | 3x speedup, ~25-30 min for 116 videos |
| Sub-agents with local Ollama | Local Ollama (text) | ❌ **BLOCKED** | Cannot execute Python/HTTP |
| Manual main session + NVIDIA | NVIDIA cloud | ✅ Works | 20 RPM limit, ~1 min/video |

### New Working Architecture (Parallel Background)

```bash
# Launch 3 parallel background jobs via Hermes terminal(background=true)
# Each processes ~39 videos via local llava:7b
# Total time: ~25-30 min (vs 1.5 hrs sequential)

# Chunk 1
/opt/homebrew/bin/python3.12 batch_chunk.py "108,109,110,..." 1 &

# Chunk 2 
/opt/homebrew/bin/python3.12 batch_chunk.py "331,332,335,..." 2 &

# Chunk 3
/opt/homebrew/bin/python3.12 batch_chunk.py "497,503,504,..." 3 &
```

**Script:** `local-ollama-vision-pipeline/scripts/batch_chunk.py`

### Key Insight
Sub-agents still can't do vision (text-only LLMs, no terminal/HTTP access). But the **main session can run parallel background terminal processes** that execute the local vision pipeline. This achieves parallelism without sub-agents.

### GPU Contention Note (2026-07-31)
Running 4 parallel jobs all hitting `llava:7b` (100% GPU each) caused slowdown: ~150-200s/video vs ~35-50s sequential. **Recommend: 2 parallel jobs max** for optimal throughput on 16GB M4.

### Vault Structure Comparison & Migration Path (2026-07-31)

During this session, we discovered the **current pipeline vault is INCOMPLETE** compared to the existing `DaVinci_Knowledge_Base`:

| Feature | DaVinci_Knowledge_Base (Existing) | Current Pipeline Vault |
|---------|-----------------------------------|------------------------|
| Frame-by-frame vision JSON | ✅ `Vision_Reports/*.json` | ❌ |
| Quick Grade Recipe (node values) | ✅ | ❌ |
| Embedded keyframes in notes | ✅ `![[0001.jpg]]` | ❌ |
| Hermes Skill cross-reference | ✅ | ❌ |
| Pipeline status tracking | ✅ Checkboxes | ❌ |
| Domain organization | ✅ Folders | ❌ Flat |
| Exports (JSON/CSV) | ✅ | ❌ |
| Transcripts folder | ✅ | ❌ Scattered |

**The 45 GB `gifs/` folder is REDUNDANT** — vault already has 81 MB embedded GIFs in `vault/media/`.

**Migration Plan (No Regeneration):**
1. Copy `vault/` → `~/DaVinci_Vault/` (427 MB = 346 MB notes + 81 MB GIFs)
2. Skills already on internal at `~/.hermes/skills/davinci-resolve-techniques/` (1,449+)
3. Copy `VISION_PROGRESS.json` → `~/DaVinci_Vault/`
4. Delete Samsung LED `gifs/` (45 GB) and completed `frames/` (~6 GB)
5. Keep original MP4s on Samsung LED if needed

**Result:** Free 54+ GB on Samsung LED, keep all curated outputs on internal.

### Storage Crisis & Migration Path (2026-07-31)
**Samsung LED at 96% full (5.4 GB free)** — pipeline working data must be migrated before continuing.

#### What's on Samsung LED (External)
| Path | Size | Keep? |
|------|------|-------|
| `Instagram Downloads/{collection}/` | ~50 GB | ✅ Original MP4s |
| `CONTENT_PROCESSING/frames/` | 7.9 GB | ⚠️ Regeneratable |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB | ⚠️ Regeneratable |
| `CONTENT_PROCESSING/analysis/` | 579 MB | ⚠️ Regeneratable |
| `CONTENT_PROCESSING/vault/` | **427 MB** | ✅ **MIGRATE** (346 MB notes + 81 MB embedded GIFs) |
| `CONTENT_PROCESSING/gifs/` | **45 GB** | ❌ **DELETE** (redundant, not linked to vault) |
| `VISION_PROGRESS.json` | 2.6 MB | ✅ **MIGRATE** |

#### What's on Internal (Already Safe)
| Path | Size | Status |
|------|------|--------|
| `~/.hermes/skills/davinci-resolve-techniques/` | ~50 MB | ✅ 1,449+ skills |
| `~/DaVinci_Vault/` (target) | ~427 MB | ✅ After migration |

#### Migration Commands (No Regeneration)
```bash
# 1. Copy vault to internal
cp -r "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/vault" ~/DaVinci_Vault

# 2. Copy progress tracking
cp "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json" ~/DaVinci_Vault/

# 3. Delete redundant gifs (45 GB)
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/gifs"

# 4. Optionally clean completed frames (keep only error/pending)
# Find completed video_ids from VISION_PROGRESS.json, remove their frame dirs

# 5. Verify internal skills already safe
ls ~/.hermes/skills/davinci-resolve-techniques/ | wc -l  # Should be 1449+
```

**Result:** Free ~54 GB on Samsung LED, keep all curated outputs on internal.

## Processing Metrics (2026-07-30 Session)

| Metric | Value |
|--------|-------|
| Latency per frame | 3-5s |
| Rate limit | 20 RPM (3.2s minimum) |
| Success rate | ~95% |
| Session throughput | ~15-20 videos |
| Phase 2c total | 1,146 videos |
| Complete this session | 236 (722→958) |
| Phase 2c progress | 958/1,146 (83.6%) |
| Pending | 47 |
| Errors | 142 |

## Error Categories

| Error Type | Handling |
|------------|----------|
| Solid color frames (no content) | Mark as error, skip |
| Blurry/abstract frames | Still produces technique, mark complete |
| Rate limit 429 | Wait 10s, retry once |
| Connection error | Retry once after 5s |
| Parse failure | Store raw response, mark error |

## Next Steps

1. Continue Phase 2c: Process remaining 267 pending videos
2. Phase 2d: Process remaining ~688 videos from other collections
3. Generate consolidated technique index across all skills
4. Rebuild Obsidian vault with updated frame references