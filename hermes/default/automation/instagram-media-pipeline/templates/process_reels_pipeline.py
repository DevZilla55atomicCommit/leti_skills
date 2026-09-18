#!/usr/bin/env python3
"""
Instagram Reels Processing Pipeline — Template
- Uses yt-dlp nightly with cookies for fast downloads
- Extracts 8 frames at 0/14/28/42/57/71/86/100% using ffmpeg
- Creates Obsidian vault notes organized by discipline
- Creates Hermes skills in ~/.hermes/skills/videographer/reel_{CODE}/

USAGE:
  1. Copy this file to your working directory
  2. Update CONFIG section with your paths
  3. Ensure cookies.txt is fresh (exported via Get cookies.txt extension)
  4. Run: python3 process_reels_pipeline.py

REQUIREMENTS:
  - yt-dlp nightly: pip install -U --pre yt-dlp
  - ffmpeg + ffprobe in PATH
  - Python 3.10+
"""

import json
import re
import os
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ============================================================
# CONFIGURATION — UPDATE THESE FOR YOUR ENVIRONMENT
# ============================================================
REEL_URLS_FILE = "/tmp/reel_urls.json"
COOKIES_FILE = "/Users/alfredkamisese/Downloads/cookies_www.instagram.com_2026-07-19.txt"
VAULT_BASE = "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Videographer"
SKILLS_BASE = "/Users/alfredkamisese/.hermes/skills/videographer"
OUTPUT_BASE = "/Volumes/Samsung LED/Instagram Downloads"  # External SSD
MAX_WORKERS = 3  # Parallel downloads (respect rate limits)
RATE_LIMIT_DELAY = 2  # seconds between starting downloads

# Frame timestamps as percentages
FRAME_PERCENTAGES = [0, 14, 28, 42, 57, 71, 86, 100]

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
# ============================================================

def extract_reel_code(url):
    """Extract reel code from Instagram URL"""
    patterns = [
        r'/reel/([A-Za-z0-9_-]+)',
        r'/p/([A-Za-z0-9_-]+)',
        r'/tv/([A-Za-z0-9_-]+)'
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
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
    """Extract 8 frames at specific timestamps"""
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
            print(f"  ⚠ Frame {i} extraction failed: {result.stderr[:200]}")
    
    frames = sorted(Path(output_dir).glob("frame_*.png"))
    return len(frames) == 8

def create_gif(frames_dir, output_path, fps=2):
    """Create GIF from extracted frames with optimized palette"""
    frame_pattern = os.path.join(frames_dir, "frame_%02d.png")
    
    # Generate palette
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", frame_pattern,
        "-vf", "scale=720:-1:flags=lanczos,palettegen=stats_mode=diff",
        "/tmp/palette.png"
    ]
    subprocess.run(cmd, capture_output=True)
    
    # Create GIF with palette
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", frame_pattern,
        "-i", "/tmp/palette.png",
        "-lavfi", "scale=720:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0

def download_reel(reel_code, url, cookies_file):
    """Download reel using yt-dlp with cookies"""
    output_template = os.path.join("/tmp", f"{reel_code}_%(height)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "--cookies", cookies_file,
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--no-playlist",
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    
    # Find downloaded file
    for f in Path("/tmp").glob(f"{reel_code}_*.mp4"):
        return str(f)
    
    return None

def get_reel_metadata(url, cookies_file):
    """Extract metadata using yt-dlp --print-json"""
    cmd = [
        "yt-dlp",
        "--cookies", cookies_file,
        "--skip-download",
        "--print-json",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    try:
        return json.loads(result.stdout.strip())
    except:
        return {}

def classify_discipline(caption, metadata):
    """Simple heuristic to classify reel discipline"""
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
**Engagement:** ❤️ {like_count} | 💬 {comment_count}

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
*Auto-generated by Hermes Agent Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    skill_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_path, "w") as f:
        f.write(skill_content)
    
    # Copy frames to skill directory
    for frame in Path(frames_dir).glob("frame_*.png"):
        shutil.copy2(frame, os.path.join(skill_dir, frame.name))
    
    return skill_path

def process_single_reel(reel_data, cookies_file, vault_base, skills_base, output_base):
    """Process one reel end-to-end"""
    url = reel_data["url"]
    reel_code = extract_reel_code(url)
    
    if not reel_code:
        return {"code": "unknown", "status": "failed", "error": "Could not extract reel code"}
    
    print(f"\n{'='*60}")
    print(f"Processing: {reel_code}")
    print(f"{'='*60}")
    
    try:
        # 1. Get metadata
        print("  📥 Fetching metadata...")
        metadata = get_reel_metadata(url, cookies_file)
        if not metadata:
            return {"code": reel_code, "status": "failed", "error": "No metadata"}
        
        caption = metadata.get("description", "")
        discipline = classify_discipline(caption, metadata)
        print(f"  📂 Discipline: {discipline}")
        
        # 2. Download video
        print("  ⬇️  Downloading video...")
        video_path = download_reel(reel_code, url, cookies_file)
        if not video_path:
            return {"code": reel_code, "status": "failed", "error": "Download failed"}
        print(f"  ✅ Downloaded: {os.path.basename(video_path)}")
        
        # 3. Get duration
        duration = get_video_duration(video_path)
        if not duration:
            return {"code": reel_code, "status": "failed", "error": "Could not get duration"}
        print(f"  ⏱️  Duration: {duration:.1f}s")
        
        # 4. Extract frames
        frames_dir = f"/tmp/frames_{reel_code}"
        print("  🖼️  Extracting frames...")
        if not extract_frames(video_path, frames_dir, duration):
            return {"code": reel_code, "status": "failed", "error": "Frame extraction failed"}
        print(f"  ✅ 8 frames extracted")
        
        # 5. Create vault note
        vault_dir = os.path.join(vault_base, discipline)
        print("  📝 Creating vault note...")
        note_path = create_vault_note(reel_code, metadata, frames_dir, discipline, vault_dir)
        print(f"  ✅ Note: {os.path.basename(note_path)}")
        
        # 6. Create Hermes skill
        print("  🔧 Creating Hermes skill...")
        skill_path = create_hermes_skill(reel_code, metadata, frames_dir, discipline, skills_base)
        print(f"  ✅ Skill: reel_{reel_code}/SKILL.md")
        
        # 7. Copy video to external storage
        final_video = os.path.join(output_base, f"{reel_code}.mp4")
        os.makedirs(output_base, exist_ok=True)
        shutil.copy2(video_path, final_video)
        print(f"  💾 Archived to: {final_video}")
        
        # 8. Create GIF
        gif_path = os.path.join(vault_dir, f"{reel_code}.gif")
        print("  🎞️  Creating GIF...")
        if create_gif(frames_dir, gif_path):
            print(f"  ✅ GIF created")
        else:
            print(f"  ⚠️  GIF creation failed")
        
        # Cleanup temp files
        try:
            os.remove(video_path)
            shutil.rmtree(frames_dir, ignore_errors=True)
        except:
            pass
        
        return {"code": reel_code, "status": "success", "discipline": discipline}
        
    except Exception as e:
        return {"code": reel_code, "status": "failed", "error": str(e)}

def main():
    print("="*60)
    print("INSTAGRAM REELS PROCESSING PIPELINE")
    print("="*60)
    
    # Verify cookies exist
    if not os.path.exists(COOKIES_FILE):
        print(f"❌ Cookies file not found: {COOKIES_FILE}")
        sys.exit(1)
    print(f"✅ Cookies: {COOKIES_FILE}")
    
    # Load reel URLs
    with open(REEL_URLS_FILE) as f:
        data = json.load(f)
    
    reels = [d for d in data if '/reel/' in d['url']]
    
    # Check already processed
    processed = set()
    if os.path.exists(SKILLS_BASE):
        for d in os.listdir(SKILLS_BASE):
            if d.startswith("reel_"):
                processed.add(d.replace("reel_", ""))
    
    remaining = [r for r in reels if extract_reel_code(r['url']) not in processed]
    
    print(f"Total reels: {len(reels)}")
    print(f"Already processed: {len(processed)}")
    print(f"Remaining: {len(remaining)}")
    
    if not remaining:
        print("✅ All reels processed!")
        return
    
    # Process with limited parallelism
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for i, reel in enumerate(remaining):
            if i > 0:
                time.sleep(RATE_LIMIT_DELAY)
            future = executor.submit(process_single_reel, reel, COOKIES_FILE, VAULT_BASE, SKILLS_BASE, OUTPUT_BASE)
            futures[future] = extract_reel_code(reel['url'])
        
        for future in as_completed(futures):
            code = futures[future]
            try:
                result = future.result(timeout=300)
                results.append(result)
                status = "✅" if result["status"] == "success" else "❌"
                print(f"\n{status} {code}: {result['status']} ({result.get('discipline', 'N/A')})")
                if result["status"] == "failed":
                    print(f"   Error: {result.get('error', 'Unknown')}")
            except Exception as e:
                results.append({"code": code, "status": "failed", "error": str(e)})
                print(f"\n❌ {code}: Exception - {e}")
    
    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    print(f"✅ Success: {success}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Vault: {VAULT_BASE}")
    print(f"🔧 Skills: {SKILLS_BASE}")
    print(f"💾 Archive: {OUTPUT_BASE}")

if __name__ == "__main__":
    main()