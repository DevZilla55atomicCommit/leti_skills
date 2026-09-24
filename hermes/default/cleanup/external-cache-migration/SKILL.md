---
title: External Cache Migration
description: Permanent migration of cache folders to external storage using symlink to free internal disk space without disrupting applications.
category: cleanup
tags:
  - cache
  - symlink
  - davinci-resolve
created: 2026-07-13
name: external-cache-migration
---

# External Cache Migration for DaVinci Resolve & Cache Folders

## Objective
Permanently move cache folders (DaVinci Resolve, HyperDictionary, cacheClip) to external storage via symlink to free internal disk space without disrupting application functionality.

## Prerequisites
- External SSD with sufficient free space (min 2x cache size)
- SSD formatted as APFS (not NTFS)
- System recognizes external drive as mounted volume
- Current cache folder usage ≤ 80% of external drive capacity

## Step-by-Step Workflow

### 1. Verify Cache Size & Destination
```bash
du -sh ~/Movies/CacheClip/ 2>&1 && df -h "/Volumes/Samsung LED" 2>&1
```

### 2. Copy Cache to External
```bash
rsync -av --progress ~/Movies/CacheClip/ "/Volumes/Samsung LED/Davinci_Backup_Cache/CacheClip/"
```

### 3. Safety Verification
```bash
du -sh "/Volumes/Samsung LED/Davinci_Backup_Cache/CacheClip/" 2>&1 && du -sh ~/Movies/CacheClip/ 2>&1
```

### 4. Create Symlink (Replace Internal with External)
```bash
mv ~/Movies/CacheClip ~/Movies/CacheClip.old && \
ln -s "/Volumes/Samsung LED/Davinci_Backup_Cache/CacheClip" ~/Movies/CacheClip
```

### 5. Verify Symlink Functionality
```bash
ls -la ~/Movies/CacheClip && du -sh ~/Movies/CacheClip/
```

### 6. Cleanup (Optional)
```bash
rm -rf ~/Movies/CacheClip.old/ 2>/dev/null
```

## Critical Safety Checks
✅ **SSD Mounted**: Confirm external drive is visible in Finder/Disk Utility
✅ **Disk Space**: External drive must have ≥ 1.5x current cache size
✅ **Symlink Test**: Run `ls -la ~/Movies/CacheClip` before and after
✅ **Application Test**: Launch DaVinci Resolve and verify cache loads correctly
✅ **Rollback**: `mv ~/Movies/CacheClip.old ~/Movies/CacheClip` if issues occur

## Common Pitfalls & Fixes
| Symptom | Cause | Fix |
|---------|-------|-----|
| "Cache folder missing" | Incorrect symlink path | Verify target path exists (`ls -la /Volumes/.../CacheClip`) |
| Resolution degradation | External drive unmounted | Re-mount SSD and re-run steps 2-4 |
| "Permission denied" | Wrong ownership permissions | `sudo chown -R $(whoami) "/Volumes/Samsung LED/Davinci_Backup_Cache/CacheClip"` |
| Disk space not freed | Cache still writing to internal | Check `du -sh ~/Movies/CacheClip` after move |

## Verification Checklist
1. `df -h /` shows internal disk space increased by cache size
2. DaVinci Resolve launches without errors
3. New media imports show cache location on external SSD
4. `ls -la ~/Movies/CacheClip` confirms symlink points to external path
5. `du -sh ~/Movies/CacheClip` matches external drive usage

## When to Repeat
- After adding new media to be optimized
- When external SSD capacity drops below 20% free space
- After macOS updates that may reset symlink permissions
- Before starting new large projects

## Integration Notes
Works with **DaVinci Resolve CacheClip**, **HyperDictionary**, and **Playwright Cache**. This workflow was executed during Phase 3 storage optimization (external cache migration) and includes production-tested verification steps that confirm symmetric usage across internal/external locations.
- Compatible with **Step Beyond** lifecycle management
- Preserves all existing cache functionality
- Enables indefinite external storage expansion

**Related but Distinct:** Vault migration (Obsidian vaults → external APFS) is covered in `vault-optimize` / `vault-setup` → `references/external-vault-migration.md`. Cache migration targets *application cache folders* (CacheClip, etc.), not the vault itself. Keep them separate: vault on external for portability, active render cache on internal NVMe for speed.