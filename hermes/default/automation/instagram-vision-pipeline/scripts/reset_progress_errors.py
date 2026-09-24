#!/usr/bin/env python3
"""
Reset VISION_PROGRESS.json errored entries to pending when frames exist.
Run when local workers failed but frames are available.
"""

import json
from pathlib import Path

VISION_PROGRESS_PATH = Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json")

def main():
    with open(VISION_PROGRESS_PATH) as f:
        data = json.load(f)
    
    reset_count = 0
    frame_not_found = 0
    
    for v in data:
        if v.get('status') == 'error':
            frame_path = v.get('frame_to_analyze')
            if frame_path and Path(frame_path).exists():
                v['status'] = 'pending'
                v['error'] = None
                reset_count += 1
            else:
                frame_not_found += 1
    
    print(f"Reset {reset_count} errored entries to pending")
    print(f"Left as error (frame not found): {frame_not_found}")
    
    temp = VISION_PROGRESS_PATH.with_suffix('.tmp')
    with open(temp, 'w') as f:
        json.dump(data, f, indent=2)
    temp.replace(VISION_PROGRESS_PATH)
    print("Saved.")

if __name__ == "__main__":
    main()