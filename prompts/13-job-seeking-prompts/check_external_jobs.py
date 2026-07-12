import sys
import json
import time
from playwright.sync_api import sync_playwright

urls = [
    "https://remotevibecodingjobs.com/jobs/fe2b15d1-9284-4644-b9a7-50ad2e0458d7",
    "https://vibehackers.io/jobs/aiml-computational-science-sr-analyst-accenture",
    "https://vibehackers.io/jobs/app-development-assistant-ai-assisted-vibe-coding-onsite-laguna-hills-dentco",
    "https://vibecodecareers.com/job/director-integration-automation-engineering-at-oura-remote-new-york-new-york/",
    "https://vibecodecareers.com/job/staff-software-engineer-at-ems-linq-denver-colorado/"
]

def main():
    print("Connecting to Chrome on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.new_page()
            
            extracted_jobs = []
            
            for url in urls:
                print(f"Visiting URL: {url}...")
                try:
                    page.goto(url, wait_until="load")
                    page.wait_for_timeout(4000)
                    
                    page_text = page.locator("body").inner_text()
                    title = page.title()
                    print(f"Loaded: '{title}' | Text length: {len(page_text)}")
                    
                    # Let's save a screenshot for each
                    safe_name = url.split("/")[-1] or url.split("/")[-2]
                    screenshot_path = f"job_view_{safe_name}.png"
                    page.screenshot(path=screenshot_path)
                    print(f"Screenshot saved to {screenshot_path}")
                    
                    # Save HTML
                    html_path = f"job_view_{safe_name}.html"
                    with open(html_path, "w") as f:
                        f.write(page.content())
                        
                    extracted_jobs.append({
                        "url": url,
                        "title_doc": title,
                        "text_len": len(page_text),
                        "snippet": page_text[:400]
                    })
                except Exception as e:
                    print(f"Error visiting {url}: {e}")
                    
            with open("external_jobs_checked.json", "w") as f:
                json.dump(extracted_jobs, f, indent=2)
            print("Successfully checked external jobs!")
            page.close()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
