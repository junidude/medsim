#!/usr/bin/env python3
"""
MedSim Server Launcher
Launches the medical simulation game server with proper configuration.
Supports multiple LLM providers: Anthropic, OpenAI, and DeepSeek.
"""

import os
import sys
import uvicorn
import argparse
from pathlib import Path
from llm_providers import set_llm_provider

def check_requirements():
    """Check if required packages are installed."""
    required_packages = []
    
    try:
        import fastapi
        required_packages.append("fastapi")
    except ImportError:
        pass
    
    try:
        import anthropic
        required_packages.append("anthropic")
    except ImportError:
        pass
    
    try:
        import openai
        required_packages.append("openai")
    except ImportError:
        pass
    
    if len(required_packages) < 3:
        print("❌ Missing required packages")
        print("Please install: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_api_keys():
    """Check if API keys are configured."""
    api_keys_path = Path("api_keys.json")
    
    if api_keys_path.exists():
        print("✅ API keys file found (api_keys.json)")
        return True
    
    # Fallback to environment variable for backward compatibility
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✅ Using ANTHROPIC_API_KEY from environment")
        return True
    
    print("❌ No API keys configured")
    print("Please create api_keys.json with your API keys or set ANTHROPIC_API_KEY")
    return False

def main():
    """Main function to start the server."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="MedSim Server - Medical Education Game")
    parser.add_argument(
        "--model", 
        type=str, 
        choices=["anthropic", "claude", "openai", "gpt4", "gpt-4", "deepseek", "deepseek-v3"],
        default="anthropic",
        help="LLM provider to use (default: anthropic)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )
    
    args = parser.parse_args()
    
    print("🏥 MedSim - Medical Education Game")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    if not check_api_keys():
        sys.exit(1)
    
    # Set the LLM provider
    try:
        provider = set_llm_provider(args.model)
        print(f"🤖 Using LLM: {provider.get_provider_name()}")
    except Exception as e:
        print(f"❌ Failed to set LLM provider: {e}")
        sys.exit(1)
    
    # Ensure static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        print(f"❌ Static directory not found: {static_dir}")
        print("Please ensure you're running from the correct directory")
        sys.exit(1)
    
    print("🚀 Starting MedSim server...")
    print(f"📱 Web interface: http://localhost:{args.port}/static/index.html")
    print(f"📚 API docs: http://localhost:{args.port}/docs")
    print(f"🔍 API health: http://localhost:{args.port}/api/health")
    print("-" * 50)
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the server
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=args.port,
            reload=True,
            reload_dirs=[".", "static"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()