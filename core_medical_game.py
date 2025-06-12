#!/usr/bin/env python3
"""
Essential Medical Simulation Core
Streamlined system for web-based medical education game.
"""

import json
import uuid
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import anthropic
from case_manager import case_manager
from session_logger import session_logger, SessionLog
from llm_providers import get_llm_provider, LLMProvider

class GameRole(Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class Specialty(Enum):
    # Primary Care Boards
    FAMILY_MEDICINE = "family_medicine"
    INTERNAL_MEDICINE = "internal_medicine"
    PEDIATRICS = "pediatrics"
    OBSTETRICS_GYNECOLOGY = "obstetrics_gynecology"
    
    # Surgical Boards
    GENERAL_SURGERY = "general_surgery"
    ORTHOPEDIC_SURGERY = "orthopedic_surgery"
    NEUROLOGICAL_SURGERY = "neurological_surgery"
    PLASTIC_SURGERY = "plastic_surgery"
    UROLOGY = "urology"
    OTOLARYNGOLOGY = "otolaryngology"
    OPHTHALMOLOGY = "ophthalmology"
    THORACIC_SURGERY = "thoracic_surgery"
    COLON_RECTAL_SURGERY = "colon_rectal_surgery"
    
    # Medical Specialties
    ANESTHESIOLOGY = "anesthesiology"
    DERMATOLOGY = "dermatology"
    EMERGENCY_MEDICINE = "emergency_medicine"
    NEUROLOGY = "neurology"
    PATHOLOGY = "pathology"
    PHYSICAL_MEDICINE_REHAB = "physical_medicine_rehabilitation"
    PSYCHIATRY = "psychiatry"
    RADIOLOGY = "radiology"
    RADIATION_ONCOLOGY = "radiation_oncology"
    NUCLEAR_MEDICINE = "nuclear_medicine"
    
    # Subspecialty Boards
    ALLERGY_IMMUNOLOGY = "allergy_immunology"
    MEDICAL_GENETICS = "medical_genetics"
    PREVENTIVE_MEDICINE = "preventive_medicine"
    
    # Internal Medicine Subspecialties
    CARDIOVASCULAR = "cardiovascular_disease"
    GASTROENTEROLOGY = "gastroenterology"
    HEMATOLOGY = "hematology"
    ONCOLOGY = "oncology"
    ENDOCRINOLOGY = "endocrinology"
    NEPHROLOGY = "nephrology"
    PULMONARY = "pulmonary_disease"
    RHEUMATOLOGY = "rheumatology"
    INFECTIOUS_DISEASE = "infectious_disease"
    GERIATRIC_MEDICINE = "geriatric_medicine"
    CRITICAL_CARE = "critical_care_medicine"
    
    # Pediatric Subspecialties
    PEDIATRIC_CARDIOLOGY = "pediatric_cardiology"
    PEDIATRIC_HEMATOLOGY_ONCOLOGY = "pediatric_hematology_oncology"
    NEONATAL_PERINATAL = "neonatal_perinatal_medicine"
    PEDIATRIC_CRITICAL_CARE = "pediatric_critical_care"
    
    # Surgical Subspecialties
    VASCULAR_SURGERY = "vascular_surgery"
    PEDIATRIC_SURGERY = "pediatric_surgery"
    HAND_SURGERY = "hand_surgery"
    SURGICAL_CRITICAL_CARE = "surgical_critical_care"
    TRAUMA_SURGERY = "trauma_surgery"
    
    # Radiology Subspecialties
    INTERVENTIONAL_RADIOLOGY = "interventional_radiology"
    NEURORADIOLOGY = "neuroradiology"
    
    # Anesthesiology Subspecialties
    PAIN_MEDICINE = "pain_medicine"
    
    # Psychiatry Subspecialties
    CHILD_PSYCHIATRY = "child_adolescent_psychiatry"
    ADDICTION_MEDICINE = "addiction_medicine"

@dataclass
class GameState:
    """Current game session state."""
    session_id: str
    role: GameRole
    difficulty: Difficulty
    specialty: Optional[Specialty]
    patient_name: str
    patient_age: int
    patient_gender: str
    chief_complaint: str
    
    # Medical condition (hidden from player if doctor role)
    hidden_condition: Optional[str] = None
    condition_data: Optional[Dict[str, Any]] = None
    
    # Game progress
    conversation_history: List[Dict[str, str]] = None
    actions_taken: List[str] = None
    diagnostic_attempts: List[str] = None
    correct_diagnosis: bool = False
    answer_shown: bool = False
    
    # AI context
    ai_system_prompt: Optional[str] = None
    
    # Session logging
    session_log: Optional[SessionLog] = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.actions_taken is None:
            self.actions_taken = []
        if self.diagnostic_attempts is None:
            self.diagnostic_attempts = []

class MedicalGameEngine:
    """Core medical simulation engine."""
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        # For backward compatibility, support direct Anthropic API key
        if anthropic_api_key:
            self.client = anthropic.Anthropic(api_key=anthropic_api_key)
            self.llm_provider = None  # Will use direct client
        else:
            self.client = None
            self.llm_provider = get_llm_provider()  # Use the configured provider
        self.active_sessions: Dict[str, GameState] = {}
    
    def _generate_llm_response(self, prompt: str, system_prompt: Optional[str] = None,
                              max_tokens: int = 1000, messages: Optional[List[Dict]] = None) -> str:
        """Generate response using configured LLM provider."""
        if self.llm_provider:
            # Use the LLM provider abstraction
            return self.llm_provider.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                messages=messages
            )
        elif self.client:
            # Use direct Anthropic client (backward compatibility)
            if messages:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=max_tokens,
                    system=system_prompt or "",
                    messages=messages
                )
            else:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=max_tokens,
                    system=system_prompt or "You are a helpful assistant.",
                    messages=[{"role": "user", "content": prompt}]
                )
            return response.content[0].text.strip()
        else:
            raise ValueError("No LLM provider configured")
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End and log a game session."""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        game_state = self.active_sessions[session_id]
        
        # Finalize session log
        if game_state.session_log:
            session_logger.finalize_session(game_state.session_log)
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return {
            "message": "Session ended and logged successfully",
            "session_id": session_id
        }
    
    def create_game_session(self, role: str, difficulty: str = "medium", 
                           specialty: str = None) -> GameState:
        """Create new game session."""
        session_id = str(uuid.uuid4())
        
        print(f"🎯 Creating session with: role={role}, difficulty={difficulty}, specialty={specialty}")
        
        game_state = GameState(
            session_id=session_id,
            role=GameRole(role),
            difficulty=Difficulty(difficulty),
            specialty=Specialty(specialty) if specialty else None,
            patient_name="",
            patient_age=0,
            patient_gender="",
            chief_complaint=""
        )
        
        # Initialize session logging
        user_data = {
            "role": role,
            "difficulty": difficulty,
            "specialty": specialty
        }
        game_state.session_log = session_logger.create_session_log(session_id, role, user_data)
        
        self.active_sessions[session_id] = game_state
        return game_state
    
    def setup_doctor_game(self, session_id: str) -> Dict[str, Any]:
        """Setup game for doctor role - use cached medical case."""
        game_state = self.active_sessions[session_id]
        
        # Get cached medical case instead of generating new one
        specialty_value = game_state.specialty.value if game_state.specialty else None
        print(f"🎯 Looking for case: difficulty={game_state.difficulty.value}, specialty={specialty_value}")
        
        condition_data = self._get_cached_medical_case(
            game_state.difficulty.value,
            specialty_value
        )
        
        # Create patient demographics
        patient_info = self._generate_patient_demographics(condition_data)
        
        # Update game state
        game_state.patient_name = patient_info["name"]
        game_state.patient_age = patient_info["age"]
        game_state.patient_gender = patient_info["gender"]
        game_state.chief_complaint = condition_data["chief_complaint"]
        game_state.hidden_condition = condition_data["name"]
        game_state.condition_data = condition_data
        game_state.ai_system_prompt = self._create_patient_ai_prompt(condition_data, patient_info)
        
        # Update session log with doctor game data
        if game_state.session_log:
            session_logger.update_session_data(
                game_state.session_log,
                patient_name=patient_info["name"],
                patient_age=patient_info["age"],
                patient_gender=patient_info["gender"],
                chief_complaint=condition_data["chief_complaint"],
                hidden_condition=condition_data["name"],
                case_data=condition_data,
                difficulty=game_state.difficulty.value,
                specialty=game_state.specialty.value if game_state.specialty else None
            )
        
        return {
            "session_id": session_id,
            "patient_name": patient_info["name"],
            "patient_age": patient_info["age"],
            "patient_gender": patient_info["gender"],
            "chief_complaint": condition_data["chief_complaint"],
            "difficulty": game_state.difficulty.value,
            "specialty": condition_data.get("specialty", "general"),
            "case_id": condition_data.get("case_id", "unknown"),
            "message": f"Patient {patient_info['name']} has arrived with: {condition_data['chief_complaint']}"
        }
    
    def setup_patient_game(self, session_id: str, patient_name: str, 
                          patient_age: int, patient_gender: str, 
                          chief_complaint: str, specialty: str) -> Dict[str, Any]:
        """Setup game for patient role - create AI doctor."""
        game_state = self.active_sessions[session_id]
        
        # Update patient info
        game_state.patient_name = patient_name
        game_state.patient_age = patient_age
        game_state.patient_gender = patient_gender
        game_state.chief_complaint = chief_complaint
        game_state.specialty = Specialty(specialty)
        
        # Create AI doctor prompt with full patient information
        game_state.ai_system_prompt = self._create_doctor_ai_prompt(
            specialty, patient_name, patient_age, patient_gender, chief_complaint
        )
        
        print(f"🩺 Patient mode AI prompt created for Dr. Smith ({specialty})")
        print(f"🩺 Patient: {patient_name}, {patient_age}y/o {patient_gender}, CC: {chief_complaint}")
        
        # Update session log with patient game data
        if game_state.session_log:
            session_logger.update_session_data(
                game_state.session_log,
                patient_name=patient_name,
                patient_age=patient_age,
                patient_gender=patient_gender,
                chief_complaint=chief_complaint,
                specialty=specialty
            )
        
        return {
            "session_id": session_id,
            "patient_name": patient_name,
            "patient_age": patient_age,
            "patient_gender": patient_gender,
            "chief_complaint": chief_complaint,
            "doctor_specialty": specialty,
            "message": f"Dr. Smith ({specialty}) will see you now.",
            "initial_ai_message": f"Hello {patient_name}, I'm Dr. Smith. I understand you're experiencing {chief_complaint}. When did this start?"
        }
    
    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Send message to AI and get response."""
        game_state = self.active_sessions[session_id]
        
        # Add user message to history
        timestamp = datetime.datetime.now().isoformat()
        game_state.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": timestamp
        })
        
        # Log user message
        if game_state.session_log:
            session_logger.log_message(game_state.session_log, "user", message, timestamp)
        
        # Generate AI response
        ai_response = self._generate_ai_response(game_state, message)
        
        # Add AI response to history
        ai_timestamp = datetime.datetime.now().isoformat()
        game_state.conversation_history.append({
            "role": "ai",
            "content": ai_response,
            "timestamp": ai_timestamp
        })
        
        # Log AI response
        if game_state.session_log:
            session_logger.log_message(game_state.session_log, "ai", ai_response, ai_timestamp)
        
        return {
            "response": ai_response,
            "conversation_history": game_state.conversation_history[-6:]  # Last 6 messages
        }
    
    def submit_diagnosis(self, session_id: str, diagnosis: str) -> Dict[str, Any]:
        """Submit diagnosis attempt (doctor role only)."""
        game_state = self.active_sessions[session_id]
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Diagnosis submission only available in doctor mode"}
        
        game_state.diagnostic_attempts.append(diagnosis)
        
        # Check if diagnosis is correct
        correct_condition = game_state.hidden_condition.lower()
        user_diagnosis = diagnosis.lower()
        
        # Flexible matching
        is_correct = any(term in user_diagnosis for term in correct_condition.split()) or \
                    any(term in correct_condition for term in user_diagnosis.split())
        
        # Log diagnostic attempt
        if game_state.session_log:
            session_logger.log_diagnostic_attempt(game_state.session_log, diagnosis, is_correct)
        
        if is_correct:
            game_state.correct_diagnosis = True
            return {
                "correct": True,
                "message": f"Correct! The patient has {game_state.hidden_condition}",
                "condition_info": {
                    "name": game_state.condition_data["name"],
                    "treatment": game_state.condition_data.get("treatment", []),
                    "prognosis": game_state.condition_data.get("prognosis", ""),
                    "difficulty": game_state.difficulty.value
                },
                "attempts": len(game_state.diagnostic_attempts)
            }
        else:
            return {
                "correct": False,
                "message": "Incorrect diagnosis. Continue your examination and gather more information.",
                "attempts": len(game_state.diagnostic_attempts)
            }
    
    def show_answer(self, session_id: str) -> Dict[str, Any]:
        """Show the correct answer for the current case (doctor role only)."""
        game_state = self.active_sessions[session_id]
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Answer viewing only available in doctor mode"}
        
        # Mark that answer was shown
        game_state.answer_shown = True
        
        # Log action
        if game_state.session_log:
            session_logger.log_action(game_state.session_log, "show_answer")
        
        return {
            "correct": True,
            "message": f"The correct diagnosis is: {game_state.hidden_condition}",
            "condition_info": {
                "name": game_state.condition_data["name"],
                "treatment": game_state.condition_data.get("treatment", []),
                "prognosis": game_state.condition_data.get("prognosis", ""),
                "difficulty": game_state.difficulty.value,
                "description": game_state.condition_data.get("description", ""),
                "symptoms": game_state.condition_data.get("symptoms", []),
                "risk_factors": game_state.condition_data.get("risk_factors", [])
            },
            "attempts": len(game_state.diagnostic_attempts),
            "answer_shown": True
        }
    
    def show_multiple_choice(self, session_id: str) -> Dict[str, Any]:
        """Show multiple choice options for the current case (doctor role only)."""
        game_state = self.active_sessions[session_id]
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Multiple choice only available in doctor mode"}
        
        # Log action
        if game_state.session_log:
            session_logger.log_action(game_state.session_log, "show_multiple_choice")
        
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
        game_state = self.active_sessions[session_id]
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Physical examination only available in doctor mode"}
        
        # Log action
        if game_state.session_log:
            session_logger.log_action(game_state.session_log, "physical_exam")
        
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
        game_state = self.active_sessions[session_id]
        
        if game_state.role != GameRole.DOCTOR:
            return {"error": "Laboratory tests only available in doctor mode"}
        
        # Log action
        if game_state.session_log:
            session_logger.log_action(game_state.session_log, "lab_tests")
        
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
        condition_name = game_state.hidden_condition.lower()
        
        # Add condition-specific abnormal values
        if "thyroid" in condition_name:
            lab_results.update({
                "TSH": "Elevated (8.5 mIU/L)",
                "Free T4": "Low (0.8 ng/dL)",
                "Anti-TPO": "Positive"
            })
            abnormal_values.extend(["TSH", "Free T4", "Anti-TPO"])
        
        if "infection" in condition_name or "fever" in condition_name:
            lab_results.update({
                "WBC": "Elevated (12,000/μL)",
                "ESR": "Elevated (45 mm/hr)",
                "CRP": "Elevated (15 mg/L)"
            })
            abnormal_values.extend(["WBC", "ESR", "CRP"])
        
        return {
            "lab_results": lab_results,
            "abnormal_values": abnormal_values,
            "message": "Laboratory test results available"
        }
    
    def get_game_state(self, session_id: str) -> Dict[str, Any]:
        """Get current game state."""
        game_state = self.active_sessions.get(session_id)
        if not game_state:
            return {"error": "Session not found"}
        
        return {
            "session_id": session_id,
            "role": game_state.role.value,
            "difficulty": game_state.difficulty.value,
            "specialty": game_state.specialty.value if game_state.specialty else None,
            "patient_name": game_state.patient_name,
            "patient_age": game_state.patient_age,
            "patient_gender": game_state.patient_gender,
            "chief_complaint": game_state.chief_complaint,
            "conversation_count": len(game_state.conversation_history),
            "actions_count": len(game_state.actions_taken),
            "diagnostic_attempts": len(game_state.diagnostic_attempts),
            "correct_diagnosis": game_state.correct_diagnosis
        }
    
    def _get_cached_medical_case(self, difficulty: str, specialty: str = None) -> Dict[str, Any]:
        """Get a medical case with 70% chance from cache, 30% chance generated."""
        import random
        
        # Check if cached cases are available
        cached_case = case_manager.get_random_case(difficulty, specialty)
        
        if cached_case:
            # We have cached cases - use 70/30 split
            use_cache = random.random() < 0.7  # 70% chance to use cache
            
            if use_cache:
                print(f"✅ Using cached case: {cached_case.get('case_id', 'unknown')}")
                return cached_case
            else:
                print(f"🎲 Randomly generating new case (30% chance)")
                generated_case = self._generate_medical_condition_llm(difficulty, specialty)
                # Ensure generated case has the requested specialty if it was specified
                if specialty and generated_case:
                    generated_case['specialty'] = specialty
                    generated_case['difficulty'] = difficulty
                    
                    # Save the generated case to the cases folder
                    if case_manager.create_case_file(generated_case):
                        print(f"💾 Saved generated case: {generated_case.get('name', 'Unknown')}")
                        # Reload cases to include the new one
                        case_manager.load_all_cases()
                    
                return generated_case
        else:
            # No cached cases available - must generate
            print(f"⚠️  No cached cases available for {difficulty}/{specialty}, falling back to LLM generation")
            generated_case = self._generate_medical_condition_llm(difficulty, specialty)
            # Ensure generated case has the requested specialty if it was specified
            if specialty and generated_case:
                generated_case['specialty'] = specialty
                generated_case['difficulty'] = difficulty
                
                # Save the generated case to the cases folder
                if case_manager.create_case_file(generated_case):
                    print(f"💾 Saved generated case: {generated_case.get('name', 'Unknown')}")
                    # Reload cases to include the new one
                    case_manager.load_all_cases()
                    
            return generated_case
    
    def _generate_medical_condition_llm(self, difficulty: str, specialty: str = None) -> Dict[str, Any]:
        """Generate medical condition using LLM."""
        import random
        import datetime
        
        # Add randomness to ensure different conditions each time
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_seed = random.randint(1, 10000)
        
        # Get existing diagnoses to avoid duplicates
        existing_diagnoses = case_manager.get_existing_diagnoses(difficulty, specialty)
        existing_list = "\n".join([f"- {diag}" for diag in existing_diagnoses[:50]])  # Show first 50
        
        prompt = f"""Generate a realistic medical condition for educational simulation:

Parameters:
- Difficulty: {difficulty}
- Specialty: {specialty or 'any appropriate'}
- Unique ID: {timestamp}-{random_seed}
- IMPORTANT: Generate a completely NEW and DIFFERENT medical condition each time

EXISTING DIAGNOSES TO AVOID (DO NOT DUPLICATE):
{existing_list}
{'... and ' + str(len(existing_diagnoses) - 50) + ' more' if len(existing_diagnoses) > 50 else ''}

You MUST generate a diagnosis that is NOT in the above list.

Return ONLY valid JSON with this structure:
{{
  "name": "Medical Condition Name",
  "specialty": "medical_specialty",
  "chief_complaint": "what patient would say",
  "symptoms": ["symptom1", "symptom2", "symptom3"],
  "physical_findings": ["finding1", "finding2"],
  "lab_results": {{"test": "result"}},
  "treatment": ["treatment1", "treatment2"],
  "prognosis": "outcome description",
  "description": "detailed condition description",
  "risk_factors": ["factor1", "factor2"],
  "patient_behavior": {{
    "anxiety_level": "low/medium/high",
    "cooperation": "good/fair/poor",
    "pain_level": "1-10"
  }},
  "multiple_choice": ["correct_diagnosis", "plausible_option2", "plausible_option3", "plausible_option4"]
}}

Difficulty guidelines:
- easy: Common conditions (cold, UTI, hypertension, gastritis, headache)
- medium: Moderate complexity (pneumonia, diabetes, migraine, bronchitis, anxiety)
- hard: Complex conditions (autoimmune, cardiac events, neurological disorders)
- expert: Rare or challenging diagnoses (rare diseases, complex presentations)

Multiple Choice Requirements:
- Include exactly 4 diagnosis options in the "multiple_choice" array
- The first element MUST be the correct diagnosis (same as "name")
- The other 3 should be plausible differential diagnoses
- Mix the order randomly so the correct answer isn't always first
- Make differentials appropriate for the difficulty level

CRITICAL: Must generate a DIFFERENT condition than previous calls. 
Generate {difficulty} level condition #{random_seed} now:"""
        
        try:
            response_text = self._generate_llm_response(
                prompt=prompt,
                system_prompt="Generate medical conditions as valid JSON only.",
                max_tokens=1000
            )
            
            json_text = response_text
            start = json_text.find('{')
            end = json_text.rfind('}') + 1
            
            if start != -1 and end > start:
                generated_case = json.loads(json_text[start:end])
                # Add case_id if not present
                if 'case_id' not in generated_case:
                    generated_case['case_id'] = f"generated_{timestamp}_{random_seed}"
                # Ensure specialty is set if requested
                if specialty and 'specialty' not in generated_case:
                    generated_case['specialty'] = specialty
                return generated_case
            
        except Exception as e:
            print(f"Error generating condition: {e}")
        
        # Fallback
        return {
            "case_id": f"generated_{timestamp}_{random_seed}",
            "name": "Common Cold",
            "specialty": specialty or "family_medicine",
            "chief_complaint": "cold symptoms",
            "symptoms": ["runny nose", "cough", "fatigue"],
            "physical_findings": ["nasal congestion"],
            "treatment": ["rest", "fluids"],
            "prognosis": "resolves in 7-10 days",
            "patient_behavior": {"anxiety_level": "low", "cooperation": "good", "pain_level": "2"},
            "multiple_choice": ["Common Cold", "Seasonal Allergies", "Sinusitis", "Influenza"]
        }
    
    def _generate_patient_demographics(self, condition_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate realistic patient demographics."""
        import random
        
        # Expanded name lists for more variety
        male_names = ["James", "John", "Robert", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George", "Timothy", "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon"]
        
        female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Helen", "Sandra", "Donna", "Carol", "Ruth", "Sharon", "Michelle", "Laura", "Sarah", "Kimberly", "Deborah", "Dorothy", "Amy", "Angela", "Ashley", "Brenda", "Emma", "Olivia", "Cynthia", "Marie", "Janet", "Catherine", "Frances", "Christine", "Samantha", "Debra", "Rachel"]
        
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]
        
        # Generate with more randomness
        gender = random.choice(["male", "female"])
        first_name = random.choice(male_names if gender == "male" else female_names)
        last_name = random.choice(last_names)
        
        # Age ranges based on condition type if available
        condition_name = condition_data.get("name", "").lower()
        if any(term in condition_name for term in ["pediatric", "child", "infant"]):
            age = random.randint(5, 17)
        elif any(term in condition_name for term in ["elderly", "senior", "geriatric"]):
            age = random.randint(65, 90)
        else:
            age = random.randint(18, 80)
        
        return {
            "name": f"{first_name} {last_name}",
            "age": age,
            "gender": gender
        }
    
    def _create_patient_ai_prompt(self, condition_data: Dict[str, Any], patient_info: Dict[str, str]) -> str:
        """Create AI system prompt for patient role."""
        
        behavior = condition_data.get("patient_behavior", {})
        
        return f"""You are {patient_info['name']}, a {patient_info['age']}-year-old {patient_info['gender']} patient.

CRITICAL RULES:
- You have {condition_data['name']} but DO NOT know this diagnosis
- Only describe symptoms in simple, non-medical terms
- Never mention the condition name or medical terminology
- Show realistic emotions based on your symptoms

YOUR PRESENTATION:
- Chief complaint: {condition_data['chief_complaint']}
- Symptoms you feel: {', '.join(condition_data.get('symptoms', [])[:3])}
- Anxiety level: {behavior.get('anxiety_level', 'medium')}
- Pain level: {behavior.get('pain_level', '5')}/10
- Cooperation: {behavior.get('cooperation', 'good')}

BEHAVIOR:
- Describe symptoms as a real patient would
- Ask questions about what might be wrong
- Show appropriate worry or concern
- Respond naturally to doctor's questions
- Be honest about what you don't know

Remember: You're seeking help, not teaching medicine. Respond in 1-3 sentences."""
    
    def _create_doctor_ai_prompt(self, specialty: str, patient_name: str, patient_age: int, 
                               patient_gender: str, chief_complaint: str) -> str:
        """Create AI system prompt for doctor role with patient information."""
        
        return f"""You are Dr. Smith, a kind {specialty} physician.

PATIENT INFORMATION:
- Name: {patient_name}
- Age: {patient_age} years old
- Gender: {patient_gender}
- Chief complaint: {chief_complaint}
- Specialty consulted: {specialty}

CONTEXT:
You are seeing {patient_name}, a {patient_age}-year-old {patient_gender} patient who came to see you for {chief_complaint}. You should address them by name and be aware of their demographic information when asking questions and providing care.

YOUR APPROACH:
- Address the patient by name ({patient_name})
- Ask focused questions appropriate for their age and gender
- Be professional and caring
- Keep responses short and clear
- Use simple language
- Consider age-appropriate differential diagnoses

COMMUNICATION STYLE:
- MAXIMUM 1-2 short sentences per response
- Be warm but concise
- Ask one question at a time
- Use kind but brief responses
- Use the patient's name occasionally

Example responses:
- "Hello {patient_name}, I understand you're experiencing {chief_complaint}. When did this start?"
- "That must be concerning for you. Any other symptoms?"
- "Let me examine you, {patient_name}. Can you describe the pain more?"

Keep it SHORT, KIND, and PERSONALIZED."""
    
    def _generate_ai_response(self, game_state: GameState, user_message: str) -> str:
        """Generate AI response based on game state and user message."""
        
        # Build conversation context
        context_messages = []
        
        # Add recent conversation history
        for msg in game_state.conversation_history[-6:]:
            role = "user" if msg["role"] == "user" else "assistant"
            context_messages.append({"role": role, "content": msg["content"]})
        
        # Add current user message
        context_messages.append({"role": "user", "content": user_message})
        
        try:
            print(f"💬 Generating AI response for {game_state.role.value} mode")
            print(f"💬 System prompt preview: {game_state.ai_system_prompt[:100]}...")
            
            response_text = self._generate_llm_response(
                prompt="",  # Not used when messages are provided
                system_prompt=game_state.ai_system_prompt,
                max_tokens=300,
                messages=context_messages
            )
            
            return response_text
            
        except Exception as e:
            print(f"AI response error: {e}")
            
            if game_state.role == GameRole.DOCTOR:
                return "I'm not feeling well, doctor. Can you help me?"
            else:
                return "Let me examine you further. Can you tell me more about your symptoms?"
    
    def generate_and_save_cases(self, difficulty: str, specialty: str, count: int = 5) -> int:
        """Generate and save multiple cases for a specific difficulty/specialty."""
        saved_count = 0
        
        for i in range(count):
            try:
                # Generate case using LLM
                case_data = self._generate_medical_condition_llm(difficulty, specialty)
                
                # Add metadata
                case_data["case_id"] = f"{difficulty}_{specialty}_{str(i+1).zfill(3)}"
                case_data["difficulty"] = difficulty
                case_data["specialty"] = specialty
                
                # Save to file
                if case_manager.create_case_file(case_data):
                    saved_count += 1
                    print(f"✅ Generated and saved case {i+1}/{count}")
                else:
                    print(f"❌ Failed to save case {i+1}/{count}")
                    
            except Exception as e:
                print(f"❌ Error generating case {i+1}/{count}: {e}")
        
        # Reload the case cache to include new cases
        case_manager.load_all_cases()
        
        return saved_count