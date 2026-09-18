---
name: obsidian-vault-performance-troubleshooting
description: Fix slow Obsidian vault loading on USB 2.0/slow storage.
version: 1.0.0
author: Alfred
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [obsidian, performance, troubleshooting, usb, indexing]
    category: vault-management
    related_skills: [vault-restructure, vault-setup, vault-setup-enhanced]
    config:
      - obsidian.vault_path
      - obsidian.storage_type
---

# Obsidian Vault Performance Troubleshooting Skill

Diagnose and fix slow Obsidian startup on slow storage (USB 2.0, network drives, HDDs). The core issue is Obsidian's synchronous indexing of all vault files on startup.

## When to Use

- Obsidian takes >10 seconds to load a vault
- Vault is on external USB 2.0, network drive, or slow HDD
- Renderer process hits 100% CPU on startup
- File explorer doesn't appear or is unresponsive

## Prerequisites

- Obsidian installed
- Access to vault `.obsidian/` config folder
- Terminal access to move/archive folders

## How to Run

1. **Identify the bottleneck** — Check vault size and folder structure:
   ```bash
   du -sh /path/to/vault/*
   find /path/to/vault -maxdepth 2 -type d | xargs du -sh 2>/dev/null | sort -hr | head -20
   ```

2. **Check for massive folders** — Common culprits:
   - `node_modules/` (npm packages)
   - Transcript/export folders (100s of MB, 1000s of files)
   - `.git/` repos inside vault
   - Build artifacts, caches, backups

3. **Move heavy folders outside vault** — Archive to same drive but outside vault root:
   ```bash
   mv /path/to/vault/HeavyFolder /path/to/HeavyFolder_archived
   ```

4. **Disable unnecessary core plugins** — Edit `.obsidian/core-plugins.json`:
   Keep only: `file-explorer`, `switcher`, `command-palette`, `slash-command`, `outline`, `word-count`
   Disable: `global-search`, `graph`, `backlink`, `canvas`, `outgoing-link`, `tag-pane`, `properties`, `page-preview`, `daily-notes`, `templates`, `note-composer`, `editor-status`, `bookmarks`, `audio-recorder`, `file-recovery`, `bases`, `sync`, `webviewer`

5. **Disable all community plugins** — Edit `.obsidian/community-plugins.json`:
   ```json
   []
   ```

6. **Fix Graph view config** — Edit `.obsidian/graph.json`:
   Remove queries referencing moved/missing folders. Keep only queries for existing paths.

7. **Set workspace to file-explorer** — Edit `.obsidian/workspace.json`:
   Default view should be file-explorer, not graph.

8. **Restart Obsidian** — Verify load time <5 seconds.

9. **Re-enable plugins selectively** — Add back only what you need, test after each.

## Quick Reference

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| 100% renderer CPU | Graph view indexing missing paths | Disable graph core plugin, fix graph.json |
| Hangs on "Loading..." | Massive folder (node_modules, transcripts) | Move outside vault |
| Slow file explorer | Too many plugins + slow storage | Disable all non-essential plugins |
| High memory (400MB+) | Large vault indexing | Archive old folders, disable global-search |

## Pitfalls

- **Don't delete folders** — Move them outside vault root; you can restore later
- **Graph view queries** — Must reference existing paths; stale queries cause CPU spin
- **Community plugins** — Some (like calendar, dataview) index on startup; disable first
- **Symlinks inside vault** — Obsidian follows them; don't symlink heavy folders back in
- **USB 2.0 limit** — ~35 MB/s theoretical, ~15 MB/s real; NVMe is 100x faster
- **APFS on USB 2.0 is catastrophic** — 0.87 MB/s writes, <1 MB/s uncached reads; ExFAT does 64 MB/s / 191 MB/s (measured)
- **ExFAT > APFS for USB 2.0 vaults** — No journaling, no copy-on-write, simple allocation table
- **Transcript/export folders** — 1000s of auto-generated files kill indexing; move outside vault first

## Verification

After fixes:
- Obsidian loads in <5 seconds
- Renderer CPU <5% at idle
- Memory <200 MB at idle
- File explorer responsive immediately

## References

- `references/usb2-bottleneck-analysis.md` — Detailed analysis of USB 2.0 vs NVMe performance
- `references/common-heavy-folders.md` — Checklist of folders that commonly cause issues
- `references/minimal-core-plugins.json` — Known-good minimal core-plugins.json
- `references/minimal-workspace.json` — Known-good workspace.json defaulting to file-explorer
- `references/exfat-migration-checklist.md` — Step-by-step ExFAT migration for USB 2.0 vaults