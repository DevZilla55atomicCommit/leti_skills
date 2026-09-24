#!/usr/bin/env python3
"""
Python decorator for automatic retry with exponential backoff on API calls.
Supports OpenAI-compatible clients, httpx, requests, aiohttp, etc.
"""

import functools
import os
import random
import re
import time
from pathlib import Path
from typing import Callable, Optional, Tuple, TypeVar, Union

# Configuration from environment
MAX_RETRIES = int(os.getenv("API_RETRY_MAX_RETRIES", "5"))
BASE_DELAY = float(os.getenv("API_RETRY_BASE_DELAY", "10"))
MAX_DELAY = float(os.getenv("API_RETRY_MAX_DELAY", "160"))
JITTER = float(os.getenv("API_RETRY_JITTER", "0.2"))
RETRY_CODES = tuple(int(x) for x in os.getenv("API_RETRY_ON", "429,500,502,503,504").split(","))
CONTINUE_PROMPT = os.getenv("API_RETRY_CONTINUE_PROMPT", "continue")

LOG_FILE = Path.home() / ".hermes" / "logs" / "api-retry.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., T])


def log_entry(level: str, **kwargs):
    """Write structured log entry."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"{timestamp} | {level}"]
    for k, v in kwargs.items():
        parts.append(f"{k}={v}")
    with open(LOG_FILE, "a") as f:
        f.write(" | ".join(parts) + "\n")


def extract_status_code(error: Exception) -> Tuple[int, Optional[float]]:
    """Extract HTTP status code and optional Retry-After delay from various exception types.
    
    Returns:
        (status_code, retry_after_seconds)
    """
    # httpx.HTTPStatusError
    if hasattr(error, "response") and hasattr(error.response, "status_code"):
        status = error.response.status_code
        retry_after = None
        if hasattr(error.response, "headers"):
            ra = error.response.headers.get("Retry-After") or error.response.headers.get("retry-after")
            if ra:
                try:
                    retry_after = float(ra)
                except ValueError:
                    pass
        return status, retry_after
    
    # requests.HTTPError
    if hasattr(error, "response") and error.response is not None:
        status = error.response.status_code
        retry_after = None
        if hasattr(error.response, "headers"):
            ra = error.response.headers.get("Retry-After") or error.response.headers.get("retry-after")
            if ra:
                try:
                    retry_after = float(ra)
                except ValueError:
                    pass
        return status, retry_after
    
    # aiohttp.ClientResponseError
    if hasattr(error, "status"):
        return error.status, None
    
    # OpenAI API errors
    if hasattr(error, "status_code"):
        return error.status_code, None
    if hasattr(error, "code"):
        return error.code, None
    
    # Generic: check error message for status codes
    error_str = str(error)
    for pattern in [r"(\d{3})", r"status[:\s]+(\d{3})", r"HTTP\s+(\d{3})"]:
        match = re.search(pattern, error_str)
        if match:
            return int(match.group(1)), None
    
    return 0, None


def calculate_delay(attempt: int, base_delay: float, max_delay: float, jitter: float) -> float:
    """Calculate exponential backoff with jitter."""
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter_amount = delay * jitter
    return delay + random.uniform(-jitter_amount, jitter_amount)


def retry_with_backoff(
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    max_delay: float = MAX_DELAY,
    jitter: float = JITTER,
    retry_on: Tuple[int, ...] = RETRY_CODES,
    continue_prompt: str = CONTINUE_PROMPT,
    on_retry: Callable[[int, float], None] = None,
    on_give_up: Callable[[Exception], None] = None,
    respect_retry_after: bool = True,
):
    """
    Decorator for automatic retry with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay cap in seconds
        jitter: Jitter factor (0-1)
        retry_on: HTTP status codes to retry on
        continue_prompt: Prompt to use for continuation (not used in decorator, for logging)
        on_retry: Callback(attempt, delay) called before each retry
        on_give_up: Callback(error) called when all retries exhausted
        respect_retry_after: If True, use Retry-After header from 429/503 responses when present
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    log_entry("ATTEMPT", func=func.__name__, attempt=attempt + 1, total=max_retries + 1)
                    result = func(*args, **kwargs)
                    
                    if attempt > 0:
                        log_entry("SUCCESS", func=func.__name__, attempt=attempt + 1)
                    return result
                   
                except Exception as e:
                    last_error = e
                    status_code, retry_after = extract_status_code(e)
                    
                    # Check if we should retry
                    should_retry = status_code in retry_on
                    
                    log_entry(
                        "ERROR",
                        func=func.__name__,
                        attempt=attempt + 1,
                        status_code=status_code,
                        error=str(e)[:200],
                        will_retry=should_retry and attempt < max_retries,
                        retry_after=retry_after,
                    )
                    
                    if should_retry and attempt < max_retries:
                        # Use Retry-After header if present and respect_retry_after is True
                        if respect_retry_after and retry_after is not None and retry_after > 0:
                            delay = min(retry_after + 1.0, max_delay)  # Add 1s buffer
                            log_entry("RETRY_AFTER", func=func.__name__, retry_after=retry_after, using_delay=delay)
                        else:
                            delay = calculate_delay(attempt, base_delay, max_delay, jitter)
                        
                        if on_retry:
                            on_retry(attempt + 1, delay)
                        else:
                            retry_reason = f"Retry-After: {retry_after:.1f}s" if respect_retry_after and retry_after else f"Rate limit ({status_code})"
                            print(f"\n[api-retry] {func.__name__}: {retry_reason}. Retry {attempt + 2}/{max_retries + 1} in {delay:.1f}s...")
                        
                        time.sleep(delay)
                        continue
                    
                    # Don't retry - either not retryable or max retries reached
                    break
            
            # All retries exhausted or non-retryable error
            log_entry("GIVE_UP", func=func.__name__, error=str(last_error)[:200])
            if on_give_up:
                on_give_up(last_error)
            raise last_error
        
        return wrapper
    return decorator


# Async version
def retry_with_backoff_async(
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    max_delay: float = MAX_DELAY,
    jitter: float = JITTER,
    retry_on: Tuple[int, ...] = RETRY_CODES,
    continue_prompt: str = CONTINUE_PROMPT,
    on_retry: Callable[[int, float], None] = None,
    on_give_up: Callable[[Exception], None] = None,
    respect_retry_after: bool = True,
):
    """Async version of retry_with_backoff."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    log_entry("ATTEMPT", func=func.__name__, attempt=attempt + 1, total=max_retries + 1)
                    result = await func(*args, **kwargs)
                    
                    if attempt > 0:
                        log_entry("SUCCESS", func=func.__name__, attempt=attempt + 1)
                    return result
                   
                except Exception as e:
                    last_error = e
                    status_code, retry_after = extract_status_code(e)
                    should_retry = status_code in retry_on
                    
                    log_entry(
                        "ERROR",
                        func=func.__name__,
                        attempt=attempt + 1,
                        status_code=status_code,
                        error=str(e)[:200],
                        will_retry=should_retry and attempt < max_retries,
                        retry_after=retry_after,
                    )
                    
                    if should_retry and attempt < max_retries:
                        if respect_retry_after and retry_after is not None and retry_after > 0:
                            delay = min(retry_after + 1.0, max_delay)
                            log_entry("RETRY_AFTER", func=func.__name__, retry_after=retry_after, using_delay=delay)
                        else:
                            delay = calculate_delay(attempt, base_delay, max_delay, jitter)
                        
                        if on_retry:
                            on_retry(attempt + 1, delay)
                        else:
                            retry_reason = f"Retry-After: {retry_after:.1f}s" if respect_retry_after and retry_after else f"Rate limit ({status_code})"
                            print(f"\n[api-retry] {func.__name__}: {retry_reason}. Retry {attempt + 2}/{max_retries + 1} in {delay:.1f}s...")
                        
                        await asyncio.sleep(delay)
                        continue
                    
                    break
            
            log_entry("GIVE_UP", func=func.__name__, error=str(last_error)[:200])
            if on_give_up:
                on_give_up(last_error)
            raise last_error
        
        return wrapper
    return decorator


# OpenAI-compatible client wrapper
class RetryingClient:
    """
    Wrapper for OpenAI-compatible clients that adds automatic retry.
    
    Usage:
        from openai import OpenAI
        from retry_decorator import RetryingClient
        
        client = RetryingClient(OpenAI(api_key="...", base_url="..."))
        response = client.chat.completions.create(...)
    """
    
    def __init__(
        self,
        client,
        max_retries: int = MAX_RETRIES,
        base_delay: float = BASE_DELAY,
        max_delay: float = MAX_DELAY,
        jitter: float = JITTER,
        retry_on: Tuple[int, ...] = RETRY_CODES,
    ):
        self._client = client
        self._config = {
            "max_retries": max_retries,
            "base_delay": base_delay,
            "max_delay": max_delay,
            "jitter": jitter,
            "retry_on": retry_on,
        }
        # Wrap the chat.completions.create method
        self.chat = self._wrap_chat(client.chat)
    
    def _wrap_chat(self, chat):
        class WrappedChat:
            def __init__(self, chat, config):
                self._chat = chat
                self._config = config
                self.completions = self._wrap_completions(chat.completions, config)
            
            def _wrap_completions(self, completions, config):
                class WrappedCompletions:
                    def __init__(self, completions, config):
                        self._completions = completions
                        self._config = config
                    
                    @retry_with_backoff(**config)
                    def create(self, *args, **kwargs):
                        return self._completions.create(*args, **kwargs)
                    
                    # Delegate other methods
                    def __getattr__(self, name):
                        return getattr(self._completions, name)
                
                return WrappedCompletions(completions, config)
            
            def __getattr__(self, name):
                return getattr(self._chat, name)
        
        return WrappedChat(chat, self._config)
    
    def __getattr__(self, name):
        return getattr(self._client, name)


# Example usage and testing
if __name__ == "__main__":
    # Test the decorator
    @retry_with_backoff(max_retries=3, base_delay=1, max_delay=5, jitter=0.1)
    def test_function(should_fail: bool = True):
        if should_fail:
            # Simulate a 429 error
            class MockError(Exception):
                def __init__(self):
                    self.status_code = 429
            raise MockError()
        return "success"
    
    print("Testing retry decorator...")
    try:
        result = test_function(should_fail=False)
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed as expected: {e}")
    
    print("\nTesting with simulated failures...")
    call_count = 0
    @retry_with_backoff(max_retries=3, base_delay=0.5, max_delay=2, jitter=0)
    def test_with_failures():
        global call_count
        call_count += 1
        if call_count < 3:
            class MockError(Exception):
                def __init__(self):
                    self.status_code = 429
            raise MockError()
        return "success after retries"
    
    try:
        result = test_with_failures()
        print(f"Result: {result} (calls: {call_count})")
    except Exception as e:
        print(f"Failed: {e}")