#!/usr/bin/env python3
"""
Case Generation Utility with Multi-LLM Support
Generates medical cases using Anthropic, OpenAI, or DeepSeek models.
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import List, Optional
from core_medical_game import MedicalGameEngine, Specialty, Difficulty
from llm_providers import set_llm_provider
from case_manager import case_manager


def setup_llm_provider(provider: str) -> None:
    """Set up the LLM provider for case generation."""
    try:
        llm = set_llm_provider(provider)
        print(f"🤖 Using LLM: {llm.get_provider_name()}")
    except Exception as e:
        print(f"❌ Failed to set LLM provider: {e}")
        sys.exit(1)


def generate_cases_for_all_specialties(count_per_combo: int = 1, delay: float = 2.0):
    """Generate cases for all difficulty levels and specialties."""
    
    # Initialize game engine (will use the configured LLM provider)
    game_engine = MedicalGameEngine()
    
    # Get all specialties and difficulties from enums
    all_specialties = [s.value for s in Specialty]
    all_difficulties = [d.value for d in Difficulty]
    
    total_generated = 0
    total_failed = 0
    
    print(f"🚀 Starting case generation...")
    print(f"Will generate {count_per_combo} case(s) for {len(all_difficulties)} difficulties × {len(all_specialties)} specialties")
    print(f"Total to generate: {len(all_difficulties) * len(all_specialties) * count_per_combo} cases")
    
    for difficulty in all_difficulties:
        print(f"\n📋 Generating {difficulty.upper()} cases...")
        
        for specialty in all_specialties:
            print(f"  🔹 {specialty}...", end='', flush=True)
            
            try:
                count = game_engine.generate_and_save_cases(
                    difficulty=difficulty,
                    specialty=specialty,
                    count=count_per_combo
                )
                total_generated += count
                
                if count == count_per_combo:
                    print(f" ✅ Generated {count} case(s)")
                else:
                    print(f" ⚠️  Generated {count}/{count_per_combo} cases")
                    total_failed += (count_per_combo - count)
                
                # Rate limiting between API calls
                time.sleep(delay)
                
            except Exception as e:
                print(f" ❌ Error: {str(e)}")
                total_failed += count_per_combo
                # Longer delay on error
                time.sleep(delay * 2)
    
    print(f"\n🎉 Case generation complete!")
    print(f"📊 Total cases generated: {total_generated}")
    if total_failed > 0:
        print(f"⚠️  Failed to generate: {total_failed} cases")


def generate_specific_cases(difficulty: str, specialty: str, count: int = 5, delay: float = 2.0):
    """Generate cases for a specific difficulty and specialty."""
    
    # Validate inputs
    if difficulty not in [d.value for d in Difficulty]:
        print(f"❌ Invalid difficulty: {difficulty}")
        print(f"Valid options: {', '.join([d.value for d in Difficulty])}")
        sys.exit(1)
    
    if specialty not in [s.value for s in Specialty]:
        print(f"❌ Invalid specialty: {specialty}")
        print(f"Valid options: {', '.join([s.value for s in Specialty])}")
        sys.exit(1)
    
    # Initialize game engine
    game_engine = MedicalGameEngine()
    
    print(f"🚀 Generating {count} cases for {difficulty}/{specialty}...")
    
    try:
        generated_count = game_engine.generate_and_save_cases(
            difficulty=difficulty,
            specialty=specialty,
            count=count
        )
        print(f"✅ Successfully generated {generated_count}/{count} cases")
        
    except Exception as e:
        print(f"❌ Error generating cases: {e}")


def list_available_options():
    """List all available difficulties and specialties."""
    print("📚 Available Options:")
    print("\nDifficulties:")
    for d in Difficulty:
        print(f"  - {d.value}")
    
    print("\nSpecialties:")
    for i, s in enumerate(Specialty):
        print(f"  - {s.value}")
        if (i + 1) % 3 == 0:  # New line every 3 specialties
            print()


def check_existing_cases(show_details: bool = False):
    """Check and display existing cases."""
    case_manager.load_all_cases()
    
    if show_details:
        case_manager.print_detailed_summary()


def main():
    """Main function for case generation."""
    parser = argparse.ArgumentParser(
        description="Generate medical cases using multiple LLM providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate cases for all specialties using Claude
  python generate_cases.py --all --model anthropic

  # Generate 5 cardiology cases using GPT-4
  python generate_cases.py --difficulty medium --specialty cardiovascular_disease --count 5 --model openai

  # Generate cases using DeepSeek with custom delay
  python generate_cases.py --all --model deepseek --delay 3

  # List available options
  python generate_cases.py --list

  # Check existing cases
  python generate_cases.py --check
        """
    )
    
    # LLM provider argument
    parser.add_argument(
        "--model", 
        type=str, 
        choices=["anthropic", "claude", "openai", "gpt4", "gpt-4", "deepseek", "deepseek-v3"],
        default="anthropic",
        help="LLM provider to use (default: anthropic)"
    )
    
    # Generation options
    parser.add_argument("--difficulty", help="Difficulty level")
    parser.add_argument("--specialty", help="Medical specialty")
    parser.add_argument("--count", type=int, default=5, help="Number of cases to generate (default: 5)")
    parser.add_argument("--all", action="store_true", help="Generate cases for all specialties")
    
    # Utility options
    parser.add_argument("--list", action="store_true", help="List available difficulties and specialties")
    parser.add_argument("--check", action="store_true", help="Check existing cases")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between API calls in seconds (default: 2.0)")
    
    args = parser.parse_args()
    
    # Handle utility commands
    if args.list:
        list_available_options()
        sys.exit(0)
    
    if args.check:
        check_existing_cases(show_details=True)
        sys.exit(0)
    
    # Set up LLM provider
    setup_llm_provider(args.model)
    
    # Load existing cases
    check_existing_cases(show_details=False)
    
    # Handle generation commands
    if args.all:
        # When using --all, default to 1 case per combination
        count = args.count if args.count != 5 else 1  # Use 1 unless explicitly set
        generate_cases_for_all_specialties(count_per_combo=count, delay=args.delay)
    elif args.difficulty and args.specialty:
        generate_specific_cases(args.difficulty, args.specialty, args.count, delay=args.delay)
    else:
        print("❌ Please specify generation options.")
        print("\nUse --help for usage examples")
        sys.exit(1)


if __name__ == "__main__":
    main()