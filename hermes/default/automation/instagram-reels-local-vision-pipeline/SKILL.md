---
name: instagram-reels-local-vision-pipeline
description: Process Instagram Reels for DaVinci with local llava:7b.
---

# Instagram Reels → DaVinci Pipeline (Local Vision)

Complete pipeline for processing Instagram Reels into DaVinci Resolve techniques using local llava:7b vision via Ollama (no rate limits, ~45s/video).

## Pipeline Overview

```
Instagram Reels → yt-dlp → MP4s → Frame Extraction → Local Vision (llava:7b) → Technique JSON → Skill Generation → Vault Notes → Index Updates
```

## Key Components

### 1. Frame Extraction
- Tool: ffmpeg (1 frame/second)
- Location: `CONTENT_PROCESSING/frames/{video_id}/`
- Output: JPG frames for vision analysis

### 2. Local Vision Analysis (llava:7b)
- Model: llava:7b via Ollama (localhost:11434)
- Speed: ~45s/video (3 frames)
- No rate limits (vs NVIDIA 20 RPM)
- Script: `~/vision_pipeline/local_vision_analyze.py`

### 3. Vision Analysis Output
- Schema: grading_style, camera_movement, lighting, effects, color_temperature, contrast_level, saturation, notes
- Output: JSON per video in VISION_PROGRESS.json

### 4. Skill Generation
- Output: 1,449+ Hermes skills in `~/.hermes/skills/davinci-resolve-techniques/`
- Each skill: frontmatter + markdown with node graph, parameters, steps

### 5. Vault Building
- Notes: 963 techniques in 7 domain folders
- GIFs: 405 valid GIFs in `media/` (643 empty removed)
- MASTER_MAPPING.md: Single source of truth

### 6. Index Management
- 130+ index files updated to reference MASTER_MAPPING.md
- Support folder indexes: analysis, media, skills, collections, tags, transcripts
- Domain folder indexes: 7 domain folders

## Pipeline Scripts (in ~/vision_pipeline/)

| Script | Purpose |
|--------|---------|
| `local_vision_analyze.py` | Core vision analysis via Ollama API |
| `batch_process_local_vision.py` | Batch process videos with local vision |
| `regenerate_mappings.py` | Regenerate all mapping files |
| `update_all_indexes.py` | Update all 130 index files |
| `create_master_mapping.py` | Create MASTER_MAPPING.md |
| `create_support_indexes.py` | Create support folder indexes |
| `create_domain_indexes.py` | Create domain folder indexes |
| `clean_support_indexes.py` | Clean index files |
| `reorganize_vault.py` | Reorganize vault structure |
| `batch_chunk.py` | Batch processing helper |
| `generate_vault_notes.py` | Generate vault notes |

## Pipeline Status (Current)

| Metric | Value |
|--------|-------|
| Total Videos | 1,165 |
| Complete | 1,030 (88%) |
| Errors | 116 |
| Pending | 19 |
| Local Vision Processed | 45+ |
| Skills Generated | 1,449+ |
| Vault Notes | 963 |
| Valid GIFs | 405 |

## Critical Learnings

### 1. Local Vision Works
- llava:7b via Ollama: 45s/video, no rate limits
- Sub-agents CANNOT run vision pipeline (no terminal/Python access)
- Only main session can run vision pipeline

### 2. Empty GIF Problem
- 643/1048 GIFs were empty (61%)
- Cause: ffmpeg failures during generation
- Solution: Delete empty, regenerate from frames if needed

### 3. MASTER_MAPPING.md is Source of Truth
- All 130+ index files updated to reference MASTER_MAPPING.md
- Memory.md and index.md deleted (merged into MASTER_MAPPING.md)
- Hero_index.md updated to point to MASTER_MAPPING.md

### 4. Pipeline Engine Location
- Active scripts: `~/vision_pipeline/` (10 scripts)
- Old pipeline files in ~/ cleaned up (~100 files removed)

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Sub-agent vision timeout | Only main session can run vision |
| Empty GIFs generated | Check file size, delete 0-byte files |
| Index files reference Memory.md | Update all to MASTER_MAPPING.md |
| Sub-agents can't run Python | Only main session has terminal access |
| Rate limits on NVIDIA | Use local llava:7b instead |

## Maintenance Commands

```bash
# Regenerate all mapping files
cd ~/vision_pipeline && python3 regenerate_mappings.py

# Create domain folder indexes
python3 create_domain_indexes.py

# Create support folder indexes
python3 create_support_indexes.py

# Clean support indexes
python3 clean_support_indexes.py

# Process vision batch
python3 batch_process_local_vision.py
```

## File Structure

```
~/vision_pipeline/           # Pipeline engine (10 scripts)
~/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
├── MASTER_MAPPING.md        # Single source of truth
├── analysis/                # 1,156 video analyses
├── media/                   # 405 valid GIFs
├── skills/                  # 1,449 Hermes skills
├── collections/             # 39 collections
├── tags/                    # 472 tags
├── transcripts/             # 1,121 transcripts
├── Color Grading & Looks/   # 854 techniques
├── Camera Theory/           # 5 techniques
├── Lighting/                # 2 techniques
├── Fusion/                  # 75 techniques
├── Photography_Videography/ # 1 technique
├── Post_Production/         # 98 techniques
├── Video_Effects/           # 7 techniques
└── Videographer/            # 365 notes
```

## References
- `references/vision_pipeline_architecture.md` — Pipeline architecture details
- `references/local_vision_troubleshooting.md` — Common issues and fixes
- `references/index_update_protocol.md` — How to update all indexes

## Templates
- `templates/technique_note.md` — Technique note template
- `templates/skill_frontmatter.yaml` — Skill frontmatter template
- `templates/domain_index.md` — Domain folder index template

## Scripts
- `scripts/validate_gifs.py` — Validate GIF files
- `scripts/update_master_mapping.py` — Update MASTER_MAPPING.md
- `scripts/clean_empty_gifs.py` — Remove empty GIFs
---
category: automation
tags: ["instagram", "reels", "davinci-resolve", "pipeline", "local-vision", "llava", "ollama", "automation"]
---