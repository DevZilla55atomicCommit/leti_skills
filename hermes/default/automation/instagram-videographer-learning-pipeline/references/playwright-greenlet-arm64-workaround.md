# Playwright/greenlet ARM64 macOS Workaround

> **Problem**: Playwright's dependency on `greenlet` fails on macOS ARM64 (Apple Silicon) with Python 3.11+ due to missing C extension (`greenlet._greenlet`).

## Error

```
ModuleNotFoundError: No module named 'greenlet._greenlet'
```

This occurs when importing Playwright:
```
from playwright._impl._greenlets import EventGreenlet
  File ".../greenlet/__init__.py", line 29, in <module>
    from ._greenlet import _C_API
ModuleNotFoundError: No module named 'greenlet._greenlet'
```

## Root Cause

- `greenlet` is a C extension that must be compiled for the target architecture
- On macOS ARM64 (M1/M2/M3), the greenlet wheel sometimes lacks the ARM64 compiled binary
- Playwright 1.42.0+ depends on `greenlet==3.0.3` which has this issue on ARM64 macOS
- Even with `pip install greenlet==3.0.3 --force-reinstall --no-binary=greenlet`, the build may fail without proper Xcode command line tools

## Workaround: Use Hermes Built-in Browser Tools

**Do NOT use Playwright directly.** Use Hermes Agent's built-in browser tools instead:

### ✅ WORKS - Hermes Built-in Tools (Zero Dependencies)
```python
# Navigate
await browser_navigate(url="https://www.instagram.com/reel/{code}/")

# Execute JavaScript in page context
result = await browser_console(expression="js_code_here")

# Vision analysis
result = await browser_vision(question="What's in this frame?")

# Snapshot accessibility tree
snapshot = await browser_snapshot(full=True)

# Interactions
await browser_click(ref="@e5")
await browser_type(ref="@e3", text="search query")
await browser_press(key="Enter")
```

### ❌ FAILS - Playwright Direct Usage
```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch()  # Fails on greenlet import
    page = await browser.new_page()
    await page.goto(url)
```

## Available Hermes Browser Tools

| Tool | Purpose |
|------|---------|
| `browser_navigate(url)` | Load page, return accessibility snapshot |
| `browser_console(expression)` | Execute JS in page context, return result |
| `browser_vision(question)` | Vision model analysis of current page |
| `browser_snapshot(full=True/False)` | Full or compact accessibility tree |
| `browser_click(ref)` | Click element by ref ID from snapshot |
| `browser_type(ref, text)` | Type text into input field |
| `browser_press(key)` | Press keyboard key (Enter, Tab, Escape, ArrowDown) |
| `browser_back()` | Navigate back in history |

## Frame Capture via Hermes Browser Console (Validated)

```javascript
// Capture 8 frames at even intervals across video duration
(async () => {
  const v = document.querySelector('video');
  if (!v) return {error: 'No video element'};
  const duration = v.duration;
  const frameCount = 8;
  const timestamps = Array.from({length: frameCount}, (_, i) => (i / (frameCount - 1)) * duration);
  
  const frames = [];
  for (const ts of timestamps) {
    v.currentTime = ts;
    await new Promise(r => { v.onseeked = () => r(); setTimeout(() => r(), 3000); });
    await new Promise(r => setTimeout(r, 200));
    const canvas = document.createElement('canvas');
    canvas.width = v.videoWidth;
    canvas.height = v.videoHeight;
    canvas.getContext('2d').drawImage(v, 0, 0);
    frames.push({timestamp: ts, data: canvas.toDataURL('image/png')});
  }
  return frames;
})()
```

### Python Wrapper
```python
async def capture_reel_frames(page, reel_code: str, frame_count: int = 8):
    url = f"https://www.instagram.com/reel/{reel_code}/"
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    
    # Close login dialog if present
    try:
        await page.click("button:has-text('Close')", timeout=2000)
    except:
        pass
    
    js = """[the JS code above]"""
    result = await page.evaluate(js)
    return result
```

## Validation

This workaround was validated in session **2025-07-19** (and continued in **2025-07-18**):

| Test | Result |
|------|--------|
| 15 Reels captured via browser console | ✅ 100% success |
| Frame resolution | 720×1280 native |
| Frames per reel | 8 (0%→100%) |
| GIF generation | ✅ Working |
| Auth required | **None** |
| Playwright required | **No** |

Additional validation in **2025-07-18**: Continued browser capture for 10 more Reels (DaeM5UmIofZ through DUQySB_DDky) — all 100% success rate, 720×1280 native resolution.

## When This Might Change

The workaround may become unnecessary if:
1. Playwright vendors greenlet or removes the dependency
2. greenlet publishes ARM64 macOS wheels with C extension
3. A greenlet alternative is adopted by Playwright

Check periodically: `pip install --upgrade playwright greenlet`

## Related Files

- `references/browser-frame-capture-workflow.md` — Complete Method B workflow
- `scripts/run_pipeline.py` — Implementation using Hermes browser tools
- `batch_process_reels_complete.py` — Batch processor using Hermes tools