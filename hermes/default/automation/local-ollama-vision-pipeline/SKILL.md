---
name: local-ollama-vision-pipeline
description: Local Ollama vision for rate-limit-free frame analysis.
trigger: Need local vision without rate limits
---

# Local Ollama Vision Pipeline

## Overview
Replace NVIDIA/cloud `vision_analyze` with a fully local Ollama vision model. The built-in `vision_analyze` tool is **hardcoded to NVIDIA vision** and cannot use local models. This skill provides a drop-in replacement via direct Ollama API calls.

## Model Selection

| Model | Size | RAM | Quality | Speed | Status |
|-------|------|-----|---------|-------|--------|
| `llava:7b` | 8.5 GB | ~9 GB | Good | ~10 sec/frame | ✅ **Recommended** |
| `gemma3:4b` | ~4 GB | ~5 GB | Good | ~8 sec/frame | ⚠️ Untested |
| `qwen3-vl:8b` | 15 GB | ~16 GB | Best | ~15 sec/frame | ❌ Too large for 16GB |
| `moondream:1.8b` | 1.8 GB | ~2 GB | Poor | ~5 sec/frame | ❌ Broken (returns "urn") |
| `qwen2.5-vl:3b` | ~3 GB | ~4 GB | Good | ~6 sec/frame | ❌ Not in registry |

**Rule:** On 16GB Mac, `llava:7b` is the only working model that fits alongside a text model.

## Setup

```bash
# Pull recommended model
ollama pull llava:7b

# Verify it works
curl -s http://localhost:11434/api/generate -d '{
  "model": "llava:7b",
  "prompt": "Describe this image",
  "images": ["<base64>"],
  "stream": false
}'
```

## Core Script: `local_vision_analyze.py`

Located at `/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`

### Usage
```bash
# Single frame
python3 local_vision_analyze.py /path/to/frame.jpg

# Frame directory (video) - analyzes up to N frames
python3 local_vision_analyze.py /path/to/frames_dir 5
```

### JSON Schema Output
```json
{
  "grading_style": "teal/orange|film look|log|S-Log3|Rec709|custom",
  "camera_movement": "static|dolly|gimbal|handheld|tripod|slider|drone|crane",
  "lighting": "key/fill ratio, soft/hard, natural, artificial, practical, mixed",
  "effects": ["transitions", "overlays", "text", "LUTs", "filters", "composites"],
  "color_temperature": "warm|cool|neutral|mixed",
  "contrast_level": "high|low|medium|flat/log",
  "saturation": "high|low|medium|desaturated",
  "notes": "DaVinci-relevant observations"
}
```

## Critical Implementation Details

### 1. Filter macOS Resource Forks
```python
# ALWAYS exclude ._* files
frame_files = sorted([f for f in Path(frame_dir).glob("*.jpg") if not f.name.startswith("._")])
```

### 2. Use Python 3.12+ (System Python 3.9 has urllib3 issues)
```bash
/opt/homebrew/bin/python3.12 local_vision_analyze.py ...
```

### 3. Extract JSON from llava's markdown wrapping
```python
if "```json" in response_text:
    response_text = response_text.split("```json")[1].split("```")[0].strip()
```

### 4. Batch Processing Pattern
```python
# Process in chunks of 10, save progress every 5
# ~35-45 sec/video (3 frames each)
# No rate limits - fully autonomous
```

## Integration with Instagram Reels Pipeline

1. **Frame extraction** → existing pipeline creates `/frames/{video_id}/frame_*.jpg`
2. **Local vision analysis** → `local_vision_analyze.py` processes frames
3. **Skill generation** → JSON output feeds existing skill generator
4. **Vault build** → existing vault builder creates notes

## Performance

| Metric | NVIDIA vision_analyze | Local llava:7b |
|--------|----------------------|----------------|
| Rate limit | 20 RPM | None |
| Speed | ~1 min/video | ~35-50 sec/video (3 frames sequential) |
| Speed (4 parallel) | N/A | ~150-200 sec/video (GPU contention) |
| Cost | API credits | Free (local) |
| Reliability | 100% | ~95% (occasional hallucination) |
| RAM | 0 | 8.5 GB |

## Batch Processing Pattern (validated this session)

```python
# In main session terminal:
cd /Users/alfredkamisese/vision_pipeline
/opt/homebrew/bin/python3.12 -c "
import json, time, sys
from pathlib import Path
sys.path.insert(0, '/Users/alfredkamisese/vision_pipeline')
from local_vision_analyze import analyze_video_frames
# ... process 5 videos at a time
"
# ~3-4 minutes per 5 videos
# Save VISION_PROGRESS.json every 5 videos
```

### Parallel Background Processing (validated 2026-07-31)

For large error backlogs, run multiple chunks in parallel using `terminal(background=true, notify_on_complete=true)`:

```bash
# Launch 3-4 parallel chunks (each ~25-30 min, total ~30 min vs 1.5 hrs sequential)
cd /Users/alfredkamisese/vision_pipeline

# Chunk 1 (error videos 0-38)
/opt/homebrew/bin/python3.12 batch_chunk.py "108,109,110,..." 1 &

# Chunk 2 (error videos 39-77)
/opt/homebrew/bin/python3.12 batch_chunk.py "331,332,335,..." 2 &

# Chunk 3 (error videos 78-115)
/opt/homebrew/bin/python3.12 batch_chunk.py "497,503,504,..." 3 &

# Chunk 4 (pending_vision videos)
/opt/homebrew/bin/python3.12 batch_chunk.py "1116,1117,1118,..." 4 &
```

**Script:** `scripts/batch_chunk.py` — processes a comma-separated list of VISION_PROGRESS.json indices.

Each chunk:
- Reads VISION_PROGRESS.json
- Processes its assigned video indices via local llava:7b
- Updates status in-place (writes back every video)
- Completes in ~25-30 min for 35-40 videos
- Uses `notify_on_complete=true` for automatic completion notification

This achieves **~3-4x speedup** over sequential processing.

### GPU Contention Warning

When running 4 parallel chunks, all hit llava:7b (100% GPU each) simultaneously → **~150-200 sec/video** vs ~45 sec sequential. 

**Recommendation:** Run max **2 parallel chunks** for optimal throughput, or accept slower per-video time for wall-clock speedup.

## Sub-Agent Limitation (confirmed this session)

**Sub-agents CANNOT run local vision pipeline.** They are text-only LLMs without:
- Terminal access
- Python execution
- Local Ollama API access
- Image processing capability

Only the **main Hermes session** can execute the pipeline.

## Pitfalls

1. **Don't use `vision_analyze` tool** — it ignores your provider config
2. **Don't use sub-agents for vision** — they can't access parent's vision model
3. **Filter ._* files** — macOS creates resource forks that cause 400 errors
4. **Use Python 3.12+** — system Python 3.9 has broken urllib3
5. **Monitor GPU memory** — llava:7b uses 100% GPU; don't run heavy GPU tasks concurrently
6. **Chunk size matters** — 5 videos/batch completes in ~3-4 min (under 600s timeout)

## Vault Structure Comparison & Migration (2026-07-31)

The current pipeline vault is INCOMPLETE compared to the existing `DaVinci_Knowledge_Base`:

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

---

## Session 2026-07-31 — Vault Reorganization, TamaZila Merge & Final Storage Cleanup

### Vault Reorganization (Flat → Domain Folders)

**Problem**: Pipeline vault had 1,023 techniques in flat `techniques/` folder with minimal cross-references.

**Solution**: Reorganization script moved techniques into domain folders based on `resolve_page` + `collection`:

| Domain Folder | Techniques | Source Mapping |
|---------------|------------|----------------|
| Color Grading & Looks | 865 | `resolve_page: Color` + various collections |
| Camera Theory | 5 | `resolve_page: Camera` + Camera collections |
| Lighting | 93 | `resolve_page: Lighting` + Ideas_for_Shooting_Videos |
| Fusion | 77 | `resolve_page: Fusion` + DR_Making_CG, DaVinci_Tricks |
| Photography_Videography | 2 | `resolve_page: Videography` |
| Post_Production | 98 | `resolve_page: Post/Video/Edit` + various |
| Video_Effects | 17 | `resolve_page: Video` + Video_Effects |

**Enhanced Frontmatter**: Each technique now includes:
- `domain: "Color Grading & Looks"` (auto-assigned)
- `moved_at: "2026-07-31"`
- `skill: "skill-filename.md"` (linked to Hermes skill)
- `analysis: "analysis/video_id/analysis.json"` (linked to vision analysis)

### Cross-Reference Generation

| Index | Files Created | Content |
|-------|---------------|---------|
| Tags | 472 | Alphanumeric tags only (filtered special chars) |
| Collections | 60 | Normalized (hyphenated, deduped apple_log/apple-log) |
| Skills | Linked in technique frontmatter | `skill: "skill-filename.md"` |
| Analysis | Linked in technique frontmatter | `analysis: "analysis/video_id/analysis.json"` |
| Media | Referenced in technique body | `![name](media/video_id_technique.gif)` |

### TamaZila Vault Merge (Internal Drive)

**Copied to `~/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`**:

| Source (Samsung LED) | Size | Destination |
|----------------------|------|-------------|
| `CONTENT_PROCESSING/vault/` | 427 MB | `DaVinci_Knowledge_Base/` |
| `~/.hermes/skills/davinci-resolve-techniques/` | 50 MB | `DaVinci_Knowledge_Base/skills/` (1,451 skills) |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB | `DaVinci_Knowledge_Base/transcripts/` |
| `CONTENT_PROCESSING/analysis/` | 14 MB | `DaVinci_Knowledge_Base/analysis/` |
| `CONTENT_PROCESSING/VISION_PROGRESS.json` | 2.6 MB | `DaVinci_Knowledge_Base/` |

**Total**: ~2.5 GB added to TamaZila vault (now ~1.5 GB on internal drive).

### Samsung LED Cleanup (54 GB Freed)

| Deleted | Size | Reason |
|---------|------|--------|
| `CONTENT_PROCESSING/gifs/` | 45 GB | Redundant — vault has 81 MB in `media/` |
| `CONTENT_PROCESSING/frames/` (1,030 complete) | 7.4 GB | Keep only 135 error/pending |
| `CONTENT_PROCESSING/vault/` | 427 MB | Merged to TamaZila |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB | Merged to TamaZila |
| `CONTENT_PROCESSING/analysis/` | 579 MB | Merged to TamaZila |
| `~/Downloads/instagram_downloads/` | 407 MB | Duplicate of Samsung LED |
| `~/Downloads/instagram-tamazila-...` | 28 MB | Old export |

**Result**: Samsung LED from 96% full (5.4 GB free) → 50% full (61 GB free)

### 430 Missing Vault Notes Generated

**Problem**: 1,030 complete videos had vision analysis + skills, but only ~600 had vault notes.

**Solution**: Batch generation script (`generate_vault_notes.py`):
- Reads `VISION_PROGRESS.json` for `status: complete`
- Checks vault for existing `video_id` in frontmatter
- Generates GIFs via ffmpeg (5-10 frames, ~1-3 sec/video)
- Creates technique notes with frontmatter, node graph, parameters, steps
- Links to existing skills in `~/.hermes/skills/davinci-resolve-techniques/`
- Outputs to `vault/techniques/` and `vault/media/`

**Results**: 430 notes created in ~5 minutes (2,046 total including duplicates), 1,005/1,030 complete videos now have vault notes.

### Remaining Work

| Category | Count | Status |
|----------|-------|--------|
| Error videos | 116 | Frames exist, need vision analysis |
| Pending vision | 19 | Frames exist, need vision analysis |
| **Total remaining** | **135** | Frames ready on Samsung LED |

Ready for next session: local llava:7b vision analysis on 135 videos.

### 5. Static Image Analysis (Posters, Photos, Graphics)

The pipeline works for **single static images** (not just video frames):

```bash
# Analyze a poster, photo, or graphic
/opt/homebrew/bin/python3.12 local_vision_analyze.py /path/to/image.jpg
```

**Use case**: Analyze reference posters to extract style, composition, color palette, typography cues — then feed into `baoyu-infographic` for prompt generation.

**Example output** for a Hawaiian festival poster:
```json
{
  "grading_style": "custom",
  "camera_movement": "static",
  "lighting": "mixed",
  "effects": ["transitions", "text", "filters"],
  "color_temperature": "warm",
  "contrast_level": "medium",
  "saturation": "high",
  "notes": "Vibrant tropical poster with warm tone, high saturation, text overlays, retro travel poster aesthetic"
}
```

This output directly informs `retro-pop-grid` style selection and color palette choices in the infographic skill.

## References

- `references/parallel-background-processing.md` — Parallel chunk execution
- `references/ollama-vision-models.md` — Model comparison & selection
- `references/vault-structure-comparison-and-migration.md` — Vault migration details
- `references/session-2026-07-31-local-vision-storage-cleanup.md` — Storage cleanup log
- `references/daVinci-prompt-schema.md` — DaVinci JSON output schema
- `references/static-image-analysis.md` — Single static image analysis (posters, photos, graphics)