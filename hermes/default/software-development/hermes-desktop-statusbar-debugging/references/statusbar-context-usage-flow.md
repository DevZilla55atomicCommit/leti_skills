# Statusbar Context Usage Flow — Desktop Debugging Reference

## The Missing "Usages Bar" Explained

When the user reports "missing status lines" / "missing Usages bar for context" in the Hermes desktop app, they're referring to the **context-usage statusbar item** (right side of statusbar) that shows:
- Visual bar: `[████░░░░░░] 47%`
- Token count: `128.2K/272K tok`
- Dropdown panel with category breakdown (system prompt, tools, conversation, memory, etc.)

## Data Flow Architecture

```
┌─────────────────┐     message.complete (with usage)      ┌──────────────────┐
│  Gateway        │ ──────────────────────────────────────► │  Desktop         │
│  (native/API)   │                                         │  $currentUsage   │
└─────────────────┘                                         │  atom            │
        │                                                   └────────┬─────────┘
        │                                                            │
        │  requestGateway('session.context_breakdown')               ▼
        │ ◄────────────────────────────────────────────────── ContextUsagePanel
        │                                                            │
        ▼                                                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Statusbar Render (use-statusbar-items.tsx)           │
│  - contextUsage = usageContextLabel(currentUsage)  → "128.2K/272K tok"     │
│  - contextBar = contextBarLabel(currentUsage)      → "[████░░░░░░] 47%"    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## The Gap: API Server vs Native Gateway

| Event Type | Native Gateway (`gateway/run.py`) | API Server (`gateway/platforms/api_server.py`) |
|------------|-----------------------------------|------------------------------------------------|
| `message.complete` | ✅ Emitted with full `usage` including `context_max`, `context_percent`, `context_used` | ❌ **Not emitted** |
| `run.completed` | Not used by desktop | ✅ Emitted with basic `usage: {input_tokens, output_tokens, total_tokens}` |
| `session.context_breakdown` RPC | ✅ Works (has live agent with context_compressor) | ⚠️ Works but needs agent with context_compressor |

### Root Cause

The desktop's message stream handler (`gateway-event.ts`) only processes **`message.complete`** events to update `$currentUsage` (lines 812-823). The API server's `_handle_session_chat_stream` emits `run.completed` but **never emits `message.complete`** with context breakdown fields.

The ContextUsagePanel calls `session.context_breakdown` RPC which works against the native gateway (has live agent with `context_compressor.context_length` and `last_prompt_tokens`) but the API server creates transient agents per request.

## Fix Options (Priority Order)

1. **Add `message.complete` emission to API server** after run completes — compute context breakdown from agent's context_compressor and emit `message.complete` with full usage. Desktop pipeline works unchanged.

2. **Extend `run.completed` payload** to include context fields (`context_max`, `context_percent`, `context_used`), then update desktop to read from both event types.

3. **Call `session.context_breakdown` directly from API server** after run completes and include in `run.completed` payload.

## Key Files for Debugging

| File | Purpose |
|------|---------|
| `apps/desktop/src/app/shell/hooks/use-statusbar-items.tsx` | Statusbar item definitions (lines 527-544) |
| `apps/desktop/src/lib/statusbar.tsx` | `contextBarLabel`, `usageContextLabel` formatters |
| `apps/desktop/src/app/shell/context-usage-panel.tsx` | Dropdown panel, calls `session.context_breakdown` |
| `apps/desktop/src/app/session/hooks/use-message-stream/gateway-event.ts` | Handles `message.complete` → updates `$currentUsage` (lines 751-824) |
| `apps/desktop/src/store/session.ts` | `$currentUsage` atom + `setCurrentUsage` (lines 571, 772) |
| `gateway/platforms/api_server.py` | `_handle_session_chat_stream` — emits `run.completed` only (line 3927) |
| `tui_gateway/methods_session.py` | `session.context_breakdown` RPC (line 1381) |
| `agent/context_breakdown.py` | `compute_session_context_breakdown()` (line 89) |

## Quick Verification Commands

```bash
# Check if API server is running (desktop uses this)
curl -s http://127.0.0.1:<port>/health/detailed | jq '.gateway_state'

# Check native gateway status
curl -s http://127.0.0.1:<port>/api/status | jq '.gateway_state, .gateway_running'

# Test context_breakdown RPC (requires active session)
# Via desktop console: requestGateway('session.context_breakdown', {session_id: '...'})
```