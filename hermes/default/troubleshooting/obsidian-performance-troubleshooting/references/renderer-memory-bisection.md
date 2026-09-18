# Renderer Memory Bisection for Large Vaults

## When to Use
- Renderer process memory >300 MB
- Obsidian sluggish despite fast storage
- CPU spikes with large vaults (>5000 files)

## Bisection Steps

### 1. Baseline Measurement
```bash
# Get renderer PID
ps aux | grep "Obsidian Helper (Renderer)" | grep -v grep | awk '{print $2}'

# Monitor memory (MB)
while true; do
  ps -o rss= -p RENDERER_PID | awk '{print $1/1024 " MB"}'
  sleep 1
done
```

### 2. Disable Core Plugins Incrementally
Edit `.obsidian/core-plugins.json`, restart Obsidian, measure after each:

| Plugin | Memory Impact | Safe to Disable |
|--------|---------------|-----------------|
| global-search | High (index) | ✅ Yes |
| backlink | High (cache) | ✅ Yes |
| outgoing-link | High (cache) | ✅ Yes |
| tag-pane | Medium | ✅ Yes |
| properties | Medium | ✅ Yes |
| page-preview | Medium | ✅ Yes |
| daily-notes | Low | ⚠️ If used |
| templates | Low | ⚠️ If used |
| canvas | High (webview) | ✅ Yes |
| canvas | High (webview) | ✅ Yes |
| audio-recorder | Low | ✅ Yes |
| file-recovery | Low | ✅ Yes |
| bases | Medium | ✅ Yes |
| webviewer | High (webview) | ✅ Yes |

### 3. Disable Community Plugins Incrementally
```bash
# Check which are enabled
cat .obsidian/community-plugins.json

# Disable one by one, restart, measure
```

### 4. Identify Massive Folders
```bash
# Find directories with 1000+ files
find /vault -type d -exec sh -c 'echo $(ls -1 "{}" 2>/dev/null | wc -l) "{}"' \; | sort -rn | head -20

# Archive or .stignore (Syncthing only!)
mv /vault/MASSIVE_FOLDER /vault/MASSIVE_FOLDER_archived
```

### 5. Check Workspace Auto-Load
```bash
cat .obsidian/workspace.json | grep -A5 -B5 '"type": "graph"'
# If graph loads on startup → disable in workspace.json
```

### 6. Check Plugin Validity
```bash
# Every plugin MUST have main.js
ls -la .obsidian/plugins/*/main.js
# Dev repos without main.js = dead weight
```

## Observed Results (This Session)

| State | Renderer RAM | Renderer CPU | Notes |
|-------|--------------|--------------|-------|
| Baseline (all plugins, graph auto-load) | 477 MB | 100% | Stuck |
| Heavy plugins moved to NVMe | ~400 MB | 100% | Still stuck |
| Graph auto-load fixed | ~300 MB | 50% | Progress |
| Transcripts archived (3,350 files) | ~250 MB | 20% | Progress |
| Core indexing plugins disabled | ~200 MB | 5% | Good |
| Community plugins disabled | ~184 MB | 0.5% | Stable |
| Ancillary folders archived | ~150 MB | 0.3% | Optimal |

## Key Insights
- **Each core plugin adds 10-30 MB** background index/cache
- **Renderer memory ≈ vault file count × 10 KB** (rough rule)
- **Community plugins with dev repos add 50+ MB** (indexing source files)
- **Massive folders (3,350 files) = 50+ MB** just for file watcher
- **Graph view auto-load = full vault index on startup**

## Target: <200 MB RAM, <5% CPU at idle