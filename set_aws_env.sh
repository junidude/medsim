#!/bin/bash
# Script to set environment variables in AWS Elastic Beanstalk

echo "=== Setting AWS Environment Variables ==="
echo ""

# Check if EB CLI is configured
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI not found. Install with: pip install awsebcli"
    exit 1
fi

# Check current environment
echo "Current environment status:"
eb status | grep -E "Environment:|CNAME:|Status:|Health:"
echo ""

# Set the environment variables
echo "Setting API keys as environment variables..."
echo "This will trigger a environment update (takes 2-3 minutes)"
echo ""

# Read API keys from api_keys.json
if [ -f "api_keys.json" ]; then
    DEEPSEEK_KEY=$(python -c "import json; print(json.load(open('api_keys.json'))['deepseek']['api_key'])" 2>/dev/null)
    ANTHROPIC_KEY=$(python -c "import json; print(json.load(open('api_keys.json'))['anthropic']['api_key'])" 2>/dev/null)
    OPENAI_KEY=$(python -c "import json; print(json.load(open('api_keys.json'))['openai']['api_key'])" 2>/dev/null)
    
    if [ -z "$DEEPSEEK_KEY" ] || [ -z "$ANTHROPIC_KEY" ]; then
        echo "❌ Could not read API keys from api_keys.json"
        exit 1
    fi
    
    echo "Found API keys:"
    echo "- DeepSeek: ****${DEEPSEEK_KEY: -4}"
    echo "- Anthropic: ****${ANTHROPIC_KEY: -4}"
    echo "- OpenAI: ****${OPENAI_KEY: -4}"
    echo ""
    
    # Set environment variables
    eb setenv \
        DEEPSEEK_API_KEY="$DEEPSEEK_KEY" \
        ANTHROPIC_API_KEY="$ANTHROPIC_KEY" \
        OPENAI_API_KEY="$OPENAI_KEY" \
        ENVIRONMENT="production"
    
    echo ""
    echo "✅ Environment variables set!"
    echo ""
    echo "Monitor the update:"
    echo "- Watch status: eb status"
    echo "- View logs: eb logs"
    echo "- Open app: eb open"
    
else
    echo "❌ api_keys.json not found"
    echo ""
    echo "Manually set environment variables with:"
    echo "eb setenv DEEPSEEK_API_KEY=your-key ANTHROPIC_API_KEY=your-key"
fi