# Auto-Compression Troubleshooting Reference

## Problem Summary
Auto-compression was failing silently or producing minimal reduction because the compression model (`nvidia/nemotron-mini-4b-instruct`) had:
- Context length: 128k (hardcoded in config)
- Output tokens: 1024 (hardcoded)
- Model size: 4B params — insufficient for 900k+ token summaries

## Root Cause
`~/.hermes/profiles/default/config.yaml` had:
```yaml
compression:
  model: nvidia/nemotron-mini-4b-instruct
  context_length: 128000
  extra_body:
    max_tokens: 1024
```
Plus a **critical override** in the global compression block:
```yaml
context_length: 65536  # This forced ALL models to 65k context!
```

## Fix Applied (2025-07-19)
Updated `~/.hermes/profiles/default/config.yaml`:

```yaml
compression:
  provider: nvidia
  model: nvidia/nemotron-3-ultra-550b-a55b  # Main model (550B params)
  timeout: 120
  extra_body:
    temperature: 0.1
    max_tokens: 4096
  enabled: true
  threshold: 0.7
  protect_last_n: 100
  context_length: 1000000  # Matches main model's 1M context
```

Removed the `context_length: 65536` override from the global compression block.

## Result
- **Before**: 998 messages, ~968k tokens → compression failed/minimal
- **After**: 998 → 595 messages, ~968k → ~527k tokens (45% reduction)
- Context bar shows 92% (stale UI) — actual usage ~52%

## Key Lessons
1. **Never set `context_length` on compression config** — it overrides model defaults
2. **Use main model for compression** — only large models can summarize 900k tokens
3. **Max tokens must be ≥ 4096** — 1024 is too small for summaries
4. **Profile config matters** — `~/.hermes/profiles/default/config.yaml` is the source of truth
5. **UI bar lags** — actual token count ≠ UI percentage

## Verification
Run `/compress` in chat — should show significant reduction like:
```
Compressed: 998 → 595 messages
Approx request size: ~968,778 → ~527,097 tokens
```