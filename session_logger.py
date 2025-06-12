#!/usr/bin/env python3
"""
Session Logger for Medical Simulation Game
Logs user information, chat conversations, and session data.
"""

import json
import datetime
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class SessionLog:
    """Complete session log data structure."""
    session_id: str
    start_time: str
    role: str  # "doctor" or "patient"
    
    # Optional fields with defaults
    end_time: Optional[str] = None
    user_data: Dict[str, Any] = None  # All user input data
    
    # Game Configuration
    difficulty: Optional[str] = None
    specialty: Optional[str] = None
    
    # Patient Information (for both roles)
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    chief_complaint: Optional[str] = None
    
    # Medical Case Data (for doctor role)
    hidden_condition: Optional[str] = None
    case_data: Optional[Dict[str, Any]] = None
    
    # Conversation Log
    chat_history: List[Dict[str, Any]] = None
    
    # Game Results
    diagnostic_attempts: List[str] = None
    correct_diagnosis: bool = False
    physical_exam_performed: bool = False
    lab_tests_performed: bool = False
    answer_shown: bool = False
    
    # Session Metrics
    total_messages: int = 0
    session_duration_minutes: Optional[float] = None
    
    # Ad Metrics
    ad_impressions: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.chat_history is None:
            self.chat_history = []
        if self.diagnostic_attempts is None:
            self.diagnostic_attempts = []
        if self.user_data is None:
            self.user_data = {}
        if self.case_data is None:
            self.case_data = {}
        if self.ad_impressions is None:
            self.ad_impressions = []

class SessionLogger:
    """Handles logging of user sessions and chat data."""
    
    def __init__(self, log_directory: str = "logs"):
        """Initialize the session logger."""
        self.log_directory = log_directory
        self.ensure_log_directory()
        
    def ensure_log_directory(self):
        """Create logs directory if it doesn't exist."""
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
            
    def create_session_log(self, session_id: str, role: str, user_data: Dict[str, Any]) -> SessionLog:
        """Create a new session log."""
        session_log = SessionLog(
            session_id=session_id,
            start_time=datetime.datetime.now().isoformat(),
            role=role,
            user_data=user_data,
            chat_history=[],
            diagnostic_attempts=[]
        )
        return session_log
    
    def update_session_data(self, session_log: SessionLog, **kwargs):
        """Update session log with additional data."""
        for key, value in kwargs.items():
            if hasattr(session_log, key):
                setattr(session_log, key, value)
    
    def log_message(self, session_log: SessionLog, role: str, content: str, timestamp: str = None):
        """Log a chat message."""
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
            
        message = {
            "role": role,  # "user", "ai", "system"
            "content": content,
            "timestamp": timestamp
        }
        
        session_log.chat_history.append(message)
        session_log.total_messages += 1
    
    def log_diagnostic_attempt(self, session_log: SessionLog, diagnosis: str, is_correct: bool):
        """Log a diagnostic attempt."""
        session_log.diagnostic_attempts.append(diagnosis)
        if is_correct:
            session_log.correct_diagnosis = True
    
    def log_action(self, session_log: SessionLog, action: str):
        """Log user actions like physical exam, lab tests, etc."""
        if action == "physical_exam":
            session_log.physical_exam_performed = True
        elif action == "lab_tests":
            session_log.lab_tests_performed = True
        elif action == "show_answer":
            session_log.answer_shown = True
    
    def log_ad_impression(self, session_log: SessionLog, ad_type: str = "banner", 
                          placement: str = "bottom", metadata: Dict[str, Any] = None):
        """Log ad impression event."""
        ad_event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": ad_type,
            "placement": placement,
            "metadata": metadata or {}
        }
        session_log.ad_impressions.append(ad_event)
    
    def finalize_session(self, session_log: SessionLog):
        """Finalize and save the session log."""
        session_log.end_time = datetime.datetime.now().isoformat()
        
        # Calculate session duration
        if session_log.start_time and session_log.end_time:
            start_dt = datetime.datetime.fromisoformat(session_log.start_time)
            end_dt = datetime.datetime.fromisoformat(session_log.end_time)
            duration = (end_dt - start_dt).total_seconds() / 60
            session_log.session_duration_minutes = round(duration, 2)
        
        # Save to file
        self.save_session_log(session_log)
    
    def save_session_log(self, session_log: SessionLog):
        """Save session log to JSON file."""
        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{session_log.role}_{timestamp}_{session_log.session_id[:8]}.json"
        filepath = os.path.join(self.log_directory, filename)
        
        # Convert to dictionary
        log_data = asdict(session_log)
        
        # Save to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            print(f"📝 Session log saved: {filepath}")
        except Exception as e:
            print(f"❌ Error saving session log: {e}")
    
    def get_session_summary(self, session_log: SessionLog) -> Dict[str, Any]:
        """Get a summary of the session."""
        return {
            "session_id": session_log.session_id,
            "role": session_log.role,
            "duration_minutes": session_log.session_duration_minutes,
            "total_messages": session_log.total_messages,
            "diagnostic_attempts": len(session_log.diagnostic_attempts or []),
            "correct_diagnosis": session_log.correct_diagnosis,
            "actions_performed": {
                "physical_exam": session_log.physical_exam_performed,
                "lab_tests": session_log.lab_tests_performed,
                "answer_shown": session_log.answer_shown
            }
        }
    
    def export_chat_history(self, session_log: SessionLog, format: str = "txt") -> str:
        """Export chat history in readable format."""
        if format == "txt":
            lines = []
            lines.append(f"Chat History - Session {session_log.session_id}")
            lines.append(f"Role: {session_log.role.title()}")
            lines.append(f"Date: {session_log.start_time}")
            lines.append("=" * 50)
            
            for msg in session_log.chat_history:
                timestamp = msg["timestamp"][:19]  # Remove microseconds
                role = msg["role"].upper()
                content = msg["content"]
                lines.append(f"[{timestamp}] {role}: {content}")
            
            return "\n".join(lines)
        
        return json.dumps(session_log.chat_history, indent=2)

# Global logger instance
session_logger = SessionLogger()