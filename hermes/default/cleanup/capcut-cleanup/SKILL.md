---
name: capcut-cleanup
description: Clean up CapCut caches safely on macOS
category: cleanup
version: 1.0.0
---

# CapCut Cache Cleanup

A focused cleanup skill for removing CapCut's cached media files to reclaim disk space on macOS.

## When to Use
- After heavy video editing sessions
- Before exporting large projects
- Regular maintenance to prevent storage bloat

## Safe Cache Locations
```bash
# Core CapCut cache directories
rm -rf "/Users/$(whoami)/Library/Application Support/CapCut/User Data/Cache"/*

# Alternative paths (if installed in different locations)
rm -rf "/Users/$(whoami)/Library/Caches/com.capcut.Cut"
```

## Verification
1. Check free space: `df -h /`
2. Launch CapCut to confirm it rebuilds caches automatically
3. No critical errors on startup

## Pitfalls
- Do NOT delete `com.capcut.Cut` container itself — only its internal caches
- macOS may re-protect some folders; ignore "Operation not permitted" for user caches