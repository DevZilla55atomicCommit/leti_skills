## Backup Retention — Aug 5, 2026 Findings

## Discovered Backup Set

| Folder | Size | Creation Time |
|--------|------|---------------|
| `org_20260805_185911_20260805_185911` | 23 GB | Aug 5 2026 18:59 |
| `org_20260805_190225_20260805_190225` | 28 GB | Aug 5 2026 19:02 |
| `org_20260805_191557_20260805_191557` | 28 GB | Aug 5 2026 19:15 |
| `org_20260805_192109_20260805_192109` | 25 GB | Aug 5 2026 19:21 |

- **Total size:** ~105 GB
- **Nature:** Full copies of the entire vault, including 14 GB of GIFs and 9.9 GB of Video_Effects.
- **Location:** `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-backups/`

## Safe Deletion Process

1. **Confirm no active usage**  
   ```bash
   lsof +D "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-backups"
   ```
   - No output → safe to delete  
   - If processes appear, stop the corresponding cron job or wait for completion.

2. **Delete the directory**  
   ```bash
   rm -rf "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-backups"

3. **Verify reclaimed space**  
   ```bash
   df -h "/Volumes/PNY128GBLED/TamaZila Obsidian Vault"
   ```
   - Expect ~105 GB reclaimed.

## Retention Recommendation

- Keep only the most recent backup (if any) for emergency restores
- Delete older copies to free space, especially when the active vault size is far smaller than the combined backup size