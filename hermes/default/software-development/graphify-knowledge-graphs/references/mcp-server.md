---
title: "Graphify MCP Server Reference"
source: "Graphify repository (graphify/serve.py, README.md)"
version: "0.9.9"
---

# Graphify MCP Server Reference

## Overview

The MCP server exposes the knowledge graph as structured tools for AI assistants. Run locally (stdio) or as HTTP server for team sharing.

---

## Quick Start

### Local stdio (for your AI assistant)
```bash
python -m graphify.serve graphify-out/graph.json
```

### HTTP Server (team/shared)
```bash
# Basic
python -m graphify.serve graphify-out/graph.json --transport http --port 8080

# Production: bind all interfaces + API key
python -m graphify.serve graphify-out/graph.json \
  --transport http \
  --host 0.0.0.0 \
  --port 8080 \
  --api-key "$SECRET"

# Docker
docker build -t graphify .
docker run -p 8080:8080 -v "$(pwd)/graphify-out:/data" graphify \
  /data/graph.json --transport http --host 0.0.0.0 --api-key "$SECRET"
```

---

## MCP Tools Exposed

| Tool | Description |
|------|-------------|
| `query_graph` | Natural language query → scoped subgraph |
| `get_node` | Get full node details by ID |
| `get_neighbors` | Get connected nodes (1-hop) |
| `shortest_path` | Shortest path between two nodes |
| `list_prs` | List PRs with CI/review status |
| `get_pr_impact` | Graph impact analysis for a PR |
| `triage_prs` | AI ranking of review queue |

---

## Transport Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--transport` | `stdio` | `stdio` or `http` |
| `--host` | `127.0.0.1` | HTTP bind host (use `0.0.0.0` to expose) |
| `--port` | `8080` | HTTP bind port |
| `--api-key` | `$GRAPHIFY_API_KEY` | Bearer token for HTTP |
| `--path` | `/mcp` | HTTP mount path |
| `--json-response` | off | Plain JSON instead of SSE |
| `--stateless` | off | No per-session state (for load balancers) |
| `--session-timeout` | `3600` | Idle session reaping (0 = disable) |

---

## Client Configuration

### Hermes Agent (native MCP)
Add to `~/.hermes/config.yaml`:
```yaml
mcp:
  servers:
    graphify:
      command: "python"
      args: ["-m", "graphify.serve", "graphify-out/graph.json"]
      transport: "stdio"
```

### Kimi Code
```bash
kimi mcp add --transport stdio graphify -- python -m graphify.serve graphify-out/graph.json
```

### VS Code / Cursor (HTTP)
```json
{
  "mcp": {
    "servers": {
      "graphify": {
        "url": "http://localhost:8080/mcp",
        "headers": { "Authorization": "Bearer YOUR_API_KEY" }
      }
    }
  }
}
```

---

## HTTP API Details

### Authentication
- Header: `Authorization: Bearer <key>` OR `X-API-Key: <key>`
- Key from `--api-key` or `GRAPHIFY_API_KEY` env var

### Endpoints
- `POST /mcp` - MCP protocol (SSE by default)
- `POST /mcp` with `Accept: application/json` - JSON response mode

---

## WSL / Linux Note

Ubuntu ships `python3`, not `python`. Use venv:
```bash
python3 -m venv .venv
.venv/bin/pip install "graphifyy[mcp]"
.venv/bin/python -m graphify.serve graphify-out/graph.json
```

---

## Use Cases

### 1. Personal Assistant Access
```bash
# Terminal 1: start server
python -m graphify.serve graphify-out/graph.json

# Terminal 2: Hermes uses it via MCP config
# Ask: "What connects AuthModule to Database?"
# Assistant calls query_graph tool
```

### 2. Team Shared Graph
```bash
# Server machine
python -m graphify.serve graphify-out/graph.json \
  --transport http --host 0.0.0.0 --port 8080 --api-key "team-secret"

# Team members configure MCP client to http://server:8080/mcp
```

### 3. CI/CD Integration
```yaml
# .github/workflows/graph.yml
- name: Build graph
  run: /graphify . --no-viz

- name: Start MCP server
  run: |
    python -m graphify.serve graphify-out/graph.json \
      --transport http --host 0.0.0.0 --port 8080 \
      --api-key ${{ secrets.GRAPHIFY_API_KEY }} &
    
- name: Run AI code review
  run: |
    # AI assistant queries graph for PR impact
    python review.py --mcp http://localhost:8080/mcp
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: graphify` | Install with `[mcp]` extra: `uv tool install "graphifyy[mcp]"` |
| Port in use | Change `--port` or kill existing process |
| API key rejected | Check `Authorization: Bearer` header format |
| SSL/TLS needed | Run behind nginx/Caddy reverse proxy |
| Large graph memory | Use `--stateless` + `--json-response` for load balancing |

---

## Integration with graphify prs

The MCP server enables `graphify prs` commands:
- `graphify prs` - dashboard
- `graphify prs 42` - deep dive on PR #42
- `graphify prs --triage` - AI ranks review queue
- `graphify prs --conflicts` - PRs sharing communities (merge-order risk)

These work via the same MCP tools (`list_prs`, `get_pr_impact`, `triage_prs`).