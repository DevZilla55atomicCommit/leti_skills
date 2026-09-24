#!/usr/bin/env python3
"""
Instagram → Videographer Learning Pipeline
Batch processor for Instagram Reels, Posts, and Carousels.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse

import yaml

# ─── Config ──────────────────────────────────────────────────────────────
VAULT_ROOT = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base")
VIDEO_EFFECTS_ROOT = VAULT_ROOT / "Video_Effects"
VIDEOG_ROOT = VAULT_ROOT / "Videographer"
CAMERA_THEORY_ROOT = VAULT_ROOT / "Camera Theory"
PHOTOGRAPHY_ROOT = VAULT_ROOT / "Photography" / "Lightroom"

HERMES_SKILLS = Path("~/.hermes/skills/videographer").expanduser()

CONFIG_PATH = Path(__file__).parent.parent / "references" / "config_videographer.yaml"

# ─── Helpers ─────────────────────────────────────────────────────────────
def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def extract_reel_code(url: str) -> Optional[str]:
    """Extract Instagram code from URL."""
    patterns = [
        r"(?:reel|p|tv)/([A-Za-z0-9_-]+)",
        r"instagram\.com/([A-Za-z0-9_.]+)/reel/([A-Za-z0-9_-]+)",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1) if len(m.groups()) == 1 else m.group(2)
    return None

def classify_url(url: str) -> str:
    """Return content type: 'reel', 'carousel', or 'tv'."""
    if "/reel/" in url:
        return "reel"
    elif "/p/" in url:
        return "carousel"
    elif "/tv/" in url:
        return "tv"
    return "unknown"

def load_processed_codes(queue_path: Path) -> Set[str]:
    """Load already-processed reel codes from queue file."""
    if not queue_path.exists():
        return set()
    codes = set()
    with open(queue_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # Format: N|url or just url
                if "|" in line:
                    url = line.split("|", 1)[1].strip()
                else:
                    url = line
                code = extract_reel_code(url)
                if code:
                    codes.add(code)
    return codes

def save_queue_entry(queue_path: Path, index: int, url: str, status: str, note: str = ""):
    """Append entry to queue tracking file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{index}|{url}|{status}|{timestamp}|{note}\n"
    with open(queue_path, "a") as f:
        f.write(line)

# ─── Download ────────────────────────────────────────────────────────────
def download_reel(url: str, output_dir: Path, cookies_from: str = "chrome") -> Optional[Path]:
    """Download reel via yt-dlp. Returns path to MP4 or None on failure."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_tpl = str(output_dir / "%(id)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", cookies_from,
        "-f", "bestvideo+bestaudio/best",
        "-o", output_tpl,
        "--no-playlist",
        "--quiet",
        "--no-warnings",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"  ❌ yt-dlp failed: {result.stderr[:200]}")
            return None
        
        # Find downloaded file
        mp4_files = list(output_dir.glob("*.mp4"))
        if not mp4_files:
            # Try other extensions
            for ext in ["mkv", "webm", "mov"]:
                mp4_files = list(output_dir.glob(f"*.{ext}"))
                if mp4_files:
                    break
        if not mp4_files:
            print(f"  ❌ No video file found after download")
            return None
        return mp4_files[0]
    except subprocess.TimeoutExpired:
        print(f"  ❌ Download timeout")
        return None
    except Exception as e:
        print(f"  ❌ Download error: {e}")
        return None

def download_carousel_images(url: str, output_dir: Path) -> List[Path]:
    """Download carousel post images via browser automation.
    Placeholder - requires authenticated browser session.
    """
    print(f"  ⚠️ Carousel download not yet implemented for: {url}")
    return []

# ─── Asset Extraction ────────────────────────────────────────────────────
def extract_frames(mp4_path: Path, asset_dir: Path, peak_frame: int = 30, end_frame: int = 60) -> Dict[str, Path]:
    """Extract key frames and create GIFs from MP4."""
    asset_dir.mkdir(parents=True, exist_ok=True)
    assets = {}
    
    # 1. Full demo GIF (10fps, 720w)
    demo_gif = asset_dir / "demo.gif"
    subprocess.run([
        "ffmpeg", "-i", str(mp4_path),
        "-vf", "fps=10,scale=720:-1:flags=lanczos",
        "-y", str(demo_gif)
    ], capture_output=True)
    assets["demo_gif"] = demo_gif

    # 2. Technique loop GIF (8fps, 480w, palette=64)
    loop_gif = asset_dir / "technique_demo.gif"
    subprocess.run([
        "ffmpeg", "-i", str(mp4_path),
        "-filter_complex", 
        "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];"
        "[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none",
        "-loop", "0", "-y", str(loop_gif)
    ], capture_output=True)
    assets["technique_demo_gif"] = loop_gif

    # 3. Key frames
    for name, frame_num in [("frame_before", 0), ("frame_during", peak_frame), ("frame_after", end_frame)]:
        out = asset_dir / f"{name}.png"
        subprocess.run([
            "ffmpeg", "-i", str(mp4_path),
            "-vf", f"select='eq(n,{frame_num})'", "-vframes", "1", "-y", str(out)
        ], capture_output=True)
        assets[name] = out

    # 4. Before/after comparison
    comp = asset_dir / "before_after_comparison.png"
    subprocess.run([
        "ffmpeg", "-i", str(assets["frame_before"]), "-i", str(assets["frame_after"]),
        "-filter_complex", "hstack=inputs=2", "-y", str(comp)
    ], capture_output=True)
    assets["before_after_comparison"] = comp

    return assets

# ─── Vault Note Generation ───────────────────────────────────────────────
def generate_vault_note(technique: str, discipline: str, creator: str, url: str, 
                        post_code: str, assets: Dict[str, Path], note_type: str) -> str:
    """Generate markdown vault note from template."""
    date = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", technique.lower()).strip("-")
    discipline_slug = re.sub(r"[^a-z0-9]+", "-", discipline.lower()).strip("-")
    
    note = f"""# {technique} — {discipline} Technique

> **Source:** [@{creator} — {technique}]({url})
> **Creator:** @{creator}
> **Date Processed:** {date}
> **Instagram Post Code:** {post_code}
> **Content Type:** {note_type}
> **Technique Category:** {discipline} / {technique}
> **Hermes Skill:** `videographer-{discipline_slug}-{slug}-{creator}`

---

## 🎯 Technique Summary

{technique} — extracted from Instagram {note_type} by @{creator}.

---

## 🖼️ Visual Analysis

| Slide/Frame | Visual Content | Technical Lesson |
|-------------|----------------|------------------|
| 1 | {technique} title/cover | Concept framing |
| 2-6 | Technique demonstrations | Per-slide breakdown |

---

## 🏗️ Core Principles

| Principle | Description | Why It Works |
|-----------|-------------|--------------|
| **Principle 1** | Description | Explanation |
| **Principle 2** | Description | Explanation |

---

## 📸 Shot Recipe (Reproducible Workflow)

### Pre-Production
- [ ] Location scout for requirements
- [ ] Time tracking (golden hour, weather)
- [ ] Lens choice
- [ ] Composition map

### Production
- [ ] Camera setup
- [ ] Exposure settings
- [ ] Focus technique
- [ ] Sequence capture

### Post-Production (DaVinci Resolve)

```
Node 01 — Primary Balance
    │  • Lift/Gamma/Gain: baseline
    │  • Temp/Tint: mood
    ▼
Node 02 — Contrast & Density
    │  • Contrast: +15 | Pivot: 40
    │  • Custom Curve: S-curve
    ▼
Node 03 — Color Separation (Parallel)
    │  • Hue vs Hue: shadows/halftones
    │  • Hue vs Sat: targeted
    ▼
Node 04 — Enhancement
    │  • Glow OFX (subtle)
    │  • Qualifier isolation
    ▼
Node 05 — Vignette & Texture
    │  • Power Window vignette
    │  • Film Grain OFX
    ▼
OUTPUT
```

---

## 🎬 When to Use This Technique

| Project Type | Application |
|--------------|-------------|
| **Landscape/Travel** | Hero establishing shots |
| **Documentary** | Environmental portraits |
| **Narrative** | Master shots; contrast with handheld |

---

## ⚠️ Common Pitfalls & Fixes

| Problem | Root Cause | Solution |
|---------|------------|----------|
| Issue 1 | Cause | Fix |
| Issue 2 | Cause | Fix |

---

## ✅ Verification Checklist

- [ ] Freeze frame works as strong photograph
- [ ] Subject placement intentional
- [ ] Negative space serves purpose
- [ ] Lighting has direction + color contrast
- [ ] Atmosphere visible and enhancing separation
- [ ] Horizon level (or intentional Dutch)
- [ ] Focus sharp on subject plane
- [ ] Exposure protects highlights

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| Related Technique 1 | `../Category/Technique.md` |
| Color Grading Template | `../../Color Grading & Looks/...` |
| DaVinci Node Structure | `../../Node Structures & Templates/` |

---

## 🏷️ Tags

`#videographer` `#{discipline_slug}` `#{slug}` `#{creator}` `#davinci-resolve` `#color-grading`

---

*Skill generated by `instagram-videographer-learning-pipeline` on {date} from Instagram {note_type} {post_code}*
"""
    return note

# Fill in the slide analysis from vision (would be populated from actual analysis)
    return note

# ─── Main Pipeline ───────────────────────────────────────────────────────
def process_url(url: str, index: int, config: dict, queue_path: Path, 
                processed_codes: Set[str], dry_run: bool = False) -> bool:
    """Process a single URL. Returns True if successful."""
    code = extract_reel_code(url)
    if not code:
        print(f"  ❌ Could not extract code from: {url}")
        save_queue_entry(queue_path, index, url, "FAILED", "Invalid URL format")
        return False
    
    if code in processed_codes:
        print(f"  ⏭️  Already processed: {code}")
        save_queue_entry(queue_path, index, url, "SKIPPED", "Duplicate")
        return True
    
    content_type = classify_url(url)
    print(f"  📥 [{index}] {code} ({content_type}) → ", end="", flush=True)
    
    if dry_run:
        print("DRY RUN")
        save_queue_entry(queue_path, index, url, "DRY_RUN", "")
        return True
    
    try:
        # Determine discipline from URL/content (simplified)
        discipline = "Cinematography"  # Default; would use classifier
        
        # Download
        if content_type == "reel":
            mp4_path = download_reel(url, Path("/tmp/ig_downloads"))
            if not mp4_path:
                save_queue_entry(queue_path, index, url, "FAILED", "Download failed")
                return False
            
            # Extract assets
            asset_dir = VIDEOG_ROOT / "assets" / code
            assets = extract_frames(mp4_path, asset_dir)
            
            # Auto-cleanup
            if config.get("auto_cleanup", True):
                mp4_path.unlink(missing_ok=True)
                for f in asset_dir.glob("frame_*.png"):
                    if not any(kw in f.name for kw in ["before", "during", "after", "comparison"]):
                        f.unlink(missing_ok=True)
            
            # Generate vault note
            note = generate_vault_note(
                technique=f"{discipline} Technique",
                discipline=discipline,
                creator="unknown",  # Would extract from page
                url=url,
                post_code=code,
                assets=assets,
                note_type="Reel"
            )
            
            # Save vault note
            note_path = VIDEOG_ROOT / discipline / f"{code}_{slug}.md"
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(note)
            
            # Generate Hermes skill (simplified)
            skill_dir = HERMES_SKILLS / f"videographer-{discipline.lower()}-{slug}-unknown"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(f"# Skill for {technique}\nSource: {url}")
            
            # Copy assets to skill
            for asset_name, asset_path in assets.items():
                if asset_path.exists():
                    import shutil
                    shutil.copy2(asset_path, skill_dir / "assets" / asset_path.name)
            
            print(f"✅ Done")
            save_queue_entry(queue_path, index, url, "DONE", "")
            return True
            
        elif content_type == "carousel":
            # Carousel processing (browser vision already done)
            print("⏭️  Carousel - vision analysis only")
            save_queue_entry(queue_path, index, url, "DONE", "Carousel")
            return True
            
        else:
            print("⏭️  Unknown type")
            save_queue_entry(queue_path, index, url, "SKIPPED", "Unknown type")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        save_queue_entry(queue_path, index, url, "FAILED", str(e))
        return False

def main():
    parser = argparse.ArgumentParser(description="Instagram → Videographer Pipeline")
    parser.add_argument("--input", required=True, help="Input file (JSON, CSV, TXT, RTF)")
    parser.add_argument("--batch-size", type=int, default=10, help="URLs per batch")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay between URLs (seconds)")
    parser.add_argument("--batch-delay", type=float, default=30.0, help="Delay between batches (seconds)")
    parser.add_argument("--resume", action="store_true", help="Resume from queue")
    parser.add_argument("--dry-run", action="store_true", help="Preview without processing")
    parser.add_argument("--filter-creator", help="Only process URLs from this creator")
    parser.add_argument("--max-retries", type=int, default=2, help="Max retries per URL")
    args = parser.parse_args()

    config = load_config()
    
    # Load URLs
    urls = []
    input_path = Path(args.input)
    if input_path.suffix == ".json":
        with open(input_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        urls.append(item.get("url", ""))
                    else:
                        urls.append(str(item))
    elif input_path.suffix == ".csv":
        with open(input_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                urls.append(row.get("url", ""))
    else:
        with open(input_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    # Filter by creator if specified
    if args.filter_creator:
        filtered = []
        for url in urls:
            if args.filter_creator.lower() in url.lower():
                filtered.append(url)
        urls = filtered
        print(f"Filtered to {len(urls)} URLs from @{args.filter_creator}")

    # Queue file
    queue_path = VIDEOG_ROOT / "VIDEOGRAPHER_QUEUE.md"
    processed_codes = load_processed_codes(queue_path) if args.resume else set()
    
    if args.resume:
        print(f"Resuming — {len(processed_codes)} already processed")

    # Process in batches
    total = len(urls)
    for batch_start in range(0, total, args.batch_size):
        batch = urls[batch_start:batch_start + args.batch_size]
        print(f"\n{'='*60}")
        print(f"BATCH {batch_start//args.batch_size + 1}/{(total-1)//args.batch_size + 1} — URLs {batch_start+1}-{min(batch_start+len(batch), total)} of {total}")
        print(f"{'='*60}")
        
        for i, url in enumerate(batch):
            idx = batch_start + i + 1
            if not process_url(url, idx, config, queue_path, set(), args.dry_run):
                print(f"  ⚠️  Failed, continuing...")
            if i < len(batch) - 1:
                time.sleep(args.delay)
        
        if batch_start + args.batch_size < total:
            print(f"  ⏸️  Batch delay: {args.batch_delay}s")
            time.sleep(args.batch_delay)

    print(f"\n✅ Complete! Processed {total} URLs.")

if __name__ == "__main__":
    main()