#!/usr/bin/env python3
"""
Wrapper for OpenAI-compatible clients (OpenAI, Anthropic via LiteLLM, NVIDIA NIM, etc.)
Adds automatic retry with exponential backoff.
"""

import os
from typing import Any, Dict, Optional
from retry_decorator import retry_with_backoff, RetryingClient


class APIClientWrapper:
    """
    High-level wrapper for OpenAI-compatible API clients.
    
    Usage:
        from openai import OpenAI
        from api_client_wrapper import APIClientWrapper
        
        # Wrap any OpenAI-compatible client
        client = APIClientWrapper(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY"),
            provider="nvidia-nim"  # Uses preset config
        )
        
        response = client.chat(
            model="nvidia/nemotron-3-ultra-550b-a55b",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=4096
        )
    """
    
    # Provider presets (from templates/providers.yaml)
    PROVIDER_PRESETS = {
        "nvidia-nim": {
            "base_url": "https://integrate.api.nvidia.com/v1",
            "max_retries": 5,
            "base_delay": 10,
            "max_delay": 160,
            "jitter": 0.2,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "max_retries": 3,
            "base_delay": 5,
            "max_delay": 60,
            "jitter": 0.2,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "anthropic": {
            "base_url": "https://api.anthropic.com/v1",
            "max_retries": 3,
            "base_delay": 5,
            "max_delay": 60,
            "jitter": 0.2,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "together": {
            "base_url": "https://api.together.xyz/v1",
            "max_retries": 3,
            "base_delay": 5,
            "max_delay": 60,
            "jitter": 0.2,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "fireworks": {
            "base_url": "https://api.fireworks.ai/inference/v1",
            "max_retries": 3,
            "base_delay": 5,
            "max_delay": 60,
            "jitter": 0.2,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "vllm": {
            "base_url": "http://localhost:8000/v1",
            "max_retries": 10,
            "base_delay": 2,
            "max_delay": 30,
            "jitter": 0.1,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "ollama": {
            "base_url": "http://localhost:11434/v1",
            "max_retries": 10,
            "base_delay": 2,
            "max_delay": 30,
            "jitter": 0.1,
            "retry_codes": (429, 500, 502, 503, 504),
        },
        "litellm": {
            "base_url": "http://localhost:4000/v1",
            "max_retries": 5,
            "base_delay": 5,
            "max_delay": 120,
            "jitter": 0.2,
            "retry_codes": (429, 500, 502, 503, 504),
        },
    }
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        provider: Optional[str] = None,
        max_retries: Optional[int] = None,
        base_delay: Optional[float] = None,
        max_delay: Optional[float] = None,
        jitter: Optional[float] = None,
        retry_codes: Optional[tuple] = None,
        **client_kwargs,
    ):
        """
        Initialize the wrapper.
        
        Args:
            base_url: API base URL
            api_key: API key
            provider: Provider preset name (overrides other params if set)
            max_retries: Max retry attempts
            base_delay: Base delay in seconds
            max_delay: Max delay cap in seconds
            jitter: Jitter factor 0-1
            retry_codes: HTTP codes to retry on
            **client_kwargs: Additional args passed to OpenAI client
        """
        # Apply provider preset if specified
        if provider and provider in self.PROVIDER_PRESETS:
            preset = self.PROVIDER_PRESETS[provider]
            base_url = preset.get("base_url", base_url)
            max_retries = max_retries or preset.get("max_retries", 5)
            base_delay = base_delay or preset.get("base_delay", 10)
            max_delay = max_delay or preset.get("max_delay", 160)
            jitter = jitter or preset.get("jitter", 0.2)
            retry_codes = retry_codes or preset.get("retry_codes", (429, 500, 502, 503, 504))
        
        # Defaults
        self.max_retries = max_retries or 5
        self.base_delay = base_delay or 10
        self.max_delay = max_delay or 160
        self.jitter = jitter or 0.2
        self.retry_codes = retry_codes or (429, 500, 502, 503, 504)
        
        # Import and create OpenAI client
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package required: pip install openai")
        
        self._client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            **client_kwargs,
        )
        
        # Wrap with retry logic
        self._retrying_client = RetryingClient(
            self._client,
            max_retries=self.max_retries,
            base_delay=self.base_delay,
            max_delay=self.max_delay,
            jitter=self.jitter,
            retry_on=self.retry_codes,
        )
    
    @property
    def client(self):
        """Access the underlying OpenAI client (with retry wrapper)."""
        return self._retrying_client
    
    def chat(
        self,
        model: str,
        messages: list,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs,
    ):
        """
        Create a chat completion with automatic retry.
        
        Args:
            model: Model name
            messages: List of message dicts
            max_tokens: Max tokens in response
            temperature: Sampling temperature
            **kwargs: Additional params passed to API
            
        Returns:
            Chat completion response
        """
        return self._retrying_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
    
    def stream_chat(
        self,
        model: str,
        messages: list,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs,
    ):
        """
        Stream a chat completion with automatic retry on connection errors.
        
        Note: Streaming retries only apply to initial connection, not mid-stream.
        """
        return self._retrying_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
            **kwargs,
        )
    
    def embeddings(
        self,
        model: str,
        input: list,
        **kwargs,
    ):
        """Create embeddings with automatic retry."""
        return self._retrying_client.embeddings.create(
            model=model,
            input=input,
            **kwargs,
        )
    
    def list_models(self):
        """List available models."""
        return self._retrying_client.models.list()
    
    def __getattr__(self, name):
        """Delegate unknown attributes to underlying client."""
        return getattr(self._retrying_client, name)


def create_client_from_env(provider: str = "nvidia-nim") -> APIClientWrapper:
    """
    Create client from environment variables.
    
    Expected env vars:
        NVIDIA_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
    """
    env_map = {
        "nvidia-nim": "NVIDIA_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "together": "TOGETHER_API_KEY",
        "fireworks": "FIREWORKS_API_KEY",
        "litellm": "LITELLM_MASTER_KEY",
    }
    
    api_key_env = env_map.get(provider, "OPENAI_API_KEY")
    api_key = os.getenv(api_key_env)
    
    if not api_key:
        raise ValueError(f"API key not found in environment: {api_key_env}")
    
    return APIClientWrapper(
        base_url="",  # Will be set from preset
        api_key=api_key,
        provider=provider,
    )


# Example usage
if __name__ == "__main__":
    import os
    
    # Example 1: Direct usage with NVIDIA NIM
    api_key = os.getenv("NVIDIA_API_KEY")
    if api_key:
        client = APIClientWrapper(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
            provider="nvidia-nim",
        )
        
        print("Testing NVIDIA NIM client with retry...")
        try:
            response = client.chat(
                model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
                messages=[{"role": "user", "content": "Say hello in one sentence"}],
                max_tokens=100,
            )
            print(f"Response: {response.choices[0].message.content}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Example 2: From environment
    # client = create_client_from_env("nvidia-nim")