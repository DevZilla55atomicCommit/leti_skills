---
name: hermes-runtime-config-troubleshooting
description: "Diagnose and fix Hermes Agent runtime configuration issues: fallback provider chains, context compression settings, gateway timeouts, retry policies, and model failover behavior. Class-level troubleshooting patterns for when the agent falls off track mid-task."
version: 1.0.0
license: MIT
author: Alfred (Maddie)
tags:
  - hermes
  - troubleshooting
  - configuration
  - fallback
  - compression
  - debugging
---

# Hermes Runtime Configuration Troubleshooting

Diagnose and fix Hermes Agent runtime configuration issues that cause mid-task failures, context loss, or model hallucination.

## When to Use This Skill

| Symptom | Likely Cause | Primary Check |
|---------|--------------|---------------|
| Model falls off track / hallucinates mid-task | Context compression too aggressive + no fallback | `compression.threshold`, `fallback_providers` |
| Session dies on rate limit / overload | No fallback chain configured | `hermes fallback list` |
| Long tasks timeout | Gateway timeout too short | `agent.gateway_timeout` |
| Retries don't happen | API max retries misconfigured | `agent.api_max_retries` |
| Local model swap loses context | Profile memory not synced | `step-beyond-memory-sync` cron + hooks |

## Core Diagnostic Commands

```bash
# 1. Check fallback chain (CRITICAL - empty = no failover)
hermes fallback list

# 2. Check compression settings
hermes config get compression.threshold compression.protect_last_n compression.protect_first_n compression.target_ratio

# 3. Check gateway/timeouts/retries
hermes config get agent.gateway_timeout agent.api_max_retries agent.service_tier

# 4. Check active model/provider
hermes config get model.default model.provider

# 5. Check memory sync status
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --status
```

## Common Fix Patterns

### Fix 1: Add Fallback Provider Chain (Highest Impact)

```bash
# Add local Ollama as first fallback (free, no rate limits)
hermes fallback add
# Pick: ollama > llama3.2 (or nemotron3-ultra if available locally)

# Add cloud fallback as second tier
hermes fallback add
# Pick: openrouter > anthropic/claude-sonnet-4 (or groq, etc.)

# Verify chain order
hermes fallback list
```

**Why this works**: When primary provider (e.g., NVIDIA Nemotron) hits rate limit/overload, Hermes silently fails or truncates. A local Ollama fallback keeps the session alive with zero API cost.

### Fix 2: Raise Compression Threshold

```bash
# Default 0.6 (60%) is aggressive for complex tasks
hermes config set compression.threshold 0.8
hermes config set compression.protect_last_n 350
hermes config set compression.protect_first_n 50
```

| Threshold | Use Case |
|-----------|----------|
| 0.6 (default) | Short chats, simple Q&A |
| 0.75-0.8 | Multi-step coding, analysis, long context |
| 0.85-0.9 | Maximum context preservation (higher token cost) |

### Fix 3: Extend Gateway Timeout for Long Tasks

```bash
# Default 1800s (30min) - increase for heavy batch jobs
hermes config set agent.gateway_timeout 3600
```

## Diagnostic Decision Tree

```
Model fails mid-task
    |
    +-- Check: hermes fallback list
    |       +-- Empty? > ADD FALLBACK CHAIN (Fix 1) <-- MOST COMMON ROOT CAUSE
    |
    +-- Check: compression.threshold
    |       +-- <= 0.65? > RAISE TO 0.8 (Fix 2)
    |
    +-- Check: agent.gateway_timeout
    |       +-- < 3600 for long tasks? > INCREASE (Fix 3)
    |
    +-- Check: memory sync (step-beyond-memory-sync)
            +-- Cron running? Session hooks installed? > VERIFY SYNC
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `step-beyond-memory-sync` | Bidirectional memory sync (Hermes <-> Obsidian) - survives model swaps |
| `hermes-provider-configuration` | Provider setup, API keys, model selection |
| `debugging-hermes-tui-commands` | TUI slash command debugging |

## References

- `references/fallback-compression-diagnosis.md` - This session's diagnosis: Nemotron primary + no fallback + aggressive compression = mid-task failure
- `references/compression-settings-guide.md` - Detailed compression parameter effects