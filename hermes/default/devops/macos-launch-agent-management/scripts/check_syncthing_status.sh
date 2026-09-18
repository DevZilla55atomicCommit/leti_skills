#!/usr/bin/env bash
# check_syncthing_status.sh
# Verifies that the Syncthing daemon is running and the web UI is reachable.
# Returns 0 if healthy, non-zero otherwise.

MAX_WAIT=30
ELAPSED=0
INTERVAL=2

while true; do
  # Check if the syncthing process is running
  if ! pgrep -f "Syncthing" > /dev/null; then
    echo "❌ Syncthing process not running"
    exit 1
  fi

  # Try to fetch the UI endpoint
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8384/)
  if [[ "$HTTP_STATUS" == "200" ]]; then
    echo "✅ Syncthing UI is reachable (HTTP 200)"
    exit 0
  fi

  # If we've exceeded the max wait time, fail
  if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    echo "❌ Syncthing UI not reachable after $MAX_WAIT seconds"
    exit 1
  fi

  echo "⏳ Waiting for Syncthing UI... ($ELAPSED/$MAX_WAIT seconds)"
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done