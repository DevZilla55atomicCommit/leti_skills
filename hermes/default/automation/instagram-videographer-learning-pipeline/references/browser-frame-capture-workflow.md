# Browser Frame Capture Workflow (Method B) — Zero-Auth Reel Processing

## Overview
**Method B** extracts frames from Instagram Reels using browser automation instead of yt-dlp. This approach requires **zero authentication**, works on any public Reel, and captures at native resolution (720×1280 validated).

## Why This Replaces yt-dlp (Method A)

| Factor | Method A (yt-dlp + cookies) | Method B (Browser Frame Capture) |
|--------|----------------------------|----------------------------------|
| Auth required | Yes (fresh Chrome cookies.txt) | **No** |
| Works on private/age-gated | No | **Only public** |
| 404/deleted handling | Fails silently | Same limitation |
| Resolution | Source quality | **Native (720×1280)** |
| Batch reliability | Cookie expiry breaks batches | **No session state** |
| ARM64 compatibility | Greenlet issues with Playwright | **Native Hermes browser tools** |
| Maintenance | yt-dlp updates, cookie rotation | **Zero maintenance** |

## Workflow Steps

### 1. Navigate to Reel
```python
await browser_navigate(url="https://www.instagram.com/reel/{code}/")
```

### 2. Handle Login Dialog
```python
try:
    await page.click("button:has-text('Close')", timeout=2000)
except:
    pass  # Dialog may not appear
```

### 3. Wait for Video Element
```python
await page.wait_for_selector("video", timeout=15000)
await asyncio.sleep(1)  # Let video buffer
```

### 4. Get Video Metadata
```python
video_info = await page.evaluate("""
    () => {
        const v = document.querySelector('video');
        return v ? {duration: v.duration, width: v.videoWidth, height: v.videoHeight} : null;
    }
""")
```

### 5. Capture Frames at Timestamps
```python
timestamps = [0, min(1500, duration*500), int(duration*1000)]  # 0ms, 50%/1.5s, end
for i, ts in enumerate(timestamps):
    v = page.evaluate(f"""
        () => {{
            const v = document.querySelector('video');
            v.currentTime = {ts/1000};
            return new Promise(r => {{
                v.onseeked = () => {{
                    const c = document.createElement('canvas');
                    c.width = v.videoWidth;
                    c.height = v.videoHeight;
                    c.getContext('2d').drawImage(v, 0, 0);
                    r(c.toDataURL('image/png'));
                }};
                setTimeout(() => r({{error: 'Seek timeout'}}), 5000);
            }});
        }}
    """)
    # Save base64 PNG
```

### 6. Generate GIFs via ffmpeg (Local)
```bash
# demo.gif - 10fps, 720px wide
ffmpeg -y -framerate 10 -i frame_%03d.png -vf "scale=720:-1:flags=lanczos" demo.gif

# technique_demo.gif - 8fps, 480px, 64 colors, looping
ffmpeg -y -framerate 8 -i frame_%03d.png \
  -filter_complex "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" \
  -loop 0 technique_demo.gif
```

## Validated Results
- **Resolution**: 720×1280 (Reel native)
- **Frames captured**: 8 per Reel (evenly spaced 0%→100%)
- **GIFs**: demo.gif (full), technique_demo.gif (loop-optimized)
- **Speed**: ~15-20 seconds per Reel including navigation
- **Success rate**: 100% on public reels tested (4 validation reels)

## Key Implementation Details

### Frame Capture Timing
```python
# 8 frames evenly distributed across duration
frame_count = 8
timestamps = [i / (frame_count - 1) * duration for i in range(frame_count)]
```

### Canvas Resolution
```javascript
canvas.width = video.videoWidth;   // 720
canvas.height = video.videoHeight; // 1280
```

### Error Handling
- Seek timeout: 5 seconds per frame
- Navigation timeout: 120 seconds
- Video element wait: 15 seconds
- Skip if video element not found

### Batch Processing
```python
BATCH_SIZE = 10
DELAY_BETWEEN = 3.0      # seconds between reels
DELAY_BETWEEN_BATCHES = 30.0  # seconds between batches
```

## Integration with Pipeline
```python
# In run_pipeline.py
async def process_reel(page, url, index, total):
    code = extract_reel_code(url)
    asset_dir = OUTPUT_ROOT / discipline_folder / "assets" / code
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Navigate & capture frames
    await capture_frames(page, url, asset_dir)
    
    # 2. Generate GIFs locally
    generate_gifs(asset_dir, code)
    
    # 3. Create vault note + skill
    create_vault_note(asset_dir, code, url, discipline, category)
    create_skill(asset_dir, code, url, discipline, category)
    
    # 4. Auto-cleanup (keep only final assets)
    cleanup_temp_files(asset_dir)
```

## Limitations
- Only works on **public** Reels
- Cannot capture audio (visual only)
- Requires browser session (Hermes built-in tools)
- Sequential processing (no parallel video elements)

## When to Use Method A (yt-dlp) Instead
- Need full video file (MP4) for archival
- Need audio track
- Reel is private but you have access via cookies
- Batch download for offline processing

## Reference Implementation
See `scripts/run_pipeline.py` → `capture_frame()` and `process_reel()` functions for the complete implementation using Hermes browser tools.

## Session History
- **2025-07-19**: Method B validated on 4 reels (DaeM5UmIofZ, DavSPEWJtMZ, Dah5kECAgEh, DaWoOJtqIP1) → 100% success
- **2025-07-19**: Full batch script `batch_process_reels_complete.py` created with auto-resume, 10-reel batches
- **2025-07-18**: Method B confirmed as production replacement for yt-dlp (Method A)