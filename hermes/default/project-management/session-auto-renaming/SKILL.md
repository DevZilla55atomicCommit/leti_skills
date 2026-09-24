---
name: session-auto-renaming
description: Automatic session renaming after first exchange
author: Alfred
tags:
  - session-management
  - configuration
content_type: markdown
---

# Session Auto-Renaming

Hermes Agent automatically assigns a descriptive title to a session after the first user/assistant exchange. This prevents unnamed sessions and makes it easier to identify work.

## Configuration

The behavior is controlled via the `auxiliary.title_generation` block in your `config.yaml`.

### Default Settings

```yaml
auxiliary:
  title_generation:
    provider: "auto"
    model: ""
    base_url: ""
    api_key: ""
    timeout: 30
    reasoning_effort: ""
    language: ""  # Empty = match user's language
```

### Customization Options

- **Enable/Disable**: Currently always enabled. To disable, set `auxiliary.title_generation.enabled: false` (add this flag in future config updates).
- **Custom Prompt**: Modify the title generation prompt by editing `agent/title_generator.py` or by setting a custom `title_generation.prompt` in config (not yet exposed UI).
- **Title Length**: The generator returns 3‑7 words by default. Adjust `_TITLE_PROMPT` constant in `title_generator.py` if you need a different length.

## Usage

Auto‑titling runs automatically after the first exchange; no manual intervention required. If you want to set a title manually, use the `/title <name>` command.

## Pitfalls & Workarounds

- **Duplicate Titles**: If the generated title collides with an existing session title, the system appends a numeric suffix. To avoid this, ensure unique topics or manually set a title via `/title`.
- **Language Mismatch**: If `language` is set incorrectly, titles may be generated in the wrong language. Leave it empty to auto‑detect the user's language.
- **Config Changes Not Applied**: Changes to `config.yaml` require restarting the Hermes gateway for the new settings to take effect.

## Extending the Feature

- **Scheduled Renaming**: Create a cron job that renames sessions older than X days based on their content.
- **Project‑Specific Templates**: Store project‑specific title templates in `references/` and reference them in a custom title generator script.

skill_manage