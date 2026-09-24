# Qualifying an External Drive as App Scratch / Cache

Moving app-owned caches (DaVinci CacheClip, render scratch, build caches) to an
external only helps if the drive is fast enough at the access pattern the app uses.

## Rule: rank scratch drives by sequential WRITE, not read

Caches are write-heavy — the app streams rendered frames/artifacts *to* disk.
A drive with fast reads but slow writes (common on QLC SSDs and ExFAT overhead)
is the worse cache drive. Benchmark both directions with `dd` before assigning:

```bash
# 2 GB sequential write, then read (paths with trailing spaces need quoting!)
dd if=/dev/zero of="/Volumes/<Drive>/.__speedtest" bs=64m count=32 2>&1 | tail -1
rm -f "/Volumes/<Drive>/.__speedtest"
```

## Decision thresholds (DaVinci-grade video work)

| Sequential write | Verdict |
|------------------|---------|
| <60 MB/s | Disqualified for cache — chokes on 4K render streams |
| 60–150 MB/s | OK for proxy/LB/SQ-grade cache and media streams (spinning-HDD territory) |
| 200+ MB/s | Handles full-res HQ cache |

Prefer the roomiest qualified volume, and never assign a drive already >85% full.

## Filesystem and identity checks (macOS)

- `diskutil list` shows the PARTITION TYPE (e.g. `Windows_NTFS`), not the actual
  filesystem — confirm with `diskutil info "/Volumes/<Drive>"` and read
  `File System Personality` (ExFAT vs APFS vs NTFS).
- ExFAT is workable for scratch but has no journaling: eject cleanly before
  unplugging or risk cache corruption. APFS is preferable where reformatting is an option.
- Volume names with trailing spaces (e.g. `/Volumes/Alfred Ext `) are real and
  must be quoted exactly in every command — an unquoted path silently targets nothing.
- Skip USB-topology forensics (`system_profiler`/`ioreg` hub tracing) when a direct
  `dd` benchmark answers the question in seconds — measure, don't trace.
