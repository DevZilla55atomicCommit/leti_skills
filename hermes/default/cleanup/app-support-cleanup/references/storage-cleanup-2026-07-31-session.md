# Storage Cleanup Session - July 31, 2026 (Follow-up)

## Session Context
User requested SSD space cleanup on Mac mini (228 GB internal). Scanned entire user directory and external volumes.

## Key Findings

### 1. Ollama Models - 46 GB (Largest Single Consumer)
**Location**: `~/.ollama/models/blobs/` (46 GB across 30+ blobs)
**Manifests**: `~/.ollama/models/manifests/registry.ollama.ai/library/` (12 models)

| Model | Size | Type | Action |
|-------|------|------|--------|
| x/flux2-klein:4b-fp8 | 9.5 GB | Image Gen | Remove if not generating |
| gemma4:e4b | 9.6 GB | LLM | Keep one variant |
| gemma4:12b | 7.6 GB | LLM | Keep one variant |
| qwen3-vl:8b | 6.1 GB | Vision-Language | Remove if no image analysis |
| minicpm-v4.5:8b | 6.1 GB | Vision-Language | Remove if no image analysis |
| qwen3.5-32k/48k/64k/128k | 6.6 GB each | Long-context LLM | Keep ONE (128k recommended) |
| qwen3.5:4b | 3.4 GB | LLM | Redundant with compressed |
| qwen3.5-4b-compress | 3.4 GB | Compressed LLM | Remove |
| nomic-embed-text | 274 MB | Embeddings | Keep |

**Total reported by `ollama list`**: ~69 GB (blobs show 46 GB due to deduplication)

**Cleanup Strategy**: Use `ollama rm <model>` to properly dereference shared blobs. Removing manifests alone leaves orphaned blobs.

### 2. LM Studio Orphaned Data - 7.8 GB
**Location**: `~/.lmstudio/` (app uninstalled)
**Contents**: `lmstudio-community/gemma-4-E4B-it-MLX-4bit/` (6.4 GB model)
**Also**: `~/Library/Application Support/LM Studio/` (1.8 MB)

**Action**: Safe to `rm -rf ~/.lmstudio` and `rm -rf "~/Library/Application Support/LM Studio"`

### 3. Desktop Video/Installer Files - ~15 GB
| Path | Size | Action |
|------|------|--------|
| `~/Desktop/Media & Design/Gamut Apple Log/DaVinci_Resolve_Studio_20.3_Mac.dmg` | 6.97 GB | **DELETE** (installed in /Applications) |
| `~/Desktop/Media & Design/Gamut Apple Log/DaVinci_Resolve_Studio_20.3_Mac.zip` | 6.96 GB | **DELETE** (duplicate) |
| `~/Desktop/A6700 Tips/Cinematic/C1394.MP4` | 537 MB | Move to external |
| `~/Desktop/Rios Custom LUTS w: Tutorials/Tutorial FULL.mp4` | 388 MB | Move to external |
| `~/Desktop/Rios Custom LUTS w: Tutorials/B-Rolls.mp4` | 83 MB | Move to external |
| `~/Desktop/A6700 Tips/Cinematic/*.crdownload` (2 files) | 41 MB | **DELETE** (incomplete downloads) |

### 4. Chrome On-Device Model Cache - 4 GB
**Location**: `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel/`
**Contents**: `weights.bin` (4 GB) - Chrome's on-device ML model for optimization guide
**Action**: Safe to delete; Chrome will re-download if needed

### 5. Draw Things (iOS App Sandbox) - 6.5 GB
**Location**: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/`
**Models**: sd_xl_turbo_f16.ckpt (4.8 GB), open_clip_vit_bigg14_f16.ckpt (1.3 GB)
**Action**: Manage via Draw Things app UI

### 6. External Drive (Alfred Ext) - 670 GB / 931 GB
**Large folders**: Z_Video_Editing_ASSETS (247 GB), Google Photo Backup (113 GB), San Francisco (100 GB), Backup_Folder (98 GB)
**Action**: Audit for duplicates; consider second backup drive

## Cleanup Commands Executed/Recommended

```bash
# Ollama - remove specific models (properly dereferences blobs)
ollama rm qwen3.5-32k:latest qwen3.5-48k:latest qwen3.5-64k:latest
ollama rm qwen3.5-4b-compress:latest
ollama rm qwen3-vl:8b minicpm-v4.5:8b  # if vision not needed
ollama rm x/flux2-klein:4b-fp8  # if image gen not needed
ollama rm gemma4:e4b  # keep 12b or e4b, not both

# LM Studio orphaned data
rm -rf ~/.lmstudio
rm -rf "~/Library/Application Support/LM Studio"

# Desktop DaVinci installers
rm ~/Desktop/"Media & Design"/"Gamut Apple Log"/DaVinci_Resolve_Studio_20.3_Mac.dmg
rm ~/Desktop/"Media & Design"/"Gamut Apple Log"/DaVinci_Resolve_Studio_20.3_Mac.zip

# Chrome model cache
rm -rf ~/Library/Application\ Support/Google/Chrome/OptGuideOnDeviceModel

# Incomplete downloads
rm ~/Desktop/"A6700 Tips"/Cinematic/*.crdownload
```

## Space Recovery Estimate
| Action | Est. Freed |
|--------|------------|
| Ollama model removal (6-8 models) | 30-45 GB |
| LM Studio orphaned data | 7.8 GB |
| DaVinci installers | 14 GB |
| Chrome OptGuide | 4 GB |
| Incomplete downloads | 41 MB |
| **Total Potential** | **55-70 GB** |

## Verification
```bash
# Before/after comparison
df -h /
du -sh ~/.ollama ~/.lmstudio ~/Desktop/"Media & Design"/"Gamut Apple Log"
```

## Notes for Future Sessions
- Ollama uses content-addressable blobs; `ollama rm` is REQUIRED for space reclamation
- LM Studio data persists after app removal - always check `~/.lmstudio` and `~/Library/Application Support/`
- DaVinci Resolve installers on Desktop are common space wasters after updates
- Chrome's OptGuideOnDeviceModel is safe to delete (auto-regenerates)
- External drive (Alfred Ext) at 72% capacity - plan for second backup drive