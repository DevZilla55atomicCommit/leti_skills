#!/usr/bin/env python3
"""
Instagram → DaVinci Video Effects Learning Pipeline
Main executor script for processing Instagram Reels into structured knowledge base.

Usage:
    python run_pipeline.py --input urls.json --batch-size 10
    python run_pipeline.py --input urls.csv --dry-run
    python run_pipeline.py --input urls.txt --retry-failed
"""

import argparse
import json
import csv
import re
import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import yaml

# Configuration
CONFIG_PATH = Path(__file__).parent.parent / "references" / "config_video_effects.yaml"
VAULT_BASE = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects")
SKILLS_BASE = Path("/Users/alfredkamisese/.hermes/skills/video-effects")
QUEUE_FILE = VAULT_BASE / "VIDEO_EFFECTS_QUEUE.json"
PROCESSED_FILE = VAULT_BASE / "PROCESSED_REELS.json"

# Load config
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

CATEGORIES = CONFIG.get("categories", [])
SKIP_PATTERNS = CONFIG.get("skip_patterns", [])
CAMERA_THEORY_KEYWORDS = CONFIG.get("camera_theory_keywords", [])
LIGHTROOM_KEYWORDS = CONFIG.get("lightroom_mobile_keywords", [])


def load_processed() -> set:
    """Load already processed reel codes."""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE) as f:
            return set(json.load(f))
    return set()


def save_processed(processed: set):
    """Save processed reel codes."""
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(processed), f)


def parse_input_file(input_path: str) -> List[Dict]:
    """Parse input file (JSON, CSV, TXT, RTF) and extract URLs."""
    path = Path(input_path)
    urls = []
    
    if path.suffix == '.json':
        with open(path) as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        urls.append({"url": item, "creator": "", "notes": "", "priority": "Normal"})
                    elif isinstance(item, dict):
                        urls.append({
                            "url": item.get("url", ""),
                            "creator": item.get("creator", ""),
                            "notes": item.get("notes", ""),
                            "priority": item.get("priority", "Normal")
                        })
    
    elif path.suffix == '.csv':
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                urls.append({
                    "url": row.get("url", "").strip(),
                    "creator": row.get("creator", "").strip(),
                    "notes": row.get("notes", "").strip(),
                    "priority": row.get("priority", "Normal").strip()
                })
    
    elif path.suffix in ['.txt', '.rtf']:
        with open(path) as f:
            content = f.read()
            # Extract URLs from text/RTF
            url_pattern = r'https?://(?:www\.)?instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)'
            for match in re.finditer(url_pattern, content):
                urls.append({
                    "url": match.group(0),
                    "creator": "",
                    "notes": "",
                    "priority": "Normal"
                })
    
    return urls


def extract_reel_code(url: str) -> Optional[str]:
    """Extract reel code from Instagram URL."""
    match = re.search(r'(?:reel|p)/([A-Za-z0-9_-]+)', url)
    return match.group(1) if match else None


def classify_effect(url: str, caption: str = "", hashtags: List[str] = None) -> Tuple[str, str, List[str]]:
    """Classify effect based on caption and hashtags."""
    text = (caption + " " + " ".join(hashtags or [])).lower()
    
    # Check skip patterns first
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "skip", pattern, []
    
    # Check camera theory keywords
    for kw in CAMERA_THEORY_KEYWORDS:
        if kw.lower() in text:
            return "camera_theory", kw, []
    
    # Check lightroom/mobile keywords
    for kw in LIGHTROOM_KEYWORDS:
        if kw.lower() in text:
            return "photography_lightroom", kw, []
    
    # Check category keywords
    for cat in CATEGORIES:
        for kw in cat.get("keywords", []):
            if kw.lower() in text:
                return cat["name"], kw, cat.get("keywords", [])
    
    return "unknown", "", []


def check_availability(url: str) -> Dict:
    """Check if reel is publicly accessible."""
    # This would use browser automation in production
    # For now, return mock data structure
    return {
        "available": True,
        "reason": "",
        "caption": "",
        "hashtags": [],
        "creator": "",
        "date": ""
    }


def download_reel(url: str, output_dir: Path) -> Optional[Path]:
    """Download reel using yt-dlp with Chrome cookies."""
    code = extract_reel_code(url)
    if not code:
        return None
    
    output_path = output_dir / f"{code}.mp4"
    
    if output_path.exists():
        return output_path
    
    try:
        cmd = [
            "yt-dlp",
            "--cookies-from-browser", "chrome",
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "-o", str(output_path),
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and output_path.exists():
            return output_path
        else:
            print(f"Download failed for {url}: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"Download timeout for {url}")
        return None
    except Exception as e:
        print(f"Download error for {url}: {e}")
        return None


def extract_frames(video_path: Path, output_dir: Path) -> List[Path]:
    """Extract key frames from video."""
    frames = []
    try:
        # Extract frames at 10fps
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-vf", "fps=10,scale=720:-1:flags=lanczos",
            str(output_dir / "frame_%03d.png")
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        
        frames = sorted(output_dir.glob("frame_*.png"))
        return frames
    except Exception as e:
        print(f"Frame extraction error: {e}")
        return []


def create_gif(video_path: Path, output_path: Path, start_sec: float = 0, duration: float = 3) -> bool:
    """Create optimized GIF from video segment."""
    try:
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-ss", str(start_sec), "-t", str(duration),
            "-vf", "fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none",
            "-loop", "0", str(output_path)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        # Optimize with gifsicle
        subprocess.run(["gifsicle", "-O3", "--lossy=80", str(output_path), "-o", str(output_path)], capture_output=True)
        return output_path.exists()
    except Exception as e:
        print(f"GIF creation error: {e}")
        return False


def create_before_after(frame_before: Path, frame_after: Path, output_path: Path) -> bool:
    """Create side-by-side comparison."""
    try:
        cmd = ["ffmpeg", "-i", str(frame_before), "-i", str(frame_after), 
               "-filter_complex", "hstack=inputs=2", str(output_path)]
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path.exists()
    except Exception as e:
        print(f"Comparison creation error: {e}")
        return False


def generate_vault_note(reel_data: Dict, classification: Dict, assets: Dict) -> str:
    """Generate vault note from template."""
    template_path = Path(__file__).parent.parent / "templates" / "vault_note_template.md"
    with open(template_path) as f:
        template = f.read()
    
    # Simple template substitution
    replacements = {
        "{{EFFECT_NAME}}": reel_data.get("effect_name", "Unknown Effect"),
        "{{SOURCE_HANDLE}}": reel_data.get("creator", "unknown"),
        "{{TECHNIQUE_SLUG}}": reel_data.get("slug", "unknown"),
        "{{SOURCE}}": reel_data.get("creator", "unknown"),
        "{{KEY_TOOLS}}": reel_data.get("tools", "unknown"),
        "{{CAPTION_EXCERPT}}": reel_data.get("caption", "")[:80],
        "{{TIME_AGO}}": reel_data.get("date", "recent"),
        "{{TECHNIQUE_NAME}}": classification.get("category", "Unknown"),
        "{{EFFECT_CATEGORY}}": classification.get("category", "Unknown").lower().replace(" ", "-"),
        "{{DATE}}": datetime.now().strftime("%Y-%m-%d"),
        "{{REEL_CODE}}": reel_data.get("code", ""),
    }
    
    for k, v in replacements.items():
        template = template.replace(k, str(v))
    
    return template


def generate_skill(reel_data: Dict, classification: Dict, assets: Dict) -> str:
    """Generate Hermes skill from template."""
    template_path = Path(__file__).parent.parent / "templates" / "skill_template.md"
    with open(template_path) as f:
        template = f.read()
    
    replacements = {
        "{{EFFECT_NAME}}": reel_data.get("effect_name", "Unknown Effect"),
        "{{SOURCE_HANDLE}}": reel_data.get("creator", "unknown"),
        "{{TECHNIQUE_SLUG}}": reel_data.get("slug", "unknown"),
        "{{REEL_CODE}}": reel_data.get("code", ""),
        "{{CAPTION_EXCERPT}}": reel_data.get("caption", "")[:80],
        "{{HASHTAGS}}": ", ".join(reel_data.get("hashtags", [])),
        "{{DAVINCI_PAGES}}": "Fusion, Color",
        "{{DIFFICULTY}}": "Intermediate",
        "{{ESTIMATED_TIME}}": "15-30 minutes",
        "{{TECHNIQUE_NAME}}": classification.get("category", "Unknown"),
        "{{EFFECT_CATEGORY}}": classification.get("category", "Unknown"),
        "{{KEY_TAGS}}": ", ".join(classification.get("keywords", [])),
        "{{DATE}}": datetime.now().strftime("%Y-%m-%d"),
        "{{MASK_TOOL}}": "PolygonMask",
        "{{MASK_PARAM_1}}": "15-30 points around subject",
        "{{MASK_PARAM_2}}": "Soft Edge: 3-5px",
        "{{TRACKER_SETTINGS}}": "Position + Rotation + Scale",
        "{{NUM_POINTS}}": "15-30",
        "{{MASK_REASON}}": "Precise vertex control",
        "{{SOFTNESS}}": "3-5",
        "{{SHAPE_DETAILS}}": "Custom polygon around subject",
        "{{WINDOW_TYPE}}": "Polygon",
        "{{SHAPE_REASON}}": "Precise subject outline",
    }
    
    for k, v in replacements.items():
        template = template.replace(k, str(v))
    
    return template


def process_reel(reel: Dict, processed: set, dry_run: bool = False) -> Dict:
    """Process a single reel."""
    code = extract_reel_code(reel["url"])
    if not code:
        return {"code": "unknown", "status": "error", "reason": "Could not extract reel code"}
    
    if code in processed:
        return {"code": code, "status": "skipped", "reason": "Already processed"}
    
    print(f"\n{'='*60}")
    print(f"Processing: {code} ({reel['url']})")
    print(f"{'='*60}")
    
    # Check availability
    availability = check_availability(reel["url"])
    if not availability["available"]:
        return {"code": code, "status": "unavailable", "reason": availability["reason"]}
    
    # Classify
    category, keyword, keywords = classify_effect(
        reel["url"], 
        availability.get("caption", ""), 
        availability.get("hashtags", [])
    )
    
    if category == "skip":
        return {"code": code, "status": "skipped", "reason": f"Skip pattern: {keyword}"}
    elif category == "camera_theory":
        return {"code": code, "status": "camera_theory", "reason": f"Camera theory: {keyword}"}
    elif category == "photography_lightroom":
        return {"code": code, "status": "photography", "reason": f"Lightroom/Mobile: {keyword}"}
    elif category == "unknown":
        return {"code": code, "status": "unknown", "reason": "Could not classify"}
    
    # Prepare reel data
    reel_data = {
        "code": code,
        "url": reel["url"],
        "creator": availability.get("creator") or reel.get("creator", "unknown"),
        "caption": availability.get("caption", ""),
        "hashtags": availability.get("hashtags", []),
        "date": availability.get("date", ""),
        "effect_name": availability.get("caption", "Unknown Effect").split("#")[0].strip()[:60],
        "slug": re.sub(r'[^a-z0-9]+', '-', availability.get("caption", "unknown-effect").lower().split("#")[0].strip())[:40],
        "tools": "PolygonMask + Tracker + AlphaDivide + Merge",
        "category": category
    }
    
    classification = {
        "category": category,
        "keyword": keyword,
        "keywords": keywords
    }
    
    if dry_run:
        print(f"  [DRY RUN] Category: {category}, Keyword: {keyword}")
        return {"code": code, "status": "dry_run", "category": category}
    
    # Create asset directories
    asset_dir = VAULT_BASE / "assets" / category.lower().replace(" ", "-") / reel_data["slug"]
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    skill_dir = SKILLS_BASE / f"davinci-resolve-{reel_data['slug']}"
    skill_asset_dir = skill_dir / "assets"
    skill_asset_dir.mkdir(parents=True, exist_ok=True)
    
    # Download video
    print(f"  Downloading video...")
    video_path = download_reel(reel["url"], asset_dir)
    if not video_path:
        return {"code": code, "status": "failed", "reason": "Download failed"}
    
    # Extract frames
    print(f"  Extracting frames...")
    frames = extract_frames(video_path, asset_dir)
    
    # Create GIFs
    print(f"  Creating GIFs...")
    demo_gif = asset_dir / "demo.gif"
    create_gif(video_path, demo_gif, 0, min(10, 24))  # Full demo up to 10s
    
    transition_gif = asset_dir / "transition_demo.gif"
    create_gif(video_path, transition_gif, 5, 3)  # 3s from 5s mark
    
    # Key frames
    frame_before = asset_dir / "frame_before.png"
    frame_during = asset_dir / "frame_during.png"
    frame_after = asset_dir / "frame_after.png"
    
    if len(frames) >= 3:
        import shutil
        shutil.copy(frames[0], frame_before)
        shutil.copy(frames[len(frames)//2], frame_during)
        shutil.copy(frames[-1], frame_after)
    
    # Before/after comparison
    comparison = asset_dir / "before_after_comparison.png"
    if frame_before.exists() and frame_after.exists():
        create_before_after(frame_before, frame_after, comparison)
    
    # Copy to skill assets
    for asset in [demo_gif, transition_gif, frame_before, frame_during, frame_after, comparison]:
        if asset.exists():
            shutil.copy(asset, skill_asset_dir / asset.name)
    
    # Generate vault note
    print(f"  Generating vault note...")
    assets = {
        "demo_gif": str(demo_gif.relative_to(VAULT_BASE)),
        "transition_gif": str(transition_gif.relative_to(VAULT_BASE)),
        "frame_before": str(frame_before.relative_to(VAULT_BASE)),
        "frame_during": str(frame_during.relative_to(VAULT_BASE)),
        "frame_after": str(frame_after.relative_to(VAULT_BASE)),
        "comparison": str(comparison.relative_to(VAULT_BASE)),
    }
    
    vault_note = generate_vault_note(reel_data, classification, assets)
    category_dir = VAULT_BASE / category.lower().replace(" ", "-")
    category_dir.mkdir(parents=True, exist_ok=True)
    
    # Find next number
    existing = list(category_dir.glob("*.md"))
    next_num = len([f for f in existing if f.name[0].isdigit()]) + 1
    vault_path = category_dir / f"{next_num:02d}-{reel_data['slug']}_{reel_data['creator']}_{reel_data['tools'].replace(' ', '-')}.md"
    
    with open(vault_path, 'w') as f:
        f.write(vault_note)
    
    # Generate skill
    print(f"  Generating Hermes skill...")
    skill_content = generate_skill(reel_data, classification, assets)
    skill_path = skill_dir / "SKILL.md"
    with open(skill_path, 'w') as f:
        f.write(skill_content)
    
    # Update tracking
    processed.add(code)
    save_processed(processed)
    
    return {
        "code": code,
        "status": "completed",
        "category": category,
        "vault_file": str(vault_path.relative_to(VAULT_BASE)),
        "skill_dir": str(skill_dir.relative_to(SKILLS_BASE.parent))
    }


def main():
    parser = argparse.ArgumentParser(description="Instagram → DaVinci Video Effects Pipeline")
    parser.add_argument("--input", required=True, help="Input file (JSON, CSV, TXT, RTF)")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for processing")
    parser.add_argument("--dry-run", action="store_true", help="Preview classifications without processing")
    parser.add_argument("--retry-failed", action="store_true", help="Retry previously failed URLs")
    parser.add_argument("--filter-creator", help="Filter to specific creator handle")
    args = parser.parse_args()
    
    # Load processed reels
    processed = load_processed()
    
    # Parse input
    print(f"Parsing input file: {args.input}")
    urls = parse_input_file(args.input)
    print(f"Found {len(urls)} URLs")
    
    # Filter by creator if specified
    if args.filter_creator:
        urls = [u for u in urls if args.filter_creator.lower() in u.get("creator", "").lower()]
        print(f"Filtered to {len(urls)} URLs for creator: {args.filter_creator}")
    
    # Filter already processed if not retry
    if not args.retry_failed:
        urls = [u for u in urls if extract_reel_code(u["url"]) not in processed]
        print(f"After dedup: {len(urls)} URLs to process")
    
    if args.dry_run:
        print("\n=== DRY RUN - Classifications ===")
        for url_data in urls[:args.batch_size]:
            code = extract_reel_code(url_data["url"])
            availability = check_availability(url_data["url"])
            category, keyword, keywords = classify_effect(
                url_data["url"], 
                availability.get("caption", ""), 
                availability.get("hashtags", [])
            )
            print(f"  {code}: {category} (keyword: {keyword})")
        return
    
    # Process in batches
    results = []
    for i in range(0, len(urls), args.batch_size):
        batch = urls[i:i+args.batch_size]
        print(f"\n--- Batch {i//args.batch_size + 1} ({len(batch)} URLs) ---")
        
        for url_data in batch:
            result = process_reel(url_data, processed, dry_run=False)
            results.append(result)
            time.sleep(2)  # Rate limiting
        
        # Save progress after each batch
        print(f"\nBatch complete. Processed: {sum(1 for r in results if r['status'] == 'completed')}")
    
    # Summary
    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    status_counts = {}
    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
    for status, count in status_counts.items():
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()