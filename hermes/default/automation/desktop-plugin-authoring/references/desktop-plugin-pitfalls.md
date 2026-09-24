# Desktop Plugin Pitfalls — Discovered Patterns

## TypeScript in `.js` files won't parse

Plugin files load as **plain ESM (uncompiled)**. These will cause "Missing initializer in const declaration" or similar syntax errors:

```javascript
// ❌ WRONG — TypeScript syntax
const audioCache = new Map<string, HTMLAudioElement>()
const $enabled = atom(true)
import { type HermesPlugin } from '@hermes/plugin-sdk'

// ✅ CORRECT — plain JavaScript
const audioCache = new Map()
const $enabled = atom(true)
import { HermesPlugin } from '@hermes/plugin-sdk'
```

## Not all documented UI components are exported

The docs list: `Button`, `Input`, `Textarea`, `Select*`, `Switch`, `Checkbox`, `SegmentedControl`, `Tabs*`, `Dialog*`, `ConfirmDialog`, `DropdownMenu*`, `ContextMenu*`, `Popover*`, `Tip`/`Tooltip*`, `Badge`, `Kbd`/`KbdGroup`, `SearchField`, `ScrollArea`, `Separator`, `Skeleton`, `GlyphSpinner`, `Loader`, `EmptyState`, `ErrorState`, `CopyButton`, `StatusDot`, `LogView`, `Codicon`, `DecodeText`

**Actually exported** (confirmed): `Button`, `Tip`, `Codicon`, `cn`, `haptic`, `useValue`, `atom`, `host`, `ctx`, `useQuery`, `useQueryClient`, `usePluginI18n`, `queryClient`, `PALETTE_AREA`, `KEYBINDS_AREA`, `STATUSBAR_AREAS`, `ROUTES_AREA`, `SIDEBAR_NAV_AREA`, `TITLEBAR_AREAS`, `Contribute`

**Workaround**: Use native HTML elements with theme-variable styling:

```javascript
// ❌ Switch may not be exported
jsx(Switch, { checked: enabled, onChange: ... })

// ✅ Always works
jsx('label', { className: 'flex items-center gap-2 cursor-pointer', children: [
  jsx('input', {
    type: 'checkbox',
    checked: enabled,
    onChange: (e) => setEnabled(e.target.checked),
    className: 'w-4 h-4 accent-(--ui-accent) rounded border-(--ui-stroke-secondary) bg-(--ui-bg-secondary)'
  }),
  'Label text'
]})
```

```javascript
// ❌ Button props may not include variant/size
jsx(Button, { variant: 'outline', size: 'sm', children: 'Test' })

// ✅ Use className with theme variables
jsx('button', {
  type: 'button',
  className: 'px-3 py-1.5 text-xs rounded border border-(--ui-stroke-secondary) bg-(--ui-bg-tertiary) hover:bg-(--chrome-action-hover) text-(--ui-text-secondary)',
  children: 'Test'
})
```

## Button component prop differences

The exported `Button` component may not support standard React props like `variant`, `size`, `disabled` the same way. Test and fall back to styled native `<button>`.

## Event listener cleanup

`host.onEvent` returns a disposer function — **always return it from `useEffect`** to avoid duplicate listeners on hot-reload:

```javascript
useEffect(() => {
  const disposer = host.onEvent('*', handler)
  return disposer // Critical!
}, [deps])
```

## Audio in plugins

- `new Audio(dataUri)` works for tiny base64 WAV files
- For larger files, use `URL.createObjectURL(file)` from file input
- Call `audio.currentTime = 0` before `audio.play()` for rapid re-triggers
- Handle promise rejection from `play()` (autoplay policy)

## Theme variables

Always use CSS custom properties, never hardcoded colors:

```css
/* ✅ */
color: var(--ui-text-secondary)
background: var(--ui-bg-tertiary)
border-color: var(--ui-stroke-secondary)
accent-color: var(--ui-accent)

/* ❌ */
color: #666
background: #1e1e1e
border-color: #333
accent-color: #00d4aa
```

## Handlers read state imperatively, not from closures

```javascript
// ❌ Stale closure — reads old value
useEffect(() => {
  host.onEvent('*', () => { console.log(config) })  // config is stale
}, [])

// ✅ Imperative read in handler
const $config = atom({...})
host.onEvent('*', () => { console.log($config.get()) })  // always current
```