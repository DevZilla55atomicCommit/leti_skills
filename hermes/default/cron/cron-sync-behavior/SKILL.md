---
name: cron-sync-behavior
description: Captures cron sync behavior for step-beyond patterns.
category: cron
version: 1.0.0
license: MIT
author: Alfred (Maddie)
---

# Cron Behavior Protocol for Step Beyond Memory Sync

**Purpose**: Document observed cron job behavior for step-beyond-memory-sync to ensure consistent interpretation across sessions.

**Observed Patterns** (verified 2026-08-02):

- **Schedule**: Executes every 30 minutes (timing offsets vary but maintain 30m intervals)
- **Default Action**: No-argument invocation defaults to `--push` (Hermes → Obsidian sync direction)
- **Hour/half-hour Runs**: Trigger `--push` + `--status` (produces visible delivery output)
- **Other Runs**: Trigger `--status` only; emits `[SILENT]` when sync state unchanged
- **Last Verified Sync**: 2026-07-15 18:42; system remains in sync
- **Silent Suppression**: Correctly suppresses delivery when no new patterns exist (`[SILENT]` output)

**Integration Notes**:
- Cron job ID: `7e54178aa1b0`
- Hook scripts: `session_start_step_beyond.sh` (pull), `session_end_step_beyond.sh` (push)
- Verification command: `hermes cron run step-beyond-memory-sync`
- Silent mode adherence: Strictly follows `[SILENT]` convention for no-op cases

**Version**: 1.0.0