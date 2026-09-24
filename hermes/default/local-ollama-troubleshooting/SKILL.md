---
name: Local Ollama Troubleshooting
description: Diagnose and resolve Ollama daemon and llama-server processes on macOS.
category: mlops
---
## Agentic-Loop Cold Start Patience (16GB M4)
- A freshly launched local coding-agent session shows spinning status with 0% context and 0 tokens for MINUTES before its first tool call — this is model load (~7GB to GPU) plus first-turn prefill over the full skill/plugin stack, not a hang.
- Do NOT verdict a local agentic loop dead before ~8-10 minutes on a cold model; early kills destroy the evidence and the loaded model. Judge only after the first tool call or a hard context/error message.
- Keep one warmup ping (`ollama ps` showing the model loaded with expected CONTEXT) before starting timed evaluations.

## Check Running Processes
- Run `ps -ef | grep -i ollama` to list all related processes.
- Identify the `ollama` daemon process and any spawned `llama-server` model servers.

## Kill Ollama Daemon
- To stop the daemon and all child processes use `killall ollama` or `pkill -f ollama`.
- Verify with `ps -ef | grep -i ollama` that no `ollama` processes remain.

## Verify Hermes Configuration
- Ensure that `~/.hermes/config.yaml` (or relevant profile config) defines the Ollama provider correctly:
  ```yaml
  providers:
    ollama-launch:
      base_url: http://127.0.0.1:11434/v1
      model_matcher: "^(ollama|local)/"
  ```
- Confirm the provider is pinned if needed (`provider: ollama-launch` in the model configuration).

## List Installed Models
- Run `ollama list` to see which models are installed and their tags.
- If a required model (e.g., `qwen3.5:latest`) is missing, reinstall it with `ollama pull <model>`.

### Compare Variants Before Pulling Duplicates

- A `model:tag` and its `model:tag-mlx` twin share base weights but differ in backend (GGUF/llama.cpp vs Apple MLX), quantizer (the `quantization` field in `ollama show`), and resident footprint (the `SIZE` column in `ollama ps`).
- Diff `ollama show <a>` against `ollama show <b>` (parameters, quantization, context length) before pulling a multi-GB second copy — pull only for a measured reason (speed shootout, RAM fit), never out of curiosity.

## Vision Capability Note
- **Local qwen3-vl:8b on 16GB M4**: Not recommended for batch vision analysis — consistently hits 60s read timeout / OOM on 16GB M4 Mac Mini.
- **Local qwen3.5:4b (3.39 GB) on 16GB M4**: Also unreliable for vision — hits 300s read timeout / "Remote end closed connection" errors. Single-frame analysis can work (~2-3 min) but concurrency >1 causes Ollama server crashes (exit code -15/-9).
- **Local `qwen3.5-*k` variants** — verify any `qwen3.5-*k` variant actually resolves (`ollama show` on a local copy, registry manifest API for remote) before depending on it; a stale `delegation.model` pointing at a removed ID fails every child at boot. Cloud vision via Hermes `vision_analyze` remains the fallback for vision tasks.
- **Workaround**: Use cloud vision via Hermes `vision_analyze` tool (NVIDIA/Google Gemini providers) which runs at ~3-5s/call.
- **Reference**: Local `ollama serve` + `ollama run qwen3-vl:8b` with `images` array in API call consistently hits 60s read timeout / OOM on 16GB M4 Mac Mini.

## Qwen3.5 96k Streaming Bug (Ollama 0.32.x)
- **Symptom**: `qwen3.5-96k:latest` on `/v1/chat/completions` with `stream: true` returns `Content-Type: application/x-ndjson` with **zero events** — the OpenAI-compat layer misbehaves for this specific quantization. Same base model at `qwen3.5:9b` correctly returns `text/event-stream` SSE.
- **Root cause**: The 96k variant (capped `num_ctx=98304`) breaks the streaming code path in Ollama's OpenAI-compat layer; it falls back to NDJSON but emits nothing.
- **Fix: Force non-streaming** — the non-streaming endpoint (`stream: false`) returns valid JSON. This is a documented Ollama feature, not a hack.
- **Gateway config** (litellm proxy example):
  ```yaml
  model_list:
    - model_name: qwen3.5-96k
      litellm_params:
        model: ollama/qwen3.5-96k:latest
        api_base: http://localhost:11434
        stream: false  # forces non-streaming
  ```
- **RAM trade-off**: 96k non-streaming = ~6 GB resident (stable on 16 GB). 9b streaming = ~9.4 GB resident (OOM on 16 GB with Desktop app). Non-streaming loses the "typing" effect but gains stability.

## Sequential Local Processing Pattern (Working)
When local vision is required, **sequential single-frame processing in foreground Python** works better than parallel sub-agents:
```python
# Single-frame analysis with qwen3.5:4b
resp = requests.post('http://127.0.0.1:11434/api/generate', 
    json={'model': 'qwen3.5:4b', 'prompt': prompt, 'images': [img_b64], 'stream': False, 'options': {'temperature': 0.1}},
    timeout=300)  # ~2-3 min per frame
```
- Accept ~2-3 min/frame
- Restart Ollama server (`pkill -9 -f "ollama serve" && ollama serve &`) every ~5 frames to prevent memory leaks
- Save progress to JSON after each frame

## Hermes Delegation Context Window Requirement
- **Minimum 64K context** required for sub-agents (hard-coded in Hermes)
- `qwen3.5:4b` reports 32K → **rejected by Hermes** even with `context_length: 262144` in config
- `qwen3.5-64k` reports 262K → **accepted** but sub-agents still timed out at 300s
- **Best practice**: Use cloud provider (NVIDIA/Gemini) for sub-agent vision tasks; local models only for foreground sequential work

## Delegation on Metered Cloud Models: Probe Billing First
- A model can resolve in the registry and still fail at inference with HTTP 402 — probe a candidate default with a tiny chat-completions call before setting it, and keep a known-free fallback named alongside.
- A 402 means billing/entitlement, not a broken model: switch the default, do not debug the model.

## Remote Registry Lookup Failures
- `ollama show`/`pull` on a remote ID can fail while the registry is healthy: confirm with a direct manifest fetch (`/v2/library/<family>/manifests/<tag>` returns schemaVersion 2 JSON anonymously) before blaming the network.
- A pull attempt that errors in seconds with zero bytes is itself the definitive test — no bandwidth is spent on a failed lookup.
- Check the daemon actually attempted the fetch (`server.log` should show activity); silence there means the failure is client-side, not network-side.

## Provisioning Rule: Verify IDs Before Promising Pulls
- Confirm the exact tag exists via the manifest API before telling anyone a model will be pulled — coder-branded variants especially (dense vs coder families differ; a plausible-sounding ID may not exist).
- If the exact ID is unverified, name the nearest verified tag and flag the substitution explicitly.

## Daemon Env Staleness (Electron-App Supervised)
- `launchctl setenv` does NOT reach an already-running Ollama.app supervisor's children — verify with `ps -E -p <serve-pid>`, then quit and reopen the app (or reboot) to activate; relaunching only `ollama serve` re-inherits the stale parent env.
- Same class of drift: a stale default such as `OLLAMA_CONTEXT_LENGTH` in the daemon env silently under-provisions models without explicit `num_ctx`. Align it with the serving target on restart.
- KV-cache math and keep-alive/flash-attention guidance: `references/kv-cache-memory.md`.

## Claude Code Window-Accounting Parity (Ollama backend)
- When a routed Claude Code session dies of context far below the model's real window, diff the working machine's `settings.json` env trio (`OLLAMA_CONTEXT_LENGTH`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`) plus `ollama show` (`num_ctx`) against the broken one — a model-field switch without the matching trio rewrite strands half the window (e.g. 48k accounting on a 98k load).
- Fix with the owner's model switcher, never by hand-editing one key — the trio must move together; re-read all three values after switching.
- A stale `ANTHROPIC_API_KEY` next to the dummy `ANTHROPIC_AUTH_TOKEN="ollama"` trips the both-set auth warning; on a pure-local setup the warning is cosmetic (Ollama ignores both), but match the working machine's values anyway to eliminate drift as a variable.
- Session commands like `/effort` can persist as defaults — after changing levels mid-session, confirm `effortLevel`/`modelSettings` in settings.json still say what you intend.

## Agentic Sampling for Small Ollama Models (act, don't ruminate)
- A local 7–14B model that thinks for minutes and never emits a tool call is usually over-constrained sampling, not incapacity: raise `temperature` toward 0.4–1.0 and lower `presence_penalty` toward ~0.6 — near-zero temperature collapses the distribution onto more reasoning instead of rare action tokens, and high presence distorts rigid tool syntax.
- Keep `top_k` modest (~20) and `top_p` ~0.85 for tool-schema precision.
- Change sampling before changing models or windows — every capacity test is invalid while the model cannot act.

## Clean Up Residual Files (if needed)
- Remove leftover model files in `~/.ollama/models` if you plan to reinstall models.
- Delete cached images or temporary files in `~/Library/Caches/com.ollama.ollama/` after stopping the daemon.

## Prevent Auto‑Start (Optional)
- Disable the Ollama menubar app from launching at login via System Settings → Users & Groups → Login Items.
- Alternatively, run `launchctl unload ~/Library/LaunchAgents/com.ollama.ollama.plist` to stop it immediately.

## macOS Persistent Service with Model Keep-Alive (launchd)
**Use this when you need Ollama running permanently with models loaded in memory (OLLAMA_KEEP_ALIVE=-1).**

### Create LaunchAgent plist
```bash
cat > ~/Library/LaunchAgents/com.ollama.ollama.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.ollama</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_KEEP_ALIVE</key>
        <string>-1</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF
```

### Load the service
```bash
launchctl unload ~/Library/LaunchAgents/com.ollama.ollama.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.ollama.ollama.plist
```

### Verify it works
```bash
# Check service is loaded
launchctl list | grep ollama

# Check model stays loaded after idle
ollama ps
# Wait 10+ minutes, run again — should still show loaded
```

### Why this works
- `EnvironmentVariables.OLLAMA_KEEP_ALIVE=-1` — tells Ollama **never unload models** (overrides default 5-minute idle timeout)
- `KeepAlive=true` — launchd restarts the process if it crashes
- `RunAtLoad=true` — starts immediately on boot/login
- Shell exports (`.bashrc`, `.zshrc`) **don't work** — systemd/launchd services have isolated environments; must set in plist

### Reverse Proxy Timeout Fixes (nginx/Caddy)
If streaming responses time out behind a proxy:

**nginx:**
```nginx
location / {
    proxy_pass http://127.0.0.1:11434;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_buffering off;
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;
}
```

**Caddy:**
```caddy
localhost:11434 {
    reverse_proxy 127.0.0.1:11434 {
        transport http {
            read_timeout 600s
            write_timeout 600s
        }
    }
}
```

**Key directives:** `proxy_buffering off` (nginx) / `flush_interval -1` (Caddy) — prevents buffering that breaks streaming; `proxy_read_timeout 600s` — allows long generations without 502/timeout.

### Per-Request Keep-Alive (API fallback)
If you can't restart the service:
```bash
# CLI
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "prompt": "test", "keep_alive": -1}'

# Python
import ollama
ollama.generate(model="llama3.2", prompt="test", keep_alive=-1)
```

## Model Warmth Without Permanent RAM Pinning (16 GB Machines)
- **Don't use launchd `KeepAlive` with `OLLAMA_KEEP_ALIVE=-1`** — pins model 24/7 (~6-10 GB), starves other workloads.
- **Use per-request `keep_alive: "2h"` (or similar)** — model stays loaded during active session, auto-unloads 2h after last request.
  ```bash
  curl -s -X POST http://localhost:11434/api/generate \
    -d '{"model":"qwen3.5-96k:latest","prompt":"ping","stream":false,"keep_alive":"2h"}'
  ```
- **Cron keep-warm** (optional): ping every 5 min to refresh the window while working.
  ```bash
  */5 * * * * curl -s -X POST http://localhost:11434/api/generate -d '{"model":"qwen3.5-96k:latest","prompt":"ping","stream":false,"keep_alive":"2h"}' > /dev/null
  ```
- **Result**: Instant first-token during session, zero RAM when idle.

---

*Skill updated: 2026-09-26 by Alfred (Maddie)*

## Ollama Cloud Provider (ollama-cloud)

The Ollama Cloud provider (`provider: ollama-cloud`) is a **registered provider** in Hermes with a fixed base URL (`https://ollama.com/v1`) and uses `OLLAMA_API_KEY` for authentication. It is NOT a local Ollama server.

### Common Issues & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `APIConnectionError` / `Connection error` to `api.ollama.com/v1` | Config uses wrong base URL | Use `https://ollama.com/v1` (not `api.ollama.com/v1`) |
| `HTTP 301 Moved Permanently` | Old base URL redirects | Update config to `https://ollama.com/v1` |
| Model not found (`gemma4:31b-cloud`) | API returns models WITHOUT `-cloud` suffix | Use clean model IDs: `gemma4:31b`, `nemotron-3-ultra`, `deepseek-v4-flash:0731`, `glm-5.2` |
| Stale model list after config change | Cached model lists | Delete `~/.hermes/context_length_cache.yaml` and `~/.hermes/ollama_cloud_models_cache.json` |
| Auxiliary title generation fails | Gateway running old code | Restart gateway: `pkill -f "hermes.*gateway"` then re-run |

### Required Code-Level Patches (Hermes < 0.21)

If `ollama-cloud` fails despite correct config, the Hermes codebase may lack explicit handling. Apply these patches:

**1. `hermes_cli/runtime_provider.py`** — In `resolve_runtime_provider()`, before `custom_runtime`:
```python
if requested_provider == "ollama-cloud":
    from hermes_cli.auth import DEFAULT_OLLAMA_CLOUD_BASE_URL, PROVIDER_REGISTRY
    pconfig = PROVIDER_REGISTRY.get("ollama-cloud")
    api_key = (explicit_api_key or "").strip() or _getenv("OLLAMA_API_KEY", "").strip()
    return {
        "provider": "ollama-cloud",
        "api_mode": "chat_completions",
        "base_url": pconfig.inference_base_url if pconfig else DEFAULT_OLLAMA_CLOUD_BASE_URL,
        "api_key": api_key,
        "source": "ollama-cloud-registered",
        "requested_provider": requested_provider,
    }
```

**2. `agent/auxiliary_client.py`** — In `_PROVIDER_ALIASES`:
```python
"ollama-cloud": "ollama-cloud",
"ollama_cloud": "ollama-cloud",
```

### Verification
```bash
export OLLAMA_API_KEY="your_key"
hermes chat -q "hello" --provider ollama-cloud -m gemma4:31b
# Should show: Endpoint: https://ollama.com/v1
```