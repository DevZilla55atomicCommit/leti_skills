#!/usr/bin/env python3
"""
CLI wrapper that runs a command with automatic retry on HTTP 429/5xx errors.
After max retries, sends a "continue" prompt via stdin to resume.
"""

import argparse
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

# Configuration from environment
MAX_RETRIES = int(os.getenv("API_RETRY_MAX_RETRIES", "5"))
BASE_DELAY = float(os.getenv("API_RETRY_BASE_DELAY", "10"))
MAX_DELAY = float(os.getenv("API_RETRY_MAX_DELAY", "160"))
JITTER = float(os.getenv("API_RETRY_JITTER", "0.2"))
RETRY_CODES = set(int(x) for x in os.getenv("API_RETRY_ON", "429,500,502,503,504").split(","))
CONTINUE_PROMPT = os.getenv("API_RETRY_CONTINUE_PROMPT", "continue")
MAX_CONTINUES = int(os.getenv("API_RETRY_MAX_CONTINUE", "3"))

LOG_FILE = Path.home() / ".hermes" / "logs" / "api-retry.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_entry(level: str, **kwargs):
    """Write structured log entry."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"{timestamp} | {level}"]
    for k, v in kwargs.items():
        parts.append(f"{k}={v}")
    with open(LOG_FILE, "a") as f:
        f.write(" | ".join(parts) + "\n")


def extract_http_codes(text: str) -> List[int]:
    """Extract HTTP status codes from text."""
    codes = []
    # Match patterns like "HTTP 429", "status 429", "429 Too Many", etc.
    patterns = [
        r"HTTP\s+(\d{3})",
        r"status[:\s]+(\d{3})",
        r"\b(\d{3})\s+(?:Too Many|Rate Limit|Internal|Bad Gateway|Service Unavailable|Gateway Timeout)",
        r'"status":\s*(\d{3})',
        r"Status:\s*(\d{3})",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            codes.append(int(match.group(1)))
    return codes


def should_retry(codes: List[int]) -> bool:
    """Check if any code matches retry criteria."""
    return any(code in RETRY_CODES for code in codes)


def calculate_delay(attempt: int) -> float:
    """Calculate exponential backoff with jitter."""
    delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
    jitter_amount = delay * JITTER
    return delay + random.uniform(-jitter_amount, jitter_amount)


def run_with_retry(
    command: List[str],
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    max_delay: float = MAX_DELAY,
    retry_codes: set = RETRY_CODES,
    continue_prompt: str = CONTINUE_PROMPT,
    max_continues: int = MAX_CONTINUES,
    stdin_prompt: bool = False,
) -> Tuple[int, str, str]:
    """
    Run command with automatic retry on rate limits.
    Returns (exit_code, stdout, stderr).
    """
    log_entry(
        "START",
        cmd=" ".join(command),
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
    )

    continue_count = 0
    last_stdout = ""
    last_stderr = ""

    for attempt in range(max_retries + 1):
        log_entry("ATTEMPT", attempt=attempt + 1, total=max_retries + 1)

        # Prepare stdin if sending continue prompt
        stdin_data = None
        if attempt > 0 and continue_count < max_continues and stdin_prompt:
            stdin_data = continue_prompt + "\n"
            continue_count += 1
            log_entry("CONTINUE_PROMPT_SENT", prompt=continue_prompt, count=continue_count)

        try:
            proc = subprocess.Popen(
                command,
                stdin=subprocess.PIPE if stdin_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = proc.communicate(input=stdin_data, timeout=300)
            exit_code = proc.returncode

            last_stdout = stdout
            last_stderr = stderr

            # Check for rate limit in output
            all_output = stdout + stderr
            codes = extract_http_codes(all_output)

            if codes and should_retry(codes) and attempt < max_retries:
                delay = calculate_delay(attempt)
                log_entry(
                    "RETRY",
                    attempt=attempt + 1,
                    total=max_retries + 1,
                    delay=round(delay, 1),
                    codes=codes,
                    cmd=" ".join(command),
                )
                print(f"\n[api-retry] Rate limit detected (codes: {codes}). Waiting {delay:.1f}s before retry {attempt + 2}/{max_retries + 1}...")
                time.sleep(delay)
                continue

            # Success or non-retryable error
            if exit_code == 0:
                log_entry("SUCCESS", attempt=attempt + 1, cmd=" ".join(command))
            else:
                log_entry("FAILURE", attempt=attempt + 1, exit_code=exit_code, codes=codes, cmd=" ".join(command))

            return exit_code, stdout, stderr

        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            log_entry("TIMEOUT", attempt=attempt + 1, cmd=" ".join(command))
            if attempt < max_retries:
                delay = calculate_delay(attempt)
                time.sleep(delay)
                continue
            return -1, stdout or "", stderr or "Command timed out"

        except Exception as e:
            log_entry("ERROR", attempt=attempt + 1, error=str(e), cmd=" ".join(command))
            if attempt < max_retries:
                delay = calculate_delay(attempt)
                time.sleep(delay)
                continue
            return -1, "", str(e)

    # Max retries exhausted
    log_entry("MAX_RETRIES_EXHAUSTED", cmd=" ".join(command))
    return -1, last_stdout, last_stderr


def main():
    parser = argparse.ArgumentParser(
        description="Run command with automatic retry on HTTP 429/5xx errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  api-retry-wrapper -- claude-code "your prompt"
  
  # With custom config
  api-retry-wrapper --max-retries 5 --base-delay 10 --max-delay 160 -- claude-code "prompt"
  
  # Send continue prompt via stdin after retries
  api-retry-wrapper --stdin-prompt -- claude-code --stdin "prompt"
  
  # Custom retry codes
  api-retry-wrapper --retry-codes "429,500,502,503,504" -- curl -X POST ...
        """
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run (after -- separator)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=MAX_RETRIES,
        help=f"Max retry attempts (default: {MAX_RETRIES})",
    )
    parser.add_argument(
        "--base-delay",
        type=float,
        default=BASE_DELAY,
        help=f"Base delay in seconds (default: {BASE_DELAY})",
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=MAX_DELAY,
        help=f"Max delay cap in seconds (default: {MAX_DELAY})",
    )
    parser.add_argument(
        "--retry-codes",
        type=str,
        default=",".join(str(c) for c in sorted(RETRY_CODES)),
        help=f"Comma-separated HTTP codes to retry (default: {','.join(str(c) for c in sorted(RETRY_CODES))})",
    )
    parser.add_argument(
        "--continue-prompt",
        type=str,
        default=CONTINUE_PROMPT,
        help=f"Prompt to send via stdin after backoff (default: '{CONTINUE_PROMPT}')",
    )
    parser.add_argument(
        "--max-continues",
        type=int,
        default=MAX_CONTINUES,
        help=f"Max continue prompts to send (default: {MAX_CONTINUES})",
    )
    parser.add_argument(
        "--stdin-prompt",
        action="store_true",
        help="Send continue prompt via stdin to the subprocess",
    )
    parser.add_argument(
        "--jitter",
        type=float,
        default=JITTER,
        help=f"Jitter factor 0-1 (default: {JITTER})",
    )

    args = parser.parse_args()

    if not args.command:
        parser.error("No command provided. Use -- to separate: api-retry-wrapper -- your-command args")

    # Parse retry codes
    retry_codes = set(int(x.strip()) for x in args.retry_codes.split(","))

    exit_code, stdout, stderr = run_with_retry(
        command=args.command,
        max_retries=args.max_retries,
        base_delay=args.base_delay,
        max_delay=args.max_delay,
        retry_codes=retry_codes,
        continue_prompt=args.continue_prompt,
        max_continues=args.max_continues,
        stdin_prompt=args.stdin_prompt,
    )

    # Output results
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, file=sys.stderr, end="")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()