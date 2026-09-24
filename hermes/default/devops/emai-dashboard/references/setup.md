# EMAI Dashboard Setup Guide

## Prerequisites
- Node.js v18+ installed
- npm v9+ installed
- Obsidian v1.6+ installed

## Configuration
1. Export current config from Obsidian:
   - Settings → Community Plugins → EMAI Dashboard → Settings → Export Config
   - Save as `emai-dashboard-config.json` in your vault's `Machine/Personalization/` folder

2. Import config into new vault:
   - Settings → Community Plugins → EMAI Dashboard → Import Config
   - Select the exported JSON file

## Build Workflow
```bash
# Navigate to plugin directory
cd "/path/to/your/vault/.obsidian/plugins/emai-dashboard"

# Install dependencies
npm install

# Build plugin
npm run build
```

## Common Config Fields
- `dailyNotesFolder`: Where daily notes are stored
- `pipelineStages`: Array of stage objects with `id`, `name`, `color`
- `metrics`: Array of metric objects with `id`, `name`, `unit`

## Reference Config
The current config used for Alfred's vault:
```json
{
  "dailyNotesFolder": "00 Human/10 Daily Notes",
  "pipelineStages": [
    { "id": "backlog", "name": "Backlog", "key": "pipelineStage", "color": "#6B7280" },
    { "id": "idea", "name": "Idea", "key": "pipelineStage", "color": "#9CA3AF" },
    { "id": "research", "name": "Research", "key": "pipelineStage", "color": "#3B82F6" },
    { "id": "pre-production", "name": "Pre-Production", "key": "pipelineStage", "color": "#8B5CF6" },
    { "id": "production", "name": "Production", "key": "pipelineStage", "color": "#EC4899" },
    { "id": "post-production", "name": "Post-Production", "key": "pipelineStage", "color": "#F59E0B" },
    { "id": "review", "name": "Review/QC", "key": "pipelineStage", "color": "#06B6D4" },
    { "id": "ready-to-publish", "name": "Ready to Publish", "key": "pipelineStage", "color": "#10B981" },
    { "id": "published", "name": "Published", "key": "pipelineStage", "color": "#059669" }
  ],
  "metrics": [
    { "id": "deepWorkHours", "name": "Deep Work Hours", "key": "deepWorkHours", "unit": "h" },
    { "id": "publishedCount", "name": "Published", "key": "publishedCount", "unit": "" },
    { "id": "watchTimeMinutes", "name": "Watch Time", "key": "watchTimeMinutes", "unit": "min" },
    { "id": "youtubeSubscribers", "name": "YouTube Subs", "key": "youtubeSubscribers", "unit": "" },
    { "id": "instagramViews", "name": "IG Views", "key": "instagramViews", "unit": "" },
    { "id": "instagramLikes", "name": "IG Likes", "key": "instagramLikes", "unit": "" },
    { "id": "forexSignals", "name": "Forex Signals", "key": "forexSignals", "unit": "" },
    { "id": "forexPnL", "name": "Forex P&L", "key": "forexPnL", "unit": "$" },
    { "id": "pipelineVelocity", "name": "Pipeline Velocity", "key": "pipelineVelocity", "unit": "days" }
  ]
}
```