# Instagram Rate Limits & Operational Observations (Empirical)

## Observed Limits (2026, residential IP, no proxies)

| Operation | Limit | Window | Notes |
|-----------|-------|--------|-------|
| Reel page loads (browser) | ~35 | minute | Hard 429 after ~40 |
| GraphQL API calls (yt-dlp) | ~60 | minute | Higher tolerance with valid cookies |
| Login attempts | 5 | hour | Then 24h lockout |
| Cookie export (Get cookies.txt) | Unlimited | — | Client-side only |
| Video playback (browser) | ~20 | minute | Separate from page loads |

## Backoff Strategy

```python
# Exponential backoff with jitter
async def backoff(attempt: int, base: float = 2.0, max_wait: float = 300.0):
    wait = min(base * (2 ** attempt) + random.uniform(0, 1), max_wait)
    await asyncio.sleep(wait)

# Per-429 response
if response.status == 429:
    retry_after = int(response.headers.get("Retry-After", 60))
    await asyncio.sleep(retry_after + random.uniform(5, 15))
```

## Batch Pattern (Proven)

```python
BATCH_SIZE = 10
BATCH_PAUSE = 60  # seconds

for i, url in enumerate(reel_urls):
    await process_reel(url)
    
    if (i + 1) % BATCH_SIZE == 0:
        print(f"Batch complete ({i+1}/{len(reel_urls)}), pausing {BATCH_PAUSE}s...")
        await asyncio.sleep(BATCH_PAUSE)
```

## IP Reputation Factors

| Factor | Impact |
|--------|--------|
| Residential IP (home) | Baseline limits |
| Datacenter IP (VPS) | 10x stricter, immediate 429 |
| VPN exit node | Often blocked entirely |
| Cookie freshness | Fresh cookies = 2x higher limits |
| User-Agent consistency | Chrome 126+ required |

## Session Lifecycle

```
Fresh login → Export cookies.txt → Batch 1 (10 reels) → 60s pause
                                                  ↓
                                              Batch 2 → 60s pause
                                                  ↓
                                              ... → Cookie refresh at ~20h
                                                  ↓
                                              Fresh cookies → Continue
```

## Error Classification

### Retryable (Transient)
- `429 Too Many Requests` — back off, retry
- `5xx Server Error` — Instagram issues, retry with backoff
- Network timeout — retry once

### Non-Retryable (Permanent)
- `404 Not Found` — Reel deleted/private/geo-blocked
- `403 Forbidden` — Account banned / IP blocked
- `Login required` — Cookies expired (refresh cookies, don't retry same)

### Conditional
- `Empty media response` — Fixed in yt-dlp nightly; if on nightly, treat as 404

## Monitoring & Metrics

Track per-session:
```python
metrics = {
    "total": 0,
    "success": 0,
    "failed_404": 0,
    "failed_429": 0,
    "failed_other": 0,
    "cookies_refreshed": 0,
    "start_time": time.time()
}
```

Target success rate: **>75%** (accounts for ~20% deleted/private reels being normal)

## Cookie Management

### Export (Get cookies.txt extension)
1. Login to Instagram in Firefox/Chrome
2. Click extension → "Export cookies.txt"
3. Save to `~/cookies/instagram_$(date +%Y%m%d).txt`

### Validate Before Batch
```bash
# Quick validation
yt-dlp --cookies cookies.txt --skip-download --print-json "https://instagram.com/reel/VALID_CODE/"
# Should return JSON with duration, title, etc.
```

### Rotation Schedule
- **Every 20 hours** or **every 500 reels** (whichever first)
- Keep last 3 cookie files for rollback
- Log which cookie file used per batch for debugging

## Playwright-Specific Limits

| Limit | Value | Workaround |
|-------|-------|------------|
| Contexts per browser | 4-6 | Multiple browser processes if needed |
| Pages per context | 1 (sequential) | Don't reuse pages |
| Video recording size | 720x1280 | Matches Reel aspect ratio |
| Max video duration | 30s (default) | `record_video_size` doesn't limit duration |

## Scaling Beyond Single Machine

If >500 reels/day needed:
1. **Multiple residential IPs** (different households / 4G dongles)
2. **Cookie pool** (5-10 accounts, rotate)
3. **Queue system** (Redis + workers) with per-IP rate limiting
4. **Monitoring** (Grafana + Prometheus) for 429 rates

**Current pipeline (this project)**: Single Mac mini, single IP, ~200 reels/session — well within limits.