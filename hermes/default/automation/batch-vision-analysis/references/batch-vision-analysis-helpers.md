# Batch Vision Analysis Reference

## Prompt Template
```text
Analyze this DaVinci Resolve technique reel frame.

Context:
- Video ID: {video_id}
- Collection: {collection}
- Caption: {caption}
- Known techniques: {techniques}
- Transcript: {transcript}

Return ONLY valid JSON with:
{
  "technique_name": "...",
  "resolve_page": "Color|Fusion|Edit|Fairlight",
  "node_graph_type": "Serial|Parallel|Layer Mixer|Compound",
  "key_nodes": ["..."],
  "parameters": {...},
  "steps_to_reproduce": ["..."]
}
```

## Progress Entry Schema
```json
{
  "video_id": "string",
  "collection": "string",
  "url": "https://www.instagram.com/reel/{video_id}",
  "caption": "string",
  "duration_sec": 0,
  "techniques": ["string"],
  "frames_analyzed": ["frame_xxx.jpg"],
  "frame_count": 0,
  "gif_path": "",
  "transcript_excerpt": "string",
  "analyzed_at": "ISO8601",
  "status": "complete|pending|error",
  "technique": "string",
  "resolve_page": "Color|Fusion|Edit|Fairlight|N/A",
  "node_graph": "Serial|Parallel|Layer Mixer|Compound|N/A",
  "key_nodes": ["string"],
  "parameters": {},
  "steps": ["string"],
  "frame_to_analyze": "path",
  "analysis_prompt": "string"
}
```

## Rate Limits
- 20 RPM = 3.2 seconds between calls
- 429 response: increase to 5-10s, retry
- Connection error: retry once after 5s

## Python Helpers
```python
import json, time, re
from datetime import datetime

def load_queue_progress(queue_path, progress_path):
    with open(queue_path) as f: queue = json.load(f)
    with open(progress_path) as f: progress = json.load(f)
    complete = {p['video_id'] for p in progress if p.get('status') == 'complete'}
    return queue, progress, [item for item in queue if item['video_id'] not in complete]

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: return {"raw_response": text, "parse_error": "Failed to parse JSON"}
    return {"raw_response": text, "parse_error": "No JSON found"}

def deduplicate_progress(progress):
    complete_ids = {p['video_id'] for p in progress if p.get('status') == 'complete'}
    return [p for p in progress if not (p.get('status') == 'pending' and p['video_id'] in complete_ids)]

def iso_now():
    return datetime.utcnow().isoformat() + "Z"
```