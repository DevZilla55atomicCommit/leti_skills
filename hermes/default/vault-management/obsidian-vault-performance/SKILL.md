---
name: obsidian-vault-performance
description: Fix slow Obsidian on external drives via plugin symlink.
version: "1.0"
author: Maddie
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [obsidian, performance, vault, plugins, usb, symlink]
    category: vault-management
    related_skills: [vault-restructure, vault-setup, obsidian]
---

# Obsidian Vault Performance Optimization

Diagnose and fix slow Obsidian startup/loading when the vault lives on an external drive (USB, network, slow disk). The root cause is almost always **heavy plugins loading over slow I/O**, not the vault size or symlink overhead.

## When to Use

- Obsidian takes >10 seconds to open a vault on external storage
- Vault is on USB HDD/SSD, SD card, or network mount
- User has many community plugins installed
- Symlink from local path to external vault (symlink is NOT the problem)

## Prerequisites

- Access to the vault's `.obsidian/` directory
- Ability to move files between external and internal storage
- Obsidian closed during changes

## How to Run

1. **Measure plugin directory size** on the external drive:
   ```bash
   du -sh /path/to/vault/.obsidian/plugins/* | sort -hr
   ```

2. **Identify heavy plugins** (>1 MB each). Common heavy plugins:
   - `obsidian-excalidraw-plugin` (~8 MB)
   - `copilot` (~5 MB)
   - `vscode-editor` (~5 MB)
   - `graphify-core` (varies, often dev repo)
   - `claudian` (~2.8 MB)
   - `terminal` (~2.4 MB)
   - `obsidian-full-calendar` (~2.4 MB)
   - `media-extended` (~2.1 MB)
   - `galaxy-graph-view` (~1.4 MB)
   - `dataview` (~1.3 MB)
   - `obsidian-kanban` (~1 MB)
   - `obsidian-git` (~744 KB)

3. **Create internal plugin directory** on fast storage:
   ```bash
   mkdir -p ~/Library/Application\ Support/obsidian-plugins
   ```

4. **Move heavy plugins** to internal storage and symlink back:
   ```bash
   mv /path/to/vault/.obsidian/plugins/heavy-plugin ~/Library/Application\ Support/obsidian-plugins/
   ln -s ~/Library/Application\ Support/obsidian-plugins/heavy-plugin /path/to/vault/.obsidian/plugins/heavy-plugin
   ```

5. **Uninstall unused plugins** entirely:
   ```bash
   rm -rf /path/to/vault/.obsidian/plugins/unused-plugin
   # Then remove from community-plugins.json
   ```

6. **Verify reduction**:
   ```bash
   du -sh /path/to/vault/.obsidian/plugins
   # Should be <10 MB for fast USB 2.0 loading
   ```

## Quick Reference

| Plugin | Typical Size | Action |
|--------|--------------|--------|
| excalidraw, copilot, vscode-editor | 5-8 MB | Move to NVMe |
| graphify-core, claudian, terminal, full-calendar, media-extended | 2-3 MB | Move or uninstall |
| dataview, kanban, git, galaxy-graph | 1-1.5 MB | Keep if used, else uninstall |
| calendar, tasks, clipper, templater, brat | <500 KB | Fine on USB |

## Procedure

### Diagnostic Checklist
1. `du -sh vault/.obsidian/plugins` — total plugin weight
2. `du -sh vault/.obsidian/plugins/* | sort -hr` — per-plugin breakdown
3. Check drive: `diskutil info /Volumes/DRIVE | grep Protocol` — USB 2.0 = 35 MB/s max
4. Target: <10 MB on USB 2.0 for <1s plugin load

### Migration Steps (per plugin)
```bash
# 1. Move
mv /external/vault/.obsidian/plugins/PLUGIN ~/Local/obsidian-plugins/

# 2. Symlink
ln -s ~/Local/obsidian-plugins/PLUGIN /external/vault/.obsidian/plugins/PLUGIN

# 3. Verify
ls -la /external/vault/.obsidian/plugins/PLUGIN
```

### Uninstall Steps
```bash
# 1. Remove plugin directory
rm -rf /external/vault/.obsidian/plugins/PLUGIN

# 2. Edit community-plugins.json — remove entry from array
```

## Pitfalls

- **Don't move core plugins** — only community plugins in `.obsidian/plugins/`
- **Symlinks must be relative or absolute to internal path** — not to another external drive
- **Obsidian must be closed** when moving/symlinking plugins
- **graphify-core is often a dev repo, not a built plugin** — may need `npm run build` or install published version via BRAT
- **community-plugins.json must be valid JSON** — use `patch` tool or `jq`, not manual edit
- **USB 3.0/3.1 drives are fine** — this workflow is for USB 2.0 or slower interfaces
- **Graph view on startup kills performance** — workspace.json `main` view type `"graph"` forces full vault index on load; change to `"file-explorer"`
- **Core plugins can be disabled** — `core-plugins.json` `"graph": false`, `"search": false` reduces startup I/O
- **Test vault first** — open Obsidian with empty `/tmp/test-vault` to isolate vault-specific vs app-specific issues
- **APFS on USB 2.0 is unusable for vaults** — 0.87 MB/s writes, <1 MB/s uncached reads; ExFAT does 64 MB/s writes, 191 MB/s uncached reads
- **ExFAT migration path** — If drive is APFS on USB 2.0: copy vault to ExFAT drive → reformat to ExFAT → copy back
- **Transcript/export folders** — 1000s of auto-generated files kill indexing; move outside vault first
- **Archived folders at drive root** — Check `/Volumes/DRIVE/*_archived/` for folders moved out of vault during troubleshooting

## Verification

After changes:
1. Restart Obsidian
2. Time to usable interface should drop from 20-30s → 3-5s
3. Check Developer Tools (Cmd+Opt+I) → Network tab — plugin `main.js` loads from local path

## References

- `references/plugin-sizes.md` — known heavy plugin sizes and alternatives
- `references/usb-diagnostics.md` — how to identify drive speed bottleneck
- `references/obsidian-usb-performance.md` — detailed session analysis (2026-08-06)
- `references/workspace-graph-view-fix.md` — workspace.json Graph view fix details
- `templates/minimal-workspace.json` — ready-to-use workspace.json opening file-explorer
- `references/exfat-migration-checklist.md` — Step-by-step ExFAT migration for USB 2.0 vaults