# MedSim Project Guidelines and Memory

This document contains the accumulated knowledge and rules for the MedSim medical education platform.

---

## Project Overview

MedSim is an AI-powered medical education platform with two modes:
- **Doctor Mode**: Practice diagnosing 400+ medical cases across 51 specialties
- **Patient Mode**: Practice patient communication and history-taking skills

### Tech Stack
- **Backend**: FastAPI with Python 3.11
- **Frontend**: Vanilla JavaScript with modern ES6+
- **LLM Providers**: DeepSeek (primary), Anthropic Claude, OpenAI GPT-4
- **Deployment**: AWS Elastic Beanstalk with GitHub Actions CI/CD
- **Session Storage**: File-based persistence with automatic cleanup

---

## Development Guidelines

### Code Style
- Use consistent indentation (follow existing patterns in each file)
- Add meaningful comments only when necessary to explain complex logic
- Follow the existing naming conventions in the codebase
- Keep functions focused and single-purpose
- NO COMMENTS unless explicitly requested

### API and Session Management
- **Retry Mechanism**: All API calls automatically retry up to 10 times for session errors
- **Timeouts**: 
  - Chat messages: 60 seconds
  - Show Answer/Multiple Choice: 30 seconds
  - Physical Exam/Lab Tests: 40 seconds
  - Session creation: 60 seconds
- **Session Persistence**: Sessions are saved to disk and survive server restarts
- **Error Handling**: Retry silently without showing attempt counts to users

### UI/UX Rules
- Keep loading states simple - no attempt counters or progress details
- Show only essential information during loading/processing
- Implement retry mechanisms silently in the background
- Use loading spinners without additional text
- Error messages only after all retries are exhausted

### LLM Provider Configuration
- **Default Provider**: DeepSeek (best cost/performance ratio)
- **Fallback Order**: DeepSeek → Anthropic → OpenAI
- **Environment Variables Required**:
  - `DEEPSEEK_API_KEY`
  - `ANTHROPIC_API_KEY` (optional)
  - `OPENAI_API_KEY` (optional)

### Patient Mode Special Rules
- "Any Specialty" option randomly selects from 51 valid specialties
- Patient sessions require both creation and setup steps
- Add 500ms delay between session creation and setup
- Handle empty specialty string as "any specialty"

### Security and API Keys
- **NEVER** commit API keys to version control
- Use environment variables in production
- Use `api_keys.json` for local development only
- All API key files are in `.gitignore`

### Deployment Process
1. Push to `main` branch triggers automatic deployment
2. GitHub Actions deploys to AWS Elastic Beanstalk
3. Environment variables must be set in EB console
4. Deployment takes ~2 minutes

### Error Handling Patterns
```python
# Always use this pattern for session operations
try:
    game_state = self._get_session(session_id)
except KeyError:
    # Wait and retry once
    time.sleep(0.5)
    game_state = self._get_session(session_id)
```

### Session Storage
- Sessions stored in `sessions/` directory
- Automatic cleanup after 24 hours
- Atomic writes using temporary files
- Thread-safe operations with locks

---

## Common Issues and Solutions

### "Game session not found" Error
1. Increased timeouts to 60 seconds
2. Added retry logic with exponential backoff
3. Sessions persist to disk between requests
4. 10 automatic retries before showing error

### "Any Specialty" in Patient Mode
- Backend randomly selects from 51 specialties
- Empty string is treated as "any specialty"
- Selected specialty shown in UI

### 502 Bad Gateway
- Usually caused by Python syntax errors
- Check indentation in modified files
- Review deployment logs

---

## Testing and Debugging

### API Health Check
```
GET /api/health
```
Shows:
- LLM provider status
- API keys configured
- Active sessions count
- Environment (development/production)

### Session Validation
```
GET /api/session/{session_id}/validate
```
Checks if session exists in memory or storage

### Debug Page
```
/static/debug.html
```
Tests all API endpoints and shows results

---

## Important Files

- `api.py` - Main FastAPI application
- `core_medical_game.py` - Game engine logic
- `llm_providers.py` - Multi-LLM abstraction
- `session_store.py` - Session persistence
- `static/app.js` - Frontend application
- `cases/` - 400+ medical cases

---

## Deployment Checklist

1. ✅ No API keys in code
2. ✅ All tests passing
3. ✅ Session persistence working
4. ✅ Retry logic implemented
5. ✅ Timeouts appropriate for LLM calls
6. ✅ Error messages user-friendly
7. ✅ Loading states clean and simple

---

## Contact

- **GitHub**: https://github.com/junidude/medsim
- **Live App**: http://medsim-env.eba-jsd4bbrm.us-east-1.elasticbeanstalk.com
- **Support**: junidude14@gmail.com