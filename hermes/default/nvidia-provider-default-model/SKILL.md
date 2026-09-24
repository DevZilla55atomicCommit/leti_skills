---
name: nvidia-provider-default-model
description: Fix for NVIDIA provider default model configuration
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, configuration, provider, nvidia, troubleshooting]
    related_skills: [hermes-agent]
---

# NVIDIA Provider Default Model Fix

## When to Use
Use this skill when you encounter errors related to the NVIDIA provider failing to recognize the model, especially after setting `provider: nvidia` in config.yaml or when the agent falls back to the NVIDIA provider and returns errors like "model not found" or HTTP 400 responses from the NVIDIA API.

**Problem:** The NVIDIA provider's `default_model` in `~/.hermes/config.yaml` is set to a non-NVIDIA model (e.g., `google/diffusiongemma-26b-a4b-it`). This causes errors when Hermes attempts to use the NVIDIA provider because the endpoint does not recognize the model name.

**Solution:** Update the provider's `default_model` to an actual NVIDIA model, such as `nvidia/nemotron-3-ultra-550b-a55b`.

**Steps:**

1. Check current setting:
   ```bash
   hermes config get providers.nvidia.default_model
   ```
2. Set correct default:
   ```bash
   hermes config set providers.nvidia.default_model nvidia/nemotron-3-ultra-550b-a55b
   ```
   (Or use the model alias interface: `hermes config set model.aliases.nvidia-default nvidia/nemotron-3-ultra-550b-a55b` and then `/model nvidia-default --global`.)
3. Verify:
   ```bash
   hermes doctor
   ```
   or test with a simple query:
   ```bash
   hermes chat -q "Say hello in one word."
   ```

**Notes:**
- The NVIDIA provider endpoint is `https://integrate.api.nvidia.com/v1`.
- Ensure the API key is valid and has access to the chosen model.
- After changing, any tool or agent that falls back to the NVIDIA provider will use the corrected default.

**Pitfall:** Leaving the default as a Google or other non-NVIDIA model results in HTTP 400 errors from the NVIDIA API (model not found) and may trigger fallback chains unexpectedly.