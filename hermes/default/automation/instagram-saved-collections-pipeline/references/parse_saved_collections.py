#!/usr/bin/env python3
"""
Parse Instagram saved_collections.json export into structured data.
Outputs: clean JSON, CSV, per-collection JSON, markdown URL list, flat URL list.
"""
import json
import csv
import os
from collections import Counter
from datetime import datetime

def parse_saved_collections(input_path, output_dir):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_items = []

    for collection in data:
        coll_name = None
        for lv in collection.get('label_values', []):
            if lv.get('label') == 'Name':
                coll_name = lv.get('value')
                break

        media_container = None
        for lv in collection.get('label_values', []):
            if lv.get('title') == 'Media' and 'dict' in lv:
                media_container = lv['dict']
                break

        if not media_container:
            continue

        for item in media_container:
            item_dict = item.get('dict', [])
            if len(item_dict) < 6:
                continue

            url_info = item_dict[0]
            caption_info = item_dict[1]
            hashtags_info = item_dict[3]
            owner_info = item_dict[4]
            brand_info = item_dict[5]

            media = {
                'collection': coll_name,
                'url': url_info.get('value', '').rstrip('/'),
                'href': url_info.get('href', '').rstrip('/'),
                'caption': caption_info.get('value', ''),
                'hashtags': [],
                'owner': '',
                'owner_username': '',
                'brand_partner': ''
            }

            # Parse hashtags (value field has the tag name)
            if 'dict' in hashtags_info:
                for h_group in hashtags_info['dict']:
                    if 'dict' in h_group:
                        for h_item in h_group['dict']:
                            val = h_item.get('value')
                            if val:
                                media['hashtags'].append(val)

            # Parse owner
            if 'dict' in owner_info:
                for o in owner_info['dict']:
                    if 'dict' in o:
                        for o2 in o['dict']:
                            if o2.get('label') == 'Name':
                                media['owner'] = o2.get('value', '')
                            elif o2.get('label') == 'Username':
                                media['owner_username'] = o2.get('value', '')

            # Parse brand partner
            if 'dict' in brand_info:
                for b in brand_info['dict']:
                    if 'dict' in b:
                        for b2 in b['dict']:
                            if b2.get('label') == 'Name':
                                media['brand_partner'] = b2.get('value', '')

            all_items.append(media)

    print(f"Total media items parsed: {len(all_items)}")

    # Summary stats
    coll_counts = Counter(i['collection'] for i in all_items)
    all_hashtags = Counter()
    for item in all_items:
        for h in item['hashtags']:
            all_hashtags[h] += 1
    all_owners = Counter()
    for item in all_items:
        if item['owner']:
            all_owners[item['owner']] += 1
        elif item['owner_username']:
            all_owners[f"@{item['owner_username']}"] += 1

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    coll_dir = os.path.join(output_dir, 'by_collection')
    os.makedirs(coll_dir, exist_ok=True)

    # 1. Full clean JSON
    clean_json = {
        'total_items': len(all_items),
        'total_collections': len(coll_counts),
        'collections': dict(coll_counts),
        'top_hashtags': dict(all_hashtags.most_common(500)),
        'top_creators': dict(all_owners.most_common(500)),
        'items': all_items
    }
    with open(os.path.join(output_dir, 'instagram_saved_clean.json'), 'w', encoding='utf-8') as f:
        json.dump(clean_json, f, indent=2, ensure_ascii=False)

    # 2. CSV for spreadsheet
    with open(os.path.join(output_dir, 'instagram_saved_clean.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Collection', 'URL', 'Caption', 'Hashtags', 'Owner', 'Owner_Username', 'Brand_Partner'])
        for item in all_items:
            writer.writerow([
                item['collection'],
                item['url'],
                item['caption'][:500],
                ' '.join(f'#{h}' for h in item['hashtags'][:50]),
                item['owner'],
                item['owner_username'],
                item['brand_partner']
            ])

    # 3. Markdown per collection
    with open(os.path.join(output_dir, 'instagram_saved_urls_by_collection.md'), 'w', encoding='utf-8') as md:
        md.write("# Instagram Saved Collections — URLs Only\n\n")
        md.write(f"*Generated from Instagram data export — {len(coll_counts)} collections, {len(all_items)} total items*\n\n")
        md.write("---\n\n")
        for coll_name in sorted(coll_counts.keys()):
            coll_items = [i for i in all_items if i['collection'] == coll_name]
            md.write(f"## {coll_name} ({len(coll_items)} items)\n\n")
            for idx, item in enumerate(coll_items, 1):
                md.write(f"{idx}. {item['url']}\n")
            md.write("\n---\n\n")

    # 4. Flat URL list
    with open(os.path.join(output_dir, 'instagram_all_urls_flat.txt'), 'w') as f:
        for item in all_items:
            f.write(item['url'] + '\n')

    # 5. Per-collection JSON files
    for coll_name, count in coll_counts.items():
        coll_items = [i for i in all_items if i['collection'] == coll_name]
        safe_name = coll_name.replace('/', '_').replace(' ', '_').replace(':', '_')
        coll_path = os.path.join(coll_dir, f'{safe_name}.json')
        with open(coll_path, 'w', encoding='utf-8') as f:
            json.dump({
                'collection': coll_name,
                'count': len(coll_items),
                'items': coll_items
            }, f, indent=2, ensure_ascii=False)

    print(f"Output written to: {output_dir}")
    print(f"  - instagram_saved_clean.json")
    print(f"  - instagram_saved_clean.csv")
    print(f"  - instagram_saved_urls_by_collection.md")
    print(f"  - instagram_all_urls_flat.txt")
    print(f"  - by_collection/ ({len(coll_counts)} files)")

    return all_items, coll_counts, all_hashtags, all_owners

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 parse_saved_collections.py <input.json> <output_dir>")
        sys.exit(1)
    parse_saved_collections(sys.argv[1], sys.argv[2])