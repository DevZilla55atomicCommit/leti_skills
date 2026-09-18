#!/usr/bin/env python3
"""Verify Claude Code subagent definitions resolve. No third-party deps.

Checks per agents/* file: frontmatter parses, `name` + `description` present,
name uses safe charset, every `skills:` entry resolves to an installed
<skills-dir>/<name>/SKILL.md (which itself must carry name+description),
and every `mcpServers:` entry matches `claude mcp list` (best-effort).
Exit nonzero on any error.

Usage:
  python3 scripts/verify-agents.py [--agents-dir D] [--skills-dir D] [--no-mcp]
"""

import argparse
import os
import re
import subprocess
import sys

TOP_KEY = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
LIST_ITEM = re.compile(r"^\s+-\s+(.+)$")
SAFE_NAME = re.compile(r"^[a-z0-9-]+$")


def parse_frontmatter(path):
    """Return (fields dict, error str|None). Narrow shape only."""
    try:
        text = open(path).read()
    except OSError as e:
        return {}, "unreadable: %s" % e
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing opening --- (no frontmatter)"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, "missing closing ---"
    fields, current = {}, None
    for line in lines[1:end]:
        m = TOP_KEY.match(line)
        if m and not line[0] in (" ", "\t"):
            current = m.group(1)
            fields.setdefault(current, m.group(2).strip())
        elif LIST_ITEM.match(line) and current:
            fields.setdefault(current + "[]", []).append(LIST_ITEM.match(line).group(1).strip())
    return fields, None


def skill_ok(skills_dir, entry):
    skill_md = os.path.join(skills_dir, entry, "SKILL.md")
    if not os.path.isfile(skill_md):
        return "MISSING dir or SKILL.md"
    fields, err = parse_frontmatter(skill_md)
    if err or not fields.get("name") or "description" not in fields:
        return "installed but invalid frontmatter"
    return None


def configured_mcp_servers():
    """Best-effort parse of `claude mcp list`. Returns None if unparseable."""
    try:
        out = subprocess.run(["claude", "mcp", "list"], capture_output=True,
                             text=True, timeout=60).stdout
    except Exception:
        return None
    names = set()
    for line in out.splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_-]+)\s*:", line)
        if m:
            names.add(m.group(1))
    return names or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents-dir", default=os.path.expanduser("~/.claude/agents"))
    ap.add_argument("--skills-dir", default=os.path.expanduser("~/.claude/skills"))
    ap.add_argument("--no-mcp", action="store_true")
    args = ap.parse_args()

    mcp = None if args.no_mcp else configured_mcp_servers()
    if not args.no_mcp and mcp is None:
        print("WARN: could not parse `claude mcp list`; skipping MCP checks")

    errors, checked = 0, 0
    for fname in sorted(os.listdir(args.agents_dir)):
        if not fname.endswith(".md"):
            continue
        checked += 1
        path = os.path.join(args.agents_dir, fname)
        fields, err = parse_frontmatter(path)
        problems = [err] if err else []
        if not err:
            if not fields.get("name"):
                problems.append("missing name (file will be skipped at load)")
            elif not SAFE_NAME.match(fields["name"]):
                print("WARN %s: name %r breaks kebab-case convention" % (fname, fields["name"]))
            if "description" not in fields:
                problems.append("missing description (file will be skipped at load)")
            for entry in fields.get("skills[]", []):
                bad = skill_ok(args.skills_dir, entry)
                if bad:
                    problems.append("skills:%s %s" % (entry, bad))
            if mcp is not None:
                for entry in fields.get("mcpServers[]", []):
                    if entry not in mcp:
                        problems.append("mcpServers:%s not in `claude mcp list`" % entry)
        if problems:
            errors += 1
            for p in problems:
                print("ERROR %s: %s" % (fname, p))
        else:
            print("OK %s" % fname)
    print("checked=%d errors=%d" % (checked, errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
