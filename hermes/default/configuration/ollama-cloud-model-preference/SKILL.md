---
name: ollama-cloud-model-preference
description: Ollama Cloud model alias correction for gemma4:31b-cloud.
version: 1.0.0
tags: [ollama-cloud, model-alias, user-preference, configuration]
---

# User Preference: Correct Cloud Model Alias

The user explicitly corrected the model name to `gemma4:31b-cloud` and removed all references to `gemma4:31b`. Update your configuration to:

```yaml
model_aliases:
  ollama-cloud: ollama-cloud/gemma4:31b-cloud

providers:
  ollama-cloud:
    default_model: gemma4:31b-cloud
    models:
      - gemma4:31b-cloud
```

## Verification

1. Run `hermes config get providers.ollama-cloud` to confirm settings.
2. Test the connection:
   ```bash
   export OLLAMA_API_KEY="your_api_key"
   hermes chat -q "hello" --provider ollama-cloud -m gemma4:31b-cloud
   ```

The session should complete without fallback warnings.