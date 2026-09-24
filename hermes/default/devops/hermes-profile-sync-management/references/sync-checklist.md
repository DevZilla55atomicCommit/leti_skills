# Hermes Profile Sync Checklist

- [ ] Verify `config.yaml` is listed in `.stignore` (run `cat ~/.hermes/profiles/.stignore`; should include `config.yaml`).
- [ ] Confirm `memories/` remains synced (file changes appear on all machines).
- [ ] Check each machine's `~/.hermes/profiles/default/config.yaml` for correct `providers.ollama-launch.api` endpoint.
- [ ] Validate Ollama models are present locally on each machine (`ollama list`).
- [ ] Launch Hermes on each machine and confirm no provider connection errors appear in logs.
- [ ] Review provider-specific API keys for any that should be machine‑local only; move those to per‑machine secret stores if needed.
- [ ] After any Hermes upgrade, re‑run this checklist to catch breaking changes in `config.yaml` schema.