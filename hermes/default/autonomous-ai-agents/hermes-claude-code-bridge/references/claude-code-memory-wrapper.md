# Claude Code Memory Wrapper Pattern

## Overview

This documents the `claude-with-memory` wrapper built in session 2026-07-21 that provides persistent memory across Claude Code invocations via `<memory-update>` XML blocks.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  ~/.claude/claude-with-memory (Python wrapper)              │
├─────────────────────────────────────────────────────────────┤
│  1. Loads ~/.claude/memory/{user,agent}.json                │
│  2. Formats as MEMORY: prefix for prompt injection          │
│  3. Runs: claude -p "MEMORY: ...\n\nUSER: {prompt}"        │
│  4. Parses response for <memory-update> blocks              │
│  5. Persists new entries to JSON files                      │
│  6. Fires sync script (non-blocking) to Obsidian            │
└─────────────────────────────────────────────────────────────┘
```

## Files

| Path | Purpose |
|------|---------|
| `~/.claude/claude-with-memory` | Executable Python wrapper |
| `~/.claude/memory/user.json` | User facts/preferences/context |
| `~/.claude/memory/agent.json` | Agent behavior corrections/patterns |
| `~/.claude/skills/step-beyond-memory.md` | Skill teaching LLM to emit updates |

## Memory Format

```json
{
  "entries": [
    {
      "content": "User prefers TypeScript over JavaScript for new projects",
      "source": "conversation",
      "timestamp": "2025-07-21T20:30:00Z",
      "kind": "preference",
      "scope": "persistent"
    }
  ]
}
```

## Memory Update Protocol

LLM emits in response:

```xml
<memory-update>
{
  "target": "user",
  "entries": [{
    "content": "User prefers TypeScript over JavaScript for new projects",
    "source": "conversation",
    "timestamp": "2025-07-21T20:30:00Z",
    "kind": "preference",
    "scope": "persistent"
  }]
}
</memory-update>
```

**Fields:**
- `target`: `"user"` or `"agent"`
- `entries`: array of memory objects
- `source`: `"conversation"`, `"observation"`, `"instruction"`, `"correction"`
- `kind`: `"fact"`, `"preference"`, `"constraint"`, `"context"`, `"behavior"`
- `scope`: `"persistent"` or `"session"`

## Usage

```bash
# Basic usage
~/.claude/claude-with-memory "Remember I use Next.js 14 with App Router" --model qwen3.5:4b --max-turns 2

# Skip memory injection
~/.claude/claude-with-memory "Quick question" --no-memory --model qwen3.5:4b

# The wrapper handles:
# - --model (default: qwen3.5:4b)
# - --max-turns (default: 10)
# - --dangerously-skip-permissions (always on)
# - --output-format json (always)
# - --bare (always)
```

## Sync to Obsidian

The wrapper calls (non-blocking):
```bash
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --push
```

This syncs local memory to the step-beyond Obsidian vault.

## Performance Notes (M4 16GB, Ollama)

| Model | Simple Query (~1 turn) | Complex (3-5 turns) |
|-------|------------------------|---------------------|
| `qwen3.5:4b` | 4-6s | 15-30s |
| `gemma4:12b` | ~3s | ~10s |
| `qwen3.5:9b` | 6-8s | 20-40s |

**Recommendation:** Use `--max-turns 1` for memory writes; increase for reasoning tasks.

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Wrapper times out | Ollama inference slow | Increase timeout, reduce max-turns, use faster model |
| No memory updates | LLM didn't emit `<memory-update>` | Skill teaches it; ensure skill is loaded |
| Memory not persisted | JSON write failed | Check file permissions, disk space |

## Session Test Results (2026-07-21)

- ✅ Wrapper executes and returns response
- ✅ Memory injection works (prefixes prompt with MEMORY:)
- ✅ `<memory-update>` parsing implemented
- ✅ JSON persistence works
- ⚠️ Local Ollama slow (4-6s per simple query) — use `--max-turns 1`
- ⚠️ Skill auto-invocation not tested — skill teaches LLM protocol