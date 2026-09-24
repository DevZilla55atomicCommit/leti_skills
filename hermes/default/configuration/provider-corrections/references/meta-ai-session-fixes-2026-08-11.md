# Meta AI Provider — Session Fixes (2026-08-11)

## Issues Fixed in This Session

### 1. Wrong Content Type for Assistant Messages
**Problem:** Meta's Responses API rejects `input_text` on assistant messages with error:
```
"content type \"input_text\" is not valid on assistant messages"
```

**Root Cause:** `convert_messages_to_input()` applied `input_text` to ALL roles.

**Fix:** Use role-specific content types:
```python
content_type = "output_text" if msg.role == "assistant" else "input_text"
```

### 2. Default max_tokens Too Low for Muse Spark 1.1
**Problem:** Model uses heavy internal reasoning (~300-600 tokens) before producing visible output. Default `max_tokens=16-50` left no room for actual response → empty `content` field.

**Fix:** Default to 2000 tokens if not explicitly set:
```python
effective_max_tokens = req.max_tokens if req.max_tokens is not None else 2000
meta_payload["max_output_tokens"] = effective_max_tokens
```

---

## Verified Working
- ✅ 5/5 consecutive requests with conversation history (name recall)
- ✅ 3/3 consecutive simple requests ("Say OK if working")
- ✅ All return populated `content` field with correct responses
- ✅ LaunchAgent auto-restart functional

---

## Files Updated
- `scripts/meta-adapter.py` — Fixed adapter with both fixes applied
- `~/meta-adapter/meta_adapter.py` — Runtime copy (manual update needed on each device)

---

## Note for Skill: meta-ai-adapter-setup
The `meta-ai-adapter-setup` skill (in `automation/`) has its own copy of the adapter at `references/meta_adapter.py`. That skill is user-owned (not curator-managed), so it couldn't be updated automatically. To sync it:
1. Run `hermes curator adopt meta-ai-adapter-setup`
2. Then update its `references/meta_adapter.py` with the fixed version