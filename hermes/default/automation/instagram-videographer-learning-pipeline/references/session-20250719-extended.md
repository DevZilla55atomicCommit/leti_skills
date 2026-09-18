# Session 2025-07-19 Extended — Instagram Pipeline Completion & External SSD Setup

## Summary
Extended session completing the pipeline setup for the remaining 210 login-walled Reels.

## Key Accomplishments

### 1. External SSD Output Path Configured
- **Path:** `/Volumes/Samsung LED/Instagram Downloads/`
- **Verified:** Directory exists, writable, empty
- **yt-dlp output template:** `-o "/Volumes/Samsung LED/Instagram Downloads/%(id)s.%(ext)s"`
- **Preserves Mac Mini SSD storage**

### 2. URL List Generated
- **File:** `/Users/alfredkamisese/reel_urls.txt`
- **Count:** 205 Reel URLs (remaining after 9 processed)
- **Format:** One URL per line, ready for yt-dlp `--batch-file`

### 3. yt-dlp Cookie Troubleshooting Documented
**Error:** `Instagram sent an empty media response`
**Root Cause:** Stale/invalid cookies.txt
**Fixes documented:**
- Re-export fresh cookies after logging into Instagram in Chrome
- Use "Get cookies.txt" Chrome extension → Export
- Verify Netscape format with required cookies: `sessionid`, `ds_user_id`, `csrftoken`, `mid`, `ig_did`
- Alternative: `--cookies-from-browser chrome` (no manual export)

### 4. Burner Profiles Debunked
**Why they fail:**
- Phone verification required (real SMS)
- Behavioral analysis (no history = instant flag)
- IP reputation (datacenter/VPN = auto-block)
- 2FA requirement
- Account warming: 2-4 weeks daily manual use
- Success probability: <5%

### 5. Third-Party Downloaders Warned Against (downreels.com)
**Why they fail:**
- Their server IPs get rate-limited/banned
- They log all your URLs
- Can't access private/age-gated content
- Your residential IP + browser session is the only reliable path

### 6. Telegram Notification Config Reminder
- **Required:** `allowed_chats` in `~/.hermes/config.yaml`
- **Format:** `allowed_chats: ["-1001234567890"]` (chat ID with `-100` prefix)
- Without this, batch completion notifications won't deliver

### 7. Pipeline Status
| Content Type | Total | Processed | Remaining |
|--------------|-------|-----------|-----------|
| Carousels | 29 | 27 | 2 (1 misclassified) |
| Reels | 214 | 9 | 205 |
| **Total** | 243 | 36 | 207 |

**Methods:**
- Carousels (27): Browser vision analysis (zero auth)
- Reels (9): Method B - Browser frame capture (720×1280, 3 frames, GIFs)
- Reels (205): Need yt-dlp + cookies (external SSD) OR browser automation

### 8. yt-dlp Command Ready for External SSD
```bash
cd ~/Downloads
yt-dlp --cookies cookies.txt \
  --batch-file /Users/alfredkamisese/reel_urls.txt \
  -o "/Volumes/Samsung LED/Instagram Downloads/%(id)s.%(ext)s" \
  --write-info-json \
  --write-thumbnail \
  --sleep-interval 3 \
  --max-sleep-interval 10
```

### 9. Post-Download Processing (Local)
```bash
# Per reel: frames + GIFs
ffmpeg -i "DZobVihCQGd.mp4" -vf fps=1/3 "frames_%03d.png"
ffmpeg -i "frames_%03d.png" -vf "fps=10,scale=720:-1" demo.gif
ffmpeg -i "frames_%03d.png" -filter_complex "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" -loop 0 technique_demo.gif
```

## Key Learnings

1. **External SSD path works** - Samsung LED drive mounted at `/Volumes/Samsung LED/`
2. **Cookie freshness is critical** - Instagram cookies expire ~30 days; must re-export after login
3. **Method B (browser frames) is production-ready** - 720×1280 capture, 3 frames, GIF generation working
4. **Zero-auth path for carousels** - Browser vision handles all carousel posts without download
5. **Login-walled Reels need yt-dlp + cookies** - 205 remaining require authenticated download
6. **Burner profiles are dead end** - Meta's anti-bot stack makes them infeasible
6. **Third-party sites are worse than useless** - They get banned, log your data, can't access private content

## Next Actions
1. Export fresh cookies.txt from Chrome after Instagram login
2. Run yt-dlp batch command above
3. Process downloaded MP4s locally (frames, GIFs, vault notes)
4. Process remaining 2 carousels via browser vision
5. Set up Telegram `allowed_chats` for batch notifications