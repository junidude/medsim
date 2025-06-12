#!/usr/bin/env python3
"""
Medical Simulation Game REST API
FastAPI backend for web-based medical education game.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from core_medical_game import MedicalGameEngine, GameRole, Difficulty, Specialty
from patient_interaction_logger import patient_logger
from llm_providers import set_llm_provider

# Pydantic models for API requests
class CreateGameRequest(BaseModel):
    role: str  # "doctor" or "patient"
    difficulty: str = "medium"
    specialty: Optional[str] = None

class SetupPatientGameRequest(BaseModel):
    session_id: str
    patient_name: str
    patient_age: int
    patient_gender: str
    chief_complaint: str
    specialty: Optional[str] = ""  # Empty string means "any specialty"

class SendMessageRequest(BaseModel):
    session_id: str
    message: str

class SubmitDiagnosisRequest(BaseModel):
    session_id: str
    diagnosis: str

class ShowAnswerRequest(BaseModel):
    session_id: str

class PhysicalExamRequest(BaseModel):
    session_id: str

class LabTestRequest(BaseModel):
    session_id: str

class EndSessionRequest(BaseModel):
    session_id: str

class LogInteractionRequest(BaseModel):
    session_id: str
    action_type: str
    action_data: Dict[str, Any]

# Initialize FastAPI app
app = FastAPI(
    title="Medical Simulation Game API",
    description="Educational medical simulation game for doctors and patients",
    version="1.0.0"
)

# CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM provider - use DeepSeek for better performance and cost
try:
    # Check if API keys are available
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if deepseek_key:
        set_llm_provider("deepseek")
        print("✅ Using DeepSeek for AI conversations")
    elif anthropic_key:
        set_llm_provider("anthropic")
        print("✅ Using Anthropic Claude for AI conversations")
    else:
        # Try loading from api_keys.json file
        set_llm_provider("deepseek")
        print("✅ Using DeepSeek from api_keys.json")
except Exception as e:
    print(f"⚠️ Failed to initialize LLM provider: {e}")
    print("⚠️ API will run but AI features will not work")

# Initialize game engine with LLM provider
game_engine = MedicalGameEngine()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve main game page."""
    return FileResponse("static/index.html")

@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    """Create new game session."""
    try:
        # Validate input
        if request.role not in ["doctor", "patient"]:
            raise HTTPException(status_code=400, detail="Role must be 'doctor' or 'patient'")
        
        if request.difficulty not in ["easy", "medium", "hard", "expert"]:
            raise HTTPException(status_code=400, detail="Invalid difficulty level")
        
        if request.specialty and request.specialty not in [s.value for s in Specialty]:
            raise HTTPException(status_code=400, detail="Invalid specialty")
        
        # Create game session
        game_state = game_engine.create_game_session(
            role=request.role,
            difficulty=request.difficulty,
            specialty=request.specialty
        )
        
        response = {
            "session_id": game_state.session_id,
            "role": game_state.role.value,
            "difficulty": game_state.difficulty.value,
            "specialty": game_state.specialty.value if game_state.specialty else None,
            "message": f"Game session created. Role: {request.role.title()}"
        }
        
        # Auto-setup for doctor role
        if request.role == "doctor":
            setup_result = game_engine.setup_doctor_game(game_state.session_id)
            response.update(setup_result)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"[ERROR] Failed to create game session: {str(e)}")
        print(f"[ERROR] Request data: role={request.role}, difficulty={request.difficulty}, specialty={request.specialty}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/setup-patient")
async def setup_patient_game(request: SetupPatientGameRequest):
    """Setup patient game session."""
    try:
        # Handle "any specialty" (empty string) by selecting a random specialty
        specialty = request.specialty
        if not specialty or specialty == "":
            # Get available specialties and choose one randomly
            import random
            available_specialties = [s.value for s in Specialty]
            specialty = random.choice(available_specialties)
            print(f"[PATIENT] Selected random specialty: {specialty}")
        elif specialty not in [s.value for s in Specialty]:
            raise HTTPException(status_code=400, detail="Invalid specialty")
        
        result = game_engine.setup_patient_game(
            session_id=request.session_id,
            patient_name=request.patient_name,
            patient_age=request.patient_age,
            patient_gender=request.patient_gender,
            chief_complaint=request.chief_complaint,
            specialty=specialty
        )
        
        # Start patient interaction logging
        patient_logger.start_session(request.session_id, {
            "patient_name": request.patient_name,
            "patient_age": request.patient_age,
            "patient_gender": request.patient_gender,
            "chief_complaint": request.chief_complaint,
            "specialty": specialty  # Use the selected specialty, not the request one
        })
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"[ERROR] Failed to setup patient game: {str(e)}")
        print(f"[ERROR] Request data: session_id={request.session_id}, patient_name={request.patient_name}, age={request.patient_age}, specialty={request.specialty}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/message")
async def send_message(request: SendMessageRequest):
    """Send message to AI character."""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get game state to check role
        game_state_info = game_engine.get_game_state(request.session_id)
        
        # Log patient conversations
        if game_state_info.get("role") == "patient":
            # Log user message
            patient_logger.log_conversation("user", request.message)
        
        result = game_engine.send_message(request.session_id, request.message)
        
        # Log AI response for patient mode
        if game_state_info.get("role") == "patient" and "response" in result:
            patient_logger.log_conversation("ai_doctor", result["response"])
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/diagnose")
async def submit_diagnosis(request: SubmitDiagnosisRequest):
    """Submit diagnosis attempt (doctor role only)."""
    try:
        if not request.diagnosis.strip():
            raise HTTPException(status_code=400, detail="Diagnosis cannot be empty")
        
        result = game_engine.submit_diagnosis(request.session_id, request.diagnosis)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/show-answer")
async def show_answer(request: ShowAnswerRequest):
    """Show the correct answer for the current case."""
    try:
        result = game_engine.show_answer(request.session_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/show-multiple-choice")
async def show_multiple_choice(request: ShowAnswerRequest):
    """Show multiple choice options for the current case."""
    try:
        result = game_engine.show_multiple_choice(request.session_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/physical-exam")
async def physical_exam(request: PhysicalExamRequest):
    """Perform physical examination (doctor role only)."""
    try:
        result = game_engine.perform_physical_exam(request.session_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/lab-tests")
async def lab_tests(request: LabTestRequest):
    """Perform laboratory tests (doctor role only)."""
    try:
        result = game_engine.perform_lab_tests(request.session_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/{session_id}/state")
async def get_game_state(session_id: str):
    """Get current game state."""
    try:
        result = game_engine.get_game_state(session_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/difficulties")
async def get_difficulties():
    """Get available difficulty levels."""
    return {
        "difficulties": [
            {"value": d.value, "name": d.value.title(), "description": get_difficulty_description(d.value)}
            for d in Difficulty
        ]
    }

def get_difficulty_description(difficulty: str) -> str:
    """Get description for difficulty level."""
    descriptions = {
        "easy": "Common conditions that are straightforward to diagnose",
        "medium": "Moderate complexity cases requiring systematic approach",
        "hard": "Complex conditions with multiple symptoms and considerations",
        "expert": "Rare diseases and challenging diagnostic scenarios"
    }
    return descriptions.get(difficulty, "")

@app.get("/api/session/{session_id}/validate")
async def validate_session(session_id: str):
    """Validate if a session exists and is active."""
    try:
        # Check if session exists
        from session_store import session_store
        
        # First check in memory
        if session_id in game_engine.active_sessions:
            return {"valid": True, "location": "memory"}
        
        # Check in storage
        if session_store.session_exists(session_id):
            # Try to load it
            session_data = session_store.load_session(session_id)
            if session_data:
                return {"valid": True, "location": "storage"}
            else:
                return {"valid": False, "error": "Session file corrupted or expired"}
        
        return {"valid": False, "error": "Session not found"}
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

@app.get("/api/health")
async def health_check():
    """API health check with detailed status."""
    from llm_providers import get_llm_provider
    
    health_status = {
        "status": "healthy",
        "api_version": "1.0.0",
        "llm_provider": None,
        "llm_status": "not_initialized",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_keys_configured": {
            "deepseek": bool(os.getenv("DEEPSEEK_API_KEY")),
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
            "openai": bool(os.getenv("OPENAI_API_KEY"))
        },
        "sessions_directory": os.path.exists("sessions"),
        "active_sessions": len(game_engine.active_sessions) if game_engine else 0
    }
    
    try:
        provider = get_llm_provider()
        health_status["llm_provider"] = provider.get_provider_name()
        health_status["llm_status"] = "initialized"
        
        # Test if provider actually works
        try:
            test_response = provider.generate("test", max_tokens=1)
            health_status["llm_test"] = "working"
        except Exception as test_error:
            health_status["llm_test"] = f"failed: {str(test_error)}"
            health_status["status"] = "degraded"
            
    except Exception as e:
        health_status["llm_status"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status

@app.get("/api/specialties")
async def get_available_specialties():
    """Get list of available specialties from cached cases."""
    from case_manager import case_manager
    
    # Get all available specialties
    all_specialties = case_manager.get_available_specialties()
    
    # Get specialties by difficulty for more detailed info if needed
    by_difficulty = case_manager.get_specialties_by_difficulty()
    
    # Format specialties with display names
    formatted_specialties = []
    specialty_display_names = {
        "addiction_medicine": "Addiction Medicine",
        "allergy_immunology": "Allergy & Immunology",
        "anesthesiology": "Anesthesiology",
        "cardiovascular_disease": "Cardiovascular Disease",
        "child_adolescent_psychiatry": "Child & Adolescent Psychiatry",
        "colon_rectal_surgery": "Colon & Rectal Surgery",
        "critical_care_medicine": "Critical Care Medicine",
        "dermatology": "Dermatology",
        "emergency_medicine": "Emergency Medicine",
        "endocrinology": "Endocrinology",
        "family_medicine": "Family Medicine",
        "gastroenterology": "Gastroenterology",
        "general": "General Medicine",
        "general_surgery": "General Surgery",
        "geriatric_medicine": "Geriatric Medicine",
        "hand_surgery": "Hand Surgery",
        "hematology": "Hematology",
        "infectious_disease": "Infectious Disease",
        "internal_medicine": "Internal Medicine",
        "interventional_radiology": "Interventional Radiology",
        "medical_genetics": "Medical Genetics",
        "neonatal_perinatal_medicine": "Neonatal-Perinatal Medicine",
        "nephrology": "Nephrology",
        "neurological_surgery": "Neurological Surgery",
        "neurology": "Neurology",
        "neuroradiology": "Neuroradiology",
        "nuclear_medicine": "Nuclear Medicine",
        "obstetrics_gynecology": "Obstetrics & Gynecology",
        "oncology": "Oncology",
        "ophthalmology": "Ophthalmology",
        "orthopedic_surgery": "Orthopedic Surgery",
        "otolaryngology": "Otolaryngology",
        "pain_medicine": "Pain Medicine",
        "pathology": "Pathology",
        "pediatric_cardiology": "Pediatric Cardiology",
        "pediatric_critical_care": "Pediatric Critical Care",
        "pediatric_hematology_oncology": "Pediatric Hematology-Oncology",
        "pediatric_surgery": "Pediatric Surgery",
        "pediatrics": "Pediatrics",
        "physical_medicine_rehabilitation": "Physical Medicine & Rehabilitation",
        "plastic_surgery": "Plastic Surgery",
        "preventive_medicine": "Preventive Medicine",
        "psychiatry": "Psychiatry",
        "pulmonary_disease": "Pulmonary Disease",
        "radiation_oncology": "Radiation Oncology",
        "radiology": "Radiology",
        "rheumatology": "Rheumatology",
        "surgical_critical_care": "Surgical Critical Care",
        "thoracic_surgery": "Thoracic Surgery",
        "trauma_surgery": "Trauma Surgery",
        "urology": "Urology",
        "vascular_surgery": "Vascular Surgery"
    }
    
    for specialty in all_specialties:
        formatted_specialties.append({
            "value": specialty,
            "display": specialty_display_names.get(specialty, specialty.replace('_', ' ').title())
        })
    
    return {
        "specialties": formatted_specialties,
        "total": len(all_specialties),
        "by_difficulty": by_difficulty
    }

@app.get("/api/cases/stats")
async def get_case_stats():
    """Get statistics about available cached cases."""
    from case_manager import case_manager
    
    stats = {}
    total_cases = 0
    
    for difficulty in ["easy", "medium", "hard", "expert"]:
        difficulty_stats = {}
        difficulty_total = 0
        
        for specialty in ["general", "cardiology", "neurology", "pulmonology", 
                         "gastroenterology", "emergency_medicine", "internal_medicine"]:
            cases = case_manager.get_available_cases(difficulty, specialty)
            if cases:
                difficulty_stats[specialty] = len(cases)
                difficulty_total += len(cases)
        
        if difficulty_total > 0:
            stats[difficulty] = {
                "specialties": difficulty_stats,
                "total": difficulty_total
            }
            total_cases += difficulty_total
    
    return {
        "total_cases": total_cases,
        "by_difficulty": stats,
        "cache_status": "loaded"
    }

@app.post("/api/game/log-interaction")
async def log_interaction(request: LogInteractionRequest):
    """Log user interaction for patient mode."""
    try:
        # Only log for patient mode sessions
        game_state_info = game_engine.get_game_state(request.session_id)
        
        if game_state_info.get("role") == "patient":
            patient_logger.log_interaction(request.action_type, request.action_data)
            return {"status": "logged"}
        else:
            return {"status": "skipped", "reason": "Not patient mode"}
            
    except Exception as e:
        # Don't fail the request if logging fails
        return {"status": "error", "message": str(e)}

@app.post("/api/game/end-session")
async def end_session(request: EndSessionRequest):
    """End and log a game session."""
    try:
        # Check if patient mode to end logging
        game_state_info = game_engine.get_game_state(request.session_id)
        
        if game_state_info.get("role") == "patient":
            patient_logger.end_session()
        
        result = game_engine.end_session(request.session_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)