# Vault Storage Optimization Workflow

## Issue
Large GIF collection in `Instagram_Reels/Photography/Videography/` consuming ~14 GB.

## Steps
1. **Identify**: Use `du -sh` to locate large GIF files.
2. **Move**: Transfer the `Videography` folder to external storage (e.g., `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Instagram_Reels/Photography/Videography`) and create a symlink in the original location.
3. **Compress** (optional): Run `gifsicle --optimize=3 --lossy=80%` on individual GIFs to reduce size by up to 80%.
4. **Archive**: For long‑term storage, copy processed GIFs to `media/archived/` and generate `README.md` index.
5. **Cleanup**: Remove original uncompressed GIFs after confirming successful move/compression.

## References
- `references/vault-storage-optimization.md` (this file)
- `vault-restructure` skill for general vault cleanup procedures.