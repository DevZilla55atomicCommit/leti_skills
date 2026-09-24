# Session Config Reference: NVIDIA Primary + Ollama Fallback

This file documents the exact configuration applied in the session on 2026-07-13 for Alfred's Hermes setup.

## Final Config State (Relevant Sections)

```yaml
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  ollama_num_ctx: 65536
  provider: nvidia
  ollama_context_length: 65536

providers:
  ollama-launch:
    api: http://127.0.0.1:11434/v1
    default_model: gemma4:12b
    models:
      - gemma4:12b
      - qwen3.5:4b
      - gemma4:e4b
      - nomic-embed-text:latest
      - minicpm-v4.5:8b
      - qwen3.5-32k:latest
      - qwen3.5-48k:latest
      - qwen3.5-64k:latest
      - qwen3.5-128k:latest
      - qwen3-vl:8b
      - x/flux2-klein:4b-fp8
      - qwen3.5-4b-compress
    name: Ollama
  google-gemini:
    api: https://generativelanguage.googleapis.com/v1beta
    api_key: AQ.Ab8RN6LTI8CF0mJTW7veVVy-7GFm_p8sEdin5ES8yNpoMatKQA
    default_model: gemini-2.5-flash-lite
    models:
      - gemini-2.5-flash
      - gemini-2.5-pro
      - gemini-2.5-flash-lite
    name: Gemini
  openrouter:
    api: https://openrouter.ai/api/v1
    api_key: "«redacted:sk-...»"
    default_model: anthropic/claude-sonnet-4.6
    models:
      - anthropic/claude-sonnet-4.6
      - anthropic/claude-opus-4.8
      - openai/gpt-5.5
      - deepseek/deepseek-v4-pro
      - meta-llama/llama-3.3-70b-instruct
    name: OpenRouter
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: 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
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    name: NVIDIA

fallback_providers:
  - provider: ollama-launch
    model: qwen3.5:4b

auxiliary:
  vision:
    provider: nvidia
    model: google/diffusiongemma-26b-a4b-it
    timeout: 120
    download_timeout: 30
    context_length: 64000
  web_extract:
    provider: nvidia
    model: meta/llama-3.1-8b-instruct
    timeout: 360
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1
    timeout: 120
    extra_body:
      temperature: 0.1
      max_tokens: 1024
    enabled: true
    threshold: 0.85
    protect_last_n: 60
    context_length: 128000
  skills_hub:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    timeout: 30
  approval:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    timeout: 30
  mcp:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
  title_generation:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    timeout: 30
    language: ''
  tts_audio_tags:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 30
  triage_specifier:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 120
  kanban_decomposer:
    provider: nvidia
    model: nvidia/nemotron-3-nano-30b-a3b
    base_url: ''
    api_key: ''
    timeout: 180
  profile_describer:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 60
  curator:
    provider: nvidia
    model: nvidia/nemotron-3-nano-30b-a3b
    timeout: 600
  monitor:
    provider: auto
    model: ''
    base_url: ''
    api_key: ''
    timeout: 60
  background_review:
    provider: auto
    model: ''
    base_url: ''
    api_key: ''
    timeout: 120
  moa_reference:
    provider: auto
    model: ''
    base_url: ''
    api_key: ''
    timeout: 600
  moa_aggregator:
    provider: auto
    model: ''
    base_url: ''
    api_key: ''
    timeout: 600
```

## Key Decisions Made

1. **Primary**: NVIDIA NIM with Nemotron 3 Ultra (550B) — highest quality, cloud-hosted
2. **Fallback**: Local Ollama with qwen3.5:4b — runs offline, no API costs
3. **Auxiliary**: All routed to NVIDIA for consistency (uses same API key), with mini/nano models for speed
   - Vision: google/diffusiongemma-26b-a4b-it (multimodal)
   - Web extract: meta/llama-3.1-8b-instruct (fast instruct)
   - Compression: nvidia/nemotron-mini-4b-instruct (small, fast)
   - Complex decomposers (kanban, curator): nvidia/nemotron-3-nano-30b-a3b (more capable)

## Commands Used

```bash
# Set primary model + provider
hermes config set model.default nvidia/nemotron-3-ultra-550b-a55b
hermes config set model.provider nvidia

# Set fallback (required Python YAML for proper array syntax)
python3 -c "
import yaml
with open('/Users/alfredkamisese/.hermes/config.yaml') as f:
    c = yaml.safe_load(f)
c['fallback_providers'] = [{'provider': 'ollama-launch', 'model': 'qwen3.5:4b'}]
with open('/Users/alfredkamisese/.hermes/config.yaml', 'w') as f:
    yaml.dump(c, f, default_flow_style=False, sort_keys=False)
"

# Set auxiliary models (batch via Python)
# (see session transcript for full script)
```