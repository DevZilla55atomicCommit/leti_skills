---
session: 2026-07-20
profile: default
primary_model: nvidia/nemotron-3-ultra-550b-a55b
primary_provider: nvidia
issue: "Model falls off track / hallucinates mid-task after hitting rate limit or connection flag"
root_cause: "No fallback provider chain configured + aggressive context compression (threshold=0.6)"
---

# Session Diagnosis: Nemotron Primary + No Fallback + Aggressive Compression

## Configuration Found (2026-07-20)

```yaml
# ~/.hermes/config.yaml - relevant sections
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  provider: nvidia

fallback_providers: []  # EMPTY - NO FAILOVER

compression:
  enabled: true
  threshold: 0.6        # 60% - aggressive
  protect_last_n: 200   # only last 200 messages protected
  protect_first_n: 40   # only first 40 messages protected
  target_ratio: 0.75
  abort_on_summary_failure: true

agent:
  gateway_timeout: 1800
  api_max_retries: 3
```

## Symptoms Observed

1. **Mid-task model degradation** - After NVIDIA free-tier rate limit hit, model responses become incoherent/hallucinated
2. **No graceful failover** - Empty `fallback_providers` means request fails hard or returns truncated garbage
3. **Context compression amplifies the problem** - At 60% threshold, mid-conversation context gets summarized aggressively; when model quality drops, summaries compound errors
4. **User must manually disable fallback** - "I have to disable it" = no usable fallback exists

## Fix Applied (Priority Order)

| Priority | Action | Command | Expected Result |
|----------|--------|---------|-----------------|
| 1 | Add Ollama local fallback | `hermes fallback add` → ollama → llama3.2 | Zero-cost failover, no rate limits |
| 2 | Add cloud fallback (OpenRouter) | `hermes fallback add` → openrouter → claude-sonnet-4 | Quality fallback when local insufficient |
| 3 | Raise compression threshold | `hermes config set compression.threshold 0.8` | Preserve 80% context before summarizing |
| 4 | Increase protected message windows | `hermes config set compression.protect_last_n 350` + `protect_first_n 50` | More context survives compression |

## Verification Commands

```bash
# Verify fallback chain
hermes fallback list
# Expected: [ollama:llama3.2, openrouter:anthropic/claude-sonnet-4]

# Verify compression settings
hermes config get compression.threshold compression.protect_last_n compression.protect_first_n
# Expected: 0.8, 350, 50

# Test failover manually (pull network cable or hit rate limit)
# Observe: session continues on local model without user intervention
```

## Key Insight

**The 30-min memory sync cron is orthogonal to this problem.** Memory sync persists *user patterns* (Step Beyond profiles) across sessions. Context compression and fallback chains govern *in-session model behavior*. They operate at different layers:

| Layer | Mechanism | Protects Against |
|-------|-----------|------------------|
| Session persistence | `step-beyond-memory-sync` cron + hooks | Model swap, session restart, crash |
| In-session context | `compression.*` settings | Context window overflow |
| In-session availability | `fallback_providers` chain | Provider outage, rate limit, quality degradation |

All three must be configured for robust operation.