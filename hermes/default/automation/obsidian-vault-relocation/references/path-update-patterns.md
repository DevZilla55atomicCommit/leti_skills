# Path Update Patterns for Obsidian Vault Migration

Quick reference for regex/sed patterns to update absolute paths when relocating an Obsidian vault.

## Basic Pattern

```bash
# General pattern (pipe delimiter for paths with slashes)
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' <file>

# With patch (preferred for structured files)
patch <file> << 'EOF'
--- a/<file>
+++ b/<file>
@@ context @@
-old/path/here
+new/path/here
EOF
```

## Per-File-Type Patterns

### JSON Files (Obsidian plugin configs, exports)
```bash
# data.json - cwd fields
sed -i '' 's|/Users/alfredkamisese/TamaZila Obsidian Vault|/Volumes/PNY128GBLED/TamaZila Obsidian Vault|g' .obsidian/plugins/lean-terminal/data.json

# Exports (knowledge_base_export.json, skills_export.json)
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' *.json
```

### CSV Files
```bash
# knowledge_base_export.csv - full_path column
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' *.csv
```

### Markdown Files
```bash
# All .md files - full paths in text, code blocks, links
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' *.md

# Specific patterns:
# - Vault location references: > **Vault Location:** `/Users/...`
# - Code blocks with paths
# - Relative links that became absolute
```

### Python Scripts
```bash
# Constants at top of file
sed -i '' 's|VAULT_BASE = Path("/Users/<user>/<Vault Name>")|VAULT_BASE = Path("/Volumes/<DRIVE_NAME>/<Vault Name>")|g' *.py
sed -i '' 's|OBSIDIAN_VAULT = Path("/Users/<user>/<Vault Name>")|OBSIDIAN_VAULT = Path("/Volumes/<DRIVE_NAME>/<Vault Name>")|g' *.py

# f-strings and string constants
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' *.py
```

### Shell Scripts
```bash
# Variables and hardcoded paths
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' *.sh

# PATTERNS_FILE, SCRIPT_DIR, etc.
```

### Syncthing Config (XML)
```bash
# Single sed for entire config
sed -i '' 's|/Users/<user>/<Vault Name>|/Volumes/<DRIVE_NAME>/<Vault Name>|g' "$HOME/Library/Application Support/Syncthing/config.xml"
```

## Exclude Patterns (for grep/rsync/diff)

```bash
# Exclude generated cache directories
--exclude-dir="graphify-out"
--exclude-dir="Hermes Image Generates"
--exclude-dir="venv"
--exclude-dir="__pycache__"
--exclude-dir="node_modules"
--exclude-dir=".git"

# Exclude specific file patterns
--exclude="*.sync-conflict-*.md"
--exclude="*.DS_Store"
--exclude="*/.DS_Store"
--exclude="*/.syncthing.*.tmp"

# Combined grep exclude
grep -r "oldpath" . \
  --include="*.md" --include="*.json" --include="*.csv" --include="*.py" --include="*.sh" \
  --exclude-dir="graphify-out" \
  --exclude-dir="Hermes Image Generates" \
  --exclude-dir="venv" \
  --exclude-dir="__pycache__" \
  --exclude-dir="node_modules" \
  --exclude-dir=".git" \
  -l
```

## Batch Update Script Template

```bash
#!/bin/bash
# batch-update-paths.sh
# Usage: ./batch-update-paths.sh "/Users/old/path" "/Volumes/new/path" "/path/to/vault"

OLD_PATH="$1"
NEW_PATH="$2"
VAULT_ROOT="$3"

if [[ -z "$OLD_PATH" || -z "$NEW_PATH" || -z "$VAULT_ROOT" ]]; then
    echo "Usage: $0 <old_path> <new_path> <vault_root>"
    exit 1
fi

cd "$VAULT_ROOT"

# Find all files with old path (excluding cache dirs)
FILES=$(grep -r "$OLD_PATH" . \
  --include="*.md" --include="*.json" --include="*.csv" --include="*.py" --include="*.sh" \
  --exclude-dir="graphify-out" \
  --exclude-dir="Hermes Image Generates" \
  --exclude-dir="venv" \
  --exclude-dir="__pycache__" \
  --exclude-dir="node_modules" \
  --exclude-dir=".git" \
  -l | sort -u)

echo "Found $(echo "$FILES" | wc -l) files to update"

for file in $FILES; do
    echo "Updating: $file"
    sed -i '' "s|$OLD_PATH|$NEW_PATH|g" "$file"
done

echo "Done. Verifying..."
grep -r "$OLD_PATH" . \
  --exclude-dir="graphify-out" \
  --exclude-dir="Hermes Image Generates" \
  --exclude-dir="venv" \
  --exclude-dir="__pycache__" \
  --exclude-dir="node_modules" \
  --exclude-dir=".git" \
  -l || echo "No remaining occurrences found."
```

## Verification Commands

```bash
# Quick verification after updates
grep -r "/Users/<user>/<Vault Name>" "<vault_root>" \
  --exclude-dir="graphify-out" \
  --exclude-dir="Hermes Image Generates" \
  --exclude-dir="venv" \
  --exclude-dir="__pycache__" \
  --exclude-dir="node_modules" \
  --exclude-dir=".git" \
  -l

# Should return empty (only cache dirs may have old paths)
```