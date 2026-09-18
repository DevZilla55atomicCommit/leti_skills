#!/usr/bin/env python3
"""
Batch process pending/error videos using local Ollama llava:7b.
Updates VISION_PROGRESS.json with results.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# Import our local vision analyzer
sys.path.insert(0, "/Users/alfredkamisese/vision_pipeline")
from local_vision_analyze import analyze_video_frames

VISION_PROGRESS_PATH = "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json"
FRAMES_ROOTS = [
    Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames"),
    Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/PROCESSING/frames"),
]

MAX_FRAMES_PER_VIDEO = 5
DELAY_BETWEEN_VIDEOS = 2  # seconds

def load_progress() -> List[Dict]:
    with open(VISION_PROGRESS_PATH, "r") as f:
        return json.load(f)

def save_progress(data: List[Dict]):
    with open(VISION_PROGRESS_PATH, "w") as f:
        json.dump(data, f, indent=2)

def find_frame_dir(video_id: str) -> Path | None:
    for root in FRAMES_ROOTS:
        frame_dir = root / video_id
        if frame_dir.exists():
            frames = list(frame_dir.glob("*.jpg"))
            frames = [f for f in frames if not f.name.startswith("._")]
            if frames:
                return frame_dir
    return None

def process_video(item: Dict, max_frames: int = MAX_FRAMES_PER_VIDEO) -> Dict:
    video_id = item["video_id"]
    frame_dir = find_frame_dir(video_id)
    
    if not frame_dir:
        return {"status": "error", "error": "No frames found", "video_id": video_id}
    
    print(f"  Processing {video_id} ({len(list(frame_dir.glob('*.jpg')))} frames)...")
    
    result = analyze_video_frames(str(frame_dir), max_frames)
    
    if "error" in result.get("aggregate", {}):
        return {"status": "error", "error": result["aggregate"]["error"], "video_id": video_id}
    
    # Build technique record
    agg = result["aggregate"]
    technique_record = {
        "status": "complete",
        "technique": f"{agg.get('grading_style', 'unknown')} grading, {agg.get('camera_movement', 'unknown')} movement",
        "resolve_page": "Color",
        "node_graph": "Serial",
        "key_nodes": ["Curves", "Color Wheels"],
        "parameters": {
            "grading_style": agg.get("grading_style"),
            "camera_movement": agg.get("camera_movement"),
            "lighting": agg.get("lighting"),
            "effects": agg.get("effects", []),
            "color_temperature": agg.get("color_temperature"),
            "contrast_level": agg.get("contrast_level"),
            "saturation": agg.get("saturation"),
        },
        "frame_to_analyze": str(sorted(frame_dir.glob("*.jpg"))[0]),
        "analysis_prompt": "Local llava:7b vision analysis",
        "steps": [
            "Open Color page in DaVinci Resolve",
            f"Apply {agg.get('grading_style', 'custom')} grading style",
            f"Match {agg.get('camera_movement', 'static')} camera movement",
            f"Set lighting: {agg.get('lighting', 'mixed')}",
        ],
        "local_vision_frames": result["frames_analyzed"],
        "vision_model": "llava:7b",
        "analyzed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    
    return technique_record

def main():
    data = load_progress()
    
    # Find pending/error videos
    to_process = [i for i, item in enumerate(data) if item.get("status") in ("pending_vision", "error")]
    
    print(f"Found {len(to_process)} videos to process")
    print(f"Total: {len(data)} | Complete: {sum(1 for d in data if d.get('status') == 'complete')}")
    
    processed = 0
    for idx in to_process:
        item = data[idx]
        video_id = item["video_id"]
        
        print(f"\n[{processed + 1}/{len(to_process)}] {video_id} ({item.get('collection', 'unknown')})")
        
        result = process_video(item)
        
        # Update item
        if result.get("status") == "complete":
            for k, v in result.items():
                if k not in ("video_id", "status"):
                    item[k] = v
            item["status"] = "complete"
            print(f"  ✓ Complete")
        else:
            item["status"] = "error"
            item["error"] = result.get("error", "Unknown error")
            print(f"  ✗ Error: {result.get('error')}")
        
        processed += 1
        
        # Save progress every 5 videos
        if processed % 5 == 0:
            save_progress(data)
            print(f"  Saved progress ({processed}/{len(to_process)})")
        
        time.sleep(DELAY_BETWEEN_VIDEOS)
    
    # Final save
    save_progress(data)
    print(f"\nDone! Processed {processed} videos.")
    
    # Summary
    complete = sum(1 for d in data if d.get("status") == "complete")
    error = sum(1 for d in data if d.get("status") == "error")
    pending = sum(1 for d in data if d.get("status") == "pending_vision")
    print(f"Final: Complete={complete}, Error={error}, Pending={pending}")

if __name__ == "__main__":
    main()