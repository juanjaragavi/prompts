import sys
import json
import time
from playwright.sync_api import sync_playwright

urls = [
    "https://www.linkedin.com/jobs/view/vibe-coder-at-darwin-ai-4436992449",
    "https://www.linkedin.com/jobs/view/vibe-coder-ai-assisted-software-engineer-full-stack-ops00069-at-dev-pro-4403797050",
    "https://www.linkedin.com/jobs/view/programador-a-con-enfoque-vibe-coding-ia-at-inteligencia-artificial-4204687223",
    "https://www.linkedin.com/jobs/view/vibe-coder-software-engineer-trilogy-remote-%2460-000-year-usd-at-trilogy-4255590650",
    "https://www.linkedin.com/jobs/view/vibe-coding-engineer-at-helm-ai-4430831660",
    "https://www.linkedin.com/jobs/view/vibe-coding-intern-at-conquest-advisors-4437115289",
    "https://www.linkedin.com/jobs/view/vibe-coding-tutor-at-varsity-tutors-a-nerdy-company-4422163394",
    "https://www.linkedin.com/jobs/view/business-systems-analyst-salesforce-vibe-coding-at-cadence-4423988839"
]

def main():
    print("Connecting to Chrome over CDP on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected successfully!")
            context = browser.contexts[0]
            page = context.new_page()
            
            extracted_jobs = []
            
            for url in urls:
                print(f"Visiting URL: {url}...")
                page.goto(url, wait_until="load")
                page.wait_for_timeout(5000)
                
                # Check if job is closed or active
                # On LinkedIn, we can check for text "No longer accepting applications" or "No se admiten más solicitudes"
                page_text = page.locator("body").inner_text()
                closed_keywords = ["no longer accepting", "no se admiten", "closed", "cerrado", "expired", "expirado"]
                is_closed = any(kw in page_text.lower() for kw in closed_keywords)
                
                # Also check the status of the apply button
                # Let's extract: Title, Company, Description, Application Method
                try:
                    title_elem = page.query_selector("h1")
                    title = title_elem.inner_text().strip() if title_elem else "N/A"
                except Exception as e:
                    title = "N/A"
                    
                try:
                    # Company is often found in the sub-header or has class job-details-jobs-unified-top-card__company-name or similar
                    # Let's find links inside top card
                    company_elem = page.query_selector(".job-details-jobs-unified-top-card__company-name a")
                    if not company_elem:
                        company_elem = page.query_selector(".jobs-unified-top-card__company-name a")
                    if not company_elem:
                        company_elem = page.query_selector("span.jobs-unified-top-card__company-name")
                    company = company_elem.inner_text().strip() if company_elem else "N/A"
                except Exception as e:
                    company = "N/A"
                
                try:
                    # Let's get the full job description
                    # Usually .jobs-description__content or #job-details
                    desc_elem = page.query_selector("#job-details")
                    if not desc_elem:
                        desc_elem = page.query_selector(".jobs-description__content")
                    if not desc_elem:
                        desc_elem = page.query_selector(".jobs-box__html-content")
                    description = desc_elem.inner_text().strip() if desc_elem else "N/A"
                except Exception as e:
                    description = "N/A"
                    
                try:
                    # Find application type
                    # Look for easy apply button or regular apply
                    easy_apply = page.query_selector("button.jobs-apply-button")
                    if easy_apply:
                        easy_apply_text = easy_apply.inner_text().strip()
                        if "Easy Apply" in easy_apply_text or "Solicitud sencilla" in easy_apply_text:
                            app_type = "LinkedIn Easy Apply"
                        else:
                            app_type = "External Portal"
                    else:
                        # Let's check link elements with apply class
                        apply_link = page.query_selector("a.jobs-apply-button")
                        if apply_link:
                            app_type = "External Portal"
                        else:
                            app_type = "External Portal"
                except Exception as e:
                    app_type = "External Portal"
                
                status = "Closed" if is_closed else "Active"
                print(f"Extracted job: {title} at {company} | Status: {status} | App Type: {app_type}")
                
                extracted_jobs.append({
                    "company": company,
                    "title": title,
                    "job_url": url,
                    "description": description,
                    "application_type": app_type,
                    "status": status
                })
                
            with open("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/temp_checked_jobs.json", "w") as f:
                json.dump(extracted_jobs, f, indent=2)
            print("Successfully saved results to temp_checked_jobs.json")
            
        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
