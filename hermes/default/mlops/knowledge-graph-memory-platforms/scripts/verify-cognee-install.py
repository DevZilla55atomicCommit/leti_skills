#!/usr/bin/env python3
"""
Cognee + Ollama Installation Verification Script

Run after installing cognee and configuring .env to verify:
1. Ollama endpoints are reachable
2. Session memory works (no LLM calls)
3. Graph memory works (full pipeline with LLM)
"""

import asyncio
import os
import sys
import subprocess
import json

# Load .env if present
def load_env():
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k] = v

load_env()

def check_ollama_model(model_name: str) -> bool:
    """Check if model exists in Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=10
        )
        return model_name in result.stdout
    except Exception:
        return False

def test_embeddings_endpoint() -> bool:
    """Test native Ollama embeddings endpoint."""
    try:
        import requests
        resp = requests.post(
            "http://localhost:11434/api/embed",
            json={"model": os.environ.get("EMBEDDING_MODEL", "nomic-embed-text:latest"), "input": "test"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            if "embedding" in data and len(data["embedding"]) == int(os.environ.get("EMBEDDING_DIMENSIONS", "768")):
                print(f"  ✅ Embeddings endpoint: {len(data['embedding'])} dims")
                return True
        print(f"  ❌ Embeddings endpoint failed: {resp.status_code} {resp.text[:100]}")
        return False
    except Exception as e:
        print(f"  ❌ Embeddings endpoint error: {e}")
        return False

async def test_session_memory() -> bool:
    """Test session memory (no LLM calls)."""
    try:
        import cognee
        os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"
        
        session_id = "verify-session"
        result = await cognee.remember("Verification fact: session memory works.", session_id=session_id)
        print(f"  ✅ Session remember: {result.status}")
        
        results = await cognee.recall("What works?", session_id=session_id)
        if results:
            print(f"  ✅ Session recall: {len(results)} results")
            return True
        print("  ❌ Session recall: no results")
        return False
    except Exception as e:
        print(f"  ❌ Session memory error: {e}")
        return False

async def test_graph_memory() -> bool:
    """Test graph memory (full pipeline with LLM)."""
    try:
        import cognee
        os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"
        
        result = await cognee.remember("Verification fact: graph memory works with qwen3.5:4b.")
        print(f"  ✅ Graph remember: {result.status}")
        
        results = await cognee.recall("What works?")
        if results:
            print(f"  ✅ Graph recall: {len(results)} results")
            for r in results[:2]:
                print(f"     - {r}")
            return True
        print("  ❌ Graph recall: no results")
        return False
    except Exception as e:
        print(f"  ❌ Graph memory error: {e}")
        return False

async def main():
    print("=" * 60)
    print("COGNEe + OLLAMA VERIFICATION")
    print("=" * 60)
    
    # Check required models
    print("\n1. Checking Ollama models...")
    chat_model = os.environ.get("LLM_MODEL", "qwen3.5:4b")
    embed_model = os.environ.get("EMBEDDING_MODEL", "nomic-embed-text:latest")
    
    for model in [chat_model, embed_model]:
        if check_ollama_model(model):
            print(f"  ✅ {model}")
        else:
            print(f"  ❌ {model} NOT FOUND — run: ollama pull {model}")
            return 1
    
    # Test embeddings endpoint
    print("\n2. Testing embeddings endpoint...")
    if not test_embeddings_endpoint():
        return 1
    
    # Test session memory
    print("\n3. Testing session memory (no LLM)...")
    if not await test_session_memory():
        return 1
    
    # Test graph memory
    print("\n4. Testing graph memory (full pipeline with LLM)...")
    print("    (This will call qwen3.5:4b for entity extraction — may take 30-60s)")
    if not await test_graph_memory():
        return 1
    
    print("\n" + "=" * 60)
    print("✅ ALL CHECKS PASSED — Cognee ready for use")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))