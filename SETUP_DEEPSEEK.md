# Setting Up DeepSeek API for MedSim

## Overview
MedSim now uses DeepSeek API for AI conversations by default. DeepSeek offers excellent performance at a lower cost compared to other providers.

## Configuration Steps

### 1. Get Your DeepSeek API Key
If you don't have one already:
1. Go to https://platform.deepseek.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key

### 2. Add DeepSeek API Key to AWS Elastic Beanstalk

#### Option A: Using AWS Console (Recommended)
1. Go to AWS Elastic Beanstalk console
2. Select your environment: `medsim-env`
3. Click "Configuration" in the left sidebar
4. Find "Software" section and click "Edit"
5. Scroll to "Environment properties"
6. Add these key-value pairs:
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key (e.g., sk-xxxxx)
   - `ANTHROPIC_API_KEY`: Your Anthropic API key (for fallback)
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)
7. Click "Apply"
8. Wait for environment to update (takes 2-3 minutes)

#### Option B: Using EB CLI
```bash
# Set environment variables
eb setenv DEEPSEEK_API_KEY=sk-your-deepseek-key-here \
          ANTHROPIC_API_KEY=sk-your-anthropic-key-here \
          OPENAI_API_KEY=sk-your-openai-key-here
```

### 3. Verify Configuration
After deployment completes:
1. Visit your app: http://medsim-env.eba-jsd4bbrm.us-east-1.elasticbeanstalk.com/
2. Start a patient mode conversation
3. Check the server logs to confirm DeepSeek is being used:
   ```bash
   eb logs --all
   ```
   Look for: "✅ Using DeepSeek for AI conversations"

## Switching Between LLM Providers

The API now automatically uses DeepSeek by default. If you want to change providers:

1. **To use Anthropic Claude**: Remove DEEPSEEK_API_KEY from environment
2. **To use OpenAI GPT-4**: Modify `api.py` to use `set_llm_provider("openai")`

## Cost Comparison

- **DeepSeek**: ~$0.14 per 1M input tokens, $0.28 per 1M output tokens
- **Claude 3.5**: ~$3 per 1M input tokens, $15 per 1M output tokens
- **GPT-4 Turbo**: ~$10 per 1M input tokens, $30 per 1M output tokens

DeepSeek offers significant cost savings while maintaining high quality responses.

## Troubleshooting

### If DeepSeek fails to initialize:
1. Check that DEEPSEEK_API_KEY is set correctly
2. Verify the API key is valid
3. The system will automatically fall back to Anthropic if available

### To check which provider is active:
```bash
eb ssh
cd /var/app/current
python -c "from llm_providers import get_llm_provider; print(get_llm_provider().get_provider_name())"
```

## Local Development

For local testing, update your `api_keys.json`:
```json
{
  "deepseek": {
    "api_key": "sk-your-deepseek-key",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
  }
}
```