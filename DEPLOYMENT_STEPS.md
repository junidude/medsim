# MedSim Deployment Steps

## 1. Push to GitHub
```bash
git push origin main
```

## 2. Add GitHub Secrets
Go to your GitHub repository settings:
1. Navigate to Settings → Secrets and variables → Actions
2. Add these secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `AWS_REGION`: us-east-1 (optional, defaults to us-east-1)

## 3. Initialize Elastic Beanstalk (if not done)
```bash
eb init medsim-app --platform python-3.11 --region us-east-1
```

## 4. Create EB Environment (if not exists)
```bash
eb create medsim-env --sample --single --timeout 30
```

## 5. Configure Environment Variables in AWS
1. Go to AWS Elastic Beanstalk console
2. Select your application and environment
3. Go to Configuration → Software → Environment properties
4. Add:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key (optional)
   - `ADSENSE_CLIENT_ID`: Your Google AdSense client ID (optional, format: ca-pub-XXXXXXXXXXXXXXXX)
   - `ADSENSE_SLOT_ID`: Your AdSense ad slot ID (optional, or use "auto")

## 6. Trigger Deployment
Once GitHub secrets are configured, the deployment will trigger automatically on push to main branch.

## Troubleshooting

### If GitHub Actions fails:
1. Check the Actions tab in your GitHub repository
2. Look for error messages in the failed workflow run
3. Common issues:
   - Missing AWS credentials secrets
   - Wrong AWS region
   - EB environment not created

### If EB deployment fails:
1. Check EB logs: `eb logs`
2. Check health: `eb health`
3. SSH into instance: `eb ssh` (if enabled)

### Important Security Note
**You need to regenerate your Anthropic API key** since it was exposed in the Git history. 
1. Go to the Anthropic console
2. Revoke the old key
3. Generate a new one
4. Update it in your local `api_keys.json` and AWS EB environment variables