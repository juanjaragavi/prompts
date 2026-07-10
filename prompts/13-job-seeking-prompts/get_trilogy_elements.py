import sys
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.new_page()
            page.goto("https://www.linkedin.com/jobs/view/vibe-coder-software-engineer-trilogy-remote-%2460-000-year-usd-at-trilogy-4255590650", wait_until="load")
            page.wait_for_timeout(8000)
            
            # Print page text content or some top parts to see if it says "No longer accepting applications"
            body_text = page.inner_text("body")
            print("Is 'no longer' in body text?", "no longer" in body_text.lower())
            print("Is 'no se aceptan' in body text?", "no se aceptan" in body_text.lower())
            print("Is 'apply' in body text?", "apply" in body_text.lower())
            print("Is 'solicitar' in body text?", "solicitar" in body_text.lower())
            
            # Let's search for any button or link containing certain keywords
            elements = page.query_selector_all("button, a")
            print(f"Total elements (buttons/links): {len(elements)}")
            for i, el in enumerate(elements):
                text = el.inner_text().strip()
                tag = el.evaluate("el => el.tagName")
                classes = el.get_attribute("class") or ""
                href = el.get_attribute("href") or "" if tag == "A" else ""
                
                # If the text has some relevant keywords
                lower_text = text.lower()
                if any(x in lower_text for x in ["apply", "solicitar", "enviar", "postul", "easy", "sencilla"]):
                    print(f"Element {i} [{tag}]: text='{text}', class='{classes}', href='{href}'")
            
            # Let's search inside job top card container
            print("\nSearching inside jobs-unified-top-card...")
            top_card = page.query_selector(".jobs-unified-top-card")
            if top_card:
                print("Found .jobs-unified-top-card!")
                sub_elements = top_card.query_selector_all("button, a")
                for j, sel in enumerate(sub_elements):
                    stext = sel.inner_text().strip()
                    stag = sel.evaluate("el => el.tagName")
                    sclasses = sel.get_attribute("class") or ""
                    shref = sel.get_attribute("href") or "" if stag == "A" else ""
                    print(f"  Topcard Element {j} [{stag}]: text='{stext}', class='{sclasses}', href='{shref}'")
            else:
                print("Could not find .jobs-unified-top-card")
                
            # Let's save page HTML for deep inspection
            html_content = page.content()
            with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/trilogy_page.html", "w") as f:
                f.write(html_content)
            print("Saved page source to trilogy_page.html")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
