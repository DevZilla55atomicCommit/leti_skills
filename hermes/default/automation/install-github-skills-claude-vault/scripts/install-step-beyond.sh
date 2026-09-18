#!/usr/bin/env bash
# Install step-beyond skills to Claude Code + Obsidian Vault
# Run this script manually in terminal

set -euo pipefail

SRC="$HOME/.claude/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"
VAULT_SKILLS="/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code"

echo "=== Creating target directories ==="
mkdir -p "$CLAUDE_SKILLS"
mkdir -p "$VAULT_SKILLS"

echo "=== Installing to Claude Code (~/.claude/skills/) ==="
cp "$SRC/step-beyond/SKILL.md" "$CLAUDE_SKILLS/step-beyond.md"
echo "✓ step-beyond.md ($(wc -c < "$CLAUDE_SKILLS/step-beyond.md") bytes)"

cp "$SRC/step-beyond-chatgpt/SKILL.md" "$CLAUDE_SKILLS/step-beyond-chatgpt.md"
echo "✓ step-beyond-chatgpt.md ($(wc -c < "$CLAUDE_SKILLS/step-beyond-chatgpt.md") bytes)"

echo "=== Installing to Obsidian Vault ==="
# step-beyond
rm -rf "$VAULT_SKILLS/step-beyond"
cp -r "$SRC/step-beyond" "$VAULT_SKILLS/step-beyond"
echo "✓ step-beyond/ ($(wc -c < "$VAULT_SKILLS/step-beyond/SKILL.md") bytes)"

# step-beyond-chatgpt
rm -rf "$VAULT_SKILLS/step-beyond-chatgpt"
cp -r "$SRC/step-beyond-chatgpt" "$VAULT_SKILLS/step-beyond-chatgpt"
echo "✓ step-beyond-chatgpt/ ($(wc -c < "$VAULT_SKILLS/step-beyond-chatgpt/SKILL.md") bytes)"

echo "=== Verification ==="
ls -la "$CLAUDE_SKILLS/step-beyond.md" "$CLAUDE_SKILLS/step-beyond-chatgpt.md"
ls -la "$VAULT_SKILLS/step-beyond/SKILL.md"
ls -la "$VAULT_SKILLS/step-beyond-chatgpt/SKILL.md"

echo "=== Test auto-invocation (run manually) ==="
echo "claude -p \"test the step-beyond skill\" --model qwen3.5:9b --bare --max-turns 3"