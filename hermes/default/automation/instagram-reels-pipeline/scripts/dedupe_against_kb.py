#!/usr/bin/env python3
"""
Deduplicate Instagram URLs against existing Obsidian Knowledge Base.

Usage:
    python3 dedupe_against_kb.py \
        --urls instagram_all_urls_flat.txt \
        --kb-root "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base" \
        --output-dir ./dedupe_output
"""

import re
import os
import argparse
from pathlib import Path


def extract_urls_from_kb(kb_root):
    """Find all instagram.com/reel/ URLs in KB markdown files."""
    urls = set()
    pattern = re.compile(r'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+')
    
    for root, dirs, files in os.walk(kb_root):
        for f in files:
            if f.endswith('.md') or f.endswith('.json'):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                        matches = pattern.findall(content)
                        for m in matches:
                            urls.add(m.rstrip('/'))
                except Exception:
                    pass
    return urls


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
    parser = argparse.ArgumentParser(description='Deduplicate URLs against KB')
    parser.add_argument('--urls', required=True, help='Flat URL list (one per line)')
    parser.add_argument('--kb-root', required=True, help='Obsidian KB root directory')
    parser.add_argument('--output-dir', default='./dedupe_output', help='Output directory')
    args = parser.parse_args()
    
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting URLs from KB: {args.kb_root}")
    kb_urls = extract_urls_from_kb(args.kb_root)
    print(f"  Found {len(kb_urls)} unique reel URLs in KB")
    
    print(f"Loading saved URLs from: {args.urls}")
    saved_urls = load_urls(args.urls)
    print(f"  Loaded {len(saved_urls)} unique URLs")
    
    # Overlap
    overlap = kb_urls & saved_urls
    new_only = saved_urls - kb_urls
    kb_only = kb_urls - saved_urls
    
    print(f"\nOverlap (already in KB): {len(overlap)}")
    print(f"New (not in KB): {len(new_only)}")
    print(f"KB-only (not in saved export): {len(kb_only)}")
    
    # Write outputs
    with open(out_dir / 'overlap.txt', 'w') as f:
        for url in sorted(overlap):
            f.write(url + '\n')
    
    with open(out_dir / 'new_only.txt', 'w') as f:
        for url in sorted(new_only):
            f.write(url + '\n')
    
    with open(out_dir / 'kb_only.txt', 'w') as f:
        for url in sorted(kb_only):
            f.write(url + '\n')
    
    print(f"\nOutputs written to {out_dir}/")
    print("  overlap.txt     - URLs already processed in KB")
    print("  new_only.txt    - Fresh URLs to process")
    print("  kb_only.txt     - URLs in KB but not in this export")


if __name__ == '__main__':
    main()