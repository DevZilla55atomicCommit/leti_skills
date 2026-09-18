# Print Mode Conflict with Running Interactive Instance

## Problem

When `claude -p` (print mode) is invoked while **another interactive Claude Code instance is running** (e.g., user's terminal on `s002`), the print mode subprocess **hangs indefinitely** — no output, no error, just deadlock.

## Root Cause

Both processes attempt to access shared resources simultaneously:
- SQLite session database (`~/.claude/sessions/`)
- Lock files / mutexes
- Session persistence mechanisms

The interactive instance holds a lock; the print mode subprocess waits forever.

## Symptoms

```bash
# This hangs 60+ seconds with no output:
claude -p "test" --model qwen3.5:9b --dangerously-skip-permissions --output-format json --max-turns 1

# Stderr shows (after timeout):
# Ignoring 2 permissions.allow entries from .claude/settings.local.json: 
# this workspace has not been trusted. Run Claude Code interactively here once 
# and accept the trust dialog, or set projects["/Users/..."].hasTrustDialogAccepted: true 
# in /Users/.../.claude.json.
```

## Workarounds (in order of preference)

### 1. Use `delegate_task` (Recommended)
The `delegate_task` tool spawns a **fully isolated subprocess** with its own environment, avoiding the shared-resource conflict entirely.

```python
delegate_task(
    goal="Build feature X",
    context="Use: claude -p --model qwen3.5:9b --dangerously-skip-permissions --output-format json --max-turns 10"
)
```

### 2. Kill Interactive Instance First
```bash
pkill -f "claude.*--model"  # Kill user's interactive session
# Then run print mode
```

### 3. Separate User/Profile
Run print mode under a different user or with isolated `HOME`:
```bash
HOME=/tmp/claude-isolated claude -p "task" ...
```

## Session Trust Dialog (Related)

The workspace trust dialog **also blocks print mode** if not accepted interactively first.

### Fix (one-time):
```json
// In ~/.claude.json
"projects": {
  "/your/workspace/path": {
    "hasTrustDialogAccepted": true
  }
}
```

Or run interactively once: `cd /workspace && claude` → press Enter → `/exit`

## Summary

| Scenario | Works? | Solution |
|----------|--------|----------|
| No other Claude running | ✅ | Direct `claude -p` |
| User has interactive session | ❌ Hangs | Use `delegate_task` |
| Workspace not trusted | ❌ Hangs | Add `hasTrustDialogAccepted` or run once interactively |
| Both issues | ❌ Hangs | `delegate_task` handles both |

## Best Practice for Hermes Orchestrator

**Always use `delegate_task` for spawning Claude Code workers** — it avoids both the print mode conflict AND the workspace trust issue by running in an isolated context.