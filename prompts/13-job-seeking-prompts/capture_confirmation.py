import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Find the page with the Darwin AI job URL
            darwin_page = None
            for page in context.pages:
                if "4436992449" in page.url:
                    darwin_page = page
                    break
            
            if not darwin_page:
                print("Darwin AI page not found in active tabs, creating a new one...")
                darwin_page = context.new_page()
                darwin_page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449/")
                darwin_page.wait_for_timeout(8000)
            else:
                print(f"Found active tab: '{darwin_page.title()}'")
                darwin_page.bring_to_front()
                darwin_page.wait_for_timeout(3000)
            
            # Take a high-quality screenshot of the page showing "Application submitted"
            screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_application_submitted.png"
            darwin_page.screenshot(path=screenshot_path, full_page=False)
            print(f"Confirmation screenshot successfully captured and saved to {screenshot_path}")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
