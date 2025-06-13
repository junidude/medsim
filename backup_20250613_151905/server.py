#!/usr/bin/env python3
"""
Unified server entry point for MedSim.
Automatically detects environment and configures appropriately.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    try:
        import fastapi
        import uvicorn
        import anthropic
        import openai
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e.name}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_api_keys():
    """Check if at least one LLM API key is configured."""
    # Check environment variables
    env_keys = [
        os.getenv("DEEPSEEK_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("OPENAI_API_KEY")
    ]
    
    if any(env_keys):
        return True
    
    # Check api_keys.json
    api_keys_file = Path("api_keys.json")
    if api_keys_file.exists():
        try:
            import json
            with open(api_keys_file, 'r') as f:
                keys = json.load(f)
                if any([keys.get("deepseek"), keys.get("anthropic"), keys.get("openai")]):
                    return True
        except:
            pass
    
    print("❌ No API keys found!")
    print("\nPlease configure at least one of the following:")
    print("1. Set environment variables:")
    print("   export DEEPSEEK_API_KEY='your-key'")
    print("   export ANTHROPIC_API_KEY='your-key'")
    print("   export OPENAI_API_KEY='your-key'")
    print("\n2. Or create api_keys.json:")
    print('   {"deepseek": "your-key", "anthropic": "your-key", "openai": "your-key"}')
    return False

def run_development_server():
    """Run the development server with auto-reload."""
    import uvicorn
    from api import app
    
    print("🚀 Starting MedSim development server...")
    print("📍 URL: http://localhost:8000")
    print("📍 API docs: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

def run_production_server():
    """Run the production server."""
    import uvicorn
    from api import app
    
    # Production configuration
    port = int(os.environ.get("PORT", 8000))
    workers = int(os.environ.get("WEB_CONCURRENCY", 4))
    
    print(f"🚀 Starting MedSim production server on port {port} with {workers} workers...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        workers=workers,
        log_level="info",
        access_log=True
    )

# For AWS Elastic Beanstalk compatibility
from api import app
application = app

if __name__ == "__main__":
    # Check environment
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        # Production mode - no checks, just run
        run_production_server()
    else:
        # Development mode - run checks first
        print("🏥 MedSim - Medical Simulation Game Server")
        print("==========================================\n")
        
        # Check requirements
        if not check_requirements():
            sys.exit(1)
        
        # Check API keys
        if not check_api_keys():
            sys.exit(1)
        
        # Run development server
        run_development_server()