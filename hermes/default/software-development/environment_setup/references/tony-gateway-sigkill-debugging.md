# TONY AI Agent Gateway — SIGKILL Debugging Reference

## Problem
The TONY AI Agent gateway server (Node.js) running at `/Users/alfredkamisese/TONY-AI-Agent/src/gateway/server.js` was repeatedly killed with SIGKILL (exit code -9) shortly after startup.

## Symptoms
- Server starts successfully: "TONY gateway listening on http://localhost:8787"
- WebSocket: "ws://localhost:8787/ws?token=***"
- Process dies within seconds/minutes with exit code -9 (SIGKILL)
- Happened repeatedly across multiple restarts

## Root Cause (Hypothesis)
macOS memory pressure / aggressive process management killing Node.js process. System showed:
- 15GB used / ~16GB physical (226M unused)
- Load average: 11.34, 9.37, 8.52
- Heavy memory compression (7GB compressed)

## Workaround Applied
Restarted with explicit Node.js heap limit:
```bash
node --max-old-space-size=512 src/gateway/server.js
```
This limits V8 heap to 512MB, reducing memory pressure.

## Commands Used
```bash
# Check system memory pressure
top -l 1 -n 0 | head -30

# Start with limited heap (background, notify on exit)
cd /Users/alfredkamisese/TONY-AI-Agent
/Users/alfredkamisese/.hermes/node/bin/node --max-old-space-size=512 src/gateway/server.js
```

## Monitoring
If it dies again with --max-old-space-size=512:
1. Check `dmesg` or Console.app for "out of memory" or "jetsam" messages
2. Try even lower: `--max-old-space-size=256`
3. Check if TONY has a memory leak (monitor heap with `node --inspect`)
4. Consider running via `systemd`/`launchd` with memory limits instead of raw node

## Related Files
- Gateway: `/Users/alfredkamisese/TONY-AI-Agent/src/gateway/server.js`
- Node binary: `/Users/alfredkamisese/.hermes/node/bin/node`

## Date
2026-07-08