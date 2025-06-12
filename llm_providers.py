#!/usr/bin/env python3
"""
LLM Provider Abstraction Layer
Supports Anthropic Claude, OpenAI GPT-4, and DeepSeek V3
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import anthropic
import openai
import requests


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                max_tokens: int = 1000, messages: Optional[List[Dict]] = None) -> str:
        """Generate text using the LLM"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider"""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                max_tokens: int = 1000, messages: Optional[List[Dict]] = None) -> str:
        """Generate text using Claude"""
        try:
            if messages:
                # Use existing message history
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system=system_prompt or "",
                    messages=messages
                )
            else:
                # Single prompt
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system=system_prompt or "You are a helpful assistant.",
                    messages=[{"role": "user", "content": prompt}]
                )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"❌ Anthropic API error: {e}")
            raise
    
    def get_provider_name(self) -> str:
        return f"Anthropic Claude ({self.model})"


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                max_tokens: int = 1000, messages: Optional[List[Dict]] = None) -> str:
        """Generate text using GPT-4"""
        try:
            if messages:
                # Convert from Anthropic format to OpenAI format
                openai_messages = []
                if system_prompt:
                    openai_messages.append({"role": "system", "content": system_prompt})
                
                for msg in messages:
                    role = "user" if msg["role"] == "user" else "assistant"
                    openai_messages.append({"role": role, "content": msg["content"]})
            else:
                # Single prompt
                openai_messages = []
                if system_prompt:
                    openai_messages.append({"role": "system", "content": system_prompt})
                openai_messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            raise
    
    def get_provider_name(self) -> str:
        return f"OpenAI ({self.model})"


class DeepSeekProvider(LLMProvider):
    """DeepSeek V3 provider"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", 
                 base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        # DeepSeek uses OpenAI-compatible API
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                max_tokens: int = 1000, messages: Optional[List[Dict]] = None) -> str:
        """Generate text using DeepSeek V3"""
        try:
            if messages:
                # Convert from Anthropic format to OpenAI format
                openai_messages = []
                if system_prompt:
                    openai_messages.append({"role": "system", "content": system_prompt})
                
                for msg in messages:
                    role = "user" if msg["role"] == "user" else "assistant"
                    openai_messages.append({"role": role, "content": msg["content"]})
            else:
                # Single prompt
                openai_messages = []
                if system_prompt:
                    openai_messages.append({"role": "system", "content": system_prompt})
                openai_messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ DeepSeek API error: {e}")
            raise
    
    def get_provider_name(self) -> str:
        return f"DeepSeek V3 ({self.model})"


class LLMFactory:
    """Factory class to create LLM providers"""
    
    @staticmethod
    def create_provider(provider_type: str, api_keys_path: str = "api_keys.json") -> LLMProvider:
        """Create an LLM provider based on type"""
        
        # Load API keys
        try:
            with open(api_keys_path, 'r') as f:
                api_keys = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"API keys file not found: {api_keys_path}")
        
        provider_type = provider_type.lower()
        
        if provider_type in ["anthropic", "claude"]:
            config = api_keys.get("anthropic", {})
            if not config.get("api_key"):
                raise ValueError("Anthropic API key not found in config")
            return AnthropicProvider(
                api_key=config["api_key"],
                model=config.get("model", "claude-3-5-sonnet-20241022")
            )
        
        elif provider_type in ["openai", "gpt4", "gpt-4"]:
            config = api_keys.get("openai", {})
            if not config.get("api_key"):
                raise ValueError("OpenAI API key not found in config")
            return OpenAIProvider(
                api_key=config["api_key"],
                model=config.get("model", "gpt-4-turbo-preview")
            )
        
        elif provider_type in ["deepseek", "deepseek-v3"]:
            config = api_keys.get("deepseek", {})
            if not config.get("api_key"):
                raise ValueError("DeepSeek API key not found in config")
            return DeepSeekProvider(
                api_key=config["api_key"],
                model=config.get("model", "deepseek-chat"),
                base_url=config.get("base_url", "https://api.deepseek.com/v1")
            )
        
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")


# Global variable to store the current provider
_current_provider: Optional[LLMProvider] = None


def set_llm_provider(provider_type: str) -> LLMProvider:
    """Set the global LLM provider"""
    global _current_provider
    _current_provider = LLMFactory.create_provider(provider_type)
    print(f"✅ LLM Provider set to: {_current_provider.get_provider_name()}")
    return _current_provider


def get_llm_provider() -> LLMProvider:
    """Get the current LLM provider"""
    global _current_provider
    if _current_provider is None:
        # Default to Anthropic
        _current_provider = LLMFactory.create_provider("anthropic")
    return _current_provider