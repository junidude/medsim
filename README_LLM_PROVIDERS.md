# LLM Provider Support

The Medical Simulation Game now supports multiple LLM providers:

1. **Anthropic Claude 3.5 Sonnet** (default)
2. **OpenAI GPT-4 Turbo**
3. **DeepSeek V3**

## Configuration

API keys are stored in `api_keys.json`:

```json
{
  "anthropic": {
    "api_key": "your-anthropic-key",
    "model": "claude-3-5-sonnet-20241022"
  },
  "openai": {
    "api_key": "your-openai-key",
    "model": "gpt-4-turbo-preview"
  },
  "deepseek": {
    "api_key": "your-deepseek-key",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
  }
}
```

## Running the Server

### Default (Anthropic Claude):
```bash
python run_server.py
```

### With OpenAI GPT-4:
```bash
python run_server.py --model openai
# or
python run_server.py --model gpt4
```

### With DeepSeek V3:
```bash
python run_server.py --model deepseek
```

### Custom Port:
```bash
python run_server.py --model openai --port 8080
```

## Testing Providers

To test all configured providers:

```bash
python test_llm_providers.py
```

## Backward Compatibility

The system maintains backward compatibility:
- If `ANTHROPIC_API_KEY` environment variable is set, it will be used
- If no `api_keys.json` exists, the system will look for `ANTHROPIC_API_KEY`

## Provider Features

### Anthropic Claude 3.5 Sonnet
- Best for: Complex medical reasoning, nuanced patient interactions
- Strengths: Deep understanding, context awareness, medical knowledge
- Model: claude-3-5-sonnet-20241022

### OpenAI GPT-4 Turbo
- Best for: Fast responses, general medical knowledge
- Strengths: Speed, broad knowledge base, consistent formatting
- Model: gpt-4-turbo-preview

### DeepSeek V3
- Best for: Cost-effective operations, standard medical scenarios
- Strengths: Good performance/cost ratio, reliable responses
- Model: deepseek-chat

## Implementation Details

The LLM abstraction is implemented in `llm_providers.py`:
- `LLMProvider`: Abstract base class
- `AnthropicProvider`: Anthropic Claude implementation
- `OpenAIProvider`: OpenAI GPT implementation  
- `DeepSeekProvider`: DeepSeek implementation
- `LLMFactory`: Factory for creating providers

The game engine (`core_medical_game.py`) automatically uses the selected provider.