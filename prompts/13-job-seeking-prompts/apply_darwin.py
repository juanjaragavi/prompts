import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            print(f"Contexts available: {len(browser.contexts)}")
            
            # Let's create a new page in the authenticated context
            page = context.new_page()
            print("Navigating to Darwin AI job URL...")
            page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449/")
            
            print("Waiting for page load...")
            page.wait_for_timeout(8000)
            
            print(f"Page Title: {page.title()}")
            print(f"Page URL: {page.url}")
            
            # Let's check if the apply button exists and what it is
            page.screenshot(path="/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_apply_page.png")
            print("Screenshot saved to /Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_apply_page.png")
            
        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
