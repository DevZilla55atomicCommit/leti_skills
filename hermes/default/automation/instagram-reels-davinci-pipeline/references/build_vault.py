#!/usr/bin/env python3
"""
Build Obsidian vault from vision analysis results.
Creates markdown notes with embedded GIFs, frontmatter, and cross-links.
"""

import json
import re
import shutil
from pathlib import Path

# Paths
PROGRESS_FILE = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
GIFS_DIR = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/gifs')
VAULT_DIR = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/vault')

# Vault structure
TECHNIQUES_DIR = VAULT_DIR / 'techniques'
COLLECTIONS_DIR = VAULT_DIR / 'collections'
TAGS_DIR = VAULT_DIR / 'tags'
MEDIA_DIR = VAULT_DIR / 'media'

for d in [TECHNIQUES_DIR, COLLECTIONS_DIR, TAGS_DIR, MEDIA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def slugify(text):
    """Convert text to valid filename slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    with open(PROGRESS_FILE) as f:
        data = json.load(f)

    completed = [v for v in data if v.get('status') == 'complete' and v.get('result')]
    print(f"Building vault for {len(completed)} techniques...")

    # Group for indexes
    collections = {}
    tags_by_name = {}

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

        # Determine collection from video_id or tags
        collection = 'cinematic'
        if any('wedding' in t for t in tags):
            collection = 'wedding'
        elif any('urban' in t for t in tags):
            collection = 'urban'
        elif any('landscape' in t for t in tags):
            collection = 'landscape'
        elif any('macro' in t for t in tags):
            collection = 'macro'
        elif any('aerial' in t for t in tags):
            collection = 'aerial'

        # Group for indexes
        if collection not in collections:
            collections[collection] = []
        collections[collection].append(video)

        for tag in tags:
            if tag not in tags_by_name:
                tags_by_name[tag] = []
            tags_by_name[tag].append(video)

        # Copy GIF if exists
        gif_src = GIFS_DIR / f'{video_id}.gif'
        gif_dst = MEDIA_DIR / f'{slugify(technique_name)}.gif'
        if gif_src.exists() and not gif_dst.exists():
            shutil.copy2(gif_src, gif_dst)

        # Build technique note
        technique_slug = slugify(technique_name)
        note_content = f"""---
video_id: {video_id}
technique_name: {technique_name}
collection: {collection}
resolve_page: {resolve_page}
node_graph_type: {node_graph_type}
key_nodes: {key_nodes}
parameters: {parameters}
difficulty: {difficulty}
tags: {tags}
source_reel: {video_id}
---

# {technique_name}

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

## Media
![{technique_name}](media/{technique_slug}.gif)

## Tags
{', '.join(f'[[#{tag}]]' for tag in tags)}

## Collection
[[{collection}]]
"""

        note_path = TECHNIQUES_DIR / f'{technique_slug}.md'
        with open(note_path, 'w') as f:
            f.write(note_content)

    # Write collection indexes
    for coll_name, videos in collections.items():
        coll_content = f"""---
collection: {coll_name}
count: {len(videos)}
---

# {coll_name.title()} Collection

{len(videos)} techniques

## Techniques
{chr(10).join(f'- [[{slugify(v["result"].get("technique_name", "Unknown"))}]]' for v in videos)}
"""
        (COLLECTIONS_DIR / f'{coll_name}.md').write_text(coll_content)

    # Write tag indexes
    for tag_name, videos in tags_by_name.items():
        tag_content = f"""---
tag: {tag_name}
count: {len(videos)}
---

# {tag_name}

{len(videos)} techniques

## Techniques
{chr(10).join(f'- [[{slugify(v["result"].get("technique_name", "Unknown"))}]]' for v in videos)}
"""
        (TAGS_DIR / f'{slugify(tag_name)}.md').write_text(tag_content)

    # Write master index
    master_content = [
        "# DaVinci Resolve Techniques Vault",
        "",
        f"Total Techniques: {len(completed)}",
        f"Collections: {len(collections)}",
        f"Tags: {len(tags_by_name)}",
        "",
        "## Collections",
        ""
    ]

    for coll_name in sorted(collections.keys()):
        master_content.append(f"- [[{coll_name}]] ({len(collections[coll_name])} techniques)")

    master_content.extend(["", "## Tags", ""])
    for tag_name in sorted(tags_by_name.keys()):
        master_content.append(f"- [[#{tag_name}]] ({len(tags_by_name[tag_name])} techniques)")

    master_content.extend(["", "## Recent Techniques", ""])
    for video in completed[-20:]:
        tech_name = video['result'].get('technique_name', 'Unknown')
        master_content.append(f"- [[{slugify(tech_name)}]]")

    (VAULT_DIR / 'index.md').write_text('\n'.join(master_content))

    print(f"\nDone! Vault created at: {VAULT_DIR}")
    print(f"Techniques: {len(completed)}")
    print(f"Collections: {len(collections)}")
    print(f"Tags: {len(tags_by_name)}")

if __name__ == '__main__':
    main()