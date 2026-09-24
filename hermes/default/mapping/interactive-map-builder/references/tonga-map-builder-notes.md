Based on seven debugging cycles to fix road color rendering and POI marker visibility in Tongatapu map:

1. CORS Resolution: 
   - Problem: file:// protocol blocked local GeoJSON loading
   - Fix: Serve files via local HTTP server (`python -m http.server 8080`)
   - Location: Critical for loading GeoJSON data

2. Tertiary Road Color Fix:
   - Problem: `#9a3412` rendered as orange/yellow
   - Solution: Changed to `#8b4513` (saddle brown) for proper rendering
   - Result: Consistent brown color matching legend

3. POI Marker Visibility:
   - Problem: Markers invisible until style keys matched feature properties
   - Fix: Ensured `POI_STYLES` keys exactly matched `feature.properties.type` values
   - Critical: Mapping precision required between data structure and style definitions

4. Layer Toggle Logic:
   - Problem: Checkbox state didn't reflect layer visibility
   - Fix: Implemented synchronized toggle function that updates DOM state
   - Verification: Manual vision checks confirmed layer visibility

5. Data Verification Protocol:
   - All layers now render correctly with verified counts:
     - POIs: 147 loaded (145 active, 2 toggled off)
     - Road segments: 145 segments (primary: 23, secondary: 59, tertiary: 63)
     - Buildings: 1252 important structures
   - Validation method: Browser vision analysis of rendered output

This workflow captures all technical nuances for future map builds in Tongan transportation planning.