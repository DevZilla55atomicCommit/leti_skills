---
name: obsidian-dashboard-plugin
description: Build Obsidian plugins that visualize pipeline stages and track metrics from daily notes.
---
# EMAI Dashboard Plugin Skill

## Overview
This skill defines how to create an Obsidian plugin that visualizes content pipeline stages and tracks key metrics (deep-work hours, published content, watch time) from daily notes. It extends the professional-web-dev-skills umbrella.

## Core Components
1. **Pipeline Stage Configuration**: Manage stage definitions with names, keys, and colors
2. **Metrics Parsing**: Extract frontmatter metrics from daily notes
3. **React Dashboard Components**: Create visualizations for pipeline flow, metric trends
4. **Settings UI**: Configure pipeline stages and tracked metrics
5. **Obsidian Plugin Architecture**: Plugin registration, ribbon icon, command integration

## Usage Patterns
| Pattern | Implementation |
|---------|----------------|
| Pipeline visualization | Use pipeline stages to render progress |
| Metric tracking | Parse daily note frontmatter for metrics |
| Dashboard refresh | Trigger data reload from daily notes |
| Settings adjustment | Update pipeline configuration dynamically |

## Linked Reference Skills
- `frontend-ui-engineering` - UI component integration
- `spec-driven-development` - Specification-based pipeline design
- `test-driven-development` - Metric validation cycles

## References
- [Obsidian Plugin Development Docs](https://help.obsidian.md/Advanced+topics/Plugin+API)
- [Obsidian React Plugin Skeleton](https://github.com/sergiolepolo/obsidian-plugin-skeleton)
- [EMAI OS Pipeline Integration](references/graphify-vault-integration.md)