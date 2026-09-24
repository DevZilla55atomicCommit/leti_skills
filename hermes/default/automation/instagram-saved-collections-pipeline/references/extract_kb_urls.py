#!/usr/bin/env python3
"""
Extract all Instagram Reel URLs from DaVinci Knowledge Base (Obsidian vault).
Used for deduplication against saved collections.
"""
import os
import re

def extract_kb_urls(kb_root):
    kb_urls = set()
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
                            kb_urls.add(m.rstrip('/'))
                except Exception as e:
                    print(f"Error reading {fpath}: {e}")

    return kb_urls

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 extract_kb_urls.py <kb_root> <output_file>")
        sys.exit(1)

    kb_root = sys.argv[1]
    output_file = sys.argv[2]

    urls = extract_kb_urls(kb_root)

    with open(output_file, 'w') as f:
        for url in sorted(urls):
            f.write(url + '\n')

    print(f"Extracted {len(urls)} unique Instagram Reel URLs from Knowledge Base")
    print(f"Written to: {output_file}")