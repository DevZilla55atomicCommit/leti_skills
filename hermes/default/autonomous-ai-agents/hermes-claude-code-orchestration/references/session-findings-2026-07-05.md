# Session Findings — 2026-07-05

## Context
- **User:** Alfred (Maddie)
- **Environment:** macOS, Hermes Agent desktop (TUI), Claude Code v2.1.197 (App Store build at `~/Library/Application Support/claude/claude-code/2.1.197/claude.app/`)
- **Backend:** Ollama at `http://localhost:11434` with models: `claude-sonet-4.6:latest`, `claude-opus-4.8:latest`, `qwen3.5:9b`, `qwen3.5:4b-mlx`, `gemma4:12b-mlx`, `gemma4:e4b-mlx`, `qwen3.5-128k:latest`, `qwen3.5-64k:latest`, `qwen3.5-48k:latest`, `qwen3.5-32k:latest`, `nomic-embed-text:latest`

---

## What Worked ✅

### 1. `delegate_task` + Print Mode (Primary Orchestrator→Worker Pattern)
```python
delegate_task(
    goal="Create a Python utility file at /tmp/demo_utility.py with calculate_fibonacci(n) and is_prime(n) functions, plus a main demo block",
    context="Working directory: /tmp. Use this exact Claude Code command pattern:\nclaude -p \"Create a Python utility file at /tmp/demo_utility.py with calculate_fibonacci(n) and is_prime(n) functions, plus a main demo block\" --model qwen3.5:4b-mlx --dangerously-skip-permissions --output-format json --max-turns 5"
)
```
**Result:** Created `/tmp/demo_utility.py` successfully with both functions and working demo. Subagent returned structured result.

**Key insight:** `delegate_task` spawns a completely isolated subprocess — avoids conflicts with the user's interactive Claude Code instance running on `s002`.

### 2. Workspace Trust Fix (One-Time Config)
Added to `~/.claude.json`:
```json
"projects": {
  "/Users/alfredkamisese": {
    "hasTrustDialogAccepted": true
  }
}
```
This prevents the "workspace not trusted" hang in print mode.

### 3. Ollama Model Names (Exact Mapping Required)
Claude Code aliases (`sonnet`, `haiku`, `opus`) **do not work** with Ollama backend — they hit Anthropic API and 404.

**Working models from this session:**
- `qwen3.5:4b-mlx` — Fast, good for simple tasks
- `qwen3.5:9b` — Balanced (user's running interactive model)
- `claude-sonet-4.6:latest` — Best general coding
- `claude-opus-4.8:latest` — Complex reasoning

---

## What Didn't Work ❌

### Direct Terminal Commands with `claude -p`
```bash
# These ALL hung (60s timeout):
claude -p "task" --model qwen3.5:4b-mlx --dangerously-skip-permissions --output-format json --max-turns 1
```
**Cause:** Conflict with running interactive instance on `s002` (PID 75738). The print mode subprocess appears to deadlock on shared resources (possibly SQLite session DB or lock files).

**Workaround:** Use `delegate_task` for all orchestrator→worker delegation.

### `--workdir` Flag
```bash
# Invalid flag - not recognized by Claude Code
claude -p "task" --workdir /tmp
```
**Fix:** Use `cwd` parameter in `delegate_task` / `terminal()`, or `cd` in tmux.

---

## Configuration State After Session

### `~/.claude.json` (Updated)
- Added `projects["/Users/alfredkamisese"].hasTrustDialogAccepted: true`
- Already had `projects[...].mcpServers.hermes` configured from prior `claude mcp add hermes`

### `~/.claude/settings.json` (Unchanged)
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "1280000"
  },
  "model": "qwen3.5:4b-mlx",
  "available_models": [...],
  "effortLevel": "medium",
  "verbose": true
}
```

### `~/.claude/settings.local.json` (Unchanged)
```json
{
  "permissions": {
    "allow": [
      "mcp__hermes__messages_read",
      "mcp__hermes-sessions__conversations_list"
    ]
  }
}
```

---

## Recommended Delegate Task Template

```python
delegate_task(
    goal="<specific coding task>",
    context=f"""Project at <path>. Use this exact command:
claude -p "<task description>" \\
  --model qwen3.5:4b-mlx \\        # or claude-sonet-4.6:latest for complex work
  --dangerously-skip-permissions \\
  --output-format json \\
  --max-turns 10"""
)
```

**Model selection guide:**
| Task Type | Model |
|-----------|-------|
| Simple refactor, tests, docs | `qwen3.5:4b-mlx` |
| Feature implementation, API work | `qwen3.5:9b` or `claude-sonet-4.6:latest` |
| Architecture, complex debugging | `claude-opus-4.8:latest` |
| Large file/context operations | `qwen3.5-128k:latest` |

---

## Next Steps for User

1. **In your running Claude Code terminal (s002):**
   ```bash
   claude mcp add hermes -- hermes mcp serve
   ```
   This enables Direction 2: Claude Code → Hermes (MCP client calling Hermes tools)

2. **For future delegations:** Use the `delegate_task` template above with appropriate model.

3. **Trust dialog:** Already fixed for `/Users/alfredkamisese`. Add new projects to `~/.claude.json` as needed.