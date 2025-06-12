#!/usr/bin/env python3
"""
Diagnostic script for MedSim API issues
"""

import os
import json
import requests
from datetime import datetime

print("=== MedSim API Diagnostics ===")
print(f"Time: {datetime.now()}")
print("")

# 1. Check if API keys are loaded
print("1. Checking API Keys:")
print("-" * 40)

# Check environment variables
env_keys = {
    "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
}

for key, value in env_keys.items():
    if value:
        print(f"✅ {key}: {'*' * 10}{value[-4:]}")
    else:
        print(f"❌ {key}: Not set in environment")

# Check api_keys.json
print("\nChecking api_keys.json:")
try:
    with open("api_keys.json", "r") as f:
        api_keys = json.load(f)
    
    for provider in ["deepseek", "anthropic", "openai"]:
        if provider in api_keys and api_keys[provider].get("api_key"):
            key = api_keys[provider]["api_key"]
            print(f"✅ {provider}: {'*' * 10}{key[-4:]}")
        else:
            print(f"❌ {provider}: Not found in api_keys.json")
except FileNotFoundError:
    print("❌ api_keys.json not found")
except Exception as e:
    print(f"❌ Error reading api_keys.json: {e}")

# 2. Test DeepSeek API directly
print("\n2. Testing DeepSeek API Directly:")
print("-" * 40)

try:
    # Get DeepSeek key
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_key and 'api_keys' in locals():
        deepseek_key = api_keys.get("deepseek", {}).get("api_key")
    
    if deepseek_key:
        print(f"Using DeepSeek key ending in: {deepseek_key[-4:]}")
        
        # Test DeepSeek API
        headers = {
            "Authorization": f"Bearer {deepseek_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API test successful' and nothing else."}
            ],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ DeepSeek API Response: {content}")
        else:
            print(f"❌ DeepSeek API Error: {response.text}")
    else:
        print("❌ No DeepSeek API key available")
        
except Exception as e:
    print(f"❌ DeepSeek test failed: {e}")

# 3. Test LLM Provider initialization
print("\n3. Testing LLM Provider Initialization:")
print("-" * 40)

try:
    from llm_providers import LLMFactory, set_llm_provider, get_llm_provider
    
    # Try to set DeepSeek
    try:
        set_llm_provider("deepseek")
        provider = get_llm_provider()
        print(f"✅ Current provider: {provider.get_provider_name()}")
        
        # Test generation
        test_response = provider.generate("Say 'test successful'", max_tokens=10)
        print(f"✅ Test generation: {test_response}")
    except Exception as e:
        print(f"❌ DeepSeek provider failed: {e}")
        
        # Try Anthropic as fallback
        try:
            set_llm_provider("anthropic")
            provider = get_llm_provider()
            print(f"⚠️  Fallback provider: {provider.get_provider_name()}")
        except Exception as e2:
            print(f"❌ Anthropic fallback also failed: {e2}")
            
except Exception as e:
    print(f"❌ LLM provider import failed: {e}")

# 4. Check session storage
print("\n4. Checking Session Storage:")
print("-" * 40)

sessions_dir = "sessions"
if os.path.exists(sessions_dir):
    session_files = list(os.listdir(sessions_dir))
    print(f"✅ Sessions directory exists")
    print(f"   Found {len(session_files)} session files")
    
    # Check recent sessions
    if session_files:
        recent_sessions = []
        for f in session_files[:5]:  # Check first 5
            try:
                with open(os.path.join(sessions_dir, f), 'r') as sf:
                    session_data = json.load(sf)
                    last_updated = session_data.get('last_updated', 'Unknown')
                    recent_sessions.append((f, last_updated))
            except:
                pass
        
        print("   Recent sessions:")
        for name, updated in recent_sessions:
            print(f"   - {name}: {updated}")
else:
    print(f"❌ Sessions directory '{sessions_dir}' not found")
    os.makedirs(sessions_dir, exist_ok=True)
    print(f"✅ Created sessions directory")

# 5. Test local API endpoints
print("\n5. Testing Local API Endpoints:")
print("-" * 40)

# Start a simple test server if needed
test_endpoints = [
    ("Health Check", "GET", "http://localhost:8000/api/health", None),
    ("Specialties", "GET", "http://localhost:8000/api/specialties", None),
    ("Create Game", "POST", "http://localhost:8000/api/game/create", {
        "role": "doctor",
        "difficulty": "medium",
        "specialty": "cardiology"
    })
]

print("Note: This requires the server to be running locally")
print("Run 'python application.py' in another terminal to test")

print("\n=== Diagnostic Summary ===")
print("If DeepSeek API is failing:")
print("1. Check if the API key is valid at https://platform.deepseek.com/")
print("2. Ensure you have credits/balance in your DeepSeek account")
print("3. The system should fallback to Anthropic if configured")
print("\nFor production (AWS):")
print("- Set API keys as environment variables in EB console")
print("- Check EB logs: eb logs --all | grep -i error")