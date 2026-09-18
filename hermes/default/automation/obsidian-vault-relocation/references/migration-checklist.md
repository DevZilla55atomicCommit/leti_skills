# Obsidian Vault Migration Checklist

Use this checklist for each vault relocation. Check off each item as completed.

## Phase 1: Prepare External Drive
- [ ] External drive connected and visible in `/Volumes/`
- [ ] Current format checked: `diskutil info /Volumes/<DRIVE_NAME>`
- [ ] Drive reformatted to APFS: `diskutil eraseDisk APFS "<DRIVE_NAME>" /dev/disk<X>`
- [ ] APFS verified: `diskutil info /Volumes/<DRIVE_NAME> | grep -E "File System|Size|Free"`

## Phase 2: Transfer Vault
- [ ] Dry run completed without errors
- [ ] Actual rsync transfer completed (exit code 0)
- [ ] Size verified: `du -sh` matches between source and destination
- [ ] File count verified: `find ... -type f | wc -l` matches (or +1 for symlink)
- [ ] Exclusions working: no node_modules, .DS_Store, .syncthing, sync-conflict files

## Phase 3: Create Symlink
- [ ] Symlink created: `ln -sfn "/Volumes/<DRIVE_NAME>/<Vault Name>" ~/<Vault_Name_Symlink>`
- [ ] Symlink verified: `ls -la ~/<Vault_Name_Symlink>` points to external location

## Phase 4: Update Absolute Paths
- [ ] Search completed: `grep -r` found all files with old path
- [ ] Obsidian plugin configs updated (.obsidian/plugins/*/data.json)
- [ ] Shell scripts updated (*.sh)
- [ ] Python scripts updated (*.py)
- [ ] Core knowledge files updated (MASTER_INDEX.md, CROSS_REFERENCE_INDEX.md, Hero_index.md, etc.)
- [ ] Pipeline configs updated (PIPELINE_PLAN.md, VIDEO_EFFECTS_PIPELINE_PLAN.md)
- [ ] Navigation files updated (Hero_index.md, Vault_Keeper_Tasks.md)
- [ ] Security/Graphify/Claude configs updated
- [ ] Verified: `grep -r "/Users/<user>/<Vault Name>"` returns only cache dirs

## Phase 5: Update Syncthing
- [ ] Syncthing stopped: `pkill -f syncthing`
- [ ] Config backed up: `cp config.xml config.xml.bak.<timestamp>`
- [ ] Config updated: `sed` replaced old path with new path
- [ ] Verified: `grep "path=" config.xml` shows new path
- [ ] Syncthing restarted: `open -a Syncthing`
- [ ] Syncthing UI shows correct path and syncing

## Phase 6: Verify All Tooling
- [ ] Obsidian lean-terminal plugin: all cwd paths correct
- [ ] Session start script works: `source session_start_step_beyond.sh`
- [ ] Session end script works: `source session_end_step_beyond.sh`
- [ ] Sync script status works: `python3 sync_step_beyond_memory.py --status`
- [ ] Pipeline script loads: `python3 process_batch.py --help`
- [ ] Symlink works: `ls -la ~/<Vault_Name_Symlink>`

## Phase 7: Cleanup (After Verification)
- [ ] Old vault removed: `rm -rf "/Users/<user>/<Vault Name>"`
- [ ] Internal drive space freed: `df -h /`

## Common Pitfalls Check
- [ ] Drive is APFS (not FAT32/exFAT)
- [ ] Symlink created before path updates
- [ ] Syncthing config updated before restart
- [ ] Cache dirs excluded from diff/search (graphify-out/, Hermes Image Generates/, venv/, __pycache__/)
- [ ] node_modules excluded from transfer
- [ ] .DS_Store excluded from rsync and diff
- [ ] Sync-conflict files cleaned before transfer