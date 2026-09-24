#!/usr/bin/env python3
"""
Full GIF regeneration from scratch.
Processes ALL 389 reels by re-downloading and creating GIFs.
"""
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

# ============================================================
# CONFIGURATION
# ============================================================
RTF_FILE = Path("/Users/alfredkamisese/Documents/Photography:Videography URLs.rtf")
TEMP_DIR = Path("/Users/alfredkamisese/instagram-davinci-pipeline/temp")
MP4_DIR = TEMP_DIR / "mp4"
GIFS_DIR = TEMP_DIR / "gifs"
VAULT_DIR = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels/Photography/Videography")

# Rate limiting
DOWNLOAD_BATCH_SIZE = 10
DOWNLOAD_DELAY = 4.0

def run_cmd(cmd: str, cwd: Path = None, timeout: int = 300) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"ERROR: {cmd}\n{result.stderr}")
    return result

def parse_rtf_urls(rtf_path: Path) -> List[Tuple[str, str]]:
    content = rtf_path.read_text(encoding='utf-8', errors='ignore')
    urls = re.findall(r'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/?', content)
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append((u, "Photography/Videography"))
    return unique

def download_batch(urls: List[Tuple[str, str]], batch_num: int) -> List[dict]:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading batch {batch_num} ({len(urls)} reels)...")
    
    url_file = Path("/tmp/reels_pipeline/urls.txt")
    url_file.parent.mkdir(exist_ok=True)
    url_file.write_text("\n".join([u for u, _ in urls]))
    
    result = run_cmd(
        "/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python /tmp/reels_pipeline/download_reels.py",
        timeout=600
    )
    
    if result.returncode != 0:
        print(f"Download failed for batch {batch_num}")
        return []
    
    downloads = Path("~/Downloads/reels_downreels").expanduser()
    results = []
    
    for url, collection in urls:
        reel_id = url.strip().rstrip("/").split("/")[-1]
        mp4s = sorted(downloads.glob("*.mp4"), key=lambda f: f.stat().st_mtime)
        if mp4s:
            src = mp4s.pop()
            dest = MP4_DIR / f"{reel_id}.mp4"
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))
            results.append({"reel_id": reel_id, "url": url, "collection": collection, "mp4": str(dest)})
            import time
            time.sleep(DOWNLOAD_DELAY)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch {batch_num}: Downloaded {len(results)}/{len(urls)} reels")
    return results

def create_gif(mp4_path: Path, gif_path: Path) -> bool:
    cmd = f'ffmpeg -y -i "{mp4_path}" -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" "{gif_path}"'
    result = run_cmd(cmd, timeout=120)
    return result.returncode == 0 and gif_path.exists()

async def process_reel(reel_id: str, mp4_path: Path) -> bool:
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing {reel_id}...")
        
        gif_path = GIFS_DIR / f"{reel_id}.gif"
        if not create_gif(mp4_path, gif_path):
            print(f"  GIF creation failed for {reel_id}")
            return False
        
        vault_gif = VAULT_DIR / f"{reel_id}.gif"
        shutil.copy2(gif_path, vault_gif)
        print(f"  GIF saved to vault: {vault_gif.name} ({vault_gif.stat().st_size / 1024 / 1024:.1f} MB)")
        
        return True
    except Exception as e:
        print(f"  Error processing {reel_id}: {e}")
        return False

def cleanup_reel(reel_id: str):
    for f in [MP4_DIR / f"{reel_id}.mp4", GIFS_DIR / f"{reel_id}.gif"]:
        if f.exists():
            f.unlink()

async def main():
    print("=== Full GIF Regeneration Pipeline ===")
    print(f"Start: {datetime.now()}")
    
    for d in [MP4_DIR, GIFS_DIR, VAULT_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Get all reel IDs from vault
    vault_reels = [d.name.replace("_frames", "") for d in VAULT_DIR.glob("*_frames") if d.is_dir()]
    print(f"Found {len(vault_reels)} reels in vault")
    
    # Get URLs
    urls = parse_rtf_urls(RTF_FILE)
    url_map = {u.split("/")[-2] if u.endswith("/") else u.split("/")[-1]: u for u, _ in urls}
    
    # Build batch URLs
    batch_urls = [(url_map[r], "Photography/Videography") for r in vault_reels if r in url_map]
    print(f"Have URLs for: {len(batch_urls)} reels")
    
    processed = 0
    failed = 0
    
    for batch_start in range(0, len(batch_urls), DOWNLOAD_BATCH_SIZE):
        batch = batch_urls[batch_start:batch_start + DOWNLOAD_BATCH_SIZE]
        batch_num = batch_start // DOWNLOAD_BATCH_SIZE + 1
        
        print(f"\n=== BATCH {batch_num} ===")
        
        downloads = download_batch(batch, batch_num)
        
        for item in downloads:
            reel_id = item["reel_id"]
            mp4_path = Path(item["mp4"])
            
            success = await process_reel(reel_id, mp4_path)
            if success:
                processed += 1
            else:
                failed += 1
            
            cleanup_reel(reel_id)
            await asyncio.sleep(0.5)
        
        print(f"Batch {batch_num} complete. Total processed: {processed}, Failed: {failed}")
    
    print(f"\n=== DONE ===")
    print(f"Total processed: {processed}")
    print(f"Failed: {failed}")
    print(f"End: {datetime.now()}")

if __name__ == "__main__":
    asyncio.run(main())