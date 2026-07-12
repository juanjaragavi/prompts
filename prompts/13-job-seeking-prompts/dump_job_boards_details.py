import sys
import json
from playwright.sync_api import sync_playwright

def main():
    urls = [
        "https://vibehackers.io/jobs",
        "https://remotevibecodingjobs.com/",
        "https://vibecodecareers.com/"
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        for url in urls:
            print(f"=== HTML DUMP FOR {url} ===")
            try:
                page.goto(url, wait_until="load", timeout=20000)
                page.wait_for_timeout(5000)
                
                # Let's save the page content
                filename = url.replace("https://", "").replace("/", "_").replace(".", "_") + ".html"
                with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/" + filename, "w") as f:
                    f.write(page.content())
                print(f"Saved to {filename}")
                
            except Exception as e:
                print(f"Error on {url}: {e}")
                
        page.close()

if __name__ == "__main__":
    main()
