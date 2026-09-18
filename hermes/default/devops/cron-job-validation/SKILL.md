---
name: cron-job-validation
description: Validate cron jobs do real work, not just return ok.
version: "1.0"
author: Hermes Agent
license: MIT
platforms: [linux, macos]
tags: [cron, validation, testing, scheduled-jobs, reliability]
category: devops
metadata:
  hermes:
    tags: [cron, validation, testing, scheduled-jobs, reliability]
    category: devops
    related_skills: [cron-behavior, cron-sync-behavior]
    config: {}
---

# Cron Job Validation

This skill covers the practice of verifying that scheduled cron jobs do what they claim to do — not just that the agent returns "ok" when the job runs.

## The Core Problem

A cron job can report **success** (the agent completes its turn without error) while doing **nothing useful** because:
- The referenced script doesn't exist on disk
- The script exists but has wrong permissions or syntax errors
- The script runs but produces no output or wrong output
- The working directory is wrong so relative paths fail
- Environment variables (API keys, paths) aren't set in the cron context

## When to Use

- After creating or modifying any cron job that runs a script
- Before relying on a cron job for production work
- When a cron job "succeeds" but expected side effects (files, logs, notifications) don't appear
- As part of any deployment/checklist for scheduled automation

## Validation Checklist

### 1. Script Existence & Executability
```bash
# Check the script exists and is executable
ls -la /path/to/script.py
# If Python: python3 /path/to/script.py --help  # or dry-run flag
# If shell: bash -n /path/to/script.sh         # syntax check
```

### 2. Dry-Run the Script Manually
Run the script exactly as cron would — same working directory, same env:
```bash
cd /correct/working/directory
HERMES_HOME=~/.hermes python3 /path/to/script.py
```
Verify it produces expected output/logs/files.

### 3. Test the Cron Job via `cronjob run`
```bash
# In Hermes CLI or via tool:
cronjob action=run job_id=<id>
```
Then **check the actual output**, not just the "executed: true" flag. Look at:
- `~/.hermes/cron/output/<job_id>/<timestamp>.md` — the agent's response
- Any log files the script writes
- Any state files the script updates

### 4. Verify Side Effects
Confirm the job did what it promised:
- Files created/moved? → `ls -la /target/dir`
- Logs written? → `tail /path/to/log`
- State file updated? → `cat /path/to/state.json`
- Notifications delivered? → Check the delivery channel

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "executed: true" but no output | Script missing or silent failure | Add explicit logging; check script path |
| Script works manually, fails in cron | Wrong cwd, missing env vars, PATH diff | Set `workdir` in job; export env in script |
| Permission denied | Script not executable | `chmod +x script.py` |
| Module not found | Wrong python env / venv not activated | Use full python path or activate venv in script |
| **Command not found / unknown command** | Typo in CLI command inside script/prompt | Verify exact command syntax (e.g. `graphify query` not `graphify q`) |
| **Duplicate cron jobs** | Multiple jobs created with same purpose/schedule | `cronjob list` → identify duplicates → `cronjob remove <job_id>`; keep only the recurring/active one |
| Model drift auto-skip (`drift_skip`, looks scheduled but never runs) | Global model changed since unpinned job creation | Pin the job (CLI flags, or direct `jobs.json` edit on older CLIs); never test-pin with a manual `run` on limited-repeat jobs — full recipe in `references/common-failure-modes.md` #11 |

## Pitfalls

- **Trusting "last_status: ok" blindly** — it only means the agent didn't crash
- **Assuming the script path in the job config is correct** — verify it exists on the target machine. On Hermes hosts scripts live in `~/.hermes/scripts/`, not `~/.hermes/cron/scripts/` (which does not exist) — check the concrete dir first.
- **Reading clustered `last_run_at` timestamps as the natural schedule** — several jobs sharing the same run minute means a manual test burst (`cronjob run` batch), not proof each schedule fires on its own. Confirm each job also has a natural-tick output at its own scheduled time.
- **Reading `next_run_at` without comparing to now** — a `next_run_at` in the past with `state: scheduled` means the scheduler is behind or stuck; a near-future one is healthy. Always run `date` alongside `cronjob list`.
- **Not testing with the same user/context as cron** — cron runs as the user who started the scheduler; test as that user
- **Forgetting that `cronjob run` executes immediately** — it bypasses the schedule but uses the same job config

## Fleet Health Check (all jobs at once)

When asked to check every cron job, batch read-only probes before opening any output file:
```bash
ls -lh ~/.hermes/scripts/
for j in <job_id_1> <job_id_2> ...; do echo "=== $j ==="; ls -t ~/.hermes/cron/output/$j/ | head -n 3; done
python3 -m py_compile ~/.hermes/scripts/<each_job_script>.py
```
Then `head -n 30` only the latest output per job and confirm each shows its promised side effect (file push, findings report, bytes freed, reminder text) — an `ok` with a header-only or skill-dump body is a silent failure.

## Verification Steps

After any cron job change:
1. `cronjob list` → confirm job shows enabled, correct schedule, correct script path
2. `cronjob run <job_id>` → trigger immediate execution
3. Check `~/.hermes/cron/output/<job_id>/<latest>.md` for the actual agent response
4. Verify expected side effects (files, logs, state, notifications)
5. If dry-run mode: confirm the log/state shows planned actions correctly

## References

- `references/cron-validation-checklist.md` — printable checklist for deployments
- `references/common-failure-modes.md` — expanded table with real examples
- `references/vault_organizer_cron.md` — Vault Organizer dry-run job validation specifics

## Scripts

- `scripts/validate-cron-job.py` — automated validation: checks script exists, runs dry-run, verifies output shape