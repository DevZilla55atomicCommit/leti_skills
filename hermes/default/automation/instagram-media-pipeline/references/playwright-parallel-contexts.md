# Playwright Parallel BrowserContexts for Instagram Reel Capture

## Architecture: 4 Isolated Contexts per Browser Process

```python
from playwright.async_api import async_playwright

async def capture_batch(reel_urls: list[str], output_root: Path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Create 4 isolated contexts (separate cookie jars, storage, cache)
        contexts = [await browser.new_context(
            record_video_dir=str(output_root / f"ctx_{i}"),
            viewport={"width": 720, "height": 1280},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ) for i in range(4)]
        
        # Distribute URLs across contexts
        semaphore = asyncio.Semaphore(4)
        
        async def worker(ctx_idx: int, url: str):
            async with semaphore:
                await capture_single_reel(contexts[ctx_idx], url, output_root / f"ctx_{ctx_idx}")
        
        tasks = [
            worker(i % 4, url)
            for i, url in enumerate(reel_urls)
        ]
        await asyncio.gather(*tasks)
        
        for ctx in contexts:
            await ctx.close()
        await browser.close()

async def capture_single_reel(context, url: str, output_dir: Path):
    page = await context.new_page()
    
    # Navigate and wait for video element
    await page.goto(url, wait_until="networkidle")
    video = page.locator("video")
    await video.wait_for(state="attached", timeout=10000)
    await page.wait_for_function("document.querySelector('video').readyState >= 2")
    
    # Get duration
    duration = await video.evaluate("v => v.duration")
    
    # Record video (Playwright handles this natively)
    # Video saved to context.record_video_dir automatically
    
    # Wait for playback to complete (or just capture first few seconds)
    await page.wait_for_timeout(min(int(duration * 1000), 30000))
    
    await page.close()
    # Video file appears in output_dir after page.close()
```

## Video Recording API (Playwright 1.42+)

```python
# Context creation with video recording
context = await browser.new_context(
    record_video_dir="videos/",
    record_video_size={"width": 720, "height": 1280}
)

page = await context.new_page()
await page.goto(url)
# ... interact ...
await page.close()

# Video file path available after page.close()
video_path = await page.video.path()  # or page.video.save_as()
```

## Local Frame Extraction (ffmpeg) — Replaces 8× browser_console seeks

```bash
# Input: recorded webm from Playwright
# Output: 8 PNG frames at even temporal distribution

DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.webm)
ffmpeg -i input.webm \
  -vf "select='eq(n,0)+gte(t,${DURATION}*0.14)+gte(t,${DURATION}*0.28)+gte(t,${DURATION}*0.42)+gte(t,${DURATION}*0.57)+gte(t,${DURATION}*0.71)+gte(t,${DURATION}*0.86)+gte(t,${DURATION}*0.99)',scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2" \
  -vsync vfr frames/frame_%02d.png
```

## BrowserContext Isolation Guarantees

| Property | Isolated per Context |
|----------|---------------------|
| Cookies | ✅ Yes |
| LocalStorage | ✅ Yes |
| SessionStorage | ✅ Yes |
| IndexedDB | ✅ Yes |
| Cache | ✅ Yes |
| Service Workers | ✅ Yes |
| Permissions | ✅ Yes |
| Video Recording | ✅ Separate file per page |

## Performance Targets

| Metric | Target |
|--------|--------|
| Contexts per browser | 4 (RAM ~400MB each on M-series) |
| Reels per context per minute | 3 (20s per reel incl. nav + record) |
| **Total throughput** | **~12 reels/minute** |
| Success rate (public reels) | ~75% |
| Success rate (with login wall) | ~0% (use yt-dlp Method A) |

## Rate Limit Strategy

```python
# Per-context delay to stay under ~35 RPM per IP
await asyncio.sleep(random.uniform(1.5, 3.0))

# Global batch pause
if reel_index % 10 == 0:
    await asyncio.sleep(60)  # 60s every 10 reels
```

## ARM64 / Apple Silicon Notes

- Playwright Chromium runs natively on ARM64 (no Rosetta)
- Use `playwright install chromium` — downloads ARM64 build
- **Known issue**: `playwright-python` + `greenlet` (used by some async frameworks) can crash
  - **Workaround**: Use plain `asyncio` (as shown above), avoid `gevent`/`eventlet`
  - Hermes browser tools use patched version — prefer those for in-app automation

## Error Handling

```python
async def capture_with_retry(context, url, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            return await capture_single_reel(context, url, output_dir)
        except PlaywrightTimeoutError:
            if attempt == max_retries:
                raise
            await asyncio.sleep(2 ** attempt)  # exponential backoff
        except Error as e:
            if "Target page, context or browser has been closed" in str(e):
                # Context crashed, need new one
                raise ContextCrashedError()
            raise
```