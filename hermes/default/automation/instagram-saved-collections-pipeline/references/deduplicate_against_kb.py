#!/usr/bin/env python3
"""
Deduplicate Instagram saved collection URLs against existing Knowledge Base.
Outputs: overlap, new-only, kb-only URL lists + per-collection breakdown.
"""
import os
import json

def load_urls(filepath):
    urls = set()
    with open(filepath, 'r') as f:
        for line in f:
            urls.add(line.strip().rstrip('/'))
    return urls

def deduplicate_against_kb(kb_urls_file, saved_urls_file, collections_dir, output_dir):
    kb_urls = load_urls(kb_urls_file)
    saved_urls = load_urls(saved_urls_file)

    overlap = kb_urls & saved_urls
    new_only = saved_urls - kb_urls
    kb_only = kb_urls - saved_urls

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, 'instagram_urls_OVERLAP.txt'), 'w') as f:
        for url in sorted(overlap):
            f.write(url + '\n')
    with open(os.path.join(output_dir, 'instagram_urls_NEW_ONLY.txt'), 'w') as f:
        for url in sorted(new_only):
            f.write(url + '\n')
    with open(os.path.join(output_dir, 'instagram_urls_KB_ONLY.txt'), 'w') as f:
        for url in sorted(kb_only):
            f.write(url + '\n')

    print(f"KB URLs: {len(kb_urls)}")
    print(f"Saved URLs: {len(saved_urls)}")
    print(f"Overlap: {len(overlap)}")
    print(f"New only: {len(new_only)}")
    print(f"KB only: {len(kb_only)}")

    # Per-collection breakdown
    print("\n=== OVERLAP BY COLLECTION ===")
    for fname in sorted(os.listdir(collections_dir)):
        if fname.endswith('.json'):
            fpath = os.path.join(collections_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            coll_name = data.get('collection', fname.replace('.json', ''))
            items = data.get('items', [])
            coll_urls = {item.get('url', '').rstrip('/') for item in items}
            coll_overlap = coll_urls & overlap
            coll_new = coll_urls & new_only
            if coll_overlap or coll_new:
                print(f"  {coll_name}: {len(coll_overlap)} done / {len(coll_new)} new / {len(items)} total")

    return overlap, new_only, kb_only

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 5:
        print("Usage: python3 deduplicate_against_kb.py <kb_urls.txt> <saved_urls.txt> <collections_dir> <output_dir>")
        sys.exit(1)
    deduplicate_against_kb(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])