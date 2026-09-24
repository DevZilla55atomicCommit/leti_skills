#!/usr/bin/env bash
# DaVinci Resolve MCP Server Connection Test Script
# Usage: ./scripts/test-davinci-resolve-mcp.sh

set -e

PYTHON="/opt/homebrew/opt/python@3.11/bin/python3.11"
SERVER="/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"

echo "Testing DaVinci Resolve MCP Server..."
echo "Python: $PYTHON"
echo "Server: $SERVER"
echo ""

# Test 1: Initialize and get tools list
echo "=== Test 1: Initialize & List Tools ==="
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}' | "$PYTHON" "$SERVER" 2>&1 | python3 -m json.tool | head -50

echo ""
echo "=== Test 2: Get Resolve Version ==="
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "resolve_control", "arguments": {"action": "get_version"}}}' | "$PYTHON" "$SERVER" 2>&1 | python3 -m json.tool

echo ""
echo "=== Test 3: Get Current Project ==="
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "project_manager", "arguments": {"action": "get_current"}}}' | "$PYTHON" "$SERVER" 2>&1 | python3 -m json.tool

echo ""
echo "=== Test 4: Get Project Summary ==="
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "project_settings", "arguments": {"action": "project_summary", "params": {"include_clips": true, "clip_limit": 10}}}}' | "$PYTHON" "$SERVER" 2>&1 | python3 -m json.tool

echo ""
echo "=== Test 5: Get Current Timeline ==="
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "timeline", "arguments": {"action": "get_current"}}}' | "$PYTHON" "$SERVER" 2>&1 | python3 -m json.tool

echo ""
echo "All tests completed!"