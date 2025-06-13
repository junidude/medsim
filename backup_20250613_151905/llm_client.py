#!/usr/bin/env python3
"""
Unified LLM client with async support and response caching.
"""

import os
import json
import asyncio
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import httpx
from functools import lru_cache

# Import provider SDKs
try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

class LLMClient:
    """Unified client for all LLM providers with caching and async support."""
    
    def __init__(self, provider: str = "deepseek", cache_ttl: int = 300):
        self.provider = provider.lower()
        self.cache_ttl = cache_ttl  # Cache time-to-live in seconds
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        
        # Load API keys from environment or config
        self.api_keys = self._load_api_keys()
        
        # Initialize HTTP client for async requests
        self.http_client = httpx.AsyncClient(timeout=60.0)
        
        # Provider-specific configurations
        self.provider_configs = {
            "deepseek": {
                "base_url": "https://api.deepseek.com/v1",
                "model": "deepseek-chat",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "anthropic": {
                "model": "claude-3-opus-20240229",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "openai": {
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment or api_keys.json."""
        keys = {}
        
        # Try environment variables first
        keys["deepseek"] = os.getenv("DEEPSEEK_API_KEY", "")
        keys["anthropic"] = os.getenv("ANTHROPIC_API_KEY", "")
        keys["openai"] = os.getenv("OPENAI_API_KEY", "")
        
        # Try api_keys.json if env vars not found
        if not any(keys.values()):
            try:
                with open("api_keys.json", "r") as f:
                    file_keys = json.load(f)
                    keys["deepseek"] = file_keys.get("deepseek", "")
                    keys["anthropic"] = file_keys.get("anthropic", "")
                    keys["openai"] = file_keys.get("openai", "")
            except:
                pass
        
        return keys
    
    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key for a prompt."""
        # Create a unique key based on prompt and parameters
        cache_data = {
            "prompt": prompt,
            "provider": self.provider,
            **kwargs
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Get cached response if available and not expired."""
        if cache_key in self.response_cache:
            cached = self.response_cache[cache_key]
            if datetime.now() < cached["expires_at"]:
                return cached["response"]
            else:
                # Remove expired cache
                del self.response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: str):
        """Cache a response with expiration."""
        self.response_cache[cache_key] = {
            "response": response,
            "expires_at": datetime.now() + timedelta(seconds=self.cache_ttl)
        }
    
    async def generate_async(self, prompt: str, **kwargs) -> str:
        """Generate response asynchronously with caching."""
        # Check cache first
        cache_key = self._get_cache_key(prompt, **kwargs)
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            return cached_response
        
        # Get provider config
        config = self.provider_configs.get(self.provider, {})
        
        # Merge with kwargs
        temperature = kwargs.get("temperature", config.get("temperature", 0.7))
        max_tokens = kwargs.get("max_tokens", config.get("max_tokens", 2000))
        
        try:
            if self.provider == "deepseek":
                response = await self._generate_deepseek_async(
                    prompt, temperature, max_tokens
                )
            elif self.provider == "anthropic":
                response = await self._generate_anthropic_async(
                    prompt, temperature, max_tokens
                )
            elif self.provider == "openai":
                response = await self._generate_openai_async(
                    prompt, temperature, max_tokens
                )
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            # Cache the response
            self._cache_response(cache_key, response)
            return response
            
        except Exception as e:
            print(f"Error generating response with {self.provider}: {e}")
            # Try fallback providers
            for fallback in ["deepseek", "anthropic", "openai"]:
                if fallback != self.provider and self.api_keys.get(fallback):
                    try:
                        self.provider = fallback
                        return await self.generate_async(prompt, **kwargs)
                    except:
                        continue
            raise
    
    async def _generate_deepseek_async(self, prompt: str, temperature: float, 
                                     max_tokens: int) -> str:
        """Generate response using DeepSeek API."""
        api_key = self.api_keys.get("deepseek")
        if not api_key:
            raise ValueError("DeepSeek API key not found")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = await self.http_client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    async def _generate_anthropic_async(self, prompt: str, temperature: float,
                                      max_tokens: int) -> str:
        """Generate response using Anthropic API."""
        if not anthropic:
            raise ImportError("anthropic package not installed")
        
        api_key = self.api_keys.get("anthropic")
        if not api_key:
            raise ValueError("Anthropic API key not found")
        
        # Use async client
        async with anthropic.AsyncAnthropic(api_key=api_key) as client:
            response = await client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
    
    async def _generate_openai_async(self, prompt: str, temperature: float,
                                   max_tokens: int) -> str:
        """Generate response using OpenAI API."""
        if not openai:
            raise ImportError("openai package not installed")
        
        api_key = self.api_keys.get("openai")
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        # Configure client
        client = openai.AsyncOpenAI(api_key=api_key)
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Synchronous wrapper for generate_async."""
        return asyncio.run(self.generate_async(prompt, **kwargs))
    
    async def generate_batch_async(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate responses for multiple prompts concurrently."""
        tasks = [self.generate_async(prompt, **kwargs) for prompt in prompts]
        return await asyncio.gather(*tasks)
    
    def clear_cache(self):
        """Clear the response cache."""
        self.response_cache.clear()
    
    def get_available_providers(self) -> List[str]:
        """Get list of providers with configured API keys."""
        return [p for p, key in self.api_keys.items() if key]
    
    async def close(self):
        """Close HTTP client."""
        await self.http_client.aclose()

# Global LLM client instance
llm_client = LLMClient()

# Convenience function for backward compatibility
def set_llm_provider(provider: str):
    """Set the default LLM provider."""
    global llm_client
    llm_client.provider = provider