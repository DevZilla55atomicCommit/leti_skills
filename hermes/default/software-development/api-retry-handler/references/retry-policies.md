# API Retry Policies Reference

## Overview

This document details the retry policies, backoff strategies, and integration patterns for handling API rate limits and transient errors.

---

## HTTP Status Codes to Retry

| Code | Name | Retry? | Reason |
|------|------|--------|--------|
| **429** | Too Many Requests | ✅ YES | Rate limit exceeded - always retry |
| **500** | Internal Server Error | ✅ YES | Transient server error |
| **502** | Bad Gateway | ✅ YES | Upstream/proxy error |
| **503** | Service Unavailable | ✅ YES | Server overloaded/maintenance |
| **504** | Gateway Timeout | ✅ YES | Upstream timeout |
| 400 | Bad Request | ❌ NO | Client error - won't succeed on retry |
| 401 | Unauthorized | ❌ NO | Auth error - needs credential fix |
| 403 | Forbidden | ❌ NO | Permission error |
| 404 | Not Found | ❌ NO | Resource doesn't exist |
| 408 | Request Timeout | ⚠️ MAYBE | Client timeout - retry with longer timeout |
| 413 | Payload Too Large | ❌ NO | Request too big |

---

## Exponential Backoff Formula

```
delay = min(base_delay × 2^attempt + jitter, max_delay)
```

### Default Values
- `base_delay`: 10 seconds
- `max_delay`: 160 seconds (capped)
- `jitter`: ±20% of calculated delay
- `max_retries`: 5 attempts

### Delay Schedule (default)

| Attempt | Calculated | With Jitter (±20%) | Cumulative |
|---------|------------|-------------------|------------|
| 1 | 10s | 8-12s | ~10s |
| 2 | 20s | 16-24s | ~30s |
| 3 | 40s | 32-48s | ~70s |
| 4 | 80s | 64-96s | ~150s |
| 5 | 160s | 128-160s (capped) | ~310s |
| **Total** | | | **~5.2 minutes** |

### Aggressive Schedule (local models)
- `base_delay`: 2s, `max_delay`: 30s, `max_retries`: 10
- Total: ~2 minutes

### Conservative Schedule (strict rate limits)
- `base_delay`: 30s, `max_delay`: 300s, `max_retries`: 5
- Total: ~15 minutes

---

## Provider-Specific Considerations

### NVIDIA NIM (Free Tier)
- **Rate Limit**: ~32 concurrent requests per model
- **Error**: 503 "Worker local total request limit reached" under load
- **Recommendation**: Use base_delay=10, max_delay=160, max_retries=5
- **Headers**: Check for `Retry-After` header (rarely present)

### OpenAI
- **Rate Limit**: Varies by tier (RPM, TPM)
- **Headers**: Returns `Retry-After` in seconds
- **Recommendation**: Parse `Retry-After` if present, otherwise use exponential backoff

### Anthropic
- **Rate Limit**: Varies by tier
- **Headers**: Returns `retry-after` header (lowercase)
- **Recommendation**: Use `retry-after` value + small buffer

### Together.ai / Fireworks
- **Rate Limit**: Generous, pay-per-token
- **Headers**: Standard `Retry-After` support
- **Recommendation**: Standard exponential backoff works well

### Local (Ollama, vLLM)
- **Rate Limit**: Hardware-bound (GPU VRAM, CPU)
- **Errors**: 503 when queue full, 504 on timeout
- **Recommendation**: Aggressive retries (base=2s, max=30s, retries=10)

---

## Integration Patterns

### Pattern 1: CLI Wrapper (Universal)

```bash
# Wrap any command
api-retry-wrapper --max-retries 5 --base-delay 10 -- your-command args

# With stdin continue prompt (for interactive CLIs)
api-retry-wrapper --stdin-prompt -- claude-code --stdin "your prompt"
```

### Pattern 2: Python Decorator (OpenAI-compatible clients)

```python
from retry_decorator import retry_with_backoff, RetryingClient
from openai import OpenAI

# Option A: Decorator
@retry_with_backoff(max_retries=5, base_delay=10)
def call_api(messages):
    return client.chat.completions.create(messages=messages, ...)

# Option B: Client wrapper (recommended)
client = RetryingClient(OpenAI(base_url="...", api_key="..."))
response = client.chat.completions.create(...)
```

### Pattern 3: Hermes Cron Job (Background Recovery)

```bash
# Create automatic monitoring cron job
hermes cronjob create \
  --name "api-rate-limit-recovery" \
  --schedule "*/2 * * * *" \
  --skills "api-retry-handler" \
  --prompt "Monitor for stuck API calls (429 errors) and send 'continue' prompts to recover"
```

### Pattern 4: Environment-Based Config

```bash
# Global defaults
export API_RETRY_MAX_RETRIES=5
export API_RETRY_BASE_DELAY=10
export API_RETRY_MAX_DELAY=160
export API_RETRY_ON="429,500,502,503,504"

# Per-session override
API_RETRY_MAX_RETRIES=10 api-retry-wrapper -- your-command
```

---

## Continue Prompt Strategy

The "continue" prompt is sent after backoff completes to resume the task.

### When It Works
- **Interactive CLIs**: `claude-code --stdin`, `codex --stdin`, REPLs
- **Hermes Agent**: Native support for continue prompts
- **Custom scripts**: Designed to accept "continue" via stdin

### When It Doesn't Work
- **One-shot commands**: `curl`, `wget`, non-interactive scripts
- **Stateless APIs**: Each request independent

### Custom Continue Prompts

```bash
# Default
--continue-prompt "continue"

# More descriptive
--continue-prompt "continue from where you left off"

# For specific tools
--continue-prompt "please continue the previous task"
```

---

## Monitoring & Observability

### Log Format
```
TIMESTAMP | LEVEL | key=value ...
```

### Log Levels
- `START` - Command started
- `ATTEMPT` - Attempt N of M
- `RETRY` - Rate limit detected, waiting Xs
- `CONTINUE_PROMPT_SENT` - Continue prompt sent
- `SUCCESS` - Command succeeded
- `FAILURE` - Command failed (non-retryable)
- `MAX_RETRIES_EXHAUSTED` - All retries used
- `GIVE_UP` - Non-retryable error

### Key Metrics to Track
1. **Retry rate** - % of calls requiring retries
2. **Recovery rate** - % of retried calls that succeed
3. **Total latency** - Base latency + retry overhead
4. **Continue prompt effectiveness** - % of recoveries that complete

---

## Troubleshooting

### "Continue prompt not working"
- Verify target process accepts stdin
- Check if tool needs `--stdin` or similar flag
- Increase `--max-continues` if multiple prompts needed

### "Still hitting rate limits after max retries"
- Increase `max_retries` and `max_delay`
- Check if multiple concurrent sessions share rate limit
- Consider request batching or spacing

### "Cron job not recovering stuck sessions"
- Check `hermes cronjob list` for job status
- Verify cron job has `api-retry-handler` skill loaded
- Check monitor logs: `~/.hermes/logs/api-retry-monitor.log`

### "Jitter not working"
- Ensure `bc` and `awk` available (for shell wrapper)
- Python version uses `random.uniform()`

---

## Advanced: Custom Retry Logic

### Retry-After Header Parsing

```python
import httpx

@retry_with_backoff(max_retries=5)
def call_with_retry_after(client, *args, **kwargs):
    try:
        return client.chat.completions.create(*args, **kwargs)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            retry_after = e.response.headers.get("Retry-After")
            if retry_after:
                wait_time = int(retry_after) + 1  # Buffer
                time.sleep(wait_time)
                # Retry will happen via decorator
        raise
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure = 0
        self.open = False
    
    def call(self, func, *args, **kwargs):
        if self.open:
            if time.time() - self.last_failure > self.recovery_timeout:
                self.open = False  # Half-open
            else:
                raise CircuitOpenError()
        
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.failure_threshold:
                self.open = True
            raise
```

---

## Related Resources

- [HTTP Retry Patterns (Google Cloud)](https://cloud.google.com/architecture/http-retry-patterns)
- [Exponential Backoff (AWS)](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [OpenAI Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Anthropic Rate Limits](https://docs.anthropic.com/en/api/rate-limits)
- [NVIDIA NIM API Reference](https://docs.nvidia.com/nim/)