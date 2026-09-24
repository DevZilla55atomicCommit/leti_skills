#!/bin/bash
# locate-app-settings.sh - Find OpenAI Codex (ChatGPT) preferences, secure preferences, and account data

BASE_DIR="$HOME/Library/Application Support/Codex/Default"

echo "=== Codex Preferences ==="
if [[ -f "$BASE_DIR/Preferences" ]]; then
  echo "Preferences file located at: $BASE_DIR/Preferences"
  cat "$BASE_DIR/Preferences"
else
  echo "Preferences file not found."
fi

echo -e "\n=== Secure Preferences ==="
if [[ -f "$BASE_DIR/Secure Preferences" ]]; then
  echo "Secure Preferences file located at: $BASE_DIR/Secure Preferences"
  cat "$BASE_DIR/Secure Preferences"
else
  echo "Secure Preferences file not found."
fi

echo -e "\n=== Account Web Data ==="
if [[ -f "$BASE_DIR/Account Web Data" ]]; then
  echo "Account Web Data located at: $BASE_DIR/Account Web Data"
  cat "$BASE_DIR/Account Web Data"
else
  echo "Account Web Data not found."
fi