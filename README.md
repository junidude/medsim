# MedSim - AI-Powered Medical Education Platform

[![Deploy to AWS](https://github.com/junidude/medsim/actions/workflows/deploy.yml/badge.svg)](https://github.com/junidude/medsim/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MedSim is an advanced medical education platform that uses AI to create realistic clinical scenarios for medical students and healthcare professionals. It offers two distinct modes: Doctor Mode for diagnostic practice and Patient Mode for communication training.

## 🎯 Features

### Doctor Mode
- **Clinical Case Simulations**: Practice with 400+ real clinical cases across 51 medical specialties
- **Difficulty Levels**: Easy, Medium, Hard, and Expert cases
- **Interactive Diagnostics**: Order physical exams, lab tests, and make diagnoses
- **AI Feedback**: Get detailed explanations and differential diagnoses
- **Multiple Choice Support**: Practice with board-style questions

### Patient Mode
- **Realistic Patient Interactions**: AI-powered patients with authentic medical histories
- **Communication Skills**: Practice taking patient histories and explaining diagnoses
- **Customizable Scenarios**: Set patient age, gender, and chief complaints
- **Conversation Logging**: Review your patient interactions for improvement

### Technical Features
- **Multi-LLM Support**: DeepSeek, Anthropic Claude, and OpenAI GPT-4
- **Session Persistence**: Continue where you left off
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Fast Performance**: Optimized API with smart caching

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+ (for local development)
- API keys for at least one LLM provider (DeepSeek recommended)

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/junidude/medsim.git
cd medsim
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API keys**
Create an `api_keys.json` file:
```json
{
  "deepseek": {
    "api_key": "your-deepseek-api-key",
    "model": "deepseek-chat"
  },
  "anthropic": {
    "api_key": "your-anthropic-api-key",
    "model": "claude-3-5-sonnet-20241022"
  },
  "openai": {
    "api_key": "your-openai-api-key",
    "model": "gpt-4-turbo-preview"
  }
}
```

4. **Run the application**
```bash
python application.py
```

5. **Access the app**
Open http://localhost:8000 in your browser

## 🌐 Production Deployment (AWS Elastic Beanstalk)

### Initial Setup

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB application**
```bash
eb init medsim-app --platform python-3.11 --region us-east-1
```

3. **Create environment**
```bash
eb create medsim-env --sample --single --timeout 30
```

4. **Set environment variables**
```bash
eb setenv DEEPSEEK_API_KEY=your-key \
         ANTHROPIC_API_KEY=your-key \
         OPENAI_API_KEY=your-key
```

5. **Deploy**
```bash
eb deploy
```

### Continuous Deployment

The project includes GitHub Actions for automatic deployment:
- Push to `main` branch triggers deployment
- Add AWS credentials as GitHub secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`

## 📁 Project Structure

```
medsim/
├── api.py                    # FastAPI backend server
├── application.py            # Entry point for AWS EB
├── core_medical_game.py      # Game engine logic
├── llm_providers.py          # Multi-LLM abstraction layer
├── case_manager.py           # Medical case management
├── session_store.py          # Session persistence
├── patient_interaction_logger.py  # Patient mode logging
├── static/                   # Frontend files
│   ├── index.html           # Main HTML
│   ├── app.js               # JavaScript application
│   └── styles.css           # Styling
├── cases/                    # Medical case library (400+ cases)
├── requirements.txt          # Python dependencies
└── .github/workflows/        # CI/CD configuration
```

## 🔧 Configuration

### Environment Variables
- `DEEPSEEK_API_KEY`: DeepSeek API key (recommended)
- `ANTHROPIC_API_KEY`: Anthropic Claude API key
- `OPENAI_API_KEY`: OpenAI API key
- `ENVIRONMENT`: Set to "production" for AWS deployment
- `PORT`: Server port (default: 8000)

### LLM Provider Selection
The system automatically selects providers in this order:
1. DeepSeek (lowest cost, good performance)
2. Anthropic Claude (fallback)
3. OpenAI GPT-4 (optional)

## 📊 API Endpoints

### Health & Status
- `GET /api/health` - System health check with LLM status
- `GET /api/specialties` - Available medical specialties
- `GET /api/difficulties` - Difficulty levels

### Game Management
- `POST /api/game/create` - Create new game session
- `POST /api/game/message` - Send message to AI
- `POST /api/game/diagnose` - Submit diagnosis
- `POST /api/game/physical-exam` - Request physical exam
- `POST /api/game/lab-tests` - Order lab tests
- `POST /api/game/show-answer` - Reveal correct diagnosis
- `POST /api/game/show-multiple-choice` - Get multiple choice options

### Patient Mode
- `POST /api/game/setup-patient` - Configure patient scenario
- `POST /api/game/end-session` - End and save session

## 🧪 Testing

### Run diagnostic script
```bash
python scripts/diagnose_api.py
```

### Check deployment
```bash
eb status
eb health
eb logs
```

## 📝 Case Management

### Adding New Cases
1. Create JSON file in `cases/difficulty/specialty/` directory
2. Follow the case format:
```json
{
  "name": "Case Name",
  "description": "Brief description",
  "specialty": "cardiology",
  "difficulty": "medium",
  "patient": {
    "age": 45,
    "gender": "male",
    "chief_complaint": "Chest pain"
  },
  "diagnosis": "Myocardial Infarction",
  "multiple_choice": [
    "Myocardial Infarction",
    "Angina Pectoris",
    "Pulmonary Embolism",
    "Aortic Dissection"
  ]
}
```

### Bulk Case Updates
Use the provided scripts:
```bash
python scripts/add_ddx_to_cases.py --model deepseek
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Medical cases inspired by real clinical scenarios
- UI design inspired by OpenEvidence
- Built with FastAPI, Anthropic Claude, and modern web technologies

## 📞 Support

- Issues: [GitHub Issues](https://github.com/junidude/medsim/issues)
- Documentation: See `/docs` folder
- Email: support@medsim.app

---

**Note**: This is an educational tool and should not be used for actual medical diagnosis or treatment.