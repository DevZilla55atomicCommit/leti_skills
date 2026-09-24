When using MCP‑connected providers such as Claude Code, the Hermes Agent enforces a 40 RPM quota from the provider’s API. To stay within this limit:

1. **Minimize inline tool calls** – bundle related actions into a single background process or script rather than issuing many separate commands.
2. **Prefer batch operations** – use `process` or `execute_code` for bulk work, and throttle loops with a delay or back‑off (`retry(fn, max_attempts=3, delay=2)` is built‑in).
3. **Monitor usage** – you can query the RPM counter via `hermes config get preferences.mcp.rpm_limit` (if set) or watch logs for `⚠️ RPM limit reached` messages.
4. **Graceful fallback** – if the limit is hit, the agent will pause and wait for the next minute before resuming; design scripts to handle brief pauses or to switch to a cached path.

Incorporate this guidance into any skill that orchestrates MCP‑related workflows so future sessions stay within the quota automatically.