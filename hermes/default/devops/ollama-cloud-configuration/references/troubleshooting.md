# Ollama Cloud Troubleshooting

## Common Issues & Fixes

### 404 Path Not Found Errors
- **Cause**: Incorrect `base_url` configuration.
- **Fix**: 
  ```bash
  hermes config set model.base_url "https://ollama.com/v1"
  hermes config set providers.ollama-cloud.api "https://ollama.com/api"
  ```

### Authentication Failures
- **Cause**: Missing or invalid API key.
- **Fix**:
  ```bash
  hermes config set providers.ollama-cloud.api_key "[YOUR_API_KEY]"
  ```

### Model Not Found Errors
- **Cause**: Model name mismatch or model not available in provider config.
- **Fix**:
  ```bash
  hermes config show providers.ollama-cloud.models
  hermes config set model.default "gpt-oss:20b"
  ```

## Test Command
Verify configuration with:
```bash
hermes chat -q "Say hello and confirm you're working" --model gpt-oss:20b
```