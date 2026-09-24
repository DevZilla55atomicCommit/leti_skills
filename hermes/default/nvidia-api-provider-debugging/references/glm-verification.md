# GLM Model Verification Guide

## Overview
Use this document to verify that GLM models (e.g., `z-ai/glm-5.2`) work with your NVIDIA NIM setup via direct API calls.

## Verification Steps

### 1. Prepare Your API Key
Ensure you have a valid NVIDIA API key with appropriate permissions.

### 2. Test Model Endpoint

```bash
curl -s -H "Authorization: Bearer YOUR_NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"z-ai/glm-5.2","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' \
  https://integrate.api.nvidia.com/v1/chat/completions --max-time 60
```

### 3. Expected Successful Response
A valid response contains:
- `id`: unique request ID
- `choices`: array with at least one choice
- `choices[0].message`: object with `content`, `role`
- `created`: timestamp
- `model`: model identifier echoed back
- `object`: should be "chat.completion"
- `usage`: token usage statistics

Example:
```json
{
  "id": "chatcmpl-e4ac664b-b5fa-4a27-a91c-12003af9182e",
  "choices": [{
    "index": 0,
    "message": {
      "content": "Hello! How can I help you today?",
      "role": "assistant"
    },
    "finish_reason": "stop"
  }],
  "created": 1783735880,
  "model": "z-ai/glm-5.2",
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 7,
    "completion_tokens": 10,
    "total_tokens": 17
  },
  "finish_reason": "stop"
}
```

### 4. Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| `401` | Invalid or missing API key | Verify `Authorization` header format and key validity |
| `429` | Rate limit exceeded | Reduce request frequency or increase `rpm` limit in config |
| `500`-`504` | Server error | Retry with exponential backoff |
| `404` | Model not found | Check model name spelling and availability in your account |
| `503` | Service unavailable | Wait and retry; check NVIDIA status page |

### 5. Common Pitfalls

- **Missing `Bearer` prefix**: Ensure the token is formatted as `Bearer <token>`.
- **Incorrect header name**: Use `Authorization`, not `api_key` for direct API calls.
- **Model name typo**: Verify exact model identifier as listed in your NVIDIA console.
- **Exceeding max tokens**: Keep `max_tokens` within allowed limits (typically 1-2000).

### 6. Automation Tip
Create a shell script to test multiple models in bulk:

```bash
#!/bin/bash
# test-glm.sh - Test GLM model availability
# Usage: ./test-glm.sh <model-name>

MODEL=$1
if [ -z "$MODEL" ]; then
  echo "Usage: $0 <model-name>"
  exit 1
fi

curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}],\"max_tokens\":10}" \
  https://integrate.api.nvidia.com/v1/chat/completions
```

Make it executable:
```bash
chmod +x test-glm.sh
```

Run tests:
```bash
./test-glm.sh z-ai/glm-5.2
./test-glm.sh meta-llama/llama-3.1-8b-instruct
```