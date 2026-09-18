# Disk Space Cleanup Checklist

## Immediate Actions
- [ ] Verify free space: `df -h /System/Volumes/Data`
- [ ] Identify large directories: `du -sh ~/.hermes/*`
- [ ] Remove old emergency backups: `rm ~/.hermes/state.db.pre-update-emergency-*.bak`
- [ ] Delete older pre-update archives: keep only the latest `pre-update-*.zip`

## Optional Deep Clean
- [ ] Truncate old session DBs: `> ~/.hermes/sessions/state.db` if older than 30 days
- [ ] Prune cache directories: `rm -rf ~/.hermes/cache/*`
- [ ] Confirm >10% free space after cleanup

## Safety Checks
- Ensure no critical files are deleted (e.g., current `state.db`, active `settings.yaml`)
- Run `df -h` again to verify reclaimed space