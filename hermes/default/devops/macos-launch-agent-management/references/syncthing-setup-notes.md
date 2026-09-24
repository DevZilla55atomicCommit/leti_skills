# Syncthing Launch Agent Setup Notes (2026-07-17)

## Errors Encountered
- `Failed to acquire lock: another Syncthing instance already running?`
- `Load failed: Input/output error` when loading launch agent

## Fix Sequence
1. **Kill existing processes**  
   ```bash
   pkill -9 -f "syncthing.*--no-browser"
   ```
2. **Unload existing LaunchAgent**  
   ```bash
   launchctl unload ~/Library/LaunchAgents/syncthing.plist 2>/dev/null || true
   ```

3. **Load corrected plist**  
   - Updated `<string>/Users/alfredkamisese/bin/syncthing</string>` path  
   - Added `STNORESTART` env var  
   ```bash
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/syncthing.plist
   ```

4. **Verify**  
   ```bash
   ps aux | grep syncthing
   curl -s http://127.0.0.1:8384/ | head -20
   ```

## Key Pitfalls
- Ensure `ProgramArguments` uses **absolute path** to syncthing binary.  
- `launchctl bootstrap` required for per-user GUI agents after plist edit.  
- `STNORESTART=1` prevents automatic restarts that can cause lock conflicts.  

## Verification Commands
- `launchctl list | grep syncthing` → shows running processes  
- Open `http://localhost:8384` → Syncthing GUI loads with 6 folders synced  
- Check logs: `tail -f ~/Library/Logs/Syncthing.log` and `~/.logs/Syncthing-Errors.log`