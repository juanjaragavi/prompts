import asyncio
from playwright.async_api import async_playwright
import os
import json

async def select_react_dropdown(page, element_id, value_to_select):
    print(f"Selecting '{value_to_select}' for dropdown '{element_id}'...")
    try:
        await page.locator(f"#{element_id}").scroll_into_view_if_needed()
        await page.locator(f"#{element_id}").click(force=True)
        await page.wait_for_timeout(500)
        await page.locator(f"#{element_id}").fill(value_to_select)
        await page.wait_for_timeout(500)
        await page.locator(f"#{element_id}").press("Enter")
        await page.wait_for_timeout(500)
    except Exception as e:
        print(f"Error selecting {element_id}: {e}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "https://job-boards.greenhouse.io/embed/job_app?for=sezzle&token=6279644003&utm_source=Jobgether&utm_content=6a4249432da8cde35c7905a0-sr.-ai-engineer&utm_campaign=search&utm_medium=website"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # 1. Fill fields
        await page.locator("#first_name").fill("Juan Miguel")
        await page.locator("#last_name").fill("Jaramillo Gaviria")
        await page.locator("#email").fill("info@juanjaramillo.tech")
        await page.locator("#phone").fill("+573054206139")
        
        await select_react_dropdown(page, "candidate-location", "Bogota")
        
        resume_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Resume.pdf"
        if os.path.exists(resume_path):
            await page.locator("#resume").set_input_files(resume_path)
            print("Resume uploaded successfully")
            
        cl_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Master_Cover_Letter.pdf"
        if os.path.exists(cl_path):
            await page.locator("#cover_letter").set_input_files(cl_path)
            print("Cover letter uploaded successfully")
            
        await select_react_dropdown(page, "question_18767277003", "Yes")
        await page.locator("#question_18767278003").fill("Bogotá, Colombia")
        await select_react_dropdown(page, "question_18767279003", "Yes")
        await select_react_dropdown(page, "question_18767281003", "Yes")
        await page.locator("#question_18767284003").fill("4200")
        await page.locator("#question_27167596003").fill("Universidad Central")
        await select_react_dropdown(page, "question_18767280003", "N/A")
        await select_react_dropdown(page, "question_18767283003", "C1")
        await select_react_dropdown(page, "question_18767282003", "Other")
        await page.locator("#question_23998750003").fill("https://www.linkedin.com/in/juan-jaramillo-ai/")
        
        await page.wait_for_timeout(2000)
        
        # Locate the submit button
        submit_btn = page.locator("#submit_app, button[type='submit'], input[type='submit']")
        print("Submit button text/html:", await submit_btn.first.evaluate("el => el.outerHTML"))
        
        # Click submit
        print("Clicking submit button...")
        await submit_btn.first.click()
        
        # Wait up to 10 seconds for any confirmation or page changes
        print("Waiting for page load/navigation or CAPTCHA blocks...")
        await page.wait_for_timeout(8000)
        
        body_text = await page.locator("body").inner_text()
        url_after = page.url
        
        is_blocked = "captcha" in body_text.lower() or "robot" in body_text.lower() or "error" in body_text.lower() or "please solve" in body_text.lower() or url_after == url
        
        status_data = {}
        
        if is_blocked:
            print("Detected block, CAPTCHA, or errors.")
            screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/screenshot_additional_job_1_login.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Block screenshot saved to: {screenshot_path}")
            
            status_data = {
                "status": "blocked",
                "details": "The application form was blocked by CAPTCHA or form validation errors on submission.",
                "screenshot_path": screenshot_path,
                "pre_drafted_answers": {
                    "first_name": "Juan Miguel",
                    "last_name": "Jaramillo Gaviria",
                    "email": "info@juanjaramillo.tech",
                    "phone": "+57 305 420 6139",
                    "location": "Bogotá, Colombia",
                    "authorized_to_work_in_colombia": "Yes",
                    "current_residency": "Bogotá, Colombia",
                    "bachelors_degree_or_equivalent": "Yes",
                    "6_plus_years_ml_experience": "Yes",
                    "undergraduate_gpa": "N/A",
                    "english_level": "C1",
                    "source": "Other (Jobgether)",
                    "linkedin_profile": "https://www.linkedin.com/in/juan-jaramillo-ai/",
                    "monthly_salary_expectation_usd": "4200",
                    "university": "Universidad Central"
                }
            }
        else:
            print("Submission appeared to succeed!")
            screenshot_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/sezzle_success.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Success screenshot saved to: {screenshot_path}")
            
            status_data = {
                "status": "submitted",
                "details": "The application was completed and submitted successfully through the Greenhouse embed form.",
                "screenshot_path": screenshot_path,
                "pre_drafted_answers": {
                    "first_name": "Juan Miguel",
                    "last_name": "Jaramillo Gaviria",
                    "email": "info@juanjaramillo.tech",
                    "phone": "+57 305 420 6139",
                    "location": "Bogotá, Colombia",
                    "authorized_to_work_in_colombia": "Yes",
                    "current_residency": "Bogotá, Colombia",
                    "bachelors_degree_or_equivalent": "Yes",
                    "6_plus_years_ml_experience": "Yes",
                    "undergraduate_gpa": "N/A",
                    "english_level": "C1",
                    "source": "Other (Jobgether)",
                    "linkedin_profile": "https://www.linkedin.com/in/juan-jaramillo-ai/",
                    "monthly_salary_expectation_usd": "4200",
                    "university": "Universidad Central"
                }
            }
            
        status_file_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/additional_application_1_status.json"
        with open(status_file_path, 'w') as f:
            json.dump(status_data, f, indent=2)
        print(f"Status file written to: {status_file_path}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
