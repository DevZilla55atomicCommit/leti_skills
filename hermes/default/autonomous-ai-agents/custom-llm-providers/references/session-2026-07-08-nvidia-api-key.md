# Session 2026-07-08: NVIDIA API Key Location for Hermes Agent

## Finding
The NVIDIA API key for Hermes Agent is configured as an environment variable reference in `~/.hermes/config.yaml`:

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}  # References environment variable
```

## Actual Key Location
The environment variable is set in `~/.zshrc`:
```bash
export NVIDIA_API_KEY="nvapi-...YOUR_KEY_HERE..."
```

**Note:** The current value in `.zshrc` is a placeholder (`nvapi-YOUR_KEY_HERE`). User needs to:
1. Get actual key from [NVIDIA Build](https://build.nvidia.com/)
2. Update `~/.zshrc` with real key
3. Run `source ~/.zshrc`
4. Restart Hermes Agent

## Config File Path
- Hermes config: `~/.hermes/config.yaml` (line 42)
- Shell config: `~/.zshrc` (line with `export NVIDIA_API_KEY`)

## Verification
```bash
# Check if env var is set
echo $NVIDIA_API_KEY

# Check Hermes config
grep -A2 "nvidia:" ~/.hermes/config.yaml

# Test with curl
curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models
```

## Related
- Hermes `config.yaml` uses `${NVIDIA_API_KEY}` env var substitution
- Works with Hermes native NVIDIA provider (not just Claude Code custom providers)
- See also: `references/claude-code-nvidia-debugging.md` for Claude Code NVIDIA integration issues