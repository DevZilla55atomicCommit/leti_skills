# Tongatapu Ride-Hailing Mapping Workflow

## Phase 1: Data Extraction

1. **Download OSM Extract**:  
   `wget https://download.geofabrik.de/pacific/oz/data-latest.osm.pbf -O tongatapu.osm.pbf`  
   Then filter Tongatapu region (lat -21.27 to -20.81, lon -175.36 to -175.03) using `osmconvert` + `--left-tile`, `--right-tile`, `--top-node`, `--bottom-node`.

2. **POI Classification**:  
   Run `python3 extract_pois.py` using the provided `/Users/alfredkamisese/extract_pois.py` script. It outputs:
   - `tongatapu_key_pois.json` (147 curated POIs)
   - `tongatapu_major_roads.geojson` (road network)
   - `tongatapu_buildings.geojson` (68,694 building footprints)

## Phase 2: Map Generation

1. **POI GeoJSON Conversion**:  
   ```python3
   import json
   with open('tongatapu_key_pois.json') as f: 
       pois = json.load(f)
   features = [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [p['lon'], p['lat']]}, 'properties': p} for p in pois]
   with open('tongatapu_key_pois.geojson', 'w') as f: json.dump({'type': 'FeatureCollection', 'features': features}, f)
   ```

2. **Aggregate into HTML Template**:  
   Replace placeholder paths in `templates/map-config.html` with generated GeoJSON URLs. Then open `tongatapu_map.html` in the preview pane.

## Phase 3: Deployment

1. **Test**:  
   Load HTML in Hermes preview pane (`open_preview`). Verify all layers toggle, popups display, and legend colors match the key.

2. **Iterate**:  
   Update `references/mapping-workflow.md` with new discoveries. Use `skill_manage(action='patch', name='tonga-ridehailing-mapping', old_string='...', new_string='...')` to persist changes.

## Output Files
- `tongatapu_key_pois.geojson` (147 POIs)
- `tongatapu_major_roads.geojson` (149 road segments)
- `tongatapu_buildings.geojson` (building footprints)
- `tongatapu_map.html` (interactive map)