#!/usr/bin/env python3
"""
Obsidian Vault Migration Verification Script
Run after migration to verify vault integrity and path updates.
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def check_rsync_diff(source: str, dest: str) -> tuple[int, list[str]]:
    """Run rsync dry-run and return (exit_code, files_to_transfer)."""
    cmd = [
        "rsync", "-avh", "--dry-run", "--delete",
        "--exclude=.DS_Store", "--exclude=*/.DS_Store",
        "--exclude=*/.syncthing.*.tmp", "--exclude=*.sync-conflict-*.md",
        "--exclude=graphify-out/", "--exclude=*/graphify-out/",
        "--exclude=*/venv/", "--exclude=*/__pycache__/",
        f"{source}/", f"{dest}/"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    files = [line for line in result.stdout.split('\n') if line and not line.startswith('sent')]
    return result.returncode, files

def check_old_paths(vault_path: str, old_path: str) -> list[str]:
    """Search for remaining old absolute paths in vault."""
    exclude_dirs = {'graphify-out', 'venv', '__pycache__', '.syncthing'}
    exclude_patterns = ['*.sync-conflict-*.md', '.DS_Store']
    
    cmd = [
        "grep", "-r", old_path, vault_path,
        "--include=*.md", "--include=*.json", "--include=*.csv",
        "--include=*.py", "--include=*.sh", "--include=*.html",
        "-l"
    ]
    
    # Add exclude-dir for each
    for d in exclude_dirs:
        cmd.extend(["--exclude-dir", d])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 1:  # No matches
        return []
    return result.stdout.strip().split('\n')

def check_lean_terminal(vault_path: str) -> bool:
    """Verify lean-terminal plugin cwd paths."""
    config_path = Path(vault_path) / ".obsidian" / "plugins" / "lean-terminal" / "data.json"
    if not config_path.exists():
        print("⚠️  lean-terminal config not found")
        return False
    
    with open(config_path) as f:
        data = json.load(f)
    
    for session in data.get('recentSessions', []):
        if session.get('cwd') != vault_path:
            print(f"❌ Bad cwd in lean-terminal: {session.get('cwd')}")
            return False
    
    print(f"✅ lean-terminal: {len(data.get('recentSessions', []))} sessions have correct cwd")
    return True

def check_step_beyond(vault_path: str) -> bool:
    """Test Step Beyond session scripts."""
    try:
        # Test session start
        result = subprocess.run([
            "bash", "-c", f'source "{vault_path}/Hermes Agent/session_start_step_beyond.sh"'
        ], capture_output=True, text=True, timeout=10)
        if "Patterns loaded into Hermes memory" not in result.stdout:
            print("❌ session_start_step_beyond.sh failed")
            return False
        
        # Test session end
        result = subprocess.run([
            "bash", "-c", f'source "{vault_path}/Hermes Agent/session_end_step_beyond.sh"'
        ], capture_output=True, text=True, timeout=10)
        if "Patterns saved to Obsidian vault" not in result.stdout:
            print("❌ session_end_step_beyond.sh failed")
            return False
        
        print("✅ Step Beyond scripts working")
        return True
    except Exception as e:
        print(f"❌ Step Beyond test error: {e}")
        return False

def check_pipeline_script(vault_path: str) -> bool:
    """Test Video Effects pipeline script loads."""
    script_path = Path(vault_path) / "Hermes Agent" / "DaVinci_Knowledge_Base" / "Video_Effects" / "scripts" / "process_batch.py"
    if not script_path.exists():
        print("⚠️  Pipeline script not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, str(script_path), "--help"], capture_output=True, text=True, timeout=10)
        if "Video Effects Pipeline Batch Processor" in result.stdout:
            print("✅ Pipeline script loads correctly")
            return True
        else:
            print("❌ Pipeline script failed to load")
            return False
    except Exception as e:
        print(f"❌ Pipeline script error: {e}")
        return False

def check_symlink(vault_path: str, symlink_path: str) -> bool:
    """Verify symlink points to vault."""
    try:
        target = os.readlink(symlink_path)
        if os.path.samefile(target, vault_path):
            print(f"✅ Symlink {symlink_path} -> {target}")
            return True
        else:
            print(f"❌ Symlink points to wrong location: {target}")
            return False
    except Exception as e:
        print(f"❌ Symlink check failed: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: verify-migration.py <source_vault> <dest_vault> [symlink_path]")
        print("  source_vault: Original vault path (for comparison)")
        print("  dest_vault:   New vault path (to verify)")
        print("  symlink_path: Optional symlink to verify (default: ~/TamaZila_Obsidian_Vault)")
        sys.exit(1)
    
    source = sys.argv[1]
    dest = sys.argv[2]
    symlink = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/TamaZila_Obsidian_Vault")
    
    old_path = source
    new_path = dest
    
    print(f"=== Vault Migration Verification ===")
    print(f"Source: {source}")
    print(f"Dest:   {dest}")
    print(f"Symlink: {symlink}")
    print()
    
    all_passed = True
    
    # 1. Size and file count
    print("1. Size & File Count:")
    src_size = subprocess.run(["du", "-sh", source], capture_output=True, text=True).stdout.split()[0]
    dst_size = subprocess.run(["du", "-sh", dest], capture_output=True, text=True).stdout.split()[0]
    src_files = subprocess.run(["find", source, "-type", "f"], capture_output=True, text=True).stdout.strip().split('\n')
    dst_files = subprocess.run(["find", dest, "-type", "f"], capture_output=True, text=True).stdout.strip().split('\n')
    print(f"   Source: {src_size}, {len(src_files)} files")
    print(f"   Dest:   {dst_size}, {len(dst_files)} files")
    if src_size == dst_size and len(src_files) == len(dst_files):
        print("   ✅ Size and count match")
    else:
        print("   ❌ MISMATCH")
        all_passed = False
    print()
    
    # 2. Rsync diff
    print("2. Rsync Diff (excludes caches, .DS_Store, conflicts):")
    code, files = check_rsync_diff(source, dest)
    if code == 0 and len(files) == 0:
        print("   ✅ No differences (excluding expected)")
    else:
        print(f"   ⚠️  {len(files)} files would be transferred")
        for f in files[:5]:
            print(f"      {f}")
        if len(files) > 5:
            print(f"      ... and {len(files) - 5} more")
    print()
    
    # 3. Old paths check
    print("3. Old Path References:")
    old_files = check_old_paths(dest, old_path)
    if len(old_files) == 0:
        print("   ✅ No old paths found")
    else:
        print(f"   ❌ {len(old_files)} files still contain old path:")
        for f in old_files[:10]:
            print(f"      {f}")
        if len(old_files) > 10:
            print(f"      ... and {len(old_files) - 10} more")
        all_passed = False
    print()
    
    # 4. Lean-terminal config
    print("4. Lean-terminal Plugin:")
    if not check_lean_terminal(dest):
        all_passed = False
    print()
    
    # 5. Step Beyond scripts
    print("5. Step Beyond Scripts:")
    if not check_step_beyond(dest):
        all_passed = False
    print()
    
    # 6. Pipeline script
    print("6. Pipeline Script:")
    if not check_pipeline_script(dest):
        all_passed = False
    print()
    
    # 7. Symlink
    print("7. Backward-Compatibility Symlink:")
    if not check_symlink(dest, symlink):
        all_passed = False
    print()
    
    # Summary
    print("=" * 40)
    if all_passed:
        print("✅ ALL CHECKS PASSED — Migration verified")
        sys.exit(0)
    else:
        print("❌ SOME CHECKS FAILED — Review above")
        sys.exit(1)

if __name__ == "__main__":
    main()