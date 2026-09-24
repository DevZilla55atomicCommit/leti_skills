---
name: obsidian-vault-relocation
description: "Relocate Obsidian vault to external: APFS, rsync, Syncthing."
trigger: "Relocate Obsidian vault to external: APFS, rsync, Syncthing."
---

# Obsidian Vault Relocation to External Storage

Complete workflow for moving an Obsidian vault to an external drive while maintaining all tooling integrations (Hermes Agent, custom scripts, Syncthing, symlinks).

## Prerequisites
- External drive connected and visible in `/Volumes/`
- Vault location known (e.g., `/Users/<user>/<Vault Name>`)
- Backup of critical data before starting

## Phase 1: Prepare External Drive

```bash
# Check current format
diskutil info /Volumes/<DRIVE_NAME> | grep -E "File System|Format"

# Choose filesystem based on drive interface:
# - Internal NVMe/SSD (fast): APFS — symlinks, xattrs, journaling, snapshots
# - External USB 2.0/3.0 (slow): ExFAT — NO journaling, NO copy-on-write, 74x faster writes, 200x+ faster uncached reads
# - Cross-platform (Windows/macOS/Linux): ExFAT

# For USB 2.0 drives, REFORMAT TO EXFAT:
diskutil eraseDisk ExFAT "<DRIVE_NAME>" /dev/disk<X>

# For internal/fast drives, use APFS:
diskutil eraseDisk APFS "<DRIVE_NAME>" /dev/disk<X>

# Verify
diskutil info /Volumes/<DRIVE_NAME> | grep -E "File System|Format|Size|Free"
```

**Filesystem Choice Critical on Slow Interfaces (USB 2.0):**
- **APFS on USB 2.0:** Catastrophically slow — journaling + copy-on-write + checksums saturate bus. Uncached reads < 1 MB/s, writes ~0.87 MB/s.
- **ExFAT on USB 2.0:** Simple allocation table, no journaling, no copy-on-write. Uncached reads ~191 MB/s, writes ~64 MB/s.
- **Test your drive:** `dd if=/dev/zero of=/Volumes/DRIVE/test bs=1m count=100` — expect >50 MB/s write on ExFAT/USB 2.0.

**Why APFS fails on USB 2.0:** Every file op triggers journal writes, COW metadata updates, checksum calculations — metadata churn saturates 35 MB/s bus before data moves.

## Phase 2: Transfer Vault

```bash
# Dry run first
rsync -avh --dry-run \
  --exclude='node_modules/' \
  --exclude='*/.DS_Store' \
  --exclude='*/.syncthing.*.tmp' \
  --exclude='*.sync-conflict-*.md' \
  "/Users/<user>/<Vault Name>/" \
  "/Volumes/<DRIVE_NAME>/<Vault Name>/"

# Actual transfer
rsync -avh --progress \
  --exclude='node_modules/' \
  --exclude='*/.DS_Store' \
  --exclude='*/.syncthing.*.tmp' \
  --exclude='*.sync-conflict-*.md' \
  "/Users/<user>/<Vault Name>/" \
  "/Volumes/<DRIVE_NAME>/<Vault Name>/"

# Verify
du -sh "/Users/<user>/<Vault Name>" "/Volumes/<DRIVE_NAME>/<Vault Name>"
find "/Users/<user>/<Vault Name>" -type f | wc -l
find "/Volumes/<DRIVE_NAME>/<Vault Name>" -type f | wc -l
```

## Phase 3: Create Backward-Compatibility Symlink

```bash
ln -sfn "/Volumes/<DRIVE_NAME>/<Vault Name>" ~/<Vault_Name_Symlink>
# Example: ln -sfn "/Volumes/PNY128GBLED/TamaZila Obsidian Vault" ~/TamaZila_Obsidian_Vault
```

Ensures any hardcoded paths in scripts, configs, or muscle memory continue working.

## Phase 4: Update Absolute Paths in Vault

Search for old paths and batch-update:

```bash
# Find all files with old path
grep -r "/Users/<user>/<Vault Name>" "/Volumes/<DRIVE_NAME>/<Vault Name>" \
  --include="*.md" --include="*.json" --include="*.csv" --include="*.py" --include="*.sh" \
  --exclude-dir="graphify-out" --exclude-dir="<Vault Name>/Hermes Image Generates" -l

# Update each category:
# 1. Obsidian plugin configs (.obsidian/plugins/*/data.json)
# 2. Shell scripts (*.sh)
# 3. Python scripts (*.py) - VAULT_BASE, OBSIDIAN_VAULT constants
# 3. Core knowledge files (MASTER_INDEX.md, CROSS_REFERENCE_INDEX.md, etc.)
# 4. Pipeline configs (PIPELINE_PLAN.md, VIDEO_EFFECTS_PIPELINE_PLAN.md)
# 5. Navigation files (Hero_index.md, The_Osidian_Vault_Keeper_Tasks.md)
# 6. Security/Claude/Graphify config files
```

**Pattern:** Use `patch` or `sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' <file>` for each file.

**Exclude generated cache dirs:** `graphify-out/`, `Hermes Image Generates/` — these regenerate on next use.

## Phase 5: Update Syncthing Config

```bash
# Stop Syncthing
pkill -f syncthing

# Backup and update
CONFIG="$HOME/Library/Application Support/Syncthing/config.xml"
cp "$CONFIG" "$CONFIG.bak.$(date +%s)"
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' "$CONFIG"

# Verify
grep "path=" "$CONFIG" | grep -i "<Vault Name>"

# Restart
open -a Syncthing
```

Only update the vault folder entry — leave `hermes-memories`, `hermes-profiles` pointing to `~/.hermes/`.

## Phase 6: Verify All Tooling

```bash
# 1. Obsidian plugin configs
python3 -c "
import json
with open('<vault>/.obsidian/plugins/lean-terminal/data.json') as f:
    data = json.load(f)
for s in data.get('recentSessions', []):
    assert s['cwd'] == '/Volumes/<DRIVE_NAME>/<Vault Name>'
print('lean-terminal paths correct')
"

# 2. Custom scripts (session hooks, sync scripts, pipeline)
bash -c 'source "<vault>/Hermes Agent/session_start_step_beyond.sh"'
bash -c 'source "<vault>/Hermes Agent/session_end_step_beyond.sh"'
python3 "<vault>/Hermes Agent/sync_step_beyond_memory.py" --status
python3 "<vault>/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/scripts/process_batch.py" --help

# 3. Symlink
ls -la ~/<Vault_Name_Symlink>
```

## Phase 7: Cleanup (After Verification)

```bash
# Only after full verification
rm -rf "/Users/<user>/<Vault Name>"
```

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| FAT32/exFAT formatting | Always use APFS for macOS-only vaults |
| Missing symlink | Create symlink before updating paths |
| Forgot Syncthing | Update Syncthing config BEFORE restarting it |
| Cache files polluting diff | Exclude `graphify-out/`, `Hermes Image Generates/`, `venv/`, `__pycache__/` |
| node_modules bloating transfer | Exclude `node_modules/` (regeneratable via `npm install`) |
| .DS_Store differences | Exclude `*/.DS_Store` in rsync and diff |
| Sync-conflict files | Clean `*.sync-conflict-*.md` before transfer |
| **USB 2.0 external drive too slow for plugin loading** | **Move heavy plugins to internal SSD, symlink back** |

## Phase 8: Performance Optimization for Slow External Drives (USB 2.0 / Network Shares)

If the external drive is USB 2.0 or a slow network share, Obsidian startup becomes painfully slow (20-30s+) because:
- Obsidian loads ALL enabled plugin `main.js` bundles on startup
- Plugin directories with thousands of files (e.g., `graphify-core` with full repo) cause massive random I/O
- USB 2.0 caps at ~35-40 MB/s sequential, far worse for random I/O

**Solution: Move heavy plugins to internal SSD, keep vault on external drive**

```bash
# 1. Create local plugin staging directory
mkdir -p "~/Library/Application Support/obsidian-plugins"

# 2. Identify heavy plugins (check .obsidian/plugins/* size)
du -sh "/Volumes/<DRIVE_NAME>/<Vault Name>/.obsidian/plugins"/*

# 3. Move heavy plugins to local SSD
mv "/Volumes/<DRIVE_NAME>/<Vault Name>/.obsidian/plugins/<heavy-plugin>" \
   "~/Library/Application Support/obsidian-plugins/"

# 4. Create symlink back to vault
ln -s "~/Library/Application Support/obsidian-plugins/<heavy-plugin>" \
      "/Volumes/<DRIVE_NAME>/<Vault Name>/.obsidian/plugins/<heavy-plugin>"

# 5. Verify Obsidian still sees the plugin
ls -la "/Volumes/<DRIVE_NAME>/<Vault Name>/.obsidian/plugins/<heavy-plugin>"
```

**Typical heavy plugins to move:**
| Plugin | Typical Size | Reason |
|--------|-------------|--------|
| `graphify-core` | 8-17 MB | Full dev repo with tests/, docs/, .git/ |
| `obsidian-excalidraw-plugin` | 8+ MB | Large main.js bundle |
| `copilot` | 5+ MB | Large main.js bundle |
| `vscode-editor` | 5+ MB | Large main.js bundle |
| Any plugin with `node_modules/` or full source tree | | Not a built plugin |

**Results:** 68% reduction in external drive plugin I/O (54 MB → 17 MB), plugin loading shifts to NVMe SSD (~3000 MB/s), startup drops from ~20-30s to ~5-10s.

**Caveat:** The moved plugin must be a valid built plugin (has `main.js`, `manifest.json`, `styles.css`). Dev repos like `graphify-core` may need `npm run build` first.

## Filesystem Benchmark Reference

**Critical for USB 2.0 drives:** See `references/filesystem-benchmark-usb2.md` for detailed benchmarks comparing APFS vs ExFAT on USB 2.0.

**Key finding:** APFS on USB 2.0 is **74x slower writes, 200x+ slower uncached reads** than ExFAT. Never use APFS on USB 2.0 for active Obsidian vaults.