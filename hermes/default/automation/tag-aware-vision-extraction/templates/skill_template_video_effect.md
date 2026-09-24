---
name: davinci-{{category}}-{{subcategory}}-{{reel_id[:8]}}
description: |
  DaVinci Resolve {{subcategory.replace('_', ' ').title()} technique from Instagram Reel {{reel_id}}
  Category: {{category}} → {{subcategory}}
  Source: https://www.instagram.com/reel/{{reel_id}}/
  Educational focus: {{educational_focus}}
version: 1.0.0
category: creative
tags:
  - davinci-resolve
  - {{category}}
  - {{subcategory}}
  - {{tags_list}}
references:
  - "instagram_reel_id": "{{reel_id}}"
  - "source_url": "https://www.instagram.com/reel/{{reel_id}}/"
  - "category": "{{category}}"
  - "subcategory": "{{subcategory}}"
  - "analyzed_at": "{{analyzed_at}}"
---

# davinci-{{category}}-{{subcategory}}-{{reel_id[:8]}}

## Overview
Technique extracted from Instagram Reel `{{reel_id}}` demonstrating **{{subcategory.replace('_', ' ')}}** in DaVinci Resolve.

## Key Techniques

{% for technique in techniques %}
- **{{technique}}**
{% endfor %}

## Structured Extraction
```json
{{extracted_data}}
```

## Application in DaVinci Resolve
See vault note for node structures, settings, and workflows.

## Practice Exercises
1. Build the node structure described above
2. Match the exact parameters from the extraction
3. Test on your own footage

## Related Skills
- `davinci-{{category}}-{{subcategory}}`

## Metadata
- **Reel ID:** {{reel_id}}
- **Category:** {{category}}
- **Subcategory:** {{subcategory}}
- **Source:** https://www.instagram.com/reel/{{reel_id}}/
- **Analyzed:** {{analyzed_at}}