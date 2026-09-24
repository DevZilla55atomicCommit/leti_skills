# Claude Code + NVIDIA NIM Debugging Notes

## Session Summary
Attempted to configure Claude Code CLI (v2.1.203) to use NVIDIA NIM hosted endpoint (`https://integrate.api.nvidia.com/v1`) with Nemotron models.

## What Works
- **Direct API calls** via `curl` to NVIDIA endpoint work perfectly
- Models available: `nvidia/nemotron-3-ultra-550b-a55b`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`, etc.
- Hermes Agent already configured and working with NVIDIA provider

## What Fails
**Client-side model validation bug in Claude Code v2.1.x**

Error message:
```
There's an issue with the selected model (nvidia/nemotron-3-nano-omni-30b-a3b-reasoning). It may not exist or you may not have access to it. Run --model to pick a different model.
```

This occurs **even when**:
- `ANTHROPIC_BASE_URL` is set to custom endpoint
- `ANTHROPIC_API_KEY` is set
- `ANTHROPIC_CUSTOM_MODEL_OPTION` is set
- `modelOverrides` maps `sonnet`/`opus` to NVIDIA model IDs
- `available_models` includes `sonnet`/`opus`
- Using `--bare` mode
- Using `--settings` file with `--setting-sources project`
- Using fresh `HOME` directory

## Debugging Attempts (All Failed)

| Approach | Result |
|----------|--------|
| Env vars only (`ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, `ANTHROPIC_CUSTOM_MODEL_OPTION`) | Failed |
| `modelOverrides` in settings.json mapping sonnet/opus → NVIDIA models | Failed |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` / `ANTHROPIC_DEFAULT_OPUS_MODEL` env vars | Failed |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` | Failed |
| `--bare` mode with `--settings` file | Failed |
| `--setting-sources project` | Failed |
| Fresh HOME directory (no cached settings) | Failed |
| `ANTHROPIC_MODEL` env var set to custom model | Failed |
| `--model sonnet` / `--model opus` with overrides | Failed |
| `--fallback-model haiku` | Failed (also validated) |
| `--betas "custom-models"` | Not a valid beta |

## Root Cause
Claude Code's model validator runs **before** checking `ANTHROPIC_BASE_URL`. The code path:
1. Parse model name from settings/env/flags
2. Validate against Anthropic's known model list
3. Only if valid, send request to `ANTHROPIC_BASE_URL`

The docs claim: "On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and behind an LLM gateway or a custom ANTHROPIC_BASE_URL, your provider or gateway defines the model names, so Claude Code passes any string through without checking it."

**This is not implemented correctly in v2.1.203.**

## Working Alternative: Hermes Agent
Hermes Agent's native `nvidia` provider works correctly:
```yaml
# ~/.hermes/config.yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
```

Usage:
```bash
hermes chat -q "Hello" -m nvidia/nemotron-3-ultra-550b-a55b
```

## Recommended Workaround Until Fixed
1. Use Hermes Agent for NVIDIA models (already configured)
2. Report bug to Anthropic: model validation should be skipped when `ANTHROPIC_BASE_URL` != `https://api.anthropic.com`
3. For local development: self-host NIM via Docker and use with Hermes
4. For cloud: use Together.ai / Fireworks which may have better compatibility

## Session Artifacts
- Original Ollama config backed up to `/Users/alfredkamisese/.claude/settings.json.original`
- NVIDIA config backed up to `/Users/alfredkamisese/.claude/settings.json.backup`
- Current settings.json has NVIDIA config with `modelOverrides` for sonnet/opus