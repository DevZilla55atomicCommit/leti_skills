# CapCut Cache Locations (macOS)

## Safe Directories to Delete

| Path | Description |
|------|-------------|
| `~/Library/Application Support/CapCut/User Data/Cache/*` | Main cache folder storing extracted assets, temporary video buffers, and preview files |
| `~/Library/Caches/com.capcut.Cut` | Legacy cache location for older CapCut versions |
| `~/Library/Containers/com.capcut.Cut/Data/Library/Caches/*` | Containerized cache (if present) |

## Commands

```bash
# Primary cleanup
rm -rf "/Users/$USER/Library/Application Support/CapCut/User Data/Cache/*"

# Alternate location
rm -rf "/Users/$USER/Library/Caches/com.capcut.Cut"
```

## Verification

1. Check available space: `df -h /`
2. Relaunch CapCut; it will automatically rebuild caches as needed

## Pitfalls

- **Do not delete the container itself** (`com.capcut.Cut`) — only its internal `Cache` subfolders
- macOS may block deletion with "Operation not permitted" — ignore for user caches
- After cleanup, CapCut may temporarily be sluggish while caches rebuild

## References

- Verified on macOS Sonoma 14.5 with CapCut 1.3.X