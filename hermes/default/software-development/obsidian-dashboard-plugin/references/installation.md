# EMAI Dashboard Plugin Installation Guide

## Prerequisites
- Obsidian v1.5.0 or later
- Node.js v18+ and npm v9+
- TSX support enabled in Obsidian plugin settings

## Installation Steps
1. **Build Plugin**: Run `npm run build` in the plugin directory
2. **Install**: Copy the built `main.js` to `.obsidian/plugins/emai-dashboard`
3. **Enable**: In Obsidian Settings → Community Plugins → enable "EMAI Dashboard"

## Configuration
- Settings appear automatically under **Settings → EMAI Dashboard**
- Pipeline stages and metrics configurable via JSON editor
- Dashboard view accessible via ribbon icon or command palette

## Development Workflow
- Use `npm run dev` for hot-reload during development
- Plugin rebuilds automatically when source files change
- Dashboard cache can be rebuilt via command palette → "Refresh Dashboard Data"

## Common Issues
- **Plugin not loading**: Check console for TypeScript errors, ensure manifest.json is valid
- **No data shown**: Verify daily notes have proper frontmatter structure
- **Type mismatches**: Ensure numeric values are used for metrics (e.g., `deepWorkHours: 3.5` not `"3.5"`)