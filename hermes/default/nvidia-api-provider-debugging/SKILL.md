---
name: nvidia-api-provider-debugging
description: Troubleshoot and diagnose NVIDIA API (NVIDIA NIM) connectivity and authentication issues across Hermes Agent's dual-provider configuration architecture (native vs LiteLLM gateway). Captures patterns for rate limiting, auth header formats, and proxy bypass behavior.
user_preference: This user explicitly prefers native-only NVIDIA provider configuration. LiteLLM gateway causes dual-path conflicts, model switching mid-session, and rate-limit confusion. Always recommend removing LiteLLM config and using direct native provider.
category: software-development
tags: [hermes, providers, nvidia, api-debugging, llm-connectivity]
---

# NVIDIA API Provider Troubleshooting

Hermes supports **two parallel configuration paths** for NVIDIA NIM models: direct native API calls and LiteLLM gateway proxy. This skill documents the debugging patterns for connectivity failures.

## ⚠️ User Preference: Native Provider Only

This user has experienced repeated issues with dual-path configuration (native + LiteLLM gateway). The standard fix is to **remove all LiteLLM NVIDIA configs** and use only the built-in Hermes native provider (`provider: nvidia` in config.yaml). LiteLLM gateway introduces model switching, rate limit conflicts, and auth header mismatches.

See `references/native-only-cleanup.md` for the complete cleanup performed in this session.

## Dual Configuration Paths

### Path 1: Direct Native Provider (config.yaml) — PREFERRED

Used by CLI/TUI sessions when making requests directly to NVIDIA API.

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    # CRITICAL: Use 'Authorization' header with Bearer token format, NOT env var interpolation
    default_model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
    models:
       - nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
       - nvidia/llama-3.1-nemotron-70b-instruct
    name: NVIDIA (native)
    rate_limit_rpm: 35         # Safety buffer (< NVIDIA's actual 40 RPM limit)
    concurrency_limit: 1       # Must be set to prevent burst 429s
    max_retries: 5
    retry_delay: 10
    max_retry_delay: 160
    retry_on:
       - 429
       - 500
       - 502
       - 503
       - 504
    # DO NOT use env var interpolation here for direct auth
    # Wrong: api_key: ${NVIDIA_API_KEY}
    # Correct: Use Authorization header with embedded Bearer token
```

### Path 2: LiteLLM Gateway Proxy (~/.config/litellm/config.yaml) — DEPRECATED for this user

Used by Hermes Gateway (Telegram, Discord, Slack). Gateway runs on port 4000.

```yaml
model_list:
   - model_name: nvidia-nano
     litellm_params:
       model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
       api_key: os.environ/NVIDIA_API_KEY  # Proper env var format for LiteLLM
       api_base: https://integrate.api.nvidia.com/v1
       custom_llm_provider: openai         # Must be 'openai' NOT 'nvidia'
       rpm: 35
       tpm: 100000
       max_parallel_requests: 1

   - model_name: nvidia-ultra
     litellm_params:
       model: nvidia_nim/nvidia/nvidia-llama/ultra*actual-model
       api_key: os.environ/NVIDIA_API_KEY
       api_base: https://integrate.api.nvidia.com/v1
       custom_llm_provider: openai         # Must be 'openai' NOT 'nvidia' (DEPRECATED PATH)
       rpm: 35
       max_parallel_requests: 1

litellm_settings:
  drop_params: true
```

### ⚠️ DEPRECATED for this user: Do not use LiteLLM gateway for NVIDIA models

This user's config should have `model_list: []` in `~/.config/litellm/config.yaml` and no NVIDIA models in any LiteLLM template. The native provider path is the only supported path.

## Common Pitfalls & Solutions

### 🔴 Problem: Connection Failed After Removing LiteLLM Block

**SYMPTOM**: Request returns error or times out after removing `nvidia-litellm` from config.

**CAUSE**: Session using native provider but still referencing env var interpolation in header.

**FIX**: Use proper Authorization header format for direct API calls:

```python
# WRONG ❌: Using api_key with env var interpolation
requests.post("https://api.example.com", headers={"api_key": os.environ["NVIDIA_API_KEY"]})

# CORRECT ✅: Using Bearer token directly
requests.post("https://api.example.com", headers={
    "Authorization": f"Bearer {os.environ['NVIDIA_API_KEY']}",
    "Content-Type": "application/json"
})
```

### 🔴 Problem: Gateway Returns 403 "Authorization Failed" with Valid Key

**SYMPTOM**: Same API key works in direct calls but fails via LiteLLM proxy.

**CAUSE**: Known LiteLLM provider bug for nvidia_nim prefix handling.

**FIX**: Use full model name format:

```yaml
# WRONG ❌
model: z-ai/glm-5.2
custom_llm_provider: openai

# CORRECT ✅
model: nvidia_nim/z-ai/glm-5.2     # Must include 'nvidia_nim/' prefix
custom_lll_provider: openai         # Still set to 'openai', not model name
```

### 🔴 Problem: 429 Rate Limit Errors

**SYMPTOM**: Rapid connection attempts return `rate limited`.

**CAUSE**: Concurrency limit too high OR gateway bypassed entirely.

**FIX**: Ensure concurrent requests ≤ actual provider limits:

```yaml
# Direct native provider: MUST be 1 for NVIDIA NIM
providers.nvidia.concurrency_limit: 1  # Prevent burst 429s from hitting rate limit

# Gateway (LiteLLM): rate limits go by rpm/tpm not concurrency
model_list[0].rpm: 35  # Safety buffer (< actual 40)
```

### 🔴 Problem: Model Switching During Session

**SYMPTOM**: System notifications model changes mid-session (e.g., from qwen3.5 to nvidia/nemotron).

**CAUSE**: Automatic fallback triggered when using LiteLLM gateway instead of direct API.

**FIX**: Remove LiteLLM config for native provider:

```yaml
# Correct pattern for stable native usage:
providers.nvidia:
  api: https://integrate.api.nvidia.com/v1
  # REMOVE this line to prevent fallback behavior:
  # api_key: ${NVIDIA_API_KEY} 

# Also configure fallback separately (NOT from same config section)
fallback_models:
- qwen3.5:4b-mlx
```

**VERIFICATION**: After removing, monitor system notifications — direct NVIDIA usage results in stable model selection without switching.

### 🔴 Problem: Dual-Path Configuration Conflicts (This User's Primary Issue)

**SYMPTOM**: Intermittent connection failures, model switching mid-session (e.g., nemotron → qwen3.5), rate limit errors despite low usage, auth failures with valid keys.

**CAUSE**: Both native provider (`provider: nvidia` in config.yaml) AND LiteLLM gateway (models in `~/.config/litellm/config.yaml`) configured for same NVIDIA API key. Requests route unpredictably through one path or the other.

**FIX**: 
1. Set `model_list: []` in `~/.config/litellm/config.yaml` (disable all LiteLLM models)
2. Remove all NVIDIA model entries from LiteLLM config templates in skills
3. Keep only `provider: nvidia` in `~/.hermes/config.yaml` with explicit `api_key` (not env var interpolation)
4. Ensure `use_gateway: false` (default) in Hermes config
5. Kill any running LiteLLM gateway processes: `pkill -f litellm`
6. Restart Hermes session to reload clean config

### 🔴 Problem: Gateway Not Running for Proxy Requests

**SYMPTOM**: Requests fail silently or timeout when gateway is down.

**CAUSE**: No active LiteLLM proxy on port 4000 to relay requests through.

**NOTE**: This problem is eliminated by using native-only config. Gateway not required.

**FIX**: Ensure gateway is running:

```bash
ps aux | grep "hermes_cli.main gateway run"

# Start gateway if needed
hermes gateway run --replace

# Verify it's listening
lsof -i :4000    # Should see LISTEN binding to 127.0.0.1:4000
```

## Diagnostics Checklist

| Symptom | Check This | Command |
|---------|-------------|---------|
| No connection at all | Gateway proxy status | `ps aux \* hermes gateway run` |
| Rate limiting errors (429) | Concurrency limits match actual limit | Verify `concurrency_limit: 1` |
| Auth failures even with valid key | LiteLLM model name format in config | Check for `nvidia_nim/` prefix |
| Session switch mid-flight | Double API vs gateway auth | Review which path session takes |
| Gateway returns error silently | Error messages in logs | `tail -100 ~/.config/litellm/logs/gateway.log` |
| Dual-path conflicts (model switching, auth failures, 429s) | Both native + LiteLLM configured | Disable LiteLLM NVIDIA models; use native only |

## Cognee Hybrid Memory: NVIDIA NIM for Extraction (Verified 2025-07-16)

For local-first setups where Ollama models lack structured output support, use **NVIDIA NIM** *only for the `cognify()` extraction step* while keeping embeddings and storage local.

### Architecture

| Component | Provider | Model | Location |
|-----------|----------|-------|----------|
| **Embeddings** | Local Ollama | `nomic-embed-text:latest` | Mac mini |
| **Graph Extraction** | NVIDIA NIM | `meta/llama-3.1-8b-instruct` | Cloud (your API key) |
| **Graph Storage** | Local Kuzu + LanceDB | — | Mac mini |
| **Session Memory** | Local SQLite | — | Mac mini |

### Working `.env`

```bash
# LLM (chat)
LLM_PROVIDER=ollama
LLM_MODEL=qwen3.5:4b
LLM_ENDPOINT=http://localhost:11434/v1
LLM_API_KEY=dummy
LLM_INSTRUCTOR_MODE=json_mode

# NEW: Extraction via NVIDIA NIM (used ONLY by cognify)
LLM_EXTRACTION_PROVIDER=nvidia_nim
LLM_EXTRACTION_MODEL=meta/llama-3.1-8b-instruct
LLM_EXTRACTION_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_EXTRACTION_API_KEY=nvapi-...

# Embeddings (local, MUST use /api/embed)
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

COGNEE_SKIP_CONNECTION_TEST=true
```

### Cost

| Operation | Model | Cost |
|-----------|-------|------|
| Graph extraction per doc | `meta/llama-3.1-8b-instruct` | ~$0.00015 / 1K tokens |
| Typical note (1 page) | ~2K tokens | **~$0.0003** |
| Full vault (557 notes) | ~500K tokens | **~$0.075** |

### Verified Function Calling on NIM

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer nvapi-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [{"role": "system", "content": "Return only valid JSON via function call."}, {"role": "user", "content": "Extract entities and relationships as JSON with fields: entities (array of strings), relationships (array of objects with subject, predicate, object). Text: Alfred prefers concise responses."}],
    "tools": [{"type": "function", "function": {"name": "extract", "description": "Extract entities and relationships", "parameters": {"type": "object", "properties": {"entities": {"type": "array", "items": {"type": "string"}}, "relationships": {"type": "array", "items": {"type": "object", "properties": {"subject": {"type": "string"}, "predicate": {"type": "string"}, "object": {"type": "string"}}}}}}]}],
    "tool_choice": {"type": "function", "function": {"name": "extract"}},
    "max_tokens": 300,
    "temperature": 0
  }'
```

**Returns:** Valid `tool_calls` with structured entities/relationships JSON.

### Test Script

```python
# test_cognee_nim.py
import cognee, asyncio, os

os.environ['COGNEE_SKIP_CONNECTION_TEST'] = 'true'

async def test():
    # Graph memory (uses NIM for extraction)
    result = await cognee.remember('Alfred prefers concise, technical responses.')
    print('Graph remember:', result)
    
    results = await cognee.recall('What does Alfred prefer?')
    for r in results:
        print('Graph recall:', r)
    
    # Session memory (no LLM calls)
    result = await cognee.remember('Session test fact.', session_id='test-session')
    print('Session remember:', result)
    
    results = await cognee.recall('What was the test?', session_id='test-session')
    for r in results:
        print('Session recall:', r)

asyncio.run(test())
```

Run: `python test_cognee_nim.py`

---\n\n## Quick Fix Templates

### Template: Native Provider Only Setup (User Standard)

```bash
# 1. Disable LiteLLM NVIDIA models
cat > ~/.config/litellm/config.yaml << 'EOF'
# LiteLLM config disabled per user request - using Hermes built-in NVIDIA provider instead
# Previous NVIDIA NIM configs removed per user request to eliminate dual-path conflicts
model_list: []
litellm_settings:
  drop_params: true
EOF

# 2. Kill any running LiteLLM gateway
pkill -f litellm 2>/dev/null || true

# 3. Verify Hermes config uses native provider only
grep -A 10 "^  nvidia:" ~/.hermes/config.yaml

# 4. Restart Hermes session to reload config
```

### Template: Native Provider Only Setup

```bash
# 1. Edit config.yaml (remove or comment nvidia-litellm section)
nano ~/.hermes/config.yaml

# 2. Verify only native provider configured
grep -A 15 "^  nvidia:" ~/.hermes/config.yaml | grep -v "nvidia-litellm" | head -20 >> ~/.bashrc

# 3. Restart session for config reload
hermes-cli gateway restart --replace && hermes-cli gateway restart
```

### Template: Verify Direct API Connectivity

```python
import requests

headers = {
     "Content-Type": "application/json",
     "Authorization": f"Bearer YOUR_NVIDIA_API_KEY",  # Use 'Bearer' not 'api_key'
     "Accept": "application/json"
}

try:
    r = requests.get("https://integrate.api.nvidia.com/v1/models", headers=headers, timeout=5)
    print(f"✓ Direct API reachable: {r.status_code}")
except Exception as e:
    print(f"✗ Direct API failed: {e}")
```

### Template: Verify No Dual-Path Conflict

```bash
# Should return empty model_list
cat ~/.config/litellm/config.yaml

# Should show only native provider
grep -A 8 "^  nvidia:" ~/.hermes/config.yaml
```

## TTS Provider Configuration (This Session)

User configured ElevenLabs TTS with British Lady voice for Hermes voice output.

### ElevenLabs Config in `~/.hermes/config.yaml`
```yaml
tts:
  provider: elevenlabs
  use_gateway: true
  elevenlabs:
    voice_id: GbqQP1rsVFijH3q1FXHV    # British Lady (British English, female)
    model_id: eleven_multilingual_v2
```

### API Key in `~/.hermes/.env`
```bash
ELEVENLABS_API_KEY=<user_provided_key>
```

### Voice Selection Rationale
- **Voice**: "British Lady" (GbqQP1rsVFijH3q1FXHV) — British English, female, professional tone
- **Model**: `eleven_multilingual_v2` — supports 29 languages including English
- **Free tier**: 10,000 characters/month (~20-30 short responses)
- **Fallback**: Edge TTS (free, unlimited) if ElevenLabs quota exceeded

### Edge TTS Fallback Config (Optional)
```yaml
# In ~/.hermes/config.yaml under tts:
edge:
  voice: en-GB-SoniaNeural    # British female, similar style
  rate: "+0%"
  pitch: "+0Hz"
```

### Test Verification
```bash
# Direct ElevenLabs API test (venv Python)
~/.hermes/hermes-agent/venv/bin/python -c "
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
audio = client.text_to_speech.convert(
    voice_id='GbqQP1rsVFijH3q1FXHV',
    model_id='eleven_multilingual_v2',
    text='Hello! This is a test of the ElevenLabs text to speech integration with Hermes Agent.',
)
with open('/tmp/test_elevenlabs.mp3', 'wb') as f:
    for chunk in audio:
        f.write(chunk)
print('Audio saved, size:', os.path.getsize('/tmp/test_elevenlabs.mp3'))
"
# Result: 84 KB MP3 generated successfully

# Hermes TTS tool test
ELEVENLABS_API_KEY=<key> ~/.hermes/hermes-agent/venv/bin/python -c "
from tools.tts_tool import text_to_speech_tool
import json
result = text_to_speech_tool(text='Hello! This is a test of the ElevenLabs text to speech integration with Hermes Agent.')
print(json.dumps(result, indent=2))
"
# Result: success=true, file_path=/Users/alfredkamisese/.hermes/cache/audio/tts_20260710_171203.mp3, media_tag=MEDIA:...
```

## Final Recommendations for This User

### LLM Daily Driver
- **Ollama `nemotron-3-nano:4b`** (~2.8 GB, ~30-50 tok/s) — fast, low RAM, strong reasoning
- **Ollama `qwen2.5:14b`** (~9 GB, ~30 tok/s) — stronger coding, fits 16GB with headroom

### Experimental Only
- **TurboQuant-MLX streaming MoE** — impressive tech demo, not practical daily driver on 16GB M2 (disk-bound)
- **Native NVIDIA API** — Use Hermes native provider for Nemotron-3-Ultra/Super via NVIDIA NIM (cloud), not local

### TTS
- **Primary**: ElevenLabs free tier with British Lady voice
- **Fallback**: Edge TTS (en-GB-SoniaNeural) if character limit exceeded
- **Auto-switch**: Not configured — user monitors usage manually

### NVIDIA NIM Model Availability (Account S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw)
**Tested 2025-07-10** — See `references/nvidia-nim-model-availability.md` for full matrix

| Category | Models |
|----------|--------|
| ✅ Working NVIDIA chat (11) | nemotron-3-ultra/super/nano/mini, llama-3.3-nemotron-super, nemotron-nano-12b-vl, nvidia-nemotron-nano-9b-v2, nemotron-3/3.5-content-safety, nemotron-content-safety-reasoning-4b, **google/diffusiongemma-26b-a4b-it** |
| ✅ Working partner chat (6) | meta/llama-3.1-70b/8b-instruct, meta/llama-3.2-11b/90b-vision-instruct, google/gemma-2-2b-it, qwen/qwen3.5-122b-a10b |
| ⏱️ Timeout (7) | nemotron-3-nano-omni, llama-3.1-nemotron-nano-8b, llama-3.3-70b, llama-3.2-1b/3b, phi-4-mini |
| ❌ 404/Unavailable (14) | nemotron-4-340b, nemotron-70b/ultra-253b, mistral-nemo-minitron, nemotron-nano-3-30b, mistral-7b/mixtral-8x7b/large-2, granite-3.0-8b, gemma-3-12b, deepseek-v4-flash, phi-3.5-moe |
| 🔧 Embeddings (2) | nv-embed-v1, llama-nemotron-embed-1b-v2 |
| 🔧 Special format (2) | nemotron-parse, nemoretriever-parse (require document input) |

**Total tested: 42 models**

### Auxiliary Model Configuration (Added This Session)
All auxiliary functions now configured with tested working models:

| Function | Provider | Model | Timeout | Rationale |
|----------|----------|-------|---------|-----------|
| **web_extract** | nvidia | `meta/llama-3.1-8b-instruct` | 360s | Fast extraction/summarization (~12ms TTFT) |
| **compression** | nvidia | `nvidia/nemotron-mini-4b-instruct` | 120s | Tiny, instant summarization |
| **skills_hub** | nvidia | `nvidia/nemotron-mini-4b-instruct` | 30s | Quick skill matching |
| **approval** | nvidia | `nvidia/nemotron-mini-4b-instruct` | 30s | Fast yes/no decisions |
| **mcp** | nvidia | `nvidia/nemotron-mini-4b-instruct` | 30s | Tool call classification |
| **title_generation** | nvidia | `nvidia/nemotron-mini-4b-instruct` | 30s | Quick title extraction |
| **curator** | nvidia | `nvidia/nemotron-3-nano-30b-a3b` | 600s | Stronger reasoning for curation |

Config applied via `hermes config set` commands — see `references/nvidia-nim-model-availability.md` for full model test results.

## Related Files

- `references/nvidia-dual-config-path.md` — Detailed explanation of two config paths (DEPRECATED for this user)
- `references/litellm-rate-limit-keys.md` — LiteLLM rate limit parameter reference (DEPRECATED for this user)
- `references/litellar-lim-provider-bugs.md` — Documented bugs in LiteLLM's NVIDIA NIM provider (DEPRECATED for this user)
- `references/native-only-cleanup.md` — Step-by-step cleanup performed in this session
- `references/nvidia-nim-model-availability.md` — **Tested model availability matrix for account S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw** — 10 working chat models, 2 timeout models, 6 404 models, 2 embedding models, 2 special-format models. Includes recommended config.yaml and re-verification commands.
- `references/auxiliary-model-config.md` — **Auxiliary function model assignments** — web_extract, compression, skills_hub, approval, mcp, title_generation, curator all configured with tested working models.