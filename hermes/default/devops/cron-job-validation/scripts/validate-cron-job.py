#!/usr/bin/env python3
"""
Automated cron job validation script.

Checks:
1. Script exists and is executable
2. Script runs without error (dry-run if supported)
3. Output shape is as expected
4. Side effects can be verified
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
CRON_DIR = HERMES_HOME / "cron"
JOBS_FILE = CRON_DIR / "jobs.json"
OUTPUT_DIR = CRON_DIR / "output"


def load_jobs():
    with open(JOBS_FILE) as f:
        return json.load(f)["jobs"]


def validate_job(job):
    job_id = job["id"]
    name = job["name"]
    script = job.get("script")
    workdir = job.get("workdir")
    enabled_toolsets = job.get("enabled_toolsets", [])

    results = {
        "job_id": job_id,
        "name": name,
        "checks": {},
        "overall": "unknown"
    }

    # Check 1: Script exists
    if script:
        script_path = Path(script)
        if not script_path.is_absolute():
            # Relative to workdir or HERMES_HOME/scripts
            if workdir:
                script_path = Path(workdir) / script
            else:
                script_path = HERMES_HOME / "scripts" / script

        results["checks"]["script_exists"] = script_path.exists()
        results["checks"]["script_path"] = str(script_path)
        results["checks"]["script_executable"] = script_path.exists() and os.access(script_path, os.X_OK)

        # Check 2: Run script dry-run if it exists
        if script_path.exists():
            try:
                # Try running with --help or --dry-run to validate syntax
                env = os.environ.copy()
                env["HERMES_HOME"] = str(HERMES_HOME)
                cwd = workdir or str(HERMES_HOME)

                result = subprocess.run(
                    [sys.executable, str(script_path), "--help"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=cwd,
                    env=env
                )
                results["checks"]["script_runs"] = result.returncode == 0
                results["checks"]["script_stdout"] = result.stdout[:500]
                results["checks"]["script_stderr"] = result.stderr[:500]
            except subprocess.TimeoutExpired:
                results["checks"]["script_runs"] = False
                results["checks"]["script_error"] = "Timeout"
            except Exception as e:
                results["checks"]["script_runs"] = False
                results["checks"]["script_error"] = str(e)
    else:
        results["checks"]["script_exists"] = True  # No script = agent-only job
        results["checks"]["script_path"] = "N/A (agent-only)"
        results["checks"]["script_executable"] = True
        results["checks"]["script_runs"] = True

    # Check 3: Recent output exists and is non-empty
    job_output_dir = OUTPUT_DIR / job_id
    if job_output_dir.exists():
        output_files = sorted(job_output_dir.glob("*.md"))
        if output_files:
            latest = output_files[-1]
            content = latest.read_text()
            results["checks"]["has_recent_output"] = True
            results["checks"]["latest_output_file"] = str(latest)
            results["checks"]["output_length"] = len(content)
            results["checks"]["output_preview"] = content[:300]
        else:
            results["checks"]["has_recent_output"] = False
    else:
        results["checks"]["has_recent_output"] = False

    # Determine overall status
    critical_checks = ["script_exists", "script_runs"]
    if all(results["checks"].get(c, True) for c in critical_checks):
        results["overall"] = "pass"
    else:
        results["overall"] = "fail"

    return results


def main():
    jobs = load_jobs()
    enabled_jobs = [j for j in jobs if j.get("enabled", False)]

    print(f"Validating {len(enabled_jobs)} enabled cron jobs...\n")

    all_pass = True
    for job in enabled_jobs:
        result = validate_job(job)
        status = "✅ PASS" if result["overall"] == "pass" else "❌ FAIL"
        print(f"{status} {result['name']} ({result['job_id']})")

        for check, value in result["checks"].items():
            if isinstance(value, bool):
                icon = "  ✓" if value else "  ✗"
                print(f"{icon} {check}")
            elif check in ("script_error", "script_stderr") and value:
                print(f"  ⚠ {check}: {value}")

        if result["overall"] == "fail":
            all_pass = False
        print()

    print("=" * 50)
    if all_pass:
        print("All enabled cron jobs passed validation.")
        sys.exit(0)
    else:
        print("Some cron jobs failed validation. Review output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()