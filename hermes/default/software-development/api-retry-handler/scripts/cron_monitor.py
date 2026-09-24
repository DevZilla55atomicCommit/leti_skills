#!/usr/bin/env python3
"""
Background monitor for stuck API calls.
Runs as a cron job to detect and recover stuck Hermes sessions.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

LOG_FILE = Path.home() / ".hermes" / "logs" / "api-retry-monitor.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Default configuration
CHECK_INTERVAL = int(os.getenv("API_RETRY_CHECK_INTERVAL", "30"))
STUCK_THRESHOLD = int(os.getenv("API_RETRY_STUCK_THRESHOLD", "60"))
RECOVERY_PROMPT = os.getenv("API_RETRY_RECOVERY_PROMPT", "continue from where you left off")
MAX_RECOVERIES_PER_RUN = int(os.getenv("API_RETRY_MAX_RECOVERIES", "3"))


def log_entry(level: str, **kwargs):
    """Write structured log entry."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"{timestamp} | {level}"]
    for k, v in kwargs.items():
        parts.append(f"{k}={v}")
    with open(LOG_FILE, "a") as f:
        f.write(" | ".join(parts) + "\n")


def get_hermes_sessions() -> List[Dict[str, Any]]:
    """Get list of active Hermes sessions/processes."""
    sessions = []
    
    # Method 1: Check for Hermes terminal processes
    try:
        result = subprocess.run(
            ["pgrep", "-af", "hermes"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.strip().split("\n"):
            if line and "hermes" in line.lower():
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    pid = parts[0]
                    cmd = parts[1]
                    sessions.append({"pid": pid, "cmd": cmd, "source": "pgrep"})
    except Exception:
        pass
    
    # Method 2: Check for tmux sessions with hermes
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}:#{session_id}:#{pane_current_command}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.strip().split("\n"):
            if line and "hermes" in line.lower():
                parts = line.split(":")
                if len(parts) >= 3:
                    sessions.append({
                        "pid": parts[1],
                        "cmd": f"tmux:{parts[0]}",
                        "source": "tmux",
                    })
    except Exception:
        pass
    
    # Method 3: Check Hermes cron jobs
    try:
        result = subprocess.run(
            ["hermes", "cronjob", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Parse output for running jobs
    except Exception:
        pass
    
    return sessions


def check_process_output(pid: str) -> Optional[str]:
    """Check recent output of a process for rate limit errors."""
    try:
        # Try to read from /proc/<pid>/fd/1 or similar
        # This is platform-specific and may not work without root
        # Alternative: check log files
        pass
    except Exception:
        pass
    return None


def check_hermes_logs_for_rate_limits() -> List[Dict[str, Any]]:
    """Check Hermes logs for recent 429 errors."""
    stuck_sessions = []
    
    # Check common log locations
    log_paths = [
        Path.home() / ".hermes" / "logs" / "api-retry.log",
        Path.home() / ".hermes" / "logs" / "hermes.log",
        Path.home() / ".hermes" / "logs" / "*.log",
        Path("/var/log/hermes/*.log"),
    ]
    
    for log_path in log_paths:
        for file in log_path.parent.glob(log_path.name):
            try:
                # Check last 100 lines for 429 errors
                result = subprocess.run(
                    ["tail", "-100", str(file)],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                lines = result.stdout.strip().split("\n")
                for i, line in enumerate(lines):
                    if "429" in line or "Too Many Requests" in line or "rate limit" in line.lower():
                        # Check if this is recent (within stuck threshold)
                        stuck_sessions.append({
                            "log_file": str(file),
                            "line_number": len(lines) - i,
                            "content": line[:200],
                            "detected_at": time.time(),
                        })
            except Exception:
                continue
    
    return stuck_sessions


def send_recovery_prompt(session_info: Dict[str, Any], prompt: str) -> bool:
    """Send recovery prompt to a stuck session."""
    pid = session_info.get("pid")
    source = session_info.get("source", "unknown")
    
    log_entry("RECOVERY_ATTEMPT", pid=pid, source=source, prompt=prompt)
    
    try:
        if source == "tmux":
            # Send to tmux pane
            session_name = session_info.get("cmd", "").replace("tmux:", "")
            subprocess.run(
                ["tmux", "send-keys", "-t", session_name, prompt, "Enter"],
                check=True,
                timeout=5,
            )
            log_entry("RECOVERY_SENT", pid=pid, method="tmux")
            return True
            
        elif source == "pgrep":
            # Try to write to stdin of process (requires appropriate permissions)
            # This is tricky without ptrace or similar
            log_entry("RECOVERY_SKIPPED", pid=pid, reason="Cannot send to raw process")
            return False
            
        else:
            log_entry("RECOVERY_SKIPPED", pid=pid, reason=f"Unknown source: {source}")
            return False
            
    except Exception as e:
        log_entry("RECOVERY_FAILED", pid=pid, error=str(e))
        return False


def create_cron_recovery_job() -> bool:
    """Create a Hermes cron job for automatic recovery."""
    try:
        # Check if cron job already exists
        result = subprocess.run(
            ["hermes", "cronjob", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if "api-rate-limit-recovery" in result.stdout:
            log_entry("CRON_EXISTS", name="api-rate-limit-recovery")
            return True
        
        # Create the cron job
        prompt = (
            "Monitor for stuck API calls (HTTP 429 rate limits) in active Hermes sessions. "
            "If a session appears stuck on a rate limit for more than 60 seconds, "
            "send a 'continue from where you left off' prompt to resume the task. "
            "Log all recovery attempts to ~/.hermes/logs/api-retry-monitor.log"
        )
        
        result = subprocess.run(
            [
                "hermes", "cronjob", "create",
                "--name", "api-rate-limit-recovery",
                "--schedule", "*/2 * * * *",  # Every 2 minutes
                "--skills", "api-retry-handler",
                "--prompt", prompt,
                "--deliver", "origin",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            log_entry("CRON_CREATED", name="api-rate-limit-recovery")
            return True
        else:
            log_entry("CRON_CREATE_FAILED", error=result.stderr)
            return False
            
    except Exception as e:
        log_entry("CRON_ERROR", error=str(e))
        return False


def monitor_once() -> int:
    """Run one monitoring cycle."""
    log_entry("MONITOR_START")
    
    # Check for stuck sessions
    stuck_from_logs = check_hermes_logs_for_rate_limits()
    
    if not stuck_from_logs:
        log_entry("MONITOR_CLEAN", message="No stuck sessions detected")
        return 0
    
    log_entry("MONITOR_FOUND", count=len(stuck_from_logs))
    
    recoveries = 0
    for session in stuck_from_logs[:MAX_RECOVERIES_PER_RUN]:
        if send_recovery_prompt(session, RECOVERY_PROMPT):
            recoveries += 1
            time.sleep(2)  # Small delay between recoveries
    
    log_entry("MONITOR_COMPLETE", recoveries=recoveries)
    return recoveries


def monitor_continuous(interval: int = CHECK_INTERVAL, threshold: int = STUCK_THRESHOLD):
    """Run continuous monitoring."""
    log_entry("CONTINUOUS_START", interval=interval, threshold=threshold)
    
    # Ensure cron job exists
    create_cron_recovery_job()
    
    while True:
        try:
            monitor_once()
        except Exception as e:
            log_entry("MONITOR_ERROR", error=str(e))
        
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor and recover stuck API calls from rate limits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run once (for cron)
  python cron_monitor.py --once
  
  # Run continuously
  python cron_monitor.py --continuous --interval 30
  
  # Create cron job only
  python cron_monitor.py --create-cron
  
  # Check status
  python cron_monitor.py --status
        """
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one monitoring cycle and exit",
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run continuous monitoring loop",
    )
    parser.add_argument(
        "--create-cron",
        action="store_true",
        help="Create the Hermes cron job for automatic monitoring",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show monitoring status and recent log entries",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=CHECK_INTERVAL,
        help=f"Check interval in seconds (default: {CHECK_INTERVAL})",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=STUCK_THRESHOLD,
        help=f"Stuck threshold in seconds (default: {STUCK_THRESHOLD})",
    )
    parser.add_argument(
        "--recovery-prompt",
        type=str,
        default=RECOVERY_PROMPT,
        help=f"Recovery prompt to send (default: '{RECOVERY_PROMPT}')",
    )
    parser.add_argument(
        "--max-recoveries",
        type=int,
        default=MAX_RECOVERIES_PER_RUN,
        help=f"Max recoveries per cycle (default: {MAX_RECOVERIES_PER_RUN})",
    )
    
    args = parser.parse_args()
    
    if args.create_cron:
        success = create_cron_recovery_job()
        sys.exit(0 if success else 1)
    
    if args.status:
        # Show recent log entries
        try:
            result = subprocess.run(
                ["tail", "-50", str(LOG_FILE)],
                capture_output=True,
                text=True,
                timeout=5,
            )
            print(result.stdout or "No log entries yet")
        except Exception:
            print("Log file not found or empty")
        sys.exit(0)
    
    if args.once:
        count = monitor_once()
        print(f"Monitoring complete. Recoveries attempted: {count}")
        sys.exit(0)
    
    if args.continuous:
        monitor_continuous(args.interval, args.threshold)
    
    # Default: run once
    count = monitor_once()
    print(f"Monitoring complete. Recoveries attempted: {count}")


if __name__ == "__main__":
    main()