#!/usr/bin/env python3
"""
Regenerate missing GIFs for Instagram Reels → DaVinci pipeline.

Run from: ~/instagram-davinci-pipeline/scripts/

This script was created to recover 246 missing GIFs that were generated
in temp/gifs/ but never copied to vault before cleanup deleted them.

Workflow:
1. Read missing reel IDs from /tmp/missing_gif.txt
2. Download MP4s via downreels.com (Playwright)
3. Generate full-video GIF (10fps, 480px width)
4. Copy GIF to vault alongside _frames folder
5. Cleanup temp files

Usage:
    python3 regenerate_missing_gifs.py

Requirements:
- Playwright with Chromium
- ffmpeg
- downreels.com accessible
- RTF file with URLs at /Users/alfredkamisese/Documents/Photography:Videography URLs.rtf

Note: The original pipeline bug was in generate_skill_and_vault() - it copied
frames to vault but NOT the GIF. Fix applied in auto_processor.py v1.0.3.
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

async def main():
    print("=== GIF Regeneration for Missing Reels ===")
    print(f"Start: {datetime.now()}")
    
    for d in [MP4_DIR, GIFS_DIR, VAULT_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Read missing reels
    missing = Path("/tmp/missing_gif.txt").read_text().strip().split("\n")
    print(f"Missing GIFs: {len(missing)}")
    
    # Get URLs
    urls = parse_rtf_urls(RTF_FILE)
    url_map = {u.split("/")[-2] if u.endswith("/") else u.split("/")[-1]: u for u, _ in urls}
    
    batch_urls = [(url_map[r], "Photography/Videography") for r in missing if r in url_map]
    print(f"Have URLs for: {len(batch_urls)} reels")
    
    processed = 0
    failed = 0
    
    for batch_start in range(0, len(batch_urls), DOWNLOAD_BATCH_SIZE):
        batch = batch_urls[batch_start:batch_start + DOWNLOAD_BATCH_SIZE]
        batch_num = batch_start // DOWNLOAD_BATCH_SIZE + 1
        
        print(f"\n=== BATCH {batch_num} ===")
        
        # Download
        url_file = Path("/tmp/reels_pipeline/urls.txt")
        url_file.parent.mkdir(exist_ok=True)
        url_file.write_text("\n".join([u for u, _ in batch]))
        
        result = run_cmd(
            "/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python /tmp/reels_pipeline/download_reels.py",
            timeout=600
        )
        
        if result.returncode != 0:
            print(f"Download failed for batch {batch_num}")
            continue
        
        # Move MP4s
        downloads = Path("~/Downloads/reels_downreels").expanduser()
        mp4s = sorted(downloads.glob("*.mp4"), key=lambda f: f.stat().st_mtime)
        
        for url, collection in batch:
            reel_id = url.strip().rstrip("/").split("/")[-1]
            if mp4s:
                src = mp4s.pop()
                dest = MP4_DIR / f"{reel_id}.mp4"
                if dest.exists():
                    dest.unlink()
                shutil.move(str(src), str(dest))
                await asyncio.sleep(DOWNLOAD_DELAY)
            else:
                print(f"No MP4 for {reel_id}")
                continue
            
            # Create GIF
            mp4_path = MP4_DIR / f"{reel_id}.mp4"
            gif_path = GIFS_DIR / f"{reel_id}.gif"
            
            cmd = f'ffmpeg -y -i "{mp4_path}" -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" "{gif_path}"'
            result = run_cmd(cmd, timeout=120)
            
            if result.returncode == 0 and gif_path.exists():
                # Copy to vault
                vault_gif = VAULT_DIR / f"{reel_id}.gif"
                shutil.copy2(gif_path, vault_gif)
                print(f"  GIF saved to vault: {vault_gif.name} ({vault_gif.stat().st_size / 1024 / 1024:.1f} MB)")
                processed += 1
            else:
                print(f"  GIF creation failed for {reel_id}")
                failed += 1
            
            # Cleanup
            for f in [mp4_path, gif_path]:
                if f.exists():
                    f.unlink()
            
            await asyncio.sleep(0.5)
        
        print(f"Batch {batch_num} complete. Total processed: {processed}, Failed: {failed}")
    
    print(f"\n=== DONE ===")
    print(f"Total processed: {processed}")
    print(f"Failed: {failed}")
    print(f"End: {datetime.now()}")

if __name__ == "__main__":
    asyncio.run(main())