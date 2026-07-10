import sys
import time
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Open page
            page = context.new_page()
            print("Navigating to Darwin AI job URL...")
            page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449/")
            
            print("Waiting for page load...")
            page.wait_for_timeout(8000)
            
            # Let's list all buttons
            buttons = page.query_selector_all("button")
            print(f"Found {len(buttons)} buttons on page.")
            for i, btn in enumerate(buttons):
                text = btn.inner_text().strip()
                if text:
                    print(f"Button {i}: '{text}'")
            
            # Find apply button. On LinkedIn jobs, it can have class 'jobs-apply-button' or text containing 'Solicitar' or 'Apply'
            apply_btn = None
            for btn in buttons:
                text = btn.inner_text().strip()
                # Check for "Solicitar", "Apply", or classes
                classes = btn.get_attribute("class") or ""
                if "Solicitar" in text or "Apply" in text or "jobs-apply-button" in classes:
                    apply_btn = btn
                    print(f"Found Apply Button: '{text}' with classes '{classes}'")
                    break
            
            if not apply_btn:
                # Also try looking for link with 'jobs-apply-button'
                apply_links = page.query_selector_all("a")
                for link in apply_links:
                    text = link.inner_text().strip()
                    classes = link.get_attribute("class") or ""
                    if "Solicitar" in text or "Apply" in text or "jobs-apply-button" in classes:
                        apply_btn = link
                        print(f"Found Apply Link: '{text}' with classes '{classes}'")
                        break
            
            if apply_btn:
                print("Clicking Apply button...")
                apply_btn.click()
                print("Waiting for 10 seconds after click...")
                page.wait_for_timeout(10000)
                
                # Check current pages in context (did it open a new tab?)
                print(f"Active pages in context: {len(context.pages)}")
                for i, pg in enumerate(context.pages):
                    print(f"Page {i}: Title: '{pg.title()}' URL: '{pg.url}'")
                    pg.screenshot(path=f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_page_{i}_after_click.png")
                    print(f"Saved screenshot for Page {i}")
            else:
                print("Apply button not found!")
                
        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
