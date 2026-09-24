---
name: vault_backup_management
type: skill
description: Manage vault backups, prune obsolete full copies safely.
status: active
tags: [backup, vault, maintenance, cleanup]
---

## Trigger
Use when:
- You discover large duplicate vault copies (e.g., `.vault-organizer-backups/`) that are safe to delete.
- A cron job promises backups but implementation does not.
- User asks about freeing space taken by old backup directories.
- Verify a backup folder's safety before deletion.

## Core Procedure
1. **Identify type** — Confirm full copy (size >10 GB, full `index.md`, etc.).  
2. **Check usage** — Ensure no active process reads the folder (`lsof +D`).  
3. **Validate redundancy** — Compare to primary vault; >95 % overlap means delete.  
4. **Delete** — `rm -rf <folder>` after confirmation.  
5. **Document** — Note in cron SKILL.md that backups are not created by current `vault_organizer.py`.

## Pitfalls & Fixes
- **Deleting in use** → Stop cron job first.  
- **Assuming any large folder is a backup** → Look for `org_YYYYMMDD_HHMMSS_...` naming and `.vault-organizer-state.json`.  
- **Keeping indefinitely** → Retain only latest 1‑2 backups; purge older ones.

## References
- `references/backup_retention.md` — Details on Aug 5, 2026 set (4 folders, 105 GB) and deletion steps.
- `references/pin_marking.md` — Session pinning & safety protocol

## Example
```bash
lsof +D "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-backups"
rm -rf "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-backups"
df -h "/Volumes/PNY128GBLED/TamaZila Obsidian Vault"
```