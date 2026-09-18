---
name: provider-block-patterns
description: Example configuration for adding a provider block without models
workflow: configuration-patterns
---

## Usage Example

Add a provider block with empty models array to register it without selecting specific models:

```yaml
nvidia-nim:
  api: https://integrate.api.nvidia.com/v1
  api_key: «your-api-key»
  models: []
  name: NVIDIA NIM
```

This configuration registers the provider but makes no model selections available initially. You can later populate the `models` array with specific model configurations.

## Best Practices

- Keep `models: []` placeholder until you determine which models to use
- Maintain the structure for future model additions
- Validate API connectivity before selecting models