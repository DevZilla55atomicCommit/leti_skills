# Statusbar Item Visibility Control

## Toggle Functions

```typescript
import { 
  $statusbarVisible, 
  toggleStatusbarVisible, 
  $statusbarHiddenIds, 
  setStatusbarItemVisible 
} from '@/store/statusbar-prefs'

// Whole bar
toggleStatusbarVisible()                    // Toggle
$statusbarVisible.set(true)                 // Show
$statusbarVisible.set(false)                // Hide
$statusbarVisible.get()                     // Read current state

// Individual items
setStatusbarItemVisible('context-usage', true)   // Show item
setStatusbarItemVisible('context-usage', false)  // Hide item

// Read hidden IDs
$statusbarHiddenIds.get()  // Returns string[] of hidden item IDs
```

## Default Hidden Items

```typescript
const STATUSBAR_HIDDEN_BY_DEFAULT = [
  'agents',
  'approval-mode', 
  'context-usage',
  'cron',
  'running-timer',
  'session-timer',
  'terminal',
  'webhooks'
]
```

## Common Use Cases

### Enable All Diagnostic Items
```typescript
const diagnosticItems = ['context-usage', 'running-timer', 'session-timer']
diagnosticItems.forEach(id => setStatusbarItemVisible(id, true))
```

### Enable Navigation Items
```typescript
const navItems = ['agents', 'cron', 'terminal', 'webhooks']
navItems.forEach(id => setStatusbarItemVisible(id, true))
```

### Check What's Hidden
```javascript
// In DevTools console
const { $statusbarHiddenIds } = await import('/src/store/statusbar-prefs.ts')
console.log('Hidden:', $statusbarHiddenIds.get())
```

## Persistence

Settings stored in:
- `localStorage.hermes.desktop.statusbarVisible` — boolean
- `localStorage.hermes.desktop.statusbarHidden` — JSON array

Survives app restarts. Clear with:
```javascript
localStorage.removeItem('hermes.desktop.statusbarVisible')
localStorage.removeItem('hermes.desktop.statusbarHidden')
```