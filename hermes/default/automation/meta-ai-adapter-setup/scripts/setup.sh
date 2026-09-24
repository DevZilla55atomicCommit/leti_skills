#!/usr/bin/env bash
# Meta AI Adapter Setup Script
# Run this to set up Meta AI muse-spark-1.1 for Hermes on a new device

set -euo pipefail

SKILL_DIR="/Users/alfredkamisese/.hermes/skills/automation/meta-ai-adapter-setup"
ADAPTER_DIR="/Users/alfredkamisese/meta-adapter"

echo "=========================================="
echo "Meta AI Adapter Setup for Hermes"
echo "=========================================="
echo ""

# 1. Prompt for API key
read -rp "Enter your Meta AI API key (from https://dev.meta.ai): " META_API_KEY
if [[ -z "$META_API_KEY" ]]; then
    echo "Error: API key is required"
    exit 1
fi

echo ""
echo "Creating adapter directory: $ADAPTER_DIR"
mkdir -p "$ADAPTER_DIR"

# 2. Copy adapter files
echo "Copying adapter files..."
cp "$SKILL_DIR/references/meta_adapter.py" "$ADAPTER_DIR/meta_adapter.py"
cp "$SKILL_DIR/references/requirements.txt" "$ADAPTER_DIR/requirements.txt"

# 3. Create run_adapter.sh with the API key
echo "Creating launcher script..."
cat > "$ADAPTER_DIR/run_adapter.sh" << 'EOF'
#!/bin/bash
# Meta AI Adapter launcher for LaunchAgent

export META_API_KEY="META_API_KEY_PLACEHOLDER"
export PYTHONPATH="/Users/alfredkamisese/Library/Python/3.9/lib/python/site-packages"

exec /Library/Developer/CommandLineTools/usr/bin/python3 /Users/alfredkamisese/meta-adapter/meta_adapter.py
EOF

# Replace placeholder with actual API key
sed -i '' "s|META_API_KEY_PLACEHOLDER|$META_API_KEY|g" "$ADAPTER_DIR/run_adapter.sh"
chmod +x "$ADAPTER_DIR/run_adapter.sh"

# 4. Install Python dependencies
echo "Installing Python dependencies..."
/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --user -r "$ADAPTER_DIR/requirements.txt"

# 5. Configure Hermes provider
echo "Configuring Hermes provider..."
hermes config set providers.meta-ai.api "http://localhost:8000/v1"
hermes config set providers.meta-ai.default_model "muse-spark-1.1"
hermes config set providers.meta-ai.models.0 "muse-spark-1.1"
hermes config set providers.meta-ai.name "Meta AI"

# 6. Install launchd LaunchAgent
echo "Installing launchd service..."
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LAUNCH_AGENT_DIR"

cp "$SKILL_DIR/references/com.alfredkamisese.meta-ai-adapter.plist" "$LAUNCH_AGENT_DIR/com.alfredkamisese.meta-ai-adapter.plist"
launchctl load "$LAUNCH_AGENT_DIR/com.alfredkamisese.meta-ai-adapter.plist"

# 7. Verify
echo ""
echo "Waiting for adapter to start..."
sleep 3

echo "Testing health endpoint..."
if curl -sf http://localhost:8000/health | grep -q "ok"; then
    echo "✓ Adapter health check passed"
else
    echo "✗ Adapter health check failed - check logs: tail -f $ADAPTER_DIR/adapter.err.log"
    exit 1
fi

echo "Testing Hermes integration..."
if hermes chat -q "Test" --provider meta-ai 2>&1 | grep -q "Ack\|Hello\|Test"; then
    echo "✓ Hermes integration test passed"
else
    echo "✗ Hermes integration test failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  hermes chat -q \"Your prompt\" --provider meta-ai"
echo "  hermes model  # Select meta-ai / muse-spark-1.1 interactively"
echo ""
echo "Manage adapter:"
echo "  launchctl unload ~/Library/LaunchAgents/com.alfredkamisese.meta-ai-adapter.plist  # Stop"
echo "  launchctl load ~/Library/LaunchAgents/com.alfredkamisese.meta-ai-adapter.plist    # Start"
echo "  tail -f ~/meta-adapter/adapter.log                                                # Logs"