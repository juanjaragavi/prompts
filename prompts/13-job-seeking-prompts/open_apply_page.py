import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Create a new page
            page = context.new_page()
            print("Navigating directly to job apply resources URL...")
            page.goto("https://www.linkedin.com/job-apply-resources/?jobPostingId=4255590650", wait_until="load")
            
            print("Waiting for page load...")
            page.wait_for_timeout(8000)
            
            print(f"Page Title: {page.title()}")
            print(f"Page URL: {page.url}")
            
            # Save screenshot
            page.screenshot(path="/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/trilogy_apply_page.png")
            print("Screenshot saved to trilogy_apply_page.png")
            
            # Let's save page HTML for inspection
            html_content = page.content()
            with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/trilogy_apply_page.html", "w") as f:
                f.write(html_content)
            print("Saved page source to trilogy_apply_page.html")
            
        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
