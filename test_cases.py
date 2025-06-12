#!/usr/bin/env python3
"""
Test the medical case caching system.
"""

from case_manager import case_manager

def test_case_loading():
    """Test that cases are loaded correctly."""
    print("🧪 Testing case loading...")
    
    # Test getting random cases
    easy_case = case_manager.get_random_case("easy", "general")
    if easy_case:
        print(f"✅ Easy general case: {easy_case['case_id']} - {easy_case['name']}")
    else:
        print("❌ No easy general cases found")
    
    medium_case = case_manager.get_random_case("medium", "general")
    if medium_case:
        print(f"✅ Medium general case: {medium_case['case_id']} - {medium_case['name']}")
    else:
        print("❌ No medium general cases found")
    
    cardiology_case = case_manager.get_random_case("hard", "cardiology")
    if cardiology_case:
        print(f"✅ Hard cardiology case: {cardiology_case['case_id']} - {cardiology_case['name']}")
    else:
        print("❌ No hard cardiology cases found")
    
    # Test case by ID
    specific_case = case_manager.get_case_by_id("easy_general_001")
    if specific_case:
        print(f"✅ Found specific case: {specific_case['name']}")
    else:
        print("❌ Could not find case by ID")
    
    print("\n📊 Case cache status:")
    case_manager._print_cache_summary()

if __name__ == "__main__":
    test_case_loading()