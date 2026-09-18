# Profile Configuration Notes

Reference for `hermes-multi-agent-orchestration` skill. Notes on actual profile configurations vs. documented examples.

---

## Hestia Profile - Model Correction

**Documented in user-profile-examples.md:** Hestia uses local Ollama qwen3.5:4b-mlx (Apple Silicon local-first)

**Actual config (per user correction):** Hestia uses NVIDIA Nemotron-3-Ultra (cloud) via the NVIDIA provider.

**Reason:** Local Ollama cold-start latency and inference speed make it impractical for ops/life-admin tasks. User explicitly prefers cloud NVIDIA for hestia to avoid local model load times.

```yaml
# Actual hestia config.yaml model section:
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  provider: nvidia
  base_url: 'https://integrate.api.nvidia.com/v1'
```

---

## "Call Out the Team" Convention

**User convention:** When user says "call out the team", they mean reference the other Hermes profiles as teammates:
- **apollo** — Creative Director (Photo/Video/UI/Brand)
- **helios** — DaVinci Resolve Colorist
- **hephaestus** — Code Architect / Web Dev (ECC)
- **hestia** — Personal Assistant / Ops / Life Admin
- **kairos** — Forex Analyst / Trader

These are the 5 specialized profiles alongside the default (Maddie) orchestrator profile.