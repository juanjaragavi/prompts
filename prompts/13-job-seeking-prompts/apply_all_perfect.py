import asyncio
import os
import json
import traceback
from playwright.async_api import async_playwright

RESUME_AI_LLM = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Resume_AI_LLM.pdf"
RESUME_VIBE_CODING = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Resume_Vibe_Coding.pdf"
RESUME_MASTER = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Resume.pdf"
COVER_LETTER = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Cover_Letter.pdf"
SPECS_SCREENSHOT = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/System_Specs_Screenshot.png"
EFSET_CERTIFICATE = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/EFSET_Certificate.pdf"

CANDIDATE = {
    "first_name": "Juan Miguel",
    "last_name": "Jaramillo Gaviria",
    "full_name": "Juan Miguel Jaramillo Gaviria",
    "email": "juanamillo@proton.me",
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
    "dob": "02/06/1984"
}

os.makedirs("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/screenshots", exist_ok=True)

async def handle_application(index, company, job_title, platform, url, context):
    print(f"\nProcessing Index {index}: {company} - {job_title} ({platform})")
    page = await context.new_page()
    status = "Pending"
    details = ""
    screenshot_path = f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/screenshots/application_{index}_screenshot.png"
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=40000)
        await page.wait_for_timeout(5000)
        
        content_lower = (await page.content()).lower()
        if "access is temporarily restricted" in content_lower or "security check" in content_lower and platform.lower() == "smartrecruiters":
            status = "Requires Manual Action"
            details = "Blocked by SmartRecruiters anti-bot protection/CAPTCHA. Manual submission required."
            await page.screenshot(path=screenshot_path)
            print(f"Index {index} blocked by SmartRecruiters Cloudflare/anti-bot shield.")
            return status, details, screenshot_path

        # Platform specific automations
        if index == 1: # Medfar (SmartRecruiters)
            status = "Requires Manual Action"
            details = "SmartRecruiters OneClick UI is protected by anti-bot systems. Manual application recommended."
            await page.screenshot(path=screenshot_path)

        elif index == 2:  # TherapyNotes (Workable)
            print("Filling TherapyNotes Workable form...")
            # Dismiss cookie consent
            await page.evaluate("""() => {
                const c = document.querySelector('[data-ui="cookie-consent"]');
                if (c) c.remove();
                const b = document.querySelector('[data-ui="backdrop"]');
                if (b) b.remove();
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
            
            file_inputs = await page.query_selector_all("input[type='file']")
            if file_inputs:
                await file_inputs[0].set_input_files(RESUME_AI_LLM)
                print("Uploaded Resume to Workable.")
            
            await page.fill("[name='CA_9452']", "$110,000 - $135,000 / year")
            await page.fill("[name='CA_9529']", "None")
            await page.fill("[name='CA_40003']", f"{CANDIDATE['portfolio']} (GitHub: {CANDIDATE['github']})")
            await page.fill("[name='CA_41768']", CANDIDATE["linkedin"])
            
            try:
                await page.click("#input_CA_42077_input")
                await page.wait_for_timeout(1000)
                await page.keyboard.type("Yes")
                await page.keyboard.press("Enter")
            except Exception as e:
                print("Error on sponsorship dropdown:", e)
                
            try:
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
                
            essay = ("I have over 17 years of experience in software engineering, with the last 4 years "
                     "focused on prompt engineering, generative AI, and agentic workflows. As AI Development Lead "
                     "at TopNetworks, I designed and built four internal SaaS tools (EmailGenius, TrafficGenius, "
                     "RouteGenius, and Social Media Genius). I designed and deployed production-grade multi-agent "
                     "orchestrations using LangGraph and CrewAI, establishing strict LLM guardrails and evaluation frameworks.")
            await page.fill("[name='QA_12085438']", essay)
            
            await page.screenshot(path=screenshot_path, full_page=True)
            print("Filled TherapyNotes form successfully.")
            
            submit_btn = await page.query_selector("button:has-text('Submit application')")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Application submitted on Workable."
            else:
                status = "Form Filled"
                details = "Could not find submit button."

        elif index == 3:  # Xsolla (Lever)
            print("Filling Xsolla Lever form...")
            resume_input = await page.query_selector("input[type='file'][id='resume-upload-input']")
            if resume_input:
                await resume_input.set_input_files(RESUME_MASTER)
                await page.wait_for_timeout(3000)
                
            await page.fill("input[name='name']", CANDIDATE["full_name"])
            await page.fill("input[name='email']", CANDIDATE["email"])
            await page.fill("input[name='phone']", CANDIDATE["phone_with_cc"])
            await page.fill("input[name='org']", "TopNetworks Inc.")
            
            await page.fill("input[name='urls[LinkedIn]']", CANDIDATE["linkedin"])
            await page.fill("input[name='urls[GitHub]']", CANDIDATE["github"])
            await page.fill("input[name='urls[Portfolio]']", CANDIDATE["portfolio"])
            
            try:
                select_loc = await page.query_selector("select[name*='questions']")
                if select_loc:
                    await select_loc.select_option(label="Colombia")
            except Exception as e:
                print("Location dropdown error:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("#btn-submit")
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Lever. Check screenshot for any CAPTCHA or success check."
            else:
                status = "Form Filled"
                details = "Could not locate Lever submit button."

        elif index == 4:  # Bjak (Ashby)
            print("Filling Bjak Ashby form...")
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(RESUME_AI_LLM)
                await page.wait_for_timeout(3000)
                
            await page.fill("input[id*='name'], input[name='name']", CANDIDATE["full_name"])
            await page.fill("input[type='email'], input[name='email']", CANDIDATE["email"])
            await page.fill("input[type='tel'], input[name='phone']", CANDIDATE["phone_with_cc"])
            
            loc_input = await page.query_selector("input[id*='location'], input[name*='location']")
            if loc_input:
                await loc_input.fill(CANDIDATE["location"])
                
            li_input = await page.query_selector("input[id*='linkedin'], input[name*='linkedin']")
            if li_input:
                await li_input.fill(CANDIDATE["linkedin"])
            gh_input = await page.query_selector("input[id*='github'], input[name*='github']")
            if gh_input:
                await gh_input.fill(CANDIDATE["github"])
                
            try:
                opt1 = await page.query_selector("label:has-text('built and owned ML systems')")
                if opt1:
                    await opt1.click()
                opt2 = await page.query_selector("label:has-text('Shipping ML systems')")
                if opt2:
                    await opt2.click()
                for label_text in ['latency', 'compute', 'failures', 'safety']:
                    opts = await page.query_selector_all(f"label:has-text('{label_text}')")
                    for opt in opts:
                        await opt.click()
            except Exception as e:
                print("Error filling Ashby MCQs:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("button.ashby-application-form-submit-button, button:has-text('Submit Application')")
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
            print("Filling Team Red Dog Crelate form...")
            await page.fill("#firstName", CANDIDATE["first_name"])
            await page.fill("#lastName", CANDIDATE["last_name"])
            await page.fill("#email", CANDIDATE["email"])
            await page.fill("#phone", CANDIDATE["phone_with_cc"])
            
            resume_input = await page.query_selector("#file-uploadResume")
            if resume_input:
                await resume_input.set_input_files(RESUME_AI_LLM)
                await page.wait_for_timeout(3000)
                
            consent_cb = await page.query_selector("input[type='checkbox']")
            if consent_cb:
                await consent_cb.check()
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("#submitButton")
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
            print("Filling Curve Dental Rippling form...")
            await page.fill("#field-8", CANDIDATE["first_name"])
            await page.fill("#field-12", CANDIDATE["last_name"])
            await page.fill("#field-16", CANDIDATE["email"])
            await page.fill("#field-31", CANDIDATE["phone_with_cc"])
            await page.fill("#field-42", CANDIDATE["location"])
            await page.fill("#field-27", "TopNetworks Inc.")
            
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(3000)
                
            await page.fill("#field-61", "$42,000 - $54,000 USD")
            await page.fill("#field-65", "17 years software engineering, 4 years AI/ML")
            
            try:
                for f_id in ["#field-55", "#field-69", "#field-75"]:
                    trigger = await page.query_selector(f_id)
                    if trigger:
                        await trigger.click()
                        await page.wait_for_timeout(1000)
                        no_option = await page.query_selector("div[role='option']:has-text('No'), li:has-text('No'), span:has-text('No')")
                        if no_option:
                            await no_option.click()
                            print(f"Selected NO for {f_id}")
                        else:
                            await page.keyboard.type("No")
                            await page.keyboard.press("Enter")
            except Exception as e:
                print("Error with Rippling dropdowns:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            # Since Rippling requires specific location matching, submit_btn might remain disabled
            # If so, we capture it and mark as Requires Manual Action
            submit_btn = await page.query_selector("button[type='submit']")
            if submit_btn and await submit_btn.is_enabled():
                await submit_btn.click()
                await page.wait_for_timeout(6000)
                await page.screenshot(path=screenshot_path, full_page=True)
                status = "Submitted"
                details = "Form submitted on Rippling."
            else:
                status = "Requires Manual Action"
                details = "Rippling submit button remained disabled (potentially due to strict Canadian location filters)."

        elif index == 7:  # Netomi (Lever)
            print("Filling Netomi Lever form...")
            resume_input = await page.query_selector("input[type='file'][id='resume-upload-input']")
            if resume_input:
                await resume_input.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(3000)
                
            await page.fill("input[name='name']", CANDIDATE["full_name"])
            await page.fill("input[name='email']", CANDIDATE["email"])
            await page.fill("input[name='phone']", CANDIDATE["phone_with_cc"])
            await page.fill("input[name='org']", "TopNetworks Inc.")
            
            await page.fill("input[name='urls[LinkedIn]']", CANDIDATE["linkedin"])
            await page.fill("input[name='urls[GitHub / Other]']", CANDIDATE["github"])
            
            try:
                ctc_input = await page.query_selector("input[name*='ctc'], input[name*='salary'], input[placeholder*='salary'], input[placeholder*='expectations']")
                if ctc_input:
                    await ctc_input.fill("$3,500 - $4,500 USD / month")
            except Exception as e:
                print("Expected CTC field fill error:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("#btn-submit")
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
            print("Filling WorkBetterNow Zoho Recruit form...")
            try:
                cookie_btn = await page.query_selector("button:has-text('Accept'), button:has-text('Got it')")
                if cookie_btn:
                    await cookie_btn.click()
            except Exception as e:
                pass
                
            apply_btn = await page.query_selector("button:has-text('Apply'), a:has-text('Apply'), [id*='apply']")
            if apply_btn:
                await apply_btn.click()
                await page.wait_for_timeout(4000)
                
            await page.fill("input[name='rec-form_746650000000063542']", CANDIDATE["first_name"])
            await page.fill("input[name='rec-form_746650000000063544']", CANDIDATE["last_name"])
            await page.fill("input[name='rec-form_746650000033319463']", CANDIDATE["full_name"])
            await page.fill("input[name='rec-form_746650000000063548']", CANDIDATE["email"])
            await page.fill("input[name='rec-form_746650000000063554']", CANDIDATE["phone"])
            await page.fill("input[name='rec-form_746650000000481107']", CANDIDATE["dob"])
            
            try:
                checkbox = await page.query_selector("#rec-form_746650000008186951")
                if checkbox:
                    await checkbox.check()
            except:
                pass
                
            prev_desc = ("As AI Development Lead at TopNetworks, I designed, built, and shipped several "
                         "internal SaaS tools (EmailGenius, TrafficGenius, RouteGenius) that replaced expensive "
                         "third-party subscriptions. I utilized Next.js 15, TypeScript, Python, and Vertex AI. "
                         "I led rapid prototyping using AI-assisted environments (Cursor, Copilot), which "
                         "significantly reduced engineering time and software licensing costs.")
            await page.fill("textarea[name='rec-form_746650000000477177']", prev_desc)
            
            try:
                resume_easy = await page.query_selector("input[name='rec-easyresume_file']")
                if resume_easy:
                    await resume_easy.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(1000)
                
                resume_eng = await page.query_selector("input[name='rec-form_746650000000072325_file']")
                if resume_eng:
                    await resume_eng.set_input_files(RESUME_VIBE_CODING)
                await page.wait_for_timeout(1000)
                
                efset = await page.query_selector("input[name='rec-form_746650000000072329_file']")
                if efset:
                    await efset.set_input_files(EFSET_CERTIFICATE)
                await page.wait_for_timeout(1000)
                
                specs = await page.query_selector("input[name='rec-form_746650000034125191_file']")
                if specs:
                    await specs.set_input_files(SPECS_SCREENSHOT)
                await page.wait_for_timeout(1000)
            except Exception as e:
                print("Error uploading Zoho Recruit files:", e)
                
            await page.screenshot(path=screenshot_path, full_page=True)
            
            submit_btn = await page.query_selector("input[type='submit'], button[type='submit'], button:has-text('Submit'), button:has-text('Apply')")
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
