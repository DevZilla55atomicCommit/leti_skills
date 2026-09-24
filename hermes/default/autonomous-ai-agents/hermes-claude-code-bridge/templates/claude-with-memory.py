#!/usr/bin/env python3
"""
Claude Code Memory Wrapper
Provides persistent memory across Claude Code invocations via <memory-update> blocks.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "memory"
USER_MEM = MEMORY_DIR / "user.json"
AGENT_MEM = MEMORY_DIR / "agent.json"
SYNC_SCRIPT = Path.home() / ".hermes" / "scripts" / "sync_step_beyond_memory.py"
CLAUDE_BIN = Path.home() / ".npm-global" / "bin" / "claude"


def load_memory(path: Path) -> list:
    """Load memory entries from JSON file."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        return data.get("entries", [])
    except (json.JSONDecodeError, OSError):
        return []


def save_memory(path: Path, entries: list) -> None:
    """Save memory entries to JSON file."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    data = {"entries": entries}
    path.write_text(json.dumps(data, indent=2))


def format_memory_context(user_entries: list, agent_entries: list) -> str:
    """Format memory entries for prompt injection."""
    lines = ["MEMORY:"]
    if user_entries:
        lines.append("User:")
        for e in user_entries[-15:]:  # Last 15 entries
            content = e.get("content", "") if isinstance(e, dict) else str(e)
            lines.append(f"  - {content}")
    else:
        lines.append("User: (none)")

    if agent_entries:
        lines.append("Agent:")
        for e in agent_entries[-15:]:
            content = e.get("content", "") if isinstance(e, dict) else str(e)
            lines.append(f"  - {content}")
    else:
        lines.append("Agent: (none)")

    lines.append("")
    lines.append("---")
    return "\n".join(lines)


def parse_memory_updates(response: str) -> dict:
    """Extract <memory-update> blocks from response."""
    pattern = r"<memory-update>\s*(\{.*?\})\s*</memory-update>"
    updates = {"user": [], "agent": []}

    for match in re.finditer(pattern, response, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            target = data.get("target", "").lower()
            entries = data.get("entries", [])
            if target in ("user", "agent") and entries:
                updates[target].extend(entries)
        except json.JSONDecodeError:
            continue

    return updates


def run_sync_script() -> None:
    """Run the Hermes sync script (non-blocking, fire-and-forget)."""
    if SYNC_SCRIPT.exists():
        try:
            subprocess.Popen(
                [sys.executable, str(SYNC_SCRIPT), "--push"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.SubprocessError):
            pass


def main():
    parser = argparse.ArgumentParser(description="Claude Code with persistent memory")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to Claude Code")
    parser.add_argument("--model", default="qwen3.5:4b", help="Model to use")
    parser.add_argument("--max-turns", type=int, default=10, help="Maximum turns")
    parser.add_argument("--claude-path", default=str(CLAUDE_BIN), help="Path to claude binary")
    parser.add_argument("--no-memory", action="store_true", help="Skip memory injection")
    args = parser.parse_args()

    # Read prompt from stdin if not provided
    if args.prompt is None:
        if sys.stdin.isatty():
            parser.error("Prompt required (or pipe via stdin)")
        args.prompt = sys.stdin.read().strip()

    # Load memory
    user_entries = load_memory(USER_MEM)
    agent_entries = load_memory(AGENT_MEM)

    # Build full prompt
    if args.no_memory or (not user_entries and not agent_entries):
        full_prompt = args.prompt
    else:
        memory_prefix = format_memory_context(user_entries, agent_entries)
        full_prompt = f"{memory_prefix}\nUSER: {args.prompt}"

    # Run Claude Code
    env = os.environ.copy()
    env["PATH"] = str(CLAUDE_BIN.parent) + ":" + env.get("PATH", "")

    cmd = [
        str(CLAUDE_BIN),
        "-p",
        full_prompt,
        "--model",
        args.model,
        "--max-turns",
        str(args.max_turns),
        "--dangerously-skip-permissions",
        "--output-format",
        "json",
        "--bare",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
    except subprocess.TimeoutExpired:
        print("Error: Claude Code timed out", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error running Claude Code: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse response
    try:
        response_data = json.loads(result.stdout.strip())
        response_text = response_data.get("result", "")
    except json.JSONDecodeError:
        response_text = result.stdout.strip()

    # Extract memory updates
    updates = parse_memory_updates(response_text)

    # Apply updates
    if updates["user"]:
        for entry in updates["user"]:
            entry.setdefault("source", "conversation")
            entry.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
            entry.setdefault("kind", "fact")
            entry.setdefault("scope", "persistent")
        user_entries.extend(updates["user"])
        save_memory(USER_MEM, user_entries)

    if updates["agent"]:
        for entry in updates["agent"]:
            entry.setdefault("source", "conversation")
            entry.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
            entry.setdefault("kind", "behavior")
            entry.setdefault("scope", "persistent")
        agent_entries.extend(updates["agent"])
        save_memory(AGENT_MEM, agent_entries)

    # Print the actual response (not JSON wrapper)
    if response_text:
        print(response_text)

    # Fire-and-forget sync
    run_sync_script()


if __name__ == "__main__":
    main()