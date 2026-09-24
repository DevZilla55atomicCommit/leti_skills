# Path Update Patterns for Obsidian Vault Migration

## Common Path Formats Encountered

### Absolute Path with Home Directory
```
/Users/alfredkamisese/TamaZila Obsidian Vault
```
**Replacement:**
```
/Volumes/PNY128GBLED/TamaZila Obsidian Vault
```

### In Markdown Links
```markdown
[Link](/Users/alfredkamisese/TamaZila Obsidian Vault/Path/File.md)
```
**Replacement:**
```markdown
[Link](/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Path/File.md)
```

### In JSON Config (escaped)
```json
"cwd": "/Users/alfredkamisese/TamaZila Obsidian Vault"
```
**Replacement:**
```json
"cwd": "/Volumes/PNY128GBLED/TamaZila Obsidian Vault"
```

### In Python Path Objects
```python
Path("/Users/alfredkamisese/TamaZila Obsidian Vault/...")
```
**Replacement:**
```python
Path("/Volumes/PNY128GBLED/TamaZila Obsidian Vault/...")
```

### In Shell Scripts
```bash
PATTERNS_FILE="/Users/alfredkamisese/TamaZila Obsidian Vault/..."
```
**Replacement:**
```bash
PATTERNS_FILE="/Volumes/PNY128GBLED/TamaZila Obsidian Vault/..."
```

### In Bash Variables (quoted)
```bash
VAULT_BASE="/Users/alfredkamisese/TamaZila Obsidian Vault/..."
```
**Replacement:**
```bash
VAULT_BASE="/Volumes/PNY128GBLED/TamaZila Obsidian Vault/..."
```

### In CSV Exports (full path column)
```csv
full_path
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/...
```
**Replacement:**
```csv
full_path
/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/...
```

### In Command-Line Examples
```bash
--vault-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/..."
```
**Replacement:**
```bash
--vault-dir "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/..."
```

## Safe Replacement Patterns

### Single File (precise)
```bash
sed -i '' 's|/Users/alfredkamisese/TamaZila Obsidian Vault|/Volumes/PNY128GBLED/TamaZila Obsidian Vault|g' file.md
```

### Multiple Files (with verification)
```bash
# First, list affected files
grep -r "/Users/alfredkamisese/TamaZila Obsidian Vault" --include="*.md" -l

# Then replace
grep -r "/Users/alfredkamisese/TamaZila Obsidian Vault" --include="*.md" -l | \
  xargs sed -i '' 's|/Users/alfredkamisese/TamaZila Obsidian Vault|/Volumes/PNY128GBLED/TamaZila Obsidian Vault|g'
```

### With Different Delimiters (for paths with slashes)
```bash
sed -i '' 's|/old/path|/new/path|g' file.md
sed -i '' 's@/old/path@/new/path@g' file.md
```

## Files to EXCLUDE from Path Updates

| Directory | Reason |
|-----------|--------|
| `graphify-out/` | Cache files regenerated on next analysis |
| `*/venv/` | Python virtual environment — reinstall |
| `*/__pycache__/` | Bytecode cache — regenerated |
| `*/.syncthing.*.tmp` | Syncthing temp files |
| `*.sync-conflict-*.md` | Conflict files — delete instead |
| `*/.DS_Store` | macOS metadata — regenerates |

## Verification Commands

```bash
# Check no old paths remain (excluding caches)
grep -r "/Users/alfredkamisese/TamaZila Obsidian Vault" "/Volumes/VOLUME_NAME/vault" \
  --include="*.md" --include="*.json" --include="*.csv" --include="*.py" --include="*.sh" \
  --exclude-dir="graphify-out" --exclude-dir="*venv*" --exclude-dir="*__pycache__*" -l

# Should return empty (exit code 1)
```