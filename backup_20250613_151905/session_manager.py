#!/usr/bin/env python3
"""
High-performance session manager with in-memory caching and async operations.
"""

import json
import os
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from pathlib import Path
import threading
import atexit

class SessionManager:
    """Manages game sessions with performance optimizations."""
    
    def __init__(self, session_dir: str = "sessions", cache_ttl: int = 3600):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.cache_ttl = cache_ttl  # Cache time-to-live in seconds
        
        # In-memory cache
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, float] = {}
        self.dirty_sessions: set = set()  # Sessions that need to be saved
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Background tasks
        self.save_interval = 5  # Save dirty sessions every 5 seconds
        self.cleanup_interval = 300  # Clean old sessions every 5 minutes
        self._start_background_tasks()
        
        # Save all on exit
        atexit.register(self._save_all_dirty_sessions)
    
    def _start_background_tasks(self):
        """Start background tasks for saving and cleanup."""
        # Save task
        self.save_thread = threading.Thread(target=self._periodic_save, daemon=True)
        self.save_thread.start()
        
        # Cleanup task
        self.cleanup_thread = threading.Thread(target=self._periodic_cleanup, daemon=True)
        self.cleanup_thread.start()
    
    def _periodic_save(self):
        """Periodically save dirty sessions to disk."""
        while True:
            time.sleep(self.save_interval)
            self._save_dirty_sessions()
    
    def _periodic_cleanup(self):
        """Periodically clean up old sessions."""
        while True:
            time.sleep(self.cleanup_interval)
            self._cleanup_old_sessions()
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session from cache or disk."""
        with self.lock:
            # Check cache first
            if session_id in self.cache:
                self.cache_timestamps[session_id] = time.time()
                return self.cache[session_id]
            
            # Load from disk if not in cache
            session_path = self.session_dir / f"{session_id}.json"
            if session_path.exists():
                try:
                    with open(session_path, 'r') as f:
                        session_data = json.load(f)
                    
                    # Add to cache
                    self.cache[session_id] = session_data
                    self.cache_timestamps[session_id] = time.time()
                    return session_data
                except Exception as e:
                    print(f"Error loading session {session_id}: {e}")
                    return None
            
            return None
    
    def save_session(self, session_id: str, session_data: Dict[str, Any], 
                    immediate: bool = False):
        """Save session to cache and optionally to disk."""
        with self.lock:
            # Update cache
            self.cache[session_id] = session_data
            self.cache_timestamps[session_id] = time.time()
            
            # Mark as dirty for background save
            self.dirty_sessions.add(session_id)
            
            # Save immediately if requested (for critical operations)
            if immediate:
                self._save_session_to_disk(session_id, session_data)
                self.dirty_sessions.discard(session_id)
    
    def _save_session_to_disk(self, session_id: str, session_data: Dict[str, Any]):
        """Save a single session to disk."""
        try:
            session_path = self.session_dir / f"{session_id}.json"
            temp_path = session_path.with_suffix('.tmp')
            
            # Write to temp file first
            with open(temp_path, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            # Atomic rename
            temp_path.replace(session_path)
            
        except Exception as e:
            print(f"Error saving session {session_id}: {e}")
    
    def _save_dirty_sessions(self):
        """Save all dirty sessions to disk."""
        with self.lock:
            if not self.dirty_sessions:
                return
            
            sessions_to_save = []
            for session_id in list(self.dirty_sessions):
                if session_id in self.cache:
                    sessions_to_save.append((session_id, self.cache[session_id].copy()))
            
            self.dirty_sessions.clear()
        
        # Save outside the lock to avoid blocking
        for session_id, session_data in sessions_to_save:
            self._save_session_to_disk(session_id, session_data)
    
    def _save_all_dirty_sessions(self):
        """Save all dirty sessions (called on exit)."""
        self._save_dirty_sessions()
    
    def delete_session(self, session_id: str):
        """Delete a session from cache and disk."""
        with self.lock:
            # Remove from cache
            self.cache.pop(session_id, None)
            self.cache_timestamps.pop(session_id, None)
            self.dirty_sessions.discard(session_id)
        
        # Delete from disk
        session_path = self.session_dir / f"{session_id}.json"
        if session_path.exists():
            try:
                session_path.unlink()
            except Exception as e:
                print(f"Error deleting session file {session_id}: {e}")
    
    def _cleanup_old_sessions(self):
        """Clean up sessions older than 24 hours."""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        # Clean disk sessions
        for session_file in self.session_dir.glob("*.json"):
            try:
                # Check file modification time
                mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
                if mtime < cutoff_time:
                    session_file.unlink()
                    print(f"Cleaned up old session: {session_file.name}")
            except Exception as e:
                print(f"Error cleaning up session {session_file}: {e}")
        
        # Clean cache entries
        with self.lock:
            current_time = time.time()
            expired_sessions = [
                sid for sid, timestamp in self.cache_timestamps.items()
                if current_time - timestamp > self.cache_ttl
            ]
            
            for session_id in expired_sessions:
                self.cache.pop(session_id, None)
                self.cache_timestamps.pop(session_id, None)
                self.dirty_sessions.discard(session_id)
    
    def evict_from_cache(self, session_id: str):
        """Manually evict a session from cache."""
        with self.lock:
            # Save if dirty before evicting
            if session_id in self.dirty_sessions and session_id in self.cache:
                self._save_session_to_disk(session_id, self.cache[session_id])
            
            self.cache.pop(session_id, None)
            self.cache_timestamps.pop(session_id, None)
            self.dirty_sessions.discard(session_id)
    
    def get_active_session_count(self) -> int:
        """Get count of active sessions in cache."""
        with self.lock:
            return len(self.cache)
    
    def get_session_ids(self) -> list:
        """Get all session IDs (from cache and disk)."""
        with self.lock:
            # Get from cache
            cached_ids = set(self.cache.keys())
        
        # Get from disk
        disk_ids = {f.stem for f in self.session_dir.glob("*.json")}
        
        return list(cached_ids | disk_ids)

# Global session manager instance
session_manager = SessionManager()