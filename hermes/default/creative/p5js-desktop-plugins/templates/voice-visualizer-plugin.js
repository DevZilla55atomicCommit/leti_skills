/**
 * Hermes Voice Visualizer Plugin — p5.js particle sphere reacting to TTS
 * Save as: ~/.hermes/desktop-plugins/voice-visualizer/plugin.js
 * Then run "Reload desktop plugins" from ⌘K in the desktop app.
 *
 * Uses Sphere Globe pattern (pulsing shell) from references/particle-patterns.md
 * Reads TTS state from desktop app's $voicePlayback atom (idle/preparing/speaking)
 */

import { cn, host, useValue, atom } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'
import { useEffect, useRef, useState } from 'react'

const ID = 'voice-visualizer'

// --- TTS State Atom (synced from desktop's voice playback) ---
const ttsStateAtom = atom({
  state: 'idle', // idle, speaking, thinking
  amplitude: 0,
  text: '',
  timestamp: 0,
})

// --- p5.js Sketch Component (Sphere Globe pattern) ---
function ParticleCanvas({ width, height }) {
  const canvasRef = useRef(null)
  const p5Ref = useRef(null)
  const [sketchReady, setSketchReady] = useState(false)

  // Read TTS state reactively
  const ttsState = useValue(ttsStateAtom)

  useEffect(() => {
    if (!canvasRef.current || p5Ref.current) return

    // Dynamic p5 import (CDN)
    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js'
    script.onload = () => {
      const sketch = (p) => {
        const CONFIG = {
          particleCount: 2000,
          sphereRadius: 160,
          pulseSpeed: 2.0,
          noiseScale: 0.003,
        }

        const PALETTE = {
          bg: 'transparent',
          idle: { h: 45, s: 60, b: 80 },
          speaking: { h: 30, s: 85, b: 95 },
          thinking: { h: 275, s: 65, b: 80 },
        }

        let particles = []
        let currentState = 'idle'
        let targetAmplitude = 0
        let currentAmplitude = 0
        let time = 0
        let containerWidth = width
        let containerHeight = height

        p.setup = () => {
          const canvas = p.createCanvas(containerWidth, containerHeight, p.WEBGL)
          canvas.parent(canvasRef.current)
          p.colorMode(p.HSB, 360, 100, 100, 100)
          p.pixelDensity(1)
          p.disableFriendlyErrors = true

          for (let i = 0; i < CONFIG.particleCount; i++) {
            const phi = Math.acos(2 * Math.random() - 1)
            const theta = Math.random() * Math.PI * 2
            particles.push({
              phi,
              theta,
              baseR: CONFIG.sphereRadius,
              offset: Math.random() * 1000,
              size: 1.5 + Math.random() * 1.5,
              hueOffset: Math.random() * 30 - 15,
            })
          }
          setSketchReady(true)
        }

        p.draw = () => {
          p.background(0, 0, 0, 0)
          time += 0.016

          currentAmplitude = p.lerp(currentAmplitude, targetAmplitude, 0.12)
          p.orbitControl(2, 2, 0.1)

          const stateColor = PALETTE[currentState]
          const pulse = 1 + currentAmplitude * 0.4 + Math.sin(time * CONFIG.pulseSpeed) * 0.05

          p.beginShape(p.POINTS)
          for (const pt of particles) {
            const n = p.noise(pt.phi * 10, pt.theta * 10, time * CONFIG.noiseScale + pt.offset)
            const r = pt.baseR * pulse * (0.95 + n * 0.15)

            const x = r * Math.sin(pt.phi) * Math.cos(pt.theta)
            const y = r * Math.cos(pt.phi)
            const z = r * Math.sin(pt.phi) * Math.sin(pt.theta)

            const distFromCenter = Math.sqrt(x * x + y * y + z * z)
            const brightness = p.map(distFromCenter, CONFIG.sphereRadius * 0.8, CONFIG.sphereRadius * 1.2, 90, 40)
            const alpha = p.map(distFromCenter, CONFIG.sphereRadius * 0.8, CONFIG.sphereRadius * 1.2, 100, 30)

            p.stroke((stateColor.h + pt.hueOffset + n * 20) % 360, stateColor.s, brightness, alpha)
            p.strokeWeight(pt.size * (0.8 + currentAmplitude * 0.5))
            p.vertex(x, y, z)
          }
          p.endShape()

          p.noStroke()
          p.fill(stateColor.h, stateColor.s, 90, 15 + currentAmplitude * 30)
          p.sphere(CONFIG.sphereRadius * 0.15 * pulse)
        }

        p.windowResized = () => {
          containerWidth = canvasRef.current?.clientWidth || width
          containerHeight = canvasRef.current?.clientHeight || height
          p.resizeCanvas(containerWidth, containerHeight)
        }

        p.setState = (state) => { currentState = state }
        p.setAmplitude = (amp) => { targetAmplitude = amp }
      }

      p5Ref.current = new window.p5(sketch)
    }
    document.head.appendChild(script)

    return () => {
      if (p5Ref.current) {
        p5Ref.current.remove()
        p5Ref.current = null
      }
    }
  }, [width, height])

  // Sync TTS state to p5 sketch
  useEffect(() => {
    if (!p5Ref.current || !sketchReady) return
    p5Ref.current.setState(ttsState.state)
    p5Ref.current.setAmplitude(ttsState.amplitude)
  }, [ttsState.state, ttsState.amplitude, sketchReady])

  return jsx('div', { ref: canvasRef, style: { width: '100%', height: '100%', minHeight: 300 } })
}

// --- Main Pane Component ---
function VoiceVisualizerPane() {
  const [width, setWidth] = useState(300)
  const [height, setHeight] = useState(400)

  // Poll desktop's voice playback store
  useEffect(() => {
    const interval = setInterval(() => {
      try {
        const playback = window.$voicePlayback?.get?.()
        if (playback) {
          const stateMap = { idle: 'idle', preparing: 'thinking', speaking: 'speaking' }
          const ampMap = { idle: 0.05, preparing: 0.2, speaking: 0.7 }
          const state = stateMap[playback.status] || 'idle'
          const baseAmp = ampMap[playback.status] || 0.05
          const amplitude = baseAmp + (state === 'speaking' ? Math.random() * 0.3 : Math.sin(Date.now() / 2000) * 0.03)

          ttsStateAtom.set({
            state,
            amplitude,
            text: '',
            timestamp: Date.now(),
          })
        }
      } catch (e) {
        // Store not accessible yet
      }
    }, 100)

    return () => clearInterval(interval)
  }, [])

  // ResizeObserver for canvas
  useEffect(() => {
    const container = document.querySelector('[data-voice-viz-container]')
    if (!container) return

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        setWidth(entry.contentRect.width)
        setHeight(entry.contentRect.height)
      }
    })
    ro.observe(container)
    return () => ro.disconnect()
  }, [])

  const ttsState = useValue(ttsStateAtom)

  const stateColors = {
    idle: 'var(--ui-text-tertiary)',
    speaking: 'var(--ui-accent)',
    thinking: 'var(--ui-warning)',
  }

  const stateLabels = {
    idle: 'Idle',
    speaking: 'Speaking',
    thinking: 'Thinking',
  }

  return jsxs('div', {
    'data-voice-viz-container': true,
    className: 'flex h-full flex-col gap-2 p-3',
    children: [
      // Header with state indicator
      jsxs('div', {
        className: 'flex items-center justify-between',
        children: [
          jsx('span', { className: 'font-medium text-sm', children: 'Voice Visualizer' }),
          jsxs('div', {
            className: 'flex items-center gap-2',
            children: [
              jsx('span', {
                className: 'relative flex h-2 w-2 rounded-full transition-colors',
                style: {
                  backgroundColor: stateColors[ttsState.state],
                  boxShadow: `0 0 8px ${stateColors[ttsState.state]}`,
                },
              }),
              jsx('span', {
                className: 'text-xs text-(--ui-text-tertiary) font-mono',
                children: stateLabels[ttsState.state],
              }),
              jsx('span', {
                className: 'text-[10px] text-(--ui-text-quaternary) font-mono',
                children: `${Math.round(ttsState.amplitude * 100)}%`,
              }),
            ],
          }),
        ],
      }),

      // Canvas area
      jsx('div', {
        style: { flex: 1, minHeight: 280, position: 'relative' },
        children: jsx(ParticleCanvas, { width, height }),
      }),

      // Current text display
      ttsState.text && jsx('div', {
        className: 'text-xs text-(--ui-text-tertiary) truncate',
        children: ttsState.text.slice(0, 80) + (ttsState.text.length > 80 ? '…' : ''),
      }),
    ],
  })
}

// --- Plugin Registration ---
export default {
  id: ID,
  name: 'Voice Visualizer',
  defaultEnabled: true,

  register(ctx) {
    ctx.i18n.register({
      en: {
        paneTitle: 'Voice Visualizer',
        speaking: 'Speaking',
        thinking: 'Thinking',
        idle: 'Idle',
      },
    })

    // Right sidebar pane — user can drag tab out to float
    ctx.register({
      id: 'voice-viz-pane',
      area: 'panes',
      title: 'Voice Visualizer',
      data: {
        placement: 'right',
        width: '320px',
      },
      render: () => jsx(VoiceVisualizerPane, {}),
    })

    // Statusbar chip for quick state glance
    ctx.register({
      id: 'voice-viz-chip',
      area: 'statusBar.right',
      order: 120,
      render: () => {
        const ttsState = useValue(ttsStateAtom)
        const colors = {
          idle: 'text-(--ui-text-tertiary)',
          speaking: 'text-(--ui-accent)',
          thinking: 'text-(--ui-warning)',
        }
        const icons = {
          idle: 'mic',
          speaking: 'mic',
          thinking: 'sparkle',
        }
        return jsx('span', {
          className: cn(
            'inline-flex h-full items-center gap-1 px-1.5 text-[0.6875rem]',
            colors[ttsState.state]
          ),
          children: [
            jsx('span', {
              className: `codicon codicon-${icons[ttsState.state]} relative`,
              style: ttsState.state === 'speaking'
                ? { animation: 'pulse 1s infinite' }
                : ttsState.state === 'thinking'
                  ? { animation: 'pulse 1.5s infinite' }
                  : {},
            }),
            ttsState.state.charAt(0).toUpperCase() + ttsState.state.slice(1),
          ],
        })
      },
    })

    // Inject CSS for pulsing animation
    if (typeof document !== 'undefined') {
      const style = document.createElement('style')
      style.textContent = `
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `
      document.head.appendChild(style)
    }
  },
}