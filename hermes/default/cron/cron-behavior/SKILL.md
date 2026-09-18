---
name: cron-behavior
description: Observes and documents cron job behaviors for Hermes memory sync.
category: cron
---

# Cron Behavior

This skill captures patterns observed in cron job executions for Hermes memory synchronization and related tasks.

## Key Patterns

- **Schedule**: Regular intervals (e.g., every 30 minutes).
- **Default Action**: Executes a specific operation (e.g., `--push`).
- **Status Reporting**: May emit `[SILENT]` when no changes are detected.
- **Silent Suppression**: Outputs exactly `[SILENT]` to avoid unnecessary delivery.

## Observed Behavior

- The cron job (ID: 7e54178aa1b0) runs every 30 minutes.
- It defaults to `--push` when invoked without arguments.
- At the start of each hour and half-hour, it also runs `--status`, which may emit `[SILENT]`.
- When there is nothing new to report, it outputs exactly `[SILENT]`.