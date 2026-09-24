# Backup Workflow Reference

## Core Process
1. **Pre-Run Backup**: Creates timestamped rsync snapshot of entire vault before organizational changes
2. **Delta Manifest**: Generates file hash manifest for efficient comparison in subsequent runs
3. **Incremental Backups**: Subsequent runs only copy changed files (reduces from ~4min to ~30sec)
4. **Retention Policy**: Configurable (default: keep last 30 days / 10 backups)

## Commands
- `vault-backup create --max-moves 10`: Create backup and generate manifest
- `vault-backup prune --keep-days 30`: Remove old backups
- `vault-backup status`: Show last backup details

## Performance Profile
- First run backup: ~4 minutes (85K files)
- Subsequent backups: ~30 seconds (incremental)
- Storage efficiency: Hard linked snapshots save space
- Monitoring: Automatic duration and file count reporting

## Integration Points
- Hooks into existing cron jobs via `0 3,11,23 * * *` schedule
- Feeds into delta scanning mechanism for fast organization runs
- Generates end-of-run manifest for next-run comparison