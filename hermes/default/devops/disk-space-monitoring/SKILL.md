---
name: disk-space-monitoring
description: Monitor and free macOS Data volume disk space.
---
# Disk Space Monitoring

## Overview
Procedures to track and reclaim disk space on `/System/Volumes/Data`, focusing on Hermes caches, session stores, and backup archives.

## Triggers
- `df -h` shows >90% usage
- User request to cleanup large `.hermes` folders
- Cron jobs detect high disk usage

## Core Steps
1. **Check Usage**: `df -h /System/Volumes/Data`
2. **Identify Large Areas**: `du -sh ~/.hermes/*`
3. **Delete Old Emergency Backups**: Remove `state.db.pre-update-emergency-*.bak` older than 7 days.
4. **Delete Old Pre‑Update Archives**: Keep latest `pre-update-*.zip`, delete older ones.
5. **Prune Session DBs**: Optionally truncate `sessions/state.db` if >30 days old.
6. **Verify Free Space**: Re‑check usage; ensure >10 % free.

## Support Files
- `references/disk-space-checklist.md` — Manual cleanup checklist.
- `scripts/cleanup-hermes.sh` — Script to enact the above steps.

## Verification
After cleanup, re‑run `df -h` to confirm sufficient free space.