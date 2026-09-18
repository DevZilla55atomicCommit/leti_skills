---
name: api-retry-handler
description: "Automatic retry handler with exponential backoff for API rate limits (429) and transient errors (5xx). Wraps API calls with automatic retry and continue prompts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [retry, retry-handler, rate-limit, 429, 5xx, exponential-backoff, api-resilience, auto-retry]
    related_skills: [custom-ai-providers, custom-llm-endpoint-gateway, hermes-agent, systematic-debugging]
---

# API Retry Handler

## Overview

Automatic retry handler with exponential backoff for API rate limits (HTTP 429) and transient server errors (5xx). Designed to wrap AI provider API calls (NVIDIA NIM, OpenAI, Anthropic, etc.) and automatically retry with exponential backoff + jitter, then prompt "continue" to resume from where it left off.

## The Problem

API providers (NVIDIA NIM, OpenAI, Anthropic, etc.) return **HTTP 429 Too Many Requests** after rate limits are exceeded. Default retry logic often gives up after 3 retries, leaving the agent stuck.

## The Solution

This skill provides:
1. **Automatic exponential backoff** with jitter (10s, 20s, 40s, 80s, max 160s)
2. **Automatic "continue" prompt** after backoff completes so the agent resumes
3. **Configurable retry policies** per provider/error type
4. **Drop-in wrapper** for any HTTP-based API client
4. **Hermes cron job** for monitoring and auto-recovery

---

## Quick Start

### 1. Shell Wrapper (Recommended for CLI Tools)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
source ~/.hermes/skills/software-development/api-retry-handler/scripts/api-retry.sh
```

Then use it to wrap any command:

```bash
# Wrap claude-code (sends "continue" via stdin after retries)
api-retry-claude "write a complex function"

# Wrap any command with custom settings
api-retry --max-retries 10 --base-delay 30 -- your-command args

# Wrap curl
api-retry-curl -X POST https://api.example.com/endpoint
```

### 2. Python Decorator (For Your Own Code)

```python
import sys
sys.path.insert(0, '/Users/alfredkamisese/.hermes/skills/software-development/api-retry-handler/scripts')
from retry_decorator import retry_with_backoff, RetryingClient
from openai import OpenAI

# Option A: Decorator on your functions
@retry_with_backoff(max_retries=5, base_delay=10, max_delay=160)
def call_my_api(messages):
    return client.chat.completions.create(messages=messages, ...)

# Option B: Wrapper client (recommended for OpenAI-compatible APIs)
client = RetryingClient(OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key="..."))
response = client.chat.completions.create(model="...", messages=[...])

# Option C: High-level wrapper with provider presets
from api_client_wrapper import APIClientWrapper, create_client_from_env
client = create_client_from_env("nvidia-nim")  # Uses NVIDIA_API_KEY from env
response = client.chat(model="nvidia/nemotron-3-ultra-550b-a55b", messages=[...])
```

### 3. Configure Hermes Agent Provider Retries (Best for Hermes Users)

In your `~/.hermes/config.yaml`, add retry settings to your provider:

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    name: NVIDIA
    # Add these retry settings:
    max_retries: 5
    retry_delay: 10
    max_retry_delay: 160
    retry_on: [429, 500, 502, 503, 504]
```

Then Hermes will automatically retry with exponential backoff!

### 4. Background Monitor (Optional)

```bash
# Run monitor manually
python3 ~/.hermes/skills/software-development/api-retry-handler/scripts/cron_monitor.py --once

# Or create a cron job (runs every 2 min)
hermes cron create \
  --name "api-retry-monitor" \
  --skill "api-retry-handler" \
  --deliver origin \
  "*/2 * * * *" \
  "Run the api-retry monitor: python3 ~/.hermes/skills/software-development/api-retry-handler/scripts/cron_monitor.py --once"
```

---

## Configuration

### Environment Variables

```bash
# Retry configuration
export API_RETRY_MAX_RETRIES=5           # Max retry attempts (default: 5)
export API_RETRY_BASE_DELAY=10           # Base delay in seconds (default: 10)
export API_RETRY_MAX_DELAY=160           # Max delay cap in seconds (default: 160)
export API_RETRY_JITTER=0.2              # Jitter factor 0-1 (default: 0.2 = 20%)
export API_RETRY_ON="429,500,502,503,504" # Comma-separated HTTP codes to retry

# Continue prompt configuration
export API_RETRY_CONTINUE_PROMPT="continue"  # Prompt to send after backoff
export API_RETRY_MAX_CONTINUE=3              # Max continue prompts per session
```

### Per-Provider Config (YAML)

```yaml
# ~/.hermes/skills/software-development/api-retry-handler/config/providers.yaml
providers:
  nvidia-nim:
    base_url: "https://integrate.api.nvidia.com/v1"
    max_retries: 5
    base_delay: 10
    max_delay: 160
    retry_codes: [429, 500, 502, 503, 504]
    headers:
      Authorization: "Bearer ${NVIDIA_API_KEY}"
    continue_prompt: "continue"
    max_continues: 3
  
  openai:
    base_url: "https://api.openai.com/v1"
    max_retries: 3
    base_delay: 5
    max_delay: 60
    retry_codes: [429, 500, 502, 503, 504]
  
  anthropic:
    base_url: "https://api.anthropic.com/v1"
    max_retries: 3
    base_delay: 5
    max_delay: 60
    retry_codes: [429, 500, 502, 503, 504]
  
  ollama:
    base_url: "http://localhost:11434/v1"
    max_retries: 10
    base_delay: 2
    max_delay: 30
    retry_codes: [429, 500, 502, 503, 504]
```

---

## Core Scripts

### 1. retry_wrapper.py — CLI Wrapper

```bash
# Wrap any command with automatic retry
python scripts/retry_wrapper.py \
  --command "curl -X POST https://api.example.com/v1/chat/completions ..." \
  --max-retries 5 \
  --base-delay 10 \
  --max-delay 160 \
  --retry-codes "429,500,502,503,504" \
  --continue-prompt "continue"
```

**Features:**
- Wraps ANY shell command
- Parses stderr/stdout for HTTP error codes
- Exponential backoff with jitter
- Sends "continue" prompt via stdin after backoff
- Logs all attempts to `~/.hermes/logs/api-retry.log`

### 2. retry_decorator.py — Python Decorator

```python
from scripts.retry_decorator import retry_with_backoff

@retry_with_backoff(
    max_retries=5,
    base_delay=10,
    max_delay=160,
    jitter=0.2,
    retry_on=(429, 500, 502, 503, 504),
    continue_prompt="continue",
    on_retry=lambda attempt, delay: print(f"Retry {attempt} in {delay}s...")
)
def call_llm_api(messages, model="nvidia/nemotron-3-ultra"):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096
    )
```

### 3. cron_monitor.py — Background Monitor

```bash
# Run as cron job for background monitoring
python scripts/cron_monitor.py \
  --check-interval 30 \
  --stuck-threshold 60 \
  --recovery-prompt "continue from where you left off"
```

**Monitors:**
- Stuck terminal sessions (no output for N seconds)
- Processes stuck on rate limits
- Sends recovery prompts automatically

---

## Integration with Hermes Agent

### Option 1: Configure Provider Retries in config.yaml (BEST)

Add retry settings directly to your provider config in `~/.hermes/config.yaml`:

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    name: NVIDIA
    # Retry configuration
    max_retries: 5
    retry_delay: 10
    max_retry_delay: 160
    retry_on: [429, 500, 502, 503, 504]
    retry_jitter: 0.2
```

This makes Hermes automatically retry with exponential backoff on 429/5xx errors!

### Option 2: Use the High-Level Python Wrapper

```python
import sys
sys.path.insert(0, '/Users/alfredkamisese/.hermes/skills/software-development/api-retry-handler/scripts')
from api_client_wrapper import APIClientWrapper, create_client_from_env

# Auto-configures from environment (NVIDIA_API_KEY, etc.)
client = create_client_from_env("nvidia-nim")

# Automatic retry with exponential backoff
response = client.chat(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    messages=[{"role": "user", "content": "Complex task that might hit rate limits"}],
    max_tokens=4096
)
```

### Option 3: Decorator for Custom Functions

```python
from retry_decorator import retry_with_backoff

@retry_with_backoff(max_retries=5, base_delay=10, max_delay=160)
def call_llm_with_retry(prompt):
    # Your custom API call
    return your_api_client.generate(prompt)
```

### Option 4: Shell Wrapper for CLI Tools

```bash
# Add to ~/.zshrc or ~/.bashrc
source ~/.hermes/skills/software-development/api-retry-handler/scripts/api-retry.sh

# Then use:
api-retry-claude "your prompt"          # claude-code with stdin continue
api-retry-codex "your prompt"           # codex
api-retry --max-retries 10 -- your-cmd  # Custom command
```

---

## Exponential Backoff Formula

```
delay = min(base_delay * (2 ** attempt) + random_jitter, max_delay)

# With defaults (base=10, max=160, jitter=0.2):
# Attempt 0: 10s  ± 2s  →  8-12s
# Attempt 1: 20s  ± 4s  →  16-24s
# Attempt 2: 40s  ± 8s  →  32-48s
# Attempt 3: 80s  ± 16s →  64-96s
# Attempt 4: 160s ± 32s →  128-160s (capped)
# Attempt 5: 160s ± 32s →  128-160s (capped)
```

---

## Logging

All retry attempts logged to:
```
~/.hermes/logs/api-retry.log
```

Format:
```
2025-01-15 10:30:45 | RETRY | attempt=1/5 | delay=12.3s | error=429 | cmd=claude-code "prompt"
2025-01-15 10:30:57 | RETRY | attempt=2/5 | delay=23.1s | error=429 | cmd=claude-code "prompt"
2025-01-15 10:31:20 | SUCCESS | attempt=3/5 | cmd=claude-code "prompt"
2025-01-15 10:31:20 | CONTINUE_PROMPT_SENT | prompt="continue"
```

---

## Troubleshooting

### Rate Limit Still Hit After Max Retries

```bash
# Increase max retries and delay
export API_RETRY_MAX_RETRIES=10
export API_RETRY_BASE_DELAY=20
export API_RETRY_MAX_DELAY=300

# Or use provider-specific config
```

### Continue Prompt Not Working

```bash
# Check if the target process accepts stdin
# Some CLI tools need explicit --stdin or similar flag
api-retry-wrapper --stdin-prompt "continue" -- claude-code --stdin "prompt"
```

### Cron Job Not Triggering

```bash
# Check cron job status
hermes cronjob list

# View logs
hermes cronjob log api-rate-limit-recovery

# Test manually
python ~/.hermes/skills/software-development/api-retry-handler/scripts/cron_monitor.py --once
```

---

## Related Skills

- `custom-ai-providers` — Configure custom AI providers (NVIDIA NIM, vLLM, etc.)
- `custom-llm-endpoint-gateway` — LiteLLM proxy gateway for unified API
- `hermes-agent` — Hermes Agent configuration
- `systematic-debugging` — Debug API issues systematically

---

## Files

```
api-retry-handler/
├── SKILL.md
├── config/
│   └── providers.yaml
├── scripts/
│   ├── retry_wrapper.py      # CLI wrapper for any command
│   ├── retry_decorator.py    # Python decorator
│   ├── cron_monitor.py       # Background monitor
│   └── api_client_wrapper.py # Wrapper for OpenAI-compatible clients
└── references/
    └── retry-policies.md
```