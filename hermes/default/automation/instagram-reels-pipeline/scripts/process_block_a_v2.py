#!/usr/bin/env python3
"""
Process already downloaded MP4 files through the videographer pipeline
Uses local files only - no re-downloading
"""

import json
import re
import os
import subprocess
import sys
import shutil
import time
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_BASE = "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Videographer"
SKILLS_BASE = "/Users/alfredkamisese/.hermes/skills/videographer"
OUTPUT_BASE = "/Volumes/Samsung LED/Instagram Downloads"

# Frame timestamps as percentages (100% = end of video, use 99.9% to avoid seeking past last frame)
FRAME_PERCENTAGES = [0, 14, 28, 42, 57, 71, 86, 99.9]

# Discipline folders for vault organization
DISCIPLINES = [
    "Camera_Movement",
    "Cinematography",
    "Post_Production",
    "Color_Grading_&_Looks",
    "Video_Effects",
    "VFX_&_Compositing",
    "Composition",
    "Lighting",
    "Camera_Theory",
    "Business_&_Career",
    "Lenses_&_Optics"
]

def extract_reel_code_from_filename(filename):
    """Extract reel code from filename"""
    # Pattern: reel:CODE:
    match = re.search(r'reel:([^:]+):', filename)
    if match:
        return match.group(1)
    # Special case: DC1iY8LvN3Y.mp4
    if filename.startswith("DC1iY8LvN3Y"):
        return "DC1iY8LvN3Y"
    return None

def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration",
        "-of", "csv=p=0",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return None

def extract_frames(video_path, output_dir, duration):
    """Extract frames at specific timestamps"""
    os.makedirs(output_dir, exist_ok=True)

    timestamps = [p / 100 * duration for p in FRAME_PERCENTAGES]

    for i, ts in enumerate(timestamps):
        frame_path = os.path.join(output_dir, f"frame_{i:02d}.png")
        cmd = [
            "ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
            "-vframes", "1", "-q:v", "2", frame_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    ⚠ Frame {i} extraction failed: {result.stderr[:200]}")

    # Verify frames - accept ≥7 frames (100% frame sometimes fails on short clips)
    frames = sorted(Path(output_dir).glob("frame_*.png"))
    return len(frames) >= 7

def create_gif(frames_dir, output_path, fps=2):
    """Create GIF from extracted frames"""
    # Generate palette
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "2",
        "-i", os.path.join(frames_dir, "frame_%02d.png"),
        "-vf", "scale=720:-1:flags=lanczos,palettegen=stats_mode=diff",
        "-y", "/tmp/palette.png"
    ], capture_output=True)

    cmd = [
        "ffmpeg", "-y", "-framerate", "2",
        "-i", os.path.join(frames_dir, "frame_%02d.png"),
        "-i", "/tmp/palette.png",
        "-lavfi", "scale=720:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0

def classify_discipline(caption):
    """Simple heuristic to classify reel discipline from caption/filename"""
    caption_lower = caption.lower()

    if any(kw in caption_lower for kw in ["movement", "camera move", "dolly", "slider", "gimbal", "tracking", "pan", "tilt", "push", "pull"]):
        return "Camera_Movement"
    elif any(kw in caption_lower for kw in ["cinematography", "lighting", "exposure", "lens", "focal", "depth of field", "bokeh", "anamorphic"]):
        return "Cinematography"
    elif any(kw in caption_lower for kw in ["color", "grade", "lut", "look", "film emulation", "log", "slog", "rec709", "hdr"]):
        return "Color_Grading_&_Looks"
    elif any(kw in caption_lower for kw in ["edit", "cut", "transition", "timeline", "premiere", "davinci", "resolve", "after effects", "fusion"]):
        return "Post_Production"
    elif any(kw in caption_lower for kw in ["effect", "vfx", "composite", "mask", "key", "track", "rotoscope", "particle"]):
        return "VFX_&_Compositing"
    elif any(kw in caption_lower for kw in ["composition", "framing", "rule of thirds", "leading lines", "symmetry", "negative space"]):
        return "Composition"
    elif any(kw in caption_lower for kw in ["light", "key light", "fill", "rim", "softbox", "led", "natural light", "golden hour"]):
        return "Lighting"
    elif any(kw in caption_lower for kw in ["lens", "mm", "focal", "aperture", "t-stop", "anamorphic", "spherical", "vintage"]):
        return "Lenses_&_Optics"
    elif any(kw in caption_lower for kw in ["business", "client", "pricing", "contract", "portfolio", "freelance", "career"]):
        return "Business_&_Career"
    else:
        return "Camera_Theory"  # Default

def create_vault_note(reel_code, metadata, frames_dir, discipline, output_dir):
    """Create Obsidian vault note"""
    os.makedirs(output_dir, exist_ok=True)

    title = metadata.get("title", f"Reel {reel_code}")
    description = metadata.get("description", "")
    uploader = metadata.get("uploader", "unknown")
    upload_date = metadata.get("upload_date", "")
    duration = metadata.get("duration", 0)
    like_count = metadata.get("like_count", 0)
    comment_count = metadata.get("comment_count", 0)

    # Format date
    if upload_date:
        try:
            dt = datetime.strptime(upload_date, "%Y%m%d")
            formatted_date = dt.strftime("%Y-%m-%d")
        except:
            formatted_date = upload_date
    else:
        formatted_date = "Unknown"

    frames_list = "\n".join([f"![[frame_{i:02d}.png]]" for i in range(8)])

    note_content = f"""---
reel_code: {reel_code}
source_url: https://www.instagram.com/reel/{reel_code}/
creator: {uploader}
date: {formatted_date}
duration: {duration:.1f}s
likes: {like_count}
comments: {comment_count}
discipline: {discipline}
tags: [instagram, reel, {discipline.lower().replace('&', '').replace('_', ' ')}]
---

# {title}

**Creator:** {uploader}
**Date:** {formatted_date}
**Duration:** {duration:.1f}s
**Engagement:** ❤ {like_count} | 💬 {comment_count}

## Description
{description}

## Frames (0%, 14%, 28%, 42%, 57%, 71%, 86%, 100%)
{frames_list}

## Analysis Notes
*Add your technical analysis here*

---
*Generated by Hermes Reels Pipeline on {datetime.now().isoformat()}*
"""

    note_path = os.path.join(output_dir, f"{reel_code}.md")
    with open(note_path, "w") as f:
        f.write(note_content)

    # Copy frames to vault directory
    for frame in Path(frames_dir).glob("frame_*.png"):
        shutil.copy2(frame, os.path.join(output_dir, frame.name))

    return note_path

def create_hermes_skill(reel_code, metadata, frames_dir, discipline, output_base):
    """Create Hermes skill directory with SKILL.md"""
    skill_dir = os.path.join(output_base, f"reel_{reel_code}")
    os.makedirs(skill_dir, exist_ok=True)

    title = metadata.get("title", f"Reel {reel_code}")
    description = metadata.get("description", "")
    uploader = metadata.get("uploader", "unknown")
    duration = metadata.get("duration", 0)

    skill_content = f"""---
name: videographer.reel_{reel_code}
description: Instagram Reel technique analysis - {title[:80]}
category: videographer
tags: [instagram, reel, {discipline.lower().replace('&', '').replace('_', '-')}, analysis]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: {datetime.now().isoformat()}
source_url: https://www.instagram.com/reel/{reel_code}/
creator: {uploader}
duration_seconds: {duration:.1f}
discipline: {discipline}
frame_count: 8
frame_timestamps: [0, 14, 28, 42, 57, 71, 86, 100]
---

# Reel Technique Analysis: {reel_code}

## Source
- **URL:** https://www.instagram.com/reel/{reel_code}/
- **Creator:** @{uploader}
- **Title:** {title}
- **Duration:** {duration:.1f}s
- **Discipline:** {discipline}

## Caption
{description}

## Frame References
Frames extracted at 8 key timestamps (0%, 14%, 28%, 42%, 57%, 71%, 86%, 100%):
- `frame_00.png` — 0% (Opening hook / establishing shot)
- `frame_01.png` — 14% (Early development)
- `frame_02.png` — 28% (First technique reveal)
- `frame_03.png` — 42% (Mid-point / core concept)
- `frame_04.png` — 57% (Secondary technique / variation)
- `frame_05.png` — 71% (Advanced application)
- `frame_06.png` — 86% (Refinement / detail)
- `frame_07.png` — 100% (Closing / result)

## Technique Breakdown
*Analyze each frame for: camera movement, lighting, composition, color, editing technique*

| Frame | Timestamp | Observation |
|-------|-----------|-------------|
| 00 | 0% | |
| 01 | 14% | |
| 02 | 28% | |
| 03 | 42% | |
| 04 | 57% | |
| 05 | 71% | |
| 06 | 86% | |
| 07 | 100% | |

## Key Takeaways
-
-
-

## DaVinci Resolve Application
*How to replicate or adapt this in Resolve:*
- Node structure:
- Color tools used:
- Fusion/Effects:
- Timeline technique:

## Tags for Retrieval
`#{discipline.lower().replace('&', '').replace('_', '-')}` `#instagram-reel` `#{reel_code}` `#technique-reference`

---
*Auto-generated by Hermes Agent Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""
    skill_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_path, "w") as f:
        f.write(skill_content)

    # Copy frames to skill directory
    for frame in Path(frames_dir).glob("frame_*.png"):
        shutil.copy2(frame, os.path.join(skill_dir, frame.name))

    return skill_path

def get_basic_metadata(reel_code):
    """Get minimal metadata from yt-dlp without downloading"""
    cookies_file = "/Users/alfredkamisese/Downloads/cookies_www.instagram.com_2026-07-19.txt"
    cmd = [
        "yt-dlp",
        "--cookies", cookies_file,
        "--skip-download",
        "--print-json",
        f"https://www.instagram.com/reel/{reel_code}/"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    try:
        return json.loads(result.stdout.strip())
    except:
        return {}

def process_single_video(video_path, reel_code):
    """Process a single downloaded video through the pipeline"""
    print(f"\n{'='*60}")
    print(f"Processing: {reel_code}")
    print(f"{'='*60}")

    try:
        # Get metadata from yt-dlp (lightweight, no download)
        print("  📥 Fetching metadata...")
        metadata = get_basic_metadata(reel_code)
        if not metadata:
            metadata = {"title": f"Reel {reel_code}", "description": "", "uploader": "unknown", "upload_date": "", "duration": 0, "like_count": 0, "comment_count": 0}

        caption = metadata.get("description", "")
        discipline = classify_discipline(caption)
        print(f"  📂 Discipline: {discipline}")

        # Get duration
        print("  ⏱  Getting duration...")
        duration = get_video_duration(video_path)
        if not duration:
            return {"code": reel_code, "status": "failed", "error": "Could not get duration"}
        print(f"  ⏱️  Duration: {duration:.1f}s")

        # Extract frames
        frames_dir = f"/tmp/frames_{reel_code}"
        print("  🖼️  Extracting frames...")
        if not extract_frames(video_path, frames_dir, duration):
            return {"code": reel_code, "status": "failed", "error": "Frame extraction failed"}
        print(f"  ✅ 8 frames extracted")

        # Create vault note
        vault_dir = os.path.join(VAULT_BASE, discipline)
        print("  📝 Creating vault note...")
        note_path = create_vault_note(reel_code, metadata, frames_dir, discipline, vault_dir)
        print(f"  ✅ Note: {os.path.basename(note_path)}")

        # Create Hermes skill
        print("  🔧 Creating Hermes skill...")
        skill_path = create_hermes_skill(reel_code, metadata, frames_dir, discipline, SKILLS_BASE)
        print(f"  ✅ Skill: reel_{reel_code}/SKILL.md")

        # Create GIF
        gif_path = os.path.join(vault_dir, f"{reel_code}.gif")
        print("  🎞️  Creating GIF...")
        if create_gif(frames_dir, gif_path):
            print(f"  ✅ GIF created")
        else:
            print(f"  ⚠️  GIF creation failed")

        # Cleanup temp frames
        try:
            shutil.rmtree(frames_dir, ignore_errors=True)
        except:
            pass

        return {"code": reel_code, "status": "success", "discipline": discipline}

    except Exception as e:
        return {"code": reel_code, "status": "failed", "error": str(e)}

def main():
    folder_path = "/Volumes/Samsung LED/Instagram Downloads/Reels/Block A/"

    # Get all MP4 files (excluding ._ files)
    mp4_files = []
    for f in os.listdir(folder_path):
        if f.endswith(".mp4") and not f.startswith("._"):
            mp4_files.append(f)

    print(f"Found {len(mp4_files)} MP4 files to process")

    results = []
    for i, filename in enumerate(mp4_files):
        reel_code = extract_reel_code_from_filename(filename)
        if not reel_code:
            print(f"Could not extract reel code from: {filename}")
            continue

        # Check if already processed
        skill_dir = f"/Users/alfredkamisese/.hermes/skills/videographer/reel_{reel_code}"
        if os.path.exists(skill_dir):
            print(f"Skipping {reel_code} - already processed")
            continue

        video_path = os.path.join(folder_path, filename)
        result = process_single_video(video_path, reel_code)
        results.append(result)

        # Rate limit
        time.sleep(1)

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")

    print("\n" + "="*60)
    print("BATCH PROCESSING COMPLETE")
    print("="*60)
    print(f"✅ Success: {success}")
    print(f"❌ Failed: {failed}")

    # Save results
    with open("/Users/alfredkamisese/block_a_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()