#!/usr/bin/env python3
"""
Background batch processor for local vision analysis.
Processes a specific list of video indices in parallel.
"""

import json
import time
import sys
from pathlib import Path

sys.path.insert(0, "/Users/alfredkamisese/vision_pipeline")
from local_vision_analyze import analyze_video_frames

VISION_PROGRESS_PATH = "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json"
FRAMES_ROOTS = [
    Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames"),
    Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/PROCESSING/frames"),
]

def find_frame_dir(video_id):
    for root in FRAMES_ROOTS:
        frame_dir = root / video_id
        if frame_dir.exists():
            frames = list(frame_dir.glob("*.jpg"))
            frames = [f for f in frames if not f.name.startswith("._")]
            if frames:
                return frame_dir
    return None

def process_chunk(chunk_indices, chunk_id):
    """Process a chunk of video indices."""
    with open(VISION_PROGRESS_PATH, "r") as f:
        data = json.load(f)
    
    print(f"[Chunk {chunk_id}] Starting {len(chunk_indices)} videos...")
    
    for idx in chunk_indices:
        item = data[idx]
        vid = item["video_id"]
        frame_dir = find_frame_dir(vid)
        
        if not frame_dir:
            item["status"] = "error"
            item["error"] = "No frames found"
            print(f"[Chunk {chunk_id}] {vid}: No frames")
            continue
        
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
            print(f"[Chunk {chunk_id}] {vid}: OK ({elapsed:.1f}s, {result['frames_analyzed']} frames)")
        else:
            item["error"] = result["aggregate"]["error"]
            print(f"[Chunk {chunk_id}] {vid}: FAILED - {result['aggregate']['error']}")
        
        time.sleep(1)
    
    # Write back (this chunk's updates)
    with open(VISION_PROGRESS_PATH, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"[Chunk {chunk_id}] Complete! Saved progress.")

if __name__ == "__main__":
    # Chunk indices passed as comma-separated args
    if len(sys.argv) < 2:
        print("Usage: python3 batch_chunk.py <comma_separated_indices> <chunk_id>")
        sys.exit(1)
    
    indices = [int(x) for x in sys.argv[1].split(",")]
    chunk_id = sys.argv[2] if len(sys.argv) > 2 else "1"
    process_chunk(indices, chunk_id)