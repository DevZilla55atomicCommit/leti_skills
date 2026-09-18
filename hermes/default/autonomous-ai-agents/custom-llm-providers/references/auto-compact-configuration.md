# Auto-Compact Configuration Reference

This document captures the auto-compact configuration options for Claude Code, researched from official docs (https://code.claude.com/docs/en/settings) during a session with Alfred (Maddie).

## Settings Keys

| Key | Scope | Default | Description |
|-----|-------|---------|-------------|
| `autoCompactEnabled` | user, project, local | `true` | Enable/disable automatic conversation compaction when context approaches limit. Appears in `/config` as "Auto-compact". |
| `DISABLE_AUTO_COMPACT` | Environment variable | unset | Force-disable auto-compact. Set to any value (e.g., `1`). Overrides all settings scopes. |

## Configuration Examples

### User Scope (`~/.claude/settings.json`) — Explicit Enable
```json
{
  "autoCompactEnabled": true,
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "1280000",
    "DISABLE_TELEMETRY": "1"
  },
  "model": "qwen3.5:4b-mlx",
  "effortLevel": "medium"
}
```

### User Scope — Disable for Manual Control
```json
{
  "autoCompactEnabled": false,
  "env": { ... }
}
```

### Environment Override (Strongest)
```bash
export DISABLE_AUTO_COMPACT=1
```

## Context Health Thresholds

From `/context` command in interactive sessions:

| Usage | State | Action |
|-------|-------|--------|
| < 70% | Normal | Full precision |
| 70-85% | Warning | Precision drops — consider `/compact` |
| > 85% | Critical | Hallucination risk spikes — use `/compact` or `/clear` |

## Best Practices for This User's Workflow

Given the user's setup:
- **Local Ollama** (qwen3.5:4b-mlx) via Hermes
- **128K output tokens** (`CLAUDE_CODE_MAX_OUTPUT_TOKENS=1280000`)
- **40 RPM API limit sensitivity**
- **Preference for local control, manual orchestration**

**Recommendation:** Keep `autoCompactEnabled: true` (default) because:
1. Auto-compact preserves CLAUDE.md and recent context intelligently
2. 128K token window gives generous headroom before compaction triggers
3. Manual `/compact focus on <topic>` is always available for targeted compaction
4. Environment override `DISABLE_AUTO_COMPACT=1` provides escape hatch for long debugging sessions

**Do NOT** set `autoCompactEnabled: false` unless the user explicitly wants full manual control and commits to monitoring `/context` regularly.

## Interactive Commands

| Command | Purpose |
|---------|---------|
| `/context` | Show colored context usage grid with optimization tips |
| `/compact [focus]` | Compress context; optionally focus on a topic (e.g., `/compact focus on auth logic`) |
| `/config` | Open settings UI; toggle "Auto-compact" on/off |
| `/clear` | Wipe conversation history for fresh start |

## Version Notes

- `autoCompactEnabled` in settings.json: Available in v2.1.119+
- Before v2.1.119: Stored in `~/.claude.json` (global config) instead of settings.json
- `/config autoCompactEnabled=true|false`: Available from v2.1.181+ for single-key changes
- `DISABLE_AUTO_COMPACT` env var: Works across all versions