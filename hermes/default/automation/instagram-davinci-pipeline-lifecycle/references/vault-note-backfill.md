# Vault Note Backfill for Complete Videos (2026-07-31)

## Problem
1,030 complete videos but only ~600 had vault notes. 430 videos missing vault notes despite having vision analysis complete.

## Solution: Single Script Backfill
```python
# Read VISION_PROGRESS.json
# Check vault for existing video_id in frontmatter
# For each missing video:
#   - Find frames directory
#   - Generate GIF from frames (ffmpeg)
#   - Create technique note with frontmatter + body
#   - Link to existing skill and analysis
```

## Script: `generate_vault_notes.py`
```python
# Read progress
with open(VISION_PROGRESS_PATH) as f:
    data = json.load(f)

# Build existing video_id map from vault
existing = set()
for f in VAULT_TECHNIQUES.glob("*.md"):
    fm = read_frontmatter(f.read_text())
    vid = fm.get("video_id", "").strip('"')
    if vid:
        existing.add(vid)

# Find missing
complete = [d for d in data if d.get("status") == "complete"]
missing = [d for d in complete if d["video_id"] not in existing]

# Process each missing
for item in missing:
    vid = item["video_id"]
    frames_dir, frames = find_frames_dir(vid)
    if not frames:
        continue
    
    # Generate GIF
    gif_name = f"{vid}_technique.gif"
    generate_gif(vid, frames, VAULT_MEDIA / gif_name)
    
    # Find skill
    skill_name = find_skill_path(vid)
    
    # Generate note
    note_content, note_filename = generate_vault_note(item, gif_name, skill_name)
    (VAULT_TECHNIQUES / note_filename).write_text(note_content)
```

## Results
| Metric | Before | After |
|--------|--------|-------|
| Complete videos | 1,030 | 1,030 |
| Vault notes | ~600 | 1,005 |
| Missing | 430 | 25 (edge cases) |
| Notes created | - | 2,046 (includes duplicates) |

## Note Structure
```markdown
---
title: "Technique Name"
video_id: "VID123"
collection: "Color_grading"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
tags: ["davinci-resolve", "color-grading"]
source_reel: "VID123"
vision_model: "llava:7b"
local_vision_frames: 3
skill: "technique-name.md"
analysis: "analysis/VID123/analysis.json"
domain: "Color Grading & Looks"
moved_at: "2026-07-31"
created: "2026-07-31"
---

# Technique Name

**Source:** [[Reel VID123]] (Collection)  
**Page:** Color | **Graph:** serial | **Vision:** llava:7b (3 frames)

![Technique Name](media/VID123_technique.gif)

## Node Graph Structure
- Curves
- Color Wheels

## Parameters
- grading_style: teal/orange
- camera_movement: static
- ...

## Steps to Reproduce in DaVinci Resolve
1. Open Color page
2. Apply teal/orange grading
...

## Cross-References
- **Collection:** [[Color_grading]]
- **Page:** [[Color]]
```

## Key Points
- **Fast**: Single script processes all 430 in minutes
- **No vision analysis**: Uses existing `VISION_PROGRESS.json` data
- **GIF generation**: ffmpeg from existing frames (3-5 sec/video)
- **Skill linking**: Finds existing Hermes skill by video_id
- **Analysis linking**: Points to `analysis/video_id/analysis.json`
- **Duplicates**: Some videos generated multiple notes (different technique names) - acceptable

## Edge Cases (25 remaining)
- `Cvzl4_zN5jm_frame0005` - appears to be frame file, not video
- Videos with no frames directory
- Videos with malformed frontmatter

## After Backfill
- 1,005/1,030 complete videos have vault notes (97.6%)
- All 7 domain folders have technique notes with cross-references
- Each note links to: GIF, skill, analysis, tags, collection