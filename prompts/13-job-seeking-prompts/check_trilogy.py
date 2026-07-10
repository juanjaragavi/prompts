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
            
            # Let's check existing pages
            print("Existing pages:")
            for i, pg in enumerate(context.pages):
                print(f"Page {i}: '{pg.title()}' - {pg.url}")
                
            # Create a new page
            page = context.new_page()
            print("Navigating to Trilogy job URL...")
            page.goto("https://www.linkedin.com/jobs/view/vibe-coder-software-engineer-trilogy-remote-%2460-000-year-usd-at-trilogy-4255590650", wait_until="load")
            
            print("Waiting for page load...")
            page.wait_for_timeout(8000)
            
            print(f"Page Title: {page.title()}")
            print(f"Page URL: {page.url}")
            
            # Save screenshot
            page.screenshot(path="/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/trilogy_logged_in.png")
            print("Screenshot saved to trilogy_logged_in.png")
            
            # Check buttons
            buttons = page.query_selector_all("button")
            print(f"Found {len(buttons)} buttons:")
            for i, btn in enumerate(buttons):
                text = btn.inner_text().strip()
                if text:
                    classes = btn.get_attribute("class") or ""
                    print(f"Button {i}: text='{text}', class='{classes}'")
                    
            # Check links
            links = page.query_selector_all("a")
            print(f"Found {len(links)} links:")
            for i, link in enumerate(links):
                text = link.inner_text().strip()
                if text and ("apply" in text.lower() or "solicitar" in text.lower()):
                    classes = link.get_attribute("class") or ""
                    href = link.get_attribute("href") or ""
                    print(f"Link {i}: text='{text}', href='{href}', class='{classes}'")

        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
