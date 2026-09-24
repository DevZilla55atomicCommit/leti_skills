---
name: syncthing-troubleshooting
description: Fixes Syncthing UI by restarting wrapper and UI check.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [syncthing, troubleshooting, desktop]
    category: desktop
---

# Syncthing Troubleshooting Guide (Hermes Environment)

## Symptoms & Diagnosis
- Syncthing web UI not loading at http://127.0.0.1:8384/
- `lsof -i :8384` shows no process listening
- `ps` reveals stale Syncthing processes but no healthy daemon
- Config file `~/Library/Application Support/Syncthing/config.xml` indicates GUI enabled on 127.0.0.1:8384

## Fix Steps
1. **Kill stale processes**
   ```bash
   pkill -9 -f "syncthing" 2>/dev/null; sleep 2
   ```
2. **Restart the wrapper**
   ```bash
   open /Applications/Syncthing.app
   ```
3. **Wait for daemon to start** (≈5 s)
4. **Verify web UI**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8384/
   # Returns 200
   ```
5. **Confirm daemon is running**
   ```bash
   ps aux | grep -i syncthing | grep -v grep
   ```
6. **Check config** (`config.xml`) ensures:
   ```xml
   <gui enabled="true" tls="false">
     <address>127.0.0.1:8384</address>
   </gui>
   ```

## Common Pitfalls
- **Menu‑bar icon missing** – wrapper crashed; simply `open /Applications/Syncthing.app` to restore.
- **Empty capture** – re‑capture after each action; use `capture_after=True` to verify.
- **Element index stale** – re‑capture before clicking; indices are only valid for the current screenshot.
- **Foreground escalation** – when `escalation.recommended: "foreground"` appears, re‑issue the click with `delivery_mode="foreground"` and `bring_to_front=True`.

## Preventive Practices
- Periodically inspect `~/Library/Application Support/Syncthing/log.txt` for recurring “checking existing file: file modified but not rescanned” warnings.
- Use `hermes computer-use doctor` to validate the `computer_use` tool environment if captures consistently fail.
- Keep the wrapper up‑to‑date via `hermes skills install computer-use` to get the latest cua-driver health checks.

## References
- `computer-use` skill: https://hermes-agent.nousresearch.com/docs/computer-use.html
- macOS packaging: `/Applications/Syncthing.app/Contents/Resources/syncthing/syncthing`