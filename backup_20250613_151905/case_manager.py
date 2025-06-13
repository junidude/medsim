#!/usr/bin/env python3
"""
Medical Case Manager
Handles loading, caching, and management of pre-generated medical cases.
"""

import json
import os
import random
import glob
from typing import Dict, List, Optional, Any
from pathlib import Path

# Ensure true randomness
random.seed()

class MedicalCaseManager:
    """Manages medical cases stored as JSON files."""
    
    def __init__(self, cases_directory: str = "cases"):
        self.cases_directory = Path(cases_directory)
        self.case_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.load_all_cases()
    
    def load_all_cases(self):
        """Load all cases from the cases directory into memory."""
        print("📚 Loading medical cases...")
        
        if not self.cases_directory.exists():
            print(f"❌ Cases directory not found: {self.cases_directory}")
            return
        
        total_cases = 0
        difficulty_counts = {}
        
        # Load cases organized by difficulty and specialty
        for difficulty in ["easy", "medium", "hard", "expert"]:
            difficulty_path = self.cases_directory / difficulty
            if not difficulty_path.exists():
                continue
            
            difficulty_total = 0
            
            # Dynamically discover all specialty directories
            for specialty_path in difficulty_path.iterdir():
                if not specialty_path.is_dir():
                    continue
                    
                specialty = specialty_path.name
                cases = self._load_cases_from_directory(specialty_path)
                if cases:
                    cache_key = f"{difficulty}_{specialty}"
                    self.case_cache[cache_key] = cases
                    difficulty_total += len(cases)
                    total_cases += len(cases)
            
            if difficulty_total > 0:
                difficulty_counts[difficulty] = difficulty_total
        
        # Print compact summary
        print(f"✅ Loaded {total_cases} cases: " + 
              ", ".join([f"{diff}: {count}" for diff, count in difficulty_counts.items()]))
    
    def _load_cases_from_directory(self, directory_path: Path) -> List[Dict[str, Any]]:
        """Load all JSON case files from a specific directory."""
        cases = []
        
        for case_file in directory_path.glob("*.json"):
            try:
                with open(case_file, 'r', encoding='utf-8') as f:
                    case_data = json.load(f)
                    # Validate case data
                    if self._validate_case(case_data):
                        cases.append(case_data)
                    else:
                        print(f"⚠️  Invalid case data in {case_file}")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"❌ Error loading case {case_file}: {e}")
        
        return cases
    
    def _validate_case(self, case_data: Dict[str, Any]) -> bool:
        """Validate that a case has required fields."""
        required_fields = [
            "case_id", "name", "specialty", "difficulty", 
            "chief_complaint", "symptoms", "treatment", "prognosis"
        ]
        
        for field in required_fields:
            if field not in case_data:
                return False
        
        return True
    
    def get_random_case(self, difficulty: str, specialty: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a random case for the specified difficulty and specialty."""
        
        # If specialty is None or empty string, select from any specialty
        if not specialty:
            # Get all cases for this difficulty level
            matching_keys = [key for key in self.case_cache.keys() if key.startswith(f"{difficulty}_")]
            if matching_keys:
                # Select a random specialty, then a random case from that specialty
                cache_key = random.choice(matching_keys)
                case = random.choice(self.case_cache[cache_key])
                return case.copy()
            else:
                return None
        
        # If specific specialty is requested
        cache_key = f"{difficulty}_{specialty}"
        if cache_key in self.case_cache and self.case_cache[cache_key]:
            case = random.choice(self.case_cache[cache_key])
            return case.copy()
        
        # Fallback: try any specialty for this difficulty
        matching_keys = [key for key in self.case_cache.keys() if key.startswith(f"{difficulty}_")]
        if matching_keys:
            cache_key = random.choice(matching_keys)
            case = random.choice(self.case_cache[cache_key])
            return case.copy()
        
        return None
    
    def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific case by its ID."""
        for cases in self.case_cache.values():
            for case in cases:
                if case.get("case_id") == case_id:
                    return case.copy()
        return None
    
    def get_available_cases(self, difficulty: str, specialty: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all available cases for a difficulty/specialty combination."""
        if specialty:
            cache_key = f"{difficulty}_{specialty}"
            if cache_key in self.case_cache:
                return [case.copy() for case in self.case_cache[cache_key]]
        
        # Return all cases for the difficulty level
        matching_cases = []
        for key, cases in self.case_cache.items():
            if key.startswith(f"{difficulty}_"):
                matching_cases.extend([case.copy() for case in cases])
        
        return matching_cases
    
    def get_available_specialties(self, difficulty: Optional[str] = None) -> List[str]:
        """Get list of specialties that have cases available.
        
        Args:
            difficulty: If specified, only return specialties for that difficulty level
            
        Returns:
            List of specialty names sorted alphabetically
        """
        specialties = set()
        
        for cache_key in self.case_cache.keys():
            if self.case_cache[cache_key]:  # Only if there are cases
                parts = cache_key.split('_', 1)
                if len(parts) == 2:
                    diff, spec = parts
                    if difficulty is None or diff == difficulty:
                        specialties.add(spec)
        
        return sorted(list(specialties))
    
    def get_specialties_by_difficulty(self) -> Dict[str, List[str]]:
        """Get available specialties grouped by difficulty."""
        result = {}
        for difficulty in ["easy", "medium", "hard", "expert"]:
            result[difficulty] = self.get_available_specialties(difficulty)
        return result
    
    def get_existing_diagnoses(self, difficulty: str = None, specialty: str = None) -> List[str]:
        """Get list of all existing diagnoses to avoid duplicates.
        
        Args:
            difficulty: Filter by difficulty level (optional)
            specialty: Filter by specialty (optional)
            
        Returns:
            List of existing diagnosis names (case-insensitive)
        """
        diagnoses = set()
        
        for key, cases in self.case_cache.items():
            # Filter by difficulty if specified
            if difficulty and not key.startswith(f"{difficulty}_"):
                continue
            
            # Filter by specialty if specified
            if specialty and not key.endswith(f"_{specialty}"):
                continue
            
            # Collect all diagnoses from matching cases
            for case in cases:
                if 'name' in case:
                    diagnoses.add(case['name'].lower())
        
        return sorted(list(diagnoses))
    
    def print_detailed_summary(self):
        """Print a detailed summary of loaded cases (on demand only)."""
        print("\n📊 Detailed Case Summary:")
        print("-" * 40)
        
        for difficulty in ["easy", "medium", "hard", "expert"]:
            difficulty_total = 0
            print(f"{difficulty.upper()}:")
            
            # Get all specialties for this difficulty from cache keys
            specialties = sorted([key.split('_', 1)[1] for key in self.case_cache.keys() 
                                if key.startswith(f"{difficulty}_")])
            
            for specialty in specialties:
                cache_key = f"{difficulty}_{specialty}"
                if cache_key in self.case_cache:
                    count = len(self.case_cache[cache_key])
                    if count > 0:
                        print(f"  {specialty}: {count} cases")
                        difficulty_total += count
            
            print(f"  Total {difficulty}: {difficulty_total} cases")
            print()
    
    def generate_case_template(self) -> Dict[str, Any]:
        """Generate a template for creating new cases."""
        return {
            "case_id": "difficulty_specialty_###",
            "name": "Medical Condition Name",
            "specialty": "medical_specialty",
            "difficulty": "easy/medium/hard/expert",
            "chief_complaint": "Patient's main complaint in their words",
            "symptoms": [
                "symptom1",
                "symptom2", 
                "symptom3"
            ],
            "physical_findings": [
                {
                    "system": "System Name",
                    "finding": "Physical examination finding"
                }
            ],
            "lab_results": {
                "Test Name": "Result value"
            },
            "treatment": [
                "treatment1",
                "treatment2"
            ],
            "prognosis": "Expected outcome and timeline",
            "description": "Detailed medical description",
            "risk_factors": [
                "risk_factor1",
                "risk_factor2"
            ],
            "patient_behavior": {
                "anxiety_level": "low/medium/high",
                "cooperation": "good/fair/poor",
                "pain_level": "1-10"
            }
        }
    
    def create_case_file(self, case_data: Dict[str, Any], save_path: Optional[str] = None) -> bool:
        """Create a new case file from case data."""
        try:
            if not self._validate_case(case_data):
                print("❌ Invalid case data provided")
                return False
            
            if not save_path:
                difficulty = case_data["difficulty"]
                specialty = case_data["specialty"]
                case_id = case_data["case_id"]
                save_path = self.cases_directory / difficulty / specialty / f"{case_id}.json"
            
            # Ensure directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(case_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Case saved: {save_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving case: {e}")
            return False

# Singleton instance for global use
case_manager = MedicalCaseManager()