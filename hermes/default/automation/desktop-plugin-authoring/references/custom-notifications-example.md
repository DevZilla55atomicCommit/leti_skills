# Custom Notifications Plugin — Complete Working Example

This plugin plays custom audio on Hermes gateway events (turn complete, approval needed, tool complete, error).

## Files

- `~/.hermes/desktop-plugins/custom-notifications/plugin.js` — main plugin
- `~/.hermes/desktop-plugins/custom-notifications/generate_sounds.py` — ElevenLabs TTS generator
- `~/.hermes/desktop-plugins/custom-notifications/sounds/` — generated audio files

## Plugin Features

1. **Gateway event listener** — subscribes to `host.onEvent('*')` and maps events to sounds:
   - `message.complete` (success) → Turn Complete sound
   - `message.complete` (error) → Error sound
   - `approval.request` → Approval Needed sound
   - `tool.complete` → Tool Complete sound (off by default)
   - `session.info` (went idle after running) → Turn Complete sound

2. **Settings pane** (right sidebar, bottom docked):
   - Master on/off toggle
   - Per-event enable/disable checkboxes
   - File input for custom audio (.mp3, .wav, .ogg)
   - Test buttons for each sound
   - Event counter + last event display

3. **Status bar chip** (🔊/🔇) showing enabled state + event count

4. **⌘K command**: "Custom Notifications: Toggle"

## ElevenLabs TTS Sound Generation

```bash
# 1. Add API key to ~/.hermes/.env
echo "ELEVENLABS_API_KEY=your_key" >> ~/.hermes/.env

# 2. Run generator
~/.hermes/desktop-plugins/custom-notifications/generate_sounds.py

# 3. Load each .mp3 in the settings pane
```

Generated sounds (youthful pro female British voice):
- `turnComplete.mp3` — "Done."
- `approvalNeeded.mp3` — "Permission needed."
- `toolComplete.mp3` — "Tool finished."
- `error.mp3` — "Error occurred."

## Key Implementation Patterns

### Audio Management

```javascript
const DEFAULT_SOUNDS = {
  turnComplete: 'data:audio/wav;base64,...',  // tiny base64 WAV
  approvalNeeded: 'data:audio/wav;base64,...',
  toolComplete: 'data:audio/wav;base64,...',
  error: 'data:audio/wav;base64,...',
}

const audioCache = new Map()

function loadAudio(key, src) {
  if (audioCache.has(key)) return audioCache.get(key)
  const audio = new Audio(src)
  audio.preload = 'auto'
  audio.volume = 0.5
  audioCache.set(key, audio)
  return audio
}

function playSound(key, customSrc) {
  const src = customSrc || DEFAULT_SOUNDS[key]
  const audio = loadAudio(key, src)
  audio.currentTime = 0
  audio.play().catch(err => console.warn('Autoplay blocked:', err))
}
```

### Event Listener with Cleanup

```javascript
function useEventListener() {
  const enabled = useValue($enabled)
  const config = useValue($soundConfig)

  useEffect(() => {
    if (!enabled) return

    const disposer = host.onEvent('*', (event) => {
      $eventCount.set($eventCount.get() + 1)
      $lastEvent.set(`${event.type} (${event.session_id?.slice(0, 8)})`)

      if (!enabled) return

      switch (event.type) {
        case 'message.complete': {
          const payload = event.payload || {}
          if (payload.status === 'error' || payload.is_error) {
            if (config.error.enabled) playSound('error', config.error.customSrc)
          } else {
            if (config.turnComplete.enabled) playSound('turnComplete', config.turnComplete.customSrc)
          }
          break
        }
        case 'approval.request':
          if (config.approvalNeeded.enabled) playSound('approvalNeeded', config.approvalNeeded.customSrc)
          break
        case 'tool.complete':
          if (config.toolComplete.enabled) playSound('toolComplete', config.toolComplete.customSrc)
          break
      }
    })

    return disposer  // CRITICAL
  }, [enabled])
}
```

### Native HTML Form Controls (since Switch not exported)

```javascript
// Checkbox with theme styling
jsx('label', { className: 'flex items-center gap-2 cursor-pointer', children: [
  jsx('input', {
    type: 'checkbox',
    checked: enabled,
    onChange: (e) => $enabled.set(e.target.checked),
    className: 'w-4 h-4 accent-(--ui-accent) rounded border-(--ui-stroke-secondary) bg-(--ui-bg-secondary)'
  }),
  jsxs('div', { children: [
    jsx('div', { className: 'font-medium', children: 'Custom Notifications' }),
    jsx('div', { className: 'text-xs text-(--ui-text-tertiary)', children: 'Play custom sounds on Hermes gateway events' }),
  ]})
]})

// Styled native button (Button props differ)
jsx('button', {
  type: 'button',
  className: 'px-3 py-1.5 text-xs rounded border border-(--ui-stroke-secondary) bg-(--ui-bg-tertiary) hover:bg-(--chrome-action-hover) text-(--ui-text-secondary) disabled:opacity-50',
  onClick: () => testSound(key),
  disabled: testPlaying === key,
  children: testPlaying === key ? 'Playing...' : 'Test'
})
```

### File Input for Custom Audio

```javascript
jsx('input', {
  type: 'file',
  accept: 'audio/*',
  onChange: (e) => {
    const file = e.target.files[0]
    if (!file) return
    const url = URL.createObjectURL(file)
    $soundConfig.set({
      ...config,
      [key]: { ...config[key], customSrc: url }
    })
  },
  className: 'flex-1 text-xs file:mr-2 file:px-2 file:py-1 file:rounded file:bg-(--ui-accent) file:text-(--ui-accent-foreground) file:border-0'
})
```

## Verification

After **Reload desktop plugins**:
1. Open right sidebar → Custom Notifications tab
2. Toggle master switch ON
3. Click "Test" for each event — should hear sound
4. Load custom .mp3 files via file inputs
5. Trigger events (send a message, request approval) — sounds should play

## Troubleshooting

- **"Plugin failed to load"**: Check console (DevTools) for syntax errors — usually TypeScript in `.js` file
- **No sound**: Browser autoplay policy — interact with page first, or check `audio.play().catch()`
- **Duplicate sounds**: Missing `return disposer` in `useEffect` cleanup
- **Stale config in handler**: Use `$config.get()` imperatively, not `config` from closure