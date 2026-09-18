# Cron Script Argument Parsing Fix

## Issue
The cron job `step-beyond-memory-sync` was failing with:
```
Script not found: /Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory.py --push
```

## Root Cause
The Hermes cron scheduler's `_run_job_script()` function treats the entire `script` field as a single file path. It does **not** parse arguments from the string.

When the cron job was configured with:
```json
"script": "sync_step_beyond_memory.py --push"
```

The scheduler looked for a file literally named `sync_step_beyond_memory.py --push` which doesn't exist.

## Solution
Two-part fix:

### 1. Update cron job config (`jobs.json`)
Changed script field to just the script name:
```json
"script": "sync_step_beyond_memory.py"
```

### 2. Update Python script default behavior
Modified `sync_step_beyond_memory.py` to default to `--push` when no arguments provided:

```python
def main():
    # Default to --push for cron job compatibility
    if len(sys.argv) < 2:
        cmd = "--push"
    else:
        cmd = sys.argv[1]
    # ... rest of logic
```

This ensures:
- Cron job runs successfully (no args needed)
- Manual usage with explicit args still works
- Default behavior matches cron job intent (Hermes → Obsidian push)

## Files Changed
- `~/.hermes/cron/jobs.json` - script field: `"sync_step_beyond_memory.py --push"` → `"sync_step_beyond_memory.py"`
- `~/.hermes/scripts/sync_step_beyond_memory.py` - added default `--push` behavior
- Skill reference copy at `skills/memory-management/step-beyond-memory-sync/scripts/sync_step_beyond_memory.py`

## Verification
```bash
# Test cron-like execution (no args)
python3 ~/.hermes/scripts/sync_step_beyond_memory.py
# Output: "Obsidian patterns already in sync with Hermes"

# Test explicit args still work
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --push
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --pull
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --status

# Check job config
cat ~/.hermes/cron/jobs.json | jq '.jobs[0].script'
# "sync_step_beyond_memory.py"
```

## Lesson for Future Cron Jobs
**Never include arguments in the `script` field.** The scheduler doesn't parse them.

Instead:
1. Make the script accept no-args mode with sensible defaults
2. Or use a wrapper script that calls the real script with args
3. Or use the `no_agent: true` mode where the script output becomes the entire job (but then the script must produce the full prompt)