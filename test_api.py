#!/usr/bin/env python3
"""
Test script to verify API functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /api/health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_specialties():
    """Test specialties endpoint"""
    print("\nTesting /api/specialties...")
    try:
        response = requests.get(f"{BASE_URL}/api/specialties")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('specialties', []))} specialties")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_game():
    """Test game creation"""
    print("\nTesting /api/game/create...")
    try:
        payload = {
            "role": "doctor",
            "difficulty": "medium",
            "specialty": "cardiology"
        }
        response = requests.post(f"{BASE_URL}/api/game/create", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Session ID: {data.get('session_id')}")
            print(f"Case: {data.get('case', {}).get('name', 'Unknown')}")
        else:
            print(f"Error response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing MedSim API...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Specialties", test_specialties),
        ("Create Game", test_create_game)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")