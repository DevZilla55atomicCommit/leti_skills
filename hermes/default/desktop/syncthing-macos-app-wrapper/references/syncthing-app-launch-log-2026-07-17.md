# Syncthing App Launch Log – 2026-07-17

## Connection Details
```json
{
  "connections": {
    "4W5M2AR-7GKMQ7S-K62RW6B-7W5L5PD-YDBJM5D-ZBDYVCG-VGIEMLI-FSQFYQC": {
      "address": "10.0.0.192:22000",
      "type": "tcp-client",
      "isLocal": true,
      "crypto": "TLS1.3-TLS_AES_128_GCM_SHA256",
      "primary": {
        "address": "10.0.0.192:22000",
        "startedAt": "2026-07-17T19:33:07-07:00",
        "inBytesTotal": 608,
        "outBytesTotal": 525
      },
      "secondary": [
        {
          "address": "10.0.0.192:22000",
          "inBytesTotal": 8,
          "outBytesTotal": 8,
          "startedAt": "2026-07-17T19:33:13-07:00",
          "type": "tcp-client",
          "isLocal": true,
          "crypto": "TLS1.3-TLS_AES_128_GCM_SHA256"
        },
        {
          "address": "[fe80::1cc6:5d2c:5888:b6a4%en12]:22000",
          "inBytesTotal": 8,
          "outBytesTotal": 8,
          "startedAt": "2026-07-17T19:33:13-07:00",
          "type": "tcp-server",
          "isLocal": true,
          "crypto": "TLS1.3-TLS_AES_128_GCM_SHA256"
        }
      ]
    }
  }
}
```

## Daemon & Wrapper Processes
```bash
# Process snapshot (captured 2026-07-17 19:33:XX)
ps aux | grep -i Syncthing
#-output
alfredkamisese   52730   0.0  0.3 436925184  49168   ??  SN    7:33PM   0:02.37 /Applications/Syncthing.app/Contents/Resources/syncthing/syncthing --no-browser --no-restart --logfile=default
alfredkamisese   52729   0.0  0.1 436708432  15872   ??  S     7:33PM   0:00.05 /Applications/Syncthing.app/Contents/Resources/syncthing/syncthing --no-browser --no-restart --logfile=default
alfredkamisese   52684   0.0  0.4 435672480  67152   ??  S     7:32PM   0:00.51 /Applications/Syncthing.app/Contents/MacOS/Syncthing
```

## Launch Commands Executed
```bash
# 1. Ensure wrapper is launched from /Applications for menu‑bar visibility
open /Applications/Syncthing.app

# 2. Wait briefly for daemon to re‑initialize
sleep 5

# 3. Verify daemon health
curl -s http://127.0.0.1:8384/ | head -5
```

## Verification Output
- **Web UI**: http://127.0.0.1:8384 loads Syncthing interface.
- **Menu‑Bar**: Syncthing icon appears in top‑right menu bar (confirmed after relaunch).
- **Daemon Status**: `ps` shows all three processes running; `curl` returns HTML UI snippet.

## Pitfalls & Fixes Noted
- **Launching from Downloads**: Bypasses embedded `Info.plist` → menu‑bar icon may not appear.
- **Wrapper Crash but Daemon Alive**: Simply `open /Applications/Syncthing.app` restores menu‑bar icon.
- **Web UI Unreachable**: Restart wrapper; daemon auto‑restarts after ~10 s.