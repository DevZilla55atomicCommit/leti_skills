# Obsidian Vault Sync Patterns

## Purpose
Ensures Step Beyond reasoning patterns persist across Hermes restarts by syncing with Obsidian vault files.

## Workflow
1. **Pull (session start)** – `python sync_step_beyond_memory.py --pull` loads Obsidian patterns into user JSON.
2. **Push (session end)** – `python sync_step_beyond_memory.py --push` writes identified patterns to Obsidian file with timestamp.
## Session-end hook – runs on Hermes session close:
   - `session_end_step_beyond.sh` executes `python sync_step_beyond_memory.py --push`
   - Checks modified hash before write
   - Verifies content integrity

## Cron job (configured and active):
   - Managed via Hermes cron system (`.hermes/cron/jobs.json`), not system crontab
   - Job ID: `7e54178aa1b0`, name: `step-beyond-memory-sync`
   - Schedule: every 30 minutes
   - Script: `/Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory.py --push`
   - 398+ runs completed, last status: ok

## Two sync script implementations exist:
1. **Obsidian vault version** (`/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/sync_step_beyond_memory.py`) — appends session marker to existing patterns
2. **Hermes scripts version** (`/Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory.py`) — replaces entire file with Hermes memory content (hash-gated)
   - Cron job uses the Hermes scripts version
   - Session-end hook uses the Obsidian vault version

## Session hooks (not auto-wired):
- `session_start_step_beyond.sh` — pulls patterns at session start (manual `source` required)
- `session_end_step_beyond.sh` — pushes patterns at session end (manual `source` required)
- These are not automatically invoked by Hermes session lifecycle; they're helper scripts for manual use or external integration

## Duplicate-Pattern Handling
- Duplicate detection via SHA‑256 hash of content
- Only new patterns appended; existing patterns preserved
- Hash stored in vault file metadata for future verification

## Verification
- Hash stored in vault file front‑matter
- `step-beyond sync-status` command reports status
- Failed sync records flagged for manual review