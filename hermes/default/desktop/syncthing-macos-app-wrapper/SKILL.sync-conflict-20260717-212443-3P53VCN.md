---
name: syncthing-macos-app-wrapper
description: Manages the Syncthing macOS .app wrapper for launching, daemon health, and menu‑bar visibility.
title: Syncthing macOS App Wrapper
slug: syncthing-macos-app-wrapper
type: desktop
tags: [syncthing, macos, app, wrapper]
status: stable
trigger: Create, launch, or troubleshoot the official Syncthing .app bundle on macOS.
purpose: Guide users through wrapper installation, menu‑bar visibility, daemon health, and web UI access.
source: Official syncthing-macos package (v2.1.2+)
---

# Syncthing macOS App Wrapper Management

A class‑level workflow for handling the official `syncthing-macos` `.app` bundle (e.g. `/Applications/Syncthing.app`). This skill captures the **full lifecycle**: creation, launch, persistence, menu‑bar visibility, daemon health checks, and web UI access.

## Trigger Conditions
- User asks to “open the app” or “run Syncthing as an app”.
- User reports the wrapper process exited or is not visible in the menu bar.
- User wants to verify the embedded daemon is running or to restart the wrapper.

## Core Steps
1. **Launch the wrapper**  
   ```bash
   open /Applications/Syncthing.app
   ```
2. **Verify the embedded daemon**  
   - Daemon binary: `/Applications/Syncthing.app/Contents/Resources/syncthing/syncthing`  
   - Health check: `curl -s http://127.0.0.1:8384/ | head -5` (expects HTML Syncthing UI)
3. **Menu‑Bar Visibility**  
   - The wrapper is a **menubar‑only** app (`LSUIElement = 1`).  
   - Look for the Syncthing icon in the **top‑right menu bar** (next to Wi‑Fi/Battery).  
   - If missing, relaunch the wrapper; the daemon will continue running.
4. **Restart the wrapper after a crash**  
   - The daemon may survive a wrapper crash; simply `open /Applications/Syncthing.app` again.  
   - To fully reset, kill all Syncthing processes: `pkill -9 -f Syncthing && sleep 2 && open /Applications/Syncthing.app`.
5. **Configuration persistence**  
   - All settings are stored in `~/Library/Application Support/Syncthing-app/`.  
   - Back up this directory for cross‑machine migration.

## Common Pitfalls & Fixes
- **Wrapper crashes but daemon stays alive** – Normal for the wrapper; restart the `.app` to restore the menu‑bar icon.  
- **No menu‑bar icon appears** – Ensure the app is launched from `/Applications`; launching from `~/Downloads` bypasses the embedded `Info.plist` settings.  
- **Web UI unreachable** – Verify the daemon is running (`ps aux | grep syncthing`). If not, launch the wrapper again; the daemon auto‑restarts after a 10 s delay.  
- **User prefers cloud sync** – If the user decides to abandon local setup, wipe the `~/Library/Application Support/Syncthing-app/` directory and use a cloud‑based relay instead.

## Verification Script
```bash
#!/usr/bin/env bash
# syncthing-app-check.sh – runs inside the wrapper’s skill context

# 1. Ensure the wrapper process is alive
if ! pgrep -f "Syncthing.app/Contents/MacOS/Syncthing" > /dev/null; then
  echo "❌ Wrapper crashed – restarting..."
  open /Applications/Syncthing.app
  sleep 3
fi

# 2. Confirm daemon is running
if pgrep -f "syncthing.*syncthing" > /dev/null; then
  echo "✅ Daemon is running"
else
  echo "❌ Daemon stopped – launching wrapper..."
  open /Applications/Syncthing.app
  sleep 5
fi

# 3. Test web UI
if curl -s -o /dev/null http://127.0.0.1:8384/; then
  echo "✅ Web UI reachable"
else
  echo "⚠️ Web UI not responding – check logs"
fi
```

## References
- `references/syncthing-app-launch-log.md` – Full terminal transcript of the launch‑agent crash sequence shown in the session above.
- `references/syncthing-app-troubleshooting-checklist.md` – Condensed checklist derived from user feedback (menu‑bar visibility, wrapper crashes, cloud‑setup preference).