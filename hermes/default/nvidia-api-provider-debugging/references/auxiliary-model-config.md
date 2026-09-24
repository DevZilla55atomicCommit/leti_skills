---
title: Auxiliary Model Configuration
applied: 2025-07-10
config_file: ~/.hermes/config.yaml
account: S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw
---

# Auxiliary Model Configuration

Applied via `hermes config set` commands on 2025-07-10. All models verified working on NVIDIA NIM for this account.

## Configuration

```yaml
auxiliary:
  vision:
    provider: nvidia
    model: google/diffusiongemma-26b-a4b-it
    timeout: 120
    download_timeout: 30
  web_extract:
    provider: nvidia
    model: meta/llama-3.1-8b-instruct
    base_url: ''
    api_key: ''
    timeout: 360
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 120
  skills_hub:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 30
  approval:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 30
  mcp:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 30
  title_generation:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: ''
    api_key: ''
    timeout: 30
    language: ''
  curator:
    provider: nvidia
    model: nvidia/nemotron-3-nano-30b-a3b
    base_url: ''
    api_key: ''
    timeout: 600
```

## Model Selection Rationale

| Category | Models | Reason |
|----------|--------|--------|
| **Fast/Small** (compression, skills_hub, approval, mcp, title_generation) | `nvidia/nemotron-mini-4b-instruct` | 4B params, ~80ms response, instant for classification/short tasks |
| **Web Extraction** | `meta/llama-3.1-8b-instruct` | 8B params, ~12ms TTFT, excellent at reading/summarizing |
| **Curator** (complex) | `nvidia/nemotron-3-nano-30b-a3b` | 30B MoE, strong reasoning for curation decisions |
| **Vision** | `google/diffusiongemma-26b-a4b-it` | Diffusion-based LLM, works for image analysis |

## Verification Commands

```bash
# Test web extraction model
curl -s -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{"model":"meta/llama-3.1-8b-instruct","messages":[{"role":"user","content":"Extract key points from: Hello world"}],"max_tokens":20}' \
  https://integrate.api.nvidia.com/v1/chat/completions --max-time 60

# Test compression model
curl -s -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nemotron-mini-4b-instruct","messages":[{"role":"user","content":"Summarize: test"}],"max_tokens":20}' \
  https://integrate.api.nvidia.com/v1/chat/completions --max-time 60
```

## Applied Commands

```bash
hermes config set auxiliary.web_extract.provider nvidia
hermes config set auxiliary.web_extract.model meta/llama-3.1-8b-instruct
hermes config set auxiliary.web_extract.base_url ''
hermes config set auxiliary.web_extract.api_key ''

hermes config set auxiliary.compression.provider nvidia
hermes config set auxiliary.compression.model nvidia/nemotron-mini-4b-instruct
hermes config set auxiliary.compression.base_url ''
hermes config set auxiliary.compression.api_key ''

hermes config set auxiliary.skills_hub.provider nvidia
hermes config set auxiliary.skills_hub.model nvidia/nemotron-mini-4b-instruct
hermes config set auxiliary.skills_hub.base_url ''
hermes config set auxiliary.skills_hub.api_key ''

hermes config set auxiliary.approval.provider nvidia
hermes config set auxiliary.approval.model nvidia/nemotron-mini-4b-instruct
hermes config set auxiliary.approval.base_url ''
hermes config set auxiliary.approval.api_key ''

hermes config set auxiliary.mcp.provider nvidia
hermes config set auxiliary.mcp.model nvidia/nemotron-mini-4b-instruct
hermes config set auxiliary.mcp.base_url ''
hermes config set auxiliary.mcp.api_key ''

hermes config set auxiliary.title_generation.provider nvidia
hermes config set auxiliary.title_generation.model nvidia/nemotron-mini-4b-instruct
hermes config set auxiliary.title_generation.base_url ''
hermes config set auxiliary.title_generation.api_key ''

hermes config set auxiliary.curator.provider nvidia
hermes config set auxiliary.curator.model nvidia/nemotron-3-nano-30b-a3b
hermes config set auxiliary.curator.base_url ''
hermes config set auxiliary.curator.api_key ''
```