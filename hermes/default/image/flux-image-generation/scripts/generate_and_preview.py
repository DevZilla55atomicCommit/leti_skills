import requests
import base64
import json
import os
from datetime import datetime
from pathlib import Path

OLLAMA_URL = 'http://localhost:11434'
MODEL = 'x/flux2-klein:latest'
OUTPUT_ROOT = Path.home() / 'Pictures' / 'Flux_Generations'

prompt = """Professional advertisement poster for "Kailahi BBQ" Hawaiian BBQ restaurant, bold vibrant advertisement typography with island-style hand-lettered logo "KAILAHI BBQ" in tropical sunset gradient colors (coral, teal, golden yellow, palm green), warm golden hour lighting, shallow depth of field, happy multigenerational Hawaiian family (grandparents, parents, children) laughing and sharing a feast at a long wooden picnic table under string lights, overflowing plates of authentic Hawaiian BBQ: kalua pig pulled pork with cabbage, huli huli chicken with char marks, grilled mahi-mahi with mango salsa, Portuguese sausage, haupia coconut pudding, poi, macaroni salad, white rice, grilled pineapple rings, corn on the cob, vibrant tropical flowers (plumeria, hibiscus, bird of paradise) as table decor, tiki torches, palm trees swaying in background, ocean sunset backdrop, cinematic lifestyle photography, Sony A7IV, 35mm f/1.4 GM lens, golden hour warm rim lighting, Kodak Portra 400 film emulation, warm highlight rolloff, teal-orange color grade, high dynamic range, film grain texture, editorial advertising photography aesthetic, professional commercial quality, joyful welcoming atmosphere, 1024x1536 portrait poster orientation"""

width = 1024
height = 1536
steps = 8
project = 'kailahi-bbq-poster'

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

print(f"Generating Kailahi BBQ poster...")
print(f"Project: {project}")
print(f"Output: {filepath}")
print(f"Dimensions: {width}x{height}, Steps: {steps}")

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
    print(f"\nGenerated: {filepath}")
    print(f"Size: {len(img_bytes)} bytes")
    print(f"Metadata saved: {filepath.with_suffix('.json')}")
    # open preview in UI
    from hermes_tools import open_preview
    open_preview(url=f'file://{filepath}')
else:
    print('Error:', data.get('error', 'No image returned'))
    print('Full response:', json.dumps(data, indent=2)[:2000])