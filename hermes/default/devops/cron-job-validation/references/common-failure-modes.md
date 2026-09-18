# Common Cron Job Failure Modes

Real-world failure patterns observed in Hermes cron jobs.

## 1. Missing Script File

**Symptom**: Job shows `executed: true`, `execution_success: true`, but nothing happens.

**Root Cause**: The `script` field in job config points to a path that doesn't exist.

**Example from this session**:
```
Script: /Users/alfredkamisese/vault_organizer.py
```
File didn't exist. Agent ran the prompt but the script wasn't there to execute.

**Fix**: Create the script OR update job config to point to existing script.

---

## 2. Script Exists But Not Executable

**Symptom**: Permission denied when cron tries to run it.

**Fix**: `chmod +x /path/to/script.py` or ensure shebang line (`#!/usr/bin/env python3`) + execute bit.

---

## 3. Wrong Working Directory

**Symptom**: Script runs but can't find input files, writes output to wrong place.

**Root Cause**: Script uses relative paths; cron runs from different cwd than manual test.

**Fix**: Set `workdir` in job config to the directory containing the script's expected inputs.

---

## 4. Missing Environment Variables

**Symptom**: Script fails with "API key not found", "HERMES_HOME not set", etc.

**Root Cause**: Cron environment doesn't inherit shell profile / `.env` automatically.

**Fix**: 
- Export required vars at top of script
- Or set them in job's environment via Hermes config
- Or use `HERMES_HOME` / `get_hermes_home()` for path resolution

---

## 5. Python Environment Mismatch

**Symptom**: `ModuleNotFoundError` for packages installed in venv.

**Root Cause**: Cron uses system python, not the project's virtualenv.

**Fix**: 
- Use full python path: `/path/to/.venv/bin/python script.py`
- Or activate venv in script: `source /path/to/.venv/bin/activate`

---

## 6. Silent Failure (No Logging)

**Symptom**: Job "succeeds" but no evidence it did anything.

**Root Cause**: Script doesn't log; agent has nothing to report.

**Fix**: Add explicit logging to script:
```python
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.info("Starting vault organizer dry-run...")
```

---

## 7. Dry-Run Mode Without Output

**Symptom**: Dry-run job runs but log/state files are empty or missing.

**Root Cause**: Script's dry-run mode doesn't write the planned actions anywhere.

**Fix**: Ensure dry-run mode writes to:
- Log file: `~/.vault-organizer.log` (or job-specific path)
- State file: `~/.vault-organizer-state.json`
- Both should be created even if no actions planned (empty list is valid output)

---

## 8. Skill Not Found

**Symptom**: Agent response starts with `⚠️ Skill(s) not found and skipped: graphify`

**Root Cause**: Job config lists skills that aren't installed/available in the current profile.

**Fix**: 
- Install the skill: `hermes skills install official/...`
- Or remove the skill from job config if not needed
- Or ensure the skill is available in the profile running the cron

---

## 9. Schedule Expression Errors

**Symptom**: Job never runs, or runs at wrong times.

**Root Cause**: Invalid cron expression or interval format.

**Fix**: Validate with `cronjob list` — check `schedule_display` matches intent. Use `crontab.guru` for cron expressions.

---

## 10. Job Stuck in Paused State

**Symptom**: Job shows `state: paused`, `enabled: false`, never runs.

**Root Cause**: Manual pause, or auto-pause after repeated failures.

**Fix**: `cronjob action=resume job_id=<id>` — but first check `last_error` to see why it was paused.

---

## 11. Model Drift Auto-Skip (Silent Block)

**Symptom**: Job shows `last_status: "error"` with error:
```
RuntimeError: [drift_skip:silent] Skipped to prevent unintended spend: global inference config drifted since this job was created (model 'nvidia/nemotron-3-ultra-550b-a55b' -> 'nvidia/nemotron-3-nano-30b-a3b'), and this job is unpinned. No inference call was made. To run on the new config, on the host running Hermes pin it explicitly: `hermes cron edit <job_id> --provider <provider> --model <model>` (or pin the original values to keep them). This alert is sent once; the job stays skipped until the config is pinned or restored. See #44585.
```

**Root Cause**: Global inference config (provider/model) changed since job creation. Hermes cron system detects the drift and **silently blocks execution** to prevent unintended spend on a different model. The job stays in `scheduled` state but never runs its payload.

**Affected Jobs in This Session** (5 jobs):
- `7e54178aa1b0` — step-beyond-memory-sync (every 30m)
- `f0343a03d940` — Vault Keeper Daily Light (daily 7am)
- `6c33533dcf96` — Vault Keeper Weekly Deep (weekly Sun 3am)
- `bec54d301c71` — Cinematic Videography Daily (daily 8am)
- `b174ee93649a` — Come Follow Me Weekly Guide (weekly Mon 7am) — *also has script syntax error*

**Fix Options** (pick one per job):

| Option | Command | Effect |
|--------|---------|--------|
| **Pin to original model** | `hermes cron edit <job_id> --provider nvidia --model nvidia/nemotron-3-ultra-550b-a55b` | Keeps original behavior; job runs on the model it was designed for |
| **Update to current global** | `hermes cron edit <job_id> --provider nvidia --model nvidia/nemotron-3-nano-30b-a3b` | Runs on current global model; may change output quality/cost |
| **Recreate job** | Delete and recreate with current config | Clean slate; inherits current global config |

**Prevention**: When creating cron jobs that use LLM inference, explicitly set `--provider` and `--model` at creation time so the job is **pinned** to a specific config. Unpinned jobs inherit global config at creation time and will drift-skip if global config changes.

**When the CLI lacks pin flags**: older CLIs accept no `--provider`/`--model` on `cron edit` despite what the drift error text suggests — check `hermes cron edit --help` before trusting it. Fallback is a direct store edit: back up `~/.hermes/cron/jobs.json`, set the job's `model`/`provider` plus matching `model_snapshot`/`provider_snapshot`, re-validate the JSON — the gateway picks the change up live with no restart. Never fire a manual `run` to verify a pin on a limited-repeat job — it can burn a repeat; let the next scheduled tick prove it (manual runs are safe only on `forever` jobs).

**Detection**: `cronjob list` shows `last_status: "error"` but `enabled: true` and `state: "scheduled"` — the job *looks* healthy but isn't running. Always check the latest output file in `~/.hermes/cron/output/<job_id>/` for the drift_skip message.