---
description: Map generator for Tongatapu spatial analysis.
category: transportation
name: tonga-ridehailing-mapping
---

# Tongatapu Ride-Hailing Spatial Visualization

Automates extraction of OpenStreetMap data for Tongatapu, classifies points of interest, and generates an interactive Leaflet.js map with layer toggles.

## Workflow
1. **Extract POIs**: `extract_pois.py` → `tongatapu_key_pois.geojson`
2. **Convert to GeoJSON**: `python3 convert.py` → `tongatapu_key_pois.geojson`
3. **Generate HTML**: Use `tongatapu_map.html` with embedded GeoJSON
4. **Preview**: `open_preview` command opens map in Hermes client

## Outputs
- `tongatapu_key_pois.geojson` (147 POIs with full properties)
- `tongatapu_major_roads.geojson` (major road network)
- `tongatapu_buildings.geojson` (68,694 building footprints)
- `tongatapu_map.html` (interactive preview pane-ready map)

## Supporting Files
- `references/mapping-workflow.md` (extraction steps)
- `templates/map-config.html` (Leaflet template)
- `scripts/generate-data.sh` (convenience wrapper)

## When to Use
- Present spatial analysis for ride-hailing service planning
- Share interactive map with stakeholders
- Standardize map generation across sessions

## Related Skills
- `tonga-ridehailing-startup` (full launch guide)
- `leaflet-interactive-map` (generic Leaflet deployment)
- `osm-extraction` (Pacific OSM harvesting)