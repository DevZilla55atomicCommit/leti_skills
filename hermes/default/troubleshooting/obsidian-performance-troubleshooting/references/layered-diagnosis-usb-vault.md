# Layered Diagnosis for USB Vault Performance

## The Core Insight

Performance problems on slow storage (USB 2.0, HDD) are **layered**. Each fix reveals the next bottleneck. Don't stop at the first fix — verify startup completes fully.

## The Layers (Observed in This Session)

### Layer 1: Plugin Load (Obvious)
- **Symptom**: 20-30s startup
- **Cause**: 54 MB plugins loading over 35 MB/s USB 2.0
- **Fix**: Move heavy plugins to NVMe via symlinks, uninstall unused
- **Revealed**: Next layer

### Layer 2: Graph View Auto-Load (Hidden)
- **Symptom**: Still slow after plugin optimization
- **Cause**: `workspace.json` opened `graph` type leaf → full vault index on startup
- **Fix**: Replace workspace to open `file-explorer` instead
- **Revealed**: Next layer

### Layer 3: Massive Folder Choking Indexer (Hidden)
- **Symptom**: UI loads but renderer 100% CPU, 400+ MB RAM, still "loading"
- **Cause**: 3,350 files / 837 MB in `Transcripts/` — global search indexer choking
- **Fix**: Move folder outside vault root
- **Revealed**: Next layer

### Layer 4: Core Indexing Plugins (Hidden)
- **Symptom**: Still renderer 100% CPU after massive folder moved
- **Cause**: All core plugins enabled — `global-search`, `backlink`, `outgoing-link`, `tag-pane`, `properties`, `page-preview`, `daily-notes`, `templates`, `canvas`, etc. all building indexes
- **Fix**: Disable all non-essential core plugins in `core-plugins.json`
- **Revealed**: Next layer

### Layer 5: Dev Repo in Plugins Folder (Hidden)
- **Symptom**: Plugin load still has dead weight
- **Cause**: `graphify-core` was a dev repo (tests/, docs/, .git/) with no `main.js`
- **Fix**: Remove or build properly
- **Revealed**: Next layer

### Layer 6: Ancillary Heavy Folders (Hidden)
- **Symptom**: Minor but cumulative
- **Cause**: `emai-dashboard/node_modules` (56 MB), `.vault-organizer-backups`, `.claude`, `.agents`, `Hermes Agent/`, `graphify-out/`
- **Fix**: Archive outside vault
- **Final**: Stable <5s startup

## Diagnosis Algorithm

```bash
# 1. Check plugins
du -sh /vault/.obsidian/plugins/* | sort -hr

# 2. Check workspace auto-load
cat /vault/.obsidian/workspace.json | grep '"type": "graph"'

# 3. Check massive folders
find /vault -type d -exec sh -c 'echo $(ls -1 "{}" 2>/dev/null | wc -l) "{}"' \; | sort -rn | head -20

# 4. Check core plugins
cat /vault/.obsidian/core-plugins.json | grep true

# 5. Check plugin validity
ls -la /vault/.obsidian/plugins/*/main.js

# 6. Check ancillary folders
du -sh /vault/* | sort -hr
```

## Verification Checklist

After each fix, verify:
- [ ] Obsidian starts in <10s
- [ ] Renderer process <200 MB RAM
- [ ] Renderer CPU <5% at idle
- [ ] File explorer responsive immediately
- [ ] No "loading" spinner after UI appears

## Key Principle

**"Each layer masks the next."** The plugin layer was the loudest, but not the only one. On fast storage, layers 2-6 are invisible. On USB 2.0, each layer adds 10-30s of hang time. Only by peeling them all do you reach stability.

## When to Stop

Stop when:
- Startup <10s on target storage
- Renderer idle <5% CPU, <200 MB RAM
- UI fully interactive immediately

Don't stop at "better than before" — that's how you get stuck at Layer 2 wondering why it's still slow.