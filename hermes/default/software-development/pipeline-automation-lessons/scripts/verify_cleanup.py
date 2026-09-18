#!/usr/bin/env python3
"""
Verify cleanup of temp directories after pipeline batch processing.

Run after each batch to ensure temp directories don't accumulate.
"""

import os
import subprocess
from pathlib import Path

def verify_cleanup():
    """Verify temp directories are clean after batch processing."""
    
    temp_dir = Path("~/instagram-davinci-pipeline/temp").expanduser()
    
    # Check each subdirectory
    subdirs = ["frames", "gifs", "mp4", "transcripts"]
    
    print("=== Temp Directory Cleanup Verification ===\n")
    
    total_size = 0
    for subdir in subdirs:
        path = temp_dir / subdir
        if path.exists():
            # Count items
            count = len(os.listdir(path))
            # Get size
            result = subprocess.run(["du", "-sh", str(path)], capture_output=True, text=True)
            size_str = result.stdout.strip().split('\t')[0]
            total_size += result.stdout.strip()
            print(f"  {subdir:12s}: {count:4d} items  {size_str}")
        else:
            print(f"  {subdir:12s}: (missing)")
    
    # Check vault assets
    vault_dir = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/assets")
    if vault_dir.exists():
        print(f"\n  Vault assets:")
        for cat in ["transitions", "compositing", "motion-graphics", "stylization", "vfx", "text-effects", "time-effects"]:
            cat_path = vault_dir / cat
            if cat_path.exists():
                result = subprocess.run(["du", "-sh", str(cat_path)], capture_output=True, text=True)
                size_str = result.stdout.strip().split('\t')[0]
                print(f"    {cat:15s}: {size_str}")
    
    print("\n=== Safe to delete temp if: ===")
    print("  1. Vault asset counts match temp counts")
    print("  2. No active processing running")
    print("  3. Manifest has valid frames_dir paths")

if __name__ == "__main__":
    verify_cleanup()