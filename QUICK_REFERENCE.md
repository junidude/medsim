# Quick Reference - Medical Simulation Game

## 🚀 Start the Server

```bash
# Default (Anthropic Claude)
python run_server.py

# With OpenAI GPT-4
python run_server.py --model openai

# With DeepSeek V3
python run_server.py --model deepseek

# Custom port
python run_server.py --model gpt4 --port 8080
```

## 🏥 Generate Medical Cases

```bash
# List all options
python generate_cases.py --list

# Check existing cases
python generate_cases.py --check

# Generate specific cases (5 medium cardiology cases with GPT-4)
python generate_cases.py --difficulty medium --specialty cardiovascular_disease --count 5 --model openai

# Generate 1 case for ALL specialties with Claude
python generate_cases.py --all --model anthropic

# Generate with custom delay (for rate limiting)
python generate_cases.py --all --model deepseek --delay 3
```

## 📋 Common Specialties

- `emergency_medicine` - Emergency Medicine
- `cardiovascular_disease` - Cardiology
- `internal_medicine` - Internal Medicine
- `pediatrics` - Pediatrics
- `psychiatry` - Psychiatry
- `oncology` - Oncology
- `neurology` - Neurology
- `orthopedic_surgery` - Orthopedic Surgery

## 🎯 Difficulties

- `easy` - Common conditions
- `medium` - Moderate complexity
- `hard` - Complex conditions
- `expert` - Rare diseases

## 🔑 API Configuration

Create `api_keys.json`:
```json
{
  "anthropic": {"api_key": "sk-ant-..."},
  "openai": {"api_key": "sk-proj-..."},
  "deepseek": {"api_key": "sk-..."}
}
```

## 🌐 Access Points

- Web Interface: http://localhost:8000/static/index.html
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health