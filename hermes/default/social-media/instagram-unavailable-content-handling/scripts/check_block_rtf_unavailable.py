#!/usr/bin/env python3
"""
check_block_rtf_unavailable.py
Usage: check_block_rtf_unavailable.py <rtf_path> <reel_id>
Check if a reel ID appears in a Block *.rtf file and report availability.
"""

import sys
from hermes_tools import read_file

def check_reel_id_in_rtf(rtf_path: str, reel_id: str) -> bool:
    try:
        # Read file content (supports .rtf, .md, .txt)
        result = read_file(path=rtf_path, limit=5000)
        content = result.get("content", "")
        return reel_id in content
    except Exception as e:
        print(f"Error reading {rtf_path}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: check_block_rtf_unavailable.py <rtf_path> <reel_id>")
    rtf_path, reel_id = sys.argv[1], sys.argv[2]
    if check_reel_id_in_rtf(rtf_path, reel_id):
        print(f"✅ {reel_id} found in {rtf_path}")
        sys.exit(0)
    else:
        print(f"❌ {reel_id} NOT found in {rtf_path}")
        sys.exit(1)