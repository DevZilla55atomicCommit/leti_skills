---
name: meta-ai-adapter-setup
description: "Set up Meta AI adapter for Hermes with launchd auto-start."
version: 1.0.0
author: Maddie
license: MIT
platforms: [macos]
tags: [hermes, meta-ai, adapter, setup, launchd, automation]
---

# Meta AI Adapter Setup Skill

Sets up the Meta AI `muse-spark-1.1` model for Hermes via a FastAPI adapter that translates OpenAI Chat Completions format to Meta's Responses API format.

## What This Does

1. **Prompts for your Meta API key** (different per device/account)
2. **Creates the adapter** at `~/meta-adapter/meta_adapter.py`
3. **Configures Hermes provider** `meta-ai` with model `muse-spark-1.1`
4. **Installs launchd LaunchAgent** for auto-start at login
5. **Verifies the setup** with a test request

## Prerequisites

- Hermes Agent installed and configured
- Python 3.9+ (uses system Python at `/Library/Developer/CommandLineTools/usr/bin/python3`)
- Meta AI API key from https://dev.meta.ai

## Usage

```bash
# Run the setup (interactive - will prompt for API key)
~/.hermes/skills/automation/meta-ai-adapter-setup/scripts/setup.sh

# Or from the skill directory
cd ~/.hermes/skills/automation/meta-ai-adapter-setup && ./scripts/setup.sh
```

## Files Created

| File | Purpose |
|------|---------|
| `~/meta-adapter/meta_adapter.py` | FastAPI adapter server |
| `~/meta-adapter/run_adapter.sh` | Launcher script with env vars |
| `~/meta-adapter/requirements.txt` | Python dependencies |
| `~/Library/LaunchAgents/com.alfredkamisese.meta-ai-adapter.plist` | launchd auto-start config |
| `~/.hermes/config.yaml` | Hermes provider configuration (updated) |

## Manual Commands (if needed)

```bash
# Start adapter manually
cd ~/meta-adapter && ./run_adapter.sh

# Check health
curl http://localhost:8000/health

# Test with Hermes
hermes chat -q "Hello" --provider meta-ai

# Manage launchd service
launchctl unload ~/Library/LaunchAgents/com.alfredkamisese.meta-ai-adapter.plist  # Stop
launchctl load ~/Library/LaunchAgents/com.alfredkamisese.meta-ai-adapter.plist    # Start
tail -f ~/meta-adapter/adapter.log                                                # Logs
```

## Configuration

The skill adds this to your `~/.hermes/config.yaml`:

```yaml
providers:
  meta-ai:
    api: http://localhost:8000/v1
    default_model: muse-spark-1.1
    models:
      - muse-spark-1.1
    name: Meta AI
```

## Notes

- Each device needs its own Meta API key
- The adapter runs on port 8000 by default
- Uses system Python 3.9 with user-site packages (`~/Library/Python/3.9`)
- launchd keeps it running across reboots/logins