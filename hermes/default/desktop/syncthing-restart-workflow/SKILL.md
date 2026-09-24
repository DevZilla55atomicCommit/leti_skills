---
name: syncthing-restart-workflow
description: Restart Syncthing on macOS when Web UI is unresponsive.
category: desktop
tags:
  - syncthing
  - troubleshooting
  - macos
---

# Syncthing Restart Workflow

**Trigger:** Syncthing Web UI unresponsive or Syncthing daemon not running.

## Steps
1. `pkill -9 -f "syncthing" 2>/dev/null; sleep 2`
2. `open /Applications/Syncthing.app`
3. `sleep 5`
4. `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8384/` (should be 200)

## Verification
- UI returns HTTP 200 on port 8384.
- Menu‑bar icon reappears if it was missing.

## Pitfalls
- Wrapper may crash; re‑run `open /Applications/Syncthing.app`.
- Ensure `~/Library/Application Support/Syncthing/config.xml` has `<gui enabled="true"...>`.
- Check `syncthing.log` for errors.