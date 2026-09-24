# Vault Migration to Faster Drive (ExFAT on USB 2.0)

## When to Use
- Current vault on APFS/HFS+ on USB 2.0
- ExFAT-formatted USB drive available (e.g., Samsung LED)
- Want to keep vault on external but need better performance

## Migration Workflow

### 1. Verify Target Drive is ExFAT
```bash
diskutil info /Volumes/TARGET_DRIVE | grep "File System"
# Should output: File System Personality: ExFAT
```

### 2. Benchmark Both Drives (Optional but Recommended)
```bash
# Sequential write test
dd if=/dev/zero of="/Volumes/SOURCE/test_100M" bs=1m count=100
dd if=/dev/zero of="/Volumes/TARGET/test_100M" bs=1m count=100

# Sequential read test (cache purged)
purge
dd if="/Volumes/SOURCE/test_100M" of=/dev/null bs=1m
purge
dd if="/Volumes/TARGET/test_100M" of=/dev/null bs=1m
```

### 3. Migrate Vault
```bash
# Copy vault (preserves symlinks, metadata)
rsync -avh --progress "/Volumes/SOURCE/Vault Name/" "/Volumes/TARGET/Vault Name/"

# Or use Finder drag-and-drop (holds Option key to copy, not move)
```

### 4. Verify Symlinks Still Work
```bash
# Check all plugin symlinks
ls -la "/Volumes/TARGET/Vault Name/.obsidian/plugins/" | grep "->"

# Verify each symlink target exists
ls -la "/Volumes/TARGET/Vault Name/.obsidian/plugins/PLUGIN_NAME/"
```

### 5. Test Obsidian Startup
```bash
# Time startup
time open -a "Obsidian" --args "/Volumes/TARGET/Vault Name"
```

### 6. (Optional) Reformat Source Drive to ExFAT
```bash
# WARNING: DESTROYS ALL DATA ON SOURCE DRIVE
diskutil eraseDisk ExFAT "SOURCE_DRIVE" /dev/diskX
```

## Test Results (This Session)
| Metric | Samsung LED (ExFAT) | PNY128GBLED (APFS) |
|--------|---------------------|---------------------|
| Sequential Write | 64.3 MB/s | 0.87 MB/s |
| Uncached Read (50 MB) | 0.26s | >60s (timeout) |
| Random I/O (100 × 4 KB) | ~0.15s | ~0.15s |

## Key Insight
**APFS on USB 2.0 is fundamentally broken for write-heavy workloads** due to journaling + copy-on-write + metadata overhead. ExFAT's simple allocation table avoids all of this.

## Notes
- Obsidian doesn't respect `.stignore` (Syncthing only) — use actual folder moves for archiving
- Keep vault on ExFAT drive; only plugin symlinks need NVMe
- After migration, verify Graph view and search work (index rebuild may be needed)