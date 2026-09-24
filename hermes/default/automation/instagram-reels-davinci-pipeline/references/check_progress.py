#!/usr/bin/env python3
"""
Progress tracking script for Instagram Reels Vision Analysis.
"""

import json
from pathlib import Path

PROGRESS_FILE = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')

def main():
    with open(PROGRESS_FILE) as f:
        data = json.load(f)

    complete = sum(1 for v in data if v.get('status') == 'complete')
    pending = sum(1 for v in data if v.get('status') == 'pending')
    error = sum(1 for v in data if v.get('status') == 'error')
    total = len(data)

    print(f'Complete: {complete}, Pending: {pending}, Error: {error}')
    print(f'Total: {total}')
    print(f'Progress: {complete/total*100:.1f}%')

    # Show next 10 pending
    pending_videos = [v['video_id'] for v in data if v.get('status') == 'pending']
    print(f'\nNext 10 pending: {pending_videos[:10]}')

    # Session progress
    base_complete = 722  # Starting point
    session_processed = complete - base_complete
    print(f'Session: {session_processed}')

if __name__ == '__main__':
    main()