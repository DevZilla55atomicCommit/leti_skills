# ExFAT Migration Checklist for USB 2.0 Vaults

## When to Use
- Vault is on APFS-formatted USB 2.0 drive
- Obsidian startup >10 seconds despite plugin optimization
- You have a second USB drive (ExFAT) or internal space for temporary copy

## Pre-Migration
```bash
# 1. Verify vault size fits on target
du -sh /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault/
df -h /Volumes/Samsung\ LED  # or internal SSD

# 2. Pause cron jobs (if any)
cronjob action=list  # verify all paused
```

## Migration Steps
```bash
# 0. Move ALL archived folders back INTO vault before migration
mv /Volumes/PNY128GBLED/*_archived /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault/

# 1. Copy vault to ExFAT drive (Samsung LED)
rsync -av --progress "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/" "/Volumes/Samsung LED/TamaZila Obsidian Vault/"

# 2. Verify copy (ignore AppleDouble ._* files on ExFAT)
diff -r "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/" "/Volumes/Samsung LED/TamaZila Obsidian Vault/" 2>&1 | grep -v "^\._"

# 3. Test open from ExFAT drive
open -a "Obsidian" --args "/Volumes/Samsung LED/TamaZila Obsidian Vault"
# Should load in <5 seconds

# 4. Reformat PNY to ExFAT (DESTROYS DATA)
# Use PHYSICAL disk (disk4), NOT APFS container (disk8)
diskutil list | grep -i pny   # find correct disk identifier
diskutil eraseDisk ExFAT "PNY128GBLED" /dev/disk4

# If eraseDisk fails (APFS container busy):
diskutil unmountDisk force /dev/disk8
diskutil eraseDisk ExFAT "PNY128GBLED" /dev/disk4

# 5. Copy back to PNY (now ExFAT)
rsync -av --progress "/Volumes/Samsung LED/TamaZila Obsidian Vault/" "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/"

# 6. Resume cron jobs
cronjob action=resume job_id=<id>
```

## Post-Migration Verification
- [ ] Obsidian loads in <5 seconds
- [ ] File explorer shows all folders
- [ ] Graph view works (if enabled)
- [ ] Plugins load correctly
- [ ] Cron jobs run successfully

## Post-Migration Verification
- [ ] Obsidian loads in <5 seconds
- [ ] File explorer shows all folders
- [ ] Graph view works (if enabled)
- [ ] Plugins load correctly
- [ ] Cron jobs run successfully

## Drive Disappearance Issue (Critical)
**Observed:** PNY128GBLED disappeared from `diskutil list` after forced unmount/erase attempts on APFS container (disk8).
**Root cause:** Forced operations on APFS container can cause USB drive to disconnect/become unrecognized.
**Prevention:**
- Always use PHYSICAL disk identifier (`disk4`), not APFS container (`disk8`)
- If drive disappears: unplug and replug USB cable
- Check `diskutil list` and `system_profiler SPStorageDataType` after replug

## Performance Targets (ExFAT on USB 2.0)
| Metric | Target |
|--------|--------|
| Startup time | <5 seconds |
| Renderer CPU (idle) | <5% |
| Memory (idle) | <200 MB |
| Sequential write | 60+ MB/s |
| Uncached read | 190+ MB/s |

## Rollback Plan
If issues arise:
1. Vault still on Samsung LED (ExFAT) — use that
2. Original PNY data gone after reformat — but Samsung copy is pristine
3. Worst case: reformat PNY back to APFS, copy from Samsung LED