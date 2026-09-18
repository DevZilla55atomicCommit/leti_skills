# Tonga Ride-Hailing Map Technical Details

## Data Processing Pipeline

### 1. PBF to GeoJSON Conversion
```bash
# Convert full Tonga extract
osmconvert tonga-latest.osm.pbf -B-o=tonga.osm.pbf

# Convert Tongatapu island extract
osmconvert tongatapu.osm.pbf -B-o=tongatapu.osm.pbf

# Filter and convert to GeoJSON
osm2geojson --input tongatapu.osm.pbf \
  --filter '["amenity"="hospital"]|["highway"="primary"]|["building"="yes"]' \
  --output tongatapu_filtered.osm.pbf

osmconvert tongatapu_filtered.osm.pbf --no-strict -o=tongatapu_buildings.geojson
```

### 2. Style Configuration
```yaml
POI_STYLES:
  poi_amenities: '#FF5733'      # Food & Services
  poi_transport: '#3498DB'      # Transport Hubs
  poi_health: '#27AE60'         # Health Facilities
  POI_ICONS:
    default: marker-icon.png
    hospital: marker-hospital.png

ROAD_COLORS:
  primary: '#1e4e8c'            # Dark Blue
  secondary: '#2c7bb6'          # Medium Blue
  tertiary: '#7b9eb1'           # Light Blue
```

## Common Issues & Fixes
| Issue | Root Cause | Fix |
|-------|------------|-----|
| POIs not rendering | Incorrect OSM type filtering | Verify `amenity=*,highway=*,building=*` in filter |
| Road colors wrong | Pre-filtering logic error | Use explicit style functions instead |
| CORS errors | Loading via `file://` protocol | Always serve via `python3 -m http.server` |
| Mobile layout broken | Missing viewport meta | Add `<meta name="viewport" content="width=device-width">` |

## Performance Optimization
- For large OSM extracts (>50MB):  
  ```bash
  osm2pgsql --create --slim -C 2560 --hstore -d osm database.osm.pbf
  ```
- Use spatial indexes for large datasets:  
  ```bash
  shp2pgsql -s 4326 -I input.shp roads | psql -d osm
  ```

## Validation Checklist
- [ ] All POI markers visible at zoom levels 12-18  
- [ ] Road hierarchy correctly styled (primary > secondary > tertiary)  
- [ ] No CORS errors in browser console  
- [ ] Mobile layout responsive (tested on iPhone 12+)  
- [ ] Legend matches color scheme exactly  

Sources:  
- [Geofabrik Tonga](https://download.geofabrik.org/pacific-islands/tonga.html)  
- [Leaflet Color Guide](https://leafletjs.com/examples/color/index.html)