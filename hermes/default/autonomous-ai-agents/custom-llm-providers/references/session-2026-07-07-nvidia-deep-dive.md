# Session 2026-07-07: NVIDIA NIM + Claude Code Deep Dive

## Objective
Configure Claude Code CLI to use NVIDIA Nemotron models via NVIDIA NIM hosted endpoint (`https://integrate.api.nvidia.com/v1`).

## Environment
- **Claude Code:** v2.1.203 (installed via npm)
- **OS:** macOS (Apple Silicon)
- **API Key:** `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` (from build.nvidia.com)
- **Models Targeted:**
  - `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` (30B, reasoning)
  - `nvidia/nemotron-3-ultra-550b-a55b` (550B, ultra)

---

## What Works (Verified)

### Direct API Calls (curl)
```bash
# List models
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" | jq '.data[].id' | grep nemotron

# Chat completion (works!)
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nemotron-3-nano-omni-30b-a3b-reasoning","messages":[{"role":"user","content":"Hello"}],"max_tokens":20}'
```

**Result:** ✅ Returns valid OpenAI-format response with reasoning content.

### Hermes Agent (Native)
```yaml
# ~/.hermes/config.yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
```
```bash
hermes chat -q "Hello" -m nvidia/nemotron-3-ultra-550b-a55b
```
**Result:** ✅ Works perfectly.

---

## What Fails (All Attempts)

### The Bug: Client-Side Model Validation
Claude Code validates model names against Anthropic's internal allowlist **before** checking `ANTHROPIC_BASE_URL`. Even with correct env vars and settings, it rejects NVIDIA model names.

**Error:**
```
There's an issue with the selected model (nvidia/nemotron-3-nano-omni-30b-a3b-reasoning). It may not exist or you may not have access to it. Run --model to pick a different model.
```

### All Failed Approaches

| # | Approach | Result |
|---|----------|--------|
| 1 | Env vars only (`ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, `ANTHROPIC_CUSTOM_MODEL_OPTION`) | ❌ |
| 2 | `modelOverrides` in settings.json mapping sonnet/opus → NVIDIA models | ❌ |
| 3 | `ANTHROPIC_DEFAULT_SONNET_MODEL` / `ANTHROPIC_DEFAULT_OPUS_MODEL` | ❌ |
| 4 | `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` | ❌ |
| 5 | `--bare` mode with `--settings` file | ❌ |
| 6 | `--setting-sources project` | ❌ |
| 7 | Fresh `HOME` directory (no cached settings) | ❌ |
| 8 | `ANTHROPIC_MODEL` env var set to custom model | ❌ |
| 9 | `--model sonnet` / `--model opus` with overrides | ❌ |
| 10 | `--fallback-model haiku` | ❌ (also validated) |
| 11 | `--betas "custom-models"` | ❌ (invalid beta) |
| 12 | `ANTHROPIC_CUSTOM_MODEL_OPTION` + `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` + `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` | ❌ |

---

## Root Cause Analysis

**Code Path (inferred):**
1. Parse model name from: CLI flag `--model` → env `ANTHROPIC_MODEL` → settings `model` → default
2. **Validate against Anthropic's hardcoded model list** ← BUG: runs unconditionally
3. If valid, send request to `ANTHROPIC_BASE_URL` (or default `api.anthropic.com`)

**Documentation Claim vs Reality:**
> "On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and behind an LLM gateway or a custom ANTHROPIC_BASE_URL, your provider or gateway defines the model names, so Claude Code passes any string through without checking it."

**Reality:** The check runs **before** the base URL branch. Validation is NOT skipped for custom endpoints in v2.1.203.

---

## Working Alternatives

### 1. Direct API Wrapper (Immediate)
```bash
# ~/.zshrc
nvidia-chat() {
  curl -s https://integrate.api.nvidia.com/v1/chat/completions \
    -H "Authorization: Bearer ***" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"nvidia/nemotron-3-nano-omni-30b-a3b-reasoning\",\"messages\":[{\"role\":\"user\",\"content\":\"$1\"}],\"max_tokens\":500}" \
    | jq -r '.choices[0].message.content'
}
# Usage: nvidia-chat "Explain quantum computing"
```

### 2. Hermes Agent (Already Configured)
```bash
hermes chat -q "Hello" -m nvidia/nemotron-3-ultra-550b-a55b
```

### 3. Switch Back to Ollama (Current Default)
```bash
~/.claude/switch-provider.sh ollama
claude -p "Hello"  # Works with qwen3.5-32k:latest
```

---

## Config Artifacts Saved

| File | Purpose |
|------|---------|
| `~/.claude/settings.json.original` | Original Ollama config (qwen3.5-32k:latest) |
| `~/.claude/settings.json.backup` | NVIDIA test config with modelOverrides |
| `~/.claude/settings.nvidia.json` | Ready-to-use NVIDIA config (for when bug fixed) |
| `~/.claude/switch-provider.sh` | Quick-switch script (ollama/nvidia/status) |

---

## NVIDIA Config Template (Ready for Fix)

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "nvapi-...",
    "ANTHROPIC_BASE_URL": "https://integrate.api.nvidia.com/v1"
  },
  "modelOverrides": {
    "sonnet": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    "opus": "nvidia/nemotron-3-ultra-550b-a55b",
    "claude-sonnet-5": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    "claude-opus-4-8": "nvidia/nemotron-3-ultra-550b-a55b"
  },
  "model": "sonnet",
  "available_models": ["sonnet", "opus"]
}
```

---

## Next Steps

1. **Report bug** to Anthropic: https://github.com/anthropics/claude-code/issues
   - Title: "Model validation not skipped for custom ANTHROPIC_BASE_URL (v2.1.203)"
   - Include: Error message, env vars tested, docs quote contradicting behavior

2. **Monitor releases** — fix likely in v2.1.204+

3. **When fixed:** Run `~/.claude/switch-provider.sh nvidia` and test `claude --model sonnet -p "Hello"`

---

## Key Learnings

1. **Always test direct API first** — validates provider works before debugging client
2. **Client-side validation is a real blocker** — not just a "nice to have" check
3. **Hermes handles this correctly** — its provider abstraction bypasses CLI validation
4. **Quick-switch pattern** — useful for any multi-provider workflow (Ollama ↔ NVIDIA ↔ Together.ai)
5. **Documentation can be ahead of implementation** — always verify behavior in your version