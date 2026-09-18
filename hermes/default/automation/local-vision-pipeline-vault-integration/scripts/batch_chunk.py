#!/usr/bin/env python3
"""
Background batch processor for local vision analysis.
Processes a specific list of video indices.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path for local_vision_analyze
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.local_vision_analyze import analyze_video_frames

VISION_PROGRESS_PATH = "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json"
FRAMES_ROOTS = [
    Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames"),
    Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/PROCESSING/frames"),
]

def find_frame_dir(video_id: str) -> Path | None:
    for root in FRAMES_ROOTS:
        frame_dir = root / video_id
        if frame_dir.exists():
            frames = list(frame_dir.glob("*.jpg"))
            frames = [f for f in frames if not f.name.startswith("._")]
            if frames:
                return frame_dir
    return None

def process_chunk(chunk_indices: List[int], chunk_id: str) -> Dict[str, int]:
    """Process a chunk of video indices."""
    with open(VISION_PROGRESS_PATH, "r") as f:
        data = json.load(f)
    
    print(f"[Chunk {chunk_id}] Starting {len(chunk_indices)} videos...")
    
    processed = 0
    errors = 0
    
    for idx in chunk_indices:
        item = data[idx]
        vid = item["video_id"]
        frame_dir = find_frame_dir(vid)
        
        if not frame_dir:
            item["status"] = "error"
            item["error"] = "No frames found"
            print(f"[Chunk {chunk_id}] {vid}: No frames")
            errors += 1
            continue
        
        print(f"[Chunk {chunk_id}] Processing {vid}...")
        
        start = time.time()
        result = analyze_video_frames(str(frame_dir), 3)
        elapsed = time.time() - start
        
        if "error" not in result.get("aggregate", {}):
            agg = result["aggregate"]
            item["status"] = "complete"
            item["technique"] = f"{agg.get('grading_style', 'unknown')} grading"
            item["resolve_page"] = "Color"
            item["node_graph"] = "Serial"
            item["key_nodes"] = ["Curves", "Color Wheels"]
            item["parameters"] = {
                "grading_style": agg.get("grading_style"),
                "camera_movement": agg.get("camera_movement"),
                "lighting": agg.get("lighting"),
                "effects": agg.get("effects", []),
                "color_temperature": agg.get("color_temperature"),
                "contrast_level": agg.get("contrast_level"),
                "saturation": agg.get("saturation"),
            }
            item["frame_to_analyze"] = str(sorted(frame_dir.glob("*.jpg"))[0])
            item["analysis_prompt"] = "Local llava:7b vision analysis"
            item["steps"] = [
                "Open Color page",
                f"Apply {agg.get('grading_style')}",
                f"Match {agg.get('camera_movement')}",
                f"Lighting: {agg.get('lighting')}"
            ]
            item["local_vision_frames"] = result["frames_analyzed"]
            item["vision_model"] = "llava:7b"
            item["analyzed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"  OK ({elapsed:.1f}s, {result['frames_analyzed']} frames)")
            processed += 1
        else:
            item["error"] = result["aggregate"]["error"]
            print(f"  FAILED - {result['aggregate']['error']}")
            errors += 1
        
        time.sleep(1)
    
    # Write back (this chunk's updates)
    with open(VISION_PROGRESS_PATH, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"[Chunk {chunk_id}] Complete! Processed: {processed}, Errors: {errors}")
    return {"processed": processed, "errors": errors}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 batch_chunk.py <comma_separated_indices> <chunk_id>")
        sys.exit(1)
    
    indices = [int(x) for x in sys.argv[1].split(",")]
    chunk_id = sys.argv[2]
    process_chunk(indices, chunk_id)