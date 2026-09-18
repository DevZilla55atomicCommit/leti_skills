#!/bin/bash
# generate_frames.sh - Wrapper script for bulk Flux frame generation

# Usage: ./generate_frames.sh --prompt "Your prompt here" --project "Your project name" --width WIDTH --height HEIGHT --steps STEPS

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --prompt)
      PROMPT="$2"
      shift
      ;;
    --project)
      PROJECT="$2"
      shift
      ;;
    --width)
      WIDTH="$2"
      shift
      ;;
    --height)
      HEIGHT="$2"
      shift
      ;;
    --steps)
      STEPS="$2"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
  shift
done

# Validate required parameters
if [ -z "$PROMPT" ] || [ -z "$PROJECT" ] || [ -z "$WIDTH" ] || [ -z "$HEIGHT" ] || [ -z "$STEPS" ]; then
  echo "Error: Missing required parameters."
  echo "Usage: $0 --prompt \"Your prompt\" --project \"project_name\" --width W --height H --steps N"
  exit 1
fi

# Call the generate_flux function from the flux_wrapper Python module
python3 -c "
import sys
sys.path.insert(0, '.')
from flux_wrapper import generate_flux
path = generate_flux(
    prompt='$PROMPT',
    project='$PROJECT',
    width=$WIDTH,
    height=$HEIGHT,
    steps=$STEPS
)
print(path)
"

# Check if the generation was successful
if [ $? -eq 0 ]; then
  echo "Generation successful: $path"
else
  echo "Generation failed."
  exit 1
fi