---
name: tonga-ride-hailing-infrastructure
tags:
  - transportation
  - ride-hailing
  - tonga
  - osrm
  - osm
description: Tonga ride‑hailing infra analysis and routing guide.
benchmarks: []
---
# Tonga Ride-Hailing Infrastructure Analysis

**Trigger**: Use when building or researching a ride-hailing (e.g., Uber-like) service in Tonga, focusing on infrastructure mapping, POI extraction, routing, and address modeling.

## Core Output
- Structured OSM-based POI inventory for Tongatapu (hotels, airports, fuel stations, govt offices, schools, etc.)
- Road network classification (primary, secondary, tertiary)
- Demand node zoning (airport corridor, CBD, waterfront, suburbs)
- Address pattern guide (landmark → road → village)
- Gap analysis vs. Google Maps coverage
- Sample OSRM/Valhalla configuration notes
- Glossary of Tongan place names & administrative zones

## Key Steps
1. **Download OSM extract** for Tongatapu (Geofabrik).
2. **Run OSRM/Valhalla** to generate routing profile.
3. **Create Gazetteer** mapping local names to coordinates.
4. **Validate high‑value POIs** with local driver.
5. **Design address UX** for landmark‑based entry.
6. **Field‑test** with driver for real‑world coverage.

## Pitfalls
- OSM lacks house numbers; rely on landmarks.
- Speed limits absent; assume urban 40 km/h.
- Separate ferry terminal requires special handling.
- Local naming varies; maintain custom alias table.

## Support Files
- `references/tonga-infrastructure-data.md` – full POI list and road network summary (see `references/` folder).
- `scripts/generate-osm-extract.sh` – example script to download and extract OSM data.
- `templates/ride-hailing-gazetteer.yaml` – template for landmark‑based address mapping.