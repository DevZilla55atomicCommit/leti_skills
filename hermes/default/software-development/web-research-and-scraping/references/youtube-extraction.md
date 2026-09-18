# YouTube Content Extraction Reference

> **Note:** YouTube is NOT effectively scrapable via Firecrawl or standard HTTP scraping due to heavy JS rendering, anti-bot measures, and dynamic content loading. Use dedicated tools instead.

---

## Recommended Tools for YouTube

### 1. **yt-dlp** (Best for: downloading videos, extracting metadata, thumbnails, subtitles)
```bash
# Install
pip install yt-dlp

# Extract video info (no download)
yt-dlp --dump-json "https://youtube.com/watch?v=VIDEO_ID"

# Download best quality + auto-generated subtitles
yt-dlp -f "bestvideo+bestaudio" --write-auto-sub --sub-lang en "URL"

# Extract audio only
yt-dlp -x --audio-format mp3 "URL"

# Get playlist info
yt-dlp --flat-playlist --dump-json "https://youtube.com/playlist?list=PLAYLIST_ID"
```

### 2. **YouTube Transcript API** (Best for: getting captions/transcripts without video download)
```bash
pip install youtube-transcript-api

# Python usage
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript("VIDEO_ID")
# Returns: [{'text': '...', 'start': 0.0, 'duration': 5.0}, ...]
```

### 3. **YouTube Data API v3** (Best for: search, channel info, playlist metadata)
- Requires API key from Google Cloud Console
- Quota: 10,000 units/day (search = 100 units, video list = 1 unit)
- Use for: finding video IDs by search query, then feed to yt-dlp/transcript API

### 4. **Browser Automation** (Last resort - what Hermes browser tools can do)
- Navigate to search results page
- Click video → expand description → click "Show transcript" 
- Extract transcript text via `browser_console` or snapshot
- **Limitation:** Rate limited, flaky, requires manual interaction patterns

---

## Pattern: YouTube → Obsidian Vault Pipeline

```python
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from datetime import datetime

VAULT_PATH = "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Color Grading & Looks"

def extract_youtube_tutorial(url_or_id):
    """Extract transcript + metadata from YouTube video, save as markdown."""
    
    # Resolve video ID
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url_or_id, download=False)
        video_id = info['id']
        title = info['title']
        channel = info.get('uploader', 'Unknown')
        upload_date = info.get('upload_date', '')
        description = info.get('description', '')
        tags = info.get('tags', [])
        duration = info.get('duration', 0)
    else:
        video_id = url_or_id
        # Fetch metadata separately
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
        title = info['title']
        channel = info.get('uploader', 'Unknown')
        upload_date = info.get('upload_date', '')
        description = info.get('description', '')
        tags = info.get('tags', [])
        duration = info.get('duration', 0)
    
    # Get transcript
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([f"[{int(t['start']//60):02d}:{int(t['start']%60):02d}] {t['text']}" for t in transcript_list])
    except Exception as e:
        transcript_text = f"[Transcript unavailable: {e}]"
    
    # Build markdown
    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()[:100]
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"yt_{video_id}_{safe_title}_{date_str}.md"
    filepath = os.path.join(VAULT_PATH, filename)
    
    md_content = f"""---
source: youtube
video_id: {video_id}
url: https://youtube.com/watch?v={video_id}
title: "{title}"
channel: {channel}
upload_date: {upload_date}
duration_seconds: {duration}
tags: {json.dumps(tags)}
extracted_date: {datetime.now().isoformat()}
vault_category: color-grading
resolve_version: auto-detect-from-content
---

# {title}

**Channel:** {channel}  
**Video:** https://youtube.com/watch?v={video_id}  
**Uploaded:** {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}  
**Duration:** {duration//60}:{duration%60:02d}

## Description
{description[:2000]}{'...' if len(description) > 2000 else ''}

## Tags
{', '.join(tags[:20])}{'...' if len(tags) > 20 else ''}

## Transcript
{transcript_text}
"""
    
    with open(filepath, 'w') as f:
        f.write(md_content)
    
    return filepath


def search_and_extract(query, max_results=10):
    """Search YouTube via yt-dlp, extract top results."""
    # yt-dlp can search: ytsearchN:"query"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }
    
    search_url = f"ytsearch{max_results}:{query}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(search_url, download=False)
    
    videos = []
    for entry in results.get('entries', []):
        if entry:
            videos.append({
                'id': entry.get('id'),
                'title': entry.get('title'),
                'url': entry.get('url') or f"https://youtube.com/watch?v={entry.get('id')}",
                'channel': entry.get('uploader'),
                'duration': entry.get('duration'),
            })
    
    return videos


# Example usage for DaVinci Resolve color grading tutorials
if __name__ == "__main__":
    queries = [
        "cinematic color grading davinci resolve 19 tutorial",
        "cinematic color grading davinci resolve 20 tutorial", 
        "cinematic color grading davinci resolve 21 tutorial",
        "davinci resolve 19 color grading workflow",
        "davinci resolve 20 new color grading tutorial film look",
        "davinci resolve node structure color grading",
        "davinci resolve power grades tutorial",
        "davinci resolve film emulation lut tutorial",
    ]
    
    for query in queries:
        print(f"\n=== Searching: {query} ===")
        videos = search_and_extract(query, max_results=5)
        for v in videos:
            print(f"  - {v['title']} ({v['id']}) - {v['channel']}")
            # Uncomment to extract:
            # extract_youtube_tutorial(v['id'])
```

---

## Mapping to Vault Memory.md

After extracting videos, update the domain's `Memory.md` with entries like:

```markdown
### YouTube Tutorials (Auto-Extracted)
- **Cinematic Color Grading | DaVinci Resolve 19 | BMPCC 6K Pro** (Mediabee Color Lab)
  - Video ID: `abc123xyz`
  - File: `yt_abc123xyz_Cinematic_Color_Grading_DaVinci_Resolve_19_20250705.md`
  - Topics: Dehancer Pro, Mononodes DCTLs, Voyager LUT, CST, Primary/Secondary grading
  - [Link](yt_abc123xyz_Cinematic_Color_Grading_DaVinci_Resolve_19_20250705.md)

- **Create Your Film Grade in DaVinci Resolve – Ultimate Tutorial** (Cullen Kelly)
  - Video ID: `def456uvw`
  - File: `yt_def456uvw_Create_Your_Film_Grade_DaVinci_Resolve_20250705.md`
  - Topics: Node structure, film emulation, look development
  - [Link](yt_def456uvw_Create_Your_Film_Grade_DaVinci_Resolve_20250705.md)
```

---

## Rate Limits & Best Practices

| Tool | Limits | Mitigation |
|------|--------|------------|
| yt-dlp | None (client-side) | Add `--sleep-interval 2` between requests |
| YouTube Transcript API | None official | Cache transcripts locally |
| YouTube Data API | 10k units/day | Use sparingly for search only; prefer yt-dlp search |

---

## DaVinci Resolve Version Detection

From video title/description/tags, auto-detect version:
- "Resolve 19" / "DaVinci 19" → v19
- "Resolve 20" / "DaVinci 20" / "v20" → v20  
- "Resolve 21" / "DaVinci 21" / "v21" → v21
- "Resolve 18" / older → legacy
- No version mentioned → check upload date (v19: late 2023, v20: late 2024, v21: 2025)

---

## Files Created This Session

*None yet - this reference documents the pattern for future extraction runs*