# Context Length Override Pitfall — Profile Config vs Model Reality

**Date:** 2026-07-18  
**Session:** `20260717_181054_79863a` (parent) → `20260717_222510_ab6181` (branched)  
**Root Cause:** Global `context_length` override in profile config incorrectly capped nemotron-3-ultra (1M context) to 64K.

---

## The Problem

**Profile config:** `~/.hermes/profiles/default/config.yaml`
```yaml
model:
  default: qwen3.5:4b
  ollama_num_ctx: 65536
  provider: nvidia
  context_length: 65536   # ← BUG: applies to ALL models in this profile
```

This `context_length: 65536` is a **global override** that Hermes applies to *every* model in the profile, including `nvidia/nemotron-3-ultra-550b-a55b` which actually has **1,000,000 token context** via NVIDIA API.

---

## Cascade of Failures

| Layer | What Happened |
|-------|---------------|
| **Context resolution** | `get_model_context_length()` returns 64K (config override wins over NVIDIA API metadata) |
| **Compression threshold** | Profile config: `threshold: 0.75` → compression triggers at 48K tokens (75% of 64K) |
| **Actual session** | Session reached ~217K tokens (4.5× the fake limit) |
| **API call** | NVIDIA returns 400: "maximum context length is 1000000 tokens... you requested 1002223" |
| **Compression cooldown** | Parent session `20260717_181054_79863a` entered cooldown until **2026-07-18 05:23:04** (12h) |
| **Branched session** | `20260717_222510_ab6181` inherits same broken config, same wrong context length |

---

## The Fix

**Remove the incorrect global override** from profile config:

```yaml
# ~/.hermes/profiles/default/config.yaml
model:
  default: qwen3.5:4b
  ollama_num_ctx: 65536
  provider: nvidia
  # context_length: 65536   ← DELETE THIS LINE
```

Or set it correctly per-model (if needed) via `custom_providers` block:
```yaml
custom_providers:
  - name: nvidia
    base_url: https://integrate.api.nvidia.com/v1
    models:
      nvidia/nemotron-3-ultra-550b-a55b:
        context_length: 1000000
```

---

## Why This Happened

1. **Config inheritance**: Profile config merges on top of global config. Profile's `model.context_length` wins.
2. **Legacy artifact**: The `context_length: 65536` was likely copied from an Ollama-only config where `qwen3.5:4b` runs locally with 64K context.
3. **No per-model granularity**: The top-level `model.context_length` is a blunt instrument — it applies to *every* model in the profile, regardless of provider.

---

## Prevention Checklist

- [ ] Never set `model.context_length` globally unless *all* models in the profile share that context window
- [ ] Use `custom_providers[].models[].context_length` for per-model overrides
- [ ] Run `hermes doctor` after config changes — it validates context lengths against known models
- [ ] Verify actual context length with `/model` command in session (shows resolved context)
- [ ] Test compression behavior: manually trigger `/compress` after long session to confirm threshold works

---

## Related Files

- Global config (correct): `~/.hermes/config.yaml` — no `model.context_length` override
- Profile config (buggy): `~/.hermes/profiles/default/config.yaml` — has the bad override
- Skill reference: `references/session-config-nvidia-ollama-2026-07-13.md` — working config from prior session