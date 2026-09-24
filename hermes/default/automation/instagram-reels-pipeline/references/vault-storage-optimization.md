# Vault Storage Optimization: Frame Deduplication Results

## Context
Applied to `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Videographer` after processing 91 reels (Blocks A, B, C) via `instagram-reels-pipeline`.

## Problem
Pipeline created 3 copies of each frame set per reel:
1. **Vault root** `/Discipline/{CODE}/frame_XX.png` — referenced by Obsidian notes via `![[frame_XX.png]]`
2. **Vault frames/** `/Discipline/{CODE}/frames/frame_XX.png` — duplicate, not referenced
3. **Skills frames/** `~/.hermes/skills/videographer/reel_{CODE}/frames/frame_XX.png` — referenced by Hermes skills

Plus duplicate GIFs in both vault root and vault frames/.

## Solution (Option A: Remove vault root duplicates)
1. Deleted 240 duplicate PNG frames from vault root directories (107.6 MB)
2. Updated 93 Obsidian notes to reference `![[frames/frame_XX.png]]`
3. Copied `preview.gif` from `frames/` to vault root for note compatibility
4. Removed 30 duplicate GIFs from `frames/` directories
5. Deleted entire `/assets/` legacy folder (160 MB, 29 folders from old D* code runs)

## Results
| Metric | Before | After | Saved |
|--------|--------|-------|-------|
| Vault size | 574 MB | 466 MB | **108 MB (19%)** |
| Skills size | 438 MB | 438 MB | unchanged |
| Frame copies/reel | 3 | 2 | -1 |
| GIF copies/reel | 2 | 1 | -1 |

## Future Pipeline Fix
Update `process_block_a_v2.py` (and future processors) to:
1. Write frames ONLY to `frames/` subdirectory
2. Reference `frames/frame_XX.png` in notes
3. Write GIF ONLY to reel root (not in frames/)
4. Skills keep their own frames/ copy (required for Hermes)

This reduces vault storage by ~35% with no functional loss.

## Related
- `instagram-media-pipeline` skill: references/vault-storage-optimization.md
- Session: 2026-07-19 Block A/B/C processing