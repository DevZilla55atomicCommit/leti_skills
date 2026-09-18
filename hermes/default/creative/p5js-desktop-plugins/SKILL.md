---
name: p5js-desktop-plugins
description: "Build p5.js desktop plugins reacting to Hermes TTS state."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [desktop, plugins, p5js, visualization, voice, tts, audio-reactive]
    category: creative
    related_skills: [hermes-desktop-plugins, p5js, p5js-hermes-bridge]
---

# p5.js Desktop Plugins for Hermes

Class-level skill for creating Hermes desktop app plugins that use p5.js (WebGL) for real-time visualizations tied to Hermes voice/TTS state.

## When to Use

- Building desktop plugins with 3D/2D canvas visualizations (particles, waveforms, spectra)
- Need real-time reactivity to Hermes TTS speaking state (`$voicePlayback` atom)
- Creating voice-reactive UI elements (JARVIS-style spheres, audio visualizers, speaking avatars)
- Want performant WebGL rendering inside a plugin pane

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Hermes Desktop App                                          │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │  Plugin Pane    │    │  Voice Playback Store           │ │
│  │  (React)        │◄───│  $voicePlayback: atom            │ │
│  │  ┌───────────┐  │    │  { status: 'idle'|'preparing'|  │ │
│  │  │ p5.js     │  │    │   'speaking' }                   │ │
│  │  │ Canvas    │  │    └─────────────────────────────────┘ │
│  │  │ (WebGL)   │  │           ▲                            │
│  │  └───────────┘  │           │ poll / subscribe           │
│  └─────────────────┘           │                            │
└─────────────────────────────────┼────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            ┌─────────────┐             ┌─────────────┐
            │  text_to_   │             │  Auto-TTS   │
            │  speech_tool│             │  (voice.    │
            │  (TTS gen)  │             │  auto_tts)  │
            └─────────────┘             └─────────────┘
```

## Key Integration Points

### 1. Voice Playback State (The Truth Source)

The desktop app tracks TTS playback in `src/store/voice-playback.ts`:

```typescript
export type VoicePlaybackStatus = 'idle' | 'preparing' | 'speaking'

export interface VoicePlaybackState {
  audioElement: HTMLAudioElement | null
  messageId: string | null
  sequence: number
  source: VoicePlaybackSource | null
  status: VoicePlaybackStatus
}

export const $voicePlayback = atom<VoicePlaybackState>({...})
```

**States:**
- `idle` — no playback
- `preparing` — synthesizing audio (streaming WS connecting or POST in flight)
- `speaking` — audio actively playing

### 2. Accessing from Plugin

Plugins run in the same renderer process, so they can access the store via `window`:

```javascript
// In plugin component
useEffect(() => {
  const interval = setInterval(() => {
    const playback = window.$voicePlayback?.get?.()
    if (playback) {
      // Map: idle → idle, preparing → thinking, speaking → speaking
      const stateMap = {
        idle: 'idle',
        preparing: 'thinking',
        speaking: 'speaking',
      }
      updateVisualization(stateMap[playback.status], playback.status === 'speaking' ? 0.7 : 0.1)
    }
  }, 100)
  return () => clearInterval(interval)
}, [])
```

### 3. p5.js Integration Pattern

**Dynamic CDN load (no bundler):**
```javascript
useEffect(() => {
  if (window.p5) return
  const script = document.createElement('script')
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js'
  script.onload = () => { new window.p5(sketch, containerRef.current) }
  document.head.appendChild(script)
}, [])
```

**Canvas lifecycle:**
```javascript
const sketch = (p) => {
  p.setup = () => {
    const canvas = p.createCanvas(w, h, p.WEBGL)
    canvas.parent(containerRef.current)
    p.pixelDensity(1)
    p.disableFriendlyErrors = true
  }
  p.draw = () => { /* render frame */ }
  p.windowResized = () => { p.resizeCanvas(newW, newH) }
}
```

**ResizeObserver for pane resizing:**
```javascript
useEffect(() => {
  const ro = new ResizeObserver(entries => {
    for (const e of entries) { setWidth(e.contentRect.width); setHeight(e.contentRect.height) }
  })
  ro.observe(containerRef.current)
  return () => ro.disconnect()
}, [])
```

## Plugin Template Structure

```javascript
import { cn, host, useValue, atom } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'
import { useEffect, useRef, useState } from 'react'

const ID = 'my-visualizer'
const vizStateAtom = atom({ state: 'idle', amplitude: 0 })

function Canvas({ width, height }) {
  const ref = useRef(null)
  const p5Ref = useRef(null)
  const [ready, setReady] = useState(false)
  const vizState = useValue(vizStateAtom)

  // 1. Load p5.js from CDN
  useEffect(() => { /* dynamic import */ }, [width, height])

  // 2. Sync viz state to p5 instance
  useEffect(() => {
    if (p5Ref.current && ready) {
      p5Ref.current.setState(vizState.state)
      p5Ref.current.setAmplitude(vizState.amplitude)
    }
  }, [vizState.state, vizState.amplitude, ready])

  // 3. ResizeObserver on container
  useEffect(() => { /* ResizeObserver */ }, [])

  return <div ref={ref} style={{ width: '100%', height: '100%', minHeight: 300 }} />
}

function Pane() {
  const [w, setW] = useState(300)
  const [h, setH] = useState(400)

  // 4. Poll voice playback store
  useEffect(() => {
    const int = setInterval(() => {
      const pb = window.$voicePlayback?.get?.()
      if (pb) {
        const map = { idle: 'idle', preparing: 'thinking', speaking: 'speaking' }
        vizStateAtom.set({ state: map[pb.status], amplitude: pb.status === 'speaking' ? 0.7 : 0.1 })
      }
    }, 100)
    return () => clearInterval(int)
  }, [])

  return (
    <div data-viz-container style={{ flex: 1 }}>
      <Canvas width={w} height={h} />
    </div>
  )
}

export default {
  id: ID,
  name: 'My Visualizer',
  register(ctx) {
    ctx.register({
      id: 'pane', area: 'panes', title: 'Visualizer',
      data: { placement: 'right', width: '320px' },
      render: () => jsx(Pane, {})
    })
    ctx.register({
      id: 'chip', area: 'statusBar.right', order: 120,
      render: () => { /* status chip using useValue(vizStateAtom) */ }
    })
  }
}
```

## Particle System Patterns

### Sphere Globe (Pulsing Shell)
- Particles on sphere surface (`phi`, `theta` spherical coords)
- Radius modulated by `amplitude * pulse + noise`
- Draw as `POINTS` for 2000+ particles at 60fps

### Flow Field (Curl Noise)
- 3D curl noise velocity field
- Ripple wave from center on speech
- Boundary wrap for infinite flow

### Helix Torus (Rotating Geometry)
- Double helix + torus knot parametric curves
- Rotation speed tied to amplitude
- Wave deformation on speaking

### Burst Explosion (Radial)
- Particles explode outward on speech start
- Shockwave rings
- Implode back to center on silence

**Performance tips:**
- Use `beginShape(POINTS)` / `endShape()` not individual `ellipse()`
- `p.disableFriendlyErrors = true` + `pixelDensity(1)`
- `orbitControl()` for free 3D interaction
- Transparent background (`background(0,0,0,0)`) lets app theme show through

## Theming

**Never hardcode colors.** Use CSS variables resolved at runtime:

```javascript
// In p5 sketch
const accent = getComputedStyle(canvas).getPropertyValue('--ui-accent').trim()
// Or for HSB: compute from known palette, use theme vars for UI text only
```

**Statusbar chip colors:**
```javascript
const colors = {
  idle: 'text-(--ui-text-tertiary)',
  speaking: 'text-(--ui-accent)',
  thinking: 'text-(--ui-warning)',
}
```

## Pitfalls

| Pitfall | Solution |
|---------|----------|
| Canvas stays small/blurry on pane resize | Use `ResizeObserver` on container, call `p.resizeCanvas(w, h)` in `p.windowResized` |
| p5.js not found / `p5` undefined | Dynamic CDN load in `useEffect`, guard with `if (window.p5)` |
| Plugin re-loads p5.js on hot-reload | Check `p5Ref.current` before creating new instance; call `remove()` on cleanup |
| Stale closure reads old amplitude | Read atom via `useValue` in React, pass to p5 via exposed `setAmplitude()` method |
| 60fps drops with 5000+ particles | Use `POINTS` primitive, not individual shapes; consider pixel buffer for 10k+ |
| White flash on pane mount | Transparent canvas background (`background(0,0,0,0)`), no `background(0)` |
| Statusbar chip doesn't update | Use `useValue(atom)` in chip render, not closure over initial value |

## References

- `references/voice-playback-store.md` — Desktop app voice playback atom details
- `references/particle-patterns.md` — Four particle system implementations
- `templates/voice-visualizer-plugin.js` — Complete working plugin template

## Related Skills

- `hermes-desktop-plugins` — Plugin SDK fundamentals (panes, chips, areas, i18n)
- `p5js` — p5.js production pipeline (color, noise, export, performance)
- `p5js-hermes-bridge` — WebSocket bridge pattern (alternative for external browser UIs)