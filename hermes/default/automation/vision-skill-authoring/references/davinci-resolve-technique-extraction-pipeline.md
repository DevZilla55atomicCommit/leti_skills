# DaVinci Resolve Technique Extraction Pipeline (Post-Download)

## Overview

After Instagram Reels are downloaded via the main pipeline, this workflow extracts DaVinci Resolve techniques from the video content using AI vision analysis, creates searchable Hermes skills, and builds an Obsidian knowledge vault.

## Pipeline Architecture

```
Instagram Reels (MP4) → Frame Extraction → Vision Analysis → Skill Generation → Obsidian Vault
```

## Phase 1: Frame Extraction (Completed)

- **Tool**: ffmpeg via `process_block_a_v2.py` / `process_local_files.py`
- **Frames per video**: 8 frames at 0%, 14%, 28%, 42%, 57%, 71%, 86%, 99.9%
- **Status**: ✅ Complete for all 1,165 videos
- **Location**: `/Volumes/Samsung LED/Instagram Downloads/.../CONTENT_PROCESSING/frames/{CODE}/frame_00.png` through `frame_07.png`

## Phase 2: Vision Analysis (In Progress)

### Tool: NVIDIA `vision_analyze` (Google/DiffusionGemma via NVIDIA)

```python
# Single call pattern
vision_analyze(
    image_url="/Volumes/Samsung LED/.../frames/CODE/frame_0001.jpg",
    question="Analyze this DaVinci Resolve technique... Return JSON with technique_name, resolve_page, node_graph_type, key_nodes, parameters, steps_to_reproduce, difficulty, tags"
)
```

### Performance
- **Speed**: ~3-5 seconds per call
- **Batch size**: Sequential (one at a time due to rate limits)
- **Model**: `google/diffusiongemma-26b-a4b-it` via NVIDIA NIM
- **Provider**: NVIDIA (not local Ollama - qwen3-vl:8b times out at 60s on 16GB M4)

### Current Progress (2026-07-28)
| Phase | Complete | Pending | Errors | Total |
|-------|----------|---------|--------|-------|
| Cinematic/Shooting | 482 | 582 | 82 | 1,165 |

### Output Format
Each analysis produces structured JSON:
```json
{
  "technique_name": "Teal and Orange Cinematic Grade",
  "resolve_page": "Color",
  "node_graph_type": "serial",
  "key_nodes": ["Primary Wheels", "Qualifier Mask", "Glow Node"],
  "parameters": {"Contrast": "High", "Saturation": "Boosted"},
  "steps_to_reproduce": ["Step 1...", "Step 2..."],
  "difficulty": "intermediate",
  "tags": ["cinematic", "teal-and-orange", "color-grading"]
}
```

### Storage
Results appended to `VISION_PROGRESS.json`:
```json
{
  "video_id": "C7JtgxmxumW",
  "status": "complete",
  "result": { ... },
  "updated_at": "2026-07-28T..."
}
```

## Phase 3: Skill Generation (Partially Complete)

### Current Approach
- **Sub-agents**: 6 parallel via Ollama Cloud (gemma4:31b-cloud) - TIMEOUT at 300s
- **Better approach**: Single Python script processing all 480+ completed analyses
- **Skills created**: 135+ in `~/.hermes/skills/davinci-resolve-techniques/`

### Skill Structure
```markdown
---
name: "Color - Teal & Orange Grading"
description: "12 related techniques for Color page teal-and-orange grading"
trigger: "Need Color page technique for teal-and-orange grading"
category: "Color"
tags: ["cinematic", "teal-and-orange", "color-grading", "masking"]
---

# Teal & Orange Grading (Color)

## Overview
Combined 12 techniques from Instagram Reels for Color page.

## Resolve Page
Color

## Node Graph Type
serial

## Key Nodes
- Primary Wheels
- Qualifier Mask
- Glow Node
- Color Wheels

## Parameters
- Contrast: High
- Saturation: Boosted highlights
- Glow Threshold: 0.45

## Steps to Reproduce
1. Apply primary grade to balance exposure...
2. Use Qualifier to select skin tones...
...

## Difficulty
intermediate

## Tags
cinematic, teal-and-orange, color-grading, masking
```

### Clustering Logic
Group by: `resolve_page` + primary `tag` + `node_graph_type`

## Phase 4: Obsidian Vault (Complete)

### Location
`/Users/alfredkamisese/Obsidian/DaVinci-Techniques/`

### Structure
```
DaVinci-Techniques/
├── techniques/          # 81 category notes
│   ├── cinematic.md
│   ├── color-grading.md
│   ├── masking.md
│   └── ...
├── index/
│   └── MASTER_INDEX.md  # Master table with links
├── skills/              # (empty - skills in Hermes)
└── frames/              # (empty - frames in skills)
```

### Master Index
Markdown table with wiki-links to category notes:
```markdown
| Category | Count | Page |
|----------|-------|------|
| [[techniques/cinematic]] | 63 | Color |
| [[techniques/color-grading]] | 23 | Color |
| [[techniques/masking]] | 12 | Color|Fusion |
```

## Configuration

### Hermes Config (`~/.hermes/config.yaml`)
```yaml
model:
  provider: nvidia
  default: nvidia/nemotron-3-ultra-550b-a55b
  api_key: nvapi-...

auxiliary:
  vision:
    provider: nvidia
    model: google/diffusiongemma-26b-a4b-it

delegation:
  provider: ollama-cloud
  model: gemma4:31b-cloud
  max_concurrent_children: 6
  child_timeout_seconds: 300
```

## Key Learnings

### 1. Vision Provider Selection
| Provider | Model | Speed | Works? |
|----------|-------|-------|--------|
| NVIDIA | google/diffusiongemma-26b-a4b-it | 3-5s | ✅ |
| Local Ollama | qwen3-vl:8b | 60s timeout | ❌ OOM on 16GB |
| Ollama Cloud | No vision models | N/A | ❌ |

### 2. Sub-Agent Timeout Issue
- **Problem**: 18 sub-agents dispatched, all timed out at 300s
- **Cause**: File I/O + API calls exceed timeout
- **Fix**: Use single Python script for skill generation (no sub-agents)

### 3. Rate Limiting
- NVIDIA vision API has rate limits (~20 RPM)
- Sequential processing required
- 480 analyses × 4s = ~32 minutes (manageable)

### 4. Frame Extraction Already Done
- All 1,165 videos have frames extracted
- Vision analysis is the only remaining bottleneck
- Can run overnight via cron

## Automation

### Cron Job (3am Daily)
```bash
0 3 * * * /Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python /Users/alfredkamisese/vision_cron_job.py >> /Users/alfredkamisese/vision_cron.log 2>&1
```
Processes 20 frames per run.

### Manual Batch
```bash
# Process next 50
for i in {1..50}; do
  # Get next pending from VISION_PROGRESS.json
  # Run vision_analyze
  # Update progress
done
```

## Next Steps

1. **Complete vision analysis** - ~580 remaining (overnight via cron)
2. **Run skill generation script** - Single Python process on all 1,165 results
3. **Refresh skills in Hermes** - `hermes skills reload` or restart
4. **Extend vault** - Add remaining techniques to category notes
5. **DaVinci MCP integration** - Link techniques to actual Resolve node graphs