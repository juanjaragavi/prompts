import asyncio
import os
import json
from playwright.async_api import async_playwright

async def main():
    print("Starting Huzzle application process...")
    async with async_playwright() as p:
        # Launch headed chromium so we can see what's happening or debug if needed
        # Actually, headless is fine, but let's launch headless first.
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Navigate to the job offer on Jobgether to follow the redirect as instructed
        jobgether_url = "https://jobgether.com/offer/6a42ac022da8cde35c796a43-ai-engineer"
        print(f"Navigating to {jobgether_url}...")
        await page.goto(jobgether_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        
        # Take a screenshot on Jobgether
        await page.screenshot(path="/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/jobgether_offer.png")
        print("Took screenshot of Jobgether page.")
        
        # Find the Apply button on Jobgether and click it to go to Workable
        # Let's target the real Workable application button instead of internal auto-apply
        apply_btn = await page.query_selector("a[href*='workable']")
        if apply_btn:
            print("Found Workable apply button on Jobgether, clicking it...")
            # We can get the href or click it
            href = await apply_btn.get_attribute("href")
            if href:
                from urllib.parse import urljoin
                resolved_href = urljoin(page.url, href)
                print(f"Following link to: {resolved_href}")
                await page.goto(resolved_href, wait_until="domcontentloaded")
            else:
                await apply_btn.click()
        else:
            print("No explicit apply button found, navigating directly to Huzzle Workable apply page.")
            await page.goto("https://apply.workable.com/huzzle/j/C51C2BFA00/apply/", wait_until="domcontentloaded")
            
        await page.wait_for_timeout(4000)
        print(f"Current page URL: {page.url}")
        
        # Ensure we are on the apply page
        if "apply" not in page.url:
            print("Not on apply page, force navigating to the application form...")
            await page.goto("https://apply.workable.com/huzzle/j/C51C2BFA00/apply/", wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)
        # Hide cookie consent and backdrops so they don't block input clicks
        print("Bypassing cookie consent & backdrop blockers...")
        await page.evaluate("""() => {
            const consent = document.querySelector('[data-ui="cookie-consent"]');
            if (consent) {
                consent.remove ? consent.remove() : consent.style.display = 'none';
                console.log("Consent banner removed.");
            }
            
            const backdrops = document.querySelectorAll('[data-ui="backdrop"]');
            for (let b of backdrops) {
                b.remove ? b.remove() : b.style.display = 'none';
            }
            console.log("Backdrops removed.");
            
            document.body.style.pointerEvents = 'auto';
        }""")
        await page.wait_for_timeout(1000)
        
        # Fill Personal Information
        print("Filling personal information...")
        await page.fill("#firstname", "Juan Miguel")
        await page.fill("#lastname", "Jaramillo Gaviria")
        await page.fill("#email", "info@juanjaramillo.tech")
        
        # Phone
        # Phone input doesn't have an ID. We can fill it by using selector name=phone or input[type="tel"]
        await page.fill("input[type='tel']", "3054206139")
        
        # Select country code "Colombia" if there is a dropdown
        # Wait, the phone country code defaults to Colombia usually or is a combobox. Let's make sure it's set if needed.
        # But typing the full phone number or standard tel is usually fine. Let's try to click Colombia in the combobox if needed.
        try:
            # Let's see if we can find telephone country code input
            cc_combo = await page.query_selector("[aria-label*='country'], [class*='country'] select, .iti__selected-flag")
            if cc_combo:
                print("Phone country code found.")
        except Exception as e:
            print(f"Phone country code error: {e}")
            
        # Address, City, Postcode, Country
        await page.fill("#address", "Bogotá, Colombia")
        await page.fill("#city", "Bogotá")
        await page.fill("#postcode", "110111")
        await page.fill("#country", "Colombia")
        
        # Upload Resume
        # We need to find the correct file input. Let's find file inputs
        print("Uploading resume...")
        resume_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Resume.pdf"
        
        # In Workable, the resume input field is usually the second one or we can target the one inside the fieldset/container that contains "Resume"
        # Let's use locator that searches for file input under resume label/header or contains resume
        file_inputs = await page.query_selector_all("input[type='file']")
        print(f"Found {len(file_inputs)} file inputs.")
        
        # Let's inspect the file inputs to see which one is resume
        resume_input = None
        for fi in file_inputs:
            # Get parent text or id
            parent_text = await page.evaluate("el => el.closest('div').parentElement.textContent", fi)
            if "resume" in parent_text.lower():
                resume_input = fi
                break
                
        if not resume_input and len(file_inputs) > 0:
            # If not found by parent text, usually the second file input is Resume (first is photo, if any)
            # Or if only one, it is Resume. Let's use the last one if multiple, or the first if only one.
            # But let's check
            if len(file_inputs) == 1:
                resume_input = file_inputs[0]
            else:
                resume_input = file_inputs[1] # usually second in Workable
                
        if resume_input:
            # Upload the file
            await resume_input.set_input_files(resume_path)
            print("Uploaded resume successfully!")
        else:
            print("Warning: Resume file input not found!")
        
        await page.wait_for_timeout(2000)
        # Cover Letter
        print("Filling cover letter...")
        cover_letter_text = """Dear Hiring Team,

I am writing to express my strong interest in contributing to your AI-driven digital initiatives. With over 17 years of experience at the intersection of technology, entrepreneurship, and artificial intelligence, I bring a rare combination of executive vision and hands-on engineering capability — the kind of profile that can take an AI concept from whiteboard to production at every layer of the stack.

Since 2022, I have specialized exclusively in Generative AI, with a focused practice in LLM fine-tuning (PEFT, RLHF), prompt engineering, and enterprise AI architecture. As AI Development Lead at TopNetworks Inc., I designed and shipped an entire internal SaaS ecosystem — EmailGenius (AI email generation via Vertex AI + PostgreSQL), TrafficGenius (invalid traffic detection with BigQuery + Cloud Armor), RouteGenius (probabilistic traffic distribution on Supabase), and Social Media Genius (AI-powered social content generation with a canvas editor) — all on a modern stack including Next.js 15–16, TypeScript, React 19, Astro 5, and Gemini 2.5 Flash on Google Cloud.

What sets me apart is the ability to operate as a one-person AI center of excellence: architecting systems, writing the code, engineering the prompts, managing hallucination risk, and communicating strategy to non-technical stakeholders.

I am excited by the opportunity to bring this full-stack AI leadership to your organization and would welcome the chance to discuss how my experience aligns with your goals.

Warm regards,

Juan Miguel Jaramillo Gaviria
https://juanjaramillo.tech
info@juanjaramillo.tech
+57 305 420 6139
Bogotá, Colombia"""
        await page.fill("#cover_letter", cover_letter_text)
        
        # Details / Custom screening questions
        print("Filling custom details...")
        
        # English proficiency radio button
        # Native/Fluent has value "6144268". Let's check it by targeting value.
        try:
            await page.click("input[name='QA_11736001'][value='6144268']")
            print("Checked English Proficiency: Native/Fluent")
        except Exception as e:
            print(f"Failed to check English radio: {e}")
            
        # Business proficient languages
        await page.fill("#QA_11736002", "English, Spanish")
        
        # Timezones able to work in:
        # Checkboxes are: 6144273 (US), 6144274 (UK), 6144275 (Europe), 6144276 (Australia)
        try:
            await page.check("input[type='checkbox'][name='6144273']") # US
            await page.check("input[type='checkbox'][name='6144274']") # UK
            await page.check("input[type='checkbox'][name='6144275']") # Europe
            print("Checked timezones: US, UK, Europe")
        except Exception as e:
            print(f"Failed to check timezones: {e}")
            
        # Tools, software, platforms
        tools_text = "Languages: Python, JavaScript, TypeScript, SQL. AI & Machine Learning: Generative AI, LLMs, Vertex AI / Vertex AI Agent-to-Agent (A2A), LangChain, LangGraph, CrewAI, Prompt Engineering, Prompt Versioning (Git Flow), RAG Pipelines, Vector Databases, NLP, Cursor AI IDE, n8n Workflow Automation. Frameworks & Libraries: Next.js 15/16, React 19, Astro 5, Tailwind CSS v4, WordPress, Node.js. Cloud & Infrastructure: Google Cloud Platform (Cloud Run, Cloud Armor, BigQuery, Compute Engine, Cloud DNS), Supabase, PostgreSQL, Vercel, Docker, Git."
        await page.fill("#QA_11736004", tools_text)
        
        # Industries
        industries_text = "AI, Tech, SaaS, Marketing, E-commerce, Dropshipping, Publishing, Digital Advertising."
        await page.fill("#QA_11736008", industries_text)
        
        # Company type preferred: Open to all (6144280)
        try:
            await page.check("input[type='checkbox'][name='6144280']")
            print("Checked preferred company type: Open to all")
        except Exception as e:
            print(f"Failed to check company type: {e}")
            
        # Worked outside home country
        outside_text = "Yes. I have worked extensively with clients and companies based in the United States, United Kingdom, Spain, Mexico, and Guatemala."
        await page.fill("#QA_11736010", outside_text)
        
        # Salary expectations
        await page.fill("#QA_11736011", "3500 - 4500 USD")
        
        # Previous monthly salary
        prev_salary_text = "In my last role as AI Development Lead at TopNetworks Inc., my compensation was equivalent to $4,000 USD/month (as an independent contractor/remote developer)."
        await page.fill("#QA_11736012", prev_salary_text)
        
        # LinkedIn profile
        await page.fill("#QA_11736013", "https://www.linkedin.com/in/juan-jaramillo-ai/")
        
        # Dropdown: How did you hear about this opportunity?
        print("Selecting 'How did you hear about this opportunity?' dropdown...")
        try:
            await page.click("#input_QA_11736014_input")
            await page.wait_for_timeout(1000)
            
            # Click on the Job posting option (ends with _6144281)
            # Or click on Other (ends with _6144285)
            job_post_opt = await page.query_selector("[id$='_6144281']")
            if job_post_opt:
                await job_post_opt.click()
                print("Selected: Job posting")
            else:
                other_opt = await page.query_selector("[id$='_6144285']")
                if other_opt:
                    await other_opt.click()
                    print("Selected: Other")
        except Exception as e:
            print(f"Failed to select referral dropdown: {e}")
            
        # Take a screenshot of the completed form before submitting
        print("Capturing completed form screenshot...")
        filled_screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/huzzle_filled.png"
        await page.screenshot(path=filled_screenshot_path, full_page=True)
        print(f"Saved filled form screenshot to {filled_screenshot_path}")
        
        # Click submit
        print("Submitting the application...")
        submit_btn = await page.query_selector("button:has-text('Submit application')")
        if submit_btn:
            await submit_btn.click()
            print("Clicked submit button.")
            
            # Wait for 10 seconds to allow the page to reload or show success
            await page.wait_for_timeout(10000)
            
            # Take a post-submit screenshot
            success_screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/screenshot_additional_job_2_submitted.png"
            await page.screenshot(path=success_screenshot_path, full_page=True)
            print(f"Saved submission screenshot to {success_screenshot_path}")
            
            # Check for success indicators
            # In Workable, success page usually has "Thank you", "application received", or a checkmark
            page_content = await page.content()
            success_keywords = ["thank you", "received", "successfully", "applied", "application submitted"]
            is_success = any(kw in page_content.lower() for kw in success_keywords) or "confirmation" in page.url.lower()
            
            status = "Submitted" if is_success else "Pending Verification"
            print(f"Application Status Determined: {status}")
            
            # Draft and save status JSON
            status_data = {
                "company": "Huzzle.com",
                "position": "AI Engineer",
                "application_status": status,
                "screenshot_path": success_screenshot_path,
                "candidate_name": "Juan Miguel Jaramillo Gaviria",
                "submission_url": page.url,
                "answers": {
                    "English proficiency": "Native/Fluent",
                    "Business languages": "English, Spanish",
                    "Timezones": ["US", "UK", "Europe"],
                    "Tools, software & platforms": tools_text,
                    "Industries": industries_text,
                    "Preferred company type": "Open to all",
                    "Worked outside home country": outside_text,
                    "Salary expectation": "3500 - 4500 USD",
                    "Previous monthly salary": prev_salary_text,
                    "LinkedIn profile": "https://www.linkedin.com/in/juan-jaramillo-ai/"
                }
            }
            
            status_json_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/additional_application_2_status.json"
            with open(status_json_path, "w") as f:
                json.dump(status_data, f, indent=2)
            print(f"Saved application status to {status_json_path}")
            
        else:
            print("Error: Submit button not found!")
            
        await browser.close()
        print("Application run complete.")

if __name__ == "__main__":
    asyncio.run(main())
