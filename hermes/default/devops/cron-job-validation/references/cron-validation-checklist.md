# Cron Job Validation Checklist

Use this checklist before deploying or trusting any scheduled cron job.

## Pre-Deployment

- [ ] Script exists at the exact path in job config
- [ ] Script is executable (`chmod +x` or shebang + execute bit)
- [ ] Script runs without error manually (same user, same cwd, same env)
- [ ] Script produces expected output/logs/files when run manually
- [ ] Job config has correct `script` path
- [ ] Job config has correct `workdir` (if script uses relative paths)
- [ ] Job config has required `enabled_toolsets` (file, terminal, etc.)
- [ ] Required environment variables are available in cron context
- [ ] **For LLM jobs: Job is explicitly pinned with `--provider` and `--model` at creation time**

## Post-Deployment (after first scheduled run)

- [ ] `cronjob list` shows job enabled with correct schedule
- [ ] `cronjob run <job_id>` executes without error
- [ ] Output file `~/.hermes/cron/output/<job_id>/<latest>.md` shows meaningful agent response
- [ ] **Check for `drift_skip` error in output — indicates model config drift blocking execution**
- [ ] Expected side effects verified:
  - [ ] Files created/moved in target directory
  - [ ] Logs written to expected log file
  - [ ] State file updated with current timestamp/data
  - [ ] Notifications delivered to expected channel
- [ ] No error messages in agent response or script stderr

## Dry-Run Mode Jobs

- [ ] Log file shows planned actions (not empty)
- [ ] State file shows planned moves/changes
- [ ] Validation step runs and reports results
- [ ] Output clearly marked as DRY-RUN (no actual changes)

## Ongoing Monitoring

- [ ] Weekly: spot-check `cronjob list` for jobs stuck in "paused" or "error" state
- [ ] **Weekly: check latest output files for `drift_skip` messages on LLM jobs**
- [ ] Monthly: re-run validation checklist for critical jobs
- [ ] After any system change (OS update, Python version, path changes): full re-validation
- [ ] **After any global inference config change (provider/model): re-pin or recreate all unpinned LLM cron jobs**