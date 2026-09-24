# Obsidian USB 2.0 Performance Analysis

## Session: 2026-08-06

### Vault Configuration
- **Location**: `/Volumes/PNY128GBLED/TamaZila Obsidian Vault` (symlinked from `~/TamaZila_Obsidian_Vault`)
- **Drive**: PNY 128 GB USB 2.0 flash drive (APFS, 35 MB/s theoretical, ~15 MB/s real)
- **Vault size**: ~35 GB total, 163+ markdown files (3 levels deep)

### Initial Problem
Obsidian stuck on "Loading..." for 20-30+ seconds, sometimes timing out completely.

### Root Causes Identified

| Factor | Impact | Evidence |
|--------|--------|----------|
| **Graph view on startup** | CRITICAL | workspace.json main view = `"type": "graph"` forces full vault index |
| **Heavy plugins on USB 2.0** | HIGH | 54 MB plugins on 15 MB/s drive = 3.6s just to read |
| **graphify-core (dev repo)** | HIGH | 17 MB with 141 test dirs, 67 src dirs — not a built plugin |
| **Excalidraw (8.4 MB main.js)** | MEDIUM | Large monolithic bundle |
| **Copilot (5.5 MB)** | MEDIUM | Large bundle |
| **VS Code Editor (5.7 MB)** | MEDIUM | Large bundle |

### Plugin Breakdown (Before Fix)

```
54 MB total on USB 2.0:
  graphify-core:       17 MB  (dev repo, not built plugin)
  excalidraw:           8 MB
  copilot:              5 MB
  vscode-editor:        5 MB
  claudian:             2.8 MB
  terminal:             2.4 MB
  full-calendar:        2.4 MB
  media-extended:       2.1 MB
  galaxy-graph-view:    1.4 MB
  dataview:             1.3 MB
  kanban:               1.0 MB
  tasks:              844 KB
  git:                744 KB
  calendar:           492 KB
  lean-terminal:      476 KB
  clipper:            456 KB
  calendar-bases:     444 KB
  templater:          344 KB
  emai-dashboard:     172 KB
  brat:               100 KB
  gmail-sidebar:       20 KB
  email-block:         20 KB
```

### Fixes Applied

1. **Moved 4 heaviest plugins to NVMe via symlinks** (27.8 MB → fast storage)
   - graphify-core, excalidraw, copilot, vscode-editor

2. **Uninstalled 7 unused plugins** (9.7 MB freed)
   - claudian, terminal, full-calendar, media-extended, git, kanban, clipper, calendar-bases, brat, gmail-sidebar, email-block

3. **Changed workspace.json** from Graph view → File Explorer

4. **Disabled core Graph plugin** in core-plugins.json

### Final State

| Location | Size | Contents |
|----------|------|----------|
| USB 2.0 | 4.9 MB | 8 lightweight plugins (calendar, dataview, tasks, lean-terminal, templater, emai-dashboard, galaxy-graph-view, calendar-beta) |
| NVMe | 8.6 MB | graphify-core only (via symlink) |

### Result
- **USB load**: 4.9 MB @ 15 MB/s = **~330 ms** plugin read time
- **Graph indexing eliminated** on startup
- **Expected startup**: 3-5 seconds (vs 20-30s before)

### Verification Commands

```bash
# Check plugin sizes
du -sh /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault/.obsidian/plugins/*

# Check workspace startup view
cat /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault/.obsidian/workspace.json | jq '.main'

# Check core plugins
cat /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault/.obsidian/core-plugins.json | jq '.graph'

# Test with empty vault
mkdir -p /tmp/test-vault/.obsidian && echo '{}' > /tmp/test-vault/.obsidian/app.json
open -a "Obsidian" --args /tmp/test-vault
```

### Key Learnings

1. **Graph view is the #1 killer** on slow storage — always check workspace.json first
2. **Plugin weight matters more than vault size** — 163 MD files = negligible; 50 MB plugins = seconds
3. **Symlink migration works** — Obsidian follows symlinks in `.obsidian/plugins/` transparently
4. **Dev repos != plugins** — graphify-core was a full source repo, not a built plugin
5. **Test vault isolates issues** — empty vault loads in ~2s confirms app is fine