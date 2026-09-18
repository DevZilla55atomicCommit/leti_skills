# Cognee + NVIDIA NIM Config Reference

This file documents the configuration that connects Cognee to NVIDIA's NIM models using credentials stored in the Hermes environment. The credentials are loaded from the Hermes `.env` file dynamically at runtime.

## Environment Variables

| Variable | Source | Description |
|---------|--------|-------------|
| `LLM_PROVIDER` | `Hermes .env` | Set to `custom` to use NVIDIA NIM |
| `LLM_MODEL` | `Hermes .env` | NVIDIA model identifier e.g. `nvidia/nemotron-3-ultra-550b-a55b` |
| `LLM_ENDPOINT` | `Hermes .env` | API endpoint URL |
| `LLM_API_KEY` | `Hermes .env` | Read automatically via `${NVIDIA_API_KEY}` |
| `EMBEDDING_PROVIDER` | `Hermes .env` | Usually `ollama` |
| `EMBEDDING_MODEL` | `Hermes .env` | Typically `nomic-embed-text:latest` |
| `EMBEDDING_ENDPOINT` | `Hermes .env` | Usually `http://localhost:11434/api/embed` |

## How It Works

When the `cognee-nvidia-graph-memory` skill runs:

1. It reads the environment via standard mechanisms (`os.getenv()`) which pulls values from the active Hermes `.env`.
2. No explicit credential storage is needed; the key is injected by the Hermes runtime.
3. The configuration points to the NVIDIA model for graph extraction while keeping embeddings and storage local.

## Usage

```bash
# In your terminal session (the credentials are already loaded)
python -c "import cognee; cognee.remember('test context')"
```

## Reference

- **Cognee docs**: https://docs.cognee.ai/
- **NVIDIA NIM models**: https://integrate.api.nvidia.com
- **Cognee GitHub**: https://github.com/topoteretes/cognee