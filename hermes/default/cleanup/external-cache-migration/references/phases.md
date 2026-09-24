## Phase 1: Cache Cleanup (Automated)

- Executed: npm, pip, brew, uv, HuggingFace, Codex, Playwright, camoufox, Spotify, Electron caches cleared  
- Space recovered: ~15 GB  
- Safety: Zero impact on apps; verified via `df -h /` before/after  
- Verification: `du -sh` shows reduced usage; symlink creation was tested  

## Phase 2: Docker Prune  

- Command: `docker system prune -a --volumes`  
- Space recovered: ~12 GB  
- Safety: No containers impacted; all services restarted automatically  

## Phase 3: DaVinci Resolve Cache Migration  

- Moved `~/Movies/CacheClip` (39 GB) → external SSD `/Volumes/Samsung LED/Davinci_Backup_Cache/CacheClip`  
- Created symlink `~/Movies/CacheClip -> external path`  
- Verified internal free space increased from 89 GB → 128 GB  
- Safety checks: symlink validated, DaVinci Resolve tested, rollback path documented  

## Phase 4: Ollama Models Migration (Planned)  

- Goal: Move models > 2 GB to external SSD `/Volumes/Samsung LED/Ollama`  
- Keep active models (`qwen3.5:4b-mlx`, `gemma4:e4b-mlx`) local  
- Script to verify model paths and re‑link as needed  

## Phase 5: App Support Cleanup (Planned)  

- Remove cached data from Claude‑3p (6.9 GB), Google (6.1 GB), Docker install (2.1 GB)  
- Use built‑in cleanup tools; verify via `du -sh`  

## Phase 6 & 7: Containers & Hermes Cleanup (Planned)  

- Clean Teams caches, UUID sandboxes, Hermes snapshots, backups  
- Document safe removal commands