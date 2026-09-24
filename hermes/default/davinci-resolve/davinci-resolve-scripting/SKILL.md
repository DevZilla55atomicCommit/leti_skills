---
name: davinci-resolve-scripting
description: 'Write and run Resolve scripts via API, MagicScript, or MCP.'
version: 1.0.0
author: Maddie
license: MIT
platforms: [macos, windows, linux]
metadata:
  hermes:
    tags: [davinci-resolve, scripting, magicscript, mcp, automation, stream-deck]
    related_skills: [davinci-resolve-mcp-color-grading]
---

# DaVinci Resolve Scripting (API + MagicScript + MCP)

## The core doctrine (from MrAlexTech, Resolve 21.1)

- Resolve 21.1's MCP server does NOT drive the UI. It reads the Scripting API, **writes a script**, runs it. Every prompt = 5–15 min of fresh script generation, possibly different each time (hallucination).
- Correct pattern: **use AI once to write the script, save it with variables, run locally forever** — offline, free, deterministic, shareable. That is what MagicScript is: a script manager (Workspace > Workflow Integrations > Magic Script).
- Keep creative decisions with the human (e.g. YOU pick shorts ranges with markers; the script only does the mechanical rebuild). If the task needs judgment over content ("find the good parts"), that is an AI-cloud task, not a script.

## Prerequisites

- Resolve Studio running (Free edition scripting is limited; MCP/MagicScript target Studio).
- macOS env (run before any external Python script):

```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

- Script install dirs (picked up under Workspace > Scripts on launch):
  - All users (macOS): `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/`
  - Per user (macOS): `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/`
- In-app runner: Workspace > Console (paste/run), or MagicScript panel for saved variable scripts.
- Python >= 3.6 64-bit. Full API doc: `README.txt` inside `$RESOLVE_SCRIPT_API` (also mirrored as gist `mhadifilms/094c933d4f5c6288c5c070bb8cc7c172`).

## MCP path (Resolve 21.1+, Studio)

1. File > Setup AI Assistants → pick installed AI (Claude Code / Claude Desktop / Codex) or attach a local LLM by pointing it at the Resolve `mcp.exe` path (Windows) / MCP bundle (Mac).
2. Prompt the AI normally ("rotate all timeline clips 180 deg"). It writes + runs a script; ask it to ALSO save the script file so you can reuse it without re-prompting.
3. Anything worth running twice → convert to a MagicScript (next section), never re-prompt.

## MagicScript authoring pattern

1. Download: https://magic-toolkit.com/magicscript (free; Win + Mac, Linux pending). Tick the Stream Deck plugin box at install.
2. Open the AI Guide: MagicScript panel > AI Guide button (bottom-right) → markdown file with save paths + variable syntax. Copy it into a FRESH AI conversation, then describe the script in the same message.
3. Authoring rules that work:
   - Ask for runtime variables for everything you might change (track number, videos-only vs photos, transition type + length in frames, bin name, timeline name, language, output path/format).
   - Many variables auto-group into tabs — expected, not an error.
   - After generation: new project → Workflow Integrations > Magic Script > Reload → double-click to test with variables → Run. Panel auto-saves the project first.
   - Mini mode pins the panel to a corner; categories/playlists (e.g. `favorites`, `weddings`) organize scripts.
4. Stream Deck binding: Stream Deck app > `Run Script` action > pick script > name the button > choose `prompt with last-used settings` vs `run at once`. Destructive scripts (strip transitions) must keep the confirm dialog.

## Boilerplate (every external Python script)

```python
import sys
sys.path.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
mp = project.GetMediaPool()
timeline = project.GetCurrentTimeline()
```

## API essentials (names to reach for)

- Project/timeline: `GetCurrentTimeline`, `GetTimelineCount`, `CreateNewTimeline(name)`, `GetItemListInTrack(type, index)` (`type`: `video`/`audio`/`subtitle`).
- Clips: `GetName`, `GetStart/GetEnd/GetDuration`, `AddMarker(frame, color, name, note, duration)` (duration>0 = ranged marker), `GetMarkers`.
- Media pool: `GetRootFolder`, `GetClipList`, `CreateNewFolder`, `ImportMedia`, `CreateTimelineFromClips`.
- Render/exports: `SetRenderSettings`, `AddRenderJob`, `StartRendering`; captions/subtitles: timeline subtitle track + export — verify exact call against local `README.txt` before shipping a script (names shift between versions).
- Always `project.Save()` (or rely on MagicScript's pre-run save) before destructive ops; destructive scripts print a warning and require confirmation.

## Proven script templates (from the tutorial)

| Script | Variables | Notes |
|---|---|---|
| `setup-timeline` | a-roll clip, ext audio, grade preset, delivery preset (YouTube 4K) | Sync ext audio to A-roll, apply grade, normalize, drop OBS rec synced, build 4K timeline. Zero AI at run. Stream Deck `setup`. |
| `erms-silence-cut` | threshold dB, min silence, filler list | Transcribe timeline (Resolve local transcription = only AI step), cut silences + ums, rebuild. Stream Deck `erms`. |
| `dynamic-zoom-on-track` | track #, videos-only flag, easing, in/out, scale | Cannot copy/paste dynamic zooms manually — script is the only clean way. |
| `dissolve-at-every-cut` | transition type (pulled live from Resolve), length frames | Star-wipe-15-frames demo; verify zoomed into cuts. |
| `strip-all-transitions` | none | Destructive + irreversible → confirm dialog mandatory. |
| `photo-slideshow-on-paper` | bin name, timeline name, scale, drop-shadow bool, dynamic-zoom bool, still duration, transition | Paper generator T1 + stills T2, Fusion rotation jitter, cross-dissolves. ~15–20 min to generate, instant to run. |
| `captions-to-srt` | language, path, filename | Generate subs on current timeline, export unformatted SRT. |
| `thumbnail-candidates-from-markers` | color filter, out path, format | Grab at markers, save + reimport to media pool. |
| `shorts-from-ranged-markers` | source timeline, grade/transitions/titles/subs toggles | Human marks ranges (M key, Alt/Opt-drag = range, snap on edit points, double-click to name). Script duplicates to vertical timelines, names, subtitles. |
| `report-fonts / assemble-bin-shooting-order / delete-empty-tracks` | per script | Bundled MagicScript examples — good first reads. |

## Pitfalls

1. Re-prompting MCP per run = slow, costly, nondeterministic. Save the script.
2. Ranged-marker scripts require cuts at range edges — script should either enforce or warn.
3. Transition/script enums differ across Resolve versions — pull live from the API, never hardcode.
4. Fusion-set properties (e.g. slideshow rotation) will not show in Edit-page inspectors — document that in the script description.
5. Resolve must be running with a project open; external scripts fail silently otherwise — guard with `if not project: sys.exit(...)`.
