#!/usr/bin/env python3
"""
Test script to verify config and bot setup
"""

import sys
from config import Config
from job_application_bot import JobApplicationBot

def test_config():
    """Test config loading"""
    print("Testing config loading...")
    try:
        config = Config()
        print("✓ Config loaded successfully")
        
        # Test candidate data
        candidate = config.get_candidate()
        print(f"✓ Candidate: {candidate['full_name']}")
        
        # Test resume paths
        resume_master = config.get_resume_path("master")
        print(f"✓ Master resume path: {resume_master}")
        
        # Test platforms
        platforms = config.get_all_platforms()
        print(f"✓ Platforms configured: {', '.join(platforms.keys())}")
        
        # Test output dirs
        output_dirs = config.get_output_dirs()
        print(f"✓ Output directories created")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {str(e)}")
        return False

def test_bot():
    """Test bot initialization"""
    print("\nTesting bot initialization...")
    try:
        bot = JobApplicationBot(headless=True)
        print("✓ Bot initialized successfully")
        print(f"✓ Logger setup: {bot.logger.name}")
        print(f"✓ Candidate loaded: {bot.candidate['first_name']} {bot.candidate['last_name']}")
        return True
    except Exception as e:
        print(f"✗ Bot test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Job Application Bot - Setup Test")
    print("=" * 60)
    
    config_ok = test_config()
    bot_ok = test_bot()
    
    print("\n" + "=" * 60)
    if config_ok and bot_ok:
        print("✓ All tests passed! Ready to run applications.")
        print("\nNext steps:")
        print("1. Update open_applications_inventory.json with your job URLs")
        print("2. Run: python apply_all_refactored.py")
        return 0
    else:
        print("✗ Some tests failed. Check configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
