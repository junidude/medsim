# 🏥 MedSim - Medical Education Game

An AI-powered medical simulation game for educational purposes, featuring realistic doctor-patient interactions with dynamic case generation.

## ✨ Features

### 🩺 **Doctor Mode**
- **AI Patients** with hidden medical conditions
- **Diagnostic Challenges** across multiple difficulty levels
- **Dynamic Case Generation** using advanced AI
- **Real-time Conversations** with realistic patient responses
- **Diagnosis Scoring** with detailed feedback

### 🤒 **Patient Mode**
- **AI Doctors** specialized by medical field
- **Interactive Consultations** with professional medical questioning
- **Educational Experience** from patient perspective
- **Multiple Specialties** available

### 🎯 **Key Capabilities**
- **Infinite Scalability** - Can generate any medical condition
- **Realistic Presentations** - AI characters don't know their diagnosis
- **Professional Quality** - Based on real medical knowledge
- **Web-Based Interface** - No installation required
- **Educational Focus** - Designed for medical learning

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/medical-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```
   
   Or create a `.env` file:
   ```bash
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

4. **Start the server**
   ```bash
   python run_server.py
   ```

5. **Open the game**
   - Web Interface: http://localhost:8000/static/index.html
   - API Documentation: http://localhost:8000/docs

## 🎮 How to Play

### Doctor Mode
1. **Choose Difficulty**: Easy → Expert
2. **Select Specialty** (optional): Cardiology, Neurology, etc.
3. **Meet Your Patient**: AI generates realistic case
4. **Conduct Interview**: Ask questions, examine patient
5. **Submit Diagnosis**: Test your medical knowledge
6. **Get Feedback**: Learn from detailed results

### Patient Mode
1. **Create Your Character**: Name, age, symptoms
2. **Choose Doctor Specialty**: Pick the right specialist
3. **Describe Symptoms**: Act as a real patient would
4. **Experience Healthcare**: Interact with AI doctor
5. **Learn Communication**: Understand patient perspective

## 🏗️ Architecture

### Backend (FastAPI)
- **`core_medical_game.py`** - Core game engine and medical AI
- **`api.py`** - REST API endpoints
- **Session Management** - Persistent game states
- **AI Integration** - Claude 3.5 Sonnet for realistic interactions

### Frontend (Vanilla JS)
- **`static/index.html`** - Main game interface
- **`static/styles.css`** - OpenEvidence-inspired design
- **`static/app.js`** - Game logic and API communication
- **Responsive Design** - Works on desktop and mobile

### Key Components

```
📁 Project Structure
├── 🎮 Core Game Engine
│   ├── core_medical_game.py     # Medical simulation logic
│   └── api.py                   # REST API endpoints
├── 🌐 Web Interface
│   ├── static/index.html        # Game interface
│   ├── static/styles.css        # Styling (OpenEvidence inspired)
│   └── static/app.js           # Frontend logic
├── 🔧 Configuration
│   ├── requirements.txt         # Python dependencies
│   └── run_server.py           # Server launcher
└── 📚 Documentation
    └── README_MEDSIM.md        # This file
```

## 🎯 API Endpoints

### Game Management
- `POST /api/game/create` - Create new game session
- `POST /api/game/setup-patient` - Setup patient mode
- `GET /api/game/{session_id}/state` - Get game state

### Gameplay
- `POST /api/game/message` - Send message to AI
- `POST /api/game/diagnose` - Submit diagnosis (doctor mode)

### Utilities
- `GET /api/specialties` - List medical specialties
- `GET /api/difficulties` - List difficulty levels
- `GET /api/health` - API health check

## 🎨 Design

The interface is inspired by [OpenEvidence](https://openevidence.com/) with:
- **Professional color scheme** (burnt orange primary)
- **Clean typography** (Inter font)
- **Responsive grid layout**
- **Medical-focused UI elements**
- **Accessible design patterns**

## 🔧 Configuration

### Environment Variables
```bash
ANTHROPIC_API_KEY=your_api_key_here  # Required
```

### Customization
- **Difficulty Levels**: Modify in `core_medical_game.py`
- **Medical Specialties**: Update `Specialty` enum
- **UI Styling**: Edit `static/styles.css`
- **API Behavior**: Configure in `api.py`

## 🚀 Advanced Features

### Dynamic Medical Knowledge
- **AI-Generated Cases** - Infinite variety of medical conditions
- **Realistic Presentations** - Patients behave authentically
- **Specialty-Focused** - Cases tailored to medical fields
- **Difficulty Scaling** - From common colds to rare diseases

### Educational Value
- **Clinical Reasoning** - Practice diagnostic thinking
- **Communication Skills** - Learn patient interaction
- **Medical Knowledge** - Exposure to diverse conditions
- **Professional Development** - Safe learning environment

## 🛠️ Development

### Adding New Features
1. **Backend Changes**: Modify `core_medical_game.py` or `api.py`
2. **Frontend Updates**: Edit files in `static/` directory
3. **Testing**: Use `/docs` endpoint for API testing
4. **Restart**: Server auto-reloads during development

### Extending Medical Knowledge
The system uses AI generation, so no manual condition coding needed:
- **New Specialties**: Add to `Specialty` enum
- **New Difficulties**: Add to `Difficulty` enum
- **Custom Conditions**: Modify AI prompts in `_generate_medical_condition`

## 📊 Examples

### Doctor Mode Case Examples
- **Easy**: Common cold, UTI, hypertension
- **Medium**: Pneumonia, diabetes, migraine
- **Hard**: Autoimmune conditions, complex presentations
- **Expert**: Rare diseases, challenging diagnoses

### Patient Mode Scenarios
- **Cardiology**: Chest pain, palpitations, shortness of breath
- **Neurology**: Headaches, seizures, memory problems
- **Emergency**: Trauma, acute conditions, urgent care

## 🔐 Security Notes

- **API Keys**: Keep Anthropic API key secure
- **Local Use**: Currently designed for local/educational use
- **Session Management**: In-memory storage (not persistent)
- **No Authentication**: Add authentication for production use

## 🤝 Contributing

1. **Fork the project**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

## 📄 License

This project is intended for educational purposes. Please ensure compliance with medical education guidelines and AI usage policies.

## 🙋‍♂️ Support

- **Issues**: Report bugs or request features
- **Documentation**: Check API docs at `/docs`
- **Medical Accuracy**: AI-generated content for educational use only
- **Technical Support**: Review logs and error messages

---

**⚠️ Disclaimer**: This is an educational simulation tool. Not intended for actual medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.