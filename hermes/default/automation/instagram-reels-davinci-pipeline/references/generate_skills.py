#!/usr/bin/env python3
"""
Generate Hermes skills from vision analysis results.
Reads VISION_PROGRESS.json, extracts completed techniques, writes SKILL.md files.
"""

import json
import re
from pathlib import Path
from datetime import datetime

# Paths
PROGRESS_FILE = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
SKILLS_DIR = Path.home() / '.hermes' / 'skills' / 'davinci-resolve-techniques'
SKILLS_DIR.mkdir(parents=True, exist_ok=True)

def slugify(text):
    """Convert text to valid skill name slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    with open(PROGRESS_FILE) as f:
        data = json.load(f)

    completed = [v for v in data if v.get('status') == 'complete' and v.get('result')]
    print(f"Processing {len(completed)} completed videos...")

    for video in completed:
        video_id = video['video_id']
        result = video['result']

        technique_name = result.get('technique_name', 'Unknown Technique')
        resolve_page = result.get('resolve_page', 'Color')
        node_graph_type = result.get('node_graph_type', 'serial')
        key_nodes = result.get('key_nodes', [])
        parameters = result.get('parameters', {})
        steps = result.get('steps_to_reproduce', [])
        difficulty = result.get('difficulty', 'intermediate')
        tags = result.get('tags', [])

        skill_slug = slugify(technique_name)
        skill_name = f'davinci-{skill_slug}'

        # Build frontmatter
        tag_list = ', '.join([f'"{t}"' for t in tags])
        frontmatter = f"""---
name: {skill_name}
description: DaVinci Resolve technique: {technique_name} from Instagram Reel {video_id}
category: davinci-resolve
tags: [{tag_list}, "davinci-resolve", "color-grading", "instagram-reel"]
difficulty: {difficulty}
resolve_page: {resolve_page}
node_graph_type: {node_graph_type}
key_nodes: {key_nodes}
parameters: {parameters}
steps: {steps}
source_reel: {video_id}
updated_at: {datetime.now().isoformat()}
---
"""

        # Build body
        body = f"""# {technique_name}

**Source**: Instagram Reel `{video_id}`

## Node Graph
Type: `{node_graph_type}`

## Key Nodes
{chr(10).join(f'- {node}' for node in key_nodes)}

## Parameters
```json
{json.dumps(parameters, indent=2)}
```

## Steps to Reproduce
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(steps))}

## Tags
{', '.join(tags)}

## Difficulty
{difficulty}

## Resolve Page
{resolve_page}
"""

        skill_path = SKILLS_DIR / f'{skill_name}.md'
        with open(skill_path, 'w') as f:
            f.write(frontmatter + body)

        print(f"Created: {skill_name}")

    print(f"\nDone! Generated {len(completed)} skills.")

if __name__ == '__main__':
    main()