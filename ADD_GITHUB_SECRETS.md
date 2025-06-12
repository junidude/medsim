# How to Add GitHub Secrets for AWS Deployment

## Step 1: Get Your AWS Credentials

### Option A: If you already have AWS CLI configured
```bash
cat ~/.aws/credentials
```
Look for:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_HERE
aws_secret_access_key = YOUR_SECRET_KEY_HERE
```

### Option B: Create new AWS credentials
1. Go to AWS Console: https://console.aws.amazon.com/
2. Click your username (top right) → Security credentials
3. Scroll to "Access keys" → "Create access key"
4. Select "Command Line Interface (CLI)"
5. Save both the Access Key ID and Secret Access Key

## Step 2: Add Secrets to GitHub

1. Go to your repository: https://github.com/junidude/medsim
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

Add these three secrets:

### Secret 1: AWS_ACCESS_KEY_ID
- Name: `AWS_ACCESS_KEY_ID`
- Secret: (paste your AWS access key ID)
- Click "Add secret"

### Secret 2: AWS_SECRET_ACCESS_KEY
- Name: `AWS_SECRET_ACCESS_KEY`
- Secret: (paste your AWS secret access key)
- Click "Add secret"

### Secret 3: AWS_REGION (Optional)
- Name: `AWS_REGION`
- Secret: `us-east-1`
- Click "Add secret"

## Step 3: Verify Secrets
After adding, you should see:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION (optional)

Listed under "Repository secrets"

## Step 4: Re-run the Workflow
1. Go to the **Actions** tab
2. Click on the failed workflow run
3. Click **Re-run all jobs**

## Alternative: Manual Deployment
If you prefer to deploy manually first:

```bash
# Make sure EB CLI is installed
pip install awsebcli

# Configure AWS credentials locally
aws configure

# Initialize EB
eb init medsim-app --platform python-3.11 --region us-east-1

# Create environment
eb create medsim-env --sample --single --timeout 30

# Deploy
eb deploy
```

Then the GitHub Actions will handle future deployments automatically.