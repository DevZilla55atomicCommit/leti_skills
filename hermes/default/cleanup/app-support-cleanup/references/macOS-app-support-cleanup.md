---
title: macOS App Support Cleanup Reference
tags: [reference, cleanup, app-support]
owner: user
created: 2026-07-13
---

# macOS App Support Cleanup Reference

## Target Folders & Sizes (As of 2026-07-13)

| Folder | Typical Size | Last Modified | Safety Note |
|--------|--------------|---------------|-------------|
| `Claude-3p` | 6.9 GB | 2026-07-12 | ✅ Safe to delete if not using Claude Desktop GUI |
| `Google` | 6.1 GB | 2026-07-12 | ✅ Safe to clear (Chrome/Drive caches) |
| `com.docker.install` | 2.1 GB | 2026-07-10 | ✅ Safe (old installer artifacts) |
| `Code` (VS Code) | 1.4 GB | 2026-07-11 | ✅ Safe (caches only) |
| `Wondershare Filmora` | 487 MB | 2026-07-09 | ✅ Safe (temp files) |
| `ON1` | 485 MB | 2026-07-08 | ✅ Safe (previews) |
| `Blackmagic Design` | 1.8 GB | 2026-07-07 | ❌ **DO NOT DELETE** if using DaVinci Resolve |
| `Adobe` | 808 MB | 2026-07-06 | ✅ Keep if using Adobe apps |

## Safety Protocol

1. **Backup First**  
   ```bash
   cp -r ~/Library/Application\ Support/[FOLDER] ~/Desktop/[FOLDER]_backup_$(date +%Y%m%d)
   ```

2. **Verify Size**  
   ```bash
   du -sh ~/Library/Application\ Support/[FOLDER]
   ```

3. **Check Critical Dependencies**  
   - Blackmagic Design = DaVinci Resolve  
   - Adobe = Premiere/After Effects  
   - `com.apple.*` = System-managed  

4. **Delete**  
   ```bash
   rm -rf ~/Library/Application\ Support/[FOLDER]
   ```

## Verification Checklist

- Compare `du -sh` before/after.  
- Confirm apps launch without errors.  
- No missing data in critical apps.