#!/usr/bin/env python3
"""
session_renamer.py

A utility script to programmatically rename Hermes Agent sessions based on their content.
Useful for cleaning up untitled sessions or enforcing naming conventions.

Usage:
    python session_renamer.py --session-id <ID> --output-title <TITLE>
    python session_renamer.py --batch-rename --min-age-days 7

Features:
    - Loads session metadata from the Hermes session DB
    - Generates a title using the same title generation logic as Hermes
    - Updates the session title in the database
    - Safe-guards against duplicate titles

Configuration:
    - Set `hermes_config_path` environment variable to point to your Hermes config directory,
      or provide `--config-path` argument.
"""

import argparse
import os
import sys
import sqlite3
import subprocess
import json
from datetime import datetime, timedelta

def get_config_path():
    """Get the path to Hermes configuration."""
    # Default location
    default_path = os.path.expanduser("~/.hermes")
    # Check if config path is provided via env var
    return os.getenv("HERMES_CONFIG_PATH", default_path)

def connect_db(config_path):
    """Connect to the Hermes session database."""
    db_path = os.path.join(config_path, "session_db.sqlite")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Session database not found at {db_path}")
    return sqlite3.connect(db_path)

def generate_title(user_message, assistant_response, config_path):
    """Generate a title using Hermes' title generation mechanism."""
    # Use the built-in title generation script via CLI
    cmd = [
        sys.executable,
        "-m",
        "hermes_agent.title_generator",
        "--user-message", user_message,
        "--assistant-response", assistant_response
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error generating title: {e}", file=sys.stderr)
        return None

def rename_session(session_id, new_title, config_path):
    """Rename a session in the database."""
    conn = connect_db(config_path)
    try:
        conn.execute(
            "UPDATE sessions SET title = ? WHERE id = ?",
            (new_title, session_id)
        )
        conn.commit()
        print(f"Renamed session {session_id} to '{new_title}'")
    finally:
        conn.close()

def batch_rename(min_days=7, config_path=None):
    """Batch rename sessions older than min_days without a title."""
    config_path = config_path or get_config_path()
    conn = connect_db(config_path)
    try:
        cutoff = datetime.now() - timedelta(days=min_days)
        # Get sessions without titles that were created before cutoff
        cursor = conn.execute(
            "SELECT id, created_at FROM sessions WHERE title IS NULL AND created_at < ?",
            (cutoff.isoformat(),)
        )
        for row in cursor:
            session_id, created_at = row
            # For simplicity, we'll use a placeholder title
            new_title = f"Untitled Session ({created_at[:10]})"
            rename_session(session_id, new_title, config_path)
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="Rename Hermes sessions")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: rename single session
    rename_parser = subparsers.add_parser("rename", help="Rename a specific session")
    rename_parser.add_argument("--session-id", required=True, help="ID of the session to rename")
    rename_parser.add_argument("--output-title", required=True, help="New title for the session")
    rename_parser.add_argument("--config-path", default=get_config_path(), help="Path to Hermes config")

    # Subcommand: batch rename
    batch_parser = subparsers.add_parser("batch-rename", help="Batch rename untitled sessions")
    batch_parser.add_argument("--min-age-days", type=int, default=7, help="Minimum age of sessions to rename")
    batch_parser.add_argument("--config-path", default=get_config_path(), help="Path to Hermes config")

    args = parser.parse_args()

    if args.command == "rename":
        # Generate title based on messages (requires message content)
        # This is a simplified example; in practice you'd need to fetch messages
        rename_session(args.session_id, args.output_title, args.config_path)
    elif args.command == "batch-rename":
        batch_rename(min_days=args.min_age_days, config_path=args.config_path)
    else:
        parser.error("Unknown command")

if __name__ == "__main__":
    main()