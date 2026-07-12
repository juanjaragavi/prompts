import sys
import json
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome on 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected!")
            context = browser.contexts[0]
            page = context.new_page()
            
            # Visit the first job
            url = "https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449"
            print(f"Visiting {url}...")
            page.goto(url, wait_until="load")
            page.wait_for_timeout(5000)
            
            print("Page Title:", page.title())
            # Save screenshot to check if it's logged in or what it sees
            page.screenshot(path="test_darwin_view.png")
            print("Screenshot saved to test_darwin_view.png")
            
            # Print page content length and some text snippets
            text = page.locator("body").inner_text()
            print("Text length:", len(text))
            print("Snippets:")
            print(text[:1000])
            
            # Close page
            page.close()
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
