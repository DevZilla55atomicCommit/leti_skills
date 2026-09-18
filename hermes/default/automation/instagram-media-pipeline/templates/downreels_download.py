#!/usr/bin/env python3
"""
Downreels.com Serial Downloader — Template
- Zero-cookie, zero-auth Instagram Reel download via downreels.com
- Serial (one-by-one) with state.json resume support
- Rate limited: 4s between requests
- Output: MP4 files + download_manifest.json
"""

import asyncio
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright

# ============================================================
# CONFIGURATION
# ============================================================
PIPELINE_ROOT = Path.home() / "instagram-davinci-pipeline"
URLS_FILE = PIPELINE_ROOT / "urls.txt"           # Format: "URL | collection_tag"
STATE_FILE = PIPELINE_ROOT / "state.json"
MANIFEST_FILE = PIPELINE_ROOT / "download_manifest.json"
MP4_DIR = PIPELINE_ROOT / "temp" / "mp4"
RATE_LIMIT_DELAY = 4  # seconds between requests

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"completed": [], "failed": {}, "current_stage": "download"}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def load_manifest():
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {}

def save_manifest(manifest):
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))

def reel_id_from_url(url: str) -> str:
    return url.strip().rstrip("/").split("/")[-1].split("?")[0]

async def download_one(page, url: str, collection: str, manifest: dict, state: dict):
    reel_id = reel_id_from_url(url)
    if reel_id in state["completed"]:
        print(f"  ⏭  {reel_id} already done")
        return True

    print(f"  ⬇  {reel_id} ({collection})")
    try:
        await page.goto("https://downreels.com/instagram-reels-downloader/", timeout=30000)
        
        # Paste URL
        await page.fill('input[placeholder*="Reel"], input[placeholder*="reel"], input[type="text"]', url)
        
        # Click DOWNLOAD
        await page.click('button:has-text("DOWNLOAD")')
        
        # Wait for result + download button
        await page.wait_for_selector('button:has-text("Download HD MP4")', timeout=60000)
        
        # Trigger download
        async with page.expect_download(timeout=60000) as download_info:
            await page.click('button:has-text("Download HD MP4")')
        download = await download_info.value
        
        mp4_path = MP4_DIR / f"{reel_id}.mp4"
        await download.save_as(mp4_path)
        
        # Verify
        if not mp4_path.exists() or mp4_path.stat().st_size < 10000:
            raise Exception("Download too small or missing")
        
        manifest[reel_id] = {
            "url": url,
            "collection": collection,
            "mp4_path": str(mp4_path),
            "downloaded_at": time.time()
        }
        state["completed"].append(reel_id)
        print(f"  ✓  {reel_id} → {mp4_path.name}")
        return True
        
    except Exception as e:
        state["failed"][reel_id] = str(e)
        print(f"  ✗  {reel_id}: {e}")
        return False

async def main():
    MP4_DIR.mkdir(parents=True, exist_ok=True)
    
    # Parse urls.txt
    urls = []
    for line in URLS_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        urls.append((parts[0], parts[1] if len(parts) > 1 else "Other"))
    
    state = load_state()
    manifest = load_manifest()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        
        for url, collection in urls:
            await download_one(page, url, collection, manifest, state)
            save_state(state)
            save_manifest(manifest)
            await asyncio.sleep(RATE_LIMIT_DELAY)
        
        await browser.close()
    
    print(f"\nDone. Completed: {len(state['completed'])}, Failed: {len(state['failed'])}")

if __name__ == "__main__":
    asyncio.run(main())