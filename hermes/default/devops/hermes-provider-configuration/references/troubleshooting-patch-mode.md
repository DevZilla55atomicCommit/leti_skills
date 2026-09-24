# Troubleshooting 'patch' mode errors

When using `skill_manage` to update skills, the **mode** parameter is critical:

- **`mode='replace'`** – Requires `old_string` to locate the text you want to replace. Use when you have a unique snippet to swap out.
- **`mode='patch'`** – Requires a complete **V4A diff** in the `patch` field. No `old_string` is needed.

**Common mistake**: Omitting `mode='patch'` while providing a `patch` string. The tool defaults to `mode='replace'`, which then expects `old_string`. This results in an error like:

```
error: old_string is required for 'patch'. Provide the text to find.
```

**Fix**: Explicitly add `mode='patch'` to the `skill_manage` call and supply the full diff in the `patch` argument. Example:

```bash
skill_manage(
  action='patch',
  name='hermes-provider-configuration',
  mode='patch',
  patch='diff --git a/devops/hermes-provider-configuration/SKILL.md b/devops/hermes-provider-configuration/SKILL.md\nindex 8e3b9c2..d7f1a4c 100644\n--- a/devops/hermes-provider-configuration/SKILL.md\n+++ b/devops/hermes-provider-configuration/SKILL.md\n@@ -...,,\n-...old text...\n+...new text...'
)
```

**Key takeaways**:

1. **Never rely on the default mode** – always set `mode` explicitly when you intend to patch.
2. **Use `patch` for additions/modifications** – it can add new sections, not just replace existing text.
3. **Keep the diff syntactically correct** – V4A format uses `*** Begin Patch`, `@@ context @@`, `-removed`, `+added` markers.
4. **Test the patch** – after applying, run `skill_view(name)` to verify the skill loads and any linked references are intact.

By following this pattern, you avoid the `old_string` requirement and can safely evolve your skill library.