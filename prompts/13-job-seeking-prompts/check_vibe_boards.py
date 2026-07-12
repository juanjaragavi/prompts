import sys
import json
from playwright.sync_api import sync_playwright

def main():
    boards = [
        "https://vibehackers.io/jobs",
        "https://remotevibecodingjobs.com/",
        "https://vibecodecareers.com/",
        "https://vibetown.pro/"
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        for url in boards:
            print(f"=== Visiting {url} ===")
            try:
                page.goto(url, wait_until="load", timeout=15000)
                page.wait_for_timeout(4000)
                body_text = page.locator("body").inner_text()
                print("Text length:", len(body_text))
                print(body_text[:1200])
                print("\n" + "="*40 + "\n")
            except Exception as e:
                print(f"Error visiting {url}: {e}")
                
        page.close()

if __name__ == "__main__":
    main()
