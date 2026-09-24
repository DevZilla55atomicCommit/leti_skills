# Playwright/Greenlet Issue on macOS ARM64

## Problem
Playwright browser automation fails with `No module named 'greenlet._greenlet'` when using `playwright.sync_api` in the Hermes environment on macOS ARM64 (Apple Silicon).

## Context
This occurred when the pipeline's fallback browser automation path was triggered after yt-dlp failed to download a reel. The fallback uses Playwright to navigate to the reel URL and capture frames via `page.evaluate()` with canvas.toDataURL().

## Error
```
No module named 'greenlet._greenlet'
```

## Root Cause
- Playwright's synchronous API (`playwright.sync_api`) depends on `greenlet` for coroutine handling
- On macOS ARM64, there's a known compatibility issue between Playwright's bundled greenlet and the Python environment
- The Hermes venv has `greenlet==3.0.3` installed but the native extension (`_greenlet`) fails to load

## Workarounds (in order of preference)

### 1. Use async API instead (recommended)
```python
from playwright.async_api import async_playwright

async def capture_frames(url, output_dir, duration):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # ... rest of capture logic with await
        await browser.close()
```

### 2. Use system Python instead of venv
```bash
# Install Playwright globally
pip3 install playwright
playwright install chromium

# Then use system python for the browser automation subprocess
```

### 3. Use subprocess with standalone script
Create a standalone Python script that uses Playwright, run it via `subprocess.run()` with the system Python interpreter that has working greenlet.

### 4. Use Selenium/undetected-chromedriver as alternative
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# ... selenium-based capture
```

## Status
**UNRESOLVED** as of 2026-07-19. The fallback path in the pipeline is currently non-functional due to this issue.

## Impact on Pipeline
- **Primary path (yt-dlp)**: Works perfectly ✅
- **Fallback path (browser capture)**: Broken ❌
- **Impact**: Reels that yt-dlp cannot download (private, deleted, or API-blocked) cannot be processed via browser fallback
- **Mitigation**: Ensure cookies are fresh so yt-dlp succeeds for maximum reels

## Testing
To verify fix:
```bash
cd /Users/alfredkamisese/.hermes/skills/automation/instagram-reels-pipeline
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    print(page.title())
    browser.close()
"
```

If this works without greenlet error, the fallback path is functional.