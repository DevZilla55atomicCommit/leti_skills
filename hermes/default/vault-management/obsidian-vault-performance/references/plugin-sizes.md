# Known Heavy Obsidian Plugin Sizes

Reference sizes from real vaults (may vary by version).

## Heavy (>2 MB) — Move to NVMe or Uninstall

| Plugin | Size | Notes |
|--------|------|-------|
| obsidian-excalidraw-plugin | ~8.2 MB | 8.4 MB main.js bundle |
| copilot | ~5.3 MB | 5.5 MB main.js bundle |
| vscode-editor | ~5.7 MB | 5.7 MB main.js bundle |
| graphify-core | ~8-17 MB | Often full dev repo, not built plugin |
| claudian | ~2.8 MB | Claude integration |
| terminal | ~2.4 MB | Terminal emulator |
| obsidian-full-calendar | ~2.4 MB | Calendar views |
| media-extended | ~2.1 MB | Media playback |

## Medium (1-2 MB) — Keep if Used, Else Uninstall

| Plugin | Size | Notes |
|--------|------|-------|
| galaxy-graph-view | ~1.4 MB | 3D graph, WebGL |
| dataview | ~1.3 MB | Query engine, core for many |
| obsidian-kanban | ~1.0 MB | Kanban boards |
| obsidian-tasks-plugin | ~844 KB | Task management |
| obsidian-git | ~744 KB | Git integration |

## Light (<500 KB) — Fine on USB

| Plugin | Size |
|--------|------|
| calendar | ~492 KB |
| lean-terminal | ~476 KB |
| obsidian-clipper | ~456 KB |
| calendar-bases | ~444 KB |
| templater-obsidian | ~344 KB |
| emai-dashboard | ~172 KB |
| obsidian42-brat | ~100 KB |
| gmail-sidebar-launcher | ~20 KB |
| email-block-plugin | ~20 KB |

## Decision Matrix

| Vault Drive | Total Plugin Target | Strategy |
|-------------|---------------------|----------|
| USB 2.0 (35 MB/s) | <10 MB | Move all >1 MB to NVMe |
| USB 3.0 (400 MB/s) | <50 MB | Move >5 MB only |
| NVMe internal | No limit | No action needed |
| Network (SMB/NFS) | <5 MB | Move all >500 KB |

## Verification Command

```bash
du -sh /path/to/vault/.obsidian/plugins/* | sort -hr
```