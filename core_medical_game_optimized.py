#!/usr/bin/env python3
"""
Optimized Medical Game Engine with performance improvements.
Key optimizations:
- Async LLM calls
- In-memory session caching with periodic saves
- Reduced file I/O operations
- Lazy case loading
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field
import random

# Import optimized modules
from llm_client import llm_client
from session_manager import session_manager
from game_logger import game_logger
from case_manager import case_manager

# Keep existing enums for compatibility
class GameRole(Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class Specialty(Enum):
    """All 51 medical specialties."""
    ADDICTION_MEDICINE = "addiction_medicine"
    ALLERGY_IMMUNOLOGY = "allergy_immunology"
    ANESTHESIOLOGY = "anesthesiology"
    CARDIOVASCULAR_DISEASE = "cardiovascular_disease"
    CHILD_ADOLESCENT_PSYCHIATRY = "child_adolescent_psychiatry"
    COLON_RECTAL_SURGERY = "colon_rectal_surgery"
    CRITICAL_CARE_MEDICINE = "critical_care_medicine"
    DERMATOLOGY = "dermatology"
    EMERGENCY_MEDICINE = "emergency_medicine"
    ENDOCRINOLOGY = "endocrinology"
    FAMILY_MEDICINE = "family_medicine"
    GASTROENTEROLOGY = "gastroenterology"
    GENERAL = "general"
    GENERAL_SURGERY = "general_surgery"
    GERIATRIC_MEDICINE = "geriatric_medicine"
    HAND_SURGERY = "hand_surgery"
    HEMATOLOGY = "hematology"
    INFECTIOUS_DISEASE = "infectious_disease"
    INTERNAL_MEDICINE = "internal_medicine"
    INTERVENTIONAL_RADIOLOGY = "interventional_radiology"
    MEDICAL_GENETICS = "medical_genetics"
    NEONATAL_PERINATAL_MEDICINE = "neonatal_perinatal_medicine"
    NEPHROLOGY = "nephrology"
    NEUROLOGICAL_SURGERY = "neurological_surgery"
    NEUROLOGY = "neurology"
    NEURORADIOLOGY = "neuroradiology"
    NUCLEAR_MEDICINE = "nuclear_medicine"
    OBSTETRICS_GYNECOLOGY = "obstetrics_gynecology"
    ONCOLOGY = "oncology"
    OPHTHALMOLOGY = "ophthalmology"
    ORTHOPEDIC_SURGERY = "orthopedic_surgery"
    OTOLARYNGOLOGY = "otolaryngology"
    PAIN_MEDICINE = "pain_medicine"
    PATHOLOGY = "pathology"
    PEDIATRIC_CARDIOLOGY = "pediatric_cardiology"
    PEDIATRIC_CRITICAL_CARE = "pediatric_critical_care"
    PEDIATRIC_HEMATOLOGY_ONCOLOGY = "pediatric_hematology_oncology"
    PEDIATRIC_SURGERY = "pediatric_surgery"
    PEDIATRICS = "pediatrics"
    PHYSICAL_MEDICINE_REHABILITATION = "physical_medicine_rehabilitation"
    PLASTIC_SURGERY = "plastic_surgery"
    PREVENTIVE_MEDICINE = "preventive_medicine"
    PSYCHIATRY = "psychiatry"
    PULMONARY_DISEASE = "pulmonary_disease"
    RADIATION_ONCOLOGY = "radiation_oncology"
    RADIOLOGY = "radiology"
    RHEUMATOLOGY = "rheumatology"
    SURGICAL_CRITICAL_CARE = "surgical_critical_care"
    THORACIC_SURGERY = "thoracic_surgery"
    TRAUMA_SURGERY = "trauma_surgery"
    UROLOGY = "urology"
    VASCULAR_SURGERY = "vascular_surgery"

@dataclass
class GameState:
    """Optimized game state with minimal serialization overhead."""
    session_id: str
    role: GameRole
    difficulty: Optional[Difficulty] = None
    specialty: Optional[Specialty] = None
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    
    # Patient information
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    chief_complaint: Optional[str] = None
    
    # Doctor role specific
    hidden_condition: Optional[str] = None
    condition_data: Optional[Dict[str, Any]] = None
    diagnostic_attempts: List[str] = field(default_factory=list)
    correct_diagnosis: bool = False
    answer_shown: bool = False
    
    # Flags
    physical_exam_performed: bool = False
    lab_tests_performed: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "role": self.role.value,
            "difficulty": self.difficulty.value if self.difficulty else None,
            "specialty": self.specialty.value if self.specialty else None,
            "conversation_history": self.conversation_history,
            "patient_name": self.patient_name,
            "patient_age": self.patient_age,
            "patient_gender": self.patient_gender,
            "chief_complaint": self.chief_complaint,
            "hidden_condition": self.hidden_condition,
            "condition_data": self.condition_data,
            "diagnostic_attempts": self.diagnostic_attempts,
            "correct_diagnosis": self.correct_diagnosis,
            "answer_shown": self.answer_shown,
            "physical_exam_performed": self.physical_exam_performed,
            "lab_tests_performed": self.lab_tests_performed,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameState":
        """Create GameState from dictionary."""
        # Convert string enums back to enum types
        role = GameRole(data["role"])
        difficulty = Difficulty(data["difficulty"]) if data.get("difficulty") else None
        specialty = Specialty(data["specialty"]) if data.get("specialty") else None
        
        # Convert datetime strings
        created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        last_modified = datetime.fromisoformat(data.get("last_modified", datetime.now().isoformat()))
        
        return cls(
            session_id=data["session_id"],
            role=role,
            difficulty=difficulty,
            specialty=specialty,
            conversation_history=data.get("conversation_history", []),
            patient_name=data.get("patient_name"),
            patient_age=data.get("patient_age"),
            patient_gender=data.get("patient_gender"),
            chief_complaint=data.get("chief_complaint"),
            hidden_condition=data.get("hidden_condition"),
            condition_data=data.get("condition_data"),
            diagnostic_attempts=data.get("diagnostic_attempts", []),
            correct_diagnosis=data.get("correct_diagnosis", False),
            answer_shown=data.get("answer_shown", False),
            physical_exam_performed=data.get("physical_exam_performed", False),
            lab_tests_performed=data.get("lab_tests_performed", False),
            created_at=created_at,
            last_modified=last_modified
        )

class OptimizedMedicalGameEngine:
    """Optimized medical game engine with async operations and caching."""
    
    def __init__(self):
        # Use optimized components
        self.llm_client = llm_client
        self.session_manager = session_manager
        self.game_logger = game_logger
        self.case_manager = case_manager
        
        # In-memory active games cache
        self.active_games: Dict[str, GameState] = {}
    
    def create_game_session(self, role: str, difficulty: str = "medium", 
                          specialty: Optional[str] = None) -> GameState:
        """Create a new game session."""
        session_id = str(uuid.uuid4())
        
        # Convert to enums
        game_role = GameRole(role)
        game_difficulty = Difficulty(difficulty) if difficulty else None
        game_specialty = Specialty(specialty) if specialty else None
        
        # Create game state
        game_state = GameState(
            session_id=session_id,
            role=game_role,
            difficulty=game_difficulty,
            specialty=game_specialty
        )
        
        # Store in memory and session manager
        self.active_games[session_id] = game_state
        self.session_manager.save_session(session_id, game_state.to_dict())
        
        # Create log entry
        self.game_logger.create_session(session_id, role, {
            "difficulty": difficulty,
            "specialty": specialty
        })
        
        return game_state
    
    def _get_session(self, session_id: str) -> GameState:
        """Get session with caching."""
        # Check memory cache first
        if session_id in self.active_games:
            return self.active_games[session_id]
        
        # Try session manager
        session_data = self.session_manager.get_session(session_id)
        if session_data:
            game_state = GameState.from_dict(session_data)
            self.active_games[session_id] = game_state
            return game_state
        
        raise KeyError(f"Session {session_id} not found")
    
    def _save_session(self, session_id: str, game_state: GameState, 
                     immediate: bool = False):
        """Save session with optional immediate persistence."""
        game_state.last_modified = datetime.now()
        
        # Update memory cache
        self.active_games[session_id] = game_state
        
        # Save to session manager (with buffering unless immediate)
        self.session_manager.save_session(
            session_id, 
            game_state.to_dict(),
            immediate=immediate
        )
    
    async def send_message_async(self, session_id: str, message: str) -> Dict[str, Any]:
        """Send message with async LLM call."""
        game_state = self._get_session(session_id)
        
        # Add to conversation history
        game_state.conversation_history.append({"role": "user", "content": message})
        
        # Log message
        self.game_logger.log_message(session_id, "user", message)
        
        # Generate AI response asynchronously
        ai_response = await self._generate_ai_response_async(game_state, message)
        
        # Add AI response to history
        game_state.conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Log AI response
        self.game_logger.log_message(session_id, "assistant", ai_response)
        
        # Save session (buffered, not immediate)
        self._save_session(session_id, game_state)
        
        return {
            "response": ai_response,
            "session_id": session_id
        }
    
    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Synchronous wrapper for send_message_async."""
        return asyncio.run(self.send_message_async(session_id, message))
    
    async def _generate_ai_response_async(self, game_state: GameState, 
                                        user_message: str) -> str:
        """Generate AI response using async LLM client."""
        if game_state.role == GameRole.DOCTOR:
            return await self._generate_patient_response_async(game_state, user_message)
        else:
            return await self._generate_doctor_response_async(game_state, user_message)
    
    async def _generate_patient_response_async(self, game_state: GameState, 
                                             doctor_message: str) -> str:
        """Generate patient response for doctor mode."""
        # Build context from condition data
        condition = game_state.condition_data or {}
        
        prompt = f"""You are playing the role of a patient with the following condition:
Diagnosis: {game_state.hidden_condition}
Chief Complaint: {condition.get('chief_complaint', 'Unknown')}
Symptoms: {', '.join(condition.get('symptoms', []))}
Medical History: {condition.get('medical_history', 'None')}

Respond to the doctor's question/statement naturally as this patient would.
Keep responses concise but informative. Don't reveal the diagnosis directly.

Doctor: {doctor_message}
Patient:"""
        
        return await self.llm_client.generate_async(prompt, temperature=0.7)
    
    async def _generate_doctor_response_async(self, game_state: GameState, 
                                            patient_message: str) -> str:
        """Generate doctor response for patient mode."""
        prompt = f"""You are an experienced and compassionate doctor.
The patient is: {game_state.patient_name}, {game_state.patient_age} year old {game_state.patient_gender}
Chief complaint: {game_state.chief_complaint}

Respond professionally to the patient's statement/question.
Be thorough but clear, showing empathy and medical expertise.

Patient: {patient_message}
Doctor:"""
        
        return await self.llm_client.generate_async(prompt, temperature=0.7)
    
    def setup_doctor_game(self, session_id: str) -> Dict[str, Any]:
        """Set up a doctor role game with a medical case."""
        game_state = self._get_session(session_id)
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "This endpoint is only for doctor role"}
        
        # Get medical case (cached)
        case_data = self._get_cached_medical_case(
            game_state.difficulty.value if game_state.difficulty else "medium",
            game_state.specialty.value if game_state.specialty else None
        )
        
        # Set up game state
        game_state.hidden_condition = case_data["name"]  # The diagnosis is stored in "name" field
        game_state.condition_data = case_data
        game_state.patient_name = self._generate_patient_name()
        # Generate age based on specialty and difficulty
        age_ranges = {
            "pediatrics": (1, 18),
            "pediatric_cardiology": (1, 18),
            "pediatric_critical_care": (1, 18),
            "pediatric_hematology_oncology": (1, 18),
            "pediatric_surgery": (1, 18),
            "geriatric_medicine": (65, 90),
            "neonatal_perinatal_medicine": (0, 1),
            "obstetrics_gynecology": (18, 45)
        }
        specialty_val = game_state.specialty.value if game_state.specialty else "general"
        min_age, max_age = age_ranges.get(specialty_val, (25, 65))
        game_state.patient_age = random.randint(min_age, max_age)
        game_state.patient_gender = random.choice(["male", "female"])
        game_state.chief_complaint = case_data.get("chief_complaint", "Not feeling well")
        
        # Update logger
        self.game_logger.update_session_data(
            session_id,
            patient_name=game_state.patient_name,
            patient_age=game_state.patient_age,
            patient_gender=game_state.patient_gender,
            chief_complaint=game_state.chief_complaint,
            hidden_condition=game_state.hidden_condition,
            case_data=case_data
        )
        
        # Save immediately for doctor setup
        self._save_session(session_id, game_state, immediate=True)
        
        # Return patient info
        return {
            "patient_name": game_state.patient_name,
            "patient_age": game_state.patient_age,
            "patient_gender": game_state.patient_gender,
            "chief_complaint": game_state.chief_complaint,
            "message": f"You are now seeing {game_state.patient_name}, a {game_state.patient_age} year old {game_state.patient_gender}. Chief complaint: {game_state.chief_complaint}"
        }
    
    def _get_cached_medical_case(self, difficulty: str, 
                               specialty: Optional[str] = None) -> Dict[str, Any]:
        """Get medical case with caching."""
        # Try to get cached case first
        cached_case = self.case_manager.get_random_case(difficulty, specialty)
        
        if cached_case:
            return cached_case
        
        # Generate new case if needed (30% chance or no cached cases)
        if random.random() < 0.3 or not cached_case:
            # Generate asynchronously but run in sync context
            new_case = asyncio.run(self._generate_medical_case_async(difficulty, specialty))
            
            # Save the new case (but don't reload entire cache)
            self.case_manager.save_case(new_case, difficulty, specialty)
            
            return new_case
        
        return cached_case
    
    async def _generate_medical_case_async(self, difficulty: str, 
                                         specialty: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new medical case asynchronously."""
        # Implementation would go here - simplified for now
        prompt = f"Generate a {difficulty} medical case for {specialty or 'any'} specialty..."
        # ... rest of generation logic
        
        # For now, return a simple case structure matching the expected format
        return {
            "case_id": f"generated_{difficulty}_{specialty or 'general'}_001",
            "name": "Generated Condition",
            "specialty": specialty or "general",
            "difficulty": difficulty,
            "chief_complaint": "Generated complaint",
            "symptoms": ["symptom1", "symptom2"],
            "treatment": ["Treatment option 1", "Treatment option 2"],
            "prognosis": "Good with proper treatment"
        }
    
    def _generate_patient_name(self) -> str:
        """Generate a random patient name."""
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", 
                      "Robert", "Lisa", "James", "Mary"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", 
                     "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def submit_diagnosis(self, session_id: str, diagnosis: str) -> Dict[str, Any]:
        """Submit and check diagnosis."""
        game_state = self._get_session(session_id)
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Only doctors can submit diagnoses"}
        
        # Add to attempts
        game_state.diagnostic_attempts.append(diagnosis)
        
        # Check if correct
        correct = diagnosis.lower().strip() == game_state.hidden_condition.lower().strip()
        
        # Log attempt
        self.game_logger.log_diagnostic_attempt(session_id, diagnosis, correct)
        
        if correct:
            game_state.correct_diagnosis = True
            self._save_session(session_id, game_state, immediate=True)
            
            return {
                "correct": True,
                "message": "Congratulations! Your diagnosis is correct.",
                "attempts": len(game_state.diagnostic_attempts),
                "condition_info": {
                    "name": game_state.condition_data.get("name"),
                    "description": game_state.condition_data.get("description", ""),
                    "treatment": game_state.condition_data.get("treatment", []),
                    "prognosis": game_state.condition_data.get("prognosis", "")
                }
            }
        else:
            self._save_session(session_id, game_state)
            
            return {
                "correct": False,
                "message": "That's not quite right. Keep investigating.",
                "attempts": len(game_state.diagnostic_attempts)
            }
    
    def get_game_state(self, session_id: str) -> Dict[str, Any]:
        """Get current game state info."""
        try:
            game_state = self._get_session(session_id)
            return {
                "session_id": session_id,
                "role": game_state.role.value,
                "patient_name": game_state.patient_name,
                "patient_age": game_state.patient_age,
                "patient_gender": game_state.patient_gender,
                "chief_complaint": game_state.chief_complaint,
                "message_count": len(game_state.conversation_history),
                "attempts": len(game_state.diagnostic_attempts),
                "session_log": self.game_logger.get_active_log(session_id)
            }
        except KeyError:
            return {"error": "Session not found"}
    
    def show_answer(self, session_id: str) -> Dict[str, Any]:
        """Show the correct answer for the current case (doctor role only)."""
        game_state = self._get_session(session_id)
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Answer viewing only available in doctor mode"}
        
        # Mark that answer was shown
        game_state.answer_shown = True
        
        # Save session
        self._save_session(session_id, game_state)
        
        return {
            "correct": True,
            "message": f"The correct diagnosis is: {game_state.hidden_condition}",
            "condition_info": {
                "name": game_state.condition_data["name"],
                "treatment": game_state.condition_data.get("treatment", []),
                "prognosis": game_state.condition_data.get("prognosis", ""),
                "difficulty": game_state.difficulty.value if game_state.difficulty else "unknown",
                "description": game_state.condition_data.get("description", ""),
                "symptoms": game_state.condition_data.get("symptoms", []),
                "risk_factors": game_state.condition_data.get("risk_factors", [])
            },
            "attempts": len(game_state.diagnostic_attempts),
            "answer_shown": True
        }
    
    def show_multiple_choice(self, session_id: str) -> Dict[str, Any]:
        """Show multiple choice options for the current case (doctor role only)."""
        game_state = self._get_session(session_id)
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Multiple choice only available in doctor mode"}
        
        # Get multiple choice options from condition data
        multiple_choice = game_state.condition_data.get("multiple_choice", [])
        
        if not multiple_choice:
            # Fallback if no multiple choice data
            return {
                "error": "Multiple choice options not available for this case",
                "message": "This case doesn't have multiple choice options. Try using 'Show Answer' instead."
            }
        
        return {
            "success": True,
            "message": "Choose from the following differential diagnoses:",
            "multiple_choice": multiple_choice
            # Don't send the correct answer - let the player figure it out
        }
    
    def perform_physical_exam(self, session_id: str) -> Dict[str, Any]:
        """Perform physical examination (doctor role only)."""
        game_state = self._get_session(session_id)
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Physical examination only available in doctor mode"}
        
        # Get physical findings from condition data
        condition_data = game_state.condition_data
        physical_findings = condition_data.get("physical_findings", [])
        
        # Format findings for display
        formatted_findings = []
        if isinstance(physical_findings, list) and physical_findings:
            for finding in physical_findings:
                if isinstance(finding, str):
                    formatted_findings.append({
                        "system": "General",
                        "finding": finding
                    })
                elif isinstance(finding, dict):
                    formatted_findings.append(finding)
        
        # If no specific findings, provide general examination results
        if not formatted_findings:
            formatted_findings = [
                {
                    "system": "General Appearance",
                    "finding": f"Patient appears {condition_data.get('patient_behavior', {}).get('anxiety_level', 'comfortable')}"
                },
                {
                    "system": "Vital Signs",
                    "finding": "Blood pressure: 120/80 mmHg, Heart rate: 72 bpm, Temperature: 98.6°F"
                }
            ]
        
        return {
            "physical_findings": formatted_findings,
            "message": "Physical examination completed"
        }
    
    def perform_lab_tests(self, session_id: str) -> Dict[str, Any]:
        """Perform laboratory tests (doctor role only)."""
        game_state = self._get_session(session_id)
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Laboratory tests only available in doctor mode"}
        
        # Get lab results from condition data
        condition_data = game_state.condition_data
        lab_results = condition_data.get("lab_results", {})
        
        # If no specific lab results, provide common tests
        if not lab_results:
            lab_results = {
                "CBC": "Normal",
                "Basic Metabolic Panel": "Normal",
                "Liver Function": "Normal"
            }
        
        # Determine which values are abnormal based on condition
        abnormal_values = []
        
        # Mark abnormal values that are already in the data
        for test, result in lab_results.items():
            if isinstance(result, str) and any(word in result.lower() for word in ["elevated", "low", "high", "abnormal", "positive"]):
                abnormal_values.append(test)
        
        return {
            "lab_results": lab_results,
            "abnormal_values": abnormal_values,
            "message": "Laboratory test results available"
        }
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End a game session."""
        try:
            game_state = self._get_session(session_id)
            
            # Save final state immediately
            self._save_session(session_id, game_state, immediate=True)
            
            # End logging
            self.game_logger.end_session(session_id)
            
            # Get summary
            summary = self.game_logger.get_session_summary(session_id)
            
            # Clean up memory
            self.active_games.pop(session_id, None)
            self.session_manager.evict_from_cache(session_id)
            
            return {
                "message": "Session ended successfully",
                "summary": summary
            }
        except KeyError:
            return {"error": "Session not found"}

# Global optimized engine instance
optimized_game_engine = OptimizedMedicalGameEngine()