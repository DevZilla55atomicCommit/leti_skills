#!/bin/bash
# Re-downloads the 8 manifest images from Unsplash CDN. Re-runnable.
# Usage: bash scripts/fetch-images.sh
set -euo pipefail
DIR="$(cd "$(dirname "$0")/../public/images" && pwd)"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
dl() { curl -sL -A "$UA" --max-time 90 "$1" -o "$DIR/$2"; echo "$2: $(du -h "$DIR/$2" | cut -f1)"; }
dl "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=1920&auto=format&fit=crop" "hero-grill-skewers.jpg"
dl "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1920&auto=format&fit=crop" "menu-bbq-ribs.jpg"
dl "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?q=80&w=1600&auto=format&fit=crop" "menu-grill-fire.jpg"
dl "https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=1600&auto=format&fit=crop" "menu-plate-lunch.jpg"
dl "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1600&auto=format&fit=crop" "menu-poke-bowl.jpg"
dl "https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=1920&auto=format&fit=crop" "interior-warm-dining.jpg"
dl "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?q=80&w=1920&auto=format&fit=crop" "interior-evening.jpg"
dl "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?q=80&w=1600&auto=format&fit=crop" "family-table.jpg"
echo "done — run npm run verify:assets to confirm."
