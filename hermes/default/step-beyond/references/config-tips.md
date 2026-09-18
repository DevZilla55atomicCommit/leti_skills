# Step Beyond Configuration Tips

## Config.yaml load_order

Ensure the `skills.load_order` array includes `step-beyond` as a plain string item, not quoted:

```yaml
skills:
  load_order:
    - step-beyond
    - step-beyond-chatgpt
```

Do NOT use quotes around the entries, e.g., avoid `"step-beyond"`; this causes Hermes to load the skill but not recognize it properly.

## Session Hooks

The bidirectional memory sync uses two scripts:

- `session_start_step_beyond.sh` – pulls patterns from Obsidian into Hermes.
- `session_end_step_beyond.sh` – pushes patterns back to Obsidian.

Both scripts are located in `~/TamaZila Obsidian Vault/Hermes Agent/`. They should be sourced at the start and end of each Hermes session.

## Common Pitfalls

- **YAML formatting errors**: Quoted entries (`"step-beyond"`) cause silent loading failures. Use array syntax `- step-beyond`.
- **Missing sync**: Without the end hook, patterns may not persist across sessions.