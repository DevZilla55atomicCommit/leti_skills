# Pipeline Automation - Reference Documents

## ID Mapping Issue

### Problem
Third-party downloaders (downreels.com) save MP4 files with their own internal IDs (e.g., `AQM-utMogMdFAjiQbB49g0Xw6ewUBer8DzROMvYK0Bx1xrjm0yyxYpU_pyQeKJG6mVXlRFPd5JHVRZTTAFFVZ4CBIyrsPr3n6zFPyUE.mp4`), not Instagram short IDs (e.g., `C-5PYQSADOG`).

Frame extraction creates directories using these internal IDs. Later stages expect Instagram short IDs.

### Solution
1. **Download order mapping**: Completed downloads are stored in `/tmp/reels_pipeline/completed.json` as Instagram short IDs in download order
2. **Frame directory order**: Frame directories are created in the same order as downloads
3. **Create mapping**: Map Instagram short ID → frame directory by matching download order to frame directory creation time

```python
# Load completed downloads (Instagram short IDs in order)
with open('/tmp/reels_pipeline/completed.json') as f:
    completed = json.load(f)

# Get frame directories sorted by creation time
frame_dirs = sorted(os.listdir(FRAMES_DIR), key=lambda d: os.path.getmtime(os.path.join(FRAMES_DIR, d)))

# Create mapping
id_map = {short_id: frame_dir for short_id, frame_dir in zip(completed, frame_dirs)}
```

4. **Update manifest**: Use mapping to set correct `frames_dir` in manifest for each reel

## Vision Analysis Rate Limiting

### Problem
Vision API has 20 RPM limit. Without rate limiting, requests fail.

### Solution
```python
VISION_RATE_LIMIT = 3  # seconds between calls (20 RPM = 3s)

for reel_id in reel_ids:
    await analyze_reel_vision(reel_id, extraction)
    await asyncio.sleep(VISION_RATE_LIMIT)  # 3s for 20 RPM
```

## External ID Mapping Pattern

### When to Use
Any time an external service uses different IDs than your internal system:
- downreels.com internal IDs vs Instagram short IDs
- YouTube video IDs vs internal IDs
- API client IDs vs database IDs

### Pattern
```python
# 1. Source IDs (your system)
source_ids = get_source_ids()  # e.g., Instagram short IDs from RTF

# 2. External IDs (downloader's system) - in download order
with open('completed.json') as f:
    external_ids = json.load(f)  # Instagram short IDs in download order

# 3. Output artifacts in external system's order
artifacts = get_artifacts_sorted_by_creation_time()  # Frame dirs, GIFs, etc.

# 4. Create mapping
id_map = {ext_id: artifact for ext_id, artifact in zip(external_ids, artifacts)}

# 5. Save for downstream use
with open('id_map.json', 'w') as f:
    json.dump(id_map, f, indent=2)
```

## Manifest-Driven Frame Resolution

### Problem
Frame directories may use external IDs. Code that assumes Instagram short IDs fails.

### Solution
Always use manifest's `frames_dir`:

```python
def get_frame_dir(reel_id: str, manifest_entry: Dict) -> Path:
    """Get frame directory, using manifest as source of truth."""
    # First try manifest's frames_dir
    frames_dir = manifest_entry.get('frames_dir', '')
    if frames_dir and os.path.exists(frames_dir):
        return Path(frames_dir)
    
    # Fallback: try Instagram short ID
    frame_dir = FRAMES_DIR / reel_id
    if frame_dir.exists():
        return frame_dir
    
    # Fallback: try ID mapping
    if reel_id in ID_MAP:
        mapped_dir = FRAMES_DIR / ID_MAP[reel_id]
        if mapped_dir.exists():
            return mapped_dir
    
    raise FileNotFoundError(f"No frame directory for {reel_id}")
```

## Cleanup Verification Pattern

### Before Deleting Temp
```python
def verify_cleanup_safe():
    """Verify temp files have been copied to vault before cleanup."""
    
    # 1. Count items in temp
    temp_frames = len(os.listdir(TEMP_FRAMES))
    temp_gifs = len(os.listdir(TEMP_GIFS))
    temp_mp4s = len(os.listdir(TEMP_MP4))
    
    # 2. Count items in vault
    vault_frames = count_vault_assets('frames')
    vault_gifs = count_vault_assets('gifs')
    vault_mp4s = count_vault_assets('mp4')
    
    # 3. Verify counts match (or vault has more)
    assert vault_frames >= temp_frames * 0.95, "Vault missing frames"
    assert vault_gifs >= temp_gifs * 0.95, "Vault missing GIFs"
    
    return True
```

## Rate Limiting Pattern

### Generic Rate Limiter
```python
import asyncio
from collections import deque
import time

class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = deque()
    
    async def acquire(self):
        now = time.time()
        # Remove old calls outside window
        while self.calls and self.calls[0] < now - self.window:
            self.calls.popleft()
        
        if len(self.calls) >= self.max_calls:
            wait = self.calls[0] + self.window - time.time()
            if wait > 0:
                await asyncio.sleep(wait)
        
        self.calls.append(time.time())
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, *args):
        pass

# Usage
vision_limiter = RateLimiter(20, 60)  # 20 calls per 60 seconds

async def analyze_with_rate_limit(reel_id, frame_dir):
    async with vision_limiter:
        return await analyze_reel_vision(reel_id, frame_dir)
```

## Key Files to Maintain

| File | Purpose | Updated By |
|------|---------|------------|
| `extraction_manifest.json` | Master catalog of all reels, frames, GIFs, MP4s | `extract.py` |
| `frame_id_map.json` | Instagram short ID → frame directory | `generate_id_mapping.py` |
| `completed.json` | Instagram short IDs in download order | `download_reels.py` |
| `id_to_frame_map.json` | Duplicate of frame_id_map.json | `generate_id_mapping.py` |

## Pipeline Stages That Must Not Skip

1. **Download** → `completed.json` (order matters!)
2. **Extract** → `extraction_manifest.json` (frames_dir must be correct!)
3. **Vision** → Rate limited (3s between calls for 20 RPM)
4. **Vault/Skill** → Uses manifest's `frames_dir` (NOT reel_id assumption)
5. **Cleanup** → Only after `verify_cleanup_safe()` passes