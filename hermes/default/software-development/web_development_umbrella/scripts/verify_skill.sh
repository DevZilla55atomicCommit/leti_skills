#!/bin/bash
# verification.sh - Verify Web Development Umbrella Skill
# Validates SKILL.md structure, presence of references, templates, scripts

set -e

# Check SKILL.md exists
if [ ! -f "$(dirname "$0")/../SKILL.md" ]; then
  echo "ERROR: SKILL.md not found"
  exit 1
fi

# Validate YAML frontmatter exists
if ! head -1 "$(dirname "$0")/../SKILL.md" | grep -q "^---$"; then
  echo "ERROR: Missing YAML frontmatter"
  exit 1
fi

# Check for references directory
if [ ! -d "$(dirname "$0")/../references" ]; then
  echo "ERROR: references directory missing"
  exit 1
fi

# Check for templates directory
if [ ! -d "$(dirname "$0")/../templates" ]; then
  echo "ERROR: templates directory missing"
  exit 1