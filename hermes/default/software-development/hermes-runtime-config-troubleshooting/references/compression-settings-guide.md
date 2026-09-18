---
title: Hermes Context Compression Settings Reference
version: 1.0.0
source: Hermes Agent config.yaml + empirical testing
---

# Compression Settings Guide

## Parameter Definitions

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `compression.threshold` | 0.6 | 0.1-0.95 | Fraction of context window used before summarization triggers |
| `compression.target_ratio` | 0.75 | 0.1-0.9 | Target context size after summarization (relative to window) |
| `compression.protect_first_n` | 40 | 0-500 | First N messages never summarized (system prompt, user profile, early context) |
| `compression.protect_last_n` | 200 | 0-2000 | Last N messages never summarized (recent conversation) |
| `compression.in_place` | true | bool | Replace messages in-place vs create summary message |
| `compression.abort_on_summary_failure` | true | bool | Fail task if summarization fails |

## How Compression Works

```
Context Window (e.g., 128k tokens for Nemotron)
├── Protected First N (40 default)     ← System prompt, user profile, early task setup
├── Compressible Middle                ← Gets summarized when threshold reached
└── Protected Last N (200 default)     ← Recent conversation, current task state
```

When `used_tokens / max_tokens >= threshold`:
1. Compressible middle is summarized by compression model
2. Result replaces middle section
3. New context size ≈ `target_ratio * max_tokens`

## Recommended Profiles

### Profile A: Default (Chat / Simple Tasks)
```yaml
threshold: 0.6
protect_last_n: 200
protect_first_n: 40
target_ratio: 0.75
```
- Good for: Q&A, short chats, simple lookups
- Risk: Loses mid-conversation nuance in multi-step tasks

### Profile B: Complex Multi-Step Tasks (Coding, Analysis, Research)
```yaml
threshold: 0.8
protect_last_n: 350
protect_first_n: 50
target_ratio: 0.8
```
- Good for: Multi-file edits, long debugging, research synthesis
- Preserves 80% context before summarizing; keeps 350 recent + 50 early messages raw
- Higher token cost but dramatically fewer "where were we?" moments

### Profile C: Maximum Preservation (Critical Tasks)
```yaml
threshold: 0.9
protect_last_n: 500
protect_first_n: 100
target_ratio: 0.85
```
- Good for: Financial analysis, legal review, complex architecture work
- Near-zero summarization until absolutely necessary
- Highest token cost

## Interaction with Fallback Chain

**Critical**: Compression happens *before* fallback. If primary model hits rate limit:
1. Request fails / returns degraded response
2. Fallback model receives *already-compressed* context
3. If compression was aggressive (0.6), fallback gets poor context → compounds errors

**Fix**: Raise threshold *and* add fallback. They're complementary.

## Token Cost Estimate

| Profile | Approx. Tokens Preserved Raw | Summarization Frequency |
|---------|------------------------------|-------------------------|
| Default (0.6) | ~240 messages | Every ~40% of window |
| Complex (0.8) | ~400 messages | Every ~20% of window |
| Max (0.9) | ~600 messages | Every ~10% of window |

Assumes ~300 tokens/message average. Actual varies by content.

## Debugging Compression

```bash
# Check current settings
hermes config get compression.threshold compression.target_ratio compression.protect_first_n compression.protect_last_n

# Monitor compression events (in session)
# Look for "Context compressed" messages in tool output

# Force compression test
hermes config set compression.threshold 0.1  # Triggers immediately
# ... run a few turns ...
hermes config set compression.threshold 0.8  # Restore
```