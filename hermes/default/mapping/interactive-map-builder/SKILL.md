---
name: interactive-map-builder
description: Create Leaflet maps for Tongan infrastructure planning.
category: mapping
---

## Trigger
Use this skill when you need to create an interactive Leaflet map for geographic data in a Tongan context — especially for ride-hailing infrastructure planning.

## Core Steps
1. Prepare GeoJSON files for POIs, roads (primary/secondary/tertiary), and buildings.
2. Include explicit road colors matching Tongan classification: primary `#1e40af`, secondary `#166534`, tertiary `#8b4513`.
3. Stylize POI markers according to legend colors.
4. Create HTML template with layer toggles and legend.
5. Serve via local HTTP server to avoid CORS issues.
6. Verify layer visibility and color rendering.

## Pitfalls & Fixes
- CORS errors when loading local GeoJSON: serve via `python -m http.server 8080` or similar.
- Color mismatch for tertiary roads: use `#8b4513` (saddle brown) for reliable rendering.
- Invisible POI markers: ensure `POI_STYLES` keys match feature properties exactly.
- Layer toggle not reflecting legend state: check checkbox `data-layer` attribute matches layer key.

## Verification
- Check stats bar shows correct counts (POIs, roads, buildings).
- Toggle layers to confirm visibility.
- Use browser vision to verify colors against legend.

## Support Files
- `references/tonga-map-builder-notes.md` — session notes and data sources.
- `templates/tonga-map-template.html` — base HTML skeleton (mirrors `/Users/alfredkamisese/tongatapu_map_final.html`).
- `scripts/tonga-map-verify.py` — verification script for counts.