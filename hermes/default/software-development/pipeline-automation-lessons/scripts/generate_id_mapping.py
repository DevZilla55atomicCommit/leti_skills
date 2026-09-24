#!/usr/bin/env python3
"""
Generate ID mapping from downreels.com internal IDs to Instagram short IDs.

Run after downloads complete to create a mapping file that can be used
by the frame extraction and vision analysis scripts.
"""

import json
import os
from pathlib import Path

def generate_id_mapping():
    """Generate mapping from Instagram short IDs to frame directory names."""
    
    # Load completed downloads (Instagram short IDs in download order)
    completed_path = Path("/tmp/reels_pipeline/completed.json")
    with open(completed_path) as f:
        completed = json.load(f)
    
    # Get frame directories sorted by creation time (download order)
    frames_dir = Path("~/instagram-davinci-pipeline/temp/frames").expanduser()
    frame_dirs = os.listdir(frames_dir)
    frame_dirs.sort(key=lambda d: os.path.getmtime(os.path.join(frames_dir, d)))
    
    # Create mapping: Instagram short ID -> frame directory
    id_map = {}
    for i, short_id in enumerate(completed):
        if i < len(frame_dirs):
            id_map[short_id] = frame_dirs[i]
    
    # Save mapping
    output_path = Path("~/instagram-davinci-pipeline/temp/frame_id_map.json").expanduser()
    with open(output_path, 'w') as f:
        json.dump(id_map, f, indent=2)
    
    print(f"Created mapping for {len(id_map)} reels")
    print(f"Saved to {output_path}")
    
    return id_map

if __name__ == "__main__":
    generate_id_mapping()