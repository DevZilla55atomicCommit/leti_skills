# Duplicate Cron Job Cleanup — Pattern Reference

## Context
Session on 2026-08-31: Found and removed 4 duplicate "Open RugbyPass Live Stream" cron jobs that were one-shot jobs for the same date/time, all completed/failed. Kept the single recurring weekly job.

## Pattern: Detecting Duplicates

```bash
# List all jobs
cronjob list

# Look for:
# - Same/similar names
# - Same schedule (especially one-shot "once at YYYY-MM-DD HH:MM")
# - Same prompt_preview content
# - Jobs in "completed" state that have identical purpose
```

## Pattern: Cleanup Procedure

1. **Identify the canonical job** — the one with recurring schedule (`forever` repeat, cron syntax like `49 7 * * 6`)
2. **Remove all others** — `cronjob remove <job_id>` for each duplicate
3. **Verify** — `cronjob list` confirms only canonical remains

## Applied Example (2026-08-31)

| Job ID | Name | Schedule | Repeat | Status | Action |
|--------|------|----------|--------|--------|--------|
| 7677467d0b0c | Open RugbyPass Live Stream | once at 2026-08-29 07:49 | 1/1 | completed | REMOVED |
| 60acc9bf561b | Open RugbyPass Live Stream (Tomorrow) | once at 2026-08-29 07:49 | 1/1 | completed | REMOVED |
| 98ed139abf85 | Open RugbyPass Live Stream (Tomorrow) | once at 2026-08-29 07:49 | 1/1 | completed | REMOVED |
| 89f0282d141d | Open RugbyPass Live Stream (Tomorrow) | once at 2026-08-29 07:49 | 1/1 | completed (error) | REMOVED |
| **c761c85fd571** | **Open RugbyPass Live Stream (Weekly Saturday 7:49)** | **49 7 \* \* 6** | **forever** | **scheduled** | **KEPT** |

## Checklist for Future Cleanups

- [ ] `cronjob list` — capture full output
- [ ] Group by name pattern / prompt content
- [ ] Identify canonical (recurring, enabled, scheduled)
- [ ] Remove duplicates (one-shot, completed, disabled, error)
- [ ] Verify remaining jobs are unique and correct
- [ ] Check script references are unique (no duplicate script files for same purpose)