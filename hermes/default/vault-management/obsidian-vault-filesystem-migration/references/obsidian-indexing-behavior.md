# Obsidian Indexing Behavior — What Triggers It & How to Minimize

## What Triggers Full Re-indexing

| Trigger | Scope | Duration (327k files) |
|---------|-------|----------------------|
| First open after migration | Full vault | ~45 min |
| Graph view open | Full vault + links | Additional ~10 min |
| Global search first use | Full text index | ~20 min |
| New plugin enable | Affected files only | Seconds |
| File move/rename outside Obsidian | Affected paths | Seconds |

## What Triggers Incremental Updates

- File save inside Obsidian (instant)
- File create/delete in vault (instant, via fs watcher)
- Settings change (plugins, core plugins)
- Workspace layout change

## Obsidian Indexing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Main Process (PID)                                         │
│  ├─ Renderer (Electron) — UI, graph, search UI              │
│  ├─ GPU Helper — hardware acceleration                       │
│  └─ Utility (Network) — sync, updates                       │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Indexer (internal, runs in Renderer)                       │
│  ├─ File watcher (fs events) — incremental                  │
│  ├─ Full scan — on first open, major changes                │
│  ├─ Search index (Lunr.js / custom) — full text             │
│  ├─ Graph index (links, backlinks, tags) — relationships    │
│  └─ Properties index (YAML frontmatter) — metadata          │
└─────────────────────────────────────────────────────────────┘
```

## What Triggers High CPU/Memory

| Component | Normal | During Indexing |
|-----------|--------|-----------------|
| Renderer CPU | < 5% | 100-130% |
| Renderer RAM | 200-500 MB | 1.5-2 GB |
| Main CPU | < 1% | 1-5% |
| Main RAM | 150-300 MB | 200-400 MB |

## How to Minimize Indexing Load

### 1. Disable Auto-Load Heavy Views
```json
// core-plugins.json
{
  "graph": false,          // Don't auto-compute graph on startup
  "global-search": false,  // Don't build search index until used
  "backlink": false,       // Skip backlink computation
  "outgoing-link": false,  // Skip outgoing link scan
  "tag-pane": false,       // Skip tag index
  "properties": false      // Skip YAML properties index
}
```

### 2. Move Heavy Folders Before First Open
Move these OUT of vault before first open:
- `Transcripts/` (thousands of .json/.txt/.wav)
- `node_modules/` (thousands of tiny JS files)
- `.vault-organizer-backups/` (many copies)
- `.git/` (if present)
- Large media folders (GB of images/video)

### 3. Minimal Core Plugins for Migration
```json
{
  "file-explorer": true,     // Essential
  "switcher": true,          // Cmd+O quick open
  "command-palette": true,   // Cmd+P commands
  "slash-command": true,     // /commands
  "outline": true,           // Document outline
  "word-count": true,        // Word count
  "graph": false,            // Disable until needed
  "global-search": false,    // Disable until needed
  "backlink": false,
  "outgoing-link": false,
  "tag-pane": false,
  "properties": false,
  "page-preview": false,
  "daily-notes": false,
  "templates": false,
  "canvas": false,
  "audio-recorder": false,
  "file-recovery": false,
  "bases": false,
  "webviewer": false
}
```

### 4. Community Plugins — Enable Gradually
```json
// community-plugins.json
["galaxy-graph-view"]  // Only graph plugin
// Add one at a time after stable
```

### 5. Workspace — Start Clean
```json
// workspace.json — minimal, file-explorer default
{
  "main": { "type": "leaf", "state": { "type": "file-explorer" } },
  "left": { "type": "split", "children": [{"type": "leaf", "state": {"type": "file-explorer"}}] },
  "active": "file-explorer"
}
```

## Indexing Timeline (327k files, ExFAT on USB 2.0)

| Time | Activity | Renderer CPU | Renderer RAM |
|------|----------|--------------|--------------|
| 0-2 min | App start, file-explorer load | 120% | 300 MB |
| 2-10 min | File scan, fs watcher setup | 130% | 800 MB |
| 10-25 min | Search index build (global-search) | 130% | 1.2 GB |
| 25-40 min | Graph index build (links/backlinks) | 130% | 1.9 GB |
| 40-45 min | Properties/YAML parse | 100% | 1.9 GB |
| 45+ min | **Complete — idle** | **< 5%** | **~800 MB** |

## Monitoring Progress

```bash
# Watch renderer process
ps aux | grep "Obsidian Helper (Renderer)" | grep -v grep

# Key indicators:
# CPU dropping from 130% → < 5%
# RAM dropping from 1.9 GB → ~800 MB
# File count stable: find VAULT -type f | wc -l
```

## Pitfalls

1. **Graph view enabled by default** — computes full graph on startup, kills USB 2.0
2. **Global search enabled** — builds full-text index on all 327k files
3. **Backlinks/outgoing links** — scans all links on startup
4. **Properties/YAML** — parses frontmatter on every file
5. **Workspace opens Graph view** — triggers graph computation immediately
6. **File watcher + 327k files** — initial fs events flood

## Best Practice for Large Vaults on Slow Storage

1. **Pre-migration**: Disable graph, search, backlinks, properties
2. **Move heavy folders out** before first open
3. **Minimal workspace** — file-explorer only
3. **Open, wait 45 min** — let indexing complete
4. **Re-enable features one at a time** — test each
5. **Keep heavy folders archived** — only link if needed