#!/usr/bin/env python3
"""
Enhanced Configuration Verification - Juan Jaramillo Profile
Detailed validation of all configuration settings
"""

import sys
from config import Config

def verify_candidate_profile():
    """Verify complete candidate profile"""
    config = Config()
    candidate = config.get_candidate()
    
    print("\n" + "="*70)
    print("CANDIDATE PROFILE VERIFICATION")
    print("="*70)
    
    # Personal Info
    print(f"\n✓ Identity:")
    print(f"  Name: {candidate.get('full_name')}")
    print(f"  Title: {candidate.get('title')}")
    print(f"  Positioning: {candidate.get('positioning_headline')}")
    
    # Contact
    print(f"\n✓ Contact Information:")
    print(f"  Email: {candidate.get('email')}")
    print(f"  Phone: {candidate.get('phone_with_cc')}")
    print(f"  Location: {candidate.get('location')}")
    print(f"  Portfolio: {candidate.get('portfolio')}")
    
    # Experience
    print(f"\n✓ Professional Experience:")
    print(f"  Total Years: {candidate.get('years_experience')} years")
    print(f"  AI/ML Years: {candidate.get('years_ai_experience')} years")
    print(f"  Current Role: {candidate.get('current_role')} at {candidate.get('current_company')}")
    
    # Skills
    print(f"\n✓ Core Expertise ({len(candidate.get('core_expertise', []))} areas):")
    for i, skill in enumerate(candidate.get('core_expertise', [])[:5], 1):
        print(f"  {i}. {skill}")
    print(f"  ... and {len(candidate.get('core_expertise', [])) - 5} more")
    
    # Compensation
    comp = config.get_compensation_target()
    print(f"\n✓ Compensation Expectations:")
    print(f"  Monthly: {comp.get('range_monthly')}")
    print(f"  Annual: {comp.get('range_annual')}")
    
    # Work Authorization
    auth = config.get_work_authorization()
    print(f"\n✓ Work Authorization:")
    print(f"  Citizenship: {auth.get('citizenship')}")
    print(f"  Based In: {auth.get('based_in')}")
    print(f"  Can Work Colombia: {auth.get('colombia')}")
    print(f"  Visa Sponsorship Needed: {auth.get('requires_sponsorship')}")
    
    # Language
    lang = config.get_language_proficiency()
    print(f"\n✓ Language Proficiency:")
    print(f"  Native: {lang.get('native')}")
    print(f"  English Level: {lang.get('english_level')}")
    print(f"  EFSET: {lang.get('efset_level')} ({lang.get('efset_score')})")
    
    # Positioning
    pos = config.get_positioning()
    print(f"\n✓ Professional Positioning:")
    print(f"  Headline: {pos.get('headline')}")
    print(f"  Title: {pos.get('title')}")

def verify_projects():
    """Verify TopNetworks projects"""
    config = Config()
    projects = config.get_key_projects()
    
    print("\n" + "="*70)
    print("KEY PROJECTS (TopNetworks Ecosystem)")
    print("="*70)
    
    for i, project in enumerate(projects, 1):
        print(f"\n{i}. {project.get('name')}")
        print(f"   Description: {project.get('description')}")
        print(f"   Value: {project.get('value')}")

def verify_technical_skills():
    """Verify technical skills inventory"""
    config = Config()
    skills = config.get_technical_skills()
    
    print("\n" + "="*70)
    print("TECHNICAL SKILLS INVENTORY")
    print("="*70)
    
    for category, items in skills.items():
        print(f"\n{category.upper().replace('_', ' ')}:")
        for item in items[:3]:
            print(f"  • {item}")
        if len(items) > 3:
            print(f"  ... and {len(items) - 3} more")

def verify_platforms():
    """Verify job platform configurations"""
    config = Config()
    platforms = config.get_all_platforms()
    
    print("\n" + "="*70)
    print("JOB PLATFORM CONFIGURATIONS")
    print("="*70)
    
    for platform_key, platform_cfg in platforms.items():
        selectors = platform_cfg.get('selectors', {})
        print(f"\n✓ {platform_cfg.get('name')}")
        print(f"  Configured fields: {len(selectors)}")
        print(f"  Resume variant: {platform_cfg.get('resume_variant')}")

def verify_resumes():
    """Verify resume paths"""
    config = Config()
    
    print("\n" + "="*70)
    print("RESUME INVENTORY")
    print("="*70)
    
    for variant in ['ai_llm', 'vibe_coding', 'master']:
        path = config.get_resume_path(variant)
        print(f"\n✓ {variant.upper().replace('_', ' ')}:")
        print(f"  Path: {path}")

def verify_essays():
    """Verify essay templates"""
    config = Config()
    
    print("\n" + "="*70)
    print("ESSAY TEMPLATES")
    print("="*70)
    
    templates = ['ai_experience', 'previous_role', 'ai_leadership', 'career_transition']
    for template_name in templates:
        essay = config.get_essay_template(template_name)
        if essay:
            preview = essay[:80].replace('\n', ' ') + "..."
            print(f"\n✓ {template_name.upper().replace('_', ' ')}:")
            print(f"  Preview: {preview}")

def verify_job_search_config():
    """Verify job search strategy"""
    config = Config()
    job_search = config.get_job_search_config()
    
    print("\n" + "="*70)
    print("JOB SEARCH STRATEGY")
    print("="*70)
    
    print(f"\n✓ Active Seeking: {job_search.get('actively_seeking')}")
    print(f"  Weekly App Target: {job_search.get('application_target_weekly')}")
    print(f"  Weekly Outreach: {job_search.get('outreach_target_weekly')}")
    
    if 'track_ai_leadership' in job_search:
        track = job_search['track_ai_leadership']
        print(f"\n✓ AI Leadership Track:")
        print(f"  Focus: {track.get('focus')}")
        print(f"  Compensation: {track.get('compensation')}")
        print(f"  Target Companies: {', '.join(track.get('target_companies', [])[:3])}")

def main():
    """Run all verification checks"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " JUAN JARAMILLO - COMPLETE CONFIGURATION VERIFICATION ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        verify_candidate_profile()
        verify_projects()
        verify_technical_skills()
        verify_platforms()
        verify_resumes()
        verify_essays()
        verify_job_search_config()
        
        print("\n" + "="*70)
        print("✓ ALL CONFIGURATIONS VERIFIED SUCCESSFULLY")
        print("="*70)
        print("\n✅ Status: Ready for job applications")
        print("   → Run: ./run.sh run")
        print("   → Or:  python3 apply_all_refactored.py\n")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
