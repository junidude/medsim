#!/bin/bash
# Script to add GitHub secrets for AWS deployment

echo "=== GitHub Secrets Setup for MedSim ==="
echo ""

# Check if we're in the right directory
if [ ! -f "api.py" ]; then
    echo "❌ Error: Not in the MedSim project directory"
    echo "Please run this script from /Users/seungjun.lee/Documents/web"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ GitHub CLI not authenticated. Running 'gh auth login'..."
    gh auth login
fi

echo "📋 This script will add AWS credentials as GitHub secrets"
echo ""

# Option 1: Use existing AWS credentials
if [ -f ~/.aws/credentials ]; then
    echo "Found AWS credentials file. Would you like to use these? (y/n)"
    read -r use_existing
    
    if [ "$use_existing" = "y" ]; then
        # Extract credentials from AWS config
        AWS_ACCESS_KEY_ID=$(grep -A2 '\[default\]' ~/.aws/credentials | grep aws_access_key_id | cut -d= -f2 | tr -d ' ')
        AWS_SECRET_ACCESS_KEY=$(grep -A2 '\[default\]' ~/.aws/credentials | grep aws_secret_access_key | cut -d= -f2 | tr -d ' ')
        
        if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
            echo "❌ Could not extract credentials from ~/.aws/credentials"
            echo "Please enter them manually."
        else
            echo "✅ Found AWS credentials"
        fi
    fi
fi

# Option 2: Manual entry
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "Enter your AWS Access Key ID:"
    read -r AWS_ACCESS_KEY_ID
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Enter your AWS Secret Access Key:"
    read -rs AWS_SECRET_ACCESS_KEY
    echo ""
fi

# Set default region
echo "Enter AWS Region (press Enter for default: us-east-1):"
read -r AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

echo ""
echo "📝 Adding secrets to GitHub repository..."

# Add secrets using gh CLI
gh secret set AWS_ACCESS_KEY_ID --body "$AWS_ACCESS_KEY_ID" --repo junidude/medsim
gh secret set AWS_SECRET_ACCESS_KEY --body "$AWS_SECRET_ACCESS_KEY" --repo junidude/medsim
gh secret set AWS_REGION --body "$AWS_REGION" --repo junidude/medsim

echo ""
echo "✅ GitHub secrets added successfully!"
echo ""
echo "🚀 You can now:"
echo "1. Go to https://github.com/junidude/medsim/actions"
echo "2. Click on the failed workflow"
echo "3. Click 'Re-run all jobs'"
echo ""
echo "Or trigger a new deployment with:"
echo "git commit --allow-empty -m 'Trigger deployment' && git push"