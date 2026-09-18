# Statusbar Visibility Defaults History

## Change Timeline

### v0.19.1 (July 30, 2026) — Statusbar ON by Default
```typescript
export const $statusbarVisible = persistentAtom(STATUSBAR_VISIBLE_STORAGE_KEY, true, Codecs.bool)
```
- Statusbar visible by default on fresh install
- Individual items still hidden by default in `STATUSBAR_HIDDEN_BY_DEFAULT`

### Post-v0.19.1 (August 2026) — Statusbar OFF by Default (Opt-In)
```typescript
export const $statusbarVisible = persistentAtom(STATUSBAR_VISIBLE_STORAGE_KEY, false, Codecs.bool)
```
Commit: `0b33ee88e4` (part of massive repo restructuring)

**Reasoning (from code comment):**
> Whole-bar visibility, VS Code's `workbench.statusBar.visible`. Off by default — the bar is opt-in. Hiding it unmounts the bar (its 15s status poll goes with it), so the way back is the `view.toggleStatusbar` keybind or the ⌘K row, never the bar itself.

## Current Defaults

| Setting | Default | Storage Key |
|---------|---------|-------------|
| Whole bar visible | `false` | `hermes.desktop.statusbarVisible` |
| Hidden items | All 8 items | `hermes.desktop.statusbarHidden` |

### STATUSBAR_HIDDEN_BY_DEFAULT (8 items)
1. `agents`
2. `approval-mode`
3. `context-usage`
4. `cron`
5. `running-timer`
6. `session-timer`
7. `terminal`
8. `webhooks`

## User Impact

After update to post-v0.19.1:
- **Statusbar completely hidden** unless user toggles it
- **All diagnostic items hidden** even after enabling bar
- Users must: (1) Press `Cmd+Shift+S` to show bar, then (2) Right-click → enable each item

## Toggle Commands

- **Keyboard**: `Cmd+Shift+S` / `Ctrl+Shift+S` → `view.toggleStatusbar`
- **Command Palette**: `Cmd+K` → "Toggle status bar"
- **Right-click bar** → "Customize" → checkbox each item

## Reset to Factory

```javascript
localStorage.removeItem('hermes.desktop.statusbarVisible')
localStorage.removeItem('hermes.desktop.statusbarHidden')
// Reload app (Cmd+R)
```