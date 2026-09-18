# Rate Limits & Constraints Reference

## Hard Limits (Non-negotiable)

| Operation | Limit | Enforcement | Consequence if Exceeded |
|-----------|-------|-------------|-------------------------|
| `vision_analyze` | 20 RPM | 3s minimum sleep between calls | 429 errors, session blocks |
| Downreels.com download | ~10 reels / 40s | 4s delay, batch size 10 | Rate limit, IP block |
| Instagram API | 40 RPM | Via downreels.com | Account ban risk |
| Auto-compression | 500 messages | `hygiene_hard_message_limit` | Uncontrolled growth |

## Soft Limits (Configurable)

| Parameter | Value | Location |
|-----------|-------|----------|
| Batch size | 10 | `auto_processor.py` / `config.yaml` |
| Download delay | 4s | `DOWNLOAD_DELAY` |
| Vision delay | 3s | `VISION_RATE_LIMIT` |
| Retry attempts | 3 | `config.yaml` |
| Backoff max | 30s | `config.yaml` |

## Exponential Backoff Schedule

```
Attempt 1: immediate
Attempt 2: 30s
Attempt 3: 60s
Attempt 4: 120s
Attempt 5: 240s
Attempt 6: 480s
```

## Rate Limit Handling Protocol

```python
# Vision API (hard limit)
await asyncio.sleep(3.0)  # Minimum 3s between calls
# If 429 received:
async def handle_rate_limit():
    for delay in [30, 60, 120, 240, 480]:
        await asyncio.sleep(delay)
        # retry
```

## Provider-Specific Notes

| Provider | Limit | Notes |
|----------|-------|-------|
| NVIDIA API | 40 RPM | Main chat model |
| NVIDIA (compression) | Variable | Uses `nemotron-mini-4b-instruct` |
| Local Ollama | Unlimited | But no vision model fits 16GB |
| Downreels.com | ~2.5/sec | Zero-auth, scrapes Instagram |

## Session 2025-07-24 Observations

- **Vision calls**: ~1,167 calls for 389 reels × 3 frames = 389 × 3 = 1,167
- **Time at 20 RPM**: 1,167 / 20 = ~58 minutes minimum
- **Actual time**: ~2 hours (includes download, extract, overhead)
- **Auto-compression failure**: Config pointed to local Ollama for NVIDIA model → silent failure → 1,014 messages unchecked

## Fix for Auto-Compression

```yaml
# ~/.hermes/config.yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: https://integrate.api.nvidia.com/v1  # NOT local!
    enabled: true
    threshold: 0.7
```