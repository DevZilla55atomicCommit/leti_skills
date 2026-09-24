# MCP Server Reload Guide

## When to reload

- After updating `.env` or `pyproject.toml`
- After patching `server.py`
- After changing environment variables
- When MCP tools stop responding

## Reload Steps

1. **Restart Hermes desktop app**
   - macOS: Cmd+R or quit and relaunch
   - Wait ~5 seconds for driver to reconnect

2. **Verify connection**
   ```bash
   mcp_cognee_memory_list_tools
   ```
   Should list: `graph_remember`, `graph_recall`, `session_remember`, `session_recall`

3. **Test a simple tool**
   ```bash
   mcp_cognee_memory_session_remember --content "Test reload" --session-id "reload-test"
   ```
   Then recall to verify:

   ```bash
   mcp_cognee_memory_session_recall --query "Test reload" --session-id "reload-test"
   ```

## Common Issues

| Symptom | Fix |
|---------|-----|
| Tools not responding | Restart Hermes again; check `.env` for API key |
| JSON parsing errors | Ensure `session_recall` returns valid JSON (patched) |
| Rate limit errors | Wait 30s before retrying (NVIDIA NIM limit: 32 concurrent) |

## FAQ

**Q: Do I need to reinstall dependencies?**  
A: No. Only required after `pip install` failures or Python version change.

**Q: Will reload affect running jobs?**  
A: No. Reload is connection-only; active jobs complete independently.