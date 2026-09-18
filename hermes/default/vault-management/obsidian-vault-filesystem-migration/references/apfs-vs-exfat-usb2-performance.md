# APFS vs ExFAT on USB 2.0 — Benchmark Results

## Test Environment

- **Mac mini M4** (internal NVMe reference)
- **PNY 128GB USB 2.0 drive** (APFS → ExFAT)
- **Samsung LED ExFAT drive** (reference, USB 3.x)
- macOS built-in `dd` for sequential, shell loop for random I/O

## Sequential Write (100 MB)

| Filesystem | Time | Throughput |
|------------|------|------------|
| APFS (PNY) | 12.07s | **0.87 MB/s** |
| ExFAT (PNY) | 1.62s | **64.3 MB/s** |
| **Speedup** | | **74x** |

## Sequential Read (50 MB, cache purged)

| Filesystem | Time | Throughput |
|------------|------|------------|
| APFS (PNY) | >60s (timeout) | **< 1 MB/s** |
| ExFAT (PNY) | 0.26s | **191 MB/s** |
| **Speedup** | | **>200x** |

## Random I/O (100 × 4 KB)

| Operation | APFS (PNY) | ExFAT (PNY) |
|-----------|------------|-------------|
| Write | 0.15s | 0.15s |
| Read | 0.15s | 0.15s |

**Note**: Random I/O similar — both limited by USB 2.0 latency, not filesystem.

## Methodology

```bash
# Sequential write
dd if=/dev/zero of=/Volumes/DRIVE/test bs=1m count=100

# Sequential read (cache purged)
purge
dd if=/Volumes/DRIVE/test of=/dev/null bs=1m

# Random write
for i in {1..100}; do dd if=/dev/urandom of=/Volumes/DRIVE/rand/file_$i bs=4k count=1; done

# Random read
purge
for i in {1..100}; do dd if=/Volumes/DRIVE/rand/file_$i of=/dev/null bs=4k; done
```

## Why APFS Fails on USB 2.0

APFS assumes fast storage (NVMe). Every operation triggers:
1. Copy-on-write metadata updates
2. Journal writes (sync to disk)
3. Checksum calculations
4. Snapshot reference counting

On USB 2.0 (35 MB/s max), metadata churn saturates bus before data moves.

ExFAT has no journaling, no COW, no snapshots — simple allocation table.

## Obsidian Impact

| Scenario | APFS (USB 2.0) | ExFAT (USB 2.0) |
|----------|----------------|-----------------|
| Vault 327k files | Hang/timeout | Loads in seconds |
| Global search index | Never completes | ~45 min initial |
| Graph view | Hangs | Works on demand |
| File open | Seconds | Instant |