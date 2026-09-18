# Native-Only NVIDIA Cleanup — Session Record

**Date**: 2026-07-10  
**User Directive**: "remove any skills that has to do with litellm also" + "discard litellm for ever using it again as it is messing up our settings in the config.yaml"

## Actions Taken

### 1. Disabled LiteLLM Config
**File**: `~/.config/litellm/config.yaml`
```yaml
# LiteLLM config disabled per user request - using Hermes built-in NVIDIA provider instead
# Previous NVIDIA NIM configs removed per user request to eliminate dual-path conflicts
model_list: []
litellm_settings:
  drop_params: true
```

### 2. Killed LiteLLM Processes
```bash
pkill -f litellm
# Result: No LiteLLM processes running
```

### 3. Removed LiteLLM-Related Skills
Deleted the following skill directories:
- `~/.hermes/skills/mlops/litellm-nvidia-gateway`
- `~/.hermes/skills/software-development/hermes-provider-configuration`
- `~/.hermes/skills/software-development/custom-ai-providers`
- `~/.hermes/skills/autonomous-ai-agents/custom-llm-endpoint-gateway`

### 4. Verified Hermes Config Uses Native Provider Only
**File**: `~/.hermes/config.yaml`
```yaml
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  provider: nvidia
  base_url: https://integrate.api.nvidia.com/v1

providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: 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
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    name: NVIDIA
```
- `use_gateway: false` (default)
- No `nvidia-litellm` provider section
- Fallback: `qwen3.5:4b-mlx` (Ollama local)

### 5. Verified NVIDIA Model Availability
```bash
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models | grep nemotron-3-ultra
# Confirmed: nvidia/nemotron-3-ultra-550b-a55b exists in catalog
```

## Result
**Single clean path**: Hermes → Built-in NVIDIA Provider → `https://integrate.api.nvidia.com/v1`

No more:
- ❌ LiteLLM proxy on port 4000
- ❌ Dual rate limits (35 rpm × 2 paths)
- ❌ Model switching mid-session from gateway fallback
- ❌ Duplicate API key usage conflicts
- ❌ Auth header format mismatches (Bearer vs api_key)

## User Preference Embedded
This user's standard configuration is **native provider only**. Any future setup should:
1. Set `model_list: []` in LiteLLM config
2. Use `provider: nvidia` in Hermes config with explicit `api_key`
3. Never add NVIDIA models to LiteLLM templates
4. Kill LiteLLM gateway if it starts