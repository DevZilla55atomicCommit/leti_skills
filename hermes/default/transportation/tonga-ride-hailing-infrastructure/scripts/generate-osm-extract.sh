#!/bin/bash
# generate-osm-extract.sh - Download latest Tongatapu OSM extract and prepare for OSRM/Valhalla

# Install dependencies (Ubuntu/Debian)
# sudo apt-get install -y wget unzip

# Download Geofabrik extract (adjust URL if newer version)
URL="https://download.geofabrik.de/australia-oceania/tonga-latest.osm.pbf"
OUTFILE="tonga-latest.osm.pbf"

# Get the extract
echo "Downloading Tongatapu OSM extract..."
wget -O "$OUTFILE" "$URL"

# Optional: extract to folder
mkdir -p tonga_osm
mv "$OUTFILE" tonga_osm/

echo "Download complete. OSM file: $OUTFILE"