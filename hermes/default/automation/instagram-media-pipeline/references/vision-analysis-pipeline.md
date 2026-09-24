# Vision Analysis Pipeline for Instagram Reels

## Overview
Automated 3-frame vision analysis per reel to extract DaVinci Resolve applicable techniques, color grades, and cinematography metadata.

## Frame Selection Strategy
- **Frame 1**: Start (0% duration) — intro/hook, camera settings, establishing shot
- **Frame 2**: Middle (~50% duration) — main content, technique demonstration
- **Frame 3**: End (~95% duration) — outro, final result, call-to-action

## Vision Analysis Schema (per frame)

```json
{
  "reel_id": "string",
  "collection": "string",
  "techniques": ["technique1", "technique2"],
  "node_structure": "description of node graph if visible",
  "color_grade": "description of look/grade",
  "camera_movement": "static/handheld/gimbal/drone/dolly/etc",
  "lighting_setup": "key/fill/backlight, natural, practical, etc",
  "composition_notes": "framing, rule of thirds, leading lines, depth",
  "daVinci_applicable": true/false,
  "key_timestamps": [0.0, 9.5, 19.0],
  "confidence": 0.85
}
```

## Focus Areas for Analysis

| Category | What to Extract |
|----------|-----------------|
| **DaVinci UI** | Node graphs, color wheels, curves, qualifiers, power windows, keyframes |
| **Color Grading** | Teal/orange, film emulation, halation, LUTs, CST, split toning |
| **Camera** | Movement, exposure, focal length, aperture, shutter, ISO, framing |
| **Lighting** | Setup (3-point, natural, practical), quality (hard/soft), direction, color temp |
| **Composition** | Rule of thirds, leading lines, depth layers, foreground framing, negative space |
| **Educational Value** | Is this teachable in DaVinci Resolve? Would a colorist/videographer benefit? |

## Rate Limiting & Timing

| Constraint | Value |
|------------|-------|
| Vision calls per reel | 3 (3 frames) |
| Delay between calls | 3 seconds minimum |
| Your RPM limit | 20 RPM |
| Recommended batch | 10 reels → wait 60s → next batch |
| Total time per reel | ~15-20 seconds (3 calls × 3s + processing) |

## Transcription (Skipped)

**Tool**: Whisper.cpp (base model)  
**Status**: BROKEN on M-series Mac — PyTorch/TypeGuard import errors in venv  
**Workaround**: Skip gracefully, log as "transcription unavailable"  
**Note**: Most reels have minimal speech (music/voiceover only); text overlays captured via vision

## Pipeline Integration

```
download → extract (frames, GIF, transcript) → vision (3 frames) → skill + vault → cleanup
    ↓           ↓              ↓               ↓           ↓
 10 reels   10×frames/    30 vision     10 skills +  10 notes → 
  ~5 min    GIF/transcript   calls         10 vaults   cleanup
```

## Known Issues & Workarounds

| Issue | Cause | Workaround |
|-------|-------|------------|
| C9FAL50v1is vision report empty ("pending_vision") | Vision not run during batch | Manual `vision_analyze` on 3 frames post-download |
| Whisper.cpp import fails | PyTorch/TypeGuard on M-series venv | Skip transcript, log "music only" or "no speech" |
| Vision 429 errors | Exceeded 20 RPM | Exponential backoff (3s→6s→12s) |
| Frame extraction timeouts | Video not loaded in headless | Wait for `video.readyState >= 2` |
| Download verification | File size < 10KB = failed | Check `stat().st_size > 10000` |

## Output Artifacts per Reel

| File | Location | Purpose |
|------|----------|---------|
| `vision_reports/{reel_id}.json` | Pipeline root | Full frame-by-frame analysis |
| `temp/frames/{reel_id}/` | Temp | 1fps JPEG frames (cleaned up) |
| `temp/gifs/{reel_id}.gif` | Temp | 5s preview GIF (cleaned up) |
| `temp/mp4/{reel_id}.mp4` | Temp | Source MP4 (cleaned up) |
| `~/.hermes/skills/creative/davinci-reel-{id[:8]}/` | Hermes skills | Skill + QUICK_REF.md |
| `~/Obsidian/EMAI/Instagram Reels/{collection}/{reel_id}.md` | Vault | Note with media refs, skill link, quick grade |

## Rate Limit Tracking

```python
# Simple token bucket
import time

class RateLimiter:
    def __init__(self, rpm=20):
        self.min_interval = 60.0 / rpm
        self.last_call = 0
    
    async def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        self.last_call = time.time()
```