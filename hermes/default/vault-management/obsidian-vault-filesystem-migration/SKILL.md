---
name: obsidian-vault-filesystem-migration
description: Migrate Obsidian vault APFS→ExFAT on USB 2.0 for 74x speed.
version: 1.0.0
author: Alfred Kamisese
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [obsidian, vault, migration, filesystem, performance, usb, apfs, exfat]
    category: vault-management
    related_skills: [vault-restructure, vault-setup]
    config: {}
---

# Obsidian Vault Filesystem Migration

Migrate an Obsidian vault from APFS to ExFAT on external USB 2.0 drives to fix catastrophic indexing/startup hangs.

## When to Use

- Obsidian vault on external USB drive loads slowly or hangs on startup
- APFS on USB 2.0 shows < 1 MB/s uncached reads and < 1 MB/s writes
- Vault has 100k+ files and global-search/graph indexing hangs
- Need to reformat drive to ExFAT for 74x write / 200x+ read speedup

## Prerequisites

- Second external drive (or internal SSD) with enough free space for vault copy (~35 GB typical)
- `rsync` available (macOS built-in)
- `diskutil` for reformatting
- Obsidian closed during migration

## Procedure

### 1. Assess Current State

```bash
# Check current filesystem and performance
diskutil info "/Volumes/YOUR_DRIVE" | grep -E "(File System|Protocol)"
dd if=/dev/zero of="/Volumes/YOUR_DRIVE/test_write" bs=1m count=100 2>&1 | tail -1
# APFS on USB 2.0: ~0.87 MB/s write, <1 MB/s uncached read
# ExFAT on USB 2.0: ~64 MB/s write, ~191 MB/s uncached read
```

### 2. Move Heavy Folders Out of Vault (Critical)

Large folders (Transcripts, node_modules, .vault-organizer-backups, Hermes Agent) cause indexing hangs. Move them to drive root temporarily:

```bash
mv "/Volumes/SOURCE/VAULT/HeavyFolder" "/Volumes/SOURCE/HeavyFolder_archived"
```

### 3. Copy Vault to Fast Intermediate Drive (ExFAT)

```bash
rsync -av --progress "/Volumes/SOURCE/VAULT/" "/Volumes/FAST_DRIVE/VAULT/"
# Verify: diff -r SOURCE/VAULT/ FAST_DRIVE/VAULT/ | head -20
# Only ._* AppleDouble metadata files should differ
```

### 4. Reformat Source Drive to ExFAT

```bash
diskutil eraseDisk ExFAT "DRIVE_NAME" /dev/diskX
# Use physical disk identifier (e.g., /dev/disk4), not partition
```

### 5. Copy Vault Back to Reformatted Drive

```bash
rsync -av --progress "/Volumes/FAST_DRIVE/VAULT/" "/Volumes/SOURCE/VAULT/"
diff -r FAST_DRIVE/VAULT/ SOURCE/VAULT/ | head -20
```

### 6. Restore Archived Folders

```bash
mv "/Volumes/SOURCE/HeavyFolder_archived" "/Volumes/SOURCE/VAULT/HeavyFolder"
```

### 7. Restart Obsidian & Verify

```bash
pkill -f "Obsidian"
open -a "Obsidian" --args "/Volumes/SOURCE/VAULT"
# Wait 5-45 min for initial indexing (327k files ~45 min)
# Renderer CPU will drop from 130% to idle, memory from 1.9 GB to ~800 MB
```

## Performance Comparison (Measured)

| Metric | APFS on USB 2.0 | ExFAT on USB 2.0 | Speedup |
|--------|-----------------|------------------|---------|
| Sequential Write | 0.87 MB/s | 64 MB/s | 74x |
| Uncached Read | < 1 MB/s | 191 MB/s | 200x+ |
| Obsidian Startup | Hang/timeout | Seconds | ∞ |

*Measured on Mac mini M4 via `dd` with cache purge. Samsung LED (ExFAT) vs PNY128GBLED (APFS→ExFAT).*

## Pitfalls

1. **Don't format partition** — use `diskutil eraseDisk` on physical disk (`/dev/disk4`), not partition (`/dev/disk4s2`)
2. **Force unmount first** — `diskutil unmountDisk force /dev/diskX` if busy
3. **APFS containers can't be erased directly** — must target physical disk
4. **Drive may disappear after forced unmount** — unplug/replug if not visible in `diskutil list`
5. **327k files takes ~3.2 hours to rsync back** — notify_on_complete recommended
6. **Obsidian indexing 327k files takes ~45 min** — renderer CPU 130% → idle, memory 1.9 GB → 800 MB
7. **Only ._* AppleDouble files differ in diff** — these are macOS extended attributes on ExFAT, harmless

## Verification Checklist

- [ ] `diskutil info /Volumes/DRIVE` shows ExFAT
- [ ] `diff -r` shows only `._*` metadata differences
- [ ] `find VAULT -type f | wc -l` matches expected count (327,559)
- [ ] Obsidian opens file explorer immediately (no hang)
- [ ] Graph view works on demand (not auto-load)
- [ ] Renderer CPU settles to idle, memory < 1 GB after indexing

## References

- `references/apfs-vs-exfat-usb2-performance.md` — benchmark methodology and raw numbers
- `references/obsidian-indexing-behavior.md` — what triggers indexing, how to minimize