# External SSD Output Configuration

## Path: `/Volumes/Samsung LED/Instagram Downloads/`

### Directory Structure
```
/Volumes/Samsung LED/
├── Instagram Downloads/          # ← yt-dlp output here
├── 1. Official LUTs/
├── 2025_LutPack/
├── Davinci_Backup_Cache/
├── Gamut Immersion Extra Content/
├── Gamut-Apple-Log-BaseLUTs/
├── Log_footages_colorgrding/
├── Music/
├── Node Tree - Gamut Powergrade/
├── Pratice/
└── TEST FOOTAGE by @dannygan_colorist/
```

### yt-dlp Output Path
```bash
-o "/Volumes/Samsung LED/Instagram Downloads/%(id)s.%(ext)s"
```

### Space Savings
- **Mac Mini SSD preserved**: ~10-15 GB for 205 Reels
- **External SSD**: Samsung LED (confirmed mounted, writable, empty)

### Verification
```bash
# Check mount
ls -la "/Volumes/Samsung LED/Instagram Downloads/"

# Check space
df -h "/Volumes/Samsung LED/"
```

### Notes
- Path contains space → must quote in bash
- macOS auto-mounts at `/Volumes/<volume-name>/`
- Ensure drive stays mounted during batch run