#!/bin/bash
# Obsidian Vault Migration - Rsync Template
# Usage: ./rsync-migrate.sh /path/to/source/vault /Volumes/TARGET_DRIVE/vault_name

set -euo pipefail

SOURCE="${1:-}"
DEST="${2:-}"

if [[ -z "$SOURCE" || -z "$DEST" ]]; then
    echo "Usage: $0 <source_vault_path> <dest_vault_path>"
    echo "Example: $0 /Users/alfredkamisese/TamaZila\\ Obsidian\\ Vault /Volumes/PNY128GBLED/TamaZila\\ Obsidian\\ Vault"
    exit 1
fi

# Exclusions: caches, temp files, conflicts, metadata
EXCLUDES=(
    --exclude='.DS_Store'
    --exclude='*/.DS_Store'
    --exclude='*/.syncthing.*.tmp'
    --exclude='*.sync-conflict-*.md'
    --exclude='graphify-out/'
    --exclude='*/graphify-out/'
    --exclude='*/venv/'
    --exclude='*/__pycache__/'
)

echo "=== Dry Run ==="
rsync -avh --dry-run --progress "${EXCLUDES[@]}" "$SOURCE/" "$DEST/"

echo ""
read -p "Proceed with actual transfer? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo "=== Actual Transfer ==="
rsync -avh --progress "${EXCLUDES[@]}" "$SOURCE/" "$DEST/"

echo ""
echo "=== Verification ==="
echo "Source size:  $(du -sh "$SOURCE" | cut -f1)"
echo "Dest size:    $(du -sh "$DEST" | cut -f1)"
echo "Source files: $(find "$SOURCE" -type f | wc -l)"
echo "Dest files:   $(find "$DEST" -type f | wc -l)"

echo ""
echo "Creating backward-compatibility symlink..."
SYMLINK_NAME="TamaZila_Obsidian_Vault"
ln -sfn "$DEST" ~/"$SYMLINK_NAME"
echo "Created ~/TamaZila_Obsidian_Vault -> $DEST"

echo ""
echo "Migration complete. Next steps:"
echo "1. Update absolute paths in vault files (see skill references/path-update-patterns.md)"
echo "2. Run verification script: python3 scripts/verify-migration.py \"$SOURCE\" \"$DEST\""
echo "3. Test Obsidian opens from new location"
echo "4. Remove old vault after verification: rm -rf \"$SOURCE\""