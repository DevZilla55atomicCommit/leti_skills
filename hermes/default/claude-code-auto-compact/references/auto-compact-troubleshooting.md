# Auto-Compact Troubleshooting with Ollama Proxy

## Common Issues & Fixes

### 1. Token Counting Not Working Through Proxy
When using Ollama as a proxy, token counting may not be accurately reported because:
- The proxy doesn't expose token usage metrics from the local model
- Anthropic's token counting relies on API-level metadata not available in local setups

### 2. Auto-Compact Not Triggering
Symptoms:
- Conversations keep growing until token limits are hit
- No automatic compaction occurs despite high token usage

### 3. Configuration Verification Steps
1. Check current settings with `/status`
2. Verify `CLAUDE_CODE_MAX_OUTPUT_TOKENS` is set to match your model's context window
4. Test with known-small prompts to force compaction
5. Monitor token usage with `claude token-count` (if available)

### 4. Debugging Token Limits
Run these commands to diagnose:
```bash
# Check current effective token limit
grep CLAUDE_CODE_MAX_OUTPUT_TOKENS ~/.claude/settings.json

# Verify model context window
echo "qwen3.5-32k context window: 32768 tokens"

# Test compactability with short prompts
claude compact-test "Short prompt"
```

### 5. Model Not Recognized (Critical)
**Symptom**: `"qwen3.5-48k:latest" isn't described by this version's model catalog` error

**Cause**: Ollama local models aren't in Anthropic's catalog. Must map via `modelOverrides`.

**Fix**: Add to settings.json:
```json
"modelOverrides": {
  "qwen3.5-48k:latest": { "behavesAs": "sonnet" }
}
```
- Use exact model name from `ollama list`
- Map to ONE of: `sonnet`, `haiku`, `opus`
- Do NOT add multiple variants (`ollama/` prefix, without prefix, etc.) — single clean entry works

### 6. Statusline Not Showing
**Symptom**: Default "manual mode" statusline instead of custom

**Causes & Fixes**:
- `statusLine.command` uses absolute path `bash /path/statusline.sh` → Use tilde: `~/.claude/statusline.sh`
- `modelOverrides` has multiple conflicting entries → Keep ONLY one entry per model
- Settings not loaded → Run `/status` to verify
- Extra keys in settings break parsing → Keep settings minimal, match original structure

**New: Inline Braille Donut Charts**
The `claude-code-local-models` skill's `scripts/statusline.sh` now includes inline braille donut charts (⠸⠿⠒⠇) at the far right of each line:
- Line 1: Context donut showing used/total with 8 segments
- Line 2: Tokens donut showing used only with 8 segments
- Colors: green (<60%), magenta (60-74%), yellow (75-89%), red (≥90%)
- Verified segment counts per percentage level

### 7. Auth Issues with Ollama
**Required env vars in settings.json `env` block**:
```json
"ANTHROPIC_BASE_URL": "http://localhost:11434",
"ANTHROPIC_AUTH_TOKEN": "ollama",
"ANTHROPIC_API_KEY": "ollama"
```
- Use `http://localhost:11434` (NOT `/v1` path in BASE_URL)
- Both API_KEY and AUTH_TOKEN must be `ollama`

### 8. Settings Structure Must Match Original
**Pitfall**: Adding extra keys (`model`, `modelOverrides`, `statusLine`) alongside `env` breaks parsing if structure differs from original working config.

**Fix**: Copy the EXACT structure from a known-working `settings.json` and only add/modify needed fields:
```json
{
  "env": { ... },
  "autoCompactEnabled": true,
  "model": "qwen3.5-48k:latest",
  "statusLine": { "type": "command", "command": "~/.claude/statusline.sh" },
  "effortLevel": "medium",
  "promptSuggestionEnabled": false,
  "tui": "fullscreen",
  "theme": "dark",
  "verbose": false,
  "switchModelsOnFlag": true,
  "modelOverrides": { "qwen3.5-48k:latest": { "behavesAs": "sonnet" } }
}
```

### 9. Context Window Recalculation in Statusline
The statusline.sh auto-detects local model context and recalculates true % vs Anthropic's 200K assumption. Verified model context mappings (from `ollama show <model> --parameters | grep num_ctx`):

| Model Pattern | Context Tokens | Notes |
|---------------|----------------|-------|
| `*32k*` / `*4b*` | 32768 | qwen3.5-32k:latest, qwen3.5:4b-mlx |
| `*48k*` | 49152 | qwen3.5-48k:latest |
| `*64k*` / `*9b*` | 65536 | qwen3.5-64k:latest, qwen3.5:9b |
| `*96k*` | 98304 | qwen3.5-96k:latest |
| `*128k*` / `*coder*` | 131072 | qwen3.5-128k:latest, qwen3-coder |
| `*:cloud*` / `*flash*` / `*nemotron*` / `*glm*` | 200000 | Cloud models (gemma4:31b-cloud, deepseek-v4-flash, nemotron-3-ultra, glm-5.2) |

**Fix**: Statusline now correctly maps all variants. Verify detection:
```bash
# Test your model detection
echo '{"model":{"display_name":"qwen3.5-96k:latest"},"context_window":{"used_percentage":50}}' | ~/.claude/statusline.sh
```
- Set `export LOCAL_MODEL_CONTEXT=98304` for precise override if auto-detection fails

### 10. Desktop App vs CLI Settings Drift
The Desktop app reads `~/.claude/settings.json` but:
- **Values may be clamped** — the app enforces a 100k floor on `CLAUDE_CODE_AUTO_COMPACT_WINDOW`; a 65536 value reports as 100k in the app's `/autocompact` message.
- **Stale env in running processes** — settings changes only apply to fresh sessions; the Desktop app's managed worker holds the old trio until quit + reopen.
- **Managed settings can override** — the app injects `--managed-settings` and `--model` flags that may shadow user values. Verify with `/autocompact` in the app session (it names the winning source) before assuming the file governs.
- **Model picker drift** — the app's picker silently loads a different variant than the pinned `model` (e.g., `qwen3.5:9b` at 131k instead of `qwen3.5-96k` at 98k). Always confirm with `curl localhost:11434/api/ps` that the serving model matches the settings trio.

### 11. RAM Pressure on 16 GB Machines
Large local models (9b+ at 128k+ context) consume 6–10 GB VRAM/RAM. On 16 GB:
- `qwen3.5:9b` at 131072 ctx → ~9.4 GB resident → 8% free, heavy swap, model overload errors.
- `qwen3.5-96k` at 98304 ctx → ~6 GB resident → stable headroom for app renderers.
**Rule:** anchor the default model + settings trio to the largest model that leaves ≥20% free RAM. Accept early compaction on larger models when switching via picker; do not size the trio to a model that starves the system.

### 12. Auto Is the Stable Default
Remove `CLAUDE_CODE_AUTO_COMPACT_WINDOW` and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` entirely. Let `auto` tune to whatever model is actually loaded (the app's message: "The auto setting picks a window tuned for your model and is strongly recommended"). This eliminates the half-finished-switch problem (four keys on old size, one on new) and survives model-picker drift. Keep `MAX_OUTPUT_TOKENS` modest (16384) so the output reserve doesn't eat the trigger.