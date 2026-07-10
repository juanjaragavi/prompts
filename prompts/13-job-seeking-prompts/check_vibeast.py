import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Find the Vibeast LinkedIn job page
            vibeast_page = None
            for page in context.pages:
                url = page.url
                title = page.title()
                if "vibeast-4401002722" in url:
                    vibeast_page = page
                    break
            
            if not vibeast_page:
                print("Vibeast LinkedIn job page not found. Creating a new one...")
                vibeast_page = context.new_page()
                vibeast_page.goto("https://www.linkedin.com/jobs/view/desarrollador-ai-native-vibe-coder-at-vibeast-4401002722/")
            
            print(f"Using Vibeast page: {vibeast_page.title()} | {vibeast_page.url}")
            vibeast_page.bring_to_front()
            vibeast_page.wait_for_timeout(3000)
            
            # Take a screenshot to inspect
            screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/vibeast_check.png"
            vibeast_page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            # Save HTML content
            html = vibeast_page.content()
            with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/vibeast_content.html", "w") as f:
                f.write(html)
            print("Content saved to vibeast_content.html")
            
            # Let's inspect the page content to see if "Solicitud sencilla" (Easy Apply) button exists
            print("Page HTML loaded. Searching for apply buttons...")
            import re
            buttons = re.findall(r'<button[^>]*>.*?</button>', html, re.IGNORECASE)
            links = re.findall(r'<a[^>]*>.*?</a>', html, re.IGNORECASE)
            
            print(f"Found {len(buttons)} buttons and {len(links)} links on the page.")
            for btn in buttons:
                if "solicit" in btn.lower() or "apply" in btn.lower() or "sencilla" in btn.lower() or "fácil" in btn.lower():
                    print(f"Match Button: {btn}")
            for lnk in links:
                if "solicit" in lnk.lower() or "apply" in lnk.lower() or "sencilla" in lnk.lower() or "fácil" in lnk.lower():
                    print(f"Match Link: {lnk}")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
