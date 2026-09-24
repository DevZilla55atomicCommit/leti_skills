# Cron Job HTTP 500 Retry Pattern

## Issue Encountered
**Date:** 2026-08-24
**Job ID:** `b174ee93649a` (Come Follow Me Weekly Study Guide)
**Schedule:** `0 7 * * 1` (Mondays 7:00 AM PDT)

**Error:**
```
RuntimeError: HTTP 500: Internal server error
```

**Context:** The cron job runs as a scheduled background task with tools: `web`, `file`, `terminal`. The error occurred during STEP 1-2 when fetching the official lesson page from `churchofjesuschrist.org` or BYU Studies.

## Root Cause Analysis
The HTTP 500 is a **server-side error** from the target website, not a client-side issue. Common causes:
- `churchofjesuschrist.org` experiencing high load or maintenance (common early Monday morning)
- BYU Studies rate limiting or temporary unavailability
- Cloudflare/WAF challenge not handled by the scraping approach
- Network transient between the agent runtime and the target servers

## Solution Pattern: Retry with Exponential Backoff

### For Cron Job Configuration
Add a retry wrapper to the cron job's prompt or create a wrapper script:

```python
# In the cron job prompt, add explicit retry logic:
# "If any web fetch returns HTTP 500, wait 60 seconds and retry once. 
# If it fails again, wait 120 seconds and retry a second time. 
# After 3 total attempts, report the failure but include what was successfully fetched."
```

### For Manual Re-run
When the cron job fails, manually re-run via:
```
cronjob action=run job_id=b174ee93649a
```

This triggers a fresh delegation that runs independently of the scheduler.

### Monitoring
Check output directory for new timestamped files:
```
~/.hermes/cron/output/b174ee93649a/
```

A successful run produces:
- `2026-08-24_07-01-21.md` (the run log)
- A new folder in `/Users/alfredkamisese/Desktop/Come Follow Me 2026/` with HTML + images

## Prevention
1. **Shift schedule slightly** — Move from 7:00 AM to 7:15 AM or 7:30 AM to avoid peak Monday morning traffic on Church sites
2. **Add retry logic to prompt** — Explicit "retry on 500" instruction in the cron job prompt
3. **Graceful degradation** — If official lesson fails, fall back to previous week's structure + known scripture block
4. **Cache lesson URLs** — Store known lesson URL patterns to avoid discovery fetches

## Related Skills
- `come-follow-me-lesson-prep` — Similar workflow, may have different error handling
- `churchofjesuschrist-navigation` — Site-specific scraping guidance

## Files to Watch
- `~/.hermes/cron/output/b174ee93649a/*.md` — Run logs
- `/Users/alfredkamisese/Desktop/Come Follow Me 2026/` — Generated guides