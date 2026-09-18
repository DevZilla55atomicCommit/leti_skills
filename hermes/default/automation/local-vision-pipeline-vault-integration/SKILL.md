---
name: local-vision-pipeline-vault-integration
description: Use local Ollama llava:7b for video batch vision and merge.
category: automation
tags: [ollama, llava, vision, daVinci, obsidian, vault, pipeline, batch-processing]
---

# Local Vision Pipeline → Vault Integration

**Trigger**: When you need to process video/image batches with vision analysis without cloud rate limits, and merge results into an organized Obsidian vault with cross-referenced mapping.

**Core Pattern**: Local Ollama (llava:7b) → Parallel background terminal processes → Domain-organized vault → MASTER_MAPPING.md

---

## 1. Local Vision Setup (llava:7b via Ollama)

### Prerequisites
```bash
# Pull model (once)
ollama pull llava:7b  # ~8.5 GB, 100% GPU

# Verify
ollama ps  # Should show llava:7b loaded
```

### Vision Analysis Script (`vision_pipeline/local_vision_analyze.py`)
```python
# Key points:
# - Uses Ollama API: http://localhost:11434/api/generate
# - Model: "llava:7b"
# - Input: base64 encoded image
# - Output: Structured JSON (grading_style, camera_movement, lighting, effects, etc.)
# - Timeout: 180s per call
# - Temperature: 0.1 for consistent JSON
```

**Performance**: ~40-50 sec/video (3 frames), no rate limits vs NVIDIA 20 RPM (~1 min/video)

---

## 2. Parallel Batch Processing

### Architecture
- **Main session**: Coordinates, monitors, merges results
- **Background terminal processes**: Run `batch_chunk.py` on disjoint video chunks
- **Each process**: Independent, writes to shared `VISION_PROGRESS.json`

### Launch Pattern
```bash
# Split video IDs into N chunks
# Launch N background processes
terminal(background=true, notify_on_complete=true, command="
  cd /path/to/vision_pipeline && 
  /opt/homebrew/bin/python3.12 batch_chunk.py 'vid1,vid2,...' chunk_N
")
```

### Monitoring
```bash
process(action='list')  # Check status
process(action='poll', session_id='...')  # Check output
```

**Critical**: Sub-agents CANNOT run this — they lack terminal/Python/Ollama API access. Only main session background processes work.

---

## 3. Vault Organization (Domain Folders)

### Domain Mapping
| resolve_page + collection | Domain Folder |
|---------------------------|---------------|
| Color + Color_grading | Color Grading & Looks |
| Camera + Camera | Camera Theory |
| Fusion + Fusion | Fusion |
| Lighting + Lighting | Lighting |
| Post + Post_Production | Post_Production |

### Technique Note Frontmatter
```yaml
---
title: "Technique Name"
video_id: "REEL_ID"
collection: "Collection_Name"
resolve_page: "Color|Fusion|Edit"
node_graph: "serial"
difficulty: "intermediate"
tags: ["tag1", "tag2"]
source_reel: "REEL_ID"
domain: "Domain Folder Name"
moved_at: "2026-07-31"
skill: "skill_filename.md"
analysis: "analysis/REEL_ID/analysis.json"
---
```

### Cross-References in Note Body
- **Skill**: `skill: "skill_filename.md"` → `skills/skill_filename.md`
- **Analysis**: `analysis: "analysis/REEL_ID/analysis.json"`
- **Media**: `![name](media/gif_name.gif)`
- **Tags**: `[[#tag]]` → `tags/tag.md`
- **Collection**: `[[Collection]]` → `collections/collection.md`

---

## 4. MASTER_MAPPING.md (Single Source of Truth)

### Structure
1. **Vault Statistics** — Counts of all assets
2. **Architectural Hierarchy** — From Memory.md (15 categories, sub-categories, Videographer pipeline)
3. **Domain Folders** — Technique counts per domain folder
4. **Support Folders** — 6 folders with index.md mappings
5. **Other Folders** — Reference/Archive categorized
4. **Cross-Reference Map** — Technique↔Skill↔Analysis↔Media↔Tags↔Collections
5. **Pipeline Tracking** — VISION_PROGRESS.json structure
5. **Maintenance Commands** — Regeneration scripts
6. **Quick Navigation** — 15 common tasks with file paths
6. **Status Legend** — ✅ Active, 📦 Reference, 📦 Archive, ⚠️ Note

### Regeneration
```bash
cd /Users/alfredkamisese/vision_pipeline
python3 regenerate_mappings.py      # knowledge_base_export.json/.csv, skills_export.json/.csv
python3 create_domain_indexes.py    # Domain folder index.md files
python3 create_support_indexes.py   # Support folder index.md files
python3 clean_support_indexes.py    # Clean malformed entries
python3 create_master_mapping.py    # MASTER_MAPPING.md
```

---

## 5. Storage Cleanup Patterns

### Samsung LED (External)
```bash
# Safe to delete (regeneratable)
rm -rf CONTENT_PROCESSING/gifs/           # 45 GB
rm -rf CONTENT_PROCESSING/frames/         # Keep only error/pending frames

# Keep (source of truth)
CONTENT_PROCESSING/vault/          # 427 MB (notes + GIFs)
CONTENT_PROCESSING/VISION_PROGRESS.json
CONTENT_PROCESSING/transcripts/    # 1.5 GB
CONTENT_PROCESSING/analysis/       # 579 MB
Instagram Downloads/{collection}/  # ~50 GB original MP4s
```

### Internal Drive
```bash
# Safe caches
rm -rf ~/Library/Caches/pip/*
rm -rf ~/Library/Caches/ms-playwright/*
rm -rf ~/Library/Caches/com.google.GeminiMacOS/*
# NOT: ~/Library/Caches/Google/Chrome/ (logs out Chrome)
```

---

## 6. Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Sub-agents for vision | Use background terminal processes instead |
| Cloud vision rate limits | Use local llava:7b via Ollama API |
| GPU contention (parallel) | Limit to 2-3 concurrent processes |
| Duplicate files (Downloads vs Samsung) | `diff -r` to verify, then delete |
| macOS resource forks (`._*`) | Filter in glob: `[f for f in glob if not f.name.startswith('._')]` |
| Malformed tags (single chars) | Filter: `len(tag) >= 3 and not tag.startswith('#')` |
| Skills without video_id | Filter in index generation |
| Missing index.md in support folders | Run `create_support_indexes.py` |

---

## 7. Quick Reference Commands

```bash
# Vision analysis (single)
/opt/homebrew/bin/python3.12 local_vision_analyze.py /path/to/frame.jpg

# Parallel batch (launch N chunks)
for chunk in chunks; do
  terminal(background=true, notify_on_complete=true, 
    command="cd /vision_pipeline && python3 batch_chunk.py '$chunk' $N")
done

# Monitor
process(action='list')

# Regenerate all mappings
python3 regenerate_mappings.py
python3 create_domain_indexes.py
python3 create_support_indexes.py
python3 clean_support_indexes.py
python3 create_master_mapping.py

# Storage check
df -h /Volumes/Samsung\ LED/
du -sh /Volumes/Samsung\ LED/Instagram\ Downloads/New\ Untouched\ Reels\ Download/CONTENT_PROCESSING/*
```

---

## 8. Skill Dependencies

- **Ollama** running with `llava:7b` loaded
- **Python 3.12+** with `requests` library
- **ffmpeg** for GIF generation
- **DaVinci Resolve MCP** for grade application
- **Hermes** with skills system for `/skill load`

---

*Class-level skill — captures the complete local vision → vault integration pattern for Instagram Reels → DaVinci Resolve pipeline.*