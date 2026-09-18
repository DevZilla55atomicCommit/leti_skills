# Ollama Backend Pitfalls for Claude Code

When using Claude Code with an Ollama backend (ANTHROPIC_BASE_URL=http://localhost:11434), several critical differences from the standard Anthropic API apply.

## Model Aliases Don't Work

**The aliases `sonnet`, `haiku`, `opus` are Anthropic API concepts only.** They do not exist in Ollama.

- ❌ `--model sonnet` → 404 model_not_found
- ❌ `--model haiku` → 404 model_not_found  
- ❌ `--model opus` → 404 model_not_found
- ✅ `--model claude-sonet-4.6:latest` (exact Ollama model name)
- ✅ `--model claude-opus-4.8:latest`
- ✅ `--model qwen3.5:9b`

## Print Mode Hangs on Ollama

Even with correct model names, `claude -p` can hang indefinitely. Workarounds:

1. **Use `--bare` flag** — skips plugins/hooks/MCP discovery for faster startup
2. **Set low `--max-turns`** (1-3 for simple tasks)
3. **Test model first**: `ollama run claude-sonet-4.6:latest "test"`
4. **Use `--output-format json`** for structured result parsing

## Settings Configuration

The backend is controlled by `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_BASE_URL": "http://localhost:11434"
  },
  "model": "qwen3.5:9b",
  "available_models": [
    "gemma4:e4b-mlx",
    "qwen3.5:4b-mlx",
    "gemma4:12b-mlx",
    "qwen3.5-128k:latest",
    "qwen3.5-48k:latest",
    "qwen3.5-32k:latest",
    "nomic-embed-text:latest",
    "qwen3.5-64k:latest",
    "qwen3.5:9b"
  ]
}
```

- Delete the credential you are NOT using instead of blanking it — a blank `"ANTHROPIC_API_KEY": ""` still counts as present and triggers the dual-auth warning. With local Ollama, keep `ANTHROPIC_AUTH_TOKEN` (dummy value) and remove the key entirely (backup first, never print values).

## Project settings.json Schema (launch-blocking)

A malformed project `.claude/settings.json` makes Claude Code refuse to start ('Files with errors are skipped entirely'). Validate before launching:

- Every `hooks.<Event>` entry requires a `matcher` string AND a `hooks` array of `{ "type": "command", "command": "..." }` — a bare `{ "command": ... }` entry is rejected and the whole file is skipped.
- `modelOverrides` and `behavesAs` are not real keys — delete them instead of guessing sibling names.
- Back up the file (`cp settings.json settings.json.bak-<date>`) before editing; settings load at session start, so mid-task edits take effect on the next launch.
- Keep `permissions.deny` narrow — a blanket `Bash` deny blocks builds, tests, and git, which silently stalls any fix task. Deny specific dangerous patterns instead.

## Hermer Orchestration Pattern

When Hermes delegates to Claude Code with Ollama backend:

```python
delegate_task(
    goal="Build auth module with JWT",
    context="Project at ~/myapp. Use claude with --model claude-sonet-4.6:latest --dangerously-skip-permissions --output-format json --max-turns 10 --bare"
)
```

Or via terminal:

```bash
claude -p "Build auth module with JWT" \
  --model claude-sonet-4.6:latest \
  --dangerously-skip-permissions \
  --output-format json \
  --max-turns 10 \
  --bare \
  --workdir ~/myapp
```

## Context Trio Must Match the Loaded Model

The `model` field can name a 96k model while `OLLAMA_CONTEXT_LENGTH`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, and `CLAUDE_CODE_AUTO_COMPACT_WINDOW` still hold another profile's values after a partial switch — the session then hits a phantom limit at the smaller size. Read all four from `settings.json` and confirm agreement; re-run the model switcher instead of hand-editing.

## Uncap Output and Timeouts for Thinking Models

A small `CLAUDE_CODE_MAX_OUTPUT_TOKENS` plus default `api.timeoutMs` strangles long agentic turns: thinking fills the budget and the turn dies before any tool call. Use a generous output cap, `timeoutMs` in the hundreds of seconds, and `maxRetries` of 10 or more.

## Parity-Debug Against a Working Host

When one machine runs the same model fine and another does not, diff `settings.json` (env trio, effort, `modelSettings`, `api` block), `ollama --version`, and the model's sampling params (`ollama show` temperature/top_k/top_p) — then align one variable at a time, cheapest first. Sampling temperature is a first-class suspect for think-forever-never-act loops: a cold model collapses into reasoning ruts while a hot one branches into action.

## Cold Starts Take Minutes

A multi-GB model load plus first-turn prefill over the full skill stack precedes the first tool call. Allow a warmup window of 5+ minutes on 16GB RAM before concluding the loop is stuck — early verdicts misdiagnose loading as paralysis.

## Write-Protect Direction Files on Delegated Builds

Declare generated docs READ-ONLY in project `CLAUDE.md` and step commands — small models otherwise rewrite specs with generic content — and commit a direction baseline first so overwrites show as diffs. Only status/changelog files may change.

## Verified Working Models (from session)

- `claude-sonet-4.6:latest` — primary coding model
- `claude-opus-4.8:latest` — complex reasoning
- `qwen3.5:9b` — fast/lightweight (configured as default)