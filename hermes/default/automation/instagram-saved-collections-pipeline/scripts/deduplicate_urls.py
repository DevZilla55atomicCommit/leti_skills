#!/usr/bin/env python3
"""
Deduplicate Instagram Saved Collection URLs against Knowledge Base URLs.
Generates overlap, new-only, and KB-only URL lists + per-collection breakdown.
"""
import json
import os
from collections import defaultdict

def load_urls(filepath):
    with open(filepath, 'r') as f:
        return {line.strip().rstrip('/') for line in f if line.strip()}

def load_collections(collection_dir):
    collections = {}
    for fname in os.listdir(collection_dir):
        if fname.endswith('.json'):
            fpath = os.path.join(collection_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                coll_name = data.get('collection', fname.replace('.json', ''))
                items = data.get('items', [])
                urls = {item.get('url', '').rstrip('/') for item in items if item.get('url')}
                collections[coll_name] = urls
    return collections

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Deduplicate Instagram URLs against KB')
    parser.add_argument('--saved-urls', required=True, help='Flat URL list from saved collections')
    parser.add_argument('--kb-urls', required=True, help='URL list extracted from Knowledge Base')
    parser.add_argument('--collections', required=True, help='Directory with per-collection JSON files')
    parser.add_argument('--output-dir', required=True, help='Output directory for results')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load URLs
    saved_urls = load_urls(args.saved_urls)
    kb_urls = load_urls(args.kb_urls)
    collections = load_collections(args.collections)

    print(f"Saved URLs: {len(saved_urls)}")
    print(f"KB URLs: {len(kb_urls)}")
    print(f"Collections: {len(collections)}")

    # Compute sets
    overlap = saved_urls & kb_urls
    new_only = saved_urls - kb_urls
    kb_only = kb_urls - saved_urls

    print(f"Overlap: {len(overlap)}")
    print(f"New only: {len(new_only)}")
    print(f"KB only: {len(kb_only)}")

    # Write master lists
    for name, url_set in [('OVERLAP', overlap), ('NEW_ONLY', new_only), ('KB_ONLY', kb_only)]:
        out_path = os.path.join(args.output_dir, f'instagram_urls_{name}.txt')
        with open(out_path, 'w') as f:
            for url in sorted(url_set):
                f.write(url + '\n')
        print(f"Written: {out_path} ({len(url_set)} URLs)")

    # Per-collection breakdown
    breakdown = {}
    for coll_name, coll_urls in collections.items():
        coll_overlap = coll_urls & overlap
        coll_new = coll_urls & new_only
        breakdown[coll_name] = {
            'total': len(coll_urls),
            'overlap': len(coll_overlap),
            'new': len(coll_new),
            'overlap_urls': sorted(coll_overlap),
            'new_urls': sorted(coll_new)
        }

    breakdown_path = os.path.join(args.output_dir, 'OVERLAP_BY_COLLECTION.json')
    with open(breakdown_path, 'w') as f:
        json.dump(breakdown, f, indent=2)
    print(f"Written: {breakdown_path}")

    # Print summary table
    print("\n=== PER-COLLECTION BREAKDOWN ===")
    print(f"{'Collection':<45} {'Total':>6} {'Done':>6} {'New':>6} {'% Done':>7}")
    print("-" * 75)
    for coll_name in sorted(breakdown.keys(), key=lambda k: -breakdown[k]['total']):
        b = breakdown[coll_name]
        pct = (b['overlap'] / b['total'] * 100) if b['total'] > 0 else 0
        print(f"{coll_name:<45} {b['total']:>6} {b['overlap']:>6} {b['new']:>6} {pct:>6.1f}%")

if __name__ == '__main__':
    main()