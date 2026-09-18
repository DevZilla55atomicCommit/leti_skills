# Vault Organizer Cron Job Validation Notes

## Job: Vault Organizer — Dry Run
- **Job ID**: `696058de26a8`
- **Schedule**: `0 3,11,23 * * *` (daily at 03:00, 11:00, 23:00)
- **Script**: `~/vault_organizer.py` (runs from vault root)
- **Skills**: `graphify`, `vault-setup`
- **Deliver**: `origin`

## Key Validation Points

### 1. Script Path
```bash
ls -la ~/vault_organizer.py
# Must exist and be executable
```

### 2. Working Directory
The job runs from the vault root:
```bash
cd /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault
python3 ~/vault_organizer.py
```

### 3. Graphify Binary Dependency
**CRITICAL**: The script's `run_validation()` function calls graphify CLI. As of 2026-08-10, the binary is at:
```
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/graphify
```
NOT at the hardcoded path `/Users/alfredkamisese/.local/share/uv/tools/graphifyy/bin/graphify`.

If graphify is moved/reinstalled, the script will fail validation silently (returns error but doesn't crash).

### 4. Skill Not Found Warning
The job config lists skills `graphify` and `vault-setup`. As of 2026-09-01, the cron agent logs:
```
⚠️ Skill(s) not found and skipped: graphify
```
But the script still runs successfully because it uses the `graphify` CLI binary directly, not the skill. The `vault-setup` skill content is embedded in the prompt and works.

**Fix options**:
- Install graphify skill in the cron profile: `hermes skills install official/graphify` (if available)
- Or remove `graphify` from job's `skills` list since it's not needed (script uses CLI)

### 5. Expected Output Shape
On success, the script logs:
```
[INFO] Validation: {'broken_wikilinks': N, 'orphan_files': M, 'missing_indexes': 0, 'link_chain_ok': True, 'errors': []}
```
- `broken_wikilinks` should be ~0 (analysis/... patterns are skipped)
- `orphan_files` should be ~0 (restricted to technique folders)
- `missing_indexes`: 0
- `link_chain_ok`: True
- `errors`: []

### 6. Manifest Generation
Each run creates a manifest:
```
.vault-organizer-manifests/manifest_org_YYYYMMDD_HHMMSS.json
```
These track file hashes for delta scanning.

### 7. State File
The script writes `.vault-organizer-state.json` with the run report (JSONL format, one line per run).

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `graphify query failed: No such file or directory` | Graphify binary path wrong | Update `vault_organizer.py` lines ~565 and ~578 |
| High broken_wikilinks (11K+) | analysis/... patterns not skipped | Add skip logic in `run_validation()` |
| High orphan_files (18K+) | Counting all vault files | Restrict to technique folders |
| "Missing link chain file" | Memory.md doesn't exist | Create `DaVinci_Knowledge_Base/Memory.md` |
| `⚠️ Skill(s) not found and skipped: graphify` | graphify skill not installed in profile | Remove from skills list or install skill |

## Manual Validation
```bash
cd /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault
python3 ~/vault_organizer.py
# Check last 30 lines for validation summary
```

## Cron Job Test via Hermes
```bash
cronjob run 696058de26a8
# Then check ~/.hermes/cron/output/696058de26a8/<latest>.md
```