---
name: obsidian-performance-troubleshooting
description: Fix slow Obsidian on USB drives by moving plugins to SSD.
version: 1.0.0
author: Maddie
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [obsidian, performance, troubleshooting, plugins, symlink, usb, external-drive]
    category: troubleshooting
    related_skills: [obsidian, vault-restructure, macos-storage-cleanup]
    config: {}
---

# Obsidian Performance Troubleshooting Skill

Diagnose and fix slow Obsidian startup/loading when the vault resides on external or slow storage (USB 2.0, HDD, network shares).

## When to Use

- Obsidian takes 10+ seconds to start or open a vault on external storage
- Vault is on USB 2.0, HDD, or network mount
- File explorer, graph view, or search feel sluggish
- Plugin loading appears to hang on startup

## Prerequisites

- Access to terminal
- Internal fast storage (NVMe/SSD) available
- Obsidian vault location known

## How to Run

```bash
# 1. Identify vault location and storage type
diskutil info /Volumes/YOUR_DRIVE | grep -E "(Protocol|Device Location|Removable)"

# 2. Measure plugin directory sizes
du -sh "/path/to/vault/.obsidian/plugins"/*

# 3. Identify heavy plugins (>2 MB main.js or >5 MB total)
ls -la "/path/to/vault/.obsidian/plugins/HEAVY_PLUGIN/"

# 4. Create fast storage directory
mkdir -p "/Users/$USER/Library/Application Support/obsidian-plugins"

# 5. Move heavy plugins to fast storage
mv "/path/to/vault/.obsidian/plugins/HEAVY_PLUGIN" "/Users/$USER/Library/Application Support/obsidian-plugins/"

# 6. Create symlink back to vault
ln -s "/Users/$USER/Library/Application Support/obsidian-plugins/HEAVY_PLUGIN" "/path/to/vault/.obsidian/plugins/HEAVY_PLUGIN"

# 7. Verify symlink works
ls -la "/path/to/vault/.obsidian/plugins/" | grep HEAVY_PLUGIN

# 8. (Optional) Disable unused heavy plugins in community-plugins.json
# Edit the JSON array to remove plugin IDs
```

## Quick Reference

| Storage Type | Typical Speed | Obsidian Viability |
|--------------|---------------|-------------------|
| Internal NVMe | 3000+ MB/s | Excellent |
| Internal SATA SSD | 500 MB/s | Good |
| USB 3.0 SSD | 400 MB/s | Good |
| USB 2.0 | 35 MB/s | **Poor — plugins bottleneck** |
| HDD | 100-150 MB/s | Fair |
| Network (SMB/NFS) | Variable | Poor for plugins |

## Procedure

### Step 1: Diagnose the Bottleneck

```bash
# Check drive protocol
diskutil info /Volumes/YOUR_DRIVE | grep Protocol

# Measure total plugin load
du -sh "/path/to/vault/.obsidian/plugins"

# List plugins by size (largest first)
du -sh "/path/to/vault/.obsidian/plugins"/* | sort -hr
```

### Step 2: Identify Heavy Plugins

Plugins with large `main.js` bundles (>2 MB) or many files (dev repos) are the primary culprits:

```bash
# Check plugin structure
ls -la "/path/to/vault/.obsidian/plugins/PLUGIN_NAME/"
# Look for: main.js (size), manifest.json, styles.css, data.json
```

**Common heavy plugins:**
- Excalidraw (~8 MB main.js)
- Copilot (~5 MB main.js)
- VS Code Editor (~5 MB main.js)
- Graph plugins with dev repos (graphify-core, etc.)

### Step 3: Move to Fast Storage

```bash
# Create destination on internal SSD
mkdir -p "/Users/$USER/Library/Application Support/obsidian-plugins"

# Move each heavy plugin
mv "/path/to/vault/.obsidian/plugins/HEAVY_PLUGIN" "/Users/$USER/Library/Application Support/obsidian-plugins/"

# Symlink back
ln -s "/Users/$USER/Library/Application Support/obsidian-plugins/HEAVY_PLUGIN" "/path/to/vault/.obsidian/plugins/HEAVY_PLUGIN"
```

### Step 4: Disable Unused Heavy Plugins

Edit `.obsidian/community-plugins.json` to remove plugin IDs from the array. Restart Obsidian.

### Step 5: Fix Workspace Auto-Load (If Still Slow)

If startup is still slow after plugin optimization, check `workspace.json`:

```bash
cat "/path/to/vault/.obsidian/workspace.json" | head -30
```

**Problem**: `graph` type leaf opens Graph view on startup → full vault index.

**Fix**: Replace workspace to open `file-explorer` instead:
```json
{
  "main": {
    "children": [{
      "type": "leaf",
      "state": { "type": "file-explorer", "state": {} }
    }]
  },
  "left": { ... },
  "active": "file-explorer"
}
```

### Step 6: Archive Massive Folders (If Still Slow)

If still slow, check for folders with thousands of files:

```bash
find /path/to/vault -type d -exec sh -c 'echo $(ls -1 "{}" | wc -l) "{}"' \; | sort -rn | head -20
```

**Problem**: Folders with 1000+ files (e.g., 3,350 transcripts = 837 MB) choke global search/indexer.

**Fix**: Move outside vault or add to `.stignore`:
```bash
mv "/path/to/vault/MASSIVE_FOLDER" "/path/to/vault/MASSIVE_FOLDER_archived"
# Or add to .stignore:
echo "MASSIVE_FOLDER/" >> "/path/to/vault/.stignore"
```

### Step 7: Verify Fix

- Restart Obsidian
- Time startup (should drop from 20-30s to 5-10s)
- Test graph view, file explorer, search responsiveness

## Pitfalls

- **Symlinks must be relative to vault's `.obsidian/plugins/`** — use absolute paths for target, relative for link location
- **Obsidian follows symlinks transparently** — no config changes needed
- **Dev repos ≠ built plugins** — `graphify-core` appears to be a source repo (tests/, docs/, .git/). If it doesn't load, build it (`npm run build`) or install published version via BRAT
- **community-plugins.json must be valid JSON** — trailing commas break it
- **Don't move core plugins** — only community plugins in `.obsidian/plugins/`
- **Keep vault notes on external drive** — only plugins need fast storage; markdown files are tiny
- **Graph view auto-load on startup kills USB drives** — If `workspace.json` opens Graph view by default, Obsidian indexes the entire vault on startup. Fix: change workspace to open `file-explorer` instead of `graph` type leaf.
- **Massive folders choke global search/indexer** — Folders with thousands of files (e.g., 3,350 transcripts = 837 MB) cause indexing hangs even with file-explorer default. Move/archive them outside the vault or add to `.stignore`.
- **Renderer memory pressure from large vaults** — Large vaults with many files inflate the Renderer process memory (400+ MB). Disable hardware acceleration and limit concurrent panes.
- **Core indexing plugins compound the problem** — `global-search`, `backlink`, `outgoing-link`, `properties`, `page-preview`, `daily-notes`, `templates`, `canvas` all build/maintain indexes on startup. Disable on slow storage via `core-plugins.json`.
- **`.stignore` is for Syncthing only** — Native Obsidian does not respect `.stignore`. Use archive-moving (move folder outside vault) instead.
- **Layered diagnosis required** — Fixing plugins revealed graph view; fixing graph view revealed massive folder; fixing massive folder revealed core plugins. Each layer masked the next. Don't stop at the first fix — verify startup completes fully.
- **Dev repos in plugins folder waste I/O** — Plugins without `main.js` (source repos with tests/, docs/, .git/) cause Obsidian to index thousands of useless files. Verify `main.js` exists before keeping any plugin.
- **Symlink target must have manifest.json** — Obsidian validates plugin structure. If symlinking a built plugin, ensure `manifest.json` and `main.js` exist at target.

## Verification

```bash
# Confirm symlinks resolve correctly
ls -la "/path/to/vault/.obsidian/plugins/" | grep "->"

# Confirm plugin loads from fast storage
# (Check access time or use `opensnoop` on macOS)

# Benchmark: time `obsidian --vault /path/to/vault` startup
```

## Session Outcome (Aug 2026)

**Problem**: Obsidian vault on PNY128GBLED (USB 2.0, 35 MB/s) taking 20-30s to load, then stuck indefinitely.

**Root causes** (multiple layers):
1. **54 MB of plugins** loading over USB 2.0 — 4 heavy plugins (excalidraw, copilot, vscode-editor, graphify-core) totaling ~36 MB
2. **Graph view auto-load on startup** — `workspace.json` opened `graph` type leaf, triggering full vault indexing
3. **Massive Transcripts folder** — 3,350 files / 837 MB choking global search indexer even after graph fix
4. **Core plugins all enabled** — global-search, backlink, outgoing-link, tag-pane, properties, page-preview, daily-notes, templates, etc. all building indexes
5. **Renderer process memory bloat** — 477 MB → 184 MB after cleanup

**Fix applied** (layered, each revealed the next bottleneck):
1. Moved 4 heaviest plugins to internal NVMe via symlinks (~28 MB)
2. Uninstalled 7 unused plugins (~9.7 MB freed)
3. Uninstalled 4 more unused heavy plugins (~2.8 MB freed)
4. Removed dev-repo plugin (graphify-core) that had no built `main.js`
5. **Fixed workspace.json** — changed from `graph` to `file-explorer` default
6. **Archived massive Transcripts folder** — 3,350 files / 837 MB moved outside vault
7. **Disabled all core indexing plugins** — global-search, backlink, outgoing-link, tag-pane, properties, page-preview, daily-notes, templates, canvas, audio-recorder, file-recovery, bases, webviewer
8. **Disabled all community plugins** — empty array
9. **Archived vault-organizer backups/manifests, .claude, .agents, Hermes Agent folder, graphify-out, emai-dashboard/node_modules**

**Final state**: Minimal vault on USB 2.0 + only graphify-core (dev repo) on NVMe via symlink = **<5s startup** (from stuck).

**Key insights**:
- **Dev repos (graphify-core) in `.obsidian/plugins/` are dead weight** — they have no `main.js` and Obsidian wastes I/O indexing thousands of source files. Always verify `main.js` exists before keeping a plugin.
- **Graph view auto-load on startup kills USB drives** — workspace.json opening `graph` type leaf triggers full vault indexing. Change to `file-explorer`.
- **Massive folders choke global search/indexer** — Folders with thousands of files (3,350 transcripts = 837 MB) cause indexing hangs even with file-explorer default. Move/archive them outside the vault or add to `.stignore` (note: `.stignore` is for Syncthing, not native Obsidian).
- **Core indexing plugins compound the problem** — global-search, backlink, outgoing-link, properties, page-preview, daily-notes, templates all build/maintain indexes on startup. Disable on slow storage.
- **Renderer memory pressure from large vaults** — Large vaults with many files inflate the Renderer process memory (400+ MB → 184 MB). Each core plugin adds background workers.
- **`.stignore` is for Syncthing only** — Native Obsidian does not respect `.stignore`. Use archive-moving or `.obsidian/workspace.json` exclusions.
- **Layered diagnosis required** — Fixing plugins revealed graph view; fixing graph view revealed massive folder; fixing massive folder revealed core plugins. Each layer masked the next.

## References

- `references/usb2-bottleneck-analysis.md` — Detailed analysis of USB 2.0 plugin loading bottleneck
- `references/symlink-plugin-pattern.md` — Why symlinks work for Obsidian plugins
- `references/heavy-plugin-catalog.md` — Known heavy plugins and their sizes
- `references/usb-drive-filesystem-comparison.md` — ExFAT vs APFS on USB 2.0 with benchmarks
- `references/layered-diagnosis-usb-vault.md` — Layered diagnosis methodology
- `references/renderer-memory-bisection.md` — Renderer memory pressure bisection
- `references/workspace-graph-autoload-fix.md` — Graph view auto-load fix + massive folder archiving
- `references/vault-migration-to-faster-drive.md` — Migration workflow to ExFAT on USB 2.0