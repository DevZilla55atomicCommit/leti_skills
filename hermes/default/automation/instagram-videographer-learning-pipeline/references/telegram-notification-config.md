# Telegram Notification Configuration for Batch Processing

## Overview
This document describes how to enable Telegram notifications for the Instagram Videographer Learning Pipeline batch processing runs.

## Current Configuration Status

The Hermes config at `~/.hermes/config.yaml` already has Telegram platform configured (lines 338-341, 533-538, 700-721), but **`allowed_chats` is empty**, which prevents notifications from being delivered to specific chats.

## Required Configuration

Add the following to `~/.hermes/config.yaml` under the `telegram:` section:

```yaml
telegram:
  reactions: true
  allowed_chats: "<YOUR_CHAT_ID>"  # REQUIRED: Get from @userinfobot or @getmyid_bot
  extra:
    rich_messages: true
    rich_drafts: false
```

### Getting Your Chat ID
1. Message `@userinfobot` or `@getmyid_bot` on Telegram
2. Copy the numeric Chat ID returned
3. Add it to `allowed_chats` in config.yaml (can be comma-separated for multiple chats)

## Notification Types Supported

When properly configured, the batch processor can send:
- **Start notification** — "🚀 Batch started: 210 reels queued"
- **Progress updates** — "📊 Progress: 50/210 reels processed (23%)"
- **Completion notification** — "✅ Batch complete: 210/210 successful, 0 failed"
- **Failure alerts** — "❌ Failed: DaM8mLZo3af - Browser timeout"

## Implementation Notes

The batch processor script (`batch_process_reels_complete.py`) can send notifications via:
- Hermes `send_message` tool (if running in Hermes session)
- Direct Telegram Bot API call (for standalone Python script)
- Hermes `cronjob` with `deliver: "telegram:<chat_id>"` for scheduled runs

## Related Files
- `~/.hermes/config.yaml` — Main config (lines 338-341, 533-538, 700-721)
- `references/config_videographer.yaml` — Pipeline config
- `scripts/run_pipeline.py` — Batch processor entry point