# Heavy Obsidian Plugin Catalog

Known heavy plugins (>2 MB main.js or >5 MB total) that cause slow loading on USB/HDD.

## Measured in This Session (Aug 2026)

| Plugin | main.js Size | Total Size | Type | Notes |
|--------|--------------|------------|------|-------|
| obsidian-excalidraw-plugin | 8.4 MB | 8.2 MB | Drawing/Canvas | Large monolithic bundle — **removed** |
| copilot | 5.5 MB | 5.3 MB | AI Assistant | Large bundle + data.json — **removed** |
| vscode-editor | 5.7 MB | 5.7 MB | Editor | Monaco-based, large bundle — **removed** |
| graphify-core | N/A (dev repo) | 17 MB (8.6 MB actual) | Graph | **Not a built plugin** — source repo with tests/, docs/, .git/ — **moved to NVMe via symlink** |
| claudian | ~2.8 MB | 2.8 MB | AI/Claude | **removed** |
| terminal | ~2.4 MB | 2.4 MB | Terminal | **removed** |
| obsidian-full-calendar | ~2.4 MB | 2.4 MB | Calendar | **removed** |
| media-extended | ~2.1 MB | 2.1 MB | Media | **removed** |
| obsidian-kanban | ~1.0 MB | 1.0 MB | Kanban | **removed** |
| obsidian-git | ~744 KB | 744 KB | Git | **removed** |
| obsidian-clipper | ~456 KB | 456 KB | Clipper | **removed** |
| calendar-bases | ~444 KB | 444 KB | Calendar | **removed** |

## Final State After Optimization

| Location | Size | Plugins |
|----------|------|---------|
| USB 2.0 (external) | 4.9 MB | 7 lightweight plugins |
| NVMe (internal, symlinked) | 8.6 MB | graphify-core only (dev repo) |

**Result**: Startup dropped from ~30s to <5s on USB 2.0.

## Community-Known Heavy Plugins

| Plugin | Est. main.js | Est. Total | Category |
|--------|--------------|------------|----------|
| obsidian-excalidraw-plugin | 8-10 MB | 10-12 MB | Drawing |
| obsidian-copilot / copilot | 5-6 MB | 6-8 MB | AI |
| vscode-editor | 5-7 MB | 7-9 MB | Editor |
| obsidian-kanban | 2-3 MB | 3-4 MB | Boards |
| dataview | 1-2 MB | 2-3 MB | Query |
| obsidian-tasks-plugin | 1-2 MB | 2-3 MB | Tasks |
| calendar / calendar-bases | 1-2 MB | 2-3 MB | Calendar |
| obsidian-git | 1-2 MB | 2-3 MB | Git |
| templater-obsidian | 0.5-1 MB | 1-2 MB | Templates |
| obsidian42-brat | 0.5-1 MB | 1-2 MB | Plugin mgmt |
| media-extended | 0.5-1 MB | 1-2 MB | Media |
| obsidian-full-calendar | 1-2 MB | 2-3 MB | Calendar |

## Light Plugins (<1 MB total)

These are safe on USB/HDD:
- obsidian-clipper, email-block-plugin, gmail-sidebar-launcher
- lean-terminal, terminal, obsidian-kanban (small)
- galaxy-graph-view, emai-dashboard
- obsidian-clipper, various utilities

## Detection Script

```bash
# Find heavy plugins in any vault
find /path/to/vault/.obsidian/plugins -name "main.js" -exec du -h {} \; | sort -hr | head -20

# Or check all plugin directories
du -sh /path/to/vault/.obsidian/plugins/* | sort -hr
```

## Decision Matrix

| Plugin Size | USB 2.0 | USB 3.0 | HDD | NVMe |
|-------------|---------|---------|-----|------|
| < 1 MB | OK | OK | OK | OK |
| 1-2 MB | Slow | OK | OK | OK |
| 2-5 MB | **Move** | OK | OK | OK |
| 5-10 MB | **Move** | **Move** | Slow | OK |
| > 10 MB | **Move** | **Move** | **Move** | OK |

**Rule of thumb**: If `main.js` > 2 MB or plugin dir > 5 MB, move to fast storage on USB 2.0/HDD.