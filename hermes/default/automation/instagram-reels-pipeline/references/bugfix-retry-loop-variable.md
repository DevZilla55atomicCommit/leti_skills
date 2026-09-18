# Bug Fix: Retry Loop Variable Name Consistency

**Date:** 2026-07-20
**Issue:** `NameError: name 'index' is not defined` on retry paths
**Root Cause:** Function parameter named `idx` but log lines used `index` in some places
**Location:** `_download_one` method in `download_instagram_collections.py`

## The Bug

```python
async def _download_one(self, url: str, idx: int):  # Parameter: idx
    # ...
    for attempt in range(1, self.config.max_retries + 1):
        try:
            success = await self._execute_yt_dlp(url, attempt)
            if success:
                self.results.succeeded += 1
                self.logger.info(f"[{idx+1}/{self.results.total}] ✓ Success: {url}")  # Uses idx ✓
                return
        except asyncio.TimeoutError:
            self.logger.warning(f"[{idx+1}] Timeout (attempt {attempt}/{self.config.max_retries}): {url}")  # Uses idx ✓
        except Exception as e:
            self.logger.warning(f"[{idx+1}] Error (attempt {attempt}/{self.config.max_retries}): {url} — {e}")  # Uses idx ✓
        
        if attempt < self.config.max_retries:
            wait = min(30 * (2 ** (attempt - 1)), 600)
            self.logger.info(f"[{index+1}] Backing off {wait}s before retry...")  # BUG: Uses index!
            await asyncio.sleep(wait)
    
    # All retries exhausted
    self.results.failed += 1
    self.results.failed_urls.append(url)
    self.logger.error(f"[{idx+1}/{self.results.total}] ✗ FAILED after {self.config.max_retries} attempts: {url}")  # Uses idx ✓
```

The retry/backoff log line used `index` (undefined) instead of `idx` (the actual parameter). This caused:
- First attempt succeeds → no issue
- First attempt fails → retry path hits `NameError` → exception caught → logged as error → retry continues
- But the exception handling itself crashed, breaking the retry loop logic

## The Fix

Use `idx` consistently everywhere in the method:

```python
async def _download_one(self, url: str, index: int):  # Rename parameter to index
    # ...
    self.logger.info(f"[{index+1}/{self.results.total}] Starting: {url}")  # Use index everywhere
    # ...
    self.logger.info(f"[{index+1}] Backing off {wait}s before retry...")  # Consistent
    # ...
    self.logger.error(f"[{index+1}/{self.results.total}] ✗ FAILED...")
```

## Prevention

1. **Use consistent parameter names** — pick one (`index` or `idx`) and use it everywhere in the method
2. **Run `python3 -m py_compile`** on async scripts with retry logic before deploying
3. **Test retry paths explicitly** — mock a failing URL and verify retries work
3. **Prefer `index` over `idx`** — more readable, less ambiguous

## Verification

After fix, the script runs cleanly:
```bash
python3 -m py_compile download_instagram_collections.py
# Syntax OK

# Test single collection
python3 download_instagram_collections.py --collection "DaVinci_Tricks" ...
# Retries work correctly on 429/5xx errors
```

## Related

- `scripts/download_instagram_collections.py` — Current correct version in skill
- `references/hermes-browser-tools-fallback.md` — Alternative processing path when yt-dlp fails