#!/usr/bin/env python3
"""
Step Beyond Memory Sync — Hermes ↔ Obsidian
Bidirectional sync for Step Beyond user-patterns.md format.
Usage:
  python3 sync_step_beyond_memory.py --pull   # Obsidian → Hermes (session start)
  python3 sync_step_beyond_memory.py --push   # Hermes → Obsidian (session end)
  python3 sync_step_beyond_memory.py --status # Show sync status
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

# Paths
OBSIDIAN_PATTERNS = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Hermes Memory/step-beyond-user-patterns.md")
HERMES_MEMORY_DIR = Path("/Users/alfredkamisese/.hermes/profiles/default/memories")
HERMES_USER_MEMORY = HERMES_MEMORY_DIR / "user.json"

def read_obsidian_patterns() -> dict:
    """Read the Obsidian patterns file with metadata."""
    if not OBSIDIAN_PATTERNS.exists():
        return {"content": "", "hash": None, "modified": None}
    content = OBSIDIAN_PATTERNS.read_text(encoding="utf-8")
    h = hashlib.sha256(content.encode()).hexdigest()
    modified = datetime.fromtimestamp(OBSIDIAN_PATTERNS.stat().st_mtime).isoformat()
    return {"content": content, "hash": h, "modified": modified}

def read_hermes_memory() -> dict:
    """Read Hermes user memory file."""
    if not HERMES_USER_MEMORY.exists():
        return {"entries": []}
    try:
        data = json.loads(HERMES_USER_MEMORY.read_text(encoding="utf-8"))
        # Normalize to {"entries": [...]} format
        if "user" in data and "entries" in data["user"]:
            return {"entries": data["user"]["entries"]}
        elif "entries" in data:
            return data
        else:
            return {"entries": []}
    except json.JSONDecodeError:
        return {"entries": []}

def extract_patterns_from_hermes(hermes_mem: dict) -> str:
    """Extract Step Beyond patterns from Hermes memory entries."""
    # Normalized format is always {"entries": [...]}
    entries = hermes_mem.get("entries", [])
    sb_entries = [
        e for e in entries
        if e.get("content", "").startswith("# Step Beyond") or e.get("scope") == "step-beyond-patterns"
    ]
    if not sb_entries:
        return ""
    # Return the most recent one
    return sb_entries[-1].get("content", "")

def update_hermes_from_obsidian() -> bool:
    """Pull Obsidian patterns → Hermes memory (update user profile). --pull"""
    current = read_obsidian_patterns()
    
    if not current["content"]:
        print("No patterns in Obsidian to sync")
        return False
    
    # Read existing Hermes user memory
    if HERMES_USER_MEMORY.exists():
        try:
            user_mem = json.loads(HERMES_USER_MEMORY.read_text())
        except json.JSONDecodeError:
            user_mem = {"entries": []}
    else:
        user_mem = {"entries": []}
    
    # Check if we already have this content (by hash)
    existing_hash = None
    for entry in user_mem.get("entries", []):
        if entry.get("content", "").startswith("# Step Beyond"):
            existing_hash = hashlib.sha256(entry["content"].encode()).hexdigest()
            break
    
    current_hash = current["hash"]
    
    if existing_hash == current_hash:
        print("Obsidian patterns already in sync with Hermes")
        return False
    
    # Remove old step-beyond entries
    user_mem["entries"] = [
        e for e in user_mem.get("entries", [])
        if not e.get("content", "").startswith("# Step Beyond")
    ]
    
    # Add new entry
    user_mem["entries"].append({
        "content": current["content"],
        "source": "obsidian-step-beyond-sync",
        "timestamp": datetime.now().isoformat(),
        "kind": "profile",
        "scope": "step-beyond-patterns"
    })
    
    HERMES_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    HERMES_USER_MEMORY.write_text(json.dumps(user_mem, indent=2))
    print(f"✓ Pulled Obsidian patterns to Hermes memory: {HERMES_USER_MEMORY}")
    return True

def update_obsidian_from_hermes() -> bool:
    """Push Hermes memory → Obsidian (replace step-beyond patterns). --push"""
    hermes_mem = read_hermes_memory()
    patterns_content = extract_patterns_from_hermes(hermes_mem)
    
    if not patterns_content:
        print("No step-beyond patterns in Hermes memory to sync")
        return False
    
    # Read current Obsidian file
    current = read_obsidian_patterns()
    
    # Check if content is already the same (by hash)
    current_hash = current["hash"]
    patterns_hash = hashlib.sha256(patterns_content.encode()).hexdigest()
    
    if current_hash == patterns_hash:
        print("Obsidian patterns already in sync with Hermes")
        return False
    
    # Replace Obsidian file content with Hermes patterns (source of truth)
    OBSIDIAN_PATTERNS.parent.mkdir(parents=True, exist_ok=True)
    OBSIDIAN_PATTERNS.write_text(patterns_content, encoding="utf-8")
    print(f"✓ Pushed Hermes patterns to Obsidian (replaced): {OBSIDIAN_PATTERNS}")
    return True

def show_status():
    """Show sync status."""
    obs = read_obsidian_patterns()
    hermes = read_hermes_memory()
    
    print("═══ Step Beyond Memory Sync Status ═══")
    print(f"\nObsidian file: {OBSIDIAN_PATTERNS}")
    print(f"  Exists: {OBSIDIAN_PATTERNS.exists()}")
    print(f"  Hash: {obs['hash'][:16]}..." if obs['hash'] else "  Hash: (empty)")
    print(f"  Modified: {obs['modified']}" if obs['modified'] else "  Modified: (never)")
    print(f"  Size: {len(obs['content'])} chars")
    
    print(f"\nHermes user memory: {HERMES_USER_MEMORY}")
    print(f"  Exists: {HERMES_USER_MEMORY.exists()}")
    user_entries = len(hermes.get("entries", []))
    print(f"  Entries: {user_entries}")
    
    # Check for step-beyond entries
    sb_entries = [
        e for e in hermes.get("entries", [])
        if e.get("content", "").startswith("# Step Beyond")
    ]
    print(f"  Step Beyond entries: {len(sb_entries)}")
    if sb_entries:
        print(f"  Last sync: {sb_entries[-1].get('timestamp', 'unknown')}")

def main():
    # Default to --push for cron job compatibility
    if len(sys.argv) < 2:
        cmd = "--push"
    else:
        cmd = sys.argv[1]
    
    if cmd == "--pull":
        update_hermes_from_obsidian()
    elif cmd == "--push":
        update_obsidian_from_hermes()
    elif cmd == "--status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()