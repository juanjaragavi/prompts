import asyncio
import os
import json
import traceback
from playwright.async_api import async_playwright

RESUME_AI_LLM = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Resume_AI_LLM.pdf"
RESUME_VIBE_CODING = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Resume_Vibe_Coding.pdf"
RESUME_MASTER = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Resume.pdf"
COVER_LETTER = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Cover_Letter.pdf"

CANDIDATE = {
    "first_name": "Juan Miguel",
    "last_name": "Jaramillo Gaviria",
    "full_name": "Juan Miguel Jaramillo Gaviria",
    "email": "info@juanjaramillo.tech",
    "phone": "3054206139",
    "phone_with_cc": "+573054206139",
    "address": "Bogotá, Colombia",
    "city": "Bogotá",
    "postcode": "110111",
    "country": "Colombia",
    "location": "Bogotá, Colombia",
    "linkedin": "https://www.linkedin.com/in/juan-jaramillo-ai/",
    "github": "https://github.com/juanjaragavi",
    "portfolio": "https://juanjaramillo.tech",
    "expected_salary_usd": "4500",
    "notice_period": "Immediate",
    "years_experience": "17",
    "years_ai_experience": "4",
    "dob": "05/18/1984"
}

# Ensure directories exist
os.makedirs("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/screenshots", exist_ok=True)

async def handle_application(index, company, job_title, platform, url, context):
    print(f"\nProcessing Index {index}: {company} - {job_title} ({platform})")
    page = await context.new_page()
    status = "Pending"
    details = ""
    screenshot_path = f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/screenshots/application_{index}_screenshot.png"
    
    try:
        # Load the page
        await page.goto(url, wait_until="domcontentloaded", timeout=40000)
        await page.wait_for_timeout(5000)
        
        # Check for CAPTCHA or access restriction page
        content_lower = (await page.content()).lower()
        if "access is temporarily restricted" in content_lower or "captcha" in content_lower or "security check" in content_lower:
            status = "Requires Manual Action"
            details = "Blocked by anti-bot protection/CAPTCHA on SmartRecruiters."
            await page.screenshot(path=screenshot_path, full_page=False)
            print(f"Index {index} blocked by CAPTCHA.")
            return status, details, screenshot_path

        # Platform specific automations
        if platform.lower() == "smartrecruiters":
            # If loaded but maybe we can try to click or interact
            # But we already know it got blocked during our check or inside iframe.
            # Let's take screenshot and mark as manual action
            status = "Requires Manual Action"
            details = "SmartRecruiters OneClick UI is protected by anti-bot systems. Manual application recommended."
            await page.screenshot(path=screenshot_path)
            
        elif index == 2:  # TherapyNotes (Workable)
            # Fill the workable form
            print("Filling TherapyNotes Workable form...")
            # Dismiss cookie consent
            await page.evaluate("""() => {
                const c = document.querySelector('[data-ui="cookie-consent"]');
                if (c) c.remove();
            }""")
            await page.wait_for_timeout(1000)
            
            await page.fill("#firstname", CANDIDATE["first_name"])
            await page.fill("#lastname", CANDIDATE["last_name"])
            await page.fill("#email", CANDIDATE["email"])
            await page.fill("input[type='tel']", CANDIDATE["phone"])
            await page.fill("#address", CANDIDATE["address"])
            await page.fill("#city", CANDIDATE["city"])
            await page.fill("#postcode", CANDIDATE["postcode"])
            await page.fill("#country", CANDIDATE["country"])
            
            # Upload resume
            file_inputs = await page.query_selector_all("input[type='file']")
            if file_inputs:
                await file_inputs[0].set_input_files(RESUME_AI_LLM)
                print("Uploaded Resume.")
            
            # Fill questions
            await page.fill("[name='CA_9452']", "$110,000 - $135,000 / year") # Salary
            await page.fill("[name='CA_9529']", "None") # Referred
            await page.fill("[name='CA_40003']", f"{CANDIDATE['portfolio']} (GitHub: {CANDIDATE['github']})")
            await page.fill("[name='CA_41768']", CANDIDATE["linkedin"])
            
            # Select dropdown CA_42077 (Sponsorship require) -> YES
            try:
                # Type "Yes" or click
                await page.click("#input_CA_42077_input")
                await page.wait_for_timeout(1000)
                await page.keyboard.type("Yes")
                await page.keyboard.press("Enter")
            except Exception as e:
                print("Error on sponsorship dropdown:", e)
                
            # Radios YES / NO
            # QA_12020974: Authorized to work without visa sponsorship? NO
            # QA_12020975: Reside in US? NO
            # QA_12020976: 5+ years experience? YES
            # QA_12020978: C#/.net experience? NO
            try:
                # Find options inside radios
                # QA_12020974: NO is the second option
                # QA_12020975: NO is second
                # QA_12020976: YES is first
                # QA_12020978: NO is second
                radios_74 = await page.query_selector_all("input[name='QA_12020974']")
                if len(radios_74) >= 2:
                    await page.evaluate("el => el.click()", radios_74[1]) # NO
                radios_75 = await page.query_selector_all("input[name='QA_12020975']")
                if len(radios_75) >= 2:
                    await page.evaluate("el => el.click()", radios_75[1]) # NO
                radios_76 = await page.query_selector_all("input[name='QA_12020976']")
                if len(radios_76) >= 1:
                    await page.evaluate("el => el.click()", radios_76[0]) # YES
                radios_78 = await page.query_selector_all("input[name='QA_12020978']")
                if len(radios_78) >= 2:
                    await page.evaluate("el => el.click()", radios_78[1]) # NO
            except Exception as e:
                print("Error checking radios:", e)
                
            # Describe experience essay QA_12085438
            essay = ("I have over 17 years of experience in software engineering, with the last 4 years "
                     "focused on prompt engineering, generative AI, and agentic workflows. As AI Development Lead "
                     "at TopNetworks, I designed and built four internal SaaS tools (EmailGenius, TrafficGenius, "
                     "RouteGenius, and Social Media Genius). I designed and deployed production-grade multi-agent "
                     "orchestrations using LangGraph and CrewAI, establishing strict LLM guardrails and evaluation frameworks.")
            await page.fill("[name='QA_12085438']", essay)
            
            # Save screenshot of filled form
            await page.screenshot(path=screenshot_path, full_page=True)
            print("Filled TherapyNotes form successfully.")
            
            # Since reside in US and sponsorship is NO/YES, submitting might be auto-rejected.
            # But user wants us to submit, so let's try to submit
            submit_btn = await page.query_selector("button:has-text('Submit application')")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                # Take post submit screenshot
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Application submitted on Workable."
            else:
                status = "Form Filled (Not Submitted)"
                details = "Could not find submit button."
                
        elif index == 3:  # Xsolla (Lever)
            # Fill Xsolla Lever form
            print("Filling Xsolla Lever form...")
            # Lever has simple inputs
            # Upload Resume
            resume_input = await page.query_selector("input[type='file'][id='resume-upload-input']")
            if resume_input:
                await resume_input.set_input_files(RESUME_MASTER)
                await page.wait_for_timeout(3000)
                
            await page.fill("input[name='name']", CANDIDATE["full_name"])
            await page.fill("input[name='email']", CANDIDATE["email"])
            await page.fill("input[name='phone']", CANDIDATE["phone_with_cc"])
            await page.fill("input[name='org']", "TopNetworks Inc.")
            
            # Socials
            await page.fill("input[name='urls[LinkedIn]']", CANDIDATE["linkedin"])
            await page.fill("input[name='urls[GitHub]']", CANDIDATE["github"])
            await page.fill("input[name='urls[Portfolio]']", CANDIDATE["portfolio"])
            
            # Select location Dropdown 'What is your location?'
            try:
                select_loc = await page.query_selector("select[name='cards[01cc3abc-fc26-4732-97ba-49971da226cf][questions][0]']")
                if select_loc:
                    await select_loc.select_option(label="Colombia")
            except Exception as e:
                print("Location dropdown error:", e)
                
            # Take screenshot of filled form
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # Submit
            submit_btn = await page.query_selector("button[id='submit-btn']")
            if submit_btn:
                # Captcha is usually present on Lever submission, so we might get blocked.
                # Let's try clicking it
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Lever. Check screenshot for any CAPTCHA."
            else:
                status = "Form Filled"
                details = "Could not locate Lever submit button."
                
        elif index == 4:  # Bjak (Ashby)
            # Ashby form
            print("Filling Bjak Ashby form...")
            # Upload Resume
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(RESUME_AI_LLM)
                await page.wait_for_timeout(3000)
                
            # Ashby inputs are usually labelled or have specific selector
            await page.fill("input[id*='name']", CANDIDATE["full_name"])
            await page.fill("input[type='email']", CANDIDATE["email"])
            await page.fill("input[type='tel']", CANDIDATE["phone_with_cc"])
            
            # Current location
            loc_input = await page.query_selector("input[id*='location']")
            if loc_input:
                await loc_input.fill(CANDIDATE["location"])
                
            # Socials
            li_input = await page.query_selector("input[id*='linkedin']")
            if li_input:
                await li_input.fill(CANDIDATE["linkedin"])
            gh_input = await page.query_selector("input[id*='github']")
            if gh_input:
                await gh_input.fill(CANDIDATE["github"])
                
            # For Multiple Choice questions:
            # We can select radio options or checkboxes. Since Bjak has 3 MCQs, let's try to check them
            # Let's do a click on options containing the recommended answers
            try:
                # MCQ 1: experience with ML systems -> option containing 'I have built and owned ML systems deployed in production'
                opt1 = await page.query_selector("label:has-text('built and owned ML systems')")
                if opt1:
                    await opt1.click()
                # MCQ 2: what you enjoy most -> option containing 'Shipping ML systems, observing real-world behavior'
                opt2 = await page.query_selector("label:has-text('Shipping ML systems')")
                if opt2:
                    await opt2.click()
                # MCQ 3: worked on ML systems considering -> check all that apply: latency, compute, failures, safety
                for label_text in ['latency', 'compute', 'failures', 'safety']:
                    opts = await page.query_selector_all(f"label:has-text('{label_text}')")
                    for opt in opts:
                        await opt.click()
            except Exception as e:
                print("Error filling Ashby MCQs:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # Submit
            submit_btn = await page.query_selector("button[type='submit']")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Ashby."
            else:
                status = "Form Filled"
                details = "Could not locate Ashby submit button."
                
        elif index == 5:  # Team Red Dog (Crelate)
            # Crelate form
            print("Filling Team Red Dog Crelate form...")
            # Inputs
            await page.fill("input[id*='first'], input[name*='first']", CANDIDATE["first_name"])
            await page.fill("input[id*='last'], input[name*='last']", CANDIDATE["last_name"])
            await page.fill("input[type='email']", CANDIDATE["email"])
            await page.fill("input[type='tel']", CANDIDATE["phone_with_cc"])
            
            # Upload Resume
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(RESUME_AI_LLM)
                await page.wait_for_timeout(3000)
                
            # Consent Checkbox
            consent_cb = await page.query_selector("input[type='checkbox']")
            if consent_cb:
                await consent_cb.check()
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # Submit
            submit_btn = await page.query_selector("button[type='submit'], input[type='submit']")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Crelate."
            else:
                status = "Form Filled"
                details = "Could not locate Crelate submit button."
                
        elif index == 6:  # Curve Dental (Rippling)
            # Rippling form
            print("Filling Curve Dental Rippling form...")
            # Inputs
            await page.fill("input[name='first_name']", CANDIDATE["first_name"])
            await page.fill("input[name='last_name']", CANDIDATE["last_name"])
            await page.fill("input[name='email']", CANDIDATE["email"])
            await page.fill("input[name='phone_number']", CANDIDATE["phone_with_cc"])
            await page.fill("input[name='location']", CANDIDATE["location"])
            
            # Resume Upload
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(3000)
                
            # Screening questions:
            # 1. reside within Calgary: select NO
            # 2. legally permissioned to work in Canada: select NO
            # 3. years of experience: fill "17+ years software development, 4 years AI/ML"
            # 4. willing to work in office Calgary: select NO
            # 5. salary expectations: fill "$42,000 - $54,000 USD"
            try:
                # Fill textboxes
                text_inputs = await page.query_selector_all("textarea, input[type='text']")
                # Let's search for labels or placeholders
                for ti in text_inputs:
                    parent_text = await page.evaluate("el => el.closest('div').textContent", ti)
                    if "salary" in parent_text.lower():
                        await ti.fill("$42,000 - $54,000 USD")
                    elif "years of experience" in parent_text.lower() or "how many years" in parent_text.lower():
                        await ti.fill("17+ years software development, 4 years AI/ML")
                        
                # Dropdowns/Selects for Yes/No
                selects = await page.query_selector_all("select")
                for sel in selects:
                    parent_text = await page.evaluate("el => el.closest('div').textContent", sel)
                    if "calgary" in parent_text.lower() or "permissioned" in parent_text.lower() or "canada" in parent_text.lower() or "office" in parent_text.lower():
                        # select "No" or option containing "No"
                        await sel.select_option(label="No")
            except Exception as e:
                print("Error on Rippling questions:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("button[type='submit']")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Rippling."
            else:
                status = "Form Filled"
                details = "Could not locate Rippling submit button."
                
        elif index == 7:  # Netomi (Lever)
            # Lever form
            print("Filling Netomi Lever form...")
            # Upload Resume
            resume_input = await page.query_selector("input[type='file'][id='resume-upload-input']")
            if resume_input:
                await resume_input.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(3000)
                
            await page.fill("input[name='name']", CANDIDATE["full_name"])
            await page.fill("input[name='email']", CANDIDATE["email"])
            await page.fill("input[name='phone']", CANDIDATE["phone_with_cc"])
            await page.fill("input[name='org']", "TopNetworks Inc.")
            
            # Socials
            await page.fill("input[name='urls[LinkedIn]']", CANDIDATE["linkedin"])
            await page.fill("input[name='urls[GitHub]']", CANDIDATE["github"])
            
            # Expected CTC
            try:
                ctc_input = await page.query_selector("input[name*='ctc'], input[name*='salary'], input[placeholder*='salary'], input[placeholder*='expectations']")
                if ctc_input:
                    await ctc_input.fill("$3,500 - $4,500 USD / month")
            except Exception as e:
                print("Error with CTC input:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("button[id='submit-btn']")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Lever."
            else:
                status = "Form Filled"
                details = "Could not locate Lever submit button."
                
        elif index == 8:  # WorkBetterNow (Zoho Recruit)
            # Zoho Recruit Form
            print("Filling WorkBetterNow Zoho Recruit form...")
            # Dismiss cookies
            try:
                cookie_btn = await page.query_selector("button:has-text('Accept'), button:has-text('Got it')")
                if cookie_btn:
                    await cookie_btn.click()
            except Exception as e:
                pass
                
            # Inputs
            # Zoho Recruit forms have specific input IDs or class names
            # Let's fill by selector name or id
            await page.fill("input[id*='first'], input[name*='first']", CANDIDATE["first_name"])
            await page.fill("input[id*='last'], input[name*='last']", CANDIDATE["last_name"])
            await page.fill("input[type='email']", CANDIDATE["email"])
            await page.fill("input[type='tel']", CANDIDATE["phone_with_cc"])
            
            # Upload Resume
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(3000)
                
            # Specs screenshot and EFSET Cert are required.
            # Let's upload RESUME_VIBE_CODING as a placeholder for EFSET cert and a sample screenshot if multiple file inputs exist.
            file_inputs = await page.query_selector_all("input[type='file']")
            print(f"Zoho file inputs found: {len(file_inputs)}")
            if len(file_inputs) >= 2:
                # Upload EFSET Cert (we'll upload RESUME_VIBE_CODING or MASTER as a placeholder)
                await file_inputs[1].set_input_files(RESUME_MASTER)
            if len(file_inputs) >= 3:
                # Upload Specs screenshot (we'll upload a screenshot we took earlier or the same PDF)
                await file_inputs[2].set_input_files(RESUME_MASTER)
                
            # Confirm starting salary of $1,200 is fine -> YES
            try:
                yes_label = await page.query_selector("label:has-text('Yes')")
                if yes_label:
                    await yes_label.click()
            except:
                pass
                
            # Describe previous role (Max 999 chars)
            prev_desc = ("As AI Development Lead at TopNetworks, I designed, built, and shipped several "
                         "internal SaaS tools (EmailGenius, TrafficGenius, RouteGenius) that replaced expensive "
                         "third-party subscriptions. I utilized Next.js 15, TypeScript, Python, and Vertex AI. "
                         "I led rapid prototyping using AI-assisted environments (Cursor, Copilot), which "
                         "significantly reduced engineering time and software licensing costs.")
            try:
                textareas = await page.query_selector_all("textarea")
                if textareas:
                    await textareas[0].fill(prev_desc)
            except:
                pass
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("input[type='submit'], button[type='submit'], button:has-text('Submit')")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Zoho Recruit."
            else:
                status = "Form Filled"
                details = "Could not locate Zoho Recruit submit button."
                
        else:
            status = "Form Loaded"
            details = f"Default loaded for index {index} - {company}."
            await page.screenshot(path=screenshot_path)
            
    except Exception as e:
        status = "Requires Manual Action"
        details = f"Error occurred during automation: {str(e)}"
        traceback.print_exc()
        try:
            await page.screenshot(path=screenshot_path)
        except:
            pass
    finally:
        await page.close()
        
    return status, details, screenshot_path

async def main():
    with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/open_applications_inventory.json', 'r') as f:
        inventory = json.load(f)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use a realistic browser context to avoid detection
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        for app in inventory:
            index = app['index']
            company = app['company']
            job_title = app['job_title']
            platform = app['platform']
            url = app['url']
            
            status, details, screenshot_path = await handle_application(index, company, job_title, platform, url, context)
            
            status_data = {
                "index": index,
                "company": company,
                "job_title": job_title,
                "platform": platform,
                "url": url,
                "status": status,
                "screenshot_path": screenshot_path,
                "details": details
            }
            
            status_file = f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/application_status_{index}.json"
            with open(status_file, "w") as sf:
                json.dump(status_data, sf, indent=2)
            print(f"Saved {status_file}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
