#!/usr/bin/env python3
"""
Instagram Saved Collections Parser

Parses Instagram's saved_collections.json export into structured data.
Handles the deeply nested label_values -> dict -> dict -> dict structure.

Usage:
    python3 parse_saved_collections.py --input saved_collections.json --output-dir ./output
"""

import json
import csv
import os
import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path


def parse_timestamp(ts):
    """Convert Unix timestamp to ISO string, handling None/invalid."""
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(ts).isoformat()
    except (ValueError, OSError):
        return None


def extract_hashtags(hashtags_info):
    """Extract hashtag strings from the nested hashtags structure."""
    hashtags = []
    if not hashtags_info or 'dict' not in hashtags_info:
        return hashtags

    for h_group in hashtags_info['dict']:
        if 'dict' not in h_group:
            continue
        for h_item in h_group['dict']:
            # The actual hashtag is in the 'value' field, label is "Name"
            val = h_item.get('value')
            if val:
                hashtags.append(val)
    return hashtags


def extract_owner(owner_info):
    """Extract owner name and username from nested owner structure."""
    owner_name = ''
    owner_username = ''
    if not owner_info or 'dict' not in owner_info:
        return owner_name, owner_username

    for o in owner_info['dict']:
        if 'dict' not in o:
            continue
        for o2 in o['dict']:
            if o2.get('label') == 'Name':
                owner_name = o2.get('value', '')
            elif o2.get('label') == 'Username':
                owner_username = o2.get('value', '')
    return owner_name, owner_username


def extract_brand_partner(brand_info):
    """Extract brand partner name from nested structure."""
    if not brand_info or 'dict' not in brand_info:
        return ''
    for b in brand_info['dict']:
        if 'dict' not in b:
            continue
        for b2 in b['dict']:
            if b2.get('label') == 'Name':
                return b2.get('value', '')
    return ''


def parse_collection(collection):
    """Parse a single collection object into list of media items."""
    # Get collection name
    coll_name = 'Unknown'
    for lv in collection.get('label_values', []):
        if lv.get('label') == 'Name':
            coll_name = lv.get('value', 'Unknown')
            break

    # Get creation and update timestamps
    created_ts = collection.get('timestamp')
    updated_ts = None
    for lv in collection.get('label_values', []):
        if lv.get('label') == 'Update time' and lv.get('timestamp_value'):
            updated_ts = lv['timestamp_value']
            break

    # Find the Media container
    media_container = None
    for lv in collection.get('label_values', []):
        if lv.get('title') == 'Media' and 'dict' in lv:
            media_container = lv['dict']
            break

    if not media_container:
        return []

    items = []
    for item in media_container:
        item_dict = item.get('dict', [])
        if len(item_dict) < 6:
            continue

        # Each item has 6 elements in fixed order:
        # 0: URL, 1: Caption, 2: Title, 3: Hashtags, 4: Owner, 5: Brand partner
        url_info = item_dict[0]
        caption_info = item_dict[1]
        title_info = item_dict[2]
        hashtags_info = item_dict[3]
        owner_info = item_dict[4]
        brand_info = item_dict[5]

        media = {
            'collection': coll_name,
            'collection_created': parse_timestamp(created_ts),
            'collection_updated': parse_timestamp(updated_ts),
            'url': url_info.get('value', ''),
            'href': url_info.get('href', ''),
            'caption': caption_info.get('value', ''),
            'title': title_info.get('value', ''),
            'hashtags': extract_hashtags(hashtags_info),
            'owner': '',
            'owner_username': '',
            'brand_partner': extract_brand_partner(brand_info)
        }

        owner_name, owner_username = extract_owner(owner_info)
        media['owner'] = owner_name
        media['owner_username'] = owner_username

        items.append(media)

    return items


def parse_saved_collections(input_path):
    """Parse the full saved_collections.json file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_items = []
    collection_stats = {}

    for collection in data:
        items = parse_collection(collection)
        coll_name = items[0]['collection'] if items else 'Unknown'
        collection_stats[coll_name] = len(items)
        all_items.extend(items)

    return all_items, collection_stats


def generate_analytics(all_items, collection_stats):
    """Generate global analytics from parsed items."""
    hashtag_counter = Counter()
    owner_counter = Counter()

    for item in all_items:
        for h in item['hashtags']:
            hashtag_counter[h] += 1
        if item['owner']:
            owner_counter[item['owner']] += 1
        elif item['owner_username']:
            owner_counter[f"@{item['owner_username']}"] += 1

    # Date ranges
    created_dates = []
    updated_dates = []
    for item in all_items:
        if item['collection_created']:
            created_dates.append(item['collection_created'])
        if item['collection_updated']:
            updated_dates.append(item['collection_updated'])

    return {
        'total_items': len(all_items),
        'total_collections': len(collection_stats),
        'items_by_collection': dict(sorted(collection_stats.items(), key=lambda x: -x[1])),
        'top_hashtags': dict(hashtag_counter.most_common(200)),
        'top_creators': dict(owner_counter.most_common(200)),
        'collection_date_range': {
            'earliest_created': min(created_dates) if created_dates else None,
            'latest_created': max(created_dates) if created_dates else None,
            'earliest_updated': min(updated_dates) if updated_dates else None,
            'latest_updated': max(updated_dates) if updated_dates else None,
        }
    }


def write_outputs(all_items, analytics, output_dir):
    """Write all output formats to output directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Full JSON
    json_path = output_dir / 'instagram_saved_clean.json'
    write_json_output(all_items, analytics, json_path)
    print(f"JSON: {json_path}")

    # CSV
    csv_path = output_dir / 'instagram_saved_clean.csv'
    write_csv_output(all_items, csv_path)
    print(f"CSV: {csv_path}")

    # Per-collection JSONs
    coll_dir = output_dir / 'by_collection'
    coll_dir.mkdir(exist_ok=True)
    write_per_collection_json(all_items, coll_dir)
    print(f"Per-collection JSON: {coll_dir} ({len(analytics['items_by_collection'])} files)")

    # Markdown summary
    md_path = output_dir / 'analytics_summary.md'
    write_markdown_summary(analytics, md_path)
    print(f"Markdown summary: {md_path}")

    print("\nDone!")
    print(f"  Total items: {analytics['total_items']:,}")
    print(f"  Total collections: {analytics['total_collections']}")
    top_coll = max(analytics['items_by_collection'], key=analytics['items_by_collection'].get)
    print(f"  Top collection: {top_coll} ({analytics['items_by_collection'][top_coll]})")
    top_tag = max(analytics['top_hashtags'], key=analytics['top_hashtags'].get)
    print(f"  Top hashtag: #{top_tag} ({analytics['top_hashtags'][top_tag]})")
    top_creator = max(analytics['top_creators'], key=analytics['top_creators'].get)
    print(f"  Top creator: {top_creator} ({analytics['top_creators'][top_creator]})")


def main():
    parser = argparse.ArgumentParser(
        description='Parse Instagram saved_collections.json export'
    )
    parser.add_argument('--input', '-i', required=True,
                        help='Path to saved_collections.json')
    parser.add_argument('--output-dir', '-o', default='./instagram_saved_output',
                        help='Output directory (default: ./instagram_saved_output)')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    print(f"Parsing: {input_path}")
    all_items, collection_stats = parse_saved_collections(input_path)
    print(f"Found {len(all_items)} items across {len(collection_stats)} collections")

    print("Generating analytics...")
    analytics = generate_analytics(all_items, collection_stats)

    print(f"Writing outputs to: {args.output_dir}")
    write_outputs(all_items, analytics, args.output_dir)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())