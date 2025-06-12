#!/usr/bin/env python3
"""
Session storage for maintaining game state across requests
Uses file-based storage for simplicity in single-server deployments
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading
from pathlib import Path

class SessionStore:
    """Simple file-based session storage"""
    
    def __init__(self, storage_dir: str = "sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.lock = threading.Lock()
        
        # Clean up old sessions on startup
        self._cleanup_old_sessions()
    
    def _get_session_path(self, session_id: str) -> Path:
        """Get the file path for a session"""
        return self.storage_dir / f"{session_id}.json"
    
    def save_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """Save session data to file"""
        with self.lock:
            session_path = self._get_session_path(session_id)
            data['last_updated'] = datetime.now().isoformat()
            
            with open(session_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from file"""
        with self.lock:
            session_path = self._get_session_path(session_id)
            
            if not session_path.exists():
                return None
            
            try:
                with open(session_path, 'r') as f:
                    data = json.load(f)
                
                # Check if session is expired (24 hours)
                last_updated = datetime.fromisoformat(data.get('last_updated', ''))
                if datetime.now() - last_updated > timedelta(hours=24):
                    self.delete_session(session_id)
                    return None
                
                return data
            except Exception as e:
                print(f"Error loading session {session_id}: {e}")
                return None
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session"""
        with self.lock:
            session_path = self._get_session_path(session_id)
            if session_path.exists():
                session_path.unlink()
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists"""
        return self._get_session_path(session_id).exists()
    
    def _cleanup_old_sessions(self) -> None:
        """Clean up sessions older than 24 hours"""
        try:
            for session_file in self.storage_dir.glob("*.json"):
                try:
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                    
                    last_updated = datetime.fromisoformat(data.get('last_updated', ''))
                    if datetime.now() - last_updated > timedelta(hours=24):
                        session_file.unlink()
                        print(f"Cleaned up old session: {session_file.stem}")
                except Exception:
                    # If we can't read the file, delete it
                    session_file.unlink()
        except Exception as e:
            print(f"Error during session cleanup: {e}")

# Global session store instance
session_store = SessionStore()