# macOS Trash Management

## Locations

| Trash Location | Path | Notes |
|----------------|------|-------|
| Main user trash | `~/.Trash/` | User's primary trash |
| External volume trash | `/Volumes/<VolumeName>/.Trashes/<UID>/` | Per-volume, per-user (UID = `id -u`) |
| Time Machine local snapshots | (hidden) | Managed via `tmutil`, not visible in Finder Trash |

## Permission Issues (TCC)

macOS TCC (Transparency, Consent, and Control) blocks **listing** `.Trashes` directories even for the owner:

```bash
ls -la ~/.Trash/          # "Operation not permitted"
ls -la /Volumes/External/.Trashes/501/  # "Operation not permitted"
```

**This is normal** — the directories exist and can be written to, but `ls` is blocked.

## Emptying Trash

### Preferred: Finder AppleScript (works without FDA)
```bash
osascript -e 'tell application "Finder" to empty the trash'
```
Run with a long foreground timeout (up to 600s) — file-count-heavy folders take minutes. Never run two empties concurrently; the second fails with `-15260 Finder busy`.

### Direct rm (requires Full Disk Access for the calling app)
```bash
rm -rf ~/.Trash/*
```
`sudo` does NOT bypass TCC — the fix is System Settings → Privacy & Security → Full Disk Access → enable the calling app (e.g. Hermes), then quit and relaunch it. Without FDA, both `ls` and `rm` on `~/.Trash` and `/Volumes/*/.Trashes/` fail with `Operation not permitted` even as owner, even under sudo.

### External volume trash (also needs FDA, not just sudo)
```bash
id -u  # e.g., 501
rm -rf "/Volumes/Volume Name/.Trashes/501/"*
```

### Force-Empty via Finder (GUI)
- **Cmd+Shift+Delete** in Finder → Empty Trash
- **Option+right-click Finder icon → Relaunch** if Finder caches stale state

## Verification

After emptying, verify with `find` (not `ls`):
```bash
# Main trash
find ~/.Trash -type f 2>/dev/null

# External volume trash
find "/Volumes/Volume Name/.Trashes/501/" -type f 2>/dev/null
```

Empty output = trash is clear. Prefer `osascript -e 'tell application "Finder" to count items of trash'` for verification since it needs no FDA. Direct `find` on Trash paths needs the same FDA grant as `rm`; without it, use the Finder count instead of `sudo find`.

## Common Pitfalls

1. **`Operation not permitted` on `ls`/`rm`** → TCC protection on the calling app, not a sudo problem — grant it Full Disk Access and relaunch it, since even sudo stays blocked without FDA.
2. **Finder shows items after terminal clear** → Finder cache. Relaunch Finder (`killall Finder`, which also recovers a wedged empty) or use Cmd+Shift+Delete.
3. **Multiple volumes** → Each mounted volume has its own `.Trashes`. Check all: `ls /Volumes/*/.Trashes/ 2>/dev/null`
4. **Verify the live copy before deleting a trashed vault/folder copy** — confirm the production path (e.g. `ls -ld /Volumes/...`) is intact and distinct from the trashed copy before emptying, since empty is irreversible.
5. **File-count-heavy folders defeat Finder enumeration** — when Finder returns `missing value` for size or `-1728` on POSIX path for a trashed folder, it cannot list contents (typically 100K+ small files); expect `-10000 AppleEvent handler failed` on empty and switch to direct `rm` with FDA instead of retrying Finder.
6. **Never run concurrent empties** — a second `empty the trash` while one is running fails with `-15260 Finder busy` and can wedge Finder; `killall Finder` recovers it.
7. **`-47 file in use`** → a trashed file is held open (preview/thumbnail/indexer); close owning apps and retry rather than forcing.

## Quick One-Liner: Empty All Trashes
```bash
rm -rf ~/.Trash/* && for v in /Volumes/*/; do [ -d "${v}.Trashes/$(id -u)" ] && sudo rm -rf "${v}.Trashes/$(id -u)"/*; done
```