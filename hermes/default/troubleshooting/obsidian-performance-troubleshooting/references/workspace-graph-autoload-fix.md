# Workspace Graph Auto-Load Fix

## Problem

Obsidian's `workspace.json` can open Graph view (`"type": "graph"`) on startup. This triggers **full vault indexing** before the UI becomes responsive.

On USB 2.0 drives, this is catastrophic:
- Vault: 1000+ files across nested folders
- Graph must scan all files, build link cache, compute force-directed layout
- USB 2.0 random I/O: ~100 IOPS → minutes of indexing

## Detection

```bash
cat "/path/to/vault/.obsidian/workspace.json" | grep -A 5 '"type": "graph"'
```

## Fix: Replace Workspace to Open File Explorer

```json
{
  "main": {
    "id": "main-root",
    "type": "split",
    "children": [{
      "id": "main-tabs",
      "type": "tabs",
      "children": [{
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
      }]
    }],
    "direction": "vertical"
  },
  "left": {
    "id": "left-root",
    "type": "split",
    "children": [{
      "id": "left-tabs",
      "type": "tabs",
      "children": [{
        "id": "file-explorer-left",
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
      }, {
        "id": "search-left",
        "type": "leaf",
        "state": {
          "type": "search",
          "state": {
            "query": "",
            "matchingCase": false,
            "explainSearch": false,
            "collapseAll": false,
            "folder": null
          },
          "icon": "lucide-search",
          "title": "Search"
        }
      }, {
        "id": "bookmarks-left",
        "type": "leaf",
        "state": {
          "type": "bookmarks",
          "state": {},
          "icon": "lucide-bookmark",
          "title": "Bookmarks"
        }
      }]
    }],
    "direction": "vertical"
  },
  "right": {
    "id": "right-root",
    "type": "split",
    "children": [{
      "id": "right-tabs",
      "type": "tabs",
      "children": [{
        "id": "outline-right",
        "type": "leaf",
        "state": {
          "type": "outline",
          "state": {},
          "icon": "lucide-list",
          "title": "Outline"
        }
      }, {
        "id": "tag-pane-right",
        "type": "leaf",
        "state": {
          "type": "tag",
          "state": {
            "sortOrder": "count",
            "showHierarchy": true
          },
          "icon": "lucide-tags",
          "title": "Tags"
        }
      }]
    }],
    "direction": "vertical"
  },
  "left-ribbon": { "hiddenIcons": {} },
  "active": "file-explorer",
  "lastOpenFiles": []
}
```

## Result

- File explorer loads instantly (directory listing only)
- No graph indexing on startup
- User can manually open Graph view when needed (and it will work better with pre-built cache)

---

# Massive Folder Archiving

## Problem

Folders with 1000+ files (especially text/markdown) choke Obsidian's:
- Global search indexer
- File watcher
- Graph view link resolution
- Backlink computation

Even with file-explorer default, background indexer runs on all vault files.

## Detection

```bash
# Find directories with most files
find /path/to/vault -type d -exec sh -c 'echo $(ls -1 "{}" 2>/dev/null | wc -l) "{}"' \; | sort -rn | head -20

# Or for markdown files specifically
find /path/to/vault -name "*.md" -type f | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -20
```

## Fix Options

### Option 1: Move Outside Vault (Recommended)

```bash
mv "/path/to/vault/MASSIVE_FOLDER" "/path/to/vault/MASSIVE_FOLDER_archived"
```

Files remain accessible via OS but not indexed by Obsidian.

### Option 2: Add to .stignore

```bash
echo "MASSIVE_FOLDER/" >> "/path/to/vault/.stignore"
```

Requires Syncthing/Obsidian Sync that respects `.stignore`. Native Obsidian doesn't use `.stignore` — this only works with Sync.

### Option 3: Use Obsidian's "Exclude from search" (Manual)

Right-click folder in file explorer → "Exclude from search" (if available in plugin).

## Real Case (This Session)

**Folder**: `Hermes Agent/DaVinci_Knowledge_Base/Transcripts/`
- **Files**: 3,350 markdown + json + txt + wav sidecars
- **Size**: 837 MB
- **Impact**: Renderer process 477 MB → 184 MB after archiving
- **Fix**: `mv Transcripts Transcripts_archived` (outside vault root)
- **Result**: Startup <5s, Renderer memory 184 MB