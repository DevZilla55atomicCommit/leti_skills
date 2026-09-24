# Instagram Cookie Setup for yt-dlp

## Quick Refresh (when cookies expire ~30 days)

1. **Install** "Get cookies.txt LOCALLY" browser extension (Firefox/Chrome)
2. **Log into** Instagram.com in your browser
3. **Click** the extension → "Export" → saves `cookies.txt`
4. **Rename** to `cookies_www.instagram.com_YYYY-MM-DD.txt`
5. **Move** to `~/Downloads/` (or update `COOKIES_FILE` in script)
6. **Test**: `yt-dlp --cookies "~/Downloads/cookies_www.instagram.com_2026-07-19.txt" --skip-download --print-json "https://www.instagram.com/reel/TEST_CODE/"`

## Pre-Flight Cookie Check (add to pipeline before batch runs)

```bash
# Quick check: sessionid expiry > now + 1 hour?
python3 -c "
import re, time
with open('~/Downloads/cookies_www.instagram.com_2026-07-19.txt') as f:
    for line in f:
        if 'sessionid' in line:
            expiry = int(line.split()[4])
            print(f'sessionid expires: {time.ctime(expiry)}')
            print(f'Time remaining: {(expiry - time.time())/3600:.1f} hours')
            if expiry < time.time() + 3600:
                print('⚠️  EXPIRES SOON — REFRESH COOKIES')
            break
"
```

## Cookie Format Required

Netscape format (what the extension exports):
```
# Netscape HTTP Cookie File
.instagram.com	TRUE	/	TRUE	1819001300	datr	xxx
.instagram.com	TRUE	/	TRUE	1815977300	ig_did	xxx
.instagram.com	TRUE	/	TRUE	1785046319	wd	966x957
.instagram.com	TRUE	/	TRUE	1819002011	csrftoken	xxx
.instagram.com	TRUE	/	TRUE	1792218011	ds_user_id	xxx
.instagram.com	TRUE	/	TRUE	1815977441	sessionid	xxx
.instagram.com	TRUE	/	TRUE	0	rur	xxx
```

## Critical Cookies (must be present)
- `sessionid` — authenticated session
- `ds_user_id` — your user ID
- `csrftoken` — CSRF protection
- `datr` / `ig_did` — device tracking

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Instagram sent an empty media response" | Cookies expired or missing `sessionid` |
| HTTP 404 on reel that works in browser | Cookie domain mismatch — ensure `.instagram.com` |
| Rate limited (429) | Reduce `MAX_WORKERS`, increase `RATE_LIMIT_DELAY` |
| Private/deleted reel | Expected — skip (404 is normal for ~25%) |

## Security Notes

- **Never commit cookies** to git (`.gitignore` them)
- **Rotate cookies** monthly
- **Use dedicated browser profile** for cookie export
- **Don't share** cookie files — they grant full account access