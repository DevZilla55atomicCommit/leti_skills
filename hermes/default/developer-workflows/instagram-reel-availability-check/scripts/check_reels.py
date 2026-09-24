#!/usr/bin/env python3
"""
check_reels.py – Automated Instagram Reel Availability Checker

This script reads a list of Instagram reel short URLs (one per line)
from `urls.txt`, navigates to each URL using Hermes' browser tools,
and determines whether the reel is publicly accessible.

Features:
- Detects public reels by checking for a `Video` element and absence of
  login prompts (`Log In`, `Sign Up`) in the page snapshot.
- Generates a simple markdown report (`report.md`) with the status of each URL.
- Handles rate‑limiting concerns by optionally inserting a short pause.

Dependencies:
- Hermes `browser_navigate`, `browser_snapshot` (exposed via the
  `hermes_tools` import).
- Standard library: `time`, `os`.
"""

import os
import time
from hermes_tools import browser_navigate, browser_snapshot

def is_public_reel(url: str) -> bool:
    """Return True if the URL resolves to a publicly accessible reel."""
    # Navigate to the URL (implicitly loads the page)
    browser_navigate(url)
    # Small pause to let dynamic content settle (adjust as needed)
    time.sleep(1)
    # Grab a compact snapshot for analysis
    snapshot = browser_snapshot()
    # Heuristic: presence of 'Video' and no login indicators
    has_video = 'Video' in snapshot
    has_login = 'Log In' in snapshot or 'Sign Up' in snapshot
    return has_video and not has_login

def main():
    # Path to the file containing one URL per line
    urls_path = 'urls.txt'
    if not os.path.exists(urls_path):
        raise FileNotFoundError(f"{urls_path} not found. Create it with one URL per line.")
    
    with open(urls_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    results = []
    for url in urls:
        if is_public_reel(url):
            results.append(f"✅ {url} – Available")
        else:
            results.append(f"❌ {url} – Unavailable (login wall or private)")
        # Optional polite throttling
        time.sleep(0.5)
    
    # Write results to a markdown report
    report_content = '\n'.join(results)
    write_file('report.md', report_content)
    print('Report written to report.md')

if __name__ == '__main__':
    main()