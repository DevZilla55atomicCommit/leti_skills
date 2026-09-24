#!/bin/bash
# Script to generate Tongatapu mapping assets
# Usage: ./generate-data.sh

python3 extract_pois.py

# Convert POIs to GeoJSON format
python3 << 'PYEOF'
import json

with open('/Users/alfredkamisese/tongatapu_key_pois.json', 'r') as f:
    pois = json.load(f)

features = [{
    'type': 'Feature',
    'geometry': {'type': 'Point', 'coordinates': [p['lon'], p['lat']]},
    'properties': p
} for p in pois]

geojson = {'type': 'FeatureCollection', 'features': features}
with open('tongatapu_key_pois.geojson', 'w') as f:
    json.dump(geojson, f)
PYEOF

echo "✅ Data generation complete"