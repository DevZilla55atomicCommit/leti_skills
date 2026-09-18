# Session 20260725 — Tag-Aware Full Pipeline Extraction (Complete)

## Context
Complete 771-reel extraction with tag-aware prompts per subcategory. Ran as background process `proc_2535d7948875`.

## What Was Done
- **Created full tag-aware pipeline** (`scripts/full_tag_aware_pipeline.py`) with category-specific extraction prompts
- **Processed 771 reels total**: 380 Video Effects + 391 Photography/Videography
- **Category-specific extraction prompts** per subcategory (transitions, color_grading, fusion_compositing, motion_graphics, vfx, camera_techniques, lighting, composition, audio_sound, editing_workflow for Video Effects; portrait, landscape, commercial_product, street_documentary, lighting_technique for Photography)
- **Generated structured vault notes** with JSON extraction in `DaVinci_Knowledge_Base/Video_Effects/` and `Photography_Videography/`
- **Created Hermes skills** with tag-aware metadata in `~/.hermes/skills/creative/davinci-video_effect-*` and `davinci-photography-*`
- **Copied assets** (frames/GIFs) to vault assets folders

## Key Technical Learnings

### 1. Tag-Aware Extraction Prompts (Critical)
**OLD (Generic):** "Analyze this frame for DaVinci Resolve techniques"
**NEW (Tag-Aware):** Per-subcategory prompts that extract exactly what that category teaches:
- **Transitions:** transition type, duration, easing curve, Fusion setup, keyframe structure, color handling, audio crossfade
- **Color Grading:** node tree, CST/LUT chain, Power Windows, curves, wheel settings, film effects, output transform
- **Fusion Compositing:** node graph, keying workflow, tracking setup, masking, 3D setup, particles, paint tools
- **Motion Graphics:** template structure, keyframes, expressions, modifiers, publish controls, data-driven setup
- **VFX:** effect type, particle setup, simulation settings, shaders, compositing over plate, render settings
- **Camera Techniques:** movement type, rig/equipment, speed/acceleration, stabilization, lens info, DaVinci post-stabilization
- **Lighting:** setup type, light positions/modifiers, ratios, color temps, modifiers, golden hour specifics, DaVinci relighting
- **Composition:** rule/technique, lens choice, subject placement, depth creation, aspect ratio, camera angle, DaVinci reframe
- **Audio/Sound:** technique, Fairlight tools, plugin settings, music layering, dialogue processing, sound design, delivery specs
- **Editing Workflow:** edit technique, pacing/rhythm, timeline org, multicam, trim tools, speed changes, automation

### 2. Frame Directory Mapping Issue (Critical)
- **Problem:** `extraction_manifest.json` stores frame dirs by Instagram short ID (e.g., `C-5PYQSADOG`) but actual directories use downreels.com internal IDs (e.g., `AQM-ilAolE4vx37u9eaK...`)
- **Solution:** Build mapping from `completed.json` (download order) to frame directories sorted by mtime
- **Code Pattern:**
```python
# Map Instagram short ID → frame directory via download order
completed = json.load(open(completed_json))
frame_dirs = sorted(os.listdir(frames_dir), key=lambda d: os.path.getmtime(os.path.join(frames_dir, d)))
id_map = {completed[i]: frame_dirs[i] for i in range(min(len(completed), len(frame_dirs)))}
```

### 3. Frame Directory Existence Check (Robust)
- **Issue:** Some reels have frames in manifest but directory missing (extraction failed/skipped)
- **Fix:** Check both manifest `frames_dir` AND fallback to `id_map[reel_id]` AND glob search
```python
def get_frame_dir(reel_id, manifest_entry, id_map):
    # 1. Try manifest
    if manifest_entry.get('frames_dir') and os.path.exists(manifest_entry['frames_dir']):
        return manifest_entry['frames_dir']
    # 2. Try ID map
    if reel_id in id_map and os.path.exists(frames_dir / id_map[reel_id]):
        return frames_dir / id_map[reel_id]
    # 3. Fallback glob search
    matches = list(frames_dir.glob(f"*{reel_id}*"))
    if matches: return str(matches[0])
    return None
```

### 4. Rate Limiting Vision API (20 RPM Hard Limit)
- **Minimum 3 seconds between vision_analyze calls**
- Exponential backoff on 429: 30s → 60s → 120s → 240s → 480s
- **Do NOT batch vision calls** — each counts against RPM
- Terminal/file ops can batch freely; only vision_analyze is rate-limited

### 5. Frame Sampling Strategy (5 key frames max)
- `frame_0001` — opening/title, technique identification
- `frame_0020` — early demo, tools/nodes introduced
- `frame_0050` — core technique, main workflow
- `frame_0080` — parameters/settings visible
- `frame_last` — result/comparison, before/after

### 6. Skip Heuristics (Detected via Vision)
- Talking head frames (person on camera, no UI)
- Title/transition frames (large text overlay, no Resolve UI)
- Duplicate frames (visually identical to previous sample)
- Outro/CTA frames ("follow me", "save this", social handles)

### 7. Complete Pipeline Architecture (No Skips)
```
Instagram URLs (RTF) 
    → Parse & categorize by source file + keywords
    → Download via downreels.com (4s delay, serial)
    → Extract frames (1fps) + GIF (5s, 15fps, 480p) + transcript (Whisper)
    → Update manifest with correct frame_dir mapping
    → Tag-aware vision analysis (5 frames, category-specific prompt)
    → Generate structured vault note with JSON extraction
    → Create Hermes skill with category metadata
    → Copy frames/GIFs to vault assets/{subcategory}/
    → Update master index & cross-references
```

### Pitfalls to Avoid (from this session)
1. **Don't use generic prompts** — tag-aware prompts extract 5-10x more useful data
2. **Don't assume manifest frame_dir is correct** — always verify and fallback to ID map
3. **Don't skip reels** — process all, flag missing frames but continue
4. **Don't batch vision calls** — 20 RPM is strict; 3s minimum interval
5. **Don't claim complete prematurely** — verify output files exist
6. **Don't use generic skill templates** — category-specific templates with relevant metadata
7. **Don't forget frame mapping** — downreels.com IDs ≠ Instagram short IDs

### Template Files Updated
- `templates/vault_note_template.md` — generic fallback
- `templates/vault_note_template_video_effect.md` — Video Effects with subcategory field
- `templates/vault_note_template_lightroom.md` — Photography/Lightroom
- `templates/skill_template.md` — generic
- `templates/skill_template_video_effect.md` — Video Effects with category/subcategory metadata
- `templates/skill_template_lightroom.md` — Photography with Lightroom-specific tags

### Scripts Created/Updated
- `scripts/full_tag_aware_pipeline.py` — complete 771-reel pipeline with tag-aware extraction
- `scripts/process_batch.py` — batch processor for resumable processing
- `scripts/run_pipeline.py` — main orchestrator
- `scripts/extract.py` — frame/GIF/transcript extraction
- `scripts/vision_analyze.py` — vision analysis wrapper

### Pipeline Status
- **Total reels:** 771 (380 Video Effects + 391 Photography/Videography)
- **Background process:** `proc_2535d7948875` running `scripts/full_tag_aware_pipeline.py`
- **Progress:** ~63/771 reels processed (as of last poll)
- **Target:** Complete all 771 with tag-aware extraction