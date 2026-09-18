---
name: cron-job-isolation-pitfalls
description: Cron job isolation and one-time test consumption pitfalls.
category: cron
version: 1.0.0
license: MIT
author: Alfred (Maddie)
metadata:
  hermes:
    tags: [cron, background-jobs, isolation, testing, pitfalls]
    related_skills: [cron-behavior, cron-sync-behavior, hermes-agent]
---

# Cron Job Isolation & Pitfalls

## When to Use

- Creating or debugging one-time (`repeat: once`) cron jobs that need testing before their scheduled run
- Any cron job that attempts UI actions (`open_preview`, `computer_use`, terminal interaction) — these will not affect the user's live session
- Understanding why a manually tested cron job didn't fire at its scheduled time
- Diagnosing why a cron job appears healthy but never runs (model drift auto-skip)

---

# Cron Job Isolation & Pitfalls

**Purpose**: Capture critical behavioral patterns of Hermes cron jobs — especially around background session isolation, one-time job test consumption, and silent execution blocks — so future sessions don't repeat the same trial-and-error.

## Background Session Isolation

**Cron jobs run in fresh background sessions** — they are fully isolated from the user's live desktop session.

| What you might expect | What actually happens |
|-----------------------|----------------------|
| `open_preview` in a cron job opens a tab in your desktop app | The cron session has its own isolated desktop; it logs "opened in preview pane" as text output but **cannot touch your live UI** |
| Terminal output from cron appears in your terminal pane | Cron sessions have their own isolated terminals |
| Any UI action (click, type, preview) affects your session | **No cross-session UI access** — each session is a separate Hermes process with its own desktop context |

**Verification**: Test runs on 2026-08-28 confirmed — `cronjob(action='run')` on a job with `open_preview` prompt produced log output saying "Opened https://rugbypass.tv/live/307714 in the preview pane" but the user's actual preview pane was unaffected.

## One-Time Job Test Consumption

**Manual `cronjob(action='run')` consumes the single execution** of a `repeat: once` job.

| Sequence | Result |
|----------|--------|
| Create one-time job scheduled for tomorrow | Job state: `scheduled`, `enabled: true` |
| Run `cronjob(action='run', job_id=...)` to test | Job fires, executes payload, then marks itself `completed`, `enabled: false`, `state: completed` |
| Wait for scheduled time tomorrow | **Job will NOT fire** — it's already consumed |

**Observed**: Three successive jobs (7677467d0b0c, 60acc9bf561b, 98ed139abf85) were created and each consumed by a manual test run. Each required recreation.

### Workarounds

1. **Create with `repeat: 2`** — one execution for test, one for scheduled run
2. **Test the action directly** — use `open_preview` or other tools in the current session instead of `cronjob run`
3. **Recreate after test** — if you must test via `cronjob run`, immediately recreate the job for the scheduled time

## Delivery Target Behavior

- `deliver: 'local'` (default) — output saved to `~/.hermes/cron/output/<job_id>/` only; no message delivered to any chat
- `deliver: 'all'` or `deliver: 'telegram'` etc. — requires gateway connection; delivers result to user's active channels
- Background cron runs are **fire-and-forget** — they don't return to the originating session

## Practical Pattern for "Open URL Tomorrow"

```python
# Instead of a cron job that tries to open preview pane:
# 1. Set a reminder (Reminders.app, Calendar, cron with deliver='all')
# 2. When reminder fires, manually open_preview(url) in your live session
# 3. Or use a gateway-connected delivery so you get a notification with the link
```

---

## Model Drift Auto-Skip (Silent Execution Block)

**New pattern discovered 2026-09-01**: Hermes cron system monitors the global inference config (provider + model) at job creation time. If the global config changes before the job runs, **unpinned jobs are silently blocked** from executing their LLM payload.

### How It Works

1. Job is created with no explicit `--provider` / `--model` (unpinned)
2. Job inherits global inference config at creation time (e.g., `nvidia/nemotron-3-ultra-550b-a55b`)
3. User changes global config (e.g., switches to `nvidia/nemotron-3-nano-30b-a3b`)
4. On next scheduled run, Hermes detects drift: `model 'old' -> 'new'`
5. Job **does not run its prompt** — it writes a `drift_skip` error to output and stays in `scheduled` state
6. Job remains `enabled: true`, `state: "scheduled"` — looks healthy but never executes

### Symptoms

- `cronjob list` shows `last_status: "error"`, `enabled: true`, `state: "scheduled"`
- Output file in `~/.hermes/cron/output/<job_id>/<timestamp>.md` contains:
```
RuntimeError: [drift_skip:silent] Skipped to prevent unintended spend: global inference config drifted since this job was created (model 'nvidia/nemotron-3-ultra-550b-a55b' -> 'nvidia/nemotron-3-nano-30b-a3b'), and this job is unpinned. No inference call was made. To run on the new config, on the host running Hermes pin it explicitly: `hermes cron edit <job_id> --provider <provider> --model <model>` (or pin the original values to keep them). This alert is sent once; the job stays skipped until the config is pinned or restored. See #44585.
```
- **No LLM inference call was made** — the job's prompt never ran

### Affected Jobs (This Session)

| Job ID | Name | Schedule | Original Model | Current Global |
|--------|------|----------|----------------|----------------|
| `7e54178aa1b0` | step-beyond-memory-sync | every 30m | nemotron-3-ultra-550b | nemotron-3-nano-30b |
| `f0343a03d940` | Vault Keeper Daily Light | daily 7am | nemotron-3-ultra-550b | nemotron-3-nano-30b |
| `6c33533dcf96` | Vault Keeper Weekly Deep | weekly Sun 3am | nemotron-3-ultra-550b | nemotron-3-nano-30b |
| `bec54d301c71` | Cinematic Videography Daily | daily 8am | nemotron-3-ultra-550b | nemotron-3-nano-30b |
| `b174ee93649a` | Come Follow Me Weekly Guide | weekly Mon 7am | nemotron-3-ultra-550b | nemotron-3-nano-30b |

### Fix Options (Per Job)

| Option | Command | When to Use |
|--------|---------|-------------|
| **Pin to original model** | `hermes cron edit <job_id> --provider nvidia --model nvidia/nemotron-3-ultra-550b-a55b` | Job was tuned for the larger model; quality matters |
| **Update to current global** | `hermes cron edit <job_id> --provider nvidia --model nvidia/nemotron-3-nano-30b-a3b` | Cost savings acceptable; job works on smaller model |
| **Recreate job** | Delete + recreate with current config | Clean slate; inherits current global |

### Prevention

**Always pin LLM cron jobs at creation**:
```bash
# Explicit provider + model = pinned job (immune to drift-skip)
hermes cron create "My Job" \
  --schedule "0 7 * * *" \
  --provider nvidia \
  --model nvidia/nemotron-3-ultra-550b-a55b \
  --prompt "..."
```

Unpinned jobs are **time bombs** — they will silently stop working the next time you change your global model.

### Detection Checklist

When reviewing `cronjob list`:
- [ ] Any job with `last_status: "error"` but `enabled: true` + `state: "scheduled"`?
- [ ] Check latest output file for `drift_skip` message
- [ ] Verify job has explicit `--provider`/`--model` (pinned) or is expected to drift-skip

### Script-Mode Jobs (`no_agent: true`) Are Immune to Model Drift

**New pattern discovered 2026-09-02**: Jobs with `"no_agent": true` (script mode) are **not affected by model drift auto-skip** because they don't invoke an LLM. The drift-skip mechanism only blocks LLM inference calls.

| Job Type | Affected by Drift-Skip? |
|----------|------------------------|
| LLM agent (`no_agent: false`, has `model`/`provider`) | **Yes** — unpinned jobs silently skip |
| Script mode (`no_agent: true`, `script: "..."`, `model: null`) | **No** — runs as background process, no LLM call |

**Observed**: Job `0995f07a2aa1` (Hermes Backup Cleanup — Daily) has `no_agent: true`, `model: null`, `provider: null`. It ran successfully on schedule at 5 AM daily and via manual test at 11:37 AM, freeing 682 MB of emergency state.db backups, despite global model changing from `nemotron-3-ultra-550b` to `nemotron-3-nano-30b`.

### UI Display Quirk: Script-Mode Jobs May Show "No Runs"

**New pattern discovered 2026-09-02**: The Hermes desktop app's cron view may display "no runs" for script-mode jobs even when they have executed successfully and have output logs.

**Symptoms**:
- `hermes cron list` shows job as active with `last_run_at` and `completed` count
- `~/.hermes/cron/output/<job_id>/` contains timestamped log files for each run
- But desktop UI shows "no runs yet" or empty history

**Root cause hypothesis**: UI may only count LLM-agent executions, not script-mode executions, or there's a display filter bug.

**Verification**: Always check `hermes cron list` (CLI) and `~/.hermes/cron/output/<job_id>/` for ground truth — don't trust the desktop UI alone for script-mode jobs.

---

*Learned from session 2026-08-28: User wanted RugbyPass stream opened at 7:49 AM via cron. Multiple test runs consumed successive one-time jobs. Preview pane opening only works from live session, not background cron.*

*Learned from session 2026-09-01: 5 cron jobs silently blocked by model drift auto-skip. Jobs appeared healthy in `cronjob list` but never executed their LLM payloads. Root cause: global inference config changed from nemotron-3-ultra-550b to nemotron-3-nano-30b after jobs were created.*

*Learned from session 2026-09-02: Script-mode cron jobs (`no_agent: true`) are immune to model drift auto-skip. Desktop UI may incorrectly show "no runs" for script jobs that have actually executed — verify via CLI and output logs.*

*Learned from session 2026-09-03: Come Follow Me Weekly Study Guide cron job (b174ee93649a) — weekly Monday 7am, `no_agent` mode, script `generate_cfm_guide.py`. Had syntax errors in f-strings (unterminated string literal, invalid syntax) causing failures on 2026-08-31 and 2026-09-01 09:54. Fixed and ran successfully at 2026-09-01 10:06:37. Produces comprehensive HTML study guide with 9 sections (3-sentence summary, core message, Q&A, scripture helps, children's table, 4 podcasts, BYU Studies, cheat sheet, sources) saved to `~/Desktop/Come Follow Me 2026/YYYY-MM-WeekX_Topic_DateRange/`. Verification: run script manually, check output directory exists with `.html` file, inspect HTML for all expected sections. No model drift risk (script mode).