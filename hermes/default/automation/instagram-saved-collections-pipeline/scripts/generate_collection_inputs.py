#!/usr/bin/env python3
"""
Generate per-collection NEW-only URL files for pipeline processing.
Reads the deduplication breakdown and creates one .txt file per collection.
"""
import json
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate per-collection NEW URL files')
    parser.add_argument('--breakdown', required=True, help='OVERLAP_BY_COLLECTION.json from deduplicate_urls.py')
    parser.add_argument('--output-dir', required=True, help='Output directory for collection NEW.txt files')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.breakdown, 'r') as f:
        breakdown = json.load(f)

    total_new = 0
    for coll_name, data in breakdown.items():
        new_urls = data.get('new_urls', [])
        if new_urls:
            # Sanitize collection name for filename
            safe_name = coll_name.replace('/', '_').replace(' ', '_').replace(':', '_')
            out_path = os.path.join(args.output_dir, f'{safe_name}_NEW.txt')
            with open(out_path, 'w') as f:
                for url in new_urls:
                    f.write(url + '\n')
            print(f"  {coll_name}: {len(new_urls)} new URLs -> {out_path}")
            total_new += len(new_urls)
        else:
            print(f"  {coll_name}: 0 new URLs (skipped)")

    print(f"\nTotal new URLs across all collections: {total_new}")
    print(f"Files created in: {args.output_dir}")

if __name__ == '__main__':
    main()