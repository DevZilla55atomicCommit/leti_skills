# Session Learnings: PNY128GBLED → ExFAT Migration (2026-08-06)

## Context
- **Source**: PNY128GBLED (128 GB, APFS, USB 2.0) — 34 GB vault
- **Target**: Samsung LED (128 GB, ExFAT, USB-C) — 60 GB free initially
- **Goal**: Reformat PNY to ExFAT, move vault back for performance

## Key Learnings

### 1. Space Requirements
- Samsung LED had **60 GB free** but vault is **~34 GB** — only ~26 GB margin after copy
- **Recommendation**: Target drive needs **≥2x vault size** free for comfortable rsync + verification
- After copy, Samsung LED had **2.17 GB free** — too tight for safety

### 2. PNY Drive Disconnect During Format
- `diskutil unmountDisk force` + `diskutil eraseDisk` caused PNY to disappear from `diskutil list`
- Drive had to be physically unplugged/replugged to reappear as `/dev/disk4` (GUID partition scheme)
- **Fix**: Try gentle unmount first (`diskutil unmount`), only force if needed

### 3. Heavy Folders Causing Index Hangs
These folders were moved OUT of vault before migration (restored after):
| Folder | Size | Files | Issue |
|--------|------|-------|-------|
| `Transcripts/` | 837 MB | 3,350 | Caused indexing hangs |
| `.vault-organizer-backups/` | Unknown | — | `du` timed out |
| `.vault-organizer-manifests/` | Unknown | — | `du` timed out |
| `graphify-out/` | 752 KB | — | Cache folder |
| `emai-dashboard/node_modules/` | 56 MB | — | npm cache |
| `.agents/`, `.claude/` | Small | — | Hidden folders |

### 4. Rsync Performance on USB 2.0
- **34 GB took ~3+ hours** (8.5% done at 3.2 hours)
- Average ~3-4 MB/s (matches ExFAT write speed on USB 2.0)
- **232,224 files** — many small files slow things down
- `notify_on_complete` essential for long transfers

### 5. Diff Verification
- Only differences were `._*` AppleDouble metadata files (ExFAT creates these for extended attributes)
- **No actual content differences** — copy was clean

### 6. Cron Jobs
- All 4 vault-related cron jobs were **already paused** — no conflicts during migration

## Updated Pre-Migration Checklist Additions

```bash
# 1. Verify target has ≥2x vault size free
df -h /Volumes/TARGET_DRIVE

# 2. Gentle unmount first (avoid drive disconnect)
diskutil unmount /dev/diskX
# Only if needed:
diskutil unmountDisk force /dev/diskX

# 3. Move these OUT before rsync (add to skill's pre-migration cleanup)
mv "/path/to/vault/Transcripts" "/Volumes/DRIVE/Transcripts_archived"
mv "/path/to/vault/.vault-organizer-backups" "/Volumes/DRIVE/.vault-organizer-backups_archived"
mv "/path/to/vault/.vault-organizer-manifests" "/Volumes/DRIVE/.vault-organizer-manifests_archived"
mv "/path/to/vault/graphify-out" "/Volumes/DRIVE/graphify-out_archived"
mv "/path/to/vault/emai-dashboard/node_modules" "/Volumes/DRIVE/emai-dashboard_node_modules_archived"
mv "/path/to/vault/.agents" "/Volumes/DRIVE/.agents_archived"
mv "/path/to/vault/.claude" "/Volumes/DRIVE/.claude_archived"

# 4. Expect 3+ hours for 34 GB on USB 2.0 ExFAT
rsync -avh --progress --exclude='.DS_Store' ... /source/ /target/

# 5. Verify only ._* files differ
diff -r /source/ /target/ | grep -v "^\._"
```

## Post-Migration
- All archived folders moved back into vault
- PNY128GBLED reformatted to ExFAT successfully
- Rsync back to PNY in progress (~3.2 hours, ~8.5% done)
- Samsung LED now has only 2.17 GB free (tight)