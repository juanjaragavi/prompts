import sys
from playwright.sync_api import sync_playwright

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            
            # Find the page with the Darwin AI job URL
            darwin_page = None
            for page in context.pages:
                if "4436992449" in page.url:
                    darwin_page = page
                    break
            
            if not darwin_page:
                print("Darwin AI page not found in active tabs, creating a new one...")
                darwin_page = context.new_page()
                darwin_page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449/")
                darwin_page.wait_for_timeout(8000)
            else:
                print(f"Found active tab: '{darwin_page.title()}'")
                darwin_page.bring_to_front()
            
            print(f"Current page URL: {darwin_page.url}")
            
            # Let's find all buttons and links in the job card or top card
            # LinkedIn job top card action buttons are usually in .jobs-search__actions or .jobs-apply-button or similar
            print("Inspecting buttons...")
            buttons = darwin_page.query_selector_all("button")
            for i, btn in enumerate(buttons):
                text = btn.inner_text().strip()
                attrs = darwin_page.evaluate("(el) => { return { id: el.id, class: el.className, text: el.innerText }; }", btn)
                print(f"Button {i}: text='{attrs['text']}', class='{attrs['class']}', id='{attrs['id']}'")
                
            print("Inspecting links...")
            links = darwin_page.query_selector_all("a")
            for i, link in enumerate(links):
                text = link.inner_text().strip()
                if "Apply" in text or "Solicitar" in text or "jobs-apply" in (link.get_attribute("class") or ""):
                    attrs = darwin_page.evaluate("(el) => { return { href: el.href, class: el.className, text: el.innerText }; }", link)
                    print(f"Link {i}: text='{attrs['text']}', class='{attrs['class']}', href='{attrs['href']}'")
            
            darwin_page.screenshot(path="/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/darwin_inspect.png")
            print("Inspection screenshot saved.")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
