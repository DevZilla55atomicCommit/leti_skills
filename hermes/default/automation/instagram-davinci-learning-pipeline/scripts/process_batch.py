#!/usr/bin/env python3
"""
Video Effects Pipeline - Batch Processor
Processes Instagram Reels from queue into DaVinci Knowledge Base.

Usage:
    python process_batch.py --input urls.json --batch-size 10
    python process_batch.py --input urls.csv --dry-run
    python process_batch.py --input urls.txt --retry-failed
"""

import json
import csv
import re
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Set

# Configuration
CONFIG_PATH = Path(__file__).parent.parent / "references" / "config_video_effects.yaml"
VAULT_BASE = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects")
SKILLS_BASE = Path("/Users/alfredkamisese/.hermes/skills/video-effects")
QUEUE_FILE = Path("/tmp/reels_queue.json")
PROCESSED_FILE = VAULT_BASE / "PROCESSED_REELS.json"

# Load config
import yaml
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

CATEGORIES = CONFIG.get("categories", [])
SKIP_PATTERNS = CONFIG.get("skip_patterns", [])
CAMERA_THEORY_KEYWORDS = CONFIG.get("camera_theory_keywords", [])
LIGHTROOM_KEYWORDS = CONFIG.get("lightroom_mobile_keywords", [])


def check_tools():
    """Verify required tools are available"""
    for tool in ["yt-dlp", "ffmpeg", "ffprobe"]:
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            print(f"❌ Missing tool: {tool}")
            return False
    return True


def load_queue() -> List[Dict]:
    """Load reel queue from JSON"""
    with open(QUEUE_FILE) as f:
        return json.load(f)


def load_processed() -> set:
    """Load already processed reel codes"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE) as f:
            return set(json.load(f))
    return set()


def save_processed(processed: set):
    """Save processed reel codes"""
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(processed), f)


def parse_input_file(input_path: str) -> List[Dict]:
    """Parse input file (JSON, CSV, TXT, RTF) and extract URLs"""
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
            url_pattern = r'https?://(?:www\.)?instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)'
            for match in re.finditer(url_pattern, content):
                urls.append({
                    "url": match.group(0),
                    "creator": "",
                    "notes": "",
                    "priority": "Normal"
                })
    
    return urls


def classify_effect(url: str, caption: str = "", hashtags: List[str] = None) -> tuple:
    """Classify effect based on caption and hashtags"""
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


def extract_reel_code(url: str) -> Optional[str]:
    """Extract reel code from Instagram URL"""
    match = re.search(r'(?:reel|p)/([A-Za-z0-9_-]+)', url)
    return match.group(1) if match else None


def download_reel(url: str, output_dir: Path, reel_code: str) -> Optional[Path]:
    """Download reel using yt-dlp with Chrome cookies"""
    output_path = output_dir / f"{reel_code}.mp4"
    
    if output_path.exists():
        return output_path
    
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", "chrome",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", str(output_dir / f"{reel_code}.%(ext)s"),
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and output_path.exists():
            return output_path
        else:
            print(f"Download failed: {result.stderr[:200]}")
            return None
    except subprocess.TimeoutExpired:
        print(f"Download timeout: {url}")
        return None
    except Exception as e:
        print(f"Download error: {e}")
        return None


def extract_assets(video_path: Path, output_dir: Path) -> Dict[str, Path]:
    """Extract frames, GIFs, and comparison images"""
    assets = {}
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Extract frames (10fps, 720p)
    frame_pattern = output_dir / "frame_%03d.png"
    cmd = ["ffmpeg", "-i", str(video_path), "-vf", "fps=10,scale=720:-1:flags=lanczos", str(frame_pattern)]
    subprocess.run(cmd, capture_output=True)
    frames = sorted(output_dir.glob("frame_*.png"))
    if frames:
        assets["frame_before"] = frames[0] if frames else None
        assets["frame_during"] = frames[len(frames)//2] if len(frames) > 1 else None
        assets["frame_after"] = frames[-1] if len(frames) > 2 else None
    
    # 2. Create transition GIF (3s loop, 8fps, 480px)
    gif_path = output_dir / "transition_demo.gif"
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-filter_complex", "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none",
        "-loop", "0", "-t", "3", str(gif_path)
    ]
    subprocess.run(cmd, capture_output=True)
    if gif_path.exists():
        assets["transition_demo"] = gif_path
    
    # 3. Full demo GIF (full length, 10fps)
    demo_gif = output_dir / "demo.gif"
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-filter_complex", "[0:v]fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none",
        "-loop", "0", str(demo_gif)
    ]
    subprocess.run(cmd, capture_output=True)
    if demo_gif.exists():
        assets["demo"] = demo_gif
    
    # 4. Key frames
    for name, frame_num in [("frame_before", 0), ("frame_during", 30), ("frame_after", 60)]:
        out_path = output_dir / f"{name}.png"
        cmd = ["ffmpeg", "-i", str(video_path), "-vf", f"select='eq(n,{frame_num})'", "-vframes", "1", str(out_path)]
        subprocess.run(cmd, capture_output=True)
        if out_path.exists():
            assets[name] = out_path
    
    # 5. Before/After comparison
    if assets.get("frame_before") and assets.get("frame_after"):
        comp_path = output_dir / "before_after_comparison.png"
        cmd = ["ffmpeg", "-i", str(assets["frame_before"]), "-i", str(assets["frame_after"]),
               "-filter_complex", "hstack=inputs=2", str(comp_path)]
        subprocess.run(cmd, capture_output=True)
        if comp_path.exists():
            assets["before_after"] = comp_path
    
    return assets


def copy_to_skills(assets: Dict, reel_code: str, category: str, effect_slug: str):
    """Copy assets to Hermes skill directory"""
    skill_dir = Path(f"/Users/alfredkamisese/.hermes/skills/video-effects/davinci-resolve-{effect_slug}")
    skill_assets = skill_dir / "assets"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_assets.mkdir(parents=True, exist_ok=True)
    
    for name, src in assets.items():
        if src and src.exists():
            import shutil
            dst = skill_assets / src.name
            shutil.copy2(src, dst)


def generate_vault_note(reel_data: Dict, assets: Dict, category: str, effect_slug: str) -> str:
    """Generate vault markdown note from template"""
    template_path = Path(__file__).parent.parent / "templates" / "vault_note_template_video_effect.md"
    if not template_path.exists():
        return f"# {reel_data.get('effect_name', 'Unknown Effect')} — @{reel_data.get('creator', 'unknown')}\n\nTemplate not found."
    
    with open(template_path) as f:
        template = f.read()
    
    # Simple template substitution
    replacements = {
        "{{EFFECT_NAME}}": reel_data.get("effect_name", "Unknown Effect"),
        "{{SOURCE_HANDLE}}": reel_data.get("creator", "unknown"),
        "{{TECHNIQUE_SLUG}}": effect_slug,
        "{{SOURCE}}": reel_data.get("creator", "unknown"),
        "{{KEY_TOOLS}}": reel_data.get("tools", "unknown"),
        "{{CAPTION_EXCERPT}}": reel_data.get("caption", "")[:80],
        "{{TIME_AGO}}": reel_data.get("date", "recent"),
        "{{TECHNIQUE_NAME}}": reel_data.get("category", "Unknown"),
        "{{EFFECT_CATEGORY}}": category.lower().replace(" ", "-"),
        "{{DATE}}": time.strftime("%Y-%m-%d"),
        "{{REEL_CODE}}": reel_data.get("code", ""),
    }
    
    for k, v in replacements.items():
        template = template.replace(k, str(v))
    
    return template


def process_reel(reel: Dict, processed: set, dry_run: bool = False) -> bool:
    """Process a single reel through the full pipeline"""
    reel_code = reel['code']
    url = reel['url']
    creator = reel.get('creator', 'unknown')
    
    if reel_code in processed:
        print(f"  ⏭️  Already processed: {reel_code}")
        return True
    
    print(f"\n{'='*60}")
    print(f"Processing {reel_code} ({url})")
    print(f"{'='*60}")
    
    # Classify
    category, keyword, keywords = classify_effect(url, reel.get('caption', ''), reel.get('hashtags', []))
    
    if category == "skip":
        print(f"  ⏭️  Skipped: {keyword}")
        return True
    elif category == "camera_theory":
        print(f"  📚 Camera Theory: {keyword}")
        return True
    elif category == "photography_lightroom":
        print(f"  📸 Photography/Lightroom: {keyword}")
        return True
    elif category == "unknown":
        print(f"  ❓ Unknown classification")
        return True
    
    # Create slug
    effect_name = reel.get("caption", "").split('#')[0].strip()[:50]
    effect_slug = re.sub(r'[^a-z0-9]+', '-', effect_name.lower()).strip('-')
    
    reel_data = {
        "code": reel_code,
        "url": url,
        "creator": creator,
        "caption": reel.get("caption", ""),
        "hashtags": reel.get("hashtags", []),
        "effect_name": effect_name or "Unknown Effect",
        "slug": effect_slug,
        "tools": "Power Window + Tracker + Keyframes",
        "category": category
    }
    
    if dry_run:
        print(f"  [DRY RUN] Category: {category}, Keyword: {keyword}")
        return True
    
    # Create asset directories
    asset_dir = VAULT_BASE / "assets" / category.lower().replace(" ", "-") / effect_slug
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    skill_dir = Path(f"/Users/alfredkamisese/.hermes/skills/video-effects/davinci-resolve-{effect_slug}")
    skill_asset_dir = skill_dir / "assets"
    skill_asset_dir.mkdir(parents=True, exist_ok=True)
    
    # Download video
    print(f"  📥 Downloading video...")
    video_path = download_reel(url, asset_dir, reel_code)
    if not video_path:
        return False
    
    # Extract assets
    print(f"  🎬 Extracting visual assets...")
    assets = extract_assets(video_path, asset_dir)
    
    # Copy to skills
    copy_to_skills(assets, reel_code, category, effect_slug)
    
    # Generate vault note
    print(f"  📝 Generating vault note...")
    vault_note = generate_vault_note(reel_data, assets, category, effect_slug)
    category_dir = VAULT_BASE / category.lower().replace(" ", "-")
    category_dir.mkdir(parents=True, exist_ok=True)
    
    existing = sorted(category_dir.glob("*.md"))
    next_num = len([f for f in existing if f.name[0].isdigit()]) + 1
    vault_file = category_dir / f"{next_num:02d}-{effect_slug}_{reel_data['creator'].replace('@','')}_{reel_data['tools'].replace(' ', '-')}.md"
    
    with open(vault_file, 'w') as f:
        f.write(vault_note)
    print(f"  📝 Vault note: {vault_file.name}")
    
    # Copy assets to skill
    copy_to_skills(assets, reel_code, category, effect_slug)
    
    # Clean up mp4
    if video_path.exists():
        try:
            video_path.unlink()
            print(f"  🗑️  Cleaned up mp4: {video_path.name}")
        except Exception as e:
            print(f"  ⚠️  Could not delete mp4: {e}")
    
    # Update tracking
    processed.add(reel_code)
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(processed), f)
    
    print(f"  ✅ Complete: {reel_code}")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Instagram → DaVinci Video Effects Pipeline")
    parser.add_argument("--input", required=True, help="Input file (JSON, CSV, TXT, RTF)")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--dry-run", action="store_true", help="Preview classifications")
    parser.add_argument("--retry-failed", action="store_true", help="Retry failed URLs")
    parser.add_argument("--filter-creator", help="Filter by creator handle")
    args = parser.parse_args()
    
    if not check_tools():
        sys.exit(1)
    
    processed = load_processed()
    urls = parse_input_file(args.input)
    print(f"Found {len(urls)} URLs")
    
    if args.filter_creator:
        urls = [u for u in urls if args.filter_creator.lower() in u.get("creator", "").lower()]
        print(f"Filtered to {len(urls)} URLs for creator: {args.filter_creator}")
    
    if args.retry_failed:
        # TODO: implement retry logic
        pass
    
    pending = [r for r in reels if r['code'] not in processed_set]
    batch = pending[args.start:args.start + args.batch_size]
    
    if args.dry_run:
        print("\n=== DRY RUN ===")
        for r in batch:
            code = extract_reel_code(r["url"])
            cat, kw, _ = classify_effect(r["url"], r.get("caption", ""), r.get("hashtags", []))
            print(f"  {code}: {cat} ({kw})")
        return
    
    success = 0
    failed = 0
    for i, reel in enumerate(batch):
        if process_reel(reel, processed):
            success += 1
        else:
            failed += 1
        time.sleep(2)  # Rate limiting
    
    print(f"\n{'='*50}")
    print(f"Batch complete: {success} success, {failed} failed")
    print(f"Total processed: {len(load_processed())}")


if __name__ == "__main__":
    main()