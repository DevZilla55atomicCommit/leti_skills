# External Vault Migration Reference

**Source Session:** 20260802_145610_5bc076 (vault scan → PNY128GBLED transfer plan)

## Problem Class
Moving a large Obsidian vault (10–30 GB) from internal NVMe to external USB storage while preserving:
- Obsidian plugin functionality (symlinks, extended attributes, case sensitivity)
- Git/history integrity
- Tooling/scripts that rely on absolute or relative paths
- Performance for active editing vs. archival access

---

## Critical Format Requirement

**External drive MUST be APFS (not FAT32/exFAT/NTFS).**

| Filesystem | Verdict | Reason |
|------------|---------|--------|
| **APFS** | ✅ Required | Journaling, symlinks, xattrs, clones, snapshots, case-sensitive option |
| FAT32 | ❌ Blocked | 4 GB file limit, no journaling, no symlinks, no xattrs, case-insensitive |
| exFAT | ⚠️ Marginal | No journaling, no symlinks, no xattrs — corruption risk on disconnect |
| NTFS | ❌ Blocked | Read-only on macOS without third-party drivers |

**Command:**
```bash
diskutil eraseDisk APFS "VOLUME_NAME" /dev/diskX
```

---

## Vault Composition Analysis (Diagnostic)

Run before any migration to size the problem:

```bash
# Total vault size
du -sh "/path/to/vault"

# Top-level breakdown
du -sh "/path/to/vault/"*/ 2>/dev/null | sort -hr

# Deep breakdown of largest dir
du -sh "/path/to/vault/LargestDir/"*/ 2>/dev/null | sort -hr

# Count regeneratable assets (frames, transcripts, generated media)
find "/path/to/vault" -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" -o -name "*.mp4" -o -name "*.wav" \) | wc -l
```

---

## Migration Classification

| Category | Action | Examples from Session |
|----------|--------|----------------------|
| **Core Vault (MOVE)** | Move to external, symlink from original path | `00 Human/`, `Machine/`, `System/`, `.obsidian/`, curated markdown KB |
| **Curated Knowledge (MOVE)** | Move — high-value, non-regeneratable | DaVinci skills, techniques, color grading docs, node structures |
| **Regeneratable Bulk (RE-EVALUATE)** | Leave on internal OR move to `_regeneratable/` on external | Instagram Reels frames (14 GB), Transcripts w/ audio (837 MB), AI-generated images (48 MB) |
| **Build Artifacts (SKIP)** | Exclude — `npm install` / pipeline rebuild | `node_modules/`, `graphify-out/`, cache folders |
| **Active Media (SKIP)** | Keep on fast internal NVMe | Project source clips, active render caches |

---

## Recommended External Layout

```
/Volumes/EXTERNAL_DRIVE/
├── VaultName/                    ← Main vault (opened directly in Obsidian)
│   ├── 00 Human/
│   ├── Machine/
│   ├── System/
│   ├── .obsidian/
│   ├── CuratedKB/                ← DaVinci skills, techniques, etc.
│   └── ...lightweight folders
└── _regeneratable/               ← Optional: bulk assets, symlinked into vault
    ├── Instagram_Reels_frames/
    ├── Transcripts_audio/
    └── Generated_Images/
```

---

## Symlink Strategy (Path Stability)

```bash
# After moving vault to external:
ln -s "/Volumes/EXTERNAL_DRIVE/VaultName" ~/VaultName
# OR open external path directly in Obsidian (no symlink needed)

# For regeneratable bulk (if kept on internal but referenced from vault):
ln -s "/Users/you/Regeneratable/Instagram_Reels_frames" "/Volumes/EXTERNAL_DRIVE/VaultName/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels/Photography/Videography/_frames"
```

---

## Pre-Migration Cleanup Commands

```bash
# 1. Remove node_modules (regeneratable)
rm -rf "/path/to/vault/emai-dashboard/node_modules"

# 2. Remove frame directories (regeneratable from reel URLs)
# rm -rf "/path/to/vault/.../Instagram_Reels/.../*_frames/"

# 3. Remove transcript audio (keep .txt/.json)
# find "/path/to/vault/.../Transcripts/" -name "*.wav" -delete

# 4. Remove generated images
# rm -rf "/path/to/vault/Hermes Agent/Hermes Image Generates/"

# 5. Remove graph exports
# rm -rf "/path/to/vault/graphify-out/"
```

---

## Verification Checklist (Post-Migration)

- [ ] `df -h /` shows internal space freed by expected amount
- [ ] Obsidian opens vault from external path without plugin errors
- [ ] `ls -la ~/VaultName` confirms symlink resolves correctly
- [ ] Git status works inside vault (no "too many open files" or permission errors)
- [ ] DaVinci/other tooling that references vault paths still resolves
- [ ] External drive auto-mounts on login (check Login Items or launchd)
- [ ] Backup strategy in place (Time Machine excludes external, or separate backup)

---

## Pitfalls Encountered

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| FAT32 format | Silent corruption, 4 GB limit, symlink failures | Reformat to APFS **before** any data copy |
| Moving `node_modules` | 50 MB+ waste, permission errors on external | Always exclude; `npm install` after move |
| Moving active render cache | DaVinci Resolve slow/laggy | Keep CacheClip on internal NVMe (use `external-cache-migration` skill) |
| No journaling (exFAT/FAT32) | Vault corruption after cable pull | APFS only |
| Symlink broken after reboot | "Vault not found" in Obsidian | Ensure external drive mounts before Obsidian launches; add to Login Items |
| Case-insensitive FS | Git sees duplicate files (README.md vs readme.md) | APFS case-sensitive or standard (standard works for most) |

---

## Integration with Other Skills

- **`external-cache-migration`** — Use for DaVinci Resolve CacheClip, HyperDictionary, etc. (separate from vault migration)
- **`vault-setup`** — Run `/start` and `/interview` after migration to verify vault health
- **`vault-optimize`** — Daily ops (`/today`, `/closeday`) unchanged; paths stable via symlink