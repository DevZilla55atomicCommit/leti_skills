#!/bin/bash
# Instagram Reels Pipeline - Storage Cleanup Script
# Run when Samsung LED >85% full

set -euo pipefail

CONTENT_PROCESSING="/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING"
VISION_PROGRESS="$CONTENT_PROCESSING/VISION_PROGRESS.json"

echo "=== Instagram Reels Pipeline Storage Cleanup ==="
echo "Target: $CONTENT_PROCESSING"
echo ""

# Show current usage
echo "Current usage:"
du -sh "$CONTENT_PROCESSING"/gifs "$CONTENT_PROCESSING"/frames "$CONTENT_PROCESSING"/transcripts "$CONTENT_PROCESSING"/vault "$CONTENT_PROCESSING"/analysis 2>/dev/null | sort -hr
echo ""

# 1. Delete gifs/ (45 GB - regeneratable from frames)
if [ -d "$CONTENT_PROCESSING/gifs" ]; then
    echo "[1/4] Deleting gifs/ (regeneratable from frames)..."
    rm -rf "$CONTENT_PROCESSING/gifs"
    echo "  ✓ Done"
else
    echo "[1/4] gifs/ already gone"
fi

# 2. Delete frames for completed videos
if [ -d "$CONTENT_PROCESSING/frames" ] && [ -f "$VISION_PROGRESS" ]; then
    echo "[2/4] Deleting frames for completed videos..."
    # Get completed video IDs from VISION_PROGRESS.json
    COMPLETE_IDS=$(python3 -c "
import json
with open('$VISION_PROGRESS') as f:
    data = json.load(f)
complete = [v['video_id'] for v in data if v.get('status') == 'complete']
print(' '.join(complete))
")
    
    for vid in $COMPLETE_IDS; do
        if [ -d "$CONTENT_PROCESSING/frames/$vid" ]; then
            rm -rf "$CONTENT_PROCESSING/frames/$vid"
        fi
    done
    echo "  ✓ Removed frames for $(echo $COMPLETE_IDS | wc -w) completed videos"
else
    echo "[2/4] Skipped (no frames/ or no VISION_PROGRESS.json)"
fi

# 3. Clean transcripts for completed videos
if [ -d "$CONTENT_PROCESSING/transcripts" ] && [ -f "$VISION_PROGRESS" ]; then
    echo "[3/4] Deleting transcripts for completed videos..."
    COMPLETE_IDS=$(python3 -c "
import json
with open('$VISION_PROGRESS') as f:
    data = json.load(f)
complete = [v['video_id'] for v in data if v.get('status') == 'complete']
print(' '.join(complete))
")
    
    for vid in $COMPLETE_IDS; do
        if [ -d "$CONTENT_PROCESSING/transcripts/$vid" ]; then
            rm -rf "$CONTENT_PROCESSING/transcripts/$vid"
        fi
    done
    echo "  ✓ Done"
else
    echo "[3/4] Skipped"
fi

# 4. Show final usage
echo ""
echo "[4/4] Final usage:"
du -sh "$CONTENT_PROCESSING"/gifs "$CONTENT_PROCESSING"/frames "$CONTENT_PROCESSING"/transcripts "$CONTENT_PROCESSING"/vault "$CONTENT_PROCESSING"/analysis 2>/dev/null | sort -hr
echo ""
df -h "/Volumes/Samsung LED"
echo ""
echo "=== Cleanup complete ==="