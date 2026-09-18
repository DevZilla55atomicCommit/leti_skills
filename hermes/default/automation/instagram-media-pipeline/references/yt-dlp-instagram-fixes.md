# yt-dlp Instagram Extractor Fixes (2026-06-28)

## PR #17075: "Rework extractor" — Merged 2026-06-28
**Author**: bashonly (yt-dlp maintainer)
**Commits**: 5 (d78c1e1, 64e0a46, ac60131, 57ced6d, f49b551)
**Files changed**: `yt_dlp/extractor/instagram.py` (+168/-193 lines)

### Key Changes
1. **Browser impersonation required** for all requests (logged-in and logged-out)
   - Uses `curl_cffi` / `impersonate` to mimic Chrome/Firefox TLS fingerprint
   - Defeats Instagram's bot detection on API endpoints

2. **New GraphQL endpoint** for logged-out extraction
   - Replaces old `__a=1` / `?__a=1&__d=dis` query params
   - Endpoint: `https://www.instagram.com/graphql/query/?query_hash=...`
   - Requires proper `x-ig-app-id`, `x-asbd-id`, `x-ig-www-claim` headers

3. **Fixed "empty media response" error** (Issue #17074)
   - Root cause: Old extractor hit deprecated API that returned empty JSON
   - Fix: New GraphQL query returns proper media metadata

4. **Fixed 404 on accessible reels** (Issue #17124)
   - Root cause: Extractor used wrong PK/shortcode mapping
   - Fix: Proper shortcode → media PK resolution via new endpoint

### Cookie Requirements
```bash
# Minimal working cookies (exported via Get cookies.txt extension)
sessionid=<value>
ds_user_id=<value>
csrftoken=<value>
ig_did=<value>  # optional but recommended
mid=<value>     # optional
```

**Fresh login required**: Cookies rotate ~24h. Export fresh before each batch.

### Working Command (nightly)
```bash
pip install -U --pre yt-dlp
yt-dlp --cookies-from-browser firefox \
       --sleep-interval 2 --max-sleep-interval 5 \
       "https://www.instagram.com/reel/CODE/"
```

### Error Taxonomy
| Error | Meaning | Action |
|-------|---------|--------|
| `HTTP Error 404: Not Found` | Reel deleted/private/geo-blocked | Skip (log as unavailable) |
| `Instagram sent an empty media response` | Old extractor / stale cookies | Update to nightly, refresh cookies |
| `Video info extraction failed: HTTP Error 404` | API endpoint changed | Nightly fixes this |
| `Login required` | Cookies expired/invalid | Re-export cookies.txt |
| `Rate limit (429)` | Too many requests | Back off 60-300s, reduce concurrency |

### Testing Checklist
- [ ] 5 public reels download successfully
- [ ] 2 private reels (own account) download with cookies
- [ ] 3 known-deleted reels return 404 cleanly
- [ ] Metadata includes: duration, caption, timestamp, like count, comment count