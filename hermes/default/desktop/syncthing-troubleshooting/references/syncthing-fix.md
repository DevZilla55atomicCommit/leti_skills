# Syncthing Fix (Hermes Environment)

## Quick Fix
1. Kill stale processes: `pkill -9 -f "syncthing" 2>/dev/null; sleep 2`
2. Restart wrapper: `open /Applications/Syncthing.app`
3. Wait 5 seconds
4. Verify UI: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8384/` (should return 200)

## Key Commands
- Restart wrapper: `open /Applications/Syncthing.app`
- Check daemon: `ps aux | grep -i syncthing | grep -v grep`
- Verify UI: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8384/`