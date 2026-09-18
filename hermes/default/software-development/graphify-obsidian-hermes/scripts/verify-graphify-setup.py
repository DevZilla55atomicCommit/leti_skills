#!/usr/bin/env python3
"""
Graphify + Hermes + Obsidian Setup Verification Script

Run this after setup to verify everything works:
    python verify-graphify-setup.py

Or from project root:
    python -m scripts.verify_graphify_setup
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


def run_cmd(cmd: list[str], cwd: Optional[Path] = None) -> tuple[int, str, str]:
    """Run command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=60
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"


def check_graphify_installed() -> bool:
    """Verify graphify CLI is available."""
    code, stdout, stderr = run_cmd(["graphify", "--version"])
    if code == 0:
        print(f"  ✅ graphify CLI: {stdout}")
        return True
    print(f"  ❌ graphify CLI not found: {stderr}")
    return False


def check_hermes_skill(project_root: Path) -> bool:
    """Verify Hermes skill is installed (project or global)."""
    project_skill = project_root / ".hermes" / "skills" / "graphify" / "SKILL.md"
    global_skill = Path.home() / ".hermes" / "skills" / "graphify" / "SKILL.md"
    
    if project_skill.exists():
        print(f"  ✅ Project Hermes skill: {project_skill}")
        return True
    elif global_skill.exists():
        print(f"  ✅ Global Hermes skill: {global_skill}")
        return True
    else:
        print("  ❌ Hermes skill not found (run: graphify hermes install [--project])")
        return False


def check_agents_md(project_root: Path) -> bool:
    """Verify AGENTS.md exists with graphify rules."""
    agents_md = project_root / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text()
        if "graphify" in content.lower():
            print(f"  ✅ AGENTS.md with graphify rules: {agents_md}")
            return True
        print(f"  ⚠️  AGENTS.md exists but missing graphify rules: {agents_md}")
        return False
    print("  ❌ AGENTS.md not found (run: graphify hermes install [--project])")
    return False


def check_graph_built(project_root: Path) -> bool:
    """Verify knowledge graph was built."""
    graph_json = project_root / "graphify-out" / "graph.json"
    if graph_json.exists():
        try:
            data = json.loads(graph_json.read_text())
            nodes = len(data.get("nodes", []))
            edges = len(data.get("links", []))
            print(f"  ✅ Graph built: {nodes} nodes, {edges} edges at {graph_json}")
            return True
        except Exception as e:
            print(f"  ⚠️  Graph exists but invalid JSON: {e}")
            return False
    print("  ❌ Graph not built (run: graphify .)")
    return False


def check_obsidian_export(vault_path: Path) -> bool:
    """Verify Obsidian vault export exists with expected structure."""
    if not vault_path.exists():
        print(f"  ❌ Vault path not found: {vault_path}")
        return False
    
    checks = [
        (vault_path / ".graphify_obsidian_manifest.json", "Manifest"),
        (vault_path / ".obsidian" / "graph.json", "Graph view colors"),
        (vault_path / "graph.canvas", "Canvas file"),
    ]
    
    all_pass = True
    for path, name in checks:
        if path.exists():
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ❌ {name} missing: {path}")
            all_pass = False
    
    # Count node notes
    md_files = list(vault_path.glob("*.md"))
    community_files = list(vault_path.glob("_COMMUNITY_*.md"))
    node_files = [f for f in md_files if not f.name.startswith("_COMMUNITY_")]
    
    print(f"  📊 Vault stats: {len(node_files)} node notes, {len(community_files)} community notes")
    
    return all_pass


def check_git_hooks(project_root: Path) -> bool:
    """Verify git hooks installed."""
    hooks_dir = project_root / ".git" / "hooks"
    if not hooks_dir.exists():
        print("  ⚠️  Not a git repository")
        return False
    
    post_commit = hooks_dir / "post-commit"
    post_checkout = hooks_dir / "post-checkout"
    
    if post_commit.exists() and "graphify" in post_commit.read_text():
        print("  ✅ post-commit hook installed")
    else:
        print("  ❌ post-commit hook missing (run: graphify hook install)")
        return False
    
    if post_checkout.exists() and "graphify" in post_checkout.read_text():
        print("  ✅ post-checkout hook installed")
    else:
        print("  ❌ post-checkout hook missing (run: graphify hook install)")
        return False
    
    return True


def test_query(project_root: Path) -> bool:
    """Test graphify query command."""
    code, stdout, stderr = run_cmd(
        ["graphify", "query", "test query"], cwd=project_root
    )
    if code == 0:
        print(f"  ✅ Query works (returned {len(stdout.split(chr(10)))} lines)")
        return True
    print(f"  ❌ Query failed: {stderr}")
    return False


def main():
    project_root = Path.cwd()
    
    # Try to find vault path from common locations
    vault_base = Path("/Users/alfredkamisese/TamaZila Obsidian Vault")
    vault_path = None
    if vault_base.exists():
        # Find most recent Graphify-* subfolder
        graphify_vaults = sorted(vault_base.glob("Graphify-*"), key=lambda p: p.stat().st_mtime, reverse=True)
        if graphify_vaults:
            vault_path = graphify_vaults[0]
    
    print(f"\n=== Graphify Setup Verification ===")
    print(f"Project: {project_root}")
    print(f"Vault:   {vault_path or 'Not found'}")
    print("")
    
    checks = [
        ("Graphify CLI", check_graphify_installed),
        ("Hermes Skill", lambda: check_hermes_skill(project_root)),
        ("AGENTS.md", lambda: check_agents_md(project_root)),
        ("Knowledge Graph", lambda: check_graph_built(project_root)),
    ]
    
    if vault_path:
        checks.append(("Obsidian Export", lambda: check_obsidian_export(vault_path)))
    
    checks.extend([
        ("Git Hooks", lambda: check_git_hooks(project_root)),
        ("Query Command", lambda: test_query(project_root)),
    ])
    
    results = []
    for name, check_fn in checks:
        print(f"Checking {name}...")
        results.append((name, check_fn()))
        print()
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    print(f"=== Summary: {passed}/{total} checks passed ===")
    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")
    
    if passed == total:
        print("\n🎉 All checks passed! Graphify is ready to use.")
        print("   In Hermes: /graphify query \"your question\"")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. See above for fixes.")
        return 1


if __name__ == "__main__":
    sys.exit(main())