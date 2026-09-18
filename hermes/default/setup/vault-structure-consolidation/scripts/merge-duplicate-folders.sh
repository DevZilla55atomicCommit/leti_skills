#!/bin/bash
# Merge Space-Folders into Underscore-Folders
# Usage: ./merge-duplicate-folders.sh [VAULT_PATH]

set -euo pipefail

VAULT="${1:-/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Videographer}"

echo "=== Merging duplicate folders in $VAULT ==="

# Define space/underscore pairs
PAIRS=(
    "Camera Movement|Camera_Movement"
    "Camera Theory|Camera_Theory"
    "Lenses & Optics|Lenses_&_Optics"
    "Business & Career|Business_&_Career"
    "VFX & Compositing|VFX_&_Compositing"
    "Post-Production|Post_Production"
    "Color Grading|Color_Grading"
)

for pair in "${PAIRS[@]}"; do
    SPACE=$(echo "$pair" | cut -d'|' -f1)
    UNDERSCORE=$(echo "$pair" | cut -d'|' -f2)
    
    SPACE_PATH="$VAULT/$SPACE"
    UNDERSCORE_PATH="$VAULT/$UNDERSCORE"
    
    if [[ -d "$SPACE_PATH" && -d "$UNDERSCORE_PATH" ]]; then
        echo "→ Merging '$SPACE' into '$UNDERSCORE'..."
        
        # Copy .md files (don't overwrite)
        find "$SPACE_PATH" -maxdepth 1 -name "*.md" -exec cp -n {} "$UNDERSCORE_PATH/" \;
        
        # Copy assets folder
        if [[ -d "$SPACE_PATH/assets" ]]; then
            cp -rn "$SPACE_PATH/assets/" "$UNDERSCORE_PATH/" 2>/dev/null || true
        fi
        
        # Copy any subfolders (reel folders)
        find "$SPACE_PATH" -maxdepth 1 -type d ! -path "$SPACE_PATH" ! -name "assets" -exec cp -rn {} "$UNDERSCORE_PATH/" \; 2>/dev/null || true
        
        # Remove empty space folder
        rm -rf "$SPACE_PATH"
        echo "  ✅ Done: $SPACE → $UNDERSCORE"
    elif [[ -d "$SPACE_PATH" ]]; then
        echo "⚠️  Only space folder exists: $SPACE (renaming)"
        mv "$SPACE_PATH" "$UNDERSCORE_PATH"
    else
        echo "✅ Already canonical: $UNDERSCORE"
    fi
done

echo ""
echo "=== Verification ==="
ls -la "$VAULT/" | grep -E "^d" | grep -v "^\." | awk '{print $NF}'

echo ""
echo "=== All indexes created ==="
find "$VAULT" -name "00-MASTER-INDEX.md" -o -name "00-INDEX*.md" | wc -l