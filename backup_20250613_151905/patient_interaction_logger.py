#!/usr/bin/env python3
"""
Patient Interaction Logger for Medical Simulation Game
Captures all patient mode interactions including conversations and UI actions.
"""

import json
import datetime
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

class PatientInteractionLogger:
    """Logger for patient mode interactions with real-time saving."""
    
    def __init__(self, logs_dir: str = "patient_logs"):
        """Initialize the patient interaction logger."""
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for organization
        self.conversations_dir = self.logs_dir / "conversations"
        self.interactions_dir = self.logs_dir / "interactions"
        self.conversations_dir.mkdir(exist_ok=True)
        self.interactions_dir.mkdir(exist_ok=True)
        
        self.current_session = None
        self.interaction_log = []
        
    def start_session(self, session_id: str, user_data: Dict[str, Any]) -> None:
        """Start a new patient session."""
        self.current_session = {
            "session_id": session_id,
            "start_time": datetime.datetime.now().isoformat(),
            "user_data": user_data,
            "conversations": [],
            "interactions": []
        }
        
        # Initialize interaction log
        self.interaction_log = [{
            "timestamp": datetime.datetime.now().isoformat(),
            "action": "session_start",
            "data": user_data
        }]
        
        # Save initial state
        self._save_current_state()
    
    def log_conversation(self, speaker: str, message: str, metadata: Optional[Dict] = None) -> None:
        """Log a conversation message."""
        if not self.current_session:
            return
            
        conversation_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "speaker": speaker,  # "user" or "ai_doctor"
            "message": message,
            "metadata": metadata or {}
        }
        
        self.current_session["conversations"].append(conversation_entry)
        
        # Log as interaction too
        self.log_interaction("conversation", {
            "speaker": speaker,
            "message": message,
            **metadata
        } if metadata else {"speaker": speaker, "message": message})
    
    def log_interaction(self, action_type: str, action_data: Dict[str, Any]) -> None:
        """Log any user interaction (button clicks, form submissions, etc.)."""
        if not self.current_session:
            return
            
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action_type,
            "data": action_data
        }
        
        self.interaction_log.append(interaction)
        self.current_session["interactions"] = self.interaction_log
        
        # Save after each interaction (overwrite mode)
        self._save_current_state()
    
    def log_button_click(self, button_id: str, button_text: str, additional_data: Optional[Dict] = None) -> None:
        """Log a button click event."""
        data = {
            "button_id": button_id,
            "button_text": button_text
        }
        if additional_data:
            data.update(additional_data)
            
        self.log_interaction("button_click", data)
    
    def log_form_submission(self, form_data: Dict[str, Any]) -> None:
        """Log form submission."""
        self.log_interaction("form_submission", form_data)
    
    def log_page_navigation(self, from_page: str, to_page: str) -> None:
        """Log page/screen navigation."""
        self.log_interaction("navigation", {
            "from": from_page,
            "to": to_page
        })
    
    def end_session(self, session_data: Optional[Dict[str, Any]] = None) -> None:
        """End the current session and save final state."""
        if not self.current_session:
            return
            
        self.current_session["end_time"] = datetime.datetime.now().isoformat()
        
        # Calculate session duration
        start = datetime.datetime.fromisoformat(self.current_session["start_time"])
        end = datetime.datetime.fromisoformat(self.current_session["end_time"])
        duration = (end - start).total_seconds() / 60  # in minutes
        self.current_session["session_duration_minutes"] = round(duration, 2)
        
        # Add any final session data
        if session_data:
            self.current_session["final_data"] = session_data
        
        # Log session end
        self.log_interaction("session_end", {
            "duration_minutes": self.current_session["session_duration_minutes"]
        })
        
        # Final save
        self._save_current_state()
        
        # Create a summary file
        self._save_session_summary()
        
        # Clear current session
        self.current_session = None
        self.interaction_log = []
    
    def _save_current_state(self) -> None:
        """Save current state to file (overwrites existing)."""
        if not self.current_session:
            return
            
        session_id = self.current_session["session_id"]
        
        # Save full interaction log (overwrites each time)
        interaction_file = self.interactions_dir / f"{session_id}_interactions.json"
        with open(interaction_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_session, f, indent=2, ensure_ascii=False)
        
        # Also save just conversations for easy access
        conversation_file = self.conversations_dir / f"{session_id}_conversation.json"
        conversation_data = {
            "session_id": session_id,
            "user_data": self.current_session["user_data"],
            "conversations": self.current_session["conversations"]
        }
        with open(conversation_file, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
    
    def _save_session_summary(self) -> None:
        """Save a summary of the session for quick analysis."""
        if not self.current_session:
            return
            
        session_id = self.current_session["session_id"]
        
        summary = {
            "session_id": session_id,
            "start_time": self.current_session["start_time"],
            "end_time": self.current_session["end_time"],
            "duration_minutes": self.current_session["session_duration_minutes"],
            "user_data": self.current_session["user_data"],
            "total_messages": len(self.current_session["conversations"]),
            "total_interactions": len(self.current_session["interactions"]),
            "interaction_types": {}
        }
        
        # Count interaction types
        for interaction in self.current_session["interactions"]:
            action = interaction["action"]
            summary["interaction_types"][action] = summary["interaction_types"].get(action, 0) + 1
        
        # Save summary
        summary_file = self.logs_dir / f"{session_id}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    def get_session_logs(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve logs for a specific session."""
        interaction_file = self.interactions_dir / f"{session_id}_interactions.json"
        if interaction_file.exists():
            with open(interaction_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_all_sessions(self) -> List[Dict[str, Any]]:
        """List all logged sessions with summaries."""
        sessions = []
        for summary_file in self.logs_dir.glob("*_summary.json"):
            with open(summary_file, 'r', encoding='utf-8') as f:
                sessions.append(json.load(f))
        
        # Sort by start time (most recent first)
        sessions.sort(key=lambda x: x["start_time"], reverse=True)
        return sessions


# Global instance for easy access
patient_logger = PatientInteractionLogger()