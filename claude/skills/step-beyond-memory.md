---
name: step-beyond-memory
description: |
  Memory wrapper skill for Hermes Agent's step-beyond memory system.
  Instructs the LLM to emit <memory-update> blocks when learning facts,
  preferences, or constraints that should persist across sessions.
  Follows the SPEC.md normative behavior from the step-beyond skill.
category: memory
version: "1.0.0"
---

# Step-Beyond Memory Skill

This skill enables persistent memory across Claude Code invocations via the `claude-with-memory` wrapper.

## Memory Update Protocol

When you learn something that should persist across sessions — facts about the user, preferences, constraints, project context, or your own behaviors — emit a `<memory-update>` block in your response:

```xml
<memory-update>
{
  "target": "user|agent",
  "entries": [
    {
      "content": "User prefers dark mode in their IDE",
      "source": "conversation",
      "timestamp": "2025-07-21T14:30:00Z",
      "kind": "preference",
      "scope": "persistent"
    }
  ]
}
</memory-update>
```

### Fields

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `target` | Yes | `"user"` \| `"agent"` | Which memory store to update |
| `content` | Yes | string | The fact/preference/constraint to remember |
| `source` | Yes | `"conversation"` \| `"observation"` \| `"instruction"` \| `"correction"` | How you learned this |
| `timestamp` | Yes | ISO 8601 UTC | When you learned it (ISO 8601 UTC) |
| `kind` | Yes | `"fact"` \| `"preference"` \| `"constraint"` \| `"context"` \| `"behavior"` | Type of memory |
| `scope` | Yes | `"persistent"` \| `"session"` | Persistence scope |

### Target: `user`
Memories about the user: preferences, constraints, facts about them, project context, communication style, tool preferences, etc.

### Target: `agent`
Memories about yourself: behaviors to adopt/avoid, correction feedback, task patterns, tool preferences, style guidelines.

## Memory Injection

The wrapper injects memory at the start of your prompt as:

```
MEMORY:
User: [user entries...]
Agent: [agent entries...]

---
USER: [your actual prompt]
```

## SPEC.md Normative Behavior (from step-beyond skill)

Per the step-beyond skill SPEC.md:

1. **Emit updates proactively** — When you learn something persistable, emit `<memory-update>` immediately in the same response.
2. **One block per target** — Emit at most one `<memory-update>` per target per response.
3. **Atomic entries** — Each entry is a single atomic fact/preference/constraint.
4. **Timestamp in UTC** — Use ISO 8601 UTC timestamps (e.g., `2025-07-21T14:30:00Z`).
5. **Source honesty** — Use `"conversation"` for user-stated facts, `"observation"` for inferred patterns, `"instruction"` for explicit user instructions, `"correction"` for user corrections.
6. **Scope honestly** — Use `"persistent"` for cross-session facts, `"session"` for transient context.
7. **No fabrication** — Only emit updates for things actually learned in the conversation.

## Example Memory Updates

### User preference
```xml
<memory-update>
{
  "target": "user",
  "entries": [
    {
      "content": "User prefers TypeScript over JavaScript for new projects",
      "source": "conversation",
      "timestamp": "2025-07-21T14:30:00Z",
      "kind": "preference",
      "scope": "persistent"
    }
  ]
}
</memory-update>
```

### Agent behavior correction
```xml
<memory-update>
{
  "target": "agent",
  "entries": [
    {
      "content": "User corrected: prefer explicit type annotations over inference in TypeScript",
      "source": "correction",
      "timestamp": "2025-07-21T14:35:00Z",
      "kind": "behavior",
      "scope": "persistent"
    }
  ]
}
</memory-update>
```

### Project context
```xml
<memory-update>
{
  "target": "user",
  "entries": [
    {
      "content": "Project uses Next.js 14 with App Router and TypeScript strict mode",
      "source": "conversation",
      "timestamp": "2025-07-21T14:40:00Z",
      "kind": "context",
      "scope": "persistent"
    }
  ]
}
</memory-update>
```

## Sync Script

The wrapper automatically calls (non-blocking):
```
python3 /Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory.py --push
```
This syncs local memory to the step-beyond memory platform.

## Usage

```bash
~/.claude/claude-with-memory "Your prompt here" [--model MODEL] [--max-turns N]
```