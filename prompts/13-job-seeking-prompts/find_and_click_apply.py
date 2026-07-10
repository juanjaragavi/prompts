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
            
            # Create a brand new page to avoid interference from other tabs
            page = context.new_page()
            print("Navigating to Darwin AI job URL in a fresh page...")
            page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449/", wait_until="load")
            
            print("Waiting for page to fully load...")
            page.wait_for_timeout(8000)
            
            print(f"Loaded page title: '{page.title()}'")
            print(f"Loaded page URL: '{page.url}'")
            
            # Take a screenshot before clicking
            page.screenshot(path="/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_before_click.png")
            print("Screenshot before click saved.")
            
            # Find the actual apply button.
            # LinkedIn uses button.jobs-apply-button or div.jobs-apply-button button, etc.
            apply_btn = page.query_selector("button.jobs-apply-button")
            if not apply_btn:
                # Let's try finding by text or general class
                buttons = page.query_selector_all("button")
                for btn in buttons:
                    text = btn.inner_text().strip()
                    classes = btn.get_attribute("class") or ""
                    if "Solicitar" in text or "Apply" in text or "jobs-apply" in classes:
                        apply_btn = btn
                        break
            
            if not apply_btn:
                # Also try looking for an <a> link with apply class
                links = page.query_selector_all("a")
                for link in links:
                    text = link.inner_text().strip()
                    classes = link.get_attribute("class") or ""
                    if "Solicitar" in text or "Apply" in text or "jobs-apply" in classes:
                        apply_btn = link
                        break

            if apply_btn:
                btn_text = apply_btn.inner_text().strip()
                print(f"Found Apply Button/Link: '{btn_text}'")
                print("Clicking it...")
                apply_btn.click()
                print("Waiting 10 seconds for action...")
                page.wait_for_timeout(10000)
                
                # Check all open pages in context
                print(f"Active pages in context: {len(context.pages)}")
                for i, pg in enumerate(context.pages):
                    print(f"Page {i}: '{pg.title()}' - URL: '{pg.url}'")
                    pg.screenshot(path=f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_after_click_page_{i}.png")
                    print(f"Saved screenshot for Page {i} to darwin_after_click_page_{i}.png")
            else:
                print("Error: Could not find any Apply button on the page!")
                # Print some button texts to help debugging
                buttons = page.query_selector_all("button")
                print(f"List of all button texts found on page:")
                for i, btn in enumerate(buttons[:15]):
                    print(f"  {i}: '{btn.inner_text().strip()}'")
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
