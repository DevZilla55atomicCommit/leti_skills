# Downreels.com Automation Reference

## Overview
Headless browser automation for downloading Instagram Reels via downreels.com — zero cookie, zero auth approach.

## Target Site
- **URL**: `https://downreels.com/instagram-reels-downloader/`
- **Alternative**: `https://downreels.com/instagram-video-downloader-free/` (for feed posts)
- **Claim**: "No login, no watermark, original quality"

## Site Flow Analysis

### DOM Selectors (as of 2026-07-22)
| Step | Element | Selector Strategy |
|------|---------|-------------------|
| 1. URL input | Text field | `input[placeholder*="Reel" i], input[placeholder*="reel" i], input[type="text"]` |
| 2. DOWNLOAD button | Primary CTA | `button:has-text("DOWNLOAD")` |
| 3. Result wait | Spinner → result | Wait for `button:has-text("Download HD MP4")` |
| 4. HD download | Final CTA | `button:has-text("Download HD MP4")` |

### Response Pattern
1. Submit URL → "FETCHING..." spinner (2-8s)
2. Result card appears: thumbnail + "Download HD MP4" button
3. Click HD button → browser triggers native download
4. File lands in headless browser's download directory

## Rate Limits & Anti-Bot

| Limit | Observed |
|-------|----------|
| Requests/minute | ~15-20 before CAPTCHA/IP block |
| Safe delay | 4-5 seconds between requests |
| Session reuse | Cookies persist across requests in same browser context |
| CAPTCHA trigger | Too fast, too many from same IP |
| Failure modes | CAPTCHA, empty result, IP block, site structure change |

### Mitigation Strategies
- **Delay**: 4-5 seconds between requests
- **Context refresh**: New browser context every 10 downloads
- **User-Agent rotation**: Not needed (headless Chromium UA accepted)
- **Backoff on 429**: 30s → 60s → 120s exponential

## Hermes Browser Tools Integration

### Available Tools
- `browser_navigate(url)` — Navigate to URL
- `browser_click(ref)` — Click element by ref from snapshot
- `browser_type(ref, text)` — Type into input
- `browser_snapshot(mode="som")` — Get DOM + numbered refs
- `browser_wait(seconds)` — Async sleep

### Automation Template
```python
async def download_reel(page, url, download_dir):
    reel_id = extract_reel_id(url)
    
    # 1. Navigate
    await page.goto("https://downreels.com/instagram-reels-downloader/")
    await page.wait_for_load_state("domcontentloaded")
    
    # 2. Fill URL
    await page.fill('input[placeholder*="Reel" i], input[placeholder*="reel" i], input[type="text"]', url.strip())
    
    # 3. Click DOWNLOAD
    await page.click('button:has-text("DOWNLOAD")')
    
    # 4. Wait for result + download button
    await page.wait_for_selector('button:has-text("Download HD MP4")', timeout=60000)
    
    # 5. Trigger download
    async with page.expect_download(timeout=60000) as download_info:
        await page.click('button:has-text("Download HD MP4")')
    
    download = await download_info.value
    await download.save_as(download_dir / download.suggested_filename)
    
    print(f"  ✓ {download.suggested_filename}")
    return True, reel_id, download.suggested_filename

async def main():
    if not URLS_FILE.exists():
        print(f"Create {URLS_FILE} with one Instagram Reel URL per line")
        return 1
    
    urls = [u.strip() for u in URLS_FILE.read_text().splitlines() if u.strip()]
    if not urls:
        print("No URLs found")
        return 1
    
    completed = set(json.loads(COMPLETED_FILE.read_text()) if COMPLETED_FILE.exists() else [])
    failed = json.loads(FAILED_FILE.read_text()) if FAILED_FILE.exists() else {}
    
    urls = [u for u in urls if u not in completed and u not in failed]
    if not urls:
        print("All URLs already processed")
        return 0
    
    print(f"Downloading {len(urls)} reels...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        
        semaphore = asyncio.Semaphore(1)
        
        for url in urls:
            success, reel_id, result = await download_reel(page, url, semaphore)
            
            if success:
                completed.add(reel_id)
            else:
                failed[reel_id] = result
            
            # Save progress
            COMPLETED_FILE.write_text(json.dumps(list(completed)))
            FAILED_FILE.write_text(json.dumps(failed))
            
            await asyncio.sleep(4)  # rate limit
        
        await browser.close()
    
    print(f"\nDone. Completed: {len(completed)}, Failed: {len(failed)}")
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

## Output Specifications

| Property | Value |
|----------|-------|
| Format | MP4 (H.264/AAC) |
| Resolution | 1280×720 (typical) |
| Duration | Up to 90s (Reels max) |
| Bitrate | ~780 kbps video, ~75 kbps audio |
| Filename | `{reel_id}.mp4` or site-generated |

## Error Taxonomy

| Error | Cause | Resolution |
|-------|-------|------------|
| Timeout waiting for HD button | Private reel / deleted / rate limited | Log, retry with fresh context |
| Download file < 10KB | Failed download / empty | Retry with fresh context |
| CAPTCHA page | IP/rate limit hit | Exponential backoff (30s→60s→120s) |
| Navigation timeout | Site down / DNS | Retry after 60s |

## Validation Criteria
```python
def verify_download(path: Path, min_size=10000) -> bool:
    return path.exists() and path.stat().st_size > min_size
```

## Batch Processing Script
Location: `templates/downreels_download.py` (Playwright version)  
Location: `templates/downreels_download_hermes.py` (Hermes browser tools version)

### Serial Batch Runner
```bash
# urls.txt: one URL per line
python3 downreels_download.py --urls urls.txt --out ~/Downloads/reels_downreels --delay 4
```

## Validation
Tested reel: `DDq6fmTR0HM` → `AQN40Vz04BypuiVuC2ws5KvNxmzyDnSdQu-WKlVj1sA2ktGpkbl6sUbW6x9OPYhVOIXsh78Gsbb4WMm-J4oQvCcAqargq6Vb72eog5U.mp4` (2.06MB, 1280×720, 19.2s, H.264/AAC)

## Legal/Compliance Note
- **Violates**: "No third-party downloaders" policy (user accepted trade-off)
- **Risk**: Site changes, IP blocks, CAPTCHA evolution
- **Mitigation**: Use as gap-fill only; primary method = yt-dlp + cookies