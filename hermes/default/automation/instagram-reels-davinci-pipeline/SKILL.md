---
name: instagram-reels-davinci-pipeline
description: "Use for Instagram Reels to DaVinci pipeline: 5 phases."
category: automation
trigger: "Use for Instagram Reels to DaVinci pipeline: 5 phases."
---

# Instagram Reels to DaVinci Resolve Pipeline

Complete workflow for converting Instagram Reels into DaVinci Resolve techniques with Hermes skills and Obsidian vault.

## Architecture Overview

```
Phase 1: Download (yt-dlp) to Phase 2: Frame Extraction (ffmpeg)
    to
Phase 3: Vision Analysis (NVIDIA Gemini) to Phase 4: Skill Authoring (Python)
    to
Phase 5: Vault Build (Python) to Phase 6: Skill Install (Hermes)
```

## Phase Details

### Phase 1: Download
- Tool: `yt-dlp` with Instagram cookies
- Output: Raw MP4 files in collection folders
- Status: Complete for 1,146 Cinematic/Shooting + ~688 other collections

### Phase 2: Frame Extraction
- Tool: `ffmpeg` extracts 1-5 frames per video
- Pattern: `/CONTENT_PROCESSING/frames/<VIDEO_ID>/frame_XXXX.jpg`
- Status: Complete for all 1,834+ videos (0 missing frames)

## Critical Finding: vision_analyze Uses Parent's NVIDIA Model, NOT Sub-Agent Config (2026-07-30)

**THE ROOT CAUSE OF SUB-AGENT FAILURES:**

The `vision_analyze` tool uses the **parent assistant's built-in NVIDIA vision model (Gemini)**, NOT the sub-agent's configured LLM. Sub-agents inherit text LLM configuration only — they **cannot access the parent's vision tool**.

### Failed Architecture (6× 600s timeouts, 1 API call each)
```yaml
# Sub-agent config - IRRELEVANT for vision
delegation:
  provider: ollama-launch     # Local Ollama - crashes M4 16GB with OOM
  model: qwen3.5-64k
  child_timeout_seconds: 600
  max_concurrent_children: 6  # 6 × 3-4GB = 18-24GB > 16GB RAM
```

**Result:** 6 parallel sub-agents launched, all timed out at 600s with only 1 API call completed. Local Ollama cannot proxy NVIDIA vision_analyze calls in sub-contexts.

### Why Even Cloud Sub-Agents Won't Work for Vision
Even with `ollama-cloud` provider, sub-agents would inherit the cloud **text** LLM but **cannot access the parent's vision_analyze tool**. The vision tool is a built-in capability of the main assistant model, not a configurable provider.

### Only Working Architecture: Manual Main Session
```python
# Main session loop (ONLY reliable path)
for video in pending_videos:
    frame = f"/Volumes/.../frames/{video}/frame_0001.jpg"
    result = vision_analyze(image_url=frame, question=VISION_PROMPT)
    # Parse JSON, update progress, write skill + vault note
    time.sleep(3.2)  # 20 RPM NVIDIA limit
```

### User Correction (2026-07-30)
> "Never run delegate tasks like that using a local ollama model as it hit OOM and crash my Mac mini"

**This applies to ALL local model sub-agents for vision tasks.** The only working path is **manual sequential processing in the main session**.

## Phase 3: Vision Analysis (CRITICAL PATH - Updated)

### Phase 4: Skill Authoring
- Script: `generate_skills.py` reads `VISION_PROGRESS.json`
- Output: SKILL.md files in `~/.hermes/skills/davinci-resolve-techniques/`
- Format: Technique clusters with node graphs, parameters, steps, tags
- Current: 1,449 skills generated

### Phase 5: Vault Build
- Script: `build_vault.py` creates Obsidian vault
- Output: 651 technique notes with embedded GIFs
- Structure: techniques/, collections/, tags/, media/, index.md
- Cross-links: `[[Collection]]`, `[[#tag]]`

### Phase 6: Skill Install
- Copy to `~/.hermes/skills/davinci-resolve-techniques/`
- Hermes auto-loads on restart

## Critical Configuration

```yaml
# ~/.hermes/config.yaml
vision:
  provider: google-gemini
  model: gemini-2.5-flash
  # NEW: Local vision fallback (llava:7b via Ollama)
  local_fallback:
    enabled: true
    model: "llava:7b"
    api_url: "http://localhost:11434/api/generate"
    frames_per_video: 3

delegation:
  max_concurrent_children: 6
  child_timeout_seconds: 300
  provider: ollama-cloud  # for sub-agent text tasks

providers:
  google-gemini:
    api_key: <from env>
  ollama:
    api_url: "http://localhost:11434"
```

## Phase 3: Vision Analysis — Dual Path (Updated 2026-07-31)

### Path A: NVIDIA Vision (Primary — rate limited)
- Tool: Built-in `vision_analyze` → NVIDIA Gemini
- Rate limit: 20 RPM (~1 min/video)
- Use for: Initial batches, quality-critical reels

### Path B: Local llava:7b (Secondary — no rate limits)
- Tool: Custom script `/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`
- Model: `llava:7b` via Ollama API (`localhost:11434`)
- Speed: ~35-50 sec/video (3 frames sequential)
- **No rate limits** — fully autonomous
- GPU: 100% GPU per process (~8.5 GB RAM)
- **Critical**: Max 2 parallel processes (GPU contention → 150-200 sec/video at 4 parallel)

### Local Vision Batch Processing (Validated 2026-07-31)

```bash
# Sequential (optimal per-video, ~45 sec/video)
cd /Users/alfredkamisese/vision_pipeline
/opt/homebrew/bin/python3.12 batch_chunk.py "108,109,110,..." 1

# Parallel background (wall-clock speedup, ~150-200 sec/video at 4x)
# Use terminal(background=true, notify_on_complete=true)
# Max 2 recommended to avoid GPU contention

# Script: batch_chunk.py processes comma-separated VISION_PROGRESS.json indices
# Updates status in-place, writes every 5 videos, notify_on_complete
```

### Sub-Agent Limitation (Confirmed)

**Sub-agents CANNOT run local vision pipeline.** They are text-only LLMs without terminal/Python/Ollama access. Only the main Hermes session can execute the pipeline.

## Session 2026-07-31 — Local Vision Pipeline & Storage Crisis Resolution

### Local llava:7b Pipeline Operational

| Metric | NVIDIA vision_analyze | Local llava:7b |
|--------|----------------------|----------------|
| Rate limit | 20 RPM | **None** |
| Speed | ~1 min/video | ~35-50 sec/video (3 frames) |
| Cost | API credits | **Free** |
| RAM | 0 | 8.5 GB |
| Max parallel | 1 | 2 (GPU contention at 4x) |

**Scripts created**: `local_vision_analyze.py`, `batch_chunk.py` (parallel background chunks)

### 430 Missing Vault Notes Generated (5 min)

**Problem**: 1,030 complete videos had vision/skills — only ~600 had vault notes.

**Solution**: `generate_vault_notes.py` batch script:
- Reads `VISION_PROGRESS.json` for complete videos
- Finds frames in `CONTENT_PROCESSING/frames/` + `PROCESSING/frames/`
- Generates GIFs via ffmpeg (~1-3 sec/video)
- Creates notes with frontmatter, node graph, parameters, steps
- Links to skills in `~/.hermes/skills/davinci-resolve-techniques/`
- **430 notes in ~5 minutes** (formatting only, no vision)

### GPU Contention with Parallel Processing

| Parallel Chunks | Time/Video | Wall Time (35-40 videos) |
|----------------|------------|--------------------------|
| 1 (sequential) | ~45 sec | ~25-30 min |
| 4 (parallel) | ~150-200 sec | ~25-30 min |

**Recommendation**: Max **2 parallel chunks** for optimal throughput.

### Storage Crisis Resolved (2026-07-31)

| Drive | Before | After | Action |
|-------|--------|-------|--------|
| Samsung LED | 96% full (5.4 GB) | ~58 GB free | Deleted `gifs/` (45 GB) + completed `frames/` (~6 GB) |
| Internal | 83% full (2.5 GB) | ~8 GB free | Deleted `~/Downloads/instagram_downloads/` (407 MB) + old export (28 MB) |

**Duplicate confirmed**: `~/Downloads/instagram_downloads/` = byte-for-byte duplicate of Samsung LED (407 MB freed)

### Pipeline Status (2026-07-31)

| Phase | Status |
|-------|--------|
| Phase 1-2 (Download + Frames) | ✅ 1,834+ videos |
| Phase 3a (NVIDIA vision) | ✅ 1,030 complete |
| Phase 3b (Local vision) | 🔄 135 remaining (116 error + 19 pending) |
| Phase 4 (Skills) | ✅ 1,449+ skills |
| Phase 5 (Vault) | ✅ 1,005 notes (430 added) + 81 MB GIFs |

### Next: Merge to TamaZila DaVinci_Knowledge_Base

**Plan**: Copy `vault/` (427 MB) + `VISION_PROGRESS.json` + `transcripts/` + `analysis/` to `~/TamaZila.../DaVinci_Knowledge_Base/`, merge with existing structure, eject Samsung LED.

---

## Session 2026-07-31 (Part 2) — Vault Merge, Index Updates & Hero_index.md Integration

### Vault Merge Complete (Samsung LED → TamaZila Obsidian Vault)

**Merged Pipeline Outputs to TamaZila Vault:**

| Data | Size | Location |
|------|------|----------|
| Techniques | 963 notes in 7 domain folders | `DaVinci_Knowledge_Base/` domain folders |
| Skills | 1,449 | `skills/` + `~/.hermes/skills/` |
| Analysis | 1,165 video dirs | `analysis/` |
| Media | 2,096 GIFs | `media/` |
| Transcripts | 6,699 files | `transcripts/` |
| Tags | 907 tag files | `tags/` |
| Collections | 58 collection files | `collections/` |
| VISION_PROGRESS.json | 2.6 MB | Root |

### Domain Folder Organization (963 Techniques)

| Domain Folder | Count | Source Collections |
|---------------|-------|-------------------|
| Color Grading & Looks | 854 | Color, DaVinci_Tricks, etc. |
| Camera Theory | 5 | Camera, Cinematic |
| Lighting | 2 | Lighting |
| Fusion | 75 | Fusion, DaVinci_Tricks |
| Photography_Videography | 1 | Videography |
| Post_Production | 98 | Post, Export |
| Video_Effects | 7 | Video_Effects |

### Each Technique Note Updated With:
- `domain: "Folder Name"` 
- `moved_at: "2026-07-31"`
- `skill: "skill_filename.md"` (linked to Hermes skill)
- `analysis: "analysis/video_id/analysis.json"`

### Support Folder Indexes Created (All with `index.md`):

| Folder | Index | Entries |
|--------|-------|---------|
| `analysis/` | `index.md` | 1,156 videos |
| `media/` | `index.md` | 2,096 GIFs |
| `skills/` | `index.md` | 1,449 skills |
| `collections/` | `index.md` | 39 collections |
| `tags/` | `index.md` | 472 tags |
| `transcripts/` | `index.md` | 1,121 transcripts |

### MASTER_MAPPING.md — Single Source of Truth
**Created** `MASTER_MAPPING.md` (237 lines) combining:
- Architectural hierarchy from Memory.md
- Disk inventory from index.md  
- All 6 support folder index references
- Domain folder technique counts
- Cross-reference map (technique↔skill↔analysis↔media↔tags↔collections)
- Pipeline tracking (VISION_PROGRESS.json structure)
- Maintenance commands & quick navigation

**Deleted**: `Memory.md` and `index.md` (replaced by MASTER_MAPPING.md)

### Index Files Updated: **130/130**
All index/mapping files updated to reference `MASTER_MAPPING.md` instead of `Memory.md`/`index.md`:
- 7 domain folder indexes
- 93 Lighting video-specific indexes
- 16 Videographer subfolder indexes
- 8 Color Grading subfolder indexes
- 6 support folder indexes
- Root-level files (CROSS_REFERENCE_INDEX.md, MASTER_SUMMARY.md)

### Hero_index.md Updated (Vault Root)
All DaVinci Knowledge Base references updated:
| Location | Before | After |
|----------|--------|-------|
| Quick Navigation table | `Memory.md` | `MASTER_MAPPING.md` |
| Folder structure tree | `Memory.md` | `MASTER_MAPPING.md` |
| Cross-Reference Documents | `Memory.md` | `MASTER_MAPPING.md` |
| Quick Actions | `Memory.md` | `MASTER_MAPPING.md` |

### Samsung LED Cleanup Complete
| Deleted | Size Freed |
|---------|------------|
| `gifs/` | 45 GB |
| `frames/` (1,030 complete videos) | ~7.4 GB |
| `vault/`, `transcripts/`, `analysis/`, `VISION_PROGRESS.json` | ~2.5 GB |
| `~/Downloads/instagram_downloads/` (duplicate) | 407 MB |
| Internal caches (pip, ms-playwright, GeminiMacOS) | ~1 GB |
| **Total** | **~55+ GB** |

### Remaining Work
**135 videos** (116 error + 19 pending) with frames ready on Samsung LED — ready for local llava:7b pipeline.

## Known Pitfalls

1. **Sub-agents + local Ollama = FAIL**: Vision calls route to parent's NVIDIA model, not accessible in sub-contexts
2. **Rate limits**: 20 RPM vision API - batch manually or accept 1/min pace
3. **SSD at 95%**: Clean temp frames after vision (`cleanup=true` default)
4. **Sub-agent timeout**: Reduced to 300s after 600s failures
5. **Syntax errors**: Python `from pathlib of Path` typo caught multiple times

## Scripts

### generate_skills.py
Reads `VISION_PROGRESS.json`, creates SKILL.md files with:
- Frontmatter: name, description, tags, difficulty, resolve_page
- Body: node graph, parameters, steps, source reel ID

### build_vault.py
Creates Obsidian vault with:
- One `.md` per technique with embedded GIF
- Collection indexes, tag indexes, master index
- Cross-links via `[[Collection]]`, `[[#tag]]`

## Progress Tracking

`VISION_PROGRESS.json` format:
```json
{
  "video_id": "C7tsJIhIdgC",
  "status": "complete|pending|error",
  "result": {technique JSON},
  "updated_at": "ISO timestamp"
}
```

Query progress:
```bash
python -c "
import json
from pathlib import Path
p = Path('.../VISION_PROGRESS.json')
data = json.load(open(p))
complete = sum(1 for v in data if v.get('status') == 'complete')
pending = sum(1 for v in data if v.get('status') == 'pending')
error = sum(1 for v in data if v.get('status') == 'error')
print(f'Complete: {complete}, Pending: {pending}, Error: {error}')
print(f'Progress: {complete/1146*100:.1f}%')
"
```

## Current Status (as of session)
- Phase 2c (Cinematic/Shooting): 906/1,146 complete (79%)
- Phase 2d (Other collections): ~688 pending
- Downstream: Skills + Vault ready for incremental updates

## Resuming Work

1. Check pending: `python -c "..."` (see above)
2. Process next batch manually via `vision_analyze`
3. Run `generate_skills.py` + `build_vault.py` after batch
4. Repeat until complete

## References

- `references/generate_skills.py` - Skill generation script
- `references/build_vault.py` - Vault build script
- `references/VISION_PROGRESS.json` - Progress tracking
- `templates/skill_template.md` - SKILL.md template