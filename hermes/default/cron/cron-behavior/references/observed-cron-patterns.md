# Observed Cron Job Patterns

- **Schedule**: Every 30 minutes (e.g., 10:34, 11:04, 11:34...).
- **Default Action**: `--push` to sync Hermes memory to the Obsidian vault.
- **Hour/Half‑hour Runs**: Also execute `--status`, which may emit `[SILENT]` when no changes are detected.
- **Silent Suppression**: Outputs exactly `[SILENT]` when there is nothing new to report.
- **Last Verified Run**: 2026-07-23 10:35:20-07:00.
- **Cron Job ID**: 7e54178aa1b0.

These patterns are extracted from the `step-beyond-memory-sync` cron job observations and documented for future reference.