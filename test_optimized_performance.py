#!/usr/bin/env python3
"""
Performance test suite for optimized MedSim codebase.
Compares performance between old and new implementations.
"""

import time
import asyncio
import statistics
from typing import List, Dict, Any
import json

# Test configurations
TEST_SESSIONS = 5
MESSAGES_PER_SESSION = 10

class PerformanceTest:
    """Test harness for comparing old vs new implementation."""
    
    def __init__(self):
        self.results = {
            "old": {"times": [], "errors": 0},
            "new": {"times": [], "errors": 0}
        }
    
    async def test_old_implementation(self):
        """Test the original implementation."""
        try:
            from core_medical_game import MedicalGameEngine
            engine = MedicalGameEngine()
            
            print("\n📊 Testing OLD implementation...")
            
            for i in range(TEST_SESSIONS):
                # Create session
                start_time = time.time()
                game_state = engine.create_game_session("doctor", "medium")
                session_id = game_state.session_id
                
                # Setup game
                engine.setup_doctor_game(session_id)
                
                # Send messages
                for j in range(MESSAGES_PER_SESSION):
                    message = f"What are the patient's symptoms? (test {j})"
                    engine.send_message(session_id, message)
                
                # End session
                engine.end_session(session_id)
                
                elapsed = time.time() - start_time
                self.results["old"]["times"].append(elapsed)
                print(f"  Session {i+1}: {elapsed:.2f}s")
                
        except Exception as e:
            print(f"  ❌ Error in old implementation: {e}")
            self.results["old"]["errors"] += 1
    
    async def test_new_implementation(self):
        """Test the optimized implementation."""
        try:
            from core_medical_game_optimized import OptimizedMedicalGameEngine
            engine = OptimizedMedicalGameEngine()
            
            print("\n📊 Testing NEW implementation...")
            
            for i in range(TEST_SESSIONS):
                # Create session
                start_time = time.time()
                game_state = engine.create_game_session("doctor", "medium")
                session_id = game_state.session_id
                
                # Setup game
                engine.setup_doctor_game(session_id)
                
                # Send messages (async)
                tasks = []
                for j in range(MESSAGES_PER_SESSION):
                    message = f"What are the patient's symptoms? (test {j})"
                    # Use sync wrapper for fair comparison
                    engine.send_message(session_id, message)
                
                # End session
                engine.end_session(session_id)
                
                elapsed = time.time() - start_time
                self.results["new"]["times"].append(elapsed)
                print(f"  Session {i+1}: {elapsed:.2f}s")
                
        except Exception as e:
            print(f"  ❌ Error in new implementation: {e}")
            self.results["new"]["errors"] += 1
    
    def compare_results(self):
        """Compare and display results."""
        print("\n" + "="*50)
        print("📈 PERFORMANCE COMPARISON RESULTS")
        print("="*50)
        
        # Old implementation stats
        if self.results["old"]["times"]:
            old_avg = statistics.mean(self.results["old"]["times"])
            old_min = min(self.results["old"]["times"])
            old_max = max(self.results["old"]["times"])
            
            print(f"\n🔴 OLD Implementation:")
            print(f"  Average time: {old_avg:.2f}s")
            print(f"  Min time: {old_min:.2f}s")
            print(f"  Max time: {old_max:.2f}s")
            print(f"  Errors: {self.results['old']['errors']}")
        
        # New implementation stats
        if self.results["new"]["times"]:
            new_avg = statistics.mean(self.results["new"]["times"])
            new_min = min(self.results["new"]["times"])
            new_max = max(self.results["new"]["times"])
            
            print(f"\n🟢 NEW Implementation:")
            print(f"  Average time: {new_avg:.2f}s")
            print(f"  Min time: {new_min:.2f}s")
            print(f"  Max time: {new_max:.2f}s")
            print(f"  Errors: {self.results['new']['errors']}")
        
        # Calculate improvement
        if self.results["old"]["times"] and self.results["new"]["times"]:
            old_avg = statistics.mean(self.results["old"]["times"])
            new_avg = statistics.mean(self.results["new"]["times"])
            improvement = ((old_avg - new_avg) / old_avg) * 100
            
            print(f"\n🚀 Performance Improvement: {improvement:.1f}%")
            print(f"   Speed increase: {old_avg/new_avg:.1f}x faster")

class FunctionalTest:
    """Test functionality to ensure nothing is broken."""
    
    async def test_all_endpoints(self):
        """Test all API endpoints."""
        print("\n🧪 Testing API Endpoints...")
        
        # Import FastAPI test client
        from fastapi.testclient import TestClient
        from api import app
        
        client = TestClient(app)
        
        tests = [
            # Test health check
            ("GET", "/api/health", None, 200),
            
            # Test game creation
            ("POST", "/api/game/create", {
                "role": "doctor",
                "difficulty": "medium"
            }, 200),
            
            # Test specialties
            ("GET", "/api/specialties", None, 200),
            
            # Test AdSense config
            ("GET", "/api/config/adsense", None, 200),
        ]
        
        passed = 0
        failed = 0
        
        for method, url, data, expected_status in tests:
            try:
                if method == "GET":
                    response = client.get(url)
                else:
                    response = client.post(url, json=data)
                
                if response.status_code == expected_status:
                    print(f"  ✓ {method} {url} - {response.status_code}")
                    passed += 1
                else:
                    print(f"  ❌ {method} {url} - {response.status_code} (expected {expected_status})")
                    failed += 1
                    
            except Exception as e:
                print(f"  ❌ {method} {url} - Error: {e}")
                failed += 1
        
        print(f"\n  Results: {passed} passed, {failed} failed")
        return failed == 0

class MemoryTest:
    """Test memory usage improvements."""
    
    def test_session_caching(self):
        """Test session caching behavior."""
        print("\n💾 Testing Session Caching...")
        
        try:
            from session_manager import session_manager
            
            # Create test sessions
            test_data = {"test": "data", "large": "x" * 1000}
            
            # Test save and retrieve
            start_time = time.time()
            for i in range(100):
                session_id = f"test_{i}"
                session_manager.save_session(session_id, test_data)
            
            save_time = time.time() - start_time
            print(f"  ✓ Saved 100 sessions in {save_time:.3f}s")
            
            # Test retrieval (should be from cache)
            start_time = time.time()
            for i in range(100):
                session_id = f"test_{i}"
                data = session_manager.get_session(session_id)
            
            retrieve_time = time.time() - start_time
            print(f"  ✓ Retrieved 100 sessions in {retrieve_time:.3f}s")
            
            # Check cache size
            active_count = session_manager.get_active_session_count()
            print(f"  ✓ Active sessions in cache: {active_count}")
            
            # Cleanup
            for i in range(100):
                session_manager.delete_session(f"test_{i}")
                
        except Exception as e:
            print(f"  ❌ Session caching error: {e}")

async def main():
    """Run all tests."""
    print("🏥 MedSim Optimization Test Suite")
    print("=================================")
    
    # Performance tests
    perf_test = PerformanceTest()
    
    # Test old implementation
    await perf_test.test_old_implementation()
    
    # Test new implementation
    await perf_test.test_new_implementation()
    
    # Compare results
    perf_test.compare_results()
    
    # Functional tests
    func_test = FunctionalTest()
    await func_test.test_all_endpoints()
    
    # Memory tests
    mem_test = MemoryTest()
    mem_test.test_session_caching()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())