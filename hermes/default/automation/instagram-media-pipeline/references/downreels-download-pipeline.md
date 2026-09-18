# Downreels.com Download Pipeline Reference

> Alternative Instagram Reel download method using downreels.com via Hermes browser tools (headless automation).
> **Use only when Instagram cookies are unavailable** (user ban risk, account restrictions).

---

## When to Use

| Scenario | Primary Method | Fallback |
|----------|----------------|----------|
| User has valid IG account, accepts cookie risk | `yt-dlp --cookies-from-browser firefox` | — |
| **User refuses cookie sharing (ban risk)** | — | **downreels.com via Hermes browser tools** |
| yt-dlp fails (login wall, IP block) | — | downreels.com |
| Quick one-off batch (< 20 URLs) | — | downreels.com |

---

## Pipeline Architecture

```
URLs.txt (10 URLs max/batch)
        │
        ▼
┌────────────────────────────────────────────────────────────────────┐
│  DOWNREELS.COM PIPELINE (Hermes browser tools + Chromium)          │
├────────────────────────────────────────────────────────────────────┤
│  1. Navigate to downreels.com/instagram-reels-downloader/         │
│  2. Fill URL input → click "DOWNLOAD"                             │
│  3. Wait for thumbnail + "Download HD MP4" button                 │
│  4. Trigger download via page.expect_download()                   │
│  5. Save MP4 to ~/Downloads/reels_downreels/{reel_id}.mp4         │
│  4s delay between requests (rate limit)                           │
│  Resume via completed/failed JSON tracking                        │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
   Downloaded MP4s → Stage 2 (Extract) → Stage 3 (Vision) → etc.
```

---

## Integration with Main Pipeline (10-URL Batch)

```bash
# 1. Create urls.txt (one URL per line)
echo "https://www.instagram.com/reel/XXXX/" > /tmp/reels_pipeline/urls.txt

# 2. Run downloader (Hermes browser tools)
# Uses browser_navigate, browser_click, browser_type, browser_snapshot

# 3. Run existing extraction (frames, GIF, transcript)
python3 ~/instagram-davinci-pipeline/scripts/extract.py

# 4. Vision analysis (3 key frames per reel)
python3 ~/instagram-davinci-pipeline/scripts/analyze.py

# 5. Generate skills + vault notes
python3 ~/instagram-davinci-pipeline/scripts/generate_skills.py
python3 ~/instagram-davinci-pipeline/scripts/create_vault_notes.py

# 6. Verify & cleanup
python3 ~/instagram-davinci-pipeline/scripts/cleanup.py
```

---

## Test Results (Session 2026-07-22)

| Reel | URL | Result |
|------|-----|--------|
| AQN40Vz04BypuiVuC2ws5KvNxmzyDnSdQu-WKlVj1sA2ktGpkbl6sUbW6x9OPYhVOIXsh78Gsbb4WMm-J4oQvCcAqargq6Vb72eog5U | instagram.com/p/CUdBRuVDhPX/ | ✅ Downloaded 2.06 MB, 1280×720, 19.2s |

---

## Caveats & Limitations

| Aspect | Detail |
|--------|--------|
| **Quality** | 720p (1280×720) H.264/AAC — NOT 1080p |
| **Auth** | None required (downreels.com uses their own proxy/cookies) |
| **Rate Limit** | ~10-20 req/min before CAPTCHA; enforce 4s delay |
| **Reliability** | Fragile — site changes break selectors; no SLA |
| **Legal/ToS** | Downreels.com scrapes Instagram; user assumes ToS risk |
| **Output** | MP4 in `~/Downloads/reels_downreels/` |
| **Fragile Selectors** | downreels.com HTML changes break automation |
| **No Batch API** | Serial only, ~15-30s per reel |
| **Use Case** | **Only when cookies unavailable** — document as "Downreels fallback" |
| **Cleanup Essential** | MP4s removed after verification (Stage 6) |

---

## Selector Cheatsheet (for Hermes browser tools)

```python
# URL input
'input[placeholder*="Reel" i], input[placeholder*="reel" i], input[type="text"]'

# DOWNLOAD button
'button:has-text("DOWNLOAD")'

# Wait for result
'button:has-text("Download HD MP4")'

# Trigger download
await page.click('button:has-text("Download HD MP4")')
async with page.expect_download(timeout=60000) as dl_info:
    download = await dl_info.value
await download.save_as(output_path)
```

---

## Rate Limiting Protocol

- **4 seconds minimum** between requests
- **Max 10 URLs per batch** (then manual pause)
- **Monitor for CAPTCHA** — if detected, pause 5-10 min
- **Rotate IP** if doing > 50 URLs (VPN/proxy)

---

## Storage Layout

```
/tmp/reels_pipeline/
├── download_reels.py       # Main downloader script (uses Hermes browser tools)
├── urls.txt                # Input: one URL per line
├── downloads/              # MP4 output (reel_id.mp4)
├── completed.json          # Completed reel_ids
├── failed.json             # Failed reel_ids with errors
└── state.json              # Browser session cookies (for reuse)
```

---

## Related Pipeline Stages

| Stage | Script | Purpose |
|-------|--------|---------|
| 1. Download | `downreels` (browser tools) | MP4 → `~/Downloads/reels_downreels/` |
| 2. Extract | `scripts/extract.py` | frames (1fps), GIF (5s), transcript (whisper) |
| 3. Vision | `scripts/analyze.py` | 3 key frames → technique JSON |
| 4. Skill | `scripts/generate_skill.py` | Hermes skill → `~/.hermes/skills/creative/` |
| 5. Vault | `scripts/create_vault_note.py` | Obsidian note → `DaVinci_Knowledge_Base/` |
| 6. Cleanup | `scripts/cleanup.py` | Verify → remove temp MP4/frames/GIFs |

---

## Downreels.com Page Structure (as of 2026-07-22)

```html
<!-- Reels downloader page -->
<input placeholder="Paste Instagram Reel URL" type="text">
<button>DOWNLOAD</button>

<!-- After click, appears: -->
<button>Download HD MP4</button>  <!-- triggers file download -->
```

**Note**: Use the **Reels** downloader page (`/instagram-reels-downloader/`), NOT the Video downloader (`/instagram-video-downloader-free/`). The Reels page handles `/reel/` and `/p/` URLs correctly.

---

## Hermes Browser Tools Implementation

```python
# Using Hermes built-in browser tools (no Playwright dependency)
async def download_via_downreels(url, output_dir):
    # 1. Navigate
    await browser_navigate("https://downreels.com/instagram-reels-downloader/")
    
    # 2. Fill URL
    await browser_type(ref="url_input", text=url)
    
    # 3. Click DOWNLOAD
    await browser_click(ref="download_btn")
    
    # 4. Wait for result (poll with browser_snapshot)
    for _ in range(30):  # max 60s
        snap = await browser_snapshot()
        if "Download HD MP4" in snap.text:
            break
        await asyncio.sleep(2)
    
    # 5. Click Download HD MP4
    await browser_click(ref="download_hd_btn")
    
    # 6. File lands in ~/Downloads/ (headless browser uses host download dir)
    # Move to output_dir
```

---

## Related Files

- `scripts/extract.py` — Stage 2: frames, GIF, transcript
- `scripts/analyze.py` — Stage 3: vision analysis (3 key frames)
- `scripts/generate_skill.py` — Stage 4: Hermes skill generation
- `scripts/create_vault_note.py` — Stage 5: Obsidian vault note
- `scripts/cleanup.py` — Stage 6: verify & remove temp files