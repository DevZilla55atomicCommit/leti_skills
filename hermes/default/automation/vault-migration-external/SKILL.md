---
name: vault-migration-external
description: Migrate Obsidian vault to external APFS drive, remap paths.
trigger: User needs to move a vault/knowledge base to external storage while preserving all internal links, configs, and tooling paths.
---

# Vault Migration to External Drive

Complete workflow for migrating an Obsidian vault (or similar large knowledge base) to an external APFS-formatted drive with full path remapping, symlink creation, and verification.

## When to Use

- Moving a large vault (>5 GB) from internal NVMe to external USB-C/Thunderbolt storage
- Need to preserve all internal links, Obsidian plugin configs, and tooling paths
- Vault contains absolute paths in configs, scripts, markdown files, and export files
- Must maintain backward compatibility via symlink

## Prerequisites

- External drive with sufficient capacity (vault size + 20% headroom)
- macOS with `diskutil`, `rsync`, `sed`, `grep` available
- Vault closure (no active editors/plugins writing during migration)

## Procedure

### 1. Prepare Target Drive

```bash
# Identify target disk (e.g., /dev/disk4)
diskutil list

# Reformat to APFS (required for symlinks, xattrs, large files, journaling)
diskutil eraseDisk APFS "VOLUME_NAME" /dev/diskX

# Verify format
diskutil info /Volumes/VOLUME_NAME/ | grep -E "File System|Format|Type"
```

**Critical**: Do NOT use FAT32/exFAT — they lack journaling, symlinks, xattrs, and have 4 GB file limit.

### 2. Full Vault Transfer (rsync)

```bash
# Dry run first
rsync -avh --dry-run \
  --exclude='.DS_Store' \
  --exclude='*/.DS_Store' \
  "/path/to/source/vault/" \
  "/Volumes/VOLUME_NAME/vault/"

# Actual transfer (preserves perms, times, symlinks, xattrs, ACLs)
rsync -avh --progress \
  --exclude='.DS_Store' \
  --exclude='*/.DS_Store' \
  "/path/to/source/vault/" \
  "/Volumes/VOLUME_NAME/vault/"

# Verify byte-for-byte match
du -sh "/path/to/source/vault" "/Volumes/VOLUME_NAME/vault"
find "/path/to/source/vault" -type f | wc -l
find "/Volumes/VOLUME_NAME/vault" -type f | wc -l
```

### 3. Create Backward-Compatibility Symlink

```bash
ln -sfn "/Volumes/VOLUME_NAME/vault" ~/vault_symlink_name
```

Use a stable name (no spaces) for scripts that hardcode `~/vault_name`.

### 4. Bulk Path Remapping

**Find all files with old absolute paths:**

```bash
OLD="/Users/username/old/vault/path"
NEW="/Volumes/VOLUME_NAME/vault"

grep -r "$OLD" "/Volumes/VOLUME_NAME/vault" \
  --include="*.md" --include="*.json" --include="*.csv" \
  --include="*.py" --include="*.sh" --include="*.yaml" \
  -l | sort -u
```

**Batch replace (safe, idempotent):**

```bash
# For each file type, use sed with in-place edit
find "/Volumes/VOLUME_NAME/vault" -type f \
  \( -name "*.md" -o -name "*.json" -o -name "*.csv" -o -name "*.py" -o -name "*.sh" \) \
  -exec sed -i '' "s|$OLD|$NEW|g" {} +

# Verify no old paths remain
grep -r "$OLD" "/Volumes/VOLUME_NAME/vault" --include="*.md" --include="*.json" -l
```

**Key file categories to check:**

| Category | Examples |
|----------|----------|
| Obsidian plugin configs | `.obsidian/plugins/*/data.json` (cwd paths) |
| Navigation indexes | `Hero_index.md`, `MASTER_INDEX.md`, `MASTER_SUMMARY.md` |
| Pipeline configs | `PIPELINE_PLAN.md`, `VIDEO_EFFECTS_QUEUE.md` |
| Export files | `knowledge_base_export.csv/json`, `skills_export.json` |
| Tooling scripts | `session_start/end_*.sh`, `sync_*.py`, `process_batch.py` |
| Memory files | `step-beyond-user-patterns.md` (memory_path) |
| Security/CI docs | `Security Audit Master Index.md`, `README-GRAPHIFY.md` |

### 5. Clean Up Stale Files

```bash
# Remove sync-conflict files (Syncthing/other sync tools)
find "/Volumes/VOLUME_NAME/vault" -name "*.sync-conflict-*" -delete

# Remove .DS_Store files (optional, regenerated on open)
find "/Volumes/VOLUME_NAME/vault" -name ".DS_Store" -delete
```

### 6. Update Agent Memory Systems

**Hermes persistent memory (memory tool):**

```bash
# Add entry noting new vault location
memory add --target memory "Vault location: /Volumes/VOLUME_NAME/vault (symlinked at ~/vault_symlink_name)"
```

**User profile memory (user tool):**

```bash
# Update Knowledge Management section in user profile
memory replace --target user \
  "Knowledge Management (RAG): Python text-extraction scripts populate a local Obsidian Vault database." \
  "Knowledge Management (RAG): Python text-extraction scripts populate a local Obsidian Vault database at /Volumes/VOLUME_NAME/vault (symlinked at ~/vault_symlink_name)."
```

### 7. Verification Checklist

Run each test and confirm ✅:

| Test | Command | Expected |
|------|---------|----------|
| Obsidian opens vault | Open `/Volumes/VOLUME_NAME/vault` in Obsidian | Search, graph, plugins work |
| Lean-terminal cwd | Check `.obsidian/plugins/lean-terminal/data.json` | All `cwd` = new path |
| Step Beyond sync | `source ~/vault_symlink_name/Hermes\ Agent/session_start_step_beyond.sh` | Patterns load from new location |
| Pipeline script | `python3 ~/vault_symlink_name/Hermes\ Agent/DaVinci_Knowledge_Base/Video_Effects/scripts/process_batch.py --help` | Loads with new `VAULT_BASE` |
| Symlink resolves | `ls -la ~/vault_symlink_name` | Points to `/Volumes/VOLUME_NAME/vault` |
| No old paths | `grep -r "$OLD" "/Volumes/VOLUME_NAME/vault" --include="*.md" -l` | Empty output |

### 8. Remove Old Vault (After Verification)

```bash
# Only after ALL tests pass and you've used new location for 1+ sessions
rm -rf "/path/to/source/vault"
```

## Pitfalls & Gotchas

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| FAT32/exFAT target | Files >4 GB fail, symlinks break, corruption on eject | **Always reformat to APFS first** |
| Missing `--exclude='*/.DS_Store'` | Thousands of `.DS_Store` files copied, diff noise | Always exclude in rsync |
| Symlink with spaces | Scripts break on `~/TamaZila Obsidian Vault` | Use `~/TamaZila_Obsidian_Vault` (underscores) |
| Partial path replacement | Some files still reference old path | Use `grep -r` verification after sed |
| Forgot user profile memory | Agent still thinks vault at old path | Update both `memory` and `user` targets |
| Active vault during rsync | Corrupted indexes, partial files | Close Obsidian, stop all sync tools first |
| Sync-conflict files remain | Duplicate patterns in Step Beyond | Delete `*.sync-conflict-*` before verification |

## Time Estimates

| Step | Typical Time (29 GB vault, USB 3.0) |
|------|-------------------------------------|
| Drive reformat | < 1 min |
| Rsync transfer | 10–30 min |
| Symlink creation | < 1 sec |
| Path grep/scan | 30–60 sec |
| Bulk sed replace | 10–30 sec |
| Verification tests | 2–5 min |
| **Total** | **~15–40 min** |

## Related Skills

- `external-cache-migration` — for migrating cache folders (similar but smaller scope)
- `macos-storage-cleanup` — for pre-migration space analysis
- `hermes-agent` — for Hermes Agent configuration after migration