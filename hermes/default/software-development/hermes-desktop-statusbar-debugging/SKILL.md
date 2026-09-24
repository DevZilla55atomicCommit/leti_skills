---
name: hermes-desktop-statusbar-debugging
description: "Debug missing Hermes desktop statusbar via gateway events."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [desktop, statusbar, debugging, context-usage, gateway-events]
    related_skills: [inspecting-hermes-desktop-dom, hermes-agent, systematic-debugging]
---

# Hermes Desktop Statusbar Debugging

## When to Use

- User reports "missing status lines" or "missing Usages bar for context"
- Context usage bar not appearing
- Gateway health / version / connection status items missing
- Trace why `$currentUsage` atom isn't updating with context fields

## Overview

The statusbar reads from several atoms:
- `$currentUsage` → context usage bar + token count (right side)
- `$connection` / `$gatewayState` → gateway health, version, connection (left)
- `$focusedSessionState` → per-session timers, cwd, subagent counts

The **context usage bar** requires `message.complete` gateway events with `usage` containing `context_max`, `context_used`, `context_percent`.

## Critical Architecture: Two Gateway Paths

```
Hermes Desktop App
       │
       ├── Native Gateway (gateway/run)  → message.complete ✅
       └── API Server (api_server)       → message.complete ❌, run.completed ✅
```

**Desktop only processes `message.complete`** for `$currentUsage` (gateway-event.ts:812-823). API server emits `run.completed` but never `message.complete`.

## Diagnostic Checklist

1. Which gateway? `ps aux | grep -E "hermes.*(gateway|api_server)"`
2. Check `$currentUsage` atom in dev console
3. Test `session.context_breakdown` RPC

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Context bar shows only "X tok" | `context_max` missing | Gateway not sending context fields |
| Context bar hidden | No `message.complete` events | API server path |
| Dropdown panel empty | `context_breakdown` RPC failed | No active agent with context_compressor |

## Fix: API Server emits `message.complete`

In `gateway/platforms/api_server.py` `_handle_session_chat_stream`, after `run.completed`:

```python
if hasattr(agent, 'context_compressor') and agent.context_compressor:
    comp = agent.context_compressor
    context_max = getattr(comp, 'context_length', 0) or 0
    context_used = getattr(comp, 'last_prompt_tokens', 0) or 0
    context_percent = max(0, min(100, round(context_used / context_max * 100))) if context_max else 0
    
    await queue.put(_event_payload("message.complete", {
        "session_id": effective_session_id,
        "message_id": message_id,
        "text": final_response,
        "usage": {
            "calls": 1, "input": usage.get("input_tokens", 0),
            "output": usage.get("output_tokens", 0),
            "total": usage.get("total_tokens", 0),
            "context_max": context_max, "context_used": context_used,
            "context_percent": context_percent,
        }
    }))
```

## Key Files

| File | Role |
|------|------|
| `apps/desktop/src/app/shell/hooks/use-statusbar-items.tsx` | Statusbar items (context-usage lines 527-544) |
| `apps/desktop/src/lib/statusbar.tsx` | Formatters: `contextBarLabel`, `usageContextLabel` |
| `apps/desktop/src/app/shell/context-usage-panel.tsx` | Dropdown panel |
| `apps/desktop/src/app/session/hooks/use-message-stream/gateway-event.ts` | Event handler |
| `apps/desktop/src/store/session.ts` | `$currentUsage` atom + `setCurrentUsage` |
| `gateway/platforms/api_server.py` | API server chat handler |
| `tui_gateway/methods_session.py` | `session.context_breakdown` RPC |
| `agent/context_breakdown.py` | `compute_session_context_breakdown()` |

## Verification

1. Start desktop with fixed gateway
2. Open chat, send message
3. Statusbar shows: `[████░░░░░░] 47%` + `128.2K/272K tok`
4. Click dropdown → category breakdown