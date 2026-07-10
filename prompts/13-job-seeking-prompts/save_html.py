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
            
            print(f"Page title: {page.title()}")
            print(f"Page URL: {page.url}")
            
            # Let's save the HTML
            html_content = page.content()
            with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_page.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Saved full page HTML to /Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_page.html")
            
            # Let's print all buttons with any text
            buttons = page.query_selector_all("button")
            print(f"Found {len(buttons)} buttons on page:")
            for i, btn in enumerate(buttons):
                text = btn.inner_text().strip()
                classes = btn.get_attribute("class") or ""
                id_val = btn.get_attribute("id") or ""
                if text:
                    print(f"  Button {i}: text='{text}', class='{classes}', id='{id_val}'")
            
            # Let's print all links with any text containing "Apply" or "Solicitar"
            links = page.query_selector_all("a")
            print(f"Found {len(links)} links on page. Checking for Apply/Solicitar:")
            for i, link in enumerate(links):
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                classes = link.get_attribute("class") or ""
                if text and ("Apply" in text or "Solicitar" in text):
                    print(f"  Link {i}: text='{text}', href='{href}', class='{classes}'")
                    
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
