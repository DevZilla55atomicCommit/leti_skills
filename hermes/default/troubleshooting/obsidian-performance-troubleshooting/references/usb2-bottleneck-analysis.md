# USB 2.0 Obsidian Plugin Loading Bottleneck Analysis

## The Problem

When an Obsidian vault resides on a USB 2.0 drive, plugin loading becomes the primary startup bottleneck.

### Why USB 2.0 is Catastrophic for Obsidian Plugins

| Metric | USB 2.0 | Internal NVMe | Ratio |
|--------|---------|---------------|-------|
| Theoretical max | 480 Mbps (60 MB/s) | 32 Gbps (4000 MB/s) | 67x |
| Real-world sequential | 35-40 MB/s | 3000+ MB/s | 75x |
| Random 4K read IOPS | ~100 | ~300,000 | 3000x |
| Latency | ~1-2 ms | ~0.02 ms | 50-100x |

### Obsidian's Plugin Loading Pattern

On startup, Obsidian:
1. Reads `.obsidian/community-plugins.json` — list of enabled plugins
2. For each plugin, loads `main.js` (often 1-8 MB single file)
3. Reads `manifest.json`, `styles.css`, `data.json`
4. For dev repos (like `graphify-core`), scans thousands of files in tests/, src/, docs/

### Real-World Impact (This Session)

**Before fix:**
- `.obsidian/plugins` = 54 MB on USB 2.0
- 4 heavy plugins = 36 MB (68% of load)
- Startup time: ~20-30 seconds

**After fix:**
- `.obsidian/plugins` = 17 MB on USB 2.0 (light plugins only)
- 1 heavy plugin = 8.6 MB on NVMe via symlink
- Expected startup: ~5-10 seconds

### The Math

Loading 36 MB over USB 2.0 (35 MB/s sequential, but random I/O is far worse):
- Sequential best case: 36 MB / 35 MB/s = ~1 second
- Real-world with random I/O, directory traversal, metadata ops: **10-20 seconds**

Same 36 MB on NVMe: **<0.1 seconds**

### Why Symlinks Work

Obsidian uses Node.js `require()` to load `main.js`. The kernel resolves symlinks transparently at the VFS layer — the application sees a regular file. No code changes needed.

```bash
# Vault sees:
/Volumes/USB/vault/.obsidian/plugins/heavy-plugin/main.js
# Kernel redirects to:
/Users/.../obsidian-plugins/heavy-plugin/main.js (on NVMe)
```

This is a **zero-cost abstraction** at the OS level.