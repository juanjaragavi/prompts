import sys
import urllib.parse
from playwright.sync_api import sync_playwright

def main():
    query = 'vibe coding job'
    print(f"Connecting and searching DDG for: {query}")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        # Navigate to DDG HTML search
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        page.goto(url, wait_until="load")
        page.wait_for_timeout(4000)
        
        # Print page content or save it
        body_text = page.locator("body").inner_text()
        print("Text length:", len(body_text))
        print("Body Snippet:")
        print(body_text[:1000])
        
        page.screenshot(path="simple_search_ddg.png")
        
        # Save HTML
        with open("simple_search_ddg.html", "w") as f:
            f.write(page.content())
            
        page.close()

if __name__ == "__main__":
    main()
