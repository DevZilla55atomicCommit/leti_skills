# Common Space Hogs on Creative/Developer macOS Machines

Based on real-world audits of Apple Silicon Macs used for video editing, AI/ML development, and creative work.

## Tier 1: Massive (10-100+ GB each)

### Ollama Models (`~/.ollama/models/blobs/`)
- **Typical**: 10-50 GB, can exceed 100 GB
- **Structure**: Content-addressed blobs (SHA256), shared across models
- **Management**: `ollama list` → `ollama rm <model>`
- **Note**: Physical disk usage < logical sum due to deduplication
- **Context-variant duplication**: Same base model installed at multiple context sizes (e.g. `qwen3.5-32k/48k/64k/96k/128k`) shows full logical size per variant but shares most blobs — keep 1-2 context sizes actually used, `ollama rm` the rest.
- **Safe removal**: Yes, via `ollama rm` only (don't delete blobs manually)

### Hermes Pre-Update Backups (`~/.hermes/backups/pre-update-*.zip`)
- **Typical**: 7-50 GB each
- **Behavior**: Created automatically before Hermes updates
- **Management**: Keep latest 1-2; delete older via `rm ~/.hermes/backups/pre-update-*.zip`
- **Note**: Full Hermes state backup (skills, profiles, state.db, sessions). Safe to delete old ones if current install works.

### Hermes Emergency State DB Backups (`~/.hermes/state.db.pre-update-emergency-*.bak`)
- **Typical**: 1 GB each (matches state.db size)
- **Behavior**: Created during Hermes updates as safety copies
- **Management**: Keep latest 1; delete older via `rm ~/.hermes/state.db.pre-update-emergency-*.bak`
- **Note**: Exact copies of state.db. Safe to delete if current Hermes works and latest emergency backup exists.

### Hermes Skills Curator Backups (`~/.hermes/skills/.curator_backups/`)
- **Typical**: ~1.1 GB per timestamped `skills.tar.gz`, accumulates weekly
- **Behavior**: Auto-created on skill curation runs (`YYYY-MM-DDTHH-MM-SSZ/skills.tar.gz`)
- **Management**: `du -sh ~/.hermes/skills/.curator_backups/* | sort -hr`; keep latest 1, delete older
- **Note**: Full skills snapshot — safe to prune when current skills load fine.

### LM Studio (`~/.lmstudio/models/`)
- **Typical**: 5-30 GB
- **Structure**: GGUF/MLX models in `lmstudio-community/` subdirs
- **Management**: LM Studio UI → Settings → Models, or delete folder if app uninstalled
- **Orphaned data**: Common — app uninstalled but models remain

### LM Studio Extensions/Backends (`~/.lmstudio/extensions/backends/`)
- **Typical**: 1-3 GB
- **Structure**: Multiple llama.cpp / mlx-llm binary versions in `vendor/` and versioned subdirs
- **Management**: Keep only latest version; delete old `llama.cpp-mac-arm64-*` and `mlx-llm-mac-arm64-*` dirs
- **Note**: Safe to clean if app is uninstalled or you don't use local inference

### Docker VM Disk (`~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw`)
- **Typical**: 20-100 GB
- **Behavior**: Grows dynamically, **never shrinks automatically**
- **Management**: `docker system prune -a --volumes` + restart Docker Desktop
- **Nuclear**: Delete `Docker.raw` → Docker recreates on next start (loses all images/containers)
- **Note**: Sparse file — `ls -la` shows virtual size (up to 500 GB), `du -sh` shows actual usage. If Docker app is uninstalled, the container dir may have a protected `.com.apple.containermanagerd.metadata.plist` that blocks `rm -rf`; the 2.2 GB `Docker.raw` is already gone, only metadata remains (negligible).

### Draw Things Local Models (`~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/`)
- **Typical**: 20-100+ GB (single biggest hog on image-gen Macs)
- **Structure**: Large `.ckpt-tensordata` files plus small `.ckpt` manifests; interrupted downloads leave giant `.partial` files
- **Management**: `du -sh ~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/* | sort -hr`; list incomplete downloads with `ls -lh .../Models/*.partial`
- **Note**: Same model in two quants (e.g. `flux_2_dev_q6p` complete + `flux_2_dev_q8p.partial`) is a duplicate — keep one. `.partial` files are safe to delete when the matching complete quant exists or the download is abandoned.
- **Model roles**: text-only LLMs (e.g. `mistral_*_instruct`) serve prompt-enhancement/chat features, vision models (e.g. `qwen_*_vl`) serve describe-image, diffusion checkpoints + CLIP + VAE serve generation — removing one breaks only its own feature. Confirm which feature the user actually opens the app for before deleting a whole family.
- **Safe removal**: Yes, delete `.partial` files and unneeded quants directly in Finder/terminal; app re-downloads on demand. Sweep orphaned `.partial.map` resume-metadata files after deleting their `.partial` downloads.
- **Hardware fit rules the keep/drop call on unified-memory Macs**: weights larger than RAM (e.g. a 24 GB checkpoint on 16 GB) cannot load without swap-thrash — keep the smaller model regardless of published quality rankings.

### Parallels Windows ISO (`~/Library/Parallels/Downloads/*.iso`)
- **Typical**: 5-10 GB
- **Behavior**: Downloaded by Parallels for Windows VM creation
- **Management**: Delete after VM is created and verified working; move to external if you might reinstall
- **Note**: Safe to delete if Windows VM already set up in Parallels

### Claude Code 3rd Party VM Bundles (`~/Library/Application Support/Claude-3p/vm_bundles/`)
- **Typical**: 8-15 GB
- **Behavior**: Cowork Linux VM (`claudevm.bundle`: `rootfs.img` + kernel + `sessiondata.img`) for sandboxed local-agent-mode runs
- **Management**: Verify stale FIRST — check `sessiondata.img`/`vmIP` mtimes, the `.cowork-adopted` marker, and running app processes. Recent timestamps mean working space, not junk.
- **Note**: Deleting an active VM breaks local-agent-mode until it re-downloads (~1 GB) and re-extracts (~10 GB). Settings, history, and auth live elsewhere and are unaffected.

### Hermes Profile Skills (`~/.hermes/profiles/*/skills/`)
- **Typical**: 6-12 MB per profile (not full 6.9 GB) when skills partially shared/symlinked
- **Behavior**: Each profile gets a copy of shared skills `~/.hermes/skills/` (~6.9 GB)
- **Management**: `rm -rf ~/.hermes/profiles/<name>/skills` for specialized profiles (not `default`)
- **Note**: Actual size varies by install; always audit first with `du -sh ~/.hermes/profiles/*/skills`
- **Safe removal**: Yes, profiles fall back to shared skills automatically

### Time Machine Local Snapshots
- **Typical**: 10-100+ GB (invisible to Finder/du)
- **Check**: `tmutil listlocalsnapshots /`
- **Thin**: `tmutil thinlocalsnapshots / 10000000000 4` (keep 10 GB, max 4)
- **Disable**: `tmutil disablelocal` (not recommended for laptops)

---

## Tier 2: Large (1-10 GB each)

### Hugging Face Cache (`~/.cache/huggingface/`)
- **Typical**: 2-15 GB
- **Structure**: `hub/` (models), `datasets/`, `modules/`
- **Management**: `huggingface-cli delete-cache` or `rm -rf ~/.cache/huggingface`

### uv Package Cache (`~/.cache/uv/`)
- **Typical**: 1-8 GB
- **Management**: `uv cache clean` or `rm -rf ~/.cache/uv`
- **Note**: Not used by Hermes; generic Python tool cache. Safe to clean if no active uv projects (check for `pyproject.toml`/`uv.lock` in dev dirs)

### pip/Poetry Cache (`~/.cache/pip/`, `~/.cache/pypoetry/`)
- **Typical**: 500 MB - 3 GB
- **Management**: `pip cache purge`

### Node/npm/pnpm (`~/.npm/`, `~/.pnpm-store/`, `node_modules/`)
- **Typical**: 1-5 GB global caches; project `node_modules` can be 100 MB - 2 GB each
- **Management**: `npm cache clean --force`, `pnpm store prune`

### Chrome On-Device ML (`~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel/`)
- **Typical**: 1-4 GB
- **Purpose**: Client-side ML for translation, optimization hints
- **Management**: Safe to delete; Chrome re-downloads as needed

### Chrome User Data (`~/Library/Application Support/Google/Chrome/`)
- **Typical**: 3-10 GB
- **Contents**: Profiles, extensions, settings, history, cookies
- **Management**: **Do NOT delete wholesale** — contains user data. Clear via Chrome Settings → Privacy → Clear browsing data. Profile folders (`Profile 1`, `Profile 2`, etc.) can be removed individually if no longer needed.
- **Note**: Separate from `~/Library/Caches/Google/` (HTTP/GPU cache, safe to clear).

### Spotify Offline Cache (`~/Library/Caches/com.spotify.client/`)
- **Typical**: 500 MB - 3 GB
- **Management**: Spotify Settings → Storage → Clear cache

### Telegram Media Cache (`~/Library/Group Containers/6N38VWS5BX.ru.keepcoder.Telegram/appstore/account-*/postbox/media/`)
- **Typical**: 1-6 GB
- **Structure**: `postbox/media/` (re-fetchable media cache) sits next to `postbox/db/` (~30 MB: login, chats — KEEP)
- **Management**: Quit Telegram first, then delete only the `media/` contents — never the `db/` dir or the whole `postbox/`, or the account logs out
- **Note**: Media re-fetches from cloud on scroll. Safe, no re-login needed when `db/` is preserved.

### VS Code / Cursor / Codex (`~/Library/Application Support/Code/`, `~/.codex/`, `~/.cursor/`)
- **Typical**: 500 MB - 3 GB each
- **Management**: Extensions take most space; uninstall unused extensions

---

## Tier 3: Moderate (100 MB - 1 GB)

### DaVinci Resolve Installers (`.dmg`, `.zip` on Desktop/Downloads)
- **Typical**: 5-15 GB each
- **Frequency**: New version every 2-3 months
- **Action**: Delete after verifying install works

### Go Module Cache (`~/go/pkg/mod/`)
- **Typical**: 500 MB - 2 GB
- **Management**: `go clean -modcache`

### Cargo Registry Cache (`~/.cargo/registry/cache/`)
- **Typical**: 200 MB - 1 GB
- **Management**: `cargo clean` (also removes target/ dirs)

### Python `site-packages` in venvs (`~/venv/`, `~/.virtualenvs/`)
- **Typical**: 100 MB - 1 GB per env
- **Management**: Delete unused venvs

### ComfyUI / Comfy Desktop (`~/Library/Application Support/Comfy Desktop/download-cache/`)
- **Typical**: 500 MB - 2 GB
- **Management**: Delete `download-cache/` folder

---

## Tier 4: Hidden/System (often missed)

### Xcode DerivedData (`~/Library/Developer/Xcode/DerivedData/`)
- **Typical**: 2-20 GB
- **Management**: Xcode → Window → Organizer → Archives/DerivedData, or `rm -rf ~/Library/Developer/Xcode/DerivedData/`

### iOS Simulators (`~/Library/Developer/CoreSimulator/Devices/`)
- **Typical**: 5-30 GB
- **Management**: `xcrun simctl delete unavailable` + `xcrun simctl erase all`

### iOS Device Backups (`~/Library/Application Support/MobileSync/Backup/`)
- **Typical**: 5-50 GB
- **Management**: Finder → Manage Backups → Delete old

### Mail Downloads (`~/Library/Containers/com.apple.mail/Data/Library/Mail Downloads/`)
- **Typical**: 100 MB - 2 GB
- **Management**: Safe to delete

### QuickLook Cache (`~/Library/Caches/com.apple.QuickLook.thumbnailcache/`, `~/Library/Caches/com.apple.quicklook.ui.helper/`)
- **Typical**: 100 MB - 1 GB
- **Management**: Safe to delete

---

## Protected: DO NOT DELETE

| Path | Reason |
|------|--------|
| `~/Library/Caches/CloudKit/` | iCloud sync engine |
| `~/Library/Caches/com.apple.Safari/` | Safari browser cache |
| `~/Library/Caches/com.apple.Safari.SafeBrowsing` | Browser integrity |
| `~/Library/Caches/com.apple.findmy.*` | Find My network |
| `~/Library/Caches/com.apple.homed/` | HomeKit |
| `~/Library/Caches/com.apple.containermanagerd/` | App sandbox |
| `~/Library/Caches/com.apple.ap.adprivacyd/` | Ad privacy |
| `~/Library/Keychains/` | Passwords, certificates |
| `~/Library/Application Support/com.apple.TCC/` | Privacy permissions database |
| `~/Library/Preferences/` | App preferences (plists) |

**Result of deleting**: App breakage, permission resets, iCloud sync issues, Keychain corruption.