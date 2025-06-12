# Medical Case Generation Guide

This guide explains how to generate medical cases using different LLM providers (Anthropic Claude, OpenAI GPT-4, and DeepSeek V3).

## Prerequisites

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys** in `api_keys.json`:
   ```json
   {
     "anthropic": {"api_key": "your-key"},
     "openai": {"api_key": "your-key"},
     "deepseek": {"api_key": "your-key"}
   }
   ```

## Basic Commands

### 1. List Available Options

See all available difficulties and specialties:
```bash
python generate_cases.py --list
```

### 2. Check Existing Cases

View what cases already exist:
```bash
python generate_cases.py --check
```

### 3. Generate Specific Cases

Generate cases for a specific specialty and difficulty:

**Using Anthropic Claude (default):**
```bash
python generate_cases.py --difficulty medium --specialty cardiology --count 5
```

**Using OpenAI GPT-4:**
```bash
python generate_cases.py --difficulty medium --specialty cardiology --count 5 --model openai
```

**Using DeepSeek V3:**
```bash
python generate_cases.py --difficulty medium --specialty cardiology --count 5 --model deepseek
```

### 4. Generate Cases for All Specialties

Generate 1 case for each difficulty/specialty combination:

**Using Anthropic Claude:**
```bash
python generate_cases.py --all --model anthropic
```

**Using OpenAI GPT-4:**
```bash
python generate_cases.py --all --model openai
```

**Using DeepSeek V3:**
```bash
python generate_cases.py --all --model deepseek
```

### 5. Advanced Options

**Custom delay between API calls** (useful for rate limiting):
```bash
python generate_cases.py --all --model openai --delay 3
```

**Generate multiple cases per combination:**
```bash
python generate_cases.py --all --model anthropic --count 2
```

## Examples by Use Case

### Generate Emergency Medicine Cases
```bash
# 10 emergency cases of varying difficulty using GPT-4
python generate_cases.py --difficulty hard --specialty emergency_medicine --count 10 --model gpt4
```

### Generate Pediatric Cases
```bash
# 5 easy pediatric cases using Claude
python generate_cases.py --difficulty easy --specialty pediatrics --count 5 --model claude
```

### Generate Cardiology Cases
```bash
# 3 expert cardiology cases using DeepSeek
python generate_cases.py --difficulty expert --specialty cardiovascular_disease --count 3 --model deepseek
```

### Batch Generation for Research
```bash
# Generate 1 case for every specialty at medium difficulty using GPT-4
for specialty in $(python generate_cases.py --list | grep -A 100 "Specialties:" | grep "  -" | awk '{print $2}'); do
    python generate_cases.py --difficulty medium --specialty $specialty --count 1 --model openai
    sleep 2  # Additional delay between specialties
done
```

## Available Specialties

Run `python generate_cases.py --list` to see all 51 available specialties, including:
- Primary Care: family_medicine, internal_medicine, pediatrics, obstetrics_gynecology
- Surgical: general_surgery, orthopedic_surgery, neurological_surgery, etc.
- Medical: emergency_medicine, cardiology, neurology, psychiatry, etc.
- Subspecialties: cardiovascular_disease, oncology, critical_care_medicine, etc.

## Available Difficulties
- `easy`: Common conditions, straightforward diagnoses
- `medium`: Moderate complexity, typical presentations
- `hard`: Complex conditions, differential diagnoses required
- `expert`: Rare diseases, challenging presentations

## Rate Limiting

Different providers have different rate limits:
- **Anthropic Claude**: ~50 requests/minute
- **OpenAI GPT-4**: ~60 requests/minute  
- **DeepSeek V3**: ~100 requests/minute

Use the `--delay` parameter to avoid hitting rate limits:
```bash
python generate_cases.py --all --model openai --delay 3  # 3 seconds between requests
```

## Output

Generated cases are saved to:
```
cases/
├── easy/
│   ├── family_medicine/
│   ├── cardiology/
│   └── ...
├── medium/
├── hard/
└── expert/
```

Each case is saved as a JSON file with a unique ID.

## Troubleshooting

1. **API Key Errors**: Ensure `api_keys.json` exists and contains valid keys
2. **Rate Limit Errors**: Increase the `--delay` parameter
3. **Invalid Specialty**: Use `--list` to see valid specialty names
4. **Connection Errors**: Check your internet connection and API endpoint status

## Provider Comparison

- **Anthropic Claude**: Best for complex medical reasoning and nuanced cases
- **OpenAI GPT-4**: Fast generation with good general medical knowledge
- **DeepSeek V3**: Cost-effective for bulk generation of standard cases