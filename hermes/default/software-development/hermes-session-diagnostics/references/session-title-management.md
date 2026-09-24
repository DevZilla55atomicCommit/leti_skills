## Session Title Management

- Hermes auto-generates titles from the first user message unless overridden with `/title <name>`.
- To rename the current session: `/title New Title`.
- To rename other sessions, use `hermes sessions rename <SESSION_ID> "New Title"`.
- The underlying `session_id` remains unchanged; only the display title updates.
- Pitfall: Renaming does not affect auto-generation for future messages; you may need to set `HERMES_AUTO_TITLE=false` in config to prevent unwanted titles.
- Example:
  ```text
  hermes sessions rename 20260712_143656_dbe407 "Multi-Agent Setup - Hermes"
  ```