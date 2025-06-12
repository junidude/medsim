#!/bin/bash
# MedSim Deployment Commands
# Execute these commands step by step

echo "===== MedSim Git & GitHub Setup ====="
echo ""
echo "Step 1: Initialize Git Repository"
echo "================================="
cd /Users/seungjun.lee/Documents/web
git init

echo ""
echo "Step 2: Add all files to staging"
echo "================================"
git add .

echo ""
echo "Step 3: Make initial commit"
echo "==========================="
git commit -m "Initial commit: MedSim medical education platform"

echo ""
echo "Step 4: Create GitHub repository"
echo "================================"
echo "Option A - Using GitHub CLI:"
echo "gh repo create medsim --public --source=. --remote=origin --push"
echo ""
echo "Option B - Manual method:"
echo "1. Go to https://github.com/new"
echo "2. Create repository named 'medsim'"
echo "3. Then run:"
echo "git remote add origin https://github.com/junidude/medsim.git"

echo ""
echo "Step 5: Push to GitHub"
echo "======================"
git branch -M main
git push -u origin main

echo ""
echo "===== AWS Elastic Beanstalk Setup ====="
echo ""
echo "Step 6: Install EB CLI (if not installed)"
echo "========================================="
echo "pip install awsebcli"

echo ""
echo "Step 7: Initialize EB Application"
echo "================================="
echo "eb init medsim-app --platform python-3.10 --region us-east-1"

echo ""
echo "Step 8: Create EB Environment"
echo "============================="
echo "eb create medsim-env --sample --single --timeout 30"

echo ""
echo "===== GitHub Secrets Configuration ====="
echo ""
echo "Add these secrets in GitHub repository settings:"
echo "1. AWS_ACCESS_KEY_ID"
echo "2. AWS_SECRET_ACCESS_KEY" 
echo "3. AWS_REGION"

echo ""
echo "===== Environment Variables in EB ====="
echo ""
echo "Add these in AWS EB Console → Configuration → Software:"
echo "- ANTHROPIC_API_KEY"
echo "- OPENAI_API_KEY (optional)"
echo "- DEEPSEEK_API_KEY (optional)"

echo ""
echo "===== Deployment Complete! ====="
echo "Every push to main will now auto-deploy!"