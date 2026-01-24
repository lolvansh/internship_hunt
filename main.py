import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def run_script(script_path, description=""):
    script_path = Path(script_path)

    print(f"\n{'='*60}")
    print(f"RUNNING: {script_path.name}")
    if description:
        print(f"DESCRIPTION: {description}")
    print(f"TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Check if script exists
    if not script_path.exists():
        print(f"❌ ERROR: Script not found at {script_path}")
        return False
    
    try:
        # Run the script with output streaming
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False,  # Shows output in real-time
            text=True
        )
        print(f"✅ SUCCESS: {script_path.name} completed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {script_path.name} failed with exit code {e.returncode}")
    except Exception as e:
        
        print(f"❌ UNEXPECTED ERROR running {script_path.name}: {e}")
        return False

def main():
    print("="*60)
    print("🚀 LEAD GENERATION AUTOMATION PIPELINE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    
    # Define pipeline steps
    pipeline = [
        {
            'script': 'comapany_details.py', 
            'description': 'Scraping company leads from Google Maps'
        },
        {
            'script': 'get_emails.py',
            'description': 'Fast email scraping (BS4 + Threads)'
        },
        {
            'script': 'retry_missed.py',
            'description': 'Deep email scraping (Playwright) for missed leads'
        },
        {
            'script': r'D:\python\cloud-cli\database\database.py',
            'description': 'Importing data to database'
        }
    ]
    
    
    for i, step in enumerate(pipeline, 1):
        print(f"\n📍 STEP {i}/{len(pipeline)}")
        
        if not run_script(step['script'], step['description']):
            print(f"\n❌ PIPELINE FAILED at step {i}: {step['script']}")

            print("Previous steps completed successfully")
            return False
    
    # Calculate duration
    duration = datetime.now() - start_time

    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETE - ALL STEPS SUCCESSFUL")
    print("="*60)
    print(f"Total duration: {duration}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)