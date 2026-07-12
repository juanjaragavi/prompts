from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449", wait_until="load")
        page.wait_for_timeout(5000)
        
        # Heuristic for title & company
        doc_title = page.title()
        print("Document Title:", doc_title)
        parts = [p.strip() for p in doc_title.split("|")]
        title = parts[0] if len(parts) > 0 else "N/A"
        company = parts[1] if len(parts) > 1 else "N/A"
        print("Extracted Title:", title)
        print("Extracted Company:", company)
        
        # Scroll to make sure content loads
        page.evaluate("window.scrollTo(0, 1000)")
        page.wait_for_timeout(2000)
        
        # Heuristic for description
        # 1. Expand text box if "Show more" or "... more" exists
        # Under [data-testid="expandable-text-box"], let's see if there's a button to expand
        expand_btn = page.query_selector('[data-testid="expandable-text-box"] button')
        if expand_btn:
            print("Found expand button inside text box, clicking...")
            expand_btn.click()
            page.wait_for_timeout(1000)
        else:
            # Maybe any button containing "more" or "Show more"
            more_btn = page.query_selector("button:has-text('more')")
            if more_btn:
                print("Found more button, clicking...")
                more_btn.click()
                page.wait_for_timeout(1000)
                
        desc_elem = page.query_selector('[data-testid="expandable-text-box"]')
        if desc_elem:
            description = desc_elem.inner_text().strip()
            print("Description length with data-testid:", len(description))
            print(description[:500])
        else:
            print("Could not find description with data-testid='expandable-text-box'")
            
        # Let's try general selectors
        print("Body text snippet containing 'What You'll Do':")
        body_text = page.locator("body").inner_text()
        if "What You'll Do" in body_text:
            print("Yes, 'What You'll Do' is in body text!")
            idx = body_text.find("What You'll Do")
            print(body_text[idx:idx+500])
            
        # Check closed status
        closed_keywords = ["no longer accepting applications", "no se admiten más solicitudes"]
        is_closed = any(kw in body_text.lower() for kw in closed_keywords)
        print("Is Closed:", is_closed)
        
        # Check application type (External or Easy Apply)
        easy_apply = "Easy Apply" in body_text or "Solicitud sencilla" in body_text
        print("Easy Apply text in body:", easy_apply)
        
        page.close()

if __name__ == "__main__":
    main()
