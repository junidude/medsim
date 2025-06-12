# MedSim Deployment Guide

## Complete Setup Instructions

### Part 1: Initialize Git Repository

1. **Initialize Git repository**
```bash
cd /Users/seungjun.lee/Documents/web
git init
```

2. **Add all files to staging**
```bash
git add .
```

3. **Make initial commit**
```bash
git commit -m "Initial commit: MedSim medical education platform"
```

### Part 2: Create GitHub Repository

4. **Create repository on GitHub**
```bash
# Using GitHub CLI (if installed)
gh repo create medsim --public --source=. --remote=origin --push

# OR manually create on GitHub.com, then:
git remote add origin https://github.com/junidude/medsim.git
```

### Part 3: Push to GitHub

5. **Push to main branch**
```bash
git branch -M main
git push -u origin main
```

### Part 4: AWS Elastic Beanstalk Setup

Before using the CI/CD pipeline, you need to:

1. **Create Elastic Beanstalk Application and Environment**
```bash
# Install EB CLI locally
pip install awsebcli

# Initialize EB application
eb init medsim-app --platform python-3.10 --region us-east-1

# Create environment
eb create medsim-env --sample --single --timeout 30
```

2. **Set Environment Variables in EB Console**
   - Go to AWS EB Console
   - Select your environment
   - Configuration → Software → Edit
   - Add environment properties:
     - `ANTHROPIC_API_KEY`: Your Anthropic API key
     - `OPENAI_API_KEY`: Your OpenAI API key (if using)
     - `DEEPSEEK_API_KEY`: Your DeepSeek API key (if using)

### Part 5: GitHub Secrets Setup

Add these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

1. **AWS_ACCESS_KEY_ID**: Your AWS access key
2. **AWS_SECRET_ACCESS_KEY**: Your AWS secret key
3. **AWS_REGION**: Your AWS region (e.g., us-east-1)

To create AWS credentials:
```bash
# Using AWS CLI
aws iam create-access-key --user-name your-iam-user

# Or create in AWS Console:
# IAM → Users → Your User → Security credentials → Create access key
```

### Part 6: Deploy

After setup, every push to main branch will automatically deploy to Elastic Beanstalk!

```bash
# Make changes
git add .
git commit -m "Update: your changes"
git push origin main
```

## Project Structure

```
medsim/
├── .github/workflows/deploy.yml  # CI/CD pipeline
├── .ebextensions/               # EB configuration
│   ├── python.config
│   ├── static-files.config
│   └── env.config
├── application.py               # EB entry point
├── api.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── Procfile                   # Process configuration
├── static/                    # Frontend files
└── cases/                     # Medical case data
```

## Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Deploy manually using EB CLI
eb deploy medsim-env

# Check deployment status
eb status

# Open application
eb open

# View logs
eb logs
```

## Troubleshooting

1. **Port Issues**: Elastic Beanstalk uses port 8000 by default
2. **Static Files**: Configured in `.ebextensions/static-files.config`
3. **Logs**: Check CloudWatch or use `eb logs`
4. **Health**: Monitor in EB console or `eb health`

## Security Notes

- Never commit `api_keys.json` (it's in .gitignore)
- Use environment variables for sensitive data
- Keep AWS credentials secure
- Use IAM roles with minimal permissions

## Monitoring

- CloudWatch Logs: `/aws/elasticbeanstalk/medsim-env/`
- Application metrics in EB console
- Set up alarms for critical metrics