import re
import json

def clean_html(text):
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

files = [
    ("job_view_fe2b15d1-9284-4644-b9a7-50ad2e0458d7.html", "https://remotevibecodingjobs.com/jobs/fe2b15d1-9284-4644-b9a7-50ad2e0458d7"),
    ("job_view_aiml-computational-science-sr-analyst-accenture.html", "https://vibehackers.io/jobs/aiml-computational-science-sr-analyst-accenture"),
    ("job_view_app-development-assistant-ai-assisted-vibe-coding-onsite-laguna-hills-dentco.html", "https://vibehackers.io/jobs/app-development-assistant-ai-assisted-vibe-coding-onsite-laguna-hills-dentco"),
    ("job_view_director-integration-automation-engineering-at-oura-remote-new-york-new-york.html", "https://vibecodecareers.com/job/director-integration-automation-engineering-at-oura-remote-new-york-new-york/"),
    ("job_view_staff-software-engineer-at-ems-linq-denver-colorado.html", "https://vibecodecareers.com/job/staff-software-engineer-at-ems-linq-denver-colorado/")
]

for fn, url in files:
    try:
        with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/" + fn, "r") as f:
            content = f.read()
            cleaned = clean_html(content)
            print(f"=== File: {fn} ===")
            print("Cleaned Length:", len(cleaned))
            print("Preview first 1500 chars:")
            print(cleaned[:1500])
            print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error reading {fn}: {e}")
