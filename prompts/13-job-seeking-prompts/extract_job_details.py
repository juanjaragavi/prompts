import sys
import json
import time
from playwright.sync_api import sync_playwright

def get_job_details(page, url):
    print(f"Navigating to {url}...")
    page.goto(url, wait_until="load")
    # Wait for the page to load initial content
    page.wait_for_timeout(5000)
    
    # Scroll down and up to trigger loading of skeleton elements
    for i in range(5):
        page.evaluate("window.scrollBy(0, 400)")
        page.wait_for_timeout(1000)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(2000)
    
    # Check if job is active or closed
    page_text = page.locator("body").inner_text()
    closed_keywords = ["no longer accepting applications", "no se admiten más solicitudes", "apply closed", "closed", "cerrado", "expired", "expirado"]
    # Usually "No longer accepting applications" is displayed in the top card or alerts
    # Let's check specifically if there is text "No longer accepting applications"
    is_closed = "no longer accepting applications" in page_text.lower() or "no se admiten más solicitudes" in page_text.lower()
    
    title = "N/A"
    try:
        # Try different selectors for Title
        title_selectors = [
            "h1.job-details-jobs-unified-top-card__job-title",
            "h1.t-24",
            "h1",
            ".jobs-unified-top-card__job-title"
        ]
        for sel in title_selectors:
            elem = page.query_selector(sel)
            if elem:
                txt = elem.inner_text().strip()
                if txt:
                    title = txt
                    break
    except Exception as e:
        pass
        
    company = "N/A"
    try:
        # Try different selectors for Company
        company_selectors = [
            ".job-details-jobs-unified-top-card__company-name a",
            ".jobs-unified-top-card__company-name a",
            "span.jobs-unified-top-card__company-name",
            ".job-details-jobs-unified-top-card__company-name",
            "a.app-shared-outline-custom"
        ]
        for sel in company_selectors:
            elem = page.query_selector(sel)
            if elem:
                txt = elem.inner_text().strip()
                if txt:
                    company = txt
                    break
    except Exception as e:
        pass

    description = "N/A"
    try:
        # Try different selectors for description
        desc_selectors = [
            "#job-details",
            ".jobs-description__content",
            ".jobs-box__html-content",
            "article.jobs-description__container"
        ]
        for sel in desc_selectors:
            elem = page.query_selector(sel)
            if elem:
                txt = elem.inner_text().strip()
                if txt and len(txt) > 50:
                    description = txt
                    break
    except Exception as e:
        pass
        
    app_type = "External Portal"
    try:
        # Try to find the apply button
        apply_btn = page.query_selector("button.jobs-apply-button")
        if apply_btn:
            btn_text = apply_btn.inner_text().strip()
            if "Easy Apply" in btn_text or "Solicitud sencilla" in btn_text:
                app_type = "LinkedIn Easy Apply"
            else:
                app_type = "External Portal"
        else:
            # Maybe there is an anchor instead
            apply_link = page.query_selector("a.jobs-apply-button")
            if apply_link:
                app_type = "External Portal"
    except Exception as e:
        pass

    status = "Closed" if is_closed else "Active"
    return {
        "company": company,
        "title": title,
        "job_url": url,
        "description": description,
        "application_type": app_type,
        "status": status
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_job_details.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        details = get_job_details(page, url)
        print(json.dumps(details, indent=2, ensure_ascii=False))
        
        # Take a screenshot to verify
        page.screenshot(path="extracted_job_view.png")
        page.close()

if __name__ == "__main__":
    main()
