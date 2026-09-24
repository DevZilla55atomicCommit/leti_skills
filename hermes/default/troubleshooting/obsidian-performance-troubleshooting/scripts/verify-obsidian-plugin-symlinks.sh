#!/usr/bin/env bash
# verify-obsidian-plugin-symlinks.sh
# Verify that Obsidian plugin symlinks resolve correctly and point to fast storage.

set -euo pipefail

VAULT_PATH="${1:-}"
FAST_STORAGE_BASE="${2:-/Users/$USER/Library/Application Support/obsidian-plugins}"

if [[ -z "$VAULT_PATH" ]]; then
    echo "Usage: $0 <vault-path> [fast-storage-base]"
    echo "Example: $0 \"/Volumes/PNY128GBLED/TamaZila Obsidian Vault\""
    exit 1
fi

PLUGINS_DIR="$VAULT_PATH/.obsidian/plugins"

if [[ ! -d "$PLUGINS_DIR" ]]; then
    echo "Error: Plugins directory not found at $PLUGINS_DIR"
    exit 1
fi

echo "=== Obsidian Plugin Symlink Verification ==="
echo "Vault: $VAULT_PATH"
echo "Fast storage base: $FAST_STORAGE_BASE"
echo ""

# Check each item in plugins directory
for item in "$PLUGINS_DIR"/*; do
    [[ -e "$item" ]] || continue
    name=$(basename "$item")
    
    if [[ -L "$item" ]]; then
        target=$(readlink "$item")
        if [[ -d "$target" ]]; then
            # Check if target is on fast storage
            if [[ "$target" == "$FAST_STORAGE_BASE"* ]]; then
                size=$(du -sh "$target" 2>/dev/null | cut -f1)
                echo "✅ $name -> $target ($size) [FAST STORAGE]"
            else
                size=$(du -sh "$target" 2>/dev/null | cut -f1)
                echo "⚠️  $name -> $target ($size) [EXTERNAL TARGET]"
            fi
        else
            echo "❌ $name -> $target [BROKEN SYMLINK]"
        fi
    elif [[ -d "$item" ]]; then
        size=$(du -sh "$item" 2>/dev/null | cut -f1)
        # Check if it's a heavy plugin that should be moved
        main_js="$item/main.js"
        if [[ -f "$main_js" ]]; then
            js_size=$(du -h "$main_js" 2>/dev/null | cut -f1)
            if [[ $(du -k "$main_js" 2>/dev/null | cut -f1) -gt 2048 ]]; then
                echo "🔴 $name ($size, main.js: $js_size) [HEAVY — SHOULD BE SYMLINKED]"
            else
                echo "🟢 $name ($size, main.js: $js_size) [LIGHT — OK ON EXTERNAL]"
            fi
        else
            echo "🟡 $name ($size) [NO main.js — CHECK MANUALLY]"
        fi
    fi
done

echo ""
echo "=== Summary ==="
symlink_count=$(find "$PLUGINS_DIR" -maxdepth 1 -type l | wc -l)
dir_count=$(find "$PLUGINS_DIR" -maxdepth 1 -type d ! -path "$PLUGINS_DIR" | wc -l)
echo "Symlinks: $symlink_count"
echo "Directories: $dir_count"
echo ""
echo "Run this after moving plugins to verify the setup."

# Additional: Verify workspace.json doesn't auto-load graph
WORKSPACE_JSON="$VAULT_PATH/.obsidian/workspace.json"
if [[ -f "$WORKSPACE_JSON" ]]; then
    echo ""
    echo "=== Workspace Auto-Load Check ==="
    if grep -q '"type": "graph"' "$WORKSPACE_JSON"; then
        echo "⚠️  workspace.json opens Graph view on startup (slow on USB)"
        echo "   Fix: Change 'graph' to 'file-explorer' in main/left/right leaves"
    else
        echo "✅ workspace.json does not auto-load Graph view"
    fi
fi

# Additional: Check for massive folders
echo ""
echo "=== Massive Folder Check ==="
find "$VAULT_PATH" -maxdepth 3 -type d -exec sh -c '
    count=$(ls -1 "{}" 2>/dev/null | wc -l)
    if [[ $count -gt 500 ]]; then
        size=$(du -sh "{}" 2>/dev/null | cut -f1)
        echo "⚠️  {} ($count files, $size) [MASSIVE — CONSIDER ARCHIVING]"
    fi
' \;

# Additional: Filesystem type check
echo ""
echo "=== Filesystem Type Check ==="
DISK=$(df "$VAULT_PATH" | tail -1 | awk '{print $1}')
FS_TYPE=$(diskutil info "$DISK" 2>/dev/null | grep "File System Personality" | awk -F: '{print $2}' | xargs)
echo "Drive: $DISK"
echo "Filesystem: $FS_TYPE"
if [[ "$FS_TYPE" == "APFS" ]]; then
    echo "⚠️  APFS on USB is slow for writes — consider ExFAT for Obsidian vaults on USB 2.0"
elif [[ "$FS_TYPE" == "ExFAT" ]]; then
    echo "✅ ExFAT on USB — optimal for Obsidian vaults"
fi