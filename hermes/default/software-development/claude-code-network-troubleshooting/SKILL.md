---
name: claude-code-network-troubleshooting
description: Fix Claude Code API retry loops and connectivity errors.
---

# Claude Code Network Troubleshooting

Diagnose and fix `Waiting for API response · will retry in 4m · check your network` and similar connectivity errors.

## Diagnostic
```bash
# Test direct API connectivity (replace with your actual key)
curl -v https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```
- **Works** → Issue is Claude Code config
- **Fails** → Network/proxy/firewall issue

## Common Fixes
| Cause | Fix |
|-------|-----|
| Corporate proxy / VPN | `export HTTPS_PROXY=http://your-proxy:port` in `~/.zshrc` |
| Firewall (Little Snitch, LuLu) | Allow outbound `api.anthropic.com:443` for `node` process |
| DNS / IPv6 issues | `export NODE_OPTIONS="--dns-result-order=ipv4first"` |
| Wrong/expired API key | `claude-code auth login` |
| Rate limiting | Increase retry config in `~/.claude/settings.json` |

## Permanent macOS Fix (LaunchAgent)
Sets proxy, API key, and DNS options for all Claude Code sessions:
```bash
cat > ~/Library/LaunchAgents/com.anthropic.claude-code.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.anthropic.claude-code</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HTTPS_PROXY</key>
        <string>http://your-proxy:port</string>
        <key>ANTHROPIC_API_KEY</key>
        <string>your-key-here</string>
        <key>NODE_OPTIONS</key>
        <string>--dns-result-order=ipv4first</string>
    </dict>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.anthropic.claude-code.plist
```

## Retry Config (in ~/.claude/settings.json)
```json
{
  "api": {
    "maxRetries": 5,
    "retryDelayMs": 5000,
    "timeoutMs": 120000
  }
}
```

## Key Principle
**Shell exports don't reach background services.** LaunchAgents/systemd have isolated environments — must set env vars in the service definition (plist), not `.zshrc`/`.bashrc`.

## Auto-Mode Classifier Timeout (Ollama Local Models)

**Symptom:** `qwen3.5-128k:latest is temporarily unavailable (timed out), so auto mode cannot determine the safety of Bash right now.`

**Cause:** The auto-mode safety classifier uses the **haiku tier** model. Large local models (qwen3.5-128k, qwen3-coder) are too slow for quick safety checks (>60s), causing the classifier to timeout.

**Fix:** Use a fast Ollama cloud model for the classifier, local model for coding.
```bash
# Fast cloud model for classifier (zero local resources, ~0.5s response)
export ANTHROPIC_DEFAULT_HAIKU_MODEL=gemma4:31b-cloud
export ANTHROPIC_DEFAULT_SONNET_MODEL=gemma4:31b-cloud
export ANTHROPIC_DEFAULT_OPUS_MODEL=gemma4:31b-cloud

# Your coding model (local, full context)
claude --model qwen3.5-128k:latest
```

| Tier | Purpose | Recommended Model |
|------|---------|-------------------|
| Haiku | Auto-mode classifier, quick summaries | `gemma4:31b-cloud` (cloud, free, ~0.5s) |
| Sonnet | Default coding | Your local model (`qwen3.5-128k:latest`) |
| Opus | Complex reasoning | Your local model or `nemotron-3-ultra:cloud` |

**Pitfall:** Do not set the classifier to a large local model — it will timeout on every bash command approval, blocking auto-mode entirely.

## Ollama Model Picker & Tier Mapping

`modelOverrides`/`behavesAs` are NOT real Claude Code settings keys — unknown keys are silently ignored, so they never populate any picker. Use only the real mechanism below.

**Problem:** With `ANTHROPIC_BASE_URL` pointed at Ollama, `/model` shows only one custom model, and background calls addressed to literal `haiku`/`sonnet`/`opus` 404 because Ollama serves no models under those names.

**Fix — real keys only:**
1. `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` (needs Claude Code v2.1.129+) — fills `/model` from the gateway's `GET /v1/models`. Verify first: `curl -s http://localhost:11434/v1/models` must list the models.
2. Tier mapping so haiku/sonnet/opus calls resolve to served names:
```json
{
  "env": {
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gemma4:31b-cloud",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.5-96k:latest",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "nemotron-3-ultra:cloud"
  }
}
```

**Pitfall:** A resume pinned to an unloaded local model cold-loads gigabytes mid-request (evict + load) and can time out disguised as "model may not exist" — warm it first with `ollama run <name> "ok" < /dev/null`, then resume.

## Safe settings edits

`settings.json` loads once per session at startup — editing the file never signals, kills, or disturbs live sessions, terminals, or model servers; new values apply to new sessions only. Every edit still follows backup → edit → validate:
```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak-$(date +%Y%m%d-%H%M%S)
# ... edit ...
python3 -m json.tool ~/.claude/settings.json > /dev/null && echo JSON_VALID
diff <backup> ~/.claude/settings.json   # must show ONLY intended keys
```

## Lost-task triage (terminal/panel disappeared)

A missing panel is UI state, not proof of death — check the process before concluding anything:
```bash
ps -o pid=,tty=,etime=,command= -p <agent-pid>   # alive? how long?
ollama ps                                        # resident models; UNTIL = keep-alive expiry
lsof -a -p <shell-pid> -d cwd                    # project folder owning the session
```
- Agent PID alive + pty owned by a Code Helper process → VS Code integrated terminal hiding in another window: match the shell cwd to a window via the Window menu, then reopen the panel there.
- Agent PID gone after a file-only change → the window/terminal was closed (SIGHUP); a config edit cannot kill processes. Recover via session resume, warming the model first (pitfall above).
- **Pitfall:** Never load, evict, or switch models while a task runs — one box cannot hold two large residents, and forcing a swap starves the working set. Wait for idle (agent PID gone, UNTIL expired), then warm the next model.