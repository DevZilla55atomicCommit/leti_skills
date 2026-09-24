---
name: obsidian-vault-migration
description: "Move Obsidian vault to external drive with path updates."
trigger: "When moving an Obsidian vault to external drive (new drive, failure, space constraints, multi-machine sync)."
---

# Obsidian Vault Migration

Complete workflow for migrating an Obsidian vault to external storage with path updates, verification, and backward compatibility.

## Prerequisites

- Target external drive connected and visible in `/Volumes/`
- Sufficient space on target (vault size + 20% buffer)
- Vault not open in Obsidian during migration
- Backup of critical `.obsidian/` config folder

## Workflow

### 1. Prepare Target Drive

```bash
# Check current format
diskutil info /Volumes/TARGET_DRIVE/ | grep -E "File System|Format"

# Choose filesystem based on drive interface:
# - Internal NVMe/SSD (fast): APFS — symlinks, xattrs, journaling, snapshots
# - External USB 2.0/3.0 (slow): ExFAT — NO journaling, NO copy-on-write, 74x faster writes, 200x+ faster uncached reads
# - Cross-platform (Windows/macOS/Linux): ExFAT

# For USB 2.0 drives, REFORMAT TO EXFAT:
diskutil eraseDisk ExFAT "VOLUME_NAME" /dev/diskX

# For internal/fast drives, use APFS:
diskutil eraseDisk APFS "VOLUME_NAME" /dev/diskX

# Verify
diskutil info /Volumes/VOLUME_NAME/ | grep -E "File System|Format|Size|Free"
```

**Filesystem Choice Critical on Slow Interfaces (USB 2.0):**
- **APFS on USB 2.0:** Catastrophically slow — journaling + copy-on-write + checksums saturate bus. Uncached reads < 1 MB/s, writes ~0.87 MB/s.
- **ExFAT on USB 2.0:** Simple allocation table, no journaling, no copy-on-write. Uncached reads ~191 MB/s, writes ~64 MB/s.
- **Test your drive:** `dd if=/dev/zero of=/Volumes/DRIVE/test bs=1m count=100` — expect >50 MB/s write on ExFAT/USB 2.0.

**Why APFS fails on USB 2.0:** Every file op triggers journal writes, COW metadata updates, checksum calculations — metadata churn saturates 35 MB/s bus before data moves.

### 2. Full Rsync Transfer

```bash
# Dry run first (preview)
rsync -avh --dry-run --progress \
  --exclude='.DS_Store' --exclude='*/.DS_Store' \
  --exclude='*/.syncthing.*.tmp' --exclude='*.sync-conflict-*.md' \
  --exclude='*/.vault-organizer-backups/' --exclude='*/.vault-organizer-manifests/' \
  --exclude='*/.agents/' --exclude='*/.claude/' \
  --exclude='*/node_modules/' --exclude='*/Transcripts/' \
  --exclude='*/Hermes Agent/' \
  "/path/to/source/vault/" "/Volumes/VOLUME_NAME/vault/"

# Actual transfer (migrate to ExFAT on USB 2.0)
rsync -avh --progress \
  --exclude='.DS_Store' --exclude='*/.DS_Store' \
  --exclude='*/.syncthing.*.tmp' --exclude='*.sync-conflict-*.md' \
  --exclude='*/.vault-organizer-backups/' --exclude='*/.vault-organizer-manifests/' \
  --exclude='*/.agents/' --exclude='*/.claude/' \
  --exclude='*/node_modules/' --exclude='*/Transcripts/' \
  --exclude='*/Hermes Agent/' \
  "/path/to/source/vault/" "/Volumes/VOLUME_NAME/vault/"

# Verify
du -sh /path/to/source/vault /Volumes/VOLUME_NAME/vault
find /path/to/source/vault -type f | wc -l
find /Volumes/VOLUME_NAME/vault -type f | wc -l
```

**Pre-migration Cleanup (Critical for USB 2.0):**
Move heavy folders OUT of vault before rsync to avoid indexing hangs:
```bash
# Move these OUT first (restore after migration if needed)
mv "/path/to/vault/Hermes Agent" "/Volumes/DRIVE/Hermes_Agent_archived"
mv "/path/to/vault/Transcripts" "/Volumes/DRIVE/Transcripts_archived"
mv "/path/to/vault/emai-dashboard/node_modules" "/Volumes/DRIVE/emai-dashboard_node_modules_archived"
mv "/path/to/vault/graphify-out" "/Volumes/DRIVE/graphify-out_archived"
mv "/path/to/vault/.vault-organizer-backups" "/Volumes/DRIVE/.vault-organizer-backups_archived"
mv "/path/to/vault/.vault-organizer-manifests" "/Volumes/DRIVE/.vault-organizer-manifests_archived"
mv "/path/to/vault/.agents" "/Volumes/DRIVE/.agents_archived"
mv "/path/to/vault/.claude" "/Volumes/DRIVE/.claude_archived"
```

**Performance Data (PNY128GBLED USB 2.0):**
| Filesystem | Sequential Write | Uncached Read | Random 4K Read |
|------------|------------------|---------------|----------------|
| APFS       | 0.87 MB/s        | < 1 MB/s      | ~0.15s/100 ops |
| ExFAT      | 64 MB/s          | 191 MB/s      | ~0.15s/100 ops |

ExFAT is **74x faster writes, 200x+ faster uncached reads** on USB 2.0.

### 3. Create Backward-Compatibility Symlink

```bash
ln -sfn "/Volumes/VOLUME_NAME/vault" ~/vault_symlink_name
```

Keeps hardcoded scripts/aliases working.

### 4. Update Absolute Paths in Vault Files

**Search for old paths:**
```bash
grep -r "/old/absolute/path" "/Volumes/VOLUME_NAME/vault" \
  --include="*.md" --include="*.json" --include="*.csv" \
  --include="*.py" --include="*.sh" -l
```

**Categories to update:**
| Category | Files | Priority |
|----------|-------|----------|
| Obsidian plugin configs | `.obsidian/plugins/*/data.json` | High |
| Runtime scripts | `*.sh`, `*.py` with hardcoded paths | High |
| Core navigation | `Hero_index.md`, `MASTER_INDEX.md` | High |
| Pipeline configs | `PIPELINE_PLAN.md`, queue files | Medium |
| Exports/exports | `knowledge_base_export.csv/json` | Medium |
| Generated caches | `graphify-out/`, `venv/` | **Skip** (regenerate) |

**Batch update pattern:**
```bash
# Single file
sed -i '' 's|/old/path|/new/path|g' file.md

# Multiple files (use with caution)
grep -r "/old/path" --include="*.md" -l | xargs sed -i '' 's|/old/path|/new/path|g'
```

### 5. Clean Up Stale Files

```bash
# Sync-conflict files from Syncthing
rm "/Volumes/VOLUME_NAME/vault/path/*.sync-conflict-*.md"

# Old .DS_Store (regenerates)
find "/Volumes/VOLUME_NAME/vault" -name ".DS_Store" -delete
```

### 6. Verify All Systems

| Check | Command |
|-------|---------|
| Obsidian opens | Open vault in Obsidian → test search, graph, plugins |
| Plugin configs | Check `.obsidian/plugins/*/data.json` cwd paths |
| Runtime scripts | `source script.sh` — verify path resolution |
| Python scripts | `python3 script.py --help` — verify imports/paths |
| Symlink | `ls -la ~/vault_symlink_name` |
| Rsync diff | `rsync -avh --dry-run --delete --exclude='.DS_Store' ...` |

### 7. Update External References

- Hermes persistent memory (`memory` tool)
- User profile memory (`user` tool)
- Shell aliases/rc files
- Cron jobs
- IDE/workspace configs

### 8. Remove Old Vault (After Verification)

```bash
# Only after ALL verification passes
rm -rf "/path/to/old/vault"
```

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| FAT32/exFAT on target (internal drive) | Use APFS for internal/fast drives; ExFAT only for slow USB 2.0/3.0 or cross-platform |
| **APFS on USB 2.0** | **Never use APFS on USB 2.0 for active vaults — 74x slower writes, 200x+ slower uncached reads. Use ExFAT.** |
| Missing `.obsidian/` plugins | Include in rsync; verify plugin cwd paths post-migration |
| Hardcoded paths in scripts | Search ALL file types: `.md`, `.json`, `.py`, `.sh`, `.csv`, `.html` |
| Symlink not followed | Use `ln -sfn` (force, no-dereference); test with `realpath` |
| Cache files with old paths | Exclude `graphify-out/`, `venv/`, `__pycache__/` from path updates — regenerate |
| Obsidian locked during move | Close Obsidian completely before rsync |
| Permission errors | Run rsync as same user; check `ls -la` on target |
| Heavy folders causing index hangs | **Move Transcripts/, node_modules/, Hermes Agent/, .vault-organizer-backups/ OUT before rsync; restore after** |
| Cron jobs running during migration | Pause all vault-related cron jobs (`cronjob action=resume` after) |

## Verification Checklist

- [ ] Vault opens in Obsidian from new location
- [ ] Search works (index rebuilt)
- [ ] Graph view renders
- [ ] All plugins load (especially those with cwd settings)
- [ ] Runtime scripts execute without path errors
- [ ] Symlink resolves correctly
- [ ] Rsync diff shows only expected differences (.DS_Store, caches, sync-conflicts)
- [ ] External tools (Hermes, Claude Code, etc.) resolve vault path