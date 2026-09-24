#!/usr/bin/env python3
"""
Local Ollama Vision Batch Worker - uses qwen3-vl:8b on port 11434
Rate: ~20 RPM (3s delay) to avoid overwhelming the model
"""

import json
import time
import base64
import requests
import re
import threading
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

VISION_PROGRESS_PATH = Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json")
MODEL = "qwen3-vl:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_WORKERS = 2
RATE_LIMIT_SECONDS = 3.0  # ~20 RPM
BATCH_SIZE = 10

last_call_time = 0
rate_lock = threading.Lock()

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] {msg}")

def encode_image(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def extract_json(text):
    """Extract JSON from qwen3-vl output (handles markdown blocks, thinking tags)"""
    # Remove thinking tags
    text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)
    
    # Try markdown code blocks
    for pattern in [r'```json\s*(.*?)\s*```', r'```\s*(.*?)\s*```']:
        matches = re.findall(pattern, text, re.DOTALL)
        for m in matches:
            try:
                return json.loads(m.strip())
            except:
                continue
    
    # Try direct JSON
    try:
        return json.loads(text.strip())
    except:
        pass
    
    # Find first complete JSON object
    try:
        start = text.index('{')
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i+1])
    except:
        pass
    
    raise ValueError(f"No valid JSON in: {text[:300]}")

def rate_limited_vision_analyze(frame_path, video_id):
    global last_call_time
    
    with rate_lock:
        elapsed = time.time() - last_call_time
        if elapsed < RATE_LIMIT_SECONDS:
            time.sleep(RATE_LIMIT_SECONDS - elapsed)
        last_call_time = time.time()
    
    b64 = encode_image(frame_path)
    
    prompt = f"""Analyze this DaVinci Resolve technique from Instagram Reel {video_id}.

Return ONLY valid JSON:
{{
  "technique_name": "Descriptive name",
  "resolve_page": "Color|Edit|Fusion|Fairlight",
  "node_graph_type": "serial|parallel|layer_mixer|compound",
  "key_nodes": ["node1", "node2"],
  "parameters": {{"param1": "value1"}},
  "steps_to_reproduce": ["step1", "step2"],
  "difficulty": "beginner|intermediate|advanced",
  "tags": ["tag1", "tag2"]
}}"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [b64],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 1024}
    }
    
    start = time.time()
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
        elapsed = time.time() - start
        
        if resp.status_code != 200:
            raise Exception(f"API error {resp.status_code}: {resp.text[:200]}")
        
        result = resp.json()
        response_text = result.get('response', '')
        parsed = extract_json(response_text)
        return parsed, elapsed
        
    except requests.Timeout:
        raise Exception("Vision analyze timeout (180s)")
    except Exception as e:
        raise Exception(f"Vision analyze failed: {e}")

def process_batch(batch_size=BATCH_SIZE):
    with open(VISION_PROGRESS_PATH) as f:
        progress = json.load(f)
    
    pending = [v for v in progress if v.get('status') == 'pending']
    log(f"Found {len(pending)} pending, processing {min(batch_size, len(pending))} with {MAX_WORKERS} workers")
    
    if not pending:
        return {"processed": 0, "errors": 0, "done": True}
    
    batch = pending[:batch_size]
    processed = 0
    errors = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for video in batch:
            frame_path = video.get('frame_to_analyze')
            if frame_path and Path(frame_path).exists():
                futures[executor.submit(rate_limited_vision_analyze, frame_path, video['video_id'])] = video
            else:
                video['status'] = 'error'
                video['error'] = 'Frame not found'
                errors += 1
                log(f"  ✗ {video['video_id']}: Frame not found")
        
        for future in as_completed(futures):
            video = futures[future]
            try:
                parsed, elapsed = future.result()
                video['status'] = 'complete'
                video['result'] = parsed
                video['updated_at'] = datetime.now().isoformat()
                processed += 1
                log(f"  ✓ {video['video_id']}: {parsed.get('technique_name', 'unknown')} ({elapsed:.1f}s)")
            except Exception as e:
                video['status'] = 'error'
                video['error'] = str(e)[:500]
                errors += 1
                log(f"  ✗ {video['video_id']}: {str(e)[:100]}")
    
    # Save atomically
    temp = VISION_PROGRESS_PATH.with_suffix('.tmp')
    with open(temp, 'w') as f:
        json.dump(progress, f, indent=2)
    temp.replace(VISION_PROGRESS_PATH)
    
    log(f"BATCH DONE: processed={processed}, errors={errors}, remaining={len(pending)-batch_size}")
    return {"processed": processed, "errors": errors, "done": len(pending) <= batch_size}

if __name__ == "__main__":
    log("=" * 50)
    log(f"LOCAL OLLAMA VISION WORKER ({MAX_WORKERS} parallel, {MODEL})")
    log(f"API: {OLLAMA_URL}")
    log("=" * 50)
    
    while True:
        result = process_batch(batch_size=BATCH_SIZE)
        if result["done"]:
            log("ALL DONE!")
            break
        time.sleep(1)