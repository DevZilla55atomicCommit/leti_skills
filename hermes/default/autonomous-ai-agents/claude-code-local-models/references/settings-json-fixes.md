# Common settings.json Issues & Fixes

## Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `statusLine.command: Expected string, but received undefined` | Missing `type: "command"` and `command` fields | Use valid statusLine schema |
| `statusLine.type: Invalid value. Expected one of: "command"` | Invalid `type` value | Only `type: "command"` is valid |
| Files with errors are skipped entirely | Any invalid setting invalidates entire file | Fix all errors or remove the invalid keys |
| Model from settings.json ignored | Cached model in `~/.claude.json` overrides | Use `--settings '{"model":"..."}'` CLI flag |
| Timeout on first request | Large model loading into VRAM | Use smaller model (qwen3.5:4b) or pre-load |

---

## Invalid vs Valid statusLine

### ❌ INVALID (causes errors)
```json
"statusLine": {
  "enabled": true,
  "showAgentInfo": true,
  "showTokenWarning": true,
  "tokenWarningThresholdPct": 75
}
```

### ✅ VALID (only this works)
```json
"statusLine": {
  "type": "command",
  "command": "~/.claude/statusline.sh",
  "enabled": true
}
```

**Only these 3 fields are allowed:** `type` (required, must be `"command"`), `command` (required, string path to script), `enabled` (optional, boolean).

**Critical finding from session (2026-07-22):** The settings `showAgentInfo`, `showTokenWarning`, `tokenWarningThresholdPct` are **not valid** in the statusLine schema. They cause:
```
statusLine.command: Expected string, but received undefined
statusLine.type: Invalid value. Expected one of: "command"
```
The `tokenWarningThresholdPct: 75` warning must be implemented **inside the custom status line script** (checking `context_window.used_percentage`), not via settings.json.

---

## Model Name Validation

Must match exactly what `ollama list` shows:

```bash
ollama list
# NAME                       ID              SIZE      MODIFIED
# qwen3.5:4b                 0c8faadc50c2    3.4 GB    2 weeks ago
# qwen3.5-32k:latest         1d29337a33aa    6.6 GB    6 weeks ago
```

✅ Valid: `qwen3.5:4b`, `qwen3.5-32k:latest`, `gemma4:12b`
❌ Invalid: `qwen3.5` (missing tag), `qwen3.5-32k` (missing `:latest`), `claude-opus-4` (not in Ollama)

---

## Cached Model Override Workaround

The cached model in `~/.claude.json` always wins over settings.json. Per-invocation fix:

```bash
# Option 1: --settings flag (inline JSON)
claude --settings '{"model":"qwen3.5:4b"}' -p "your prompt"

# Option 2: --settings file (create once, reuse)
echo '{"model":"qwen3.5:4b"}' > /tmp/claude-model.json
claude --settings /tmp/claude-model.json -p "your prompt"

# Option 3: --model flag (highest priority)
claude --model qwen3.5:4b -p "your prompt"
```

---

## First-Load Timeout Prevention

Large models (qwen3.5-32k:latest, qwen3.5-128k:latest, gemma4:12b) take **60-180s to load into VRAM** on first use.

```bash
# Pre-load model into VRAM before running Claude
ollama run qwen3.5-32k:latest "warm up" &
sleep 60  # wait for load
kill $!   # stop warm-up

# Now claude will respond quickly
claude --model qwen3.5-32k:latest -p "task"
```

Or just use smaller models for quick tasks:
- `qwen3.5:4b` — ~3.4GB, loads in seconds, good for code review/fixes
- `qwen3.5:4b` with 32K context still handles most coding tasks

---

## Complete Working settings.json Template

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  },
  "model": "qwen3.5:4b",
  "effortLevel": "medium",
  "promptSuggestionEnabled": false,
  "theme": "dark",
  "verbose": false,
  "switchModelsOnFlag": true,
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "enabled": true
  }
}
```

**Place at:** `~/.claude/settings.json` (global) or `.claude/settings.json` (project)