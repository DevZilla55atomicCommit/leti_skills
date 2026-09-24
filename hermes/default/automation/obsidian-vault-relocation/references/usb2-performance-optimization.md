# USB 2.0 External Drive Performance Optimization for Obsidian

## Problem
Obsidian on a USB 2.0 external drive (PNY128GBLED / "USB 2.0 FD") exhibits 20-30+ second startup times because:
- USB 2.0 = 480 Mbps theoretical (~35-40 MB/s real sequential, far worse for random I/O)
- Obsidian loads ALL enabled plugin `main.js` bundles on startup
- Heavy plugins with thousands of files cause massive random I/O

## Solution: Symlink Heavy Plugins to Internal SSD

### Identify Heavy Plugins
```bash
du -sh "/Volumes/<DRIVE_NAME>/<Vault Name>/.obsidian/plugins"/*
```

### Move to Local SSD
```bash
mkdir -p "~/Library/Application Support/obsidian-plugins"
mv "/Volumes/<DRIVE>/<Vault>/.obsidian/plugins/<heavy-plugin>" \
   "~/Library/Application Support/obsidian-plugins/"
ln -s "~/Library/Application Support/obsidian-plugins/<heavy-plugin>" \
      "/Volumes/<DRIVE>/<Vault>/.obsidian/plugins/<heavy-plugin>"
```

### Plugins Moved in This Session
| Plugin | Original Size | Type |
|--------|--------------|------|
| graphify-core | 17 MB → 8.6 MB (dev repo) | Full source tree (tests/, docs/, .git/) |
| obsidian-excalidraw-plugin | 8.2 MB | Large main.js bundle (8.4 MB) |
| copilot | 5.3 MB | Large main.js bundle (5.5 MB) |
| vscode-editor | 5.7 MB | Large main.js bundle (5.7 MB) |

**Total moved: ~27.8 MB** (68% reduction in external drive plugin I/O)

## Verification
```bash
# Check symlinks
ls -la "/Volumes/<DRIVE>/<Vault>/.obsidian/plugins/" | grep -E "graphify|excalidraw|copilot|vscode"

# Verify local copies have proper plugin structure
ls -la "~/Library/Application Support/obsidian-plugins/<plugin>/main.js"
```

## Results
- External `.obsidian/plugins`: 54 MB → 17 MB
- Plugin loading shifts from USB 2.0 (~35 MB/s) to NVMe SSD (~3000+ MB/s)
- Expected startup: 20-30s → 5-10s

## Caveats
- Moved plugin MUST be a valid built plugin (`main.js`, `manifest.json`, `styles.css`)
- Dev repos like `graphify-core` may need `npm run build` first
- Symlinks work transparently — Obsidian follows them at runtime