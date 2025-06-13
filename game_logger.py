#!/usr/bin/env python3
"""
Unified Game Logger for Medical Simulation
Combines session logging and patient interaction logging into one system.
"""

import json
import datetime
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import atexit

class LogType(Enum):
    SESSION = "session"
    PATIENT_INTERACTION = "patient_interaction"
    CONVERSATION = "conversation"
    ACTION = "action"
    AD_IMPRESSION = "ad_impression"

@dataclass
class GameLog:
    """Unified log structure for all game events."""
    session_id: str
    timestamp: str
    log_type: LogType
    role: str  # "doctor" or "patient"
    data: Dict[str, Any]
    
    # Session-specific fields
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None
    
    # Game configuration
    difficulty: Optional[str] = None
    specialty: Optional[str] = None
    
    # Patient information
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    chief_complaint: Optional[str] = None
    
    # Medical case data
    hidden_condition: Optional[str] = None
    case_data: Optional[Dict[str, Any]] = None
    
    # Conversation and actions
    chat_history: List[Dict[str, Any]] = None
    diagnostic_attempts: List[str] = None
    correct_diagnosis: bool = False
    physical_exam_performed: bool = False
    lab_tests_performed: bool = False
    answer_shown: bool = False
    
    # Metrics
    total_messages: int = 0
    session_duration_minutes: Optional[float] = None
    ad_impressions: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.chat_history is None:
            self.chat_history = []
        if self.diagnostic_attempts is None:
            self.diagnostic_attempts = []
        if self.ad_impressions is None:
            self.ad_impressions = []

class GameLogger:
    """Unified logger for all game events with performance optimizations."""
    
    def __init__(self, log_directory: str = "logs", patient_log_directory: str = "patient_logs"):
        self.log_directory = log_directory
        self.patient_log_directory = patient_log_directory
        self.ensure_directories()
        
        # In-memory cache for active sessions
        self.active_logs: Dict[str, GameLog] = {}
        self.log_lock = threading.Lock()
        
        # Buffer for batch writes
        self.write_buffer: List[GameLog] = []
        self.buffer_lock = threading.Lock()
        
        # Start background writer thread
        self._start_background_writer()
        
        # Register cleanup on exit
        atexit.register(self._flush_all_logs)
    
    def ensure_directories(self):
        """Create log directories if they don't exist."""
        os.makedirs(self.log_directory, exist_ok=True)
        os.makedirs(os.path.join(self.patient_log_directory, "conversations"), exist_ok=True)
        os.makedirs(os.path.join(self.patient_log_directory, "interactions"), exist_ok=True)
    
    def _start_background_writer(self):
        """Start background thread for batch writing logs."""
        import threading
        self.writer_thread = threading.Thread(target=self._background_writer, daemon=True)
        self.writer_thread.start()
    
    def _background_writer(self):
        """Background thread that writes logs every 5 seconds."""
        import time
        while True:
            time.sleep(5)
            self._flush_buffer()
    
    def _flush_buffer(self):
        """Write buffered logs to disk."""
        with self.buffer_lock:
            if not self.write_buffer:
                return
            
            logs_to_write = self.write_buffer[:]
            self.write_buffer.clear()
        
        # Write logs in batch
        for log in logs_to_write:
            self._write_log_to_disk(log)
    
    def _flush_all_logs(self):
        """Flush all pending logs on shutdown."""
        self._flush_buffer()
        # Also save any active sessions
        with self.log_lock:
            for session_id, log in self.active_logs.items():
                self._write_log_to_disk(log)
    
    def create_session(self, session_id: str, role: str, user_data: Dict[str, Any] = None) -> GameLog:
        """Create a new game session log."""
        log = GameLog(
            session_id=session_id,
            timestamp=datetime.datetime.now().isoformat(),
            log_type=LogType.SESSION,
            role=role,
            data={},
            start_time=datetime.datetime.now().isoformat(),
            user_data=user_data or {}
        )
        
        with self.log_lock:
            self.active_logs[session_id] = log
        
        return log
    
    def get_active_log(self, session_id: str) -> Optional[GameLog]:
        """Get active log from memory cache."""
        with self.log_lock:
            return self.active_logs.get(session_id)
    
    def log_message(self, session_id: str, role: str, content: str):
        """Log a chat message."""
        log = self.get_active_log(session_id)
        if not log:
            return
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        with self.log_lock:
            log.chat_history.append(message)
            log.total_messages += 1
    
    def log_action(self, session_id: str, action: str, data: Dict[str, Any] = None):
        """Log user actions."""
        log = self.get_active_log(session_id)
        if not log:
            return
        
        with self.log_lock:
            if action == "physical_exam":
                log.physical_exam_performed = True
            elif action == "lab_tests":
                log.lab_tests_performed = True
            elif action == "show_answer":
                log.answer_shown = True
            
            # Log action with timestamp
            action_log = {
                "action": action,
                "timestamp": datetime.datetime.now().isoformat(),
                "data": data or {}
            }
            log.data.setdefault("actions", []).append(action_log)
    
    def log_diagnostic_attempt(self, session_id: str, diagnosis: str, is_correct: bool):
        """Log diagnostic attempt."""
        log = self.get_active_log(session_id)
        if not log:
            return
        
        with self.log_lock:
            log.diagnostic_attempts.append(diagnosis)
            if is_correct:
                log.correct_diagnosis = True
    
    def log_ad_impression(self, session_id: str, ad_type: str = "banner", 
                         placement: str = "bottom", metadata: Dict[str, Any] = None):
        """Log ad impression event."""
        log = self.get_active_log(session_id)
        if not log:
            return
        
        ad_event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": ad_type,
            "placement": placement,
            "metadata": metadata or {}
        }
        
        with self.log_lock:
            log.ad_impressions.append(ad_event)
    
    def log_patient_interaction(self, action_type: str, action_data: Dict[str, Any]):
        """Log patient mode UI interactions."""
        timestamp = datetime.datetime.now()
        
        # Create interaction log
        interaction = {
            "timestamp": timestamp.isoformat(),
            "action_type": action_type,
            "action_data": action_data
        }
        
        # Write to interaction log file (patient mode specific)
        filename = f"interaction_{timestamp.strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.patient_log_directory, "interactions", filename)
        
        # Append to daily log file
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    interactions = json.load(f)
            else:
                interactions = []
            
            interactions.append(interaction)
            
            with open(filepath, 'w') as f:
                json.dump(interactions, f, indent=2)
        except Exception as e:
            print(f"Error logging patient interaction: {e}")
    
    def update_session_data(self, session_id: str, **kwargs):
        """Update session log with additional data."""
        log = self.get_active_log(session_id)
        if not log:
            return
        
        with self.log_lock:
            for key, value in kwargs.items():
                if hasattr(log, key):
                    setattr(log, key, value)
    
    def end_session(self, session_id: str):
        """End and save session."""
        log = self.get_active_log(session_id)
        if not log:
            return
        
        with self.log_lock:
            log.end_time = datetime.datetime.now().isoformat()
            
            # Calculate duration
            if log.start_time:
                start_dt = datetime.datetime.fromisoformat(log.start_time)
                end_dt = datetime.datetime.fromisoformat(log.end_time)
                duration = (end_dt - start_dt).total_seconds() / 60
                log.session_duration_minutes = round(duration, 2)
            
            # Remove from active logs
            self.active_logs.pop(session_id, None)
        
        # Add to write buffer
        with self.buffer_lock:
            self.write_buffer.append(log)
    
    def _write_log_to_disk(self, log: GameLog):
        """Write log to disk (called by background thread)."""
        try:
            # Determine filename based on log type and role
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if log.role == "patient" and log.log_type == LogType.SESSION:
                # Patient conversation logs
                filename = f"conversation_{timestamp}_{log.session_id[:8]}.json"
                filepath = os.path.join(self.patient_log_directory, "conversations", filename)
            else:
                # Regular session logs
                filename = f"session_{log.role}_{timestamp}_{log.session_id[:8]}.json"
                filepath = os.path.join(self.log_directory, filename)
            
            # Convert to dictionary and save
            log_data = asdict(log)
            # Convert enums to strings
            log_data["log_type"] = log.log_type.value
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving log to disk: {e}")
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of a session."""
        log = self.get_active_log(session_id)
        if not log:
            return {}
        
        return {
            "session_id": session_id,
            "role": log.role,
            "duration_minutes": log.session_duration_minutes,
            "total_messages": log.total_messages,
            "diagnostic_attempts": len(log.diagnostic_attempts or []),
            "correct_diagnosis": log.correct_diagnosis,
            "actions_performed": {
                "physical_exam": log.physical_exam_performed,
                "lab_tests": log.lab_tests_performed,
                "answer_shown": log.answer_shown
            }
        }

# Global logger instance
game_logger = GameLogger()