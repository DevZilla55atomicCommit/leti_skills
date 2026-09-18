---
name: macos-launch-agent-management
title: macOS Launch Agent Management
category: devops
description: Managing background services via Launch Agents on macOS.
---

# macOS Launch Agent Management

This skill captures the workflow for managing background services (Launch Agents) on macOS, including starting, stopping, debugging, and monitoring.

## Triggers
- Need to start/stop a service defined as a Launch Agent
- Want to inspect logs or status
- Encountering lock or startup errors

## Core Workflow
1. **List**: `launchctl list | grep <label>`
2. **Stop**: `launchctl bootout gui/$(id -u) <plist_path>` or `pkill -9 -f "<process_name>"`
3. **Unload**: `launchctl unload <plist_path>`
4. **Start**: `launchctl bootstrap gui/$(id -u) <plist_path>` or use `open` to launch GUI
5. **View Logs**: `tail -f ~/Library/Logs/<service>.log` and `tail -f ~/Library/Logs/<service>-Errors.log`
6. **Web UI**: Open `http://localhost:8384` for Syncthing, or service-specific UI

## Common Pitfalls
- **Lock acquisition errors**: Another instance may be running; use `pkill` to stop hidden processes.
- **Plist syntax errors**: Validate with `plutil <plist_path>`.
- **Bootstrap failures**: Ensure the LaunchAgent label matches the service name and that the program path is absolute.
- **LaunchAgent not starting**: Check `launchctl list` for the service; verify HOME env var in plist.

## Verification

 +**Delayed daemon startup** (e.g., Syncthing): The embedded binary may pause up to 10 seconds before launching; wait before probing the UI.
 +**Menubar‑only UI** (LSUIElement=1): The app shows no Dock icon; launch via menu‑bar icon or open `http://localhost:8384` directly.
 +**UI not reachable immediately**: Give the daemon ~15 seconds after launch before checking `http://localhost:8384`.
- Confirm process appears in `ps aux | grep <process_name>`.
- Verify web UI loads at expected URL.
- Check log files for error messages.

## Scripts
- `scripts/restart_syncthing.sh`: Automated restart script for Syncthing launch agent.

## References
- Add session-specific notes in `references/*.md`.