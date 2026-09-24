# Flux Image Generation Quickstart

## Prerequisites
- Ollama running (default: localhost:11434)
- Flux model installed: `ollama pull x/flux2-klein:4b`
- Python 3.9+ with `requests` library

## Generation Script
Run this Python snippet to test generation:

```python
import requests, base64, json, os
from datetime import datetime
from pathlib import Path

OLLAMA_URL = 'http://localhost:11434'
MODEL = 'x/flux2-klein:4b'
OUTPUT_ROOT = Path.home() / 'Pictures' / 'Flux_Generations'

prompt = 'cinematic portrait, Sony A7IV S-Log3, Kodak 2383 film look, 85mm f1.4, golden hour rim lighting, shallow depth of field'
width = 1024
height = 1024
steps = 8
project = 'test_project'

project_dir = OUTPUT_ROOT / project
project_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%H%M%S')
safe_prompt = ''.join(c if c.isalnum() or c in '-_' else '_' for c in prompt[:50])
filename = f'{timestamp}_{safe_prompt}.png'
filepath = project_dir / filename

payload = {
    'model': MODEL,
    'prompt': prompt,
    'width': width,
    'height': height,
    'steps': steps,
    'stream': False,
}

resp = requests.post(f'{OLLAMA_URL}/api/generate', json=payload, timeout=300)
data = resp.json()

if 'image' in data:
    img_bytes = base64.b64decode(data['image'])
    filepath.write_bytes(img_bytes)
    meta = {
        'prompt': prompt,
        'model': MODEL,
        'width': width,
        'height': height,
        'steps': steps,
        'timestamp': datetime.now().isoformat(),
        'project': project,
        'filepath': str(filepath),
    }
    (filepath.with_suffix('.json')).write_text(json.dumps(meta, indent=2))
    print(f'Generated: {filepath}')
    print(f'Size: {len(img_bytes)} bytes')
else:
    print('Error:', data.get('error', 'No image returned'))
```