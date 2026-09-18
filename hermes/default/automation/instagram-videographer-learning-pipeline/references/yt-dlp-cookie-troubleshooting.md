# yt-dlp Cookie Troubleshooting for Instagram Reels

## Problem: "Instagram sent an empty media response"

### Root Cause
The cookies.txt file exported from Chrome is either:
1. **Stale/expired** - Instagram cookies have short lifespans (~30 days)
2. **Wrong format** - Must be Netscape HTTP Cookie File format
3. **Missing critical cookies** - Need: `sessionid`, `ds_user_id`, `csrftoken`, `mid`, `ig_did`
3. **Wrong domain** - Must be `.instagram.com` (leading dot)

---

## Quick Fix: Re-export Fresh Cookies

```bash
# 1. Log OUT of Instagram in Chrome
# 2. Log back IN to Instagram in Chrome
# 3. Open "Get cookies.txt" extension → Export → Save as cookies.txt
# 4. Move to ~/Downloads/cookies.txt
```

### Verify cookies.txt format
```bash
head -30 ~/Downloads/cookies.txt
```

Should look like:
```
# Netscape HTTP Cookie File
.instagram.com	TRUE	/	TRUE	1735689600	sessionid	YOUR_SESSION_ID_HERE
.instagram.com	TRUE	/	TRUE	1735689600	ds_user_id	YOUR_USER_ID
.instagram.com	TRUE	/	TRUE	1735689600	csrftoken	YOUR_CSRF_TOKEN
.instagram.com	TRUE	/	TRUE	1735689600	mid	YOUR_MID
.instagram.com	TRUE	/	TRUE	1735689600	ig_did	YOUR_IG_DID
```

**Required cookies (must all be present):**
| Cookie | Purpose |
|--------|---------|
| `sessionid` | **Full account access** - primary auth token |
| `ds_user_id` | Your numeric user ID |
| `csrftoken` | CSRF protection for POST requests |
| `mid` | Machine ID |
| `ig_did` | Device ID |

---

## Alternative: Use `--cookies-from-browser chrome`

```bash
yt-dlp --cookies-from-browser chrome \
  --batch-file /Users/alfredkamisese/reel_urls.txt \
  -o "/Volumes/Samsung LED/Instagram Downloads/%(id)s.%(ext)s" \
  --write-info-json --write-thumbnail \
  --sleep-interval 3 --max-sleep-interval 10
```

**Pros:** No manual cookie export, uses Chrome's live cookie store
**Cons:** Requires Chrome closed or running with profile accessible

---

## Complete Batch Command (External SSD Output)

```bash
cd ~/Downloads  # where cookies.txt lives

yt-dlp --cookies cookies.txt \
  --batch-file /Users/alfredkamisese/reel_urls.txt \
  -o "/Volumes/Samsung LED/Instagram Downloads/%(id)s.%(ext)s" \
  --write-info-json \
  --write-thumbnail \
  --sleep-interval 3 \
  --max-sleep-interval 10
```

**Output location:** `/Volumes/Samsung LED/Instagram Downloads/`

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `empty media response` | Cookies stale/invalid | Re-export fresh cookies after login |
| `Unable to extract media` | Post deleted/private/age-gated | Skip or use browser Method B |
| `Sign in required` | Cookies not sent | Check cookie domain (`.instagram.com`) |
| `HTTP 403 Forbidden` | Rate limited / IP blocked | Increase `--sleep-interval` |

---

## Anti-Ban Settings (Critical)

```bash
--sleep-interval 3 \
--max-sleep-interval 10 \
--limit-rate 2M \
--no-playlist
```

- **3-10s random delay** between downloads
- **2MB/s rate limit** to avoid triggering rate limits
- **No playlists** to avoid accidental bulk requests

---

## Testing Single URL First

```bash
yt-dlp --cookies cookies.txt \
  "https://www.instagram.com/reel/DZobVihCQGd/" \
  -o "/Volumes/Samsung LED/Instagram Downloads/%(id)s.%(ext)s"
```

If single URL works → batch will work. If single fails → fix cookies first.

---

## File Structure After Download

```
/Volumes/Samsung LED/Instagram Downloads/
├── DZobVihCQGd.mp4
├── DZobVihCQGd.info.json
├── DZobVihCQGd.jpg
├── DZRgDZwCvI4.mp4
├── DZRgDZwCvI4.info.json
├── DZRgDZwCvI4.jpg
└── ...
```

---

## Post-Download Processing

```bash
# Extract frames (every 3 seconds for 60s reels)
ffmpeg -i "DZobVihCQGd.mp4" -vf fps=1/3 "frames_%03d.png"

# Generate GIFs
ffmpeg -i "frames_%03d.png" -vf "fps=10,scale=720:-1" demo.gif
ffmpeg -i "frames_%03d.png" -filter_complex "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" -loop 0 technique_demo.gif
```