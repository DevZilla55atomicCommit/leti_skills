#!/bin/bash
# obsidian-vault-migrate.sh
# Complete Obsidian vault migration to ExFAT on USB 2.0
# Usage: ./obsidian-vault-migrate.sh <source_vault> <target_drive>

set -euo pipefail

SOURCE="${1:-/Volumes/PNY128GBLED/TamaZila Obsidian Vault}"
TARGET_DRIVE="${2:-/Volumes/Samsung LED}"
VAULT_NAME="$(basename "$SOURCE")"
TARGET="${TARGET_DRIVE}/${VAULT_NAME}"

echo "=== Obsidian Vault Migration to ExFAT ==="
echo "Source: $SOURCE"
echo "Target: $TARGET"
echo ""

# 1. Verify source exists
if [[ ! -d "$SOURCE" ]]; then
    echo "ERROR: Source vault not found: $SOURCE"
    exit 1
fi

# 2. Verify target drive exists
if [[ ! -d "$TARGET_DRIVE" ]]; then
    echo "ERROR: Target drive not mounted: $TARGET_DRIVE"
    exit 1
fi

# 3. Check target is ExFAT
FS=$(diskutil info "$TARGET_DRIVE" | grep "File System Personality" | awk -F: '{print $2}' | xargs)
if [[ "$FS" != "ExFAT" ]]; then
    echo "WARNING: Target drive is $FS, not ExFAT. Performance will suffer on USB 2.0."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 4. Move heavy folders OUT before migration
echo "=== Moving heavy folders out of vault ==="
HEAVY_FOLDERS=(
    "Hermes Agent"
    "Transcripts"
    "emai-dashboard/node_modules"
    "graphify-out"
    ".vault-organizer-backups"
    ".vault-organizer-manifests"
    ".agents"
    ".claude"
)

ARCHIVE_ROOT="$TARGET_DRIVE"
for folder in "${HEAVY_FOLDERS[@]}"; do
    SRC="$SOURCE/$folder"
    if [[ -e "$SRC" ]]; then
        DEST="$ARCHIVE_ROOT/$(basename "$folder")_archived"
        echo "Moving $folder -> $DEST"
        mv "$SRC" "$DEST"
    fi
done

# 5. Rsync with exclusions
echo "=== Rsync to target (ExFAT) ==="
rsync -avh --progress \
    --exclude='.DS_Store' --exclude='*/.DS_Store' \
    --exclude='*/.syncthing.*.tmp' --exclude='*.sync-conflict-*.md' \
    --exclude='*/.vault-organizer-backups/' --exclude='*/.vault-organizer-manifests/' \
    --exclude='*/.agents/' --exclude='*/.claude/' \
    --exclude='*/node_modules/' --exclude='*/Transcripts/' \
    --exclude='*/Hermes Agent/' \
    "$SOURCE/" "$TARGET/"

# 6. Verify
echo "=== Verification ==="
echo "Source size: $(du -sh "$SOURCE" | cut -f1)"
echo "Target size: $(du -sh "$TARGET" | cut -f1)"
echo "Source files: $(find "$SOURCE" -type f | wc -l)"
echo "Target files: $(find "$TARGET" -type f | wc -l)"

# 7. Diff check
echo "=== Diff check (should only show .DS_Store, caches, sync-conflicts) ==="
rsync -avh --dry-run --delete \
    --exclude='.DS_Store' --exclude='*/.DS_Store' \
    --exclude='*/.syncthing.*.tmp' --exclude='*.sync-conflict-*.md' \
    "$SOURCE/" "$TARGET/" | head -30

echo ""
echo "=== Migration complete ==="
echo "Vault copied to: $TARGET"
echo "Heavy folders archived at: $ARCHIVE_ROOT/*_archived"
echo ""
echo "Next steps:"
echo "1. Open vault in Obsidian from $TARGET"
echo "2. Verify search, graph, plugins work"
echo "3. Reformat source drive to ExFAT: diskutil eraseDisk ExFAT \"PNY128GBLED\" /dev/disk8"
echo "4. Copy back: rsync -avh --progress \"$TARGET/\" \"/Volumes/PNY128GBLED/$VAULT_NAME/\""
echo "5. Restore archived folders if needed"

# === SESSION 2026-08-06 LEARNINGS (added post-migration) ===
# Key learnings from PNY128GBLED -> ExFAT migration:
#
# 1. SPACE: Target needs ≥2x vault size free (34 GB vault needs ~70 GB free for safety)
#    Samsung LED had 60 GB free, vault 34 GB -> only 26 GB margin, got tight at 2.17 GB free
#
# 2. PNY DISCONNECT: diskutil unmountDisk force + eraseDisk caused drive to disappear
#    Fix: Try gentle unmount first (diskutil unmount), only force if needed
#
# 4. HEAVY FOLDERS to move OUT before rsync (caused index hangs):
#    - Transcripts/ (837 MB, 3,350 files)
#    - .vault-organizer-backups/ (du timed out)
#    - .vault-organizer-manifests/ (du timed out)
#    - graphify-out/ (752 KB)
#    - emai-dashboard/node_modules/ (56 MB)
#    - .agents/, .claude/ (hidden folders)
#
# 5. RSYNC on USB 2.0 ExFAT: ~3-4 MB/s avg, 34 GB took ~3+ hours
#    232k files, notify_on_complete essential
#
# 6. DIFF: Only ._* AppleDouble metadata files differ (ExFAT creates these)
#    No actual content differences
#
# 7. CRON: All 4 vault cron jobs already paused - no conflicts
#
# 8. POST-MIGRATION: All archived folders moved back, PNY reformatted to ExFAT
#    Rsync back in progress, Samsung LED now has only 2.17 GB free