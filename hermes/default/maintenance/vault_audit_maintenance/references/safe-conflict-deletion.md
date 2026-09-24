# Safe Conflict File Deletion Workflow

## Purpose
Ensure that conflict files can be deleted without breaking the vault structure.

## Prerequisites
- `conflict-files-list.txt` listing files to evaluate.
- Access to canonical file existence check.

## Steps
1. **Identify Conflict Files**  
   - Common sources: Syncthing conflict files, temporary backup files, duplicate reels.  
   - Example pattern: `*_conflict_*` or files with a trailing `~` or `1`.

2. **Check Canonical Version Existence**  
   - For each conflict file, verify if a non-conflict (canonical) version exists.  
   - Use a command like `ls` or a script to check.

3. **Verify Correct Version**  
   - Ensure the canonical version is the intended, up‑to‑date file.  
   - Open it to confirm content matches expectations.

4. **Delete Conflict File**  
   - If a canonical version exists, delete the conflict file safely:  
     ```bash
     rm "/path/to/conflict/file"
     ```
   - If no canonical version exists and the conflict file is truly redundant, proceed with deletion.

5. **Re-run Audit**  
   - After deletion, re-run the vault audit (e.g., `cronjob run vault_audit_daily`) to confirm no conflict files remain.

6. **Commit Changes**  
   - If version control is enabled, commit the deletion to keep history.

## Verification
- Run `ls "/path/to/vault"` to ensure the conflict file is no longer present.  
- Re-generate the conflict‑files list and verify it is empty.  
- Confirm the vault audit report shows no duplicate or conflict entries.

## Pitfalls
- **Accidental Deletion**: Never delete a file that is the only version of a note or asset.  
- **Path Mistakes**: Double‑check paths before using `rm`.  
- **Backup First**: Keep a backup of the vault before bulk deletions.  
- **Version Control**: If using Git, ensure the deletion is committed to avoid orphaned files.

## Example
```bash
# List conflict files
find "/Users/alfredkamisese/TamaZila Obsidian Vault" -name "*_conflict_*" -type f

# For each conflict file, check canonical version
for conflict in *_conflict_*; do
  canonical="${conflict%_conflict_*}"
  if [ -e "$canonical" ]; then
    echo "Canonical exists for $conflict"
    rm "$conflict"
  else
    echo "No canonical version for $conflict; proceeding with deletion"
    rm "$conflict"
  fi
done

# Re-run audit
cronjob run vault_audit_daily