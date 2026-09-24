# Session Findings — 2026-07-08

## Context
- **User:** Alfred (Maddie)
- **Environment:** macOS, Hermes Agent desktop (TUI), Claude Code v2.1.197 (App Store build)
- **Backend:** Ollama at `http://localhost:11434` with models: `qwen3.5:9b`, `gemma4:12b-mlx`, `gemma4:e4b-mlx`, `qwen3.5:4b-mlx`, `x/flux2-klein:4b`, `nomic-embed-text:latest`, `qwen3.5-128k:latest`, `qwen3.5-64k:latest`, `qwen3.5-48k:latest`, `qwen3.5-32k:latest`

---

## What Worked ✅

### 1. Skill Installation into Claude Code's `~/.claude/skills/`
Created a comprehensive **Code Review Checklist** skill at `~/.claude/skills/code-review-checklist.md` directly via `write_file` (since `claude -p` was timing out). The skill includes 7 review categories with checklists:
- Security Review (injection, auth, secrets, data protection)
- Performance Considerations (DB, caching, resources, frontend)
- Code Quality & Maintainability (structure, naming, error handling, types)
- Testing Requirements (unit, integration, E2E, test quality)
- Documentation Standards (code docs, architecture docs)
- Architecture & Design Patterns (SOLID, common patterns, microservices)
- Git & CI/CD (commit quality, CI pipeline)

Output format specified as structured JSON findings.

### 2. Dynamic Claude Code Binary Path Discovery
Updated verification script to dynamically find current version:
```bash
CLAUDE_BASE="/Users/alfredkamisese/Library/Application Support/claude/claude-code"
CLAUDE_VERSION=$(ls -1 "$CLAUDE_BASE" 2>/dev/null | sort -V | tail -1)
CLAUDE_PATH="$CLAUDE_BASE/$CLAUDE_VERSION/claude.app/Contents/MacOS/claude"
```

### 3. `--workdir` Flag Confirmed Removed in v2.x
Verified: `claude -p "task" --workdir /tmp` returns "unknown option --workdir"
- Use `cwd` in `delegate_task` context instead
- Or `cd` in shell/tmux before running

### 4. Ollama Model Selection
Available models working:
- `qwen3.5:9b` — Balanced (user's running interactive model)
- `qwen3.5:4b-mlx` — Fast, good for simple tasks
- `gemma4:12b-mlx` / `gemma4:e4b-mlx` — Alternative options
- `qwen3.5-128k:latest` — Large context operations

---

## What Didn't Work ❌

### Direct `claude -p` with Ollama Backend
```bash
cd /tmp && claude -p "Create skill..." --model qwen3.5:9b --dangerously-skip-permissions --output-format json --max-turns 8 --bare
```
**Result:** Timed out after 120s (same as 2026-07-05 finding)
**Cause:** Conflict with running interactive instance (SQLite lock contention, model loading)
**Workaround:** Use `delegate_task` for all orchestrator→worker delegation, OR write files directly via Hermes tools

### Simple Test Command Also Hangs
```bash
claude -p "Reply with just: OK" --model qwen3.5:9b --dangerously-skip-permissions --output-format json --max-turns 1 --bare
```
**Result:** Timed out after 60s

---

## Configuration State After Session

### Files Created
- `/Users/alfredkamisese/.claude/skills/code-review-checklist.md` — Comprehensive code review skill

### Updated Skills
- `hermes-claude-code-orchestration` — Added macOS binary path, CLI flags table, print mode hang analysis
- `hermes-claude-code-bridge` — Added same findings
- `hermes-claude-code-orchestration/scripts/verify-orchestration-setup.sh` — Dynamic version detection, removed `--workdir`, dynamic model selection
- `hermes-claude-code-orchestration/templates/delegate-task-template.md` — Removed `--workdir` from all examples

---

## Key Takeaways for Future Sessions

1. **Always use `delegate_task`** for Hermes → Claude Code delegation — avoids interactive instance conflicts
2. **`--workdir` flag is gone** — use `cwd` in `delegate_task` context
3. **Ollama model names must be exact** — no aliases (`sonnet`, `haiku`, `opus` fail)
4. **Print mode with Ollama is unreliable** when user has interactive session — pre-trust workspace or use `delegate_task`
5. **Direct file writes via Hermes tools** work as fallback when Claude Code CLI hangs