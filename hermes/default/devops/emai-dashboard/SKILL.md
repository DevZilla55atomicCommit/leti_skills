---
title: EMAI Dashboard Plugin Management
description: Maintain the EMAI Dashboard plugin for Obsidian to visualize pipeline stages, metrics, and daily notes.
tags: ["obsidian", "plugin", "emai-dashboard", "dashboard", "workflow"]
name: emai-dashboard
---
# EMAI Dashboard Management

A class-level skill for maintaining the EMAI Dashboard plugin used to visualize pipeline stages, metrics, and daily notes in Obsidian. This skill covers:

## Installation
- Manual install via Community Plugins
- CLI-based rebuilds using `npm run build`

## Configuration
- Config file: `.obsidian/plugins/emai-dashboard/data.json`
- Export/import via plugin settings
- Custom JSON config located at:
  ```
  /Users/alfredkamisese/TamaZila Obsidian Vault/Machine/Personalization/emai-dashboard-config.json
  ```

## Rebuild Workflow
1. Navigate to plugin directory
2. Update `package.json` if source files change
3. Run `npm run build`
4. Copy `main.js` to `.obsidian/plugins/emai-dashboard/`
5. Reload plugin in Obsidian

## Common Issues
### Blank Dashboard
- Check console for JS errors (`Cmd+Option+I`)
- Verify `main.js` exists in plugin directory
- Ensure config JSON is valid

### Build Errors
- Missing `src/main.tsx` - ensure TypeScript source exists
- Dependency issues - run `npm install` if needed

## Best Practices
- Keep config JSON under version control
- Export config before making breaking changes
- Test rebuilds on minimal config first

## Related Skills
- `obsidian-plugin-development` (general plugin scaffolding)
- `emai-dashboard-workflows` (session-specific workflow examples)

## References
- [Obsidian Plugin Development Guide](https://pobs.io)
- [EMAI Dashboard GitHub Repo](https://github.com/alfredkamisese/emai-dashboard)

---