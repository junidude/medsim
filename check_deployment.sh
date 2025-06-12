#!/bin/bash
# Script to check MedSim deployment status

echo "=== MedSim Deployment Status Check ==="
echo ""

# Method 1: Check GitHub Actions status
echo "📋 Method 1: GitHub Actions Status"
echo "-----------------------------------"
echo "Checking latest workflow run..."
gh run list --repo junidude/medsim --limit 5

echo ""
echo "To see detailed logs of the latest run:"
echo "gh run view --repo junidude/medsim"
echo ""

# Method 2: Check Elastic Beanstalk status (if eb is configured)
if command -v eb &> /dev/null; then
    echo "📋 Method 2: Elastic Beanstalk Status"
    echo "-------------------------------------"
    
    # Check if .elasticbeanstalk exists
    if [ -d ".elasticbeanstalk" ]; then
        echo "Checking EB environment health..."
        eb status
        echo ""
        echo "Environment Health:"
        eb health
    else
        echo "❌ EB not initialized in this directory"
        echo "Run: eb init medsim-app --platform python-3.11 --region us-east-1"
    fi
else
    echo "❌ EB CLI not installed. Install with: pip install awsebcli"
fi

echo ""
echo "📋 Other ways to check:"
echo "----------------------"
echo "1. GitHub Actions: https://github.com/junidude/medsim/actions"
echo "2. AWS Console: https://console.aws.amazon.com/elasticbeanstalk"
echo "3. Application URL: (will be shown in EB status output)"
echo ""
echo "📝 Useful commands:"
echo "- View EB logs: eb logs"
echo "- Open app in browser: eb open"
echo "- SSH to instance: eb ssh"