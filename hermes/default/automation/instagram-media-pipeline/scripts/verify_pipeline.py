#!/usr/bin/env python3
"""
Verification script for Instagram Media Pipeline components.
Run this to validate all dependencies and basic functionality.
"""

import subprocess
import sys
import asyncio
from pathlib import Path


def run_cmd(cmd: list[str], capture=True) -> tuple[int, str, str]:
    """Run command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True, timeout=30)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"


def check_yt_dlp() -> bool:
    """Check yt-dlp version and Instagram extractor."""
    code, out, err = run_cmd(["yt-dlp", "--version"])
    if code != 0:
        print("❌ yt-dlp not installed")
        return False
    
    print(f"✅ yt-dlp version: {out}")
    
    # Check if nightly (has Instagram fixes)
    code, out, err = run_cmd(["yt-dlp", "--extractor-descriptions", "instagram"])
    if "Instagram" in out:
        print("✅ Instagram extractor available")
        return True
    else:
        print("⚠️ Instagram extractor may be missing")
        return False


def check_ffmpeg() -> bool:
    """Check ffmpeg availability."""
    code, out, err = run_cmd(["ffmpeg", "-version"])
    if code != 0:
        print("❌ ffmpeg not installed")
        return False
    
    version_line = out.split('\n')[0]
    print(f"✅ {version_line}")
    return True


def check_playwright() -> bool:
    """Check Playwright Python availability."""
    try:
        import playwright
        print(f"✅ playwright-python: {playwright.__version__}")
        
        # Check if Chromium is installed
        code, out, err = run_cmd(["playwright", "install", "--dry-run", "chromium"])
        if "would be installed" in out or "already installed" in out:
            print("✅ Chromium available")
            return True
        else:
            print("⚠️ Chromium may need installation: playwright install chromium")
            return True
    except ImportError:
        print("❌ playwright-python not installed")
        return False


def check_instaloader() -> bool:
    """Check Instaloader availability."""
    code, out, err = run_cmd(["instaloader", "--version"])
    if code != 0:
        print("❌ instaloader not installed")
        return False
    print(f"✅ instaloader: {out}")
    return True


def check_cookies_file(path: str) -> bool:
    """Validate cookies.txt format."""
    p = Path(path)
    if not p.exists():
        print(f"❌ Cookies file not found: {path}")
        return False
    
    content = p.read_text()
    required = ['sessionid', 'ds_user_id', 'csrftoken']
    missing = [c for c in required if c not in content]
    
    if missing:
        print(f"⚠️ Cookies file missing fields: {missing}")
        return False
    
    print(f"✅ Cookies file valid: {path}")
    return True


async def test_yt_dlp_reel(url: str, cookies: str = None) -> bool:
    """Test yt-dlp on a single reel."""
    cmd = ["yt-dlp", "--skip-download", "--print-json", url]
    if cookies:
        cmd.insert(1, "--cookies")
        cmd.insert(2, cookies)
    
    print(f"Testing yt-dlp on: {url}")
    code, out, err = run_cmd(cmd)
    
    if code == 0:
        print("✅ yt-dlp extraction successful")
        import json
        data = json.loads(out)
        print(f"   Title: {data.get('title', 'N/A')}")
        print(f"   Duration: {data.get('duration', 'N/A')}s")
        print(f"   Uploader: {data.get('uploader', 'N/A')}")
        return True
    else:
        print(f"❌ yt-dlp failed: {err}")
        return False


async def main():
    print("=" * 50)
    print("Instagram Media Pipeline - Dependency Check")
    print("=" * 50)
    
    all_ok = True
    
    # Core dependencies
    all_ok &= check_yt_dlp()
    all_ok &= check_ffmpeg()
    all_ok &= check_playwright()
    all_ok &= check_instaloader()
    
    # Optional: cookies file
    cookies_path = "/Users/alfredkamisese/cookies.txt"
    if Path(cookies_path).exists():
        check_cookies_file(cookies_path)
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ All core dependencies satisfied")
    else:
        print("⚠️ Some dependencies missing - pipeline may have reduced functionality")
    print("=" * 50)
    
    # Quick live test if URL provided
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        print(f"\nRunning live test on: {test_url}")
        await test_yt_dlp_reel(test_url, cookies_path if Path(cookies_path).exists() else None)


if __name__ == "__main__":
    asyncio.run(main())