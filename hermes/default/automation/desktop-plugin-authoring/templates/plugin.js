/**
 * Hermes Desktop Plugin Template
 * Save as: ~/.hermes/desktop-plugins/<your-plugin-id>/plugin.js
 * Then run "Reload desktop plugins" from ⌘K.
 */

import { 
  cn, host, ctx, haptic, useValue, atom, Tip, Button, Codicon,
  useQuery, useQueryClient, usePluginI18n, queryClient,
  PALETTE_AREA, KEYBINDS_AREA, STATUSBAR_AREAS, ROUTES_AREA,
  SIDEBAR_NAV_AREA, TITLEBAR_AREAS, Contribute
} from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'
import { useEffect, useState, useRef } from 'react'

const ID = 'your-plugin-id'

// ---- State Atoms ----
const $enabled = atom(true)
const $config = atom({ /* your config */ })

// ---- Components ----
function MyComponent() {
  const enabled = useValue($enabled)
  const config = useValue($config)
  
  return jsx('div', {
    className: 'flex h-full flex-col gap-4 p-4 text-sm',
    children: [
      jsx('div', { className: 'font-medium', children: 'My Plugin' }),
      // Your UI here
    ]
  })
}

// ---- Event Listener ----
function useEventListener() {
  const enabled = useValue($enabled)
  
  useEffect(() => {
    if (!enabled) return
    
    const disposer = host.onEvent('*', (event) => {
      // event.type: 'message.complete', 'approval.request', 'tool.complete', 'session.info', etc.
      // event.payload: varies by type
      // event.session_id: current session
      
      switch (event.type) {
        case 'message.complete':
          // Handle turn complete
          break
        case 'approval.request':
          // Handle approval needed
          break
        case 'tool.complete':
          // Handle tool finished
          break
      }
    })
    
    return disposer
  }, [enabled])
}

// ---- Main Plugin Export ----
export default {
  id: ID,
  name: 'Your Plugin Name',
  register(ctx) {
    ctx.i18n.register({
      en: {
        paneTitle: 'Your Plugin',
      }
    })

    // Status bar chip
    ctx.register({
      id: 'status-chip',
      area: STATUSBAR_AREAS.right,
      order: 90,
      render: () => {
        const enabled = useValue($enabled)
        return jsx(Tip, {
          label: `Your Plugin: ${enabled ? 'ON' : 'OFF'}`,
          children: jsx('button', {
            type: 'button',
            className: cn(
              'px-2 py-1 text-[0.625rem] rounded border border-(--ui-stroke-secondary) bg-(--ui-bg-tertiary) hover:bg-(--chrome-action-hover)',
              enabled ? 'text-(--ui-accent)' : 'text-(--ui-text-tertiary)'
            ),
            onClick: () => $enabled.set(!enabled),
            children: enabled ? '●' : '○'
          })
        })
      }
    })

    // Settings pane (right sidebar)
    ctx.register({
      id: 'settings-pane',
      area: 'panes',
      title: 'Your Plugin',
      data: { placement: 'right', width: '360px', dock: { pane: 'workspace', pos: 'bottom' }, height: '400px' },
      render: () => {
        useEventListener()
        return jsx(MyComponent, {})
      }
    })

    // ⌘K palette command
    ctx.register({
      id: 'toggle-cmd',
      area: PALETTE_AREA,
      data: {
        id: `${ID}.toggle`,
        action: `${ID}.toggle`,
        label: 'Your Plugin: Toggle',
        keywords: ['plugin', 'toggle'],
        run: () => {
          const next = !$enabled.get()
          $enabled.set(next)
          host.notify({ kind: 'info', message: `Your Plugin ${next ? 'enabled' : 'disabled'}` })
        }
      }
    })
  }
}