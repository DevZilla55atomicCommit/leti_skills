# Hermes Auto-Compression Tuning for Step Beyond Workflows
<!-- Reference: Compression settings that preserve Step Beyond reasoning chains -->

## Problem

Default Hermes compression (threshold 0.75, target_ratio 0.6) aggressively summarizes large context windows (49K→30K tokens in one pass). This collapses the **CONTEXT → INTENT → DECIDE → BUILD → INITIATIVE → EXECUTE → VERIFY → DELIVER → LEARN** trace that Step Beyond depends on.

## Recommended Settings (Applied 2026-07-13)

### Primary Compression
```yaml
compression:
  enabled: true
  threshold: 0.60           # Earlier trigger: ~39K tokens (vs 49K)
  target_ratio: 0.75        # Gentler: keep 75% (vs 60%)
  protect_last_n: 200       # More recent context: 200 msgs (vs 150)
  protect_first_n: 40       # Cover skills + system prompt: 40 msgs (vs 20)
  hygiene_hard_message_limit: 500  # More breathing room
  abort_on_summary_failure: true   # Fail safe vs silent loss
  in_place: true
```

### Auxiliary Compression (Summarizer Model)
```yaml
auxiliary:
  compression:
    model: nvidia/nemotron-mini-4b-instruct  # Local Ollama
    base_url: http://127.0.0.1:11434/v1
    threshold: 0.70           # Earlier trigger on 128k ctx = 89.6K tokens
    protect_last_n: 100       # More protection on second pass
    temperature: 0.1
    max_tokens: 1024
```

## Why These Values

| Parameter | Default | Tuned | Rationale |
|-----------|---------|-------|-----------|
| threshold | 0.75 | 0.60 | Smaller, more frequent compressions lose less per pass |
| target_ratio | 0.60 | 0.75 | 25% reduction per pass vs 40% — preserves reasoning chains |
| protect_last_n | 150 | 200 | Step Beyond traces often span 50-100 messages |
| protect_first_n | 20 | 40 | Skills + system prompt + vault context ≈ 30-35 messages |
| abort_on_summary_failure | false | true | Prevents silent corruption of reasoning trace |

## Applying

```bash
hermes config set compression.threshold 0.60
hermes config set compression.target_ratio 0.75
hermes config set compression.protect_last_n 200
hermes config set compression.hygiene_hard_message_limit 500
hermes config set compression.protect_first_n 40
hermes config set compression.abort_on_summary_failure true
hermes config set auxiliary.compression.threshold 0.70
hermes config set auxiliary.compression.protect_last_n 100
```

## Verification

```bash
# Check current config
grep -A 15 "compression:" ~/.hermes/config.yaml

# Watch logs for compression events
tail -f ~/.hermes/logs/agent.log | grep -i compression
```

## Trade-offs

| Gain | Cost |
|------|------|
| Step Beyond traceability preserved | More frequent compression passes |
| Gentler per-pass reduction | Slightly higher average token usage |
| Explicit failure mode | Session pauses if summarizer fails |

For DaVinci/creative/technical workflows with structured reasoning, the gain outweighs the cost.