---
name: computer-use-debug
description: |
  Enhanced version of computer-use skill with additional debugging
  patterns and failure troubleshooting from recent EMAI Dashboard build.
version: 1.0.0
platforms: [macos, windows, linux]
metadata:
  hermes:
    tags: [debug, computer-use, desktop, automation, gui, cross-platform]
    category: desktop
    related_skills: [computer-use]
---
# Enhanced Computer Use

This skill extends the standard `computer-use` with additional debugging
patterns and failure troubleshooting insights gathered from recent
EMAI Dashboard builds.

## Failure modes — detailed troubleshooting

| Symptom | Likely cause + remedy |
|---|---|
| `cua-driver not installed` | Run `hermes computer-use install`, or `hermes tools` and enable Computer Use |
| Captures consistently return empty / "no on-screen window" | On Linux: DISPLAY may not be set (X11) or you're on pure Wayland — ask the user to run `hermes computer-use doctor`. On Windows: you may be in Session 0 (SSH session) instead of the interactive desktop — see the cua-driver `WINDOWS.md` deep-dive |
| Element index stale (\"Element N not in cache\") | SOM indices are only valid until the next `capture`. Re-capture before clicking. The wrapper carries opaque `element_token`s for stale-detection; you'll see an explicit error rather than a wrong click |
| Click had no effect | Read the structured verdict, don't just recapture. `effect:\"unverifiable\"` → re-capture and confirm yourself. `effect:\"suspected_noop\"` / `code:\"background_unavailable\"` / `escalation.recommended` → climb the ladder: try `coordinate=[x,y]` (px), then `delivery_mode=\"foreground\"`. A modal (e.g. an Electron consent dialog) may be blocking input — foreground delivery is how you dismiss it. Don't conclude the app is undrivable |
| Type text disappears into a terminal emulator | cua-driver detects terminals (Ghostty, iTerm2, Terminal.app, Windows Terminal, mintty, etc.) and routes through key-event synthesis — should "just work" on a recent cua-driver. If it doesn't, ask the user to run `hermes computer-use doctor` |
| `blocked pattern in type text` | You tried to `type` a shell command matching the dangerous-pattern block list (`curl ... \| bash`, `sudo rm -rf`, etc.). Break the command up or reconsider |
| Duplicate function declarations in TSX | Check for duplicate named functions/components: `grep -n "function" src/main.tsx` to find repeated definitions → fix by removing/re-exporting duplicates before build |
| Anything else weird | **First action: ask the user to run `hermes computer-use doctor`.** It runs the cua-driver `health_report` MCP tool and prints a structured per-check matrix. Their output tells you (and them) exactly what's wrong |

### Common debugging patterns from recent session (EMAI Dashboard build)
- **Duplicate declarations error**: Fix by removing duplicate named functions (e.g., LoadingState, ErrorState) when TypeScript reports TS2314 errors → clean function definitions before build
- **Build configuration errors**: When `esbuild` fails with path/module errors, verify the source path structure and ensure all imports are correctly resolved before building
- **Plugin copy errors**: If `cp` fails with "No such file or directory", verify the source file exists before copying to target location
- **Tokio runtime errors in browser extensions**: If you see "Runtime: net/http: superfluous path segment", ensure the built `main.js` is placed in `.obsidian/plugins/<plugin>/main.js` and not in a nested subdirectory