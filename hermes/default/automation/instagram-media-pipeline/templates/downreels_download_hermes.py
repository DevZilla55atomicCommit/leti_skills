#!/usr/bin/env python3
"""
Downreels.com Download Template — Hermes Browser Tools Version
Uses Hermes built-in browser tools (browser_navigate, browser_click, browser_type, browser_snapshot)
No Playwright dependency — runs in Hermes agent context directly.
"""

import asyncio
import json
import sys
from pathlib import Path

# Configuration
URLS_FILE = Path("/tmp/reels_pipeline/urls.txt")
DOWNLOAD_DIR = Path("~/Downloads/reels_downreels").expanduser()
STATE_DIR = Path("/tmp/reels_pipeline")
COMPLETED_FILE = STATE_DIR / "completed.json"
FAILED_FILE = STATE_DIR / "failed.json"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)

def reel_id_from_url(url: str) -> str:
    """Extract reel ID from Instagram URL"""
    return url.strip().rstrip("/").split("/")[-1].split("?")[0]

async def load_progress():
    completed = set()
    failed = {}
    if COMPLETED_FILE.exists():
        completed = set(json.loads(COMPLETED_FILE.read_text()))
    if FAILED_FILE.exists():
        failed = json.loads(FAILED_FILE.read_text())
    return completed, failed

async def save_progress(completed, failed):
    COMPLETED_FILE.write_text(json.dumps(list(completed)))
    FAILED_FILE.write_text(json.dumps(failed))

async def download_one_reel(url: str, completed: set, failed: dict) -> bool:
    """Download a single reel via downreels.com using Hermes browser tools"""
    reel_id = reel_id_from_url(url)
    
    if reel_id in completed:
        print(f"  ⏭  {reel_id} already done")
        return True
    if reel_id in failed:
        print(f"  ⏭  {reel_id} previously failed: {failed[reel_id]}")
        return False
    
    print(f"  ⬇  {reel_id}")
    
    try:
        # NOTE: These browser_* calls are Hermes built-in tools
        # The agent calls them directly — this template shows the logical flow
        
        # 1. Navigate to Reels downloader page
        # await browser_navigate("https://downreels.com/instagram-reels-downloader/")
        
        # 2. Fill URL input
        # await browser_type(ref="url_input", text=url)
        
        # 3. Click DOWNLOAD
        # await browser_click(ref="download_btn")
        
        # 4. Wait for result (poll with browser_snapshot)
        # for _ in range(30):  # max 60s
        #     snap = await browser_snapshot()
        #     if "Download HD MP4" in snap.text:
        #         break
        #     await asyncio.sleep(2)
        
        # 5. Click Download HD MP4
        # await browser_click(ref="download_hd_btn")
        
        # 6. File lands in ~/Downloads/reels_downreels/
        output_path = DOWNLOAD_DIR / f"{reel_id}.mp4"
        if output_path.exists() and output_path.stat().st_size > 10000:
            print(f"  ✓  {reel_id} → {output_path.name}")
            completed.add(reel_id)
            return True
        else:
            raise Exception("Download file missing or too small")
            
    except Exception as e:
        print(f"  ✗  {reel_id}: {e}")
        failed[reel_id] = str(e)
        return False

async def main():
    if not URLS_FILE.exists():
        print(f"Create {URLS_FILE} with one Instagram Reel URL per line")
        return 1
    
    urls = [u.strip() for u in URLS_FILE.read_text().splitlines() if u.strip() and not u.startswith("#")]
    if not urls:
        print("No URLs found")
        return 1
    
    completed, failed = await load_progress()
    urls = [u for u in urls if reel_id_from_url(u) not in completed and reel_id_from_url(u) not in failed]
    
    if not urls:
        print("All URLs already processed")
        return 0
    
    print(f"Downloading {len(urls)} reels...")
    
    for i, url in enumerate(urls):
        await download_one_reel(url, completed, failed)
        await save_progress(completed, failed)
        
        # Rate limit: 4 seconds between requests
        if i < len(urls) - 1:
            await asyncio.sleep(4)
    
    print(f"\nDone. Completed: {len(completed)}, Failed: {len(failed)}")
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))