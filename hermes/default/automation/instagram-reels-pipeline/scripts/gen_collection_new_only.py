#!/usr/bin/env python3
"""
Generate per-collection NEW_ONLY URL files from full collections and deduplication results.

Usage:
    python3 gen_collection_new_only.py \
        --collections-dir instagram_saved_output/by_collection \
        --overlap overlap.txt \
        --output-dir instagram_new_urls_by_collection
"""

import json
import os
import argparse
from pathlib import Path


def load_urls(filepath):
    """Load URLs from flat text file."""
    urls = set()
    with open(filepath, 'r') as f:
        for line in f:
            url = line.strip()
            if url:
                urls.add(url.rstrip('/'))
    return urls


def main():
    parser = argparse.ArgumentParser(description='Generate per-collection NEW_ONLY URL files')
    parser.add_argument('--collections-dir', required=True, help='Directory with per-collection JSON files')
    parser.add_argument('--overlap', required=True, help='overlap.txt from dedupe script')
    parser.add_argument('--output-dir', required=True, help='Output directory for NEW_ONLY files')
    args = parser.parse_args()
    
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Load overlap URLs
    overlap_urls = load_urls(args.overlap)
    print(f"Loaded {len(overlap_urls)} overlap URLs")
    
    # Process each collection JSON
    collections_dir = Path(args.collections_dir)
    total_new = 0
    total_all = 0
    
    for json_file in sorted(collections_dir.glob('*.json')):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        coll_name = data.get('name', json_file.stem)
        items = data.get('items', [])
        
        # Get all URLs for this collection
        coll_urls = {item['url'].rstrip('/') for item in items}
        
        # Split into done vs new
        done_urls = coll_urls & overlap_urls
        new_urls = coll_urls - overlap_urls
        
        total_all += len(coll_urls)
        total_new += len(new_urls)
        
        if new_urls:
            # Write NEW_ONLY file
            safe_name = coll_name.replace('/', '_').replace(' ', '_').replace(':', '_')
            out_file = out_dir / f'{safe_name}_NEW.txt'
            with open(out_file, 'w') as f:
                for url in sorted(new_urls):
                    f.write(url + '\n')
            print(f"  {coll_name}: {len(new_urls)} new / {len(coll_urls)} total -> {out_file.name}")
        else:
            print(f"  {coll_name}: 0 new / {len(coll_urls)} total (all done)")
    
    print(f"\nTotal: {total_new} new / {total_all} total across {len(list(collections_dir.glob('*.json')))} collections")


if __name__ == '__main__':
    main()