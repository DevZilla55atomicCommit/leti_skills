# Repo Assessment: cognee (topoteretes/cognee)

**Upstream:** `topoteretes/cognee` (DevZilla55 fork is stale — use upstream)
**License:** Apache-2.0
**Language:** Python 3.10–3.14

---

## Verdict: **GO** — Add as MCP server + Hermes skill wrapper

---

## What It Is

Open-source AI memory platform: knowledge graphs (Kuzu/Neo4j/Postgres) + vector embeddings (LanceDB/pgvector/Qdrant) + session cache (SQLite/Postgres). Core API: `remember()`, `recall()`, `forget()`, `improve()`, `serve()`. Self-hosted or cloud. Active (v1.3.0, 4 days ago, 8,652 commits).

---

## Integration Path

| Your Layer | How | Effort |
|------------|-----|--------|
| Hermes Skill | `import cognee; await cognee.remember(...)` | **L** |
| MCP Server | `docker run -e TRANSPORT_MODE=sse cognee/cognee-mcp:main` | **L** |
| Cron/Background | `cognee-cli remember "fact"` | **L** |
| Claude Code | `claude plugin install cognee-memory@cognee` | **L** |
| Obsidian | `cognee.remember(vault_path)` → graph search | **M** |

---

## Costs

| Factor | Estimate |
|--------|----------|
| Install size | ~200 MB / deps: openai, instructor, lancedb, rdflib, fastapi, sqlalchemy, neo4j, playwright... |
| LLM tokens | ~$0.01–0.10 per document (cognify = entity extraction + summarization per chunk) |
| First-run migration | **Y** — `run_migrations_and_block()` on first `cognee` import |
| Ongoing maintenance | Low — stable API, active team |

---

## Risks

- **Heavy deps** — ~50 packages; conflicts possible in constrained envs
- **Token cost at scale** — `cognify()` calls LLM per chunk; budget for large vaults
- **Migration churn** — Alembic runs on first import; read `cognee/migrations/` before prod
- **Agent scoping** — MCP defaults to per-client dataset (`cursor_vscode_memory`); set `COGNEE_MCP_AGENT_SCOPED=false` for shared

---

## Evidence

| Check | Result |
|-------|--------|
| Upstream resolved | **Y** — DevZilla55 is stale fork; use `topoteretes/cognee` |
| `pyproject.toml` read | **Y** — optional deps: postgres, neo4j, ollama, anthropic, tracing... |
| Core module inspected | **Y** — `cognee/api/v1/remember/remember.py`, `recall.py`, `cognify.py` |
| MCP/CLI entrypoint found | **Y** — `cognee-mcp/src/server.py`, `cognee/cli/_cognee.py` |
| Minimal test run | **N** — would need `LLM_API_KEY` |
| Issue search | Migration lock contention, Neo4j connection pooling, Ollama model naming |

---

## Recommendation

1. **Add MCP server** to Hermes config (`cognee-mcp` via Docker, SSE transport)
2. **Write thin Hermes skill** wrapping Python SDK for `remember/recall` in skills
3. **Test with DaVinci vault subset** — `await cognee.remember(vault_path)` → `recall("Kodak 2383 workflow")`
4. **If token cost acceptable**, expand to full vault + Forex notes

---

## Notes

- **Local default**: SQLite + Kuzu + LanceDB — zero services needed
- **Postgres recommended** for prod: `pip install "cognee[postgres]"` + `DB_PROVIDER=postgres VECTOR_DB_PROVIDER=pgvector GRAPH_DATABASE_PROVIDER=postgres`
- **MCP env vars**: `TRANSPORT_MODE=http|sse|stdio`, `LLM_API_KEY`, `COGNEE_MCP_AGENT_SCOPED=false`
- **Cloud mode**: `cognee.serve("https://host", api_key)` — all calls route remote
- **Claude Code plugin** captures session → syncs to graph on `SessionEnd`