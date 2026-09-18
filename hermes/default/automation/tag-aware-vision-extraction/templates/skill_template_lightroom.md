---
name: davinci-photography-{{subcategory}}-{{reel_id[:8]}}
description: |
  Photography/Video technique from Instagram Reel {{reel_id}}
  Category: photography → {{subcategory}}
  Source: https://www.instagram.com/reel/{{reel_id}}/
  Educational focus: {{educational_focus}}
version: 1.0.0
category: creative
tags:
  - photography
  - {{subcategory}}
  - {{tags_list}}
references:
  - "instagram_reel_id": "{{reel_id}}"
  - "source_url": "https://www.instagram.com/reel/{{reel_id}}/"
  - "category": "photography"
  - "subcategory": "{{subcategory}}"
  - "analyzed_at": "{{analyzed_at}}"
---

# davinci-photography-{{subcategory}}-{{reel_id[:8]}}

## Overview
Technique extracted from Instagram Reel `{{reel_id}}` demonstrating **{{subcategory.replace('_', ' ')}}** in photography/videography.

## Key Techniques

{% for technique in techniques %}
- **{{technique}}**
{% endfor %}

## Structured Extraction
```json
{{extracted_data}}
```

## Application
See vault note for camera settings, lighting, composition, and post-processing workflows.

## Practice Exercises
1. Recreate the lighting setup described
2. Match the camera settings
3. Apply the composition technique

## Related Skills
- `davinci-photography-{{subcategory}}`

## Metadata
- **Reel ID:** {{reel_id}}
- **Category:** photography
- **Subcategory:** {{subcategory}}
- **Source:** https://www.instagram.com/reel/{{reel_id}}/
- **Analyzed:** {{analyzed_at}}