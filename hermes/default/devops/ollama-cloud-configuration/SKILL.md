---
name: Ollama Cloud Configuration
description: Configure Ollama Cloud provider in Hermes Agent.
trigger: configure Ollama Cloud provider in Hermes Agent.
features: |
  - Set API key and base URL in ~/.hermes/config.yaml
  - Select and test models (e.g., gpt-oss:20b, gemma4:31b)
  - Handle retries and fallback to default provider
  - Execute test query: "Say hello and confirm you're working"
  - Switch models via `/model <name>` or `--model <name>` flag
  - Use `hermes config set` commands for provider options
---
## Setup Ollama Cloud Provider

1. **Add API key**
   ```bash
   hermes config set providers.ollama-cloud.api_key "[YOUR_API_KEY]"
   ```

2. **Set API endpoint**
   ```bash
   hermes config set model.base_url "https://ollama.com/v1"
   ```

3. **Configure default model** (optional)
   ```bash
   hermes config set model.default "gpt-oss:20b"
   ```

## Testing the Configuration

```bash
hermes chat -q "Say hello and confirm you're working" --model gpt-oss:20b
```

- Success: Agent responds with greeting.
- Failure: Check API key, base URL, and model availability.

## Model Selection

- List available models:
  ```bash
  hermes config show providers.ollama-cloud.models
  ```
- Switch model:
  ```bash
  hermes chat -q "Your query" --model <model-name>
  ```

## Troubleshooting

- **404 Path Not Found**: Verify `base_url` is `https://ollama.com/v1`.
- **Model Not Found**: Ensure the model exists in `providers.ollama-cloud.models`.
- **Authentication Failure**: Confirm the API key is correctly set.

## Example Workflow

```bash
# Set API key and base URL
hermes config set providers.ollama-cloud.api_key "92436dd56b4b4bbd9ac09fd29cc98029.AwVGlG_ctR7S8mAj5X2L00pq"
hermes config set model.base_url "https://ollama.com/v1"

# Test with default model
hermes chat -q "Say hello" --model gpt-oss:20b

# Switch to gemma4:31b
hermes chat -q "Summarize this" --model gemma4:31b
```

> **Note**: Always use direct `hermes config` commands to modify configuration. Do not edit `~/.hermes/config.yaml` manually unless necessary.