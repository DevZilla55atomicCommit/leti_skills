---
name: provider-block-patterns
description: "How to add a provider configuration block without selecting models in Hermes (supports API key insertion and empty models placeholder)."
tags: [configuration, provider, setup]
---

# Adding a Provider Without Models

When you want to register a provider but defer model selection, use an empty `models` array:

```yaml
nvidia-nim:
  api: https://integrate.api.nvidia.com/v1
  api_key: «your-api-key»
  models: []
  name: NVIDIA NIM
```

This registers the provider and allows you to later add models or select them via the UI.

## When to Use This

- You have credentials but haven't chosen specific models yet.
- You want to keep the provider available for future use.
- You are setting up the config ahead of model selection.

## Tips

- Keep the `models: []` placeholder until you decide which models to use.
- You can later populate the `models` section with specific model entries.
- The provider can be selected via `hermes model` UI once models are added.

## Reference

For more details on Hermes configuration, see the official docs: <https://hermes-agent.nousresearch.com/docs/user-guide/configuration>