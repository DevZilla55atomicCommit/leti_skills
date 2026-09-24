# USB Drive Diagnostics for Obsidian Vault Performance

Quick commands to identify drive speed bottlenecks.

## Identify Drive Protocol

```bash
# macOS
diskutil info /Volumes/DRIVE_NAME | grep -E "(Protocol|Device Location|Removable|Solid State)"

# Linux
lsblk -d -o NAME,TRAN,MODEL,SIZE /dev/sdX
```

## Expected Speeds by Protocol

| Protocol | Theoretical | Real-World Read | Random 4K Read |
|----------|-------------|-----------------|----------------|
| USB 2.0 | 480 Mbps (60 MB/s) | 30-40 MB/s | **0.5-1 MB/s** |
| USB 3.0 / 3.1 Gen 1 | 5 Gbps (625 MB/s) | 300-400 MB/s | 20-40 MB/s |
| USB 3.1 Gen 2 | 10 Gbps (1.25 GB/s) | 800-900 MB/s | 50-80 MB/s |
| USB 4 / Thunderbolt 3/4 | 40 Gbps (5 GB/s) | 2.5-3 GB/s | 100-200 MB/s |
| NVMe (internal) | 32 Gbps+ | 3-7 GB/s | 200-500 MB/s |

## Key Insight

**Random 4K read speed** matters most for Obsidian plugin loading (many small JS files). USB 2.0 is **100-400x slower** than internal NVMe for this workload.

## Quick Benchmark

```bash
# macOS - test random read
dd if=/Volumes/DRIVE/testfile of=/dev/null bs=4k count=1000 iflag=direct 2>&1 | grep -E "(bytes|MB/s)"

# Or use disk speed test apps: Blackmagic Disk Speed Test, AmorphousDiskMark
```

## Decision Rule

If `Protocol: USB` and `Device Location: External` and drive is **not** USB 3.0+:
- Target plugin load <10 MB
- Move all plugins >1 MB to internal NVMe via symlink
- Uninstall unused plugins

## Verify After Fix

```bash
# Time Obsidian launch
time open -a Obsidian --args /path/to/vault

# Or in Obsidian: Cmd+Opt+I → Network tab → filter "main.js" → check load times
```