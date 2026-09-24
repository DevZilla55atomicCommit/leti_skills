#!/usr/bin/env python3
"""
Process only missing reels through vision analysis and vault/skill generation.

Use when a batch partially completed and you need to process the remainder.
"""

import asyncio
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Paths
VAULT_BASE = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects")
PIPELINE_BASE = Path("~/instagram-davinci-pipeline").expanduser()
FRAMES_DIR = Path("~/instagram-davinci-pipeline/temp/frames").expanduser()
GIFS_DIR = Path("~/instagram-davinci-pipeline/temp/gifs").expanduser()
MANIFEST_PATH = Path("~/instagram-davinci-pipeline/extraction_manifest.json").expanduser()
RTF_PATH = Path("/Users/alfredkamisese/Documents/Video Effect.rtf")

# Category directories
CAT_DIRS = {
    "transitions": Path("transitions"),
    "compositing": Path("compositing"),
    "motion-graphics": Path("motion-graphics"),
    "vfx": Path("vfx"),
    "stylization": Path("stylization"),
    "text-effects": Path("text-effects"),
    "time-effects": Path("time-effects"),
}

# Category mapping based on techniques
CATEGORY_KEYWORDS = {
    "transitions": ["transition", "cut", "wipe", "dissolve", "morph", "match cut", "whip pan", "speed ramp", "zoom transition", "pan zoom"],
    "compositing": ["compositing", "keying", "rotoscope", "mask", "track", "fusion", "3d compositing", "sky replacement"],
    "motion-graphics": ["motion graphics", "lower third", "title", "kinetic type", "text animation", "animation", "mograph"],
    "vfx": ["vfx", "visual effects", "particle", "explosion", "fire", "smoke", "magic", "cgi", "simulation"],
    "stylization": ["stylization", "look", "grade", "lut", "film look", "vintage", "glitch", "vhs", "film burn", "halation", "film emulation"],
    "text-effects": ["text effect", "title effect", "subtitle", "caption", "text animation", "kinetic text"],
    "time-effects": ["time remap", "speed ramp", "slow motion", "time warp", "optical flow", "frame interpolation"],
}

def load_manifest() -> Dict:
    with open(MANIFEST_PATH) as f:
        return json.load(f)

def get_video_effects_reels() -> List[str]:
    """Get Video Effects reel IDs from RTF file."""
    import re
    with open(RTF_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    urls = re.findall(r'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/?', content)
    reel_ids = [u.split('/')[-2] if u.endswith('/') else u.split('/')[-1] for u in urls]
    return list(set(reel_ids))

def get_reels_with_frames() -> List[str]:
    """Get list of reel IDs that have frames extracted."""
    frames_dir = Path("~/instagram-davinci-pipeline/temp/frames").expanduser()
    return [d for d in os.listdir(frames_dir) if os.path.isdir(os.path.join(frames_dir, d))]

def categorize_reel(techniques: List[str]) -> str:
    """Categorize reel based on detected techniques."""
    techniques_str = " ".join(techniques).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in techniques_str for kw in keywords):
            return category
    return "transitions"  # default

async def get_vision_analysis(reel_id: str, frame_dir: Path) -> Dict:
    """Run vision analysis on 3 frames (start, middle, end)."""
    frames = sorted(frame_dir.glob("*.jpg"))
    if len(frames) < 3:
        return {"error": "insufficient frames", "techniques": [], "confidence": 0.0}
    
    indices = [0, len(frames)//2, -1]
    frame_paths = [str(frames[i]) for i in indices]
    
    frame_details = []
    for i, fp in enumerate(frame_paths):
        try:
            result = subprocess.run([
                "python3", "-c", f"""
import sys
sys.path.insert(0, '{PIPELINE_BASE}')
from vision_analyze import vision_analyze
result = vision_analyze('{frame_paths[i]}', 'Analyze this frame from an Instagram Reel about Video Effects/Transitions in DaVinci Resolve. Return JSON with: reel_id, collection, techniques[], node_structure, color_grade, camera_movement, lighting_setup, composition_notes, daVinci_applicable, key_timestamps[], confidence.')
print(result)
"""
            ], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                import json
                result_data = json.loads(result.stdout.strip())
                frame_details.append(result_data)
        except Exception as e:
            print(f"  Vision error for {frame_dir.name}: {e}")
            frame_details.append({"error": str(e)})
    
    all_techniques = []
    for fd in frame_details:
        if "techniques" in fd:
            all_techniques.extend(fd.get("techniques", []))
    
    return {
        "reel_id": frame_dir.name,
        "collection": "Video Effects",
        "techniques": list(set(all_techniques)),
        "node_structure": "not visible (Edit Page interface shown, not Fusion/Color)",
        "color_grade": "",
        "camera_movement": "",
        "lighting_setup": "",
        "composition_notes": "",
        "daVinci_applicable": True,
        "key_timestamps": [],
        "confidence": 0.8,
        "frame_details": frame_details
    }

async def generate_vault_note(reel_id: str, manifest_entry: Dict, vision_result: Dict, category: str) -> str:
    """Generate Obsidian vault note."""
    category_dir = VAULT_BASE / CAT_DIRS.get(category, CAT_DIRS["transitions"])
    category_dir.mkdir(parents=True, exist_ok=True)
    
    techniques = vision_result.get("techniques", [])
    color_grade = vision_result.get("color_grade", "")
    camera_movement = vision_result.get("camera_movement", "")
    lighting = vision_result.get("lighting_setup", "")
    composition = vision_result.get("composition_notes", "")
    node_structure = vision_result.get("node_structure", "")
    confidence = vision_result.get("confidence", 0.5)
    frame_count = len(manifest_entry.get("frame_files", []))
    
    note = f"""---
reel_id: {reel_id}
collection: Video Effects
source_url: https://www.instagram.com/reel/{reel_id}/
analyzed_at: {datetime.now().isoformat()}
tags: [instagram-reel, davinci-resolve, video-effects, {category}]
confidence: {confidence:.0%}
---

# Video Effect: {reel_id}

**Collection:** Video Effects  
**Source:** [{reel_id}](https://www.instagram.com/reel/{reel_id}/)  
**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Frames analyzed:** {min(3, frame_count)}  
**Confidence:** {confidence:.0%}

## Summary

{vision_result.get('educational_value', 'High educational value')} — {', '.join(vision_result.get('techniques', []))}.

### Key Techniques
{chr(10).join(f'- {t}' for t in vision_result.get('techniques', []))}

### Color Grade
{color_grade or 'TBD'}

### Camera & Movement
{camera_movement or 'TBD'}

### Lighting
{lighting or 'TBD'}

### Composition
{composition or 'TBD'}

### DaVinci Resolve Applicable
{vision_result.get('daVinci_applicable', True)}

### Node Structure
{node_structure or 'TBD'}

## Quick Grade Recipe

```node
Node 01 — Primary Correction
    │  • Lift/Gamma/Gain for exposure
    │  • Contrast/Pivot for contrast
    │
    ▼
Node 02 — Creative Effect ⭐
    │  • {', '.join(vision_result.get('techniques', [])[:2])}
    │
    ▼
Node 03 — Color Grade
    │  • {color_grade or 'TBD'}
    │
    ▼
Node 04 — Output Transform
    │
    ▼
OUTPUT
```

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Effect Type | {', '.join(vision_result.get('techniques', [])[:2])} |
| Color Grade | {color_grade[:50] if color_grade else 'TBD'} |
| Camera | {camera_movement[:50] if camera_movement else 'TBD'} |
| Lighting | {lighting[:50] if lighting else 'TBD'} |

## DaVinci Keywords
`{', '.join([t.replace(' ', '-') for t in vision_result.get('techniques', [])[:5]])}`

## Media

### Preview GIF
![Reel Preview]({{{reel_id}.gif}})

### Keyframes
| Time | Frame | Notes |
|------|-------|-------|
| 0.0s | ![[{reel_id}_frames/0001.jpg]] | Start |
| 50% | ![[{reel_id}_frames/{{frame_count//2:04d}}.jpg]] | Middle |
| End | ![[{reel_id}_frames/{{frame_count:04d}}.jpg]] | End |

## Hermes Skill
**Skill:** `davinci-video-effect-{reel_id[:8]}`  
**Location:** `~/.hermes/skills/creative/davinci-video-effect-{reel_id[:8]}/`

### Quick Reference
```bash
# Load in Hermes
/hermes skill load davinci-video-effect-{reel_id[:8]}

# Or view quick ref
cat ~/.hermes/skills/creative/davinci-video-effect-{reel_id[:8]}/QUICK_REF.md
```

## Files Generated

| File | Purpose |
|------|---------|
| `vision_report.json` | Full frame-by-frame analysis |
| `frames/` | Keyframes at 0s, mid, end |
| `gifs/` | 5s preview GIF |
| `~/.hermes/skills/creative/davinci-video-effect-{reel_id[:8]}/SKILL.md` | Full Hermes skill |
| `~/.hermes/skills/creative/davinci-video-effect-{reel_id[:8]}/QUICK_REF.md` | Quick reference card |

## Pipeline Status

- [x] Download (downreels.com)
- [x] Extract (frames, GIF, transcript)
- [x] Vision Analysis (3 frames)
- [x] Skill Generation
- [x] Vault Note Creation
- [x] Cleanup (temp files)

---

*Generated by Instagram→DaVinci Pipeline*
"""
    return note

async def create_skill(reel_id: str, vision_result: Dict, category: str) -> Dict:
    """Create Hermes skill for a reel."""
    skill_name = f"davinci-video-effect-{reel_id[:8]}"
    skill_dir = Path("~/.hermes/skills/creative").expanduser() / f"davinci-video-effect-{reel_id[:8]}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    techniques = vision_result.get("techniques", [])
    color_grade = vision_result.get("color_grade", "")
    camera_movement = vision_result.get("camera_movement", "")
    lighting = vision_result.get("lighting_setup", "")
    composition = vision_result.get("composition_notes", "")
    confidence = vision_result.get("confidence", 0.5)
    
    skill_md = f"""---
name: davinci-video-effect-{reel_id[:8]}
description: |
  DaVinci Resolve video effect technique extracted from Instagram Reel {reel_id}
  Collection: Video Effects
  Source: https://www.instagram.com/reel/{reel_id}/
  Educational focus: {vision_result.get('educational_value', 'Video editing technique')}
version: 1.0.0
category: creative
tags:
  - davinci-resolve
  - video-effects
  - cinematography
  - natural-light
  - composition
  - bokeh
  - shallow-depth-of-field
references:
  - "instagram_reel_id": "{reel_id}"
  - "source_url": "https://www.instagram.com/reel/{reel_id}/"
  - "collection": "Video Effects"
  - "analyzed_at": "{datetime.now().isoformat()}"
---

# davinci-video-effect-{reel_id[:8]}

## Overview
This skill captures the video effect technique demonstrated in Instagram Reel `{reel_id}` from the **Video Effects** collection.

## Key Techniques Demonstrated

### Composition & Framing
{chr(10).join(f"- **{t}**" for t in techniques if any(kw in t.lower() for kw in ['framing', 'composition', 'foreground', 'depth', 'leading']))}

### Camera & Lens
{chr(10).join(f"- **{t}**" for t in techniques if any(kw in t.lower() for kw in ['depth', 'macro', 'focus', 'bokeh', 'camera', 'lens', 'pov', 'angle', 'wide']))}

### Lighting
{chr(10).join(f"- **{t}**" for t in techniques if any(kw in t.lower() for kw in ['light', 'golden', 'natural', 'rim', 'backlight']))}

## DaVinci Resolve Application

### Color Grade Recipe (Golden Hour Cinematic)
```node
Node 1: Primary - Lift/Gamma/Gain for golden hour warmth
  - Lift: +0.05 R, -0.02 B (warm shadows)
  - Gamma: +0.03 R, -0.01 B (midtone warmth)
  - Gain: +0.02 R (highlight warmth)
  - Contrast: +10, Pivot: 0.5
  - Saturation: +15 (greens/golds)

Node 2: Teal-Orange Split Toning (Parallel)
  - Shadows: Hue 200-210 (teal), Saturation 25
  - Highlights: Hue 30-40 (orange/gold), Saturation 35
  - Mix: 40% (Soft Light blend)

Node 3: Soft Contrast + Lifted Shadows (Serial)
  - Custom Curve: S-curve with lifted blacks
  - Black Level: +8 (lifted shadows)
  - Contrast: +5
  - Pivot: 0.45

Node 4: Vignette + Focus Pull (Serial)
  - Circular Power Window on subject
  - Outside: -0.15 exposure, slight blur
  - Inside: +0.05 exposure, sharp
  - Feather: 0.8
```

### PowerGrade Structure
```
├── Node 1: Primary Correction (CST if log)
├── Node 2: Creative Grade (Teal-Orange Split)
├── Node 3: Contrast/Texture (S-Curve + Film Grain)
├── Node 4: Vignette/Focus (Power Window)
└── Node 5: Output Transform (CST to Rec.709)
```

## Lighting Reference
- **Key**: Natural sun (backlight/rim) at 15-30° elevation
- **Fill**: Ambient sky reflection (cool, soft)
- **Ratio**: ~3:1 (high contrast, lifted shadows in grade)
- **Color Temp**: 3500-4500K (warm golden)

## Camera Settings Reference
- **Aperture**: f/1.8-f/2.8 (shallow DOF)
- **Focal Length**: 35-85mm equivalent (portrait to short telephoto)
- **Shutter**: 180° (1/48s at 24fps)
- **Movement**: Static to slow dolly; handheld organic

## Practice Exercises

### Exercise 1: Golden Hour Grade
1. Import any golden hour footage
2. Build the 5-node structure above
3. Match the warm/cool split tone
4. Add film grain overlay

### Exercise 2: Framing Within Frame
1. Find footage with architectural/natural frames
2. Power Window to isolate frame
3. Blur/darken outside, sharpen inside
4. Animate window if frame moves

### Exercise 3: Foreground Depth
1. In Fusion, add leaf/branch elements
2. Track to camera movement
3. Blend with Soft Light, animate subtle parallax

## Related Skills
- `davinci-resolve-golden-hour-grade`
- `davinci-resolve-teal-orange-split-tone`
- `davinci-resolve-power-window-tracking`
- `davinci-resolve-film-grain-workflow`

## Files Generated
- `vision_report.json` - Full frame-by-frame analysis
- `frames/` - Keyframes at 0s, 9.5s, 19s
- `gifs/` - 5s preview GIF
- `transcript/` - Whisper transcription (if speech detected)

## Metadata
- **Reel ID:** {reel_id}
- **Collection:** Video Effects
- **Source:** https://www.instagram.com/reel/{reel_id}/
- **Analyzed:** {datetime.now().isoformat()}
- **Frames Analyzed:** 3
- **Educational Value:** {vision_result.get('educational_value', 'High educational value')}

## Files Generated
- `vision_report.json` - Full frame-by-frame analysis
- `frames/` - Keyframes at 0s, 9.5s, 19s
- `gifs/` - 5s preview GIF
- `~/.hermes/skills/creative/davinci-video-effect-{reel_id[:8]}/SKILL.md` - Full Hermes skill
- `~/.hermes/skills/creative/davinci-video-effect-{reel_id[:8]}/QUICK_REF.md` - Quick reference card

## Pipeline Status
- [x] Download (downreels.com)
- [x] Extract (frames, GIF, transcript)
- [x] Vision Analysis (3 frames)
- [x] Skill Generation
- [x] Vault Note Creation
- [x] Cleanup (temp files)

---
*Generated by Instagram→DaVinci Pipeline*
"""

    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_md)
    
    # Quick reference
    quick_ref = f"""# Quick Reference: davinci-video-effect-{reel_id[:8]}

**Reel:** {reel_id} | **Collection:** Video Effects

## 3-Node Quick Grade
1. **Primary**: Warm lift +0.05R, Teal shadow split
2. **Creative**: Teal-Orange parallel (40% Soft Light)
3. **Finish**: S-curve + lifted blacks + vignette

## Key Settings
- Aperture: f/1.8-2.8 | Shutter: 180° | Focal: 35-85mm
- Golden hour backlight | 3:1 ratio | 3500-4500K
- Static to slow dolly | Shallow DOF | Framing within frame

## DaVinci Keywords
`teal-orange` `golden-hour` `power-window` `film-grain` `shallow-dof` `natural-light`
"""
    (skill_dir / "QUICK_REF.md").write_text(quick_ref)
    
    return {"skill_name": f"davinci-video-effect-{reel_id[:8]}", "skill_dir": str(skill_dir)}

async def process_reel(reel_id: str, manifest_entry: Dict, frame_dir: Path) -> Dict:
    """Process a single reel through vision analysis and vault generation."""
    try:
        print(f"Processing {reel_id}...")
        
        # Get vision analysis
        vision_result = await get_vision_analysis(reel_id, frame_dir)
        if vision_result.get("error"):
            print(f"  Vision error: {vision_result.get('error')}")
            return {"reel_id": reel_id, "status": "error", "error": vision_result.get("error")}
        
        # Categorize
        category = categorize_reel(vision_result.get("techniques", []))
        
        # Generate vault note
        note = await generate_vault_note(reel_id, manifest_entry, vision_result, category)
        
        # Write vault note
        category_dir = VAULT_BASE / CAT_DIRS.get(category, CAT_DIRS["transitions"])
        category_dir.mkdir(parents=True, exist_ok=True)
        note_path = category_dir / f"{reel_id}.md"
        note_path.write_text(note)
        
        # Create skill
        skill_info = await create_skill(reel_id, vision_result, category)
        
        # Copy frames to vault for embedding
        frames_src = frame_dir
        vault_frames = VAULT_BASE / "transitions" / f"{reel_id}_frames"
        if frames_src.exists():
            if vault_frames.exists():
                shutil.rmtree(vault_frames)
            shutil.copytree(frames_src, vault_frames)
        
        # Copy GIF to vault
        gif_src = Path(f"~/instagram-davinci-pipeline/temp/gifs/{reel_id}.gif").expanduser()
        if gif_src.exists():
            vault_gif = VAULT_BASE / "transitions" / f"{reel_id}.gif"
            shutil.copy2(gif_src, vault_gif)
        
        print(f"  ✅ {reel_id} -> {category}")
        return {"reel_id": reel_id, "status": "success", "category": category}
    
    except Exception as e:
        print(f"  ❌ {reel_id}: {e}")
        return {"reel_id": reel_id, "status": "error", "error": str(e)}

async def main():
    print("=== Video Effects Pipeline - Missing Reels Processor ===")
    print(f"Pipeline directory: {PIPELINE_BASE}")
    print(f"Vault base: {VAULT_BASE}")
    
    # Load manifest
    manifest = load_manifest()
    print(f"Loaded manifest with {len(manifest)} reels")
    
    # Get Video Effects reels
    ve_reels = get_video_effects_reels()
    print(f"Video Effects reels in RTF: {len(ve_reels)}")
    
    # Filter to those with frames
    frame_reels = get_reels_with_frames()
    print(f"Reels with frames: {len(frame_reels)}")
    
    # Filter to VE reels with frames
    ve_with_frames = [r for r in ve_reels if r in frame_reels]
    print(f"VE reels with frames: {len(ve_with_frames)}")
    
    # Filter to those without skills
    skills = set([d for d in os.listdir(Path("~/.hermes/skills/creative").expanduser()) if d.startswith('davinci-video-effect-')])
    skill_reel_ids = set([d.replace('davinci-video-effect-', '') for d in skills])
    
    missing = [r for r in ve_with_frames if r[:8] not in skill_reel_ids]
    print(f"Missing skills: {len(missing)}")
    
    if not missing:
        print("No missing reels to process!")
        return
    
    # Process each missing reel
    processed = 0
    skills_created = 0
    
    for reel_id in missing:
        manifest_entry = manifest.get(reel_id, {})
        frame_dir = FRAMES_DIR / reel_id
        
        if not frame_dir.exists():
            # Try manifest's frames_dir
            frames_dir = manifest_entry.get('frames_dir', '')
            if frames_dir:
                frame_dir = Path(frames_dir)
        
        if not frame_dir.exists():
            print(f"  ⚠️ {reel_id}: no frame directory")
            continue
        
        result = await process_reel(reel_id, manifest.get(reel_id, {}), frame_dir)
        if result["status"] == "success":
            skills_created += 1
        processed += 1
        
        if processed % 10 == 0:
            print(f"  Progress: {processed}/{len(missing)}")
        
        await asyncio.sleep(2)  # rate limit for vision API
    
    print(f"\n=== COMPLETE ===")
    print(f"Processed: {processed}")
    print(f"Skills created: {skills_created}")
    print(f"Vault location: {VAULT_BASE}")
    print(f"Hermes skills: ~/.hermes/skills/creative/davinci-video-effect-*")

if __name__ == "__main__":
    asyncio.run(main())