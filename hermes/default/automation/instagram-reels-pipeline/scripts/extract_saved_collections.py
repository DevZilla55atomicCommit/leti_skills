#!/usr/bin/env python3
"""
Extract Instagram Saved Collections Export to structured outputs.

Features:
- Per-collection JSON with full metadata
- Flat CSV for spreadsheet analysis
- Markdown grouped by collection
- Flat URL list (all)
- Per-collection URL files
- NEW_ONLY URL files (deduplicated against KB)
- Collection processing stats

Usage:
    python3 extract_saved_collections.py \
        --input ~/Downloads/instagram-tamazila-2026-07-20-0Ni7mnhM/your_instagram_activity/saved/saved_collections.json \
        --output-dir ~/Downloads/instagram_saved_output \
        --kb-urls ~/Downloads/kb_instagram_urls.txt \
        --new-only-dir ~/Downloads/instagram_new_urls_by_collection
"""

import json
import csv
import os
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime


def load_kb_urls(kb_urls_file):
    """Load known KB URLs for deduplication."""
    kb_urls = set()
    if kb_urls_file and os.path.exists(kb_urls_file):
        with open(kb_urls_file) as f:
            for line in f:
                url = line.strip().rstrip('/')
                if url:
                    kb_urls.add(url)
    return kb_urls


def extract_collections(input_file):
    """Parse saved_collections.json and yield (collection_name, items) tuples."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for collection in data:
        # Get collection name
        coll_name = "Unknown"
        media_container = None
        
        for lv in collection.get('label_values', []):
            if lv.get('label') == 'Name':
                coll_name = lv.get('value', 'Unknown')
            if lv.get('title') == 'Media' and 'dict' in lv:
                media_container = lv['dict']
        
        if not media_container:
            continue
        
        items = []
        for item in media_container:
            item_dict = item.get('dict', [])
            if len(item_dict) < 6:
                continue
            
            url_info = item_dict[0]
            caption_info = item_dict[1]
            hashtags_info = item_dict[3]
            owner_info = item_dict[4]
            brand_info = item_dict[5]
            
            url = url_info.get('value', '').strip()
            if not url or 'instagram.com' not in url:
                continue
            
            # Extract hashtags
            hashtags = []
            if 'dict' in hashtags_info:
                for h_group in hashtags_info['dict']:
                    if 'dict' in h_group:
                        for h_item in h_group['dict']:
                            val = h_item.get('value') or h_item.get('label')
                            if val and val != 'Name':
                                hashtags.append(val)
            
            # Extract owner
            owner = ''
            owner_username = ''
            if 'dict' in owner_info:
                for o in owner_info['dict']:
                    if 'dict' in o:
                        for o2 in o['dict']:
                            if o2.get('label') == 'Name':
                                owner = o2.get('value', '')
                            elif o2.get('label') == 'Username':
                                owner_username = o2.get('value', '')
            
            # Extract brand
            brand = ''
            if 'dict' in brand_info:
                for b in brand_info['dict']:
                    if 'dict' in b:
                        for b2 in b['dict']:
                            if b2.get('label') == 'Name':
                                brand = b2.get('value', '')
            
            items.append({
                'url': url,
                'href': url_info.get('href', ''),
                'caption': caption_info.get('value', ''),
                'hashtags': hashtags,
                'owner': owner,
                'owner_username': owner_username,
                'brand_partner': brand
            })
        
        yield coll_name, items


def sanitize_filename(name):
    """Sanitize collection name for filesystem."""
    for ch in ['/', ' ', ':', 'ð', 'â', '¦', 'Ÿ', '¨']:
        name = name.replace(ch, '_')
    while '__' in name:
        name = name.replace('__', '_')
    return name.strip('_')


def main():
    parser = argparse.ArgumentParser(description='Extract Instagram Saved Collections export')
    parser.add_argument('--input', required=True, help='Path to saved_collections.json')
    parser.add_argument('--output-dir', default='./instagram_saved_output', help='Output directory')
    parser.add_argument('--csv', help='Output CSV file (optional)')
    parser.add_argument('--kb-urls', help='File with known KB URLs for deduplication')
    parser.add_argument('--new-only-dir', help='Output directory for NEW_ONLY URL files')
    args = parser.parse_args()
    
    kb_urls = load_kb_urls(args.kb_urls)
    print(f"Loaded {len(kb_urls)} known KB URLs")
    
    os.makedirs(args.output_dir, exist_ok=True)
    if args.new_only_dir:
        os.makedirs(args.new_only_dir, exist_ok=True)
    
    all_items = []
    collection_stats = []
    
    for coll_name, items in extract_collections(args.input):
        safe_name = sanitize_filename(coll_name)
        
        # Save per-collection JSON
        json_path = os.path.join(args.output_dir, f'{safe_name}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'collection': coll_name,
                'count': len(items),
                'items': items
            }, f, indent=2, ensure_ascii=False)
        
        # Save URL list (all)
        urls_path = os.path.join(args.output_dir, f'{safe_name}_urls.txt')
        with open(urls_path, 'w') as f:
            for item in items:
                f.write(item['url'].rstrip('/') + '\n')
        
        # Save NEW_ONLY URL list (deduplicated)
        if args.new_only_dir:
            new_items = [item for item in items if item['url'].rstrip('/') not in kb_urls]
            new_only_path = os.path.join(args.new_only_dir, f'{safe_name}_NEW.txt')
            with open(new_only_path, 'w') as f:
                for item in new_items:
                    f.write(item['url'].rstrip('/') + '\n')
            
            done = len(items) - len(new_items)
            collection_stats.append({
                'collection': coll_name,
                'total': len(items),
                'done': done,
                'new': len(new_items)
            })
        
        # Accumulate for CSV
        for item in items:
            all_items.append({
                'collection': coll_name,
                'url': item['url'],
                'caption': item['caption'][:500],
                'hashtags': ' '.join(f'#{h}' for h in item['hashtags']),
                'owner': item['owner'],
                'owner_username': item['owner_username'],
                'brand_partner': item['brand_partner']
            })
        
        print(f"  {coll_name}: {len(items)} items")
    
    # Write CSV
    if args.csv:
        with open(args.csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['collection', 'url', 'caption', 'hashtags', 'owner', 'owner_username', 'brand_partner'])
            writer.writeheader()
            writer.writerows(all_items)
        print(f"CSV written: {args.csv}")
    
    # Print collection stats
    if args.new_only_dir:
        print("\n=== Collection Processing Status ===")
        print(f"{'Collection':<40} {'Total':>6} {'Done':>6} {'New':>6}")
        print("-" * 60)
        for stat in sorted(collection_stats, key=lambda x: -x['new']):
            print(f"{stat['collection']:<40} {stat['total']:>6} {stat['done']:>6} {stat['new']:>6}")
        
        total_done = sum(s['done'] for s in collection_stats)
        total_new = sum(s['new'] for s in collection_stats)
        total_all = sum(s['total'] for s in collection_stats)
        print("-" * 60)
        print(f"{'TOTAL':<40} {total_all:>6} {total_done:>6} {total_new:>6}")


if __name__ == '__main__':
    main()