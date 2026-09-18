---
name: desktop-plugin-authoring
description: "Author Hermes desktop plugins — panes, statusbar, commands."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [desktop, plugins, ui, extension, sdk, javascript, react]
    category: automation
    related_skills: [hermes-agent, hermes-desktop-plugins]
---

# Hermes Desktop Plugin Authoring

Write plugins for the Hermes desktop app: statusbar items, layout panes, command-palette commands, keybinds, routes, and themes. A plugin is a single plain-JavaScript ESM file the app loads at runtime — no build step, no repo changes.

**Full human reference**: `website/docs/developer-guide/desktop-plugin-sdk.md`

## When to Use

- User wants a new desktop UI element (pane, statusbar widget, dashboard, command) without modifying the app
- Need to surface computed data (via gateway RPC) inside the app
- Want to react to gateway events (turn complete, approval needed, tool finished, etc.)

## Prerequisites

- Hermes desktop app (`hermes desktop` / `hermes gui`) — CLI/gateway alone doesn't load plugins
- Write access to `$HERMES_HOME/desktop-plugins/` (usually `~/.hermes/desktop-plugins/`)
- For profiles: `~/.hermes/profiles/<name>/desktop-plugins/`

## Quick Start

1. Create `$HERMES_HOME/desktop-plugins/<kebab-id>/plugin.js`
2. Folder name MUST equal plugin `id`
3. Default export shape: `{ id, name, register(ctx) }`
4. App watches directory — loads within seconds, hot-reloads on save
5. If not appearing: ⌘K → **Reload desktop plugins**
6. Errors show as toast — fix and save again

## Core Imports (ONLY these work)

```javascript
import { 
  cn, host, ctx, haptic, useValue, atom, Tip, Button, Codicon,
  useQuery, useQueryClient, usePluginI18n, queryClient,
  PALETTE_AREA, KEYBINDS_AREA, STATUSBAR_AREAS, ROUTES_AREA,
  SIDEBAR_NAV_AREA, TITLEBAR_AREAS, Contribute
} from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'
import { useEffect, useState, useRef } from 'react'
```

**Do NOT import** anything else — other specifiers fail to resolve.

## Architecture

### State Atoms (module-level, persist across renders)

```javascript
const $clicks = atom(0)           // nanostore atom
const $config = atom({...})       // reactive state
```

### Components (React, but JSX-free)

```javascript
function MyComponent() {
  const count = useValue($clicks)  // subscribe in leaf
  return jsx('div', { children: `Clicked ${count}x` })
}
```

### Event Listeners (subscribe to gateway events)

```javascript
function useEventListener() {
  useEffect(() => {
    const disposer = host.onEvent('*', (event) => {
      // event.type: 'message.complete', 'approval.request', 'tool.complete', 'session.info', etc.
      // event.payload: varies by type
      // event.session_id: current session
    })
    return disposer  // CRITICAL: return for cleanup on hot-reload
  }, [deps])
}
```

### Register UI Contributions

```javascript
export default {
  id: 'my-plugin',
  name: 'My Plugin',
  register(ctx) {
    // i18n
    ctx.i18n.register({ en: { paneTitle: 'My Pane' } })
    
    // Status bar chip
    ctx.register({
      id: 'chip',
      area: STATUSBAR_AREAS.right,
      order: 90,
      render: () => jsx(MyChipComponent, {})
    })
    
    // Pane (right sidebar)
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'My Pane',
      data: { placement: 'right', width: '340px', dock: { pane: 'workspace', pos: 'bottom' }, height: '400px' },
      render: () => { useEventListener(); return jsx(MyPane, {}) }
    })
    
    // ⌘K palette command
    ctx.register({
      id: 'cmd',
      area: PALETTE_AREA,
      data: {
        id: 'my-plugin.action',
        action: 'my-plugin.action',
        label: 'My Plugin: Do Thing',
        keywords: ['plugin', 'thing'],
        run: () => { /* ... */ }
      }
    })
    
    // Keybind (rebindable in settings)
    ctx.register({
      id: 'keybind',
      area: KEYBINDS_AREA,
      data: {
        id: 'my-plugin.action',
        label: 'My Plugin: Do Thing',
        defaults: [],  // no default binding
        run: () => { /* ... */ }
      }
    })
  }
}
```

## Pane Placement

- `placement: 'left'|'right'|'bottom'|'main'` — semantic zone (tabs with same role)
- `dock: { pane: 'workspace', pos: 'top'|'bottom'|'left'|'right'|'center' }` — specific edge
- Always set `height` for bottom docked panes so they don't take half the zone

## Theme Variables (NEVER hardcode colors)

```css
/* Text */
color: var(--ui-text-secondary)      /* primary labels */
color: var(--ui-text-tertiary)       /* descriptions, muted */
color: var(--ui-text-quaternary)     /* very subtle */

/* Backgrounds */
background: var(--ui-bg-tertiary)    /* cards, panels */
background: var(--ui-bg-secondary)   /* inputs, elevated */
background: var(--ui-chrome-action-hover)  /* hover states */

/* Borders */
border-color: var(--ui-stroke-secondary)

/* Accent */
color: var(--ui-accent)
background: var(--ui-accent)
accent-color: var(--ui-accent)

/* Semantic */
color: var(--ui-error)
color: var(--ui-warning)
color: var(--ui-success)
```

For canvas: `getComputedStyle(canvas).getPropertyValue('--ui-accent')`

## Common Pitfalls

### 1. TypeScript syntax in `.js` files — WON'T PARSE

```javascript
// ❌ FAILS: "Missing initializer in const declaration"
const audioCache = new Map<string, HTMLAudioElement>()
const $enabled = atom(true)
import { type HermesPlugin } from '@hermes/plugin-sdk'

// ✅ WORKS: plain JavaScript
const audioCache = new Map()
const $enabled = atom(true)
import { HermesPlugin } from '@hermes/plugin-sdk'
```

### 2. Not all documented UI components are exported

Docs list: `Button`, `Input`, `Textarea`, `Select*`, `Switch`, `Checkbox`, `SegmentedControl`, `Tabs*`, `Dialog*`, `ConfirmDialog`, `DropdownMenu*`, `ContextMenu*`, `Popover*`, `Tip`/`Tooltip*`, `Badge`, `Kbd`/`KbdGroup`, `SearchField`, `ScrollArea`, `Separator`, `Skeleton`, `GlyphSpinner`, `Loader`, `EmptyState`, `ErrorState`, `CopyButton`, `StatusDot`, `LogView`, `Codicon`, `DecodeText`

**Actually exported** (confirmed): `Button`, `Tip`, `Codicon`, `cn`, `haptic`, `useValue`, `atom`, `host`, `ctx`, `useQuery`, `useQueryClient`, `usePluginI18n`, `queryClient`, `PALETTE_AREA`, `KEYBINDS_AREA`, `STATUSBAR_AREAS`, `ROUTES_AREA`, `SIDEBAR_NAV_AREA`, `TITLEBAR_AREAS`, `Contribute`

**Workaround**: Use native HTML with theme-variable className:

```javascript
// ❌ Switch may not be exported
jsx(Switch, { checked: enabled, onChange: ... })

// ✅ Native checkbox with theme styling
jsx('label', { className: 'flex items-center gap-2 cursor-pointer', children: [
  jsx('input', {
    type: 'checkbox',
    checked: enabled,
    onChange: (e) => setEnabled(e.target.checked),
    className: 'w-4 h-4 accent-(--ui-accent) rounded border-(--ui-stroke-secondary) bg-(--ui-bg-secondary)'
  }),
  'Label'
]})

/* Button props may differ — fallback to styled native button */
jsx('button', {
  type: 'button',
  className: 'px-3 py-1.5 text-xs rounded border border-(--ui-stroke-secondary) bg-(--ui-bg-tertiary) hover:bg-(--chrome-action-hover) text-(--ui-text-secondary)',
  children: 'Test'
})
```

### 3. Event listener cleanup — ALWAYS return disposer

```javascript
useEffect(() => {
  const disposer = host.onEvent('*', handler)
  return disposer  // Prevents duplicate listeners on hot-reload
}, [deps])
```

### 4. Handlers read state imperatively, not from closures

```javascript
// ❌ Stale closure — reads old value
useEffect(() => {
  host.onEvent('*', () => { console.log(config) })  // config is stale
}, [])

// ✅ Imperative read in handler
const $config = atom({...})
host.onEvent('*', () => { console.log($config.get()) })  // always current
```

### 5. Audio playback

```javascript
const audio = new Audio(dataUriOrBlobUrl)
audio.preload = 'auto'
audio.volume = 0.5
audio.currentTime = 0  // reset for rapid re-triggers
audio.play().catch(err => console.warn('Autoplay blocked:', err))
```

## Gateway Event Types (common)

| Event | Payload | When |
|-------|---------|------|
| `message.complete` | `{ text, status?, is_error? }` | Agent finished (check `status === 'error'` or `is_error`) |
| `message.delta` | `{ text }` | Streaming token |
| `approval.request` | `{ tool, args }` | Needs user permission |
| `tool.start` | `{ tool, args }` | Tool began |
| `tool.complete` | `{ tool, result, is_error? }` | Tool finished |
| `session.info` | `{ is_active, running, ... }` | Session state change |
| `session.reclaimed` | `{}` | Session was taken over |

Subscribe with `host.onEvent('*', handler)` or specific type.

## Verification Checklist

- [ ] Plugin loads after **Reload desktop plugins** (no error toast)
- [ ] UI appears in correct area (statusbar, pane, palette, keybind)
- [ ] Pane is draggable like core panes
- [ ] Theme variables work (switch theme in Settings → Appearance)
- [ ] Hot-reload works (save file, UI updates without reload)
- [ ] No console errors (check DevTools if needed)
- [ ] Event listeners don't duplicate on hot-reload (check event count)

## Example: Custom Notifications Plugin

See `references/custom-notifications-example.md` for a complete working example that:
- Listens to `message.complete`, `approval.request`, `tool.complete`
- Plays custom audio per event type
- Settings pane with checkboxes, file inputs, test buttons
- Status bar indicator with event count
- ⌘K toggle command
- ElevenLabs TTS sound generator script

## References

- `references/desktop-plugin-pitfalls.md` — detailed pitfall catalog
- `templates/plugin.js` — starter template
- `scripts/generate-test-sounds.py` — ElevenLabs TTS generator