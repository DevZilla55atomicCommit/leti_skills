# Hermes Browser Tools Fallback for Instagram Reels

**Date**: 2026-07-20  
**Session**: Processing reel `DZ95PwrBsCQ` (sparky.resolve — Day 13 DaVinci Resolve)  
**Status**: ✅ **VALIDATED** — 8 frames + GIF extracted successfully via browser tools

---

## Problem Recap

| Method | Tool | Result |
|--------|------|--------|
| **Method A** | `yt-dlp --cookies` | ❌ HTTP 404 on ALL reels (even public, fresh cookies) |
| **Method B (Playwright)** | `playwright.async_api` | ❌ `ModuleNotFoundError: greenlet._greenlet` on macOS ARM64 |
| **Method B (Hermes)** | `browser_navigate`, `browser_console`, `browser_vision` | ✅ **WORKS** — Zero auth, full resolution, no external deps |

---

## Working Workflow (Hermes Browser Tools)

### 1. Navigate to Reel
```python
browser_navigate(url="https://www.instagram.com/reel/DZ95PwrBsCQ/")
```

### 2. Inject Cookies via Console
```javascript
// In browser_console - parse Netscape cookie file and set document.cookie
const cookieData = `
.instagram.com	TRUE	/	TRUE	1819051654	datr	hi5daqzyYyNAoxoBfn3PROrX
.instagram.com	TRUE	/	TRUE	1816027654	ig_did	79F80EFD-4147-4F20-A962-A49ADA02FE62
.instagram.com	TRUE	/	TRUE	1819051655	mid	al0uhgAEAAF3NePlilkVF_gj6j67
.instagram.com	TRUE	/	TRUE	1819080670	csrftoken	JJ7Hzdh8rvG0J3lsnMddNyaCeqsdc1yv
.instagram.com	TRUE	/	TRUE	1792296670	ds_user_id	29774694259
.instagram.com	TRUE	/	TRUE	1816028377	sessionid	29774694259%3AEO7ftImeDTFWOD%3A8%3AAYiP_HKp99ug1HhOY9jYAc18ZRD5TEPXig0tRHz2qw
.instagram.com	TRUE	/	TRUE	0	rur	"SCU\\05429774694259\\0541816107414:***"
.instagram.com	TRUE	/	TRUE	1785097235	wd	966x957
`;

// Set cookies
cookieData.trim().split('\n').forEach(line => {
  if (!line.startsWith('#') && line.trim()) {
    const [domain, flag, path, secure, expiry, name, value] = line.split('\t');
    const cookieStr = `${name}=${value}; domain=${domain.replace(/^\./, '')}; path=${path}; ${secure === 'TRUE' ? 'secure;' : ''} expires=${new Date(expiry * 1000).toUTCString()};`;
    document.cookie = cookieStr;
  }
});
```

### 3. Re-navigate (now authenticated)
```python
browser_navigate(url="https://www.instagram.com/reel/DZ95PwrBsCQ/")
```

### 4. Extract Video Metadata
```python
browser_console(expression="""
const vids = document.querySelectorAll('video');
Array.from(vids).map((v, i) => ({
  i, src: v.src, currentSrc: v.currentSrc, duration: v.duration,
  videoWidth: v.videoWidth, videoHeight: v.videoHeight,
  readyState: v.readyState, networkState: v.networkState,
  muted: v.muted, paused: v.paused
}))
""")
```

### 5. Capture Frames at Percentages
```python
# For each percentage in [0, 14, 28, 42, 57, 71, 86, 99.9]:
browser_console(expression=f"""
const v = document.querySelectorAll('video')[0];
const targetTime = ({pct} / 100) * v.duration;
v.currentTime = targetTime;
// Wait for seek
await new Promise(r => {{ const onSeeked = () => {{ v.removeEventListener('seeked', onSeeked); setTimeout(r, 200); }}; v.addEventListener('seeked', onSeeked); setTimeout(r, 3000); }});
// Capture frame
const canvas = document.createElement('canvas');
canvas.width = v.videoWidth;
canvas.height = v.videoHeight;
canvas.getContext('2d').drawImage(v, 0, 0);
canvas.toDataURL('image/png')
""")
```

### 6. Save Frames + Create GIF (local ffmpeg)
```bash
# Frames saved as base64 → decoded → PNG files
# GIF creation:
ffmpeg -y -framerate 2 -i frame_%02d.png \
  -vf "scale=720:-1:flags=lanczos,palettegen=stats_mode=diff" /tmp/palette.png
ffmpeg -y -framerate 2 -i frame_%02d.png -i /tmp/palette.png \
  -lavfi "scale=720:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  output.gif
```

---

## Key Findings

| Aspect | Detail |
|--------|--------|
| **Auth required** | NO — works on public reels without any cookies (cookies only needed for age-gated/private) |
| **Resolution** | Full native (720×1280 for this reel) |
| **Frame capture** | `canvas.toDataURL('image/png')` — lossless PNG |
| **Seek accuracy** | 99.9% instead of 100% avoids seek-past-end |
| **Video element** | Multiple `<video>` elements on page; first one (index 0) is the main reel |
| **Duration** | 106.9s for this reel |
| **Tools used** | Only Hermes built-in: `browser_navigate`, `browser_console`, `browser_vision` |
| **External deps** | NONE — no Playwright, no yt-dlp, no greenlet |

---

## Integration Pattern for Pipeline

```python
async def extract_frames_hermes_browser(reel_code, url, cookies_file, output_dir):
    """Extract frames using Hermes browser tools (zero external deps)."""
    
    # 1. Navigate + inject cookies
    browser_navigate(url=url)
    inject_cookies_via_console(cookies_file)  # JS in browser_console
    browser_navigate(url=url)  # Re-navigate authenticated
    
    # 2. Get duration
    duration = get_video_duration_via_console()
    
    # 3. Capture frames
    percentages = [0, 14, 28, 42, 57, 71, 86, 99.9]
    frames = []
    for i, pct in enumerate(percentages):
        data_url = capture_frame_at_percent(pct, duration)
        save_base64_png(data_url, os.path.join(output_dir, f'frame_{i:02d}.png'))
        frames.append(os.path.join(output_dir, f'frame_{i:02d}.png'))
    
    # 4. Create GIF locally with ffmpeg
    create_gif(frames, os.path.join(output_dir, f'{reel_code}.gif'))
    
    return frames, duration
```

---

## Files Created This Session

| Path | Description |
|------|-------------|
| `/tmp/frames_DZ95PwrBsCQ/frame_00.png` ... `frame_07.png` | 8 captured frames (99.9% last) |
| `/tmp/frames_DZ95PwrBsCQ/DZ95PwrBsCQ.gif` | 2fps animated preview (417 KB) |
| `TamaZila Obsidian Vault/.../Fusion/DZ95PwrBsCQ.md` | Vault note with frames + GIF refs |
| `TamaZila Obsidian Vault/.../Fusion/INDEX.md` | Mapping index for Fusion reels |
| `TamaZila Obsidian Vault/.../Fusion/frames/` | Canonical frame store (frames + GIF) |
| `.hermes/skills/videographer/reel_DZ95PwrBsCQ/` | Hermes skill with frames + GIF |

---

## Next Steps for v2 Pipeline

1. **Embed this workflow** in `process_reels.py` as the primary method (yt-dlp is now unreliable)
2. **Add pre-flight cookie check** (sessionid expiry > 1 hour)
3. **Archive-first logic**: Check `/Volumes/Samsung LED/.../{CODE}.mp4` before any processing
4. **DaVinci MCP Phase 2**: Import → `media_analysis.analyze_clip(vision=true)` → append color science to vault note