#!/usr/bin/env python3
"""
Tongatapu Map Verification Script
Verifies counts for POIs, roads, and buildings after map build.
Run after Python data files are loaded via serve-script.py.
"""

import json
import re

def verify_data():
    # Load data files
    with open('tongatapu_key_pois.geojson') as f:
        pois = json.load(f)['features']
    
    with open('tongatapu_major_roads.geojson') as f:
        roads = json.load(f)['features']
    
    with open('tongatapu_buildings.geojson') as f:
        buildings = json.load(f)['features']
    
    # Print counts
    print(f"[VERIFICATION START]")
    print(f"POIs loaded: {len(pois)} (expected ≥145, loaded: {len(pois)})")
    print(f"Road segments: {len(roads)} (expected 145, loaded: {len(roads)})")
    print(f"Buildings: {len(buildings)} (expected ≥1200)")
    
    # Validate thresholds
    assert len(pois) >= 145, f"POI count ({len(pois)}) below minimum 145"
    assert len(roads) == 145, f"Road segments ({len(roads)}) not exactly 145"
    assert len(buildings) >= 1200, f"Building count ({len(buildings)}) below minimum 1200"
    
    # Print validation status
    print(f"[VERIFICATION PASSED] All counts valid")
    return True

if __name__ == "__main__":
    verify_data()