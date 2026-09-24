#!/usr/bin/env bash
# Obsidian Vault Migration Verification Script
# Usage: ./verify-migration.sh /Volumes/SOURCE/VAULT /Volumes/DEST/VAULT

set -euo pipefail

SOURCE="${1:-/Volumes/PNY128GBLED/TamaZila Obsidian Vault}"
DEST="${2:-/Volumes/Samsung LED/TamaZila Obsidian Vault}"

echo "=== Obsidian Vault Migration Verification ==="
echo "Source: $SOURCE"
echo "Dest:   $DEST"
echo

# 1. Filesystem check
echo "1. Filesystem verification:"
diskutil info "$(dirname "$SOURCE")" | grep "File System"
diskutil info "$(dirname "$DEST")" | grep "File System"
echo

# 2. File count
echo "2. File count comparison:"
SRC_COUNT=$(find "$SOURCE" -type f | wc -l)
DST_COUNT=$(find "$DEST" -type f | wc -l)
echo "  Source: $SRC_COUNT files"
echo "  Dest:   $DST_COUNT files"
if [[ "$SRC_COUNT" -eq "$DST_COUNT" ]]; then
    echo "  ✅ Match"
else
    echo "  ❌ MISMATCH"
fi
echo

# 3. Size comparison
echo "3. Size comparison:"
SRC_SIZE=$(du -sh "$SOURCE" 2>/dev/null | cut -f1)
DST_SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)
echo "  Source: $SRC_SIZE"
echo "  Dest:   $DST_SIZE"
echo

# 4. Diff check (only metadata files should differ)
echo "4. Content diff (excluding ._* metadata):"
DIFF_OUTPUT=$(diff -r "$SOURCE" "$DEST" 2>&1 | grep -v "^\._" | head -20)
if [[ -z "$DIFF_OUTPUT" ]]; then
    echo "  ✅ No content differences (only ._* metadata)"
else
    echo "  ❌ Content differences found:"
    echo "$DIFF_OUTPUT"
fi
echo

# 5. Obsidian config check
echo "5. Obsidian config verification:"
for CONFIG in core-plugins.json community-plugins.json graph.json workspace.json; do
    if [[ -f "$SOURCE/.obsidian/$CONFIG" && -f "$DEST/.obsidian/$CONFIG" ]]; then
        if diff "$SOURCE/.obsidian/$CONFIG" "$DEST/.obsidian/$CONFIG" >/dev/null; then
            echo "  ✅ $CONFIG matches"
        else
            echo "  ⚠️  $CONFIG differs"
        fi
    fi
done
echo

# 6. Performance test (optional)
echo "6. Quick write test (10 MB):"
dd if=/dev/zero of="$(dirname "$SOURCE")/test_write" bs=1m count=10 2>&1 | tail -1
dd if=/dev/zero of="$(dirname "$DEST")/test_write" bs=1m count=10 2>&1 | tail -1
rm -f "$(dirname "$SOURCE")/test_write" "$(dirname "$DEST")/test_write"
echo

echo "=== Verification Complete ==="