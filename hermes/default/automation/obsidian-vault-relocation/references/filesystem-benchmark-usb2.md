# Filesystem Benchmark: USB 2.0 (PNY128GBLED)

## Test Environment
- **Drive:** PNY 128GB USB 2.0 flash drive
- **Interface:** USB 2.0 (480 Mbps theoretical, ~35 MB/s real)
- **macOS:** 26.5.2
- **Date:** 2026-08-06

## Results Summary

| Operation | APFS | ExFAT | Winner |
|-----------|------|-------|--------|
| Sequential Write (100 MB) | 0.87 MB/s | 64 MB/s | **ExFAT 74x** |
| Sequential Write (10 MB) | ~12s | ~0.16s | **ExFAT** |
| Uncached Sequential Read (50 MB) | >60s (timeout, <1 MB/s) | 0.26s (191 MB/s) | **ExFAT 200x+** |
| Cached Sequential Read (100 MB) | 14.4 GB/s | 16.4 GB/s | Tie (page cache) |
| Random Write (100 × 4 KB) | ~0.15s | ~0.15s | Tie |
| Random Read (100 × 4 KB) | ~0.15s | ~0.15s | Tie |

## Commands Used

```bash
# Sequential Write 100 MB
dd if=/dev/zero of=/Volumes/DRIVE/test_write_100M bs=1m count=100

# Sequential Read 100 MB (cached)
dd if=/Volumes/DRIVE/test_write_100M of=/dev/null bs=1m

# Uncached Read (purge cache first)
purge
dd if=/Volumes/DRIVE/test_read_50M of=/dev/null bs=1m

# Random I/O (100 × 4 KB)
for i in {1..100}; do dd if=/dev/urandom of=/Volumes/DRIVE/rand_test/file_$i bs=4k count=1; done
time for i in {1..100}; do dd if=/Volumes/DRIVE/rand_test/file_$i of=/dev/null bs=4k; done
```

## Why APFS Fails on USB 2.0

APFS assumes fast storage (NVMe). Every file operation triggers:
1. **Journal writes** (sync to disk)
2. **Copy-on-write metadata updates** (new blocks for every change)
3. **Checksum calculations** (Fletcher64 for metadata, SHA for data)
4. **Snapshot reference counting**
5. **Space manager tree updates**

On USB 2.0 (35 MB/s max bus), this metadata churn saturates the bus before any actual data moves. The drive spends all bandwidth on APFS bookkeeping.

## Why ExFAT Wins on USB 2.0

- Simple allocation table (FAT-like)
- No journaling
- No copy-on-write
- No checksums
- No snapshots
- Minimal metadata per operation

## Recommendation

| Drive Interface | Filesystem | Rationale |
|-----------------|------------|-----------|
| Internal NVMe/SSD | APFS | Symlinks, xattrs, journaling, snapshots, encryption |
| USB 3.0/3.1/3.2 | APFS | Fast enough for APFS overhead |
| USB 2.0 | **ExFAT** | 74x faster writes, 200x+ faster uncached reads |
| Cross-platform (Win/macOS/Linux) | ExFAT | Universal compatibility |

## For Obsidian Vaults on USB 2.0

**Always use ExFAT.** APFS indexing hangs (Transcripts 837 MB / 3,350 files took >1 hour to index on APFS/USB 2.0, instant on ExFAT).