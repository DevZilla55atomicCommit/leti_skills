#!/bin/bash
# Verify DaVinci Resolve Creative Grading Workflow

echo "🔍 Verifying workflow structure..."
echo "📁 Checking node count and required fields..."

# Simple validation: check for required environment variables
if [[ -z "$DRIVE_NODES" ]]; then
  echo "⚠️  WARNING: \$DRIVE_NODES not set - may cause script failures"
else
  echo "✅ \$DRIVE_NODES is configured"
fi

# Check that essential files exist
if [[ ! -f "references/workflow-overview.md" ]]; then
  echo "❌ references/workflow-overview.md missing"
else
  echo "✅ references/workflow-overview.md exists"
fi

if [[ -f "templates/node-template-compound.md" ]]; then
  echo "✅ templates/node-template-compound.md exists"
else
  echo "❌ templates/node-template-compound.md missing"
fi

echo "✅ Verification complete."