---
name: uscis-alerts-monitoring
description: Systematically monitor USCIS Newsroom alerts for immigration policy updates, court rulings, and policy changes.
---
# Overview
Systematically monitor USCIS Newsroom alerts for immigration policy updates, court rulings, and policy changes. Use browser navigation to capture relevant pages, extract key summary items, and maintain a running log.

# Triggers
- User asks for latest US immigration updates.
- User requests tracking of specific topics (e.g., H-1B, asylum, TPS).
- User wants structured summary of USCIS alerts.

# Workflow
1. Navigate to https://www.uscis.gov/newsroom/alerts
2. Use browser_snapshot to capture page structure.
3. Identify article headings and details via element refs.
4. Extract key fields: release date, summary, links.
5. Log findings in a note (e.g., obsidian or markdown) with tags.
6. Optionally archive full snapshot for reference.

# Pitfalls
- Avoid click loops; use snapshot to identify correct links.
- Beware of pagination; capture full article list.
- Verify date stamps; USCIS may republish older content.

# References
- references/uscis-alerts-workflow.md
- scripts/extract_uscis_alerts.py