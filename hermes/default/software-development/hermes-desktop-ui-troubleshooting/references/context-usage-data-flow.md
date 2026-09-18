# Context Usage Data Flow

## Overview

How the Context Meter (`context-usage` statusbar item) gets its data and why it may appear empty.

## Data Pipeline

```
Gateway (TUI) → message.complete event → Desktop message stream → $currentUsage atom → Statusbar render
                    ↓
            session.context_breakdown RPC → ContextUsagePanel dropdown
```

### Required Gateway Events

The desktop's `$currentUsage` atom is updated from **`message.complete` events** (line 812-823 in `gateway-event.ts`):

```typescript
if (payload?.usage) {
  updateSessionState(sessionId, state => ({
    ...state,
    usage: { calls: 0, input: 0, output: 0, total: 0, ...state.usage, ...payload.usage }
  }))
  if (isActiveEvent) {
    setCurrentUsage(current => ({ ...current, ...payload.usage }))
  }
}
```

The `payload.usage` must contain:
- `context_max` — model's context window size
- `context_percent` — percentage used (0-100)
- `context_used` — tokens in current prompt

### Context Breakdown (Dropdown Panel)

When user clicks the context meter, `ContextUsagePanel` calls:
```typescript
requestGateway<ContextBreakdown>('session.context_breakdown', { session_id })
```

Gateway method: `tui_gateway/methods_session.py:1381` → `session.context_breakdown`

Returns `ContextBreakdown`:
```typescript
interface ContextBreakdown {
  categories: ContextUsageCategory[]  // system_prompt, tools, conversation, etc.
  context_max: number
  context_percent: number
  context_used: number
  estimated_total: number
  model: string
}
```

## Platform Differences

| Platform | Emits `message.complete` | Has `session.context_breakdown` | Context Meter Works |
|----------|-------------------------|--------------------------------|---------------------|
| Native Gateway (TUI) | ✅ Yes, with context fields | ✅ Yes | ✅ Full |
| API Server (`/v1/chat/completions`) | ❌ No (emits `run.completed`) | ❌ No | ❌ Empty |
| API Server (`/api/sessions/{id}/chat/stream`) | ❌ No (SSE: `run.completed`) | ❌ No | ❌ Empty |

### API Server Limitation

The API server (`gateway/platforms/api_server.py`) creates agents via `_create_agent()` and runs them via `_run_agent()`. It returns usage in `run.completed`:
```python
usage = {
    "input_tokens": getattr(agent, "session_prompt_tokens", 0) or 0,
    "output_tokens": getattr(agent, "session_completion_tokens", 0) or 0,
    "total_tokens": getattr(agent, "session_total_tokens", 0) or 0,
}
```
But **no `message.complete` event is emitted**, so desktop's `$currentUsage` never gets context fields.

## Debugging Empty Context Meter

1. **Check connection type**: `Settings → Connection → Mode` — must be "Local" (not "Remote" or "Cloud")
2. **Verify gateway running**: Statusbar "Gateway" item should show green "Ready"
3. **Complete a turn**: Data only arrives on `message.complete` after a turn finishes
4. **Check DevTools console**:
   ```javascript
   // In Hermes desktop DevTools (Cmd+Option+I)
   const { $currentUsage } = await import('/src/store/session.ts')
   $currentUsage.get()  // Should show context_max, context_used, context_percent
   ```
5. **Check message stream events**:
   ```javascript
   // In use-message-stream hook, add logging to see event types received
   ```

## Fix Options (For Developers)

1. **Add `message.complete` emission to API server** with context breakdown computed from agent's `context_compressor`
2. **Extend `run.completed` payload** to include context fields, update desktop to read from both event types
3. **Call `session.context_breakdown` from API server** after run completes, include in `run.completed`

## Related Files

- `apps/desktop/src/app/session/hooks/use-message-stream/gateway-event.ts` — Event handling
- `apps/desktop/src/app/shell/hooks/use-statusbar-items.tsx` — Statusbar item creation
- `apps/desktop/src/app/shell/context-usage-panel.tsx` — Dropdown panel
- `gateway/platforms/api_server.py` — API server event emission
- `tui_gateway/methods_session.py` — `session.context_breakdown` method
- `agent/context_breakdown.py` — `compute_session_context_breakdown()`