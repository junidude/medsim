#!/usr/bin/env python3
"""
Add Multiple Choice (Differential Diagnoses) to existing cases
This script adds 4 differential diagnoses to each case file that doesn't already have them.
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any
from llm_providers import set_llm_provider, get_llm_provider


def generate_differential_diagnoses(case_data: Dict[str, Any], llm_provider) -> List[str]:
    """Generate 4 differential diagnoses for a given case using LLM."""
    
    # Create a prompt with case details
    prompt = f"""Given this medical case, provide exactly 4 differential diagnoses that would be reasonable to consider based on the presentation. Include the correct diagnosis among the 4 options.

Case Details:
- Chief Complaint: {case_data.get('chief_complaint', 'Not specified')}
- Symptoms: {', '.join(case_data.get('symptoms', []))}
- Physical Findings: {', '.join(case_data.get('physical_findings', []))}
- Specialty: {case_data.get('specialty', 'general').replace('_', ' ').title()}
- Correct Diagnosis: {case_data.get('name', 'Unknown')}

Requirements:
1. Include the correct diagnosis ({case_data.get('name', 'Unknown')}) as one of the 4 options
2. The other 3 should be plausible differential diagnoses that share similar symptoms
3. List them in random order (don't always put the correct answer first)
4. Keep each diagnosis name concise (2-4 words typically)
5. Make them appropriate for the difficulty level: {case_data.get('difficulty', 'medium')}

Return ONLY a JSON array with exactly 4 diagnosis names, like:
["Diagnosis 1", "Diagnosis 2", "Diagnosis 3", "Diagnosis 4"]
"""

    try:
        response = llm_provider.generate(
            prompt=prompt,
            system_prompt="You are a medical educator creating multiple choice questions. Return only valid JSON.",
            max_tokens=200
        )
        
        # Extract JSON from response
        json_start = response.find('[')
        json_end = response.rfind(']') + 1
        
        if json_start != -1 and json_end > json_start:
            diagnoses = json.loads(response[json_start:json_end])
            
            # Ensure we have exactly 4 options and the correct diagnosis is included
            if len(diagnoses) == 4:
                # Check if correct diagnosis is in the list (case-insensitive)
                correct_diagnosis = case_data.get('name', '')
                has_correct = any(diag.lower() == correct_diagnosis.lower() for diag in diagnoses)
                
                if not has_correct:
                    # Replace the first option with the correct diagnosis
                    diagnoses[0] = correct_diagnosis
                    # Shuffle to randomize position
                    import random
                    random.shuffle(diagnoses)
                
                return diagnoses
        
    except Exception as e:
        print(f"  ⚠️  Error generating DDx: {str(e)}")
    
    # Fallback: Create basic differential with correct answer
    correct = case_data.get('name', 'Unknown Condition')
    specialty = case_data.get('specialty', 'general')
    
    # Common differentials by specialty (fallback options)
    fallback_options = {
        'cardiology': ['Acute Coronary Syndrome', 'Heart Failure', 'Arrhythmia'],
        'emergency_medicine': ['Acute Abdomen', 'Sepsis', 'Trauma'],
        'neurology': ['Stroke', 'Migraine', 'Seizure Disorder'],
        'psychiatry': ['Major Depression', 'Anxiety Disorder', 'Bipolar Disorder'],
        'pediatrics': ['Viral Syndrome', 'Otitis Media', 'Asthma'],
        'internal_medicine': ['Diabetes Mellitus', 'Hypertension', 'COPD'],
        'gastroenterology': ['GERD', 'Peptic Ulcer Disease', 'IBD'],
        'dermatology': ['Contact Dermatitis', 'Psoriasis', 'Eczema'],
        'orthopedic_surgery': ['Fracture', 'Sprain', 'Arthritis'],
        'oncology': ['Lymphoma', 'Metastatic Disease', 'Leukemia']
    }
    
    # Get fallback options for the specialty
    options = fallback_options.get(specialty, ['Viral Infection', 'Bacterial Infection', 'Autoimmune Disorder'])
    
    # Create list with correct answer and 3 other options
    ddx = [correct] + options[:3]
    
    # Shuffle to randomize position
    import random
    random.shuffle(ddx)
    
    return ddx


def update_case_file(file_path: Path, llm_provider, dry_run: bool = False) -> bool:
    """Update a single case file with Multiple Choice options."""
    
    try:
        # Read existing case
        with open(file_path, 'r', encoding='utf-8') as f:
            case_data = json.load(f)
        
        # Check if already has Multiple Choice
        if 'multiple_choice' in case_data:
            return False  # Skip - already has DDx
        
        # Generate differential diagnoses
        ddx = generate_differential_diagnoses(case_data, llm_provider)
        
        # Add to case data
        case_data['multiple_choice'] = ddx
        
        # Save updated case (unless dry run)
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(case_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Updated: {file_path.name}")
        print(f"     DDx: {ddx}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error updating {file_path}: {str(e)}")
        return False


def process_all_cases(cases_dir: Path, llm_provider, dry_run: bool = False, 
                     delay: float = 1.0, limit: int = None) -> Dict[str, int]:
    """Process all case files in the cases directory."""
    
    stats = {
        'total': 0,
        'updated': 0,
        'skipped': 0,
        'errors': 0
    }
    
    # Find all JSON files
    case_files = list(cases_dir.rglob('*.json'))
    print(f"\n📊 Found {len(case_files)} case files")
    
    if limit:
        case_files = case_files[:limit]
        print(f"   (Processing first {limit} files only)")
    
    # Process each file
    for i, file_path in enumerate(case_files):
        stats['total'] += 1
        
        # Show progress
        print(f"\n[{i+1}/{len(case_files)}] Processing: {file_path.relative_to(cases_dir)}")
        
        # Check if already has multiple_choice
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                case_data = json.load(f)
                if 'multiple_choice' in case_data:
                    print("  ⏭️  Skipped - already has Multiple Choice")
                    stats['skipped'] += 1
                    continue
        except:
            pass
        
        # Update the file
        if update_case_file(file_path, llm_provider, dry_run):
            stats['updated'] += 1
        else:
            stats['errors'] += 1
        
        # Rate limiting
        if i < len(case_files) - 1:  # Don't delay after last file
            time.sleep(delay)
    
    return stats


def main():
    """Main function to add differential diagnoses to cases."""
    
    parser = argparse.ArgumentParser(
        description="Add Multiple Choice (differential diagnoses) to existing cases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update all cases using Claude (default)
  python add_ddx_to_cases.py

  # Update using GPT-4
  python add_ddx_to_cases.py --model openai

  # Dry run - see what would be updated without making changes
  python add_ddx_to_cases.py --dry-run

  # Update only first 10 cases (for testing)
  python add_ddx_to_cases.py --limit 10

  # Custom delay between API calls
  python add_ddx_to_cases.py --delay 2.0
        """
    )
    
    parser.add_argument(
        "--model",
        type=str,
        choices=["anthropic", "claude", "openai", "gpt4", "gpt-4", "deepseek", "deepseek-v3"],
        default="anthropic",
        help="LLM provider to use (default: anthropic)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between API calls in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of files to process (for testing)"
    )
    
    parser.add_argument(
        "--cases-dir",
        type=str,
        default="cases",
        help="Directory containing case files (default: cases)"
    )
    
    args = parser.parse_args()
    
    # Set up LLM provider
    try:
        llm_provider = set_llm_provider(args.model)
        print(f"🤖 Using LLM: {llm_provider.get_provider_name()}")
    except Exception as e:
        print(f"❌ Failed to set LLM provider: {e}")
        sys.exit(1)
    
    # Check cases directory
    cases_dir = Path(args.cases_dir)
    if not cases_dir.exists():
        print(f"❌ Cases directory not found: {cases_dir}")
        sys.exit(1)
    
    print("\n🔄 Adding Multiple Choice to existing cases...")
    if args.dry_run:
        print("   (DRY RUN - no files will be modified)")
    print("=" * 60)
    
    # Process all cases
    stats = process_all_cases(
        cases_dir=cases_dir,
        llm_provider=llm_provider,
        dry_run=args.dry_run,
        delay=args.delay,
        limit=args.limit
    )
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   Total files: {stats['total']}")
    print(f"   ✅ Updated: {stats['updated']}")
    print(f"   ⏭️  Skipped: {stats['skipped']}")
    print(f"   ❌ Errors: {stats['errors']}")
    
    if args.dry_run:
        print("\n💡 This was a dry run. To actually update files, run without --dry-run")
    else:
        print("\n✨ Update complete!")


if __name__ == "__main__":
    main()