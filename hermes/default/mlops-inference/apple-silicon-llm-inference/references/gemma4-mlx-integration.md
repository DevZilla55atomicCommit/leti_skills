# Gemma 4 12B on Apple Silicon (M1/M2/M3/M4)

## Quick Integration with Hermes

### 1. Serve via MLX + Speculative Decoding
```bash
# Install dependencies
pip install mlx-dspark

# Launch with DeepSeek DSpark drafter (2x speedup on M4)
mlx-dspark serve \
  --model mlx-community/gemma-4-12b-4bit \
  --mode auto \
  --port 8080
```

### 2. Configure Hermes Provider
Add to `~/.hermes/config.yaml`:
```yaml
providers:
  mlx-gemma:
    base_url: "http://127.0.0.1:8080/v1"
    api_key: "not-needed"
    models: ["gemma-4-12b-4bit"]
    format: "openai"
    # Speculative decoding enabled automatically
```

### 3. Switch to Provider
```bash
hermes config set model.provider mlx-gemma
hermes config set model.default gemma-4-12b-4bit
hermes reset  # Apply changes
```

### 4. Performance Expectations
| Metric | Value |
|--------|-------|
| Tokens/sec (M4 Pro) | 8-12 tok/s (baseline) → 15-22 tok/s with dspark |
| Memory usage | ~14 GB (fits 16GB RAM) |
| Power efficiency | ~30% lower GPU energy vs Ollama |

### 5. Verification Script
```bash
curl -X POST http://127.0.0.1:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-12b-4bit",
    "prompt": "Explain quantum entanglement",
    "max_tokens": 128,
    "temperature": 0.7
  }' | jq '.choices[0].text'
```

### 6. Pitfalls & Fixes
| Symptom | Fix |
|---------|-----|
| `METAL: Out of memory` | Increase wired limit: `sudo sysctl iogpu.wired_limit_mb=57344` |
| Low throughput (<5 tok/s) | Check `iogpu.wired_limit_mb` setting |
| Model not found | Verify `mlx-dspark serve` is running and model name matches |