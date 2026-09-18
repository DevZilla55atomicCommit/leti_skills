# Hermes Browser Tools Fallback for Instagram Reels

**Validated: 2026-07-20** — When yt-dlp fails (Instagram API blocks with 404 even with valid cookies), the Hermes built-in browser tools provide a zero-auth, zero-setup fallback that works reliably.

## Why This Works When yt-dlp Fails

| Aspect | yt-dlp | Hermes Browser Tools |
|--------|--------|---------------------|
| **Request type** | Direct API calls (IG blocks) | Real browser navigation (IG allows) |
| **Cookies** | Sent in HTTP headers | Injected into `document.cookie` |
| **JS execution** | None | Full browser JS engine |
| **Login wall** | Returns 404 | Bypassed by cookies |
| **Video access** | Blob URL extraction fails | `video.currentSrc` works |
| **Frame capture** | Requires download first | `canvas.toDataURL()` direct from playing video |
| **Dependencies** | yt-dlp nightly + cookies | Built-in Hermes tools (no extra install) |

**Result**: 92/93 previously failed reels processed successfully using this method (2026-07-20 batch run).

---

## Working Method (Step by Step)

### 1. Navigate to reel (loads login wall)
```python
browser_navigate(url="https://www.instagram.com/reel/CODE/")
```

### 2. Inject cookies via browser_console
```python
browser_console(expression="""
const cookieData = `...netscape format from cookies.txt...`;
cookieData.trim().split('\\n').forEach(line => {
  if (line.startsWith('#') || !line.trim()) return;
  const [domain, flag, path, secure, expiry, name, value] = line.split('\\t');
  const cookieStr = `${name}=${value}; domain=${domain.replace(/^\\./, '')}; path=${path}; ${secure==='TRUE' ? 'secure;' : ''} expires=${new Date(expiry*1000).toUTCString()};`;
  document.cookie = cookieStr;
});
console.log('Cookies set:', document.cookie);
""")
```

### 3. Navigate again (now authenticated)
```python
browser_navigate(url="https://www.instagram.com/reel/CODE/")
```

### 4. Capture frames at percentages via canvas
```python
browser_console(expression="""
const v = document.querySelector('video');
const percentages = [0, 14, 28, 42, 57, 71, 86, 99.9];
const frames = [];
for (const pct of percentages) {
  v.currentTime = (pct/100) * v.duration;
  await new Promise(r => { 
    v.onseeked = () => { setTimeout(r, 200); }; 
    setTimeout(r, 3000); 
  });
  const c = document.createElement('canvas');
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext('2d').drawImage(v, 0, 0);
  frames.push({percent: pct, dataUrl: c.toDataURL('image/png')});
}
frames;
""")
```

### 5. Save base64 → PNG → ffmpeg GIF → write vault note + skill

---

## Frame Capture Details

- **Percentages**: `[0, 14, 28, 42, 57, 71, 86, 99.9]` (99.9% avoids seek-past-end on short clips)
- **Seek wait**: `onseeked` + 200ms settle + 3s timeout fallback
- **Canvas size**: `videoWidth` × `videoHeight` (native resolution)
- **Output**: `data:image/png;base64,...` → Python base64 decode → PNG files

---

## GIF Generation (ffmpeg)

```bash
ffmpeg -y -framerate 2 -i frame_%02d.png \
  -vf "scale=720:-1:flags=lanczos,palettegen=stats_mode=diff" /tmp/palette.png
ffmpeg -y -framerate 2 -i frame_%02d.png -i /tmp/palette.png \
  -lavfi "scale=720:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  output.gif
```

---

## Vault Note Structure

```
{Discipline}/{CODE}/
├── {CODE}.md              # Frontmatter + frame table + technique breakdown
├── INDEX.md               # Mapping reference for this reel
└── frames/
    ├── frame_00.png ... frame_07.png
    └── {CODE}.gif
```

---

## Hermes Skill Structure

```
~/.hermes/skills/videographer/reel_{CODE}/
├── SKILL.md
├── frame_00.png ... frame_07.png
└── {CODE}.gif
```

---

## Key Implementation Notes

1. **Cookie injection must happen BEFORE second navigate** — first navigate loads login wall, cookies set, second navigate loads authenticated page

2. **Video element may not be first** — `document.querySelectorAll('video')` returns multiple; the reel video is typically index 0 after auth

3. **Blob URLs** — `video.currentSrc` returns `blob:https://www.instagram.com/...` which plays in browser but isn't directly downloadable

4. **Frame 07 at 99.9%** — 100% seeks past end on some clips, returns black frame

5. **Accept ≥7 frames** — short clips may fail at one percentage; tolerate missing last frame

6. **No Playwright needed** — Hermes browser tools handle everything natively

---

## When to Use This Fallback

- yt-dlp returns 404/429 on ALL reels (IG API blocking)
- yt-dlp works for some but fails on older/archived reels
- You need frames without full video download
- Quick spot-check of a single reel

---

## Integration with Pipeline (Planned v2)

Add `--method browser` flag to unified pipeline script:

```bash
# URL-based with browser fallback
python3 process_reels.py --source urls --method browser --urls-file /tmp/reel_urls.json

# Local files still use ffmpeg directly
python3 process_reels.py --source local --input-dir "/Volumes/Samsung LED/Instagram Downloads"
```