import sys
import re
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
                if "vibeast-4401002722" in url:
                    vibeast_page = page
                    break
            
            if not vibeast_page:
                print("Vibeast LinkedIn job page not found.")
                return
            
            print(f"Using Vibeast page: {vibeast_page.title()} | {vibeast_page.url}")
            vibeast_page.bring_to_front()
            
            # Print page text to see if there's any "Inicia sesión" or profile details
            text = vibeast_page.locator("body").inner_text()
            print("\n--- BODY TEXT EXCERPT ---")
            lines = text.split("\n")
            print("\n".join(lines[:30]))
            print("...")
            print("\n".join(lines[-30:]))
            print("-------------------------\n")
            
            # Let's search for any buttons or links with "solicitar" or "apply" or "sencilla"
            print("Locating all buttons...")
            buttons = vibeast_page.locator("button").all()
            print(f"Found {len(buttons)} button elements:")
            for idx, btn in enumerate(buttons):
                try:
                    btn_text = btn.inner_text().strip()
                    btn_html = btn.evaluate("el => el.outerHTML")
                    print(f"Button {idx}: '{btn_text}' | HTML: {btn_html[:200]}")
                except Exception as e:
                    print(f"Button {idx} error: {e}")
                    
            print("\nLocating all links...")
            links = vibeast_page.locator("a").all()
            print(f"Found {len(links)} link elements:")
            for idx, lnk in enumerate(links):
                try:
                    lnk_text = lnk.inner_text().strip()
                    lnk_href = lnk.get_attribute("href")
                    print(f"Link {idx}: '{lnk_text}' | Href: {lnk_href}")
                except Exception as e:
                    print(f"Link {idx} error: {e}")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
