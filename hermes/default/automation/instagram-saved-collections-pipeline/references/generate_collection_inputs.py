#!/usr/bin/env python3
"""
Generate per-collection NEW-only URL .txt files for pipeline processing.
Reads the NEW_ONLY list and per-collection JSONs, outputs one .txt per collection.
"""
import os
import json

def generate_collection_inputs(new_only_file, collections_dir, output_dir):
    # Load new-only URLs
    new_urls = set()
    with open(new_only_file, 'r') as f:
        for line in f:
            new_urls.add(line.strip().rstrip('/'))

    os.makedirs(output_dir, exist_ok=True)

    for fname in sorted(os.listdir(collections_dir)):
        if fname.endswith('.json'):
            fpath = os.path.join(collections_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            coll_name = data.get('collection', fname.replace('.json', ''))
            items = data.get('items', [])

            coll_new_urls = []
            for item in items:
                url = item.get('url', '').rstrip('/')
                if url in new_urls:
                    coll_new_urls.append(url)

            if coll_new_urls:
                safe_name = coll_name.replace('/', '_').replace(' ', '_').replace(':', '_')
                out_path = os.path.join(output_dir, f'{safe_name}_NEW.txt')
                with open(out_path, 'w') as f:
                    for url in sorted(coll_new_urls):
                        f.write(url + '\n')
                print(f"  {coll_name}: {len(coll_new_urls)} new URLs -> {out_path}")

    # Also create a master new-only flat list (copy of new_only_file for convenience)
    master_path = os.path.join(output_dir, 'ALL_NEW_URLS.txt')
    with open(master_path, 'w') as f:
        for url in sorted(new_urls):
            f.write(url + '\n')
    print(f"\nMaster list: {master_path} ({len(new_urls)} URLs)")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print("Usage: python3 generate_collection_inputs.py <new_only.txt> <collections_dir> <output_dir>")
        sys.exit(1)
    generate_collection_inputs(sys.argv[1], sys.argv[2], sys.argv[3])