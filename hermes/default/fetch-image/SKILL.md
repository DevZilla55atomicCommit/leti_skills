---
name: fetch-image
description: 'Fetch remote image to scratch, return MEDIA: path for chat.'
category: automation
---
# fetch-image Skill

Fetch a remote image and return a `MEDIA:` path that renders inline in Hermes desktop chat.

## Usage

```python
# In execute_code or delegate_task context
from hermes_tools import terminal

# Fetch and get MEDIA path
result = terminal(command='bash -c "cd ~/.hermes/cache/scratch && curl -sL -o lechon_$(date +%s).jpg \"https://example.com/image.jpg\" && realpath lechon_*.jpg | tail -1"')
# Returns MEDIA:/Users/alfredkamisese/.hermes/cache/scratch/lechon_1234567890.jpg
```

## Helper Function (recommended)

Add to your session or use inline:

```python
async def fetch_image(url: str, filename: str = None) -> str:
    """Download image from URL, return MEDIA: path for inline display."""
    import hashlib, os
    from hermes_tools import terminal
    
    # Generate deterministic filename from URL hash
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    ext = os.path.splitext(url.split('?')[0])[1] or '.jpg'
    if not ext.startswith('.'):
        ext = '.jpg'
    fname = filename or f'fetch_{url_hash}{ext}'
    
    scratch = os.path.expanduser('~/.hermes/cache/scratch')
    os.makedirs(scratch, exist_ok=True)
    fpath = os.path.join(scratch, fname)
    
    # Download with curl (follow redirects, timeout, silent)
    cmd = f'curl -sL --max-time 30 -o {fpath} {url}'
    result = terminal(command=cmd)
    
    if result['exit_code'] == 0 and os.path.exists(fpath) and os.path.getsize(fpath) > 0:
        return f'MEDIA:{fpath}'
    else:
        raise RuntimeError(f'Failed to fetch image: {result.get("error", "unknown")}')
```

## Direct Terminal One-Liner

```bash
# Quick fetch - returns MEDIA: path
cd ~/.hermes/cache/scratch && curl -sL -o img_$(date +%s).jpg "https://example.com/image.jpg" && echo "MEDIA:$(realpath img_*.jpg | tail -1)"
```

## Notes
- Images saved to `~/.hermes/cache/scratch/` (auto-pruned after 24h idle)
- No permanent storage — user saves manually if needed
- Supports any image format (jpg, png, webp, gif)
- Follows redirects, 30s timeout
- Returns `MEDIA:/absolute/path` for immediate inline render in chat

## Example Workflow

1. User asks: "Show me a Cebu lechon photo"
2. Agent searches web, gets image URL
3. Agent calls `fetch_image(url)` -> gets `MEDIA:/path/to/file`
4. Agent responds with that MEDIA: line -> image renders inline in chat
5. User sees image immediately, can right-click -> Save if they want to keep it

---
*This skill enables "show-and-forget" web images in Hermes chat without preview pane.*