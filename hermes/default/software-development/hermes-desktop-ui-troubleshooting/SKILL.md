---
name: hermes-desktop-ui-troubleshooting
description: "Fix missing Hermes desktop statusbar and hidden UI items."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [desktop, ui, troubleshooting, statusbar, visibility]
    related_skills: [hermes-agent, inspecting-hermes-desktop-dom]
---

# Hermes Desktop UI Troubleshooting

## Overview

Common UI issues in the Hermes desktop app and how to fix them. Covers statusbar visibility, hidden items, layout problems, and configuration resets.

## When to Use

- Statusbar missing entirely (bottom bar gone)
- Specific status items missing (context meter, running timer, session timer, etc.)
- UI elements not appearing after update
- Layout issues, missing panels, or configuration drift

## Statusbar Visibility

### The Problem

As of recent updates, **the entire statusbar is OFF by default** (`$statusbarVisible = false`). Individual items like `context-usage`, `running-timer`, `session-timer`, `agents`, `approval-mode`, `cron`, `terminal`, `webhooks` are also **hidden by default** in `STATUSBAR_HIDDEN_BY_DEFAULT`.

### Fix: Show the Statusbar

1. **Keyboard shortcut**: Press `Cmd+Shift+S` (macOS) / `Ctrl+Shift+S` (Linux/Windows) — toggles `view.toggleStatusbar`
2. **Command Palette**: Press `Cmd+K` → search "Toggle status bar"
3. **Right-click the statusbar** (once visible) → check items to enable:
   - "Context meter" (shows token usage bar)
   - "Running timer" (shows turn duration)
   - "Session timer" (shows session duration)
   - "Agents", "Approval mode", "Cron", "Terminal", "Webhooks"

### Permanent Fix: Change Defaults in Source

The regression was introduced when defaults changed from visible→hidden. To restore sane defaults, patch `apps/desktop/src/store/statusbar-prefs.ts`:

```typescript
// Change whole-bar default from false → true
export const $statusbarVisible = persistentAtom(STATUSBAR_VISIBLE_STORAGE_KEY, true, Codecs.bool)

// Reduce HIDDEN_BY_DEFAULT to only navigation/utility items
export const STATUSBAR_HIDDEN_BY_DEFAULT: readonly string[] = [
  'agents',
  'cron',
  'terminal',
  'webhooks'
]
// context-usage, approval-mode, running-timer, session-timer now visible by default
```

Then rebuild: `cd apps/desktop && npm run build`

### Configuration Keys

Stored in localStorage / Hermes config:
- `hermes.desktop.statusbarVisible` — boolean, whole-bar visibility (default: `false`)
- `hermes.desktop.statusbarHidden` — string array of hidden item IDs (default: all items in `STATUSBAR_HIDDEN_BY_DEFAULT`)

### Programmatic Toggle

```typescript
import { $statusbarVisible, toggleStatusbarVisible, $statusbarHiddenIds, setStatusbarItemVisible } from '@/store/statusbar-prefs'

// Toggle whole bar
toggleStatusbarVisible()
// or
$statusbarVisible.set(true)

// Show specific item
setStatusbarItemVisible('context-usage', true)
setStatusbarItemVisible('running-timer', true)
```

## Common Missing Items

| Item ID | Toggle Label | What It Shows |
|---------|--------------|---------------|
| `context-usage` | Context meter | Visual token usage bar + dropdown with category breakdown |
| `running-timer` | Running timer | Current turn duration (live) |
| `session-timer` | Session timer | Total session duration |
| `agents` | Agents | Subagent count + failed indicator |
| `approval-mode` | Approval mode | Current approval mode (when gateway open) |
| `cron` | Cron | Cron jobs shortcut |
| `terminal` | Terminal | Terminal pane toggle |
| `webhooks` | Webhooks | Webhooks shortcut |

## Context Usage Bar Specifics

The context meter (`context-usage`) requires **live usage data from the gateway**:
- Native gateway (TUI): Emits `message.complete` with `context_max`, `context_percent`, `context_used`
- API Server platform: Currently emits `run.completed` with basic usage only — **context breakdown not included**

If the bar shows but reads "0/0" or empty:
1. Ensure you're connected to a native gateway (not API server only)
2. Check that a turn has completed (data arrives on `message.complete`)
3. Open the dropdown → it calls `session.context_breakdown` RPC

## Debugging Steps

1. **Verify statusbar mount**: Check `document.querySelector('[data-slot="statusbar"]')` exists
2. **Check visibility atom**: `$statusbarVisible.get()` in DevTools console
3. **Check hidden IDs**: `$statusbarHiddenIds.get()` — should not include items you want visible
4. **Inspect item render**: Right-click statusbar → "Customize" menu lists all toggleable items
5. **CDP inspection**: Use `inspecting-hermes-desktop-dom` skill to read live DOM

## Reset to Defaults

Clear localStorage keys:
```javascript
localStorage.removeItem('hermes.desktop.statusbarVisible')
localStorage.removeItem('hermes.desktop.statusbarHidden')
// Then reload app (Cmd+R)
```

## Related Skills

- `inspecting-hermes-desktop-dom` — CDP-based DOM inspection for deeper debugging
- `hermes-agent` — General Hermes configuration (CLI, providers, models)

## References

- `references/statusbar-visibility-defaults.md` — History of default value changes
- `references/context-usage-data-flow.md` — How context meter gets its data
- `references/statusbar-item-control.md` — Programmatic toggle reference