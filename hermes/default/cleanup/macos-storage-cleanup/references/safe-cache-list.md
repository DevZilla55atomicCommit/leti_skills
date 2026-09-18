# Safe vs Protected Caches on macOS

## ✅ SAFE TO DELETE — Apps Will Rebuild Automatically

### User Application Caches (`~/Library/Caches/`)
- `com.spotify.client` — Spotify offline playback cache
- `com.google.Chrome` / `com.google.Chrome.*` — Chrome HTTP cache, GPU cache, shader cache
- `com.microsoft.VSCode` / `com.microsoft.VSCode.*` — VS Code extension host cache
- `com.electron.*` — Generic Electron app caches
- `com.blackmagic-design.DaVinciResolve` — Resolve render cache (can be large)
- `com.apple.python` — pip/pipx build caches
- `com.apple.dt.Xcode` — Xcode derived data (safe but Xcode rebuilds slowly)
- `pip` / `pipx` / `uv` / `poetry` — Python package caches
- `node-gyp` / `npm` / `pnpm` / `yarn` — Node build caches
- `go-build` — Go build cache
- `cargo` — Rust build cache
- `comfyui-desktop-*` — ComfyUI model download cache
- `electron-builder` — Electron app update caches

### User Dot-Caches (`~/.cache/`)
- `uv/` — uv package cache (very aggressive, safe to nuke)
- `pip/` — pip wheel cache
- `huggingface/` — HF Hub model/dataset cache
- `torch/` — PyTorch compiled kernels, downloaded weights
- `mlx/` — Apple MLX compiled kernels
- `codex-runtimes/` — Codex agent runtime images
- `codex/` — Codex auth, config cache
- `pre-commit/` — pre-commit hook cache
- `ruff/` — Ruff linter cache
- `mypy/` — MyPy cache
- `pytest/` — pytest cache

### Application Support — Cache-Like Subdirs
- `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel/` — Chrome on-device ML models
- `~/Library/Application Support/Google/Chrome/component_crx_cache/` — Extension CRX cache
- `~/Library/Application Support/Comfy Desktop/download-cache/` — ComfyUI model downloads
- `~/Library/Application Support/Claude/` — Claude app cache (safe)
- `~/Library/Application Support/Claude-3p/vm_bundles/` — **Claude Code disposable VM bundles (safe, very large)**
- `~/Library/Application Support/Code/CachedData/` — VS Code cached extension data
- `~/Library/Application Support/Codex/runtimes/` — Codex runtimes

---

## ❌ PROTECTED / DO NOT DELETE — macOS Will Block or Break Things

### CloudKit & iCloud Sync
- `~/Library/Caches/CloudKit/` — Core iCloud sync engine
- `~/Library/Caches/com.apple.clouddocs/` — iCloud Drive
- `~/Library/Caches/com.apple.bird/` — Backup/Restore daemon
- `~/Library/Caches/com.apple.CloudPhotosConfiguration/` — Photos sync

### Safari & WebKit
- `~/Library/Caches/com.apple.Safari/` — Safari cache, history, cookies
- `~/Library/Caches/com.apple.WebKit.*` — WebKit framework caches
- `~/Library/Caches/com.apple.SafariSafeBrowsing/` — Safe Browsing lists

### Find My & Location
- `~/Library/Caches/com.apple.findmy.*` — Find My network
- `~/Library/Caches/com.apple.geod/` — Geolocation daemon
- `~/Library/Caches/com.apple.locationd.*` — Location services

### HomeKit & Accessories
- `~/Library/Caches/com.apple.homed/` — HomeKit daemon
- `~/Library/Caches/com.apple.homekit.*` — HomeKit frameworks

### Apple Services & Identity
- `~/Library/Caches/com.apple.accountsd/` — Apple ID / iCloud auth
- `~/Library/Caches/com.apple.ids.*` — Identity services
- `~/Library/Caches/com.apple.ap.adprivacyd/` — Ad privacy daemon
- `~/Library/Caches/com.apple.assistantd/` — Siri/Assistant
- `~/Library/Caches/com.apple.assistant.*` — Siri caches
- `~/Library/Caches/com.apple.siri.*` — Siri caches

### Media & Entertainment
- `~/Library/Caches/com.apple.MediaLibraryService/` — Media library
- `~/Library/Caches/com.apple.AMPArtworkAgent/` — Apple Music artwork
- `~/Library/Caches/com.apple.iTunesCloud/` — iTunes Match/iCloud Music Library
- `~/Library/Caches/com.apple.appstoreagent/` — App Store agent
- `~/Library/Caches/com.apple.storekitagent/` — StoreKit (in-app purchases)

### System Frameworks
- `~/Library/Caches/com.apple.parsecd/` — Parsed content (Spotlight, etc.)
- `~/Library/Caches/com.apple.helpd/` — Help viewer
- `~/Library/Caches/com.apple.metadata.*` — Spotlight metadata
- `~/Library/Caches/com.apple.quicklook.*` — QuickLook thumbnails

---

## ⚠️ CAUTION — Delete With Care

### Application Support (Not Caches)
- `~/Library/Application Support/Code/User/` — VS Code settings, keybindings, snippets
- `~/Library/Application Support/Claude/conversations/` — Claude chat history
- `~/Library/Application Support/obsidian/` — Obsidian vault config (vaults elsewhere)
- `~/Library/Application Support/Spotify/Users/*/prefs` — Spotify preferences
- `~/Library/Application Support/Docker/` — Docker Desktop settings (not the VM disk)

### Containers (Sandboxed App Data)
- `~/Library/Containers/com.apple.*` — System apps (Mail, Messages, Photos, etc.)
- `~/Library/Containers/com.microsoft.Outlook` — Outlook data (use app to manage)
- `~/Library/Containers/com.microsoft.Word` — Word data
- `~/Library/Containers/com.liuliu.draw-things` — Draw Things models (if you use it)

### Keychains & Security
- `~/Library/Keychains/` — **Never delete** — passwords, certs, keys
- `~/Library/Certificates/` — Identity certificates

---

## Quick Test: Is It Safe?
```bash
# Try to delete - if "Operation not permitted", it's protected
rm -rf ~/Library/Caches/com.apple.Safari  # Will fail = protected
rm -rf ~/Library/Caches/com.spotify.client  # Works = safe
```

## Rule of Thumb
- **`~/Library/Caches/com.apple.*`** → Mostly protected, skip
- **`~/Library/Caches/com.<vendor>.*`** → Usually safe (Spotify, Google, Microsoft, etc.)
- **`~/.cache/*`** → Always safe
- **`~/Library/Application Support/*/Cache*/` or `*Cache*`** → Usually safe
- **`~/Library/Containers/com.apple.*`** → Protected
- **`~/Library/Containers/com.<vendor>.*`** → App-specific, check if you use the app