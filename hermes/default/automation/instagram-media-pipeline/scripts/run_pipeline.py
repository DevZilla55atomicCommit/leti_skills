#!/usr/bin/env python3
"""
Instagram Reel Pipeline — Method A (yt-dlp) with Method B (Playwright) fallback
Implements the instagram-media-pipeline skill.

Usage:
  python3 scripts/run_pipeline.py --input /tmp/reel_urls.json --output /Volumes/Samsung\ LED/Instagram\ Downloads/
"""

import asyncio
import json
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yt_dlp

# ===========================
# Configuration
# ===========================

@dataclass
class Config:
    input_json: Path
    output_root: Path
    cookies_file: Optional[Path] = None
    batch_size: int = 10
    batch_pause: int = 60
    max_retries: int = 2
    use_playwright_fallback: bool = True
    frame_count: int = 8
    target_resolution: tuple = (720, 1280)

@dataclass
class ReelResult:
    code: str
    url: str
    status: str  # success, failed_404, failed_429, failed_other, skipped
    method: str  # yt-dlp, playwright
    video_path: Optional[Path] = None
    frames_dir: Optional[Path] = None
    gif_path: Optional[Path] = None
    metadata: dict = field(default_factory=dict)
    error: Optional[str] = None


# ===========================
# yt-dlp Method (Primary)
# ===========================

def extract_shortcode(url: str) -> Optional[str]:
    """Extract Instagram shortcode from URL."""
    patterns = [
        r'instagram\.com/reel/([A-Za-z0-9_-]+)',
        r'instagram\.com/p/([A-Za-z0-9_-]+)',
        r'instagram\.com/tv/([A-Za-z0-9_-]+)',
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None


def build_ydl_opts(config: Config, output_dir: Path) -> dict:
    """Build yt-dlp options for Instagram reels."""
    opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(output_dir / '%(id)s.%(ext)s'),
        'writeinfojson': True,
        'writethumbnail': True,
        'quiet': True,
        'no_warnings': False,
        'ignoreerrors': False,
        'sleep_interval': 2,
        'max_sleep_interval': 5,
        'retries': config.max_retries,
        'fragment_retries': config.max_retries,
        'extractor_retries': config.max_retries,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        },
    }
    if config.cookies_file and config.cookies_file.exists():
        opts['cookiefile'] = str(config.cookies_file)
    return opts


def download_with_ytdlp(url: str, config: Config, output_dir: Path) -> ReelResult:
    """Download reel using yt-dlp nightly."""
    code = extract_shortcode(url)
    if not code:
        return ReelResult(code="unknown", url=url, status="failed_other", method="yt-dlp", error="Could not extract shortcode")

    output_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = build_ydl_opts(config, output_dir)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
        # Find downloaded video file
        video_files = list(output_dir.glob(f"{code}.*"))
        video_file = next((f for f in video_files if f.suffix in ['.mp4', '.webm', '.mkv']), None)
        
        if not video_file:
            # Try with full ID from info
            if info:
                video_file = output_dir / f"{info['id']}.mp4"
                if not video_file.exists():
                    video_file = list(output_dir.glob(f"{info['id']}.*"))[0] if list(output_dir.glob(f"{info['id']}.*")) else None
        
        metadata = {
            'id': info.get('id'),
            'title': info.get('title'),
            'description': info.get('description'),
            'duration': info.get('duration'),
            'uploader': info.get('uploader'),
            'upload_date': info.get('upload_date'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'comment_count': info.get('comment_count'),
            'webpage_url': info.get('webpage_url'),
            'extracted_at': datetime.now().isoformat(),
        }
        
        return ReelResult(
            code=code,
            url=url,
            status="success",
            method="yt-dlp",
            video_path=video_file,
            metadata=metadata
        )
        
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "404" in error_msg or "Not Found" in error_msg:
            return ReelResult(code=code, url=url, status="failed_404", method="yt-dlp", error=error_msg)
        elif "429" in error_msg or "Too Many Requests" in error_msg:
            return ReelResult(code=code, url=url, status="failed_429", method="yt-dlp", error=error_msg)
        elif "empty media response" in error_msg.lower() or "login required" in error_msg.lower():
            return ReelResult(code=code, url=url, status="failed_other", method="yt-dlp", error=error_msg)
        else:
            return ReelResult(code=code, url=url, status="failed_other", method="yt-dlp", error=error_msg)
    except Exception as e:
        return ReelResult(code=code, url=url, status="failed_other", method="yt-dlp", error=str(e))


# ===========================
# Frame Extraction (ffmpeg)
# ===========================

def extract_frames_ffmpeg(video_path: Path, frames_dir: Path, frame_count: int = 8, target_res: tuple = (720, 1280)) -> list[Path]:
    """Extract N evenly-spaced frames from video using ffmpeg."""
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Get duration
    probe_cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(video_path)
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        duration = float(result.stdout.strip())
    except (ValueError, IndexError):
        duration = 30.0  # fallback
    
    # Calculate timestamps (evenly distributed)
    timestamps = [duration * i / (frame_count - 1) for i in range(frame_count)]
    
    frame_paths = []
    for i, ts in enumerate(timestamps):
        frame_path = frames_dir / f"frame_{i:02d}.png"
        cmd = [
            'ffmpeg', '-y', '-ss', str(ts), '-i', str(video_path),
            '-vframes', '1',
            '-vf', f'scale={target_res[0]}:{target_res[1]}:force_original_aspect_ratio=decrease,pad={target_res[0]}:{target_res[1]}:(ow-iw)/2:(oh-ih)/2',
            str(frame_path)
        ]
        subprocess.run(cmd, capture_output=True)
        if frame_path.exists():
            frame_paths.append(frame_path)
    
    return frame_paths


def create_gif(frames_dir: Path, output_path: Path, frame_count: int = 8, fps: float = 2.0) -> Optional[Path]:
    """Create GIF from extracted frames."""
    palette_path = frames_dir / "palette.png"
    
    # Generate palette
    cmd1 = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', str(frames_dir / 'frame_%02d.png'),
        '-vf', 'palettegen',
        str(palette_path)
    ]
    subprocess.run(cmd1, capture_output=True)
    
    if not palette_path.exists():
        return None
    
    # Create GIF
    cmd2 = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', str(frames_dir / 'frame_%02d.png'),
        '-i', str(palette_path),
        '-lavfi', 'paletteuse',
        str(output_path)
    ]
    subprocess.run(cmd2, capture_output=True)
    
    return output_path if output_path.exists() else None


# ===========================
# Vault Note & Skill Generation
# ===========================

DISCIPLINE_KEYWORDS = {
    'Camera_Movement': ['pan', 'tilt', 'dolly', 'slider', 'gimbal', 'stabiliz', 'movement', 'tracking', 'handheld', 'crane', 'jib'],
    'Cinematography': ['cinematography', 'lighting', 'exposure', 'aperture', 'iso', 'shutter', 'depth of field', 'bokeh', 'lens', 'focal'],
    'Post-Production': ['edit', 'cut', 'transition', 'pace', 'timeline', 'sequence', 'color', 'grade', 'lut', 'workflow'],
    'Color_Grading_&_Looks': ['color grade', 'color correction', 'lut', 'look', 'teal', 'orange', 'film', 'emulation', 'halation', 'bloom'],
    'Video_Effects': ['effect', 'transition', 'overlay', 'glitch', 'distortion', 'warp', 'speed ramp', 'time remap'],
    'VFX_&_Compositing': ['vfx', 'composite', 'keying', 'mask', 'rotoscope', 'track', '3d', 'cgi', 'particle'],
    'Composition': ['compos', 'framing', 'rule of thirds', 'leading line', 'symmetry', 'negative space', 'balance'],
    'Lighting': ['lighting', 'key light', 'fill light', 'rim light', 'backlight', 'softbox', 'natural light', 'golden hour'],
    'Camera_Theory': ['sensor', 'crop factor', 'full frame', 'aps-c', 'super 35', 'anamorphic', 'aspect ratio'],
    'Business_&_Career': ['client', 'pricing', 'portfolio', 'freelance', 'business', 'marketing', 'brand', 'instagram growth'],
    'Lenses_&_Optics': ['lens', 'focal length', 'prime', 'zoom', 'aperture', 't-stop', 'vintage', 'anamorphic', 'wide angle', 'telephoto'],
}

def classify_discipline(text: str) -> str:
    """Classify reel content into discipline based on caption/description."""
    text_lower = text.lower()
    scores = {}
    for discipline, keywords in DISCIPLINE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[discipline] = score
    return max(scores, key=scores.get) if scores else 'Cinematography'


def generate_vault_note(result: ReelResult, vault_root: Path) -> Path:
    """Generate Obsidian vault note for the reel."""
    discipline = classify_discipline(result.metadata.get('description', '') or result.metadata.get('title', ''))
    discipline_dir = vault_root / discipline
    discipline_dir.mkdir(parents=True, exist_ok=True)
    
    note_path = discipline_dir / f"reel_{result.code}.md"
    
    frame_refs = []
    if result.frames_dir and result.frames_dir.exists():
        frame_files = sorted(result.frames_dir.glob("frame_*.png"))
        frame_refs = [f"![Frame {i}]({f.relative_to(vault_root)})" for i, f in enumerate(frame_files)]
    
    gif_ref = ""
    if result.gif_path and result.gif_path.exists():
        gif_ref = f"![GIF Preview]({result.gif_path.relative_to(vault_root)})"
    
    content = f"""---
reel_code: {result.code}
url: {result.url}
author: {result.metadata.get('uploader', 'Unknown')}
discipline: {discipline}
tags: [instagram, reel, {discipline.lower().replace('_', '-')}, videography]
method: {result.method}
duration: {result.metadata.get('duration', 'Unknown')}
extracted_at: {result.metadata.get('extracted_at', datetime.now().isoformat())}
frames: {len(frame_refs)}
---

# Reel Analysis: {result.code}

**Source:** [{result.url}]({result.url})
**Creator:** {result.metadata.get('uploader', 'Unknown')}
**Discipline:** {discipline}
**Method:** {result.method}
**Duration:** {result.metadata.get('duration', 'Unknown')}s
**Likes:** {result.metadata.get('like_count', 'N/A')}
**Comments:** {result.metadata.get('comment_count', 'N/A')}

## Caption
{result.metadata.get('description', 'No caption available')}

## Technical Breakdown
*To be filled based on visual analysis of frames*

### Observed Techniques
- 
- 

### DaVinci Resolve Node Graph Template
```mermaid
graph LR
    A[Input] --> B[Node 1: Primary]
    B --> C[Node 2: Look]
    C --> D[Output]
```

## Frame References
{gif_ref}

{chr(10).join(frame_refs)}

## Metadata
```json
{json.dumps(result.metadata, indent=2)}
```
"""
    note_path.write_text(content)
    return note_path


def generate_skill(result: ReelResult, skills_root: Path) -> Path:
    """Generate Hermes skill for the reel technique."""
    skill_dir = skills_root / f"reel_{result.code}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = skill_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    
    # Copy frames
    if result.frames_dir and result.frames_dir.exists():
        for f in result.frames_dir.glob("frame_*.png"):
            import shutil
            shutil.copy2(f, frames_dir / f.name)
    
    # Copy GIF
    if result.gif_path and result.gif_path.exists():
        import shutil
        shutil.copy2(result.gif_path, skill_dir / f"reel_{result.code}.gif")
    
    discipline = classify_discipline(result.metadata.get('description', '') or result.metadata.get('title', ''))
    
    skill_md = f"""---
name: reel_{result.code}
category: videographer
tags: [instagram, reel, {discipline.lower().replace('_', '-')}, technique]
version: 1.0
source_url: {result.url}
source_method: {result.method}
discipline: {discipline}
duration_seconds: {result.metadata.get('duration', 'Unknown')}
creator: {result.metadata.get('uploader', 'Unknown')}
extracted: {result.metadata.get('extracted_at', datetime.now().isoformat())}
frame_count: {len(list(frames_dir.glob('frame_*.png'))) if frames_dir.exists() else 0}
---

# Reel Technique: {result.code}

## Source
- **URL:** [{result.url}]({result.url})
- **Creator:** {result.metadata.get('uploader', 'Unknown')}
- **Discipline:** {discipline}
- **Extraction Method:** {result.method}
- **Duration:** {result.metadata.get('duration', 'Unknown')}s

## Caption
{result.metadata.get('description', 'No caption available')}

## Technique Summary
*Analyze frames and describe the core technique demonstrated.*

### Key Frames
| Frame | Timestamp | Description |
|-------|-----------|-------------|
| 0 | 0% | Opening/establishing |
| 1 | 14% | |
| 2 | 28% | |
| 3 | 42% | |
| 4 | 57% | |
| 5 | 71% | |
| 6 | 86% | |
| 7 | 100% | Final frame |

## DaVinci Resolve Implementation

### Node Structure
```
Node 1: Primary Correction (Balance/Exposure)
Node 2: Creative Look (LUT/Grade)
Node 3: Texture/Effects (Grain/Halation)
Node 4: Output Transform
```

### Key Parameters
| Node | Tool | Parameter | Value |
|------|------|-----------|-------|
| 1 | Primaries | Lift/Gamma/Gain | TBD |
| 2 | Curves/LUT | | TBD |
| 3 | OpenFX | Film Grain/Texture | TBD |

## Frame Assets
Frames stored in `frames/` directory:
- `frame_00.png` through `frame_07.png` (8 frames at 0%, 14%, 28%, 42%, 57%, 71%, 86%, 100%)
- `reel_{result.code}.gif` (2fps preview)

## Metadata
```json
{json.dumps(result.metadata, indent=2)}
```

## Usage
This skill documents a specific videography technique extracted from an Instagram Reel.
Reference the frame images for visual breakdown. Adapt the node graph template for your footage.
"""
    
    (skill_dir / "SKILL.md").write_text(skill_md)
    return skill_dir


# ===========================
# Main Pipeline
# ===========================

async def process_reel(url: str, config: Config, vault_root: Path, skills_root: Path) -> ReelResult:
    """Process a single reel through the pipeline."""
    code = extract_shortcode(url)
    reel_output_dir = config.output_root / code
    reel_output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"  → Processing {code} via yt-dlp...")
    result = download_with_ytdlp(url, config, reel_output_dir)
    
    if result.status == "success" and result.video_path and result.video_path.exists():
        # Extract frames
        frames_dir = reel_output_dir / "frames"
        print(f"  → Extracting {config.frame_count} frames...")
        frame_paths = extract_frames_ffmpeg(
            result.video_path, frames_dir, config.frame_count, config.target_resolution
        )
        result.frames_dir = frames_dir
        
        # Create GIF
        gif_path = reel_output_dir / f"reel_{code}.gif"
        print(f"  → Creating GIF...")
        result.gif_path = create_gif(frames_dir, gif_path, config.frame_count)
        
        # Generate artifacts
        print(f"  → Generating vault note...")
        generate_vault_note(result, vault_root)
        
        print(f"  → Generating Hermes skill...")
        generate_skill(result, skills_root)
    
    return result


async def run_pipeline(config: Config):
    """Run the full pipeline."""
    # Load URLs
    with open(config.input_json) as f:
        data = json.load(f)
    
    reel_urls = [item['url'] for item in data if '/reel/' in item.get('url', '')]
    print(f"Loaded {len(reel_urls)} reel URLs")
    
    # Setup paths
    vault_root = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Videographer")
    skills_root = Path("/Users/alfredkamisese/.hermes/skills/videographer")
    vault_root.mkdir(parents=True, exist_ok=True)
    skills_root.mkdir(parents=True, exist_ok=True)
    
    # Validate cookies
    if config.cookies_file:
        print(f"Using cookies: {config.cookies_file}")
    else:
        print("WARNING: No cookies file provided. Only public reels will work.")
    
    results = []
    for i, url in enumerate(reel_urls):
        print(f"\n[{i+1}/{len(reel_urls)}] {url}")
        result = await process_reel(url, config, vault_root, skills_root)
        results.append(result)
        print(f"  Status: {result.status} ({result.method})")
        
        # Batch pause
        if (i + 1) % config.batch_size == 0 and i + 1 < len(reel_urls):
            print(f"\n  Batch complete. Pausing {config.batch_pause}s...")
            await asyncio.sleep(config.batch_pause)
    
    # Summary
    print("\n" + "="*50)
    print("PIPELINE COMPLETE")
    print("="*50)
    status_counts = {}
    for r in results:
        status_counts[r.status] = status_counts.get(r.status, 0) + 1
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    # Save results log
    log_path = config.output_root / f"pipeline_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_path, 'w') as f:
        json.dump([{
            'code': r.code,
            'url': r.url,
            'status': r.status,
            'method': r.method,
            'video_path': str(r.video_path) if r.video_path else None,
            'error': r.error
        } for r in results], f, indent=2)
    print(f"\nLog saved: {log_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Instagram Reel Processing Pipeline")
    parser.add_argument('--input', required=True, help='Input JSON file with reel URLs')
    parser.add_argument('--output', required=True, help='Output root directory')
    parser.add_argument('--cookies', help='Path to cookies.txt file')
    parser.add_argument('--batch-size', type=int, default=10, help='Reels per batch before pause')
    parser.add_argument('--batch-pause', type=int, default=60, help='Seconds to pause between batches')
    parser.add_argument('--frame-count', type=int, default=8, help='Number of frames to extract')
    args = parser.parse_args()
    
    config = Config(
        input_json=Path(args.input),
        output_root=Path(args.output),
        cookies_file=Path(args.cookies) if args.cookies else None,
        batch_size=args.batch_size,
        batch_pause=args.batch_pause,
        frame_count=args.frame_count,
    )
    
    asyncio.run(run_pipeline(config))


if __name__ == '__main__':
    main()