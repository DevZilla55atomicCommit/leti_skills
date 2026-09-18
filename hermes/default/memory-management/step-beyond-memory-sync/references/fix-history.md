# Fix History — Step Beyond Memory Sync

## 2026-07-13: Hermes Memory Format Mismatch & Push Duplication

### Problem
Cron job failed with "Script not found" error, then push produced duplicate content in Obsidian.

**Root causes:**
1. **Format mismatch**: Script expected `{"user": {"entries": [...]}}` but Hermes uses `{"entries": [...]}` directly
2. **Push appended instead of replaced**: Each push added full patterns again, duplicating the file

### Fixes Applied

**sync_step_beyond_memory.py changes:**
1. `read_hermes_memory()` - Normalizes both formats to `{"entries": [...]}`
2. `extract_patterns_from_hermes()` - Uses normalized format
3. `update_obsidian_from_hermes()` - Replaces content (not append), with hash comparison)
4. `show_status()` - Reads normalized format

### Verification
- `--status` shows correct entry counts (1 entry, 1 Step Beyond)
- `--push` reports "already in sync" (idempotent)
- `--pull` reports "already in sync" (idempotent)
- Obsidian file: 66 lines, clean (no duplication)

### Lesson
Always verify the actual on-disk format of Hermes memory files before assuming structure. The `user.json` schema changed from nested `user.entries` to flat `entries`.

### Files Modified
- `/Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory.py` (patched in place)
- This skill updated with fix history

---

## 2026-07-13: Cron Job Script Path Resolution Failure

### Problem
Cron job `step-beyond-memory-sync` failed with "Script not found" error because the `script` field in `jobs.json` included the argument `--push`:
```json
"script": "sync_step_beyond_memory.py --push"
```

The scheduler's `_run_job_script()` function treats the entire string as a file path and validates it against `HERMES_HOME/scripts/`. A file named `sync_step_beyond_memory.py --push` doesn't exist.

### Root Cause
The cron job configuration included CLI arguments in the `script` field, but the scheduler only expects a script path (relative to `HERMES_HOME/scripts/` or absolute). It doesn't parse arguments.

### Fixes Applied

1. **Updated `jobs.json`**: Changed `script` to just `"sync_step_beyond_memory.py"` (no args)
2. **Updated `sync_step_beyond_memory.py`**: Added default behavior - when run without arguments, defaults to `--push` mode (Hermes → Obsidian sync)

### Verification
- Direct execution: `python3 ~/.hermes/scripts/sync_step_beyond_memory.py` → "Obsidian patterns already in sync with Hermes"
- Explicit `--push`: Same result (idempotent)
- `--status`: Shows correct sync status
- Next cron run (scheduled ~00:04) should succeed

### Lesson
The cron job `script` field expects only a script path, not a command with arguments. For default behaviors, make the script itself handle no-argument defaults rather than encoding arguments in the cron config.

### Files Modified
- `/Users/alfredkamisese/.hermes/cron/jobs.json` (script field)
- `/Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory.py` (default to --push)