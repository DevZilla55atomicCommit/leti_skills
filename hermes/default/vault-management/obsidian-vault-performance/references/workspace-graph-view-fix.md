# Workspace.json Graph View Fix

## Problem

Obsidian's `workspace.json` controls the UI layout on startup. If the main view is set to Graph (`"type": "graph"`), Obsidian must build the entire graph index before showing the UI — this scans all markdown files and links, which is extremely slow on USB 2.0 drives.

## Detection

```bash
cat /path/to/vault/.obsidian/workspace.json | jq '.main.children[0].children[0].state.type'
# Returns "graph" = problematic
```

## Fix

Replace the main view with file-explorer:

```json
{
  "main": {
    "id": "main-root",
    "type": "split",
    "children": [
      {
        "id": "main-tabs",
        "type": "tabs",
        "children": [
          {
            "id": "file-explorer",
            "type": "leaf",
            "state": {
              "type": "file-explorer",
              "state": {
                "sortOrder": "alphabetical",
                "autoReveal": false
              },
              "icon": "lucide-folder-closed",
              "title": "Files"
            }
          }
        ]
      }
    ],
    "direction": "vertical"
  }
}
```

## Complete Minimal Workspace

See `templates/minimal-workspace.json` for a full working workspace.json that opens file-explorer by default with standard left/right panels.

## Verification

After fix, Obsidian opens directly to file list — no graph indexing delay.