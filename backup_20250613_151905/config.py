"""
Configuration management for MedSim application
Handles environment variables for both local and production environments
"""

import os
import json
from pathlib import Path
from typing import Optional

class Config:
    """Application configuration"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.port = int(os.getenv("PORT", 8000))
        
        # Try to load API keys from environment first, then from file
        self.anthropic_api_key = self._get_api_key("ANTHROPIC_API_KEY", "anthropic")
        self.openai_api_key = self._get_api_key("OPENAI_API_KEY", "openai")
        self.deepseek_api_key = self._get_api_key("DEEPSEEK_API_KEY", "deepseek")
        
        # AWS settings
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        # Google AdSense settings
        self.adsense_client_id = os.getenv("ADSENSE_CLIENT_ID", "")
        self.adsense_slot_id = os.getenv("ADSENSE_SLOT_ID", "")
        
    def _get_api_key(self, env_name: str, key_name: str) -> Optional[str]:
        """Get API key from environment or api_keys.json file"""
        # First try environment variable
        key = os.getenv(env_name)
        if key:
            return key
            
        # Then try api_keys.json file (for local development)
        if self.environment == "development":
            api_keys_file = Path("api_keys.json")
            if api_keys_file.exists():
                try:
                    with open(api_keys_file, 'r') as f:
                        keys = json.load(f)
                        return keys.get(key_name)
                except Exception:
                    pass
                    
        return None
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"
    
    def get_llm_provider_key(self, provider: str) -> Optional[str]:
        """Get API key for specific LLM provider"""
        provider_map = {
            "anthropic": self.anthropic_api_key,
            "claude": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "gpt4": self.openai_api_key,
            "gpt-4": self.openai_api_key,
            "deepseek": self.deepseek_api_key,
            "deepseek-v3": self.deepseek_api_key
        }
        return provider_map.get(provider.lower())

# Global config instance
config = Config()