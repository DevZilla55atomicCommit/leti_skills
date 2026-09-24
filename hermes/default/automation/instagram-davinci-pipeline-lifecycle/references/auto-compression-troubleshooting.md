# Auto-Compression Troubleshooting — Root Cause & Fix

## Problem
Session `20260715_203740_bc494a` grew to **1,014 messages** (2× `hygiene_hard_message_limit: 500`) without auto-compression triggering.

## Root Cause
Misconfigured auxiliary compression model in `~/.hermes/config.yaml`:

```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1   # LOCAL OLLAMA — MODEL NOT PRESENT
    enabled: true
    threshold: 0.7
```

**Problem:** Config points to local Ollama for `nvidia/nemotron-mini-4b-instruct`, but that model doesn't exist locally (only `qwen3.5-4b-compress` is pulled). When compression triggered, it called a non-existent local model → failed silently → `abort_on_summary_failure: true` prevented retry → session grew unchecked.

## Fix Applied
```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: https://integrate.api.nvidia.com/v1  # NVIDIA API directly
    # removed extra_body, timeout, etc. — use defaults
```

**Verified:** `nvidia/nemotron-mini-4b-instruct` IS available on NVIDIA API (confirmed via `/v1/models`).

## Diagnostic Checklist
When auto-compression fails silently:
1. Check `provider` + `base_url` match — model must exist at that endpoint
2. Verify model name in `/v1/models` on the target endpoint
3. Check `auxiliary.compression.enabled: true`
4. Check `compression.threshold: 0.6` (global) vs `0.7` (context_engine) — both must be exceeded
5. Check `abort_on_summary_failure: true` — if true, silent failure = no retry
6. Check `protect_last_n: 200` (global) vs `100` (context_engine) — too much protection delays compression

## Lesson
**Never point NVIDIA provider to local Ollama base_url unless the model is actually pulled there.** Use provider defaults or explicit NVIDIA API URL.

## Session Impact
- 1,014 messages uncompressed
- Context at 95% before manual intervention
- Background processing with `notify_on_complete` proven as workaround for long pipelines