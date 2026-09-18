#!/usr/bin/env python3
"""
Local vision analysis using Ollama (llava:7b) to replace NVIDIA vision_analyze.
Outputs the same JSON schema for DaVinci Resolve technique extraction.
"""

import base64
import json
import sys
import os
import requests
from pathlib import Path
from typing import Dict, Any, Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:7b"
TIMEOUT = 180  # seconds

# JSON schema for DaVinci Resolve technique extraction
VISION_PROMPT = """Analyze this video frame for DaVinci Resolve color grading and editing techniques.
Identify and output ONLY valid JSON with these keys:
{
  "grading_style": "string (e.g., teal/orange, film look, log, S-Log3, Rec709, custom)",
  "camera_movement": "string (static, dolly, gimbal, handheld, tripod, slider, drone, crane)",
  "lighting": "string (key/fill ratio, soft/hard, natural, artificial, practical, mixed)",
  "effects": "array of strings (transitions, overlays, text, LUTs, filters, composites)",
  "color_temperature": "string (warm, cool, neutral, mixed)",
  "contrast_level": "string (high, low, medium, flat/log)",
  "saturation": "string (high, low, medium, desaturated)",
  "notes": "string (any additional DaVinci-relevant observations)"
}"""

def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_frame(image_path: str) -> Dict[str, Any]:
    """Send frame to local Ollama llava:7b and return parsed JSON."""
    img_b64 = encode_image(image_path)
    
    payload = {
        "model": MODEL,
        "prompt": VISION_PROMPT,
        "images": [img_b64],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_predict": 512
        }
    }
    
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        response_text = data.get("response", "").strip()
        
        # Extract JSON from response (llava often wraps in ```json```)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        return json.loads(response_text)
    
    except requests.exceptions.Timeout:
        return {"error": f"Timeout after {TIMEOUT}s", "image": image_path}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}", "image": image_path}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse failed: {e}", "raw_response": response_text, "image": image_path}

def analyze_video_frames(frame_dir: str, max_frames: int = 5) -> Dict[str, Any]:
    """Analyze multiple frames from a video (frame directory)."""
    frame_files = sorted([f for f in Path(frame_dir).glob("*.jpg") if not f.name.startswith("._")])[:max_frames]
    if not frame_files:
        frame_files = sorted([f for f in Path(frame_dir).glob("*.png") if not f.name.startswith("._")])[:max_frames]
    if not frame_files:
        frame_files = sorted([f for f in Path(frame_dir).glob("*.jpeg") if not f.name.startswith("._")])[:max_frames]
    
    results = []
    for frame in frame_files:
        result = analyze_frame(str(frame))
        result["frame"] = str(frame)
        results.append(result)
    
    # Aggregate results (simple majority/merge for now)
    return {
        "frames_analyzed": len(results),
        "frame_results": results,
        "aggregate": aggregate_results(results)
    }

def aggregate_results(results: list) -> Dict[str, Any]:
    """Simple aggregation of multiple frame analyses."""
    if not results:
        return {}
    
    # Take first non-error result as base, note variations
    base = None
    for r in results:
        if "error" not in r:
            base = r
            break
    
    if not base:
        return {"error": "All frames failed"}
    
    return base

def main():
    if len(sys.argv) < 2:
        print("Usage: local_vision_analyze.py <image_path|frame_dir> [max_frames]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    max_frames = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    path = Path(input_path)
    if path.is_file():
        result = analyze_frame(str(path))
        result["frame"] = str(path)
        print(json.dumps(result, indent=2))
    elif path.is_dir():
        result = analyze_video_frames(str(path), max_frames)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": f"Path not found: {input_path}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()