#!/usr/bin/env python3
"""
Deterministic summarization script for Medi-Cal updates.
Reads references/latest-updates.md and outputs a concise bullet list.
"""

import markdown

# Read the updates file
with open('references/latest-updates.md', 'r') as f:
    content = f.read()

# Simple regex-based extraction of table rows
import re

rows = re.findall(r'\| *([^|]*) *\| *([^|]*) *\|', content)
header = re.search(r'^\| *([-=]) *\| *([-=]) *\|', content, re.MULTILINE)

if header:
    # Extract column headers
    headers = [h.strip() for h in header.group(0).strip('|').split('|')]
    print('## Recent Medi-Cal Updates\n')
    print('| ' + ' | '.join(headers) + ' |')
    print('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    
    # Print each row as a bullet
    for date, update in rows:
        print(f"- **{date}**: {update}")
else:
    print('Could not parse updates table.')