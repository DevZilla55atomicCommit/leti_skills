---
name: ridehailing-map
description: Generate ride-hailing maps for Tonga using OSM data.
---
Develop interactive ride-hailing maps for Tonga using OpenStreetMap data.

## Core Workflow
1. **Data Acquisition**  
   - Download OSM extracts: `tonga-latest.osm.pbf`, `tongatapu.osm.pbf`  
   - Filter transport data: `highway=*,amenity=*,building=*,public_transport=*`

2. **Processing**  
   ```bash
   osmconvert tongatapu.osm.pbf -B-o=tongatapu.osm.pbf
   osm2geojson --input tongatapu.osm.pbf --output tongatapu_buildings.geojson
   ```

3. **Styling & Assembly**  
   - Apply explicit CSS for POIs/roads  
   - Inline GeoJSON into `tongatapu_data.js`  
   - Use `tongatapu_map_final.html` template with viewport meta

## Common Pitfalls & Fixes
| Issue | Fix |
|-------|-----|
| Missing POIs | Check OSM type filters for `poi_` prefix |
| Road colors wrong | Use explicit style functions instead of pre-filtering |
| Map blank on mobile | Add viewport meta tag |

## Dependencies
- `osmconvert` (PBF processing)  
- `osm2geojson` (conversion)  
- `leaflet` (mapping)  
- `python3` (HTTP server)

## Example
```bash
osmconvert tongatapu.osm.pbf -B-o=tongatapu.osm.pbf
osm2geojson --input tongatapu.osm.pbf --output tongatapu_buildings.geojson
python3 -m http.server 8080
```