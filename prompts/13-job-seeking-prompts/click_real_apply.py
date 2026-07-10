import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Create a fresh page
            page = context.new_page()
            print("Navigating to Darwin AI job URL...")
            page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449/", wait_until="load")
            page.wait_for_timeout(8000)
            
            # Print page title and URL
            print(f"Page title: {page.title()}")
            print(f"Page URL: {page.url}")
            
            # Let's search for buttons on the page that have exactly 'Solicitar' or 'Apply' or similar
            buttons = page.query_selector_all("button")
            real_apply_btn = None
            
            for btn in buttons:
                text = btn.inner_text().strip()
                classes = btn.get_attribute("class") or ""
                # Check if it has class 'jobs-apply-button'
                if "jobs-apply-button" in classes:
                    real_apply_btn = btn
                    print(f"Found button with jobs-apply-button class: text='{text}'")
                    break
                # Check for exact text matches or 'Solicitar'
                if text == "Solicitar" or text == "Apply" or text == "Apply now":
                    real_apply_btn = btn
                    print(f"Found button with exact text: '{text}'")
                    break
                    
            if not real_apply_btn:
                # Let's search inside the top card container
                # The top card class is usually 'jobs-top-card' or contains 'topcard'
                topcard = page.query_selector("[class*='top-card']") or page.query_selector("[class*='topcard']")
                if topcard:
                    print("Found top card container, searching buttons inside it...")
                    topcard_buttons = topcard.query_selector_all("button")
                    for btn in topcard_buttons:
                        text = btn.inner_text().strip()
                        if text:
                            print(f"  Topcard button: '{text}'")
                        if "Solicitar" in text or "Apply" in text:
                            real_apply_btn = btn
                            print(f"  Found apply button in top card: '{text}'")
                            break
                            
            if not real_apply_btn:
                # Try finding any link inside the top card
                if topcard:
                    topcard_links = topcard.query_selector_all("a")
                    for link in topcard_links:
                        text = link.inner_text().strip()
                        if text:
                            print(f"  Topcard link: '{text}'")
                        if "Solicitar" in text or "Apply" in text:
                            real_apply_btn = link
                            print(f"  Found apply link in top card: '{text}'")
                            break

            if not real_apply_btn:
                # General search for elements containing 'Solicitar' or 'Apply' but not similar jobs
                all_links = page.query_selector_all("a")
                for link in all_links:
                    text = link.inner_text().strip()
                    classes = link.get_attribute("class") or ""
                    # Ensure it's not a similar job link
                    if ("Solicitar" in text or "Apply" in text) and "similar-jobs" not in (link.get_attribute("href") or ""):
                        real_apply_btn = link
                        print(f"Found link by general search: '{text}'")
                        break

            if real_apply_btn:
                print(f"Clicking real apply element: '{real_apply_btn.inner_text().strip()}'")
                real_apply_btn.click()
                print("Waiting 10 seconds for navigation or popup...")
                page.wait_for_timeout(10000)
                
                # Check open pages in context
                print(f"Active pages in context: {len(context.pages)}")
                for i, pg in enumerate(context.pages):
                    print(f"Page {i}: '{pg.title()}' - URL: '{pg.url}'")
                    pg.screenshot(path=f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_real_apply_{i}.png")
                    print(f"Saved screenshot for Page {i} to darwin_real_apply_{i}.png")
            else:
                print("Error: Could not find the real Apply button!")
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
