import asyncio
import os
import json
from playwright.async_api import async_playwright, BrowserContext
from job_application_bot import JobApplicationBot
from lever_handler import LeverFormHandler
from config import Config

class EnhancedMultiPlatformBot(LeverFormHandler):
    """Enhanced bot with Phase 2 Lever JavaScript support"""
    
    async def apply_to_job(
        self,
        index: int,
        company: str,
        job_title: str,
        platform: str,
        url: str,
        context: BrowserContext
    ):
        """Route to platform-specific handler with Phase 2 enhancements"""
        self.logger.info(f"Processing Index {index}: {company} - {job_title} ({platform})")
        
        page = await context.new_page()
        status = "Pending"
        details = ""
        screenshot_path = ""
        
        try:
            if not await self.load_page(page, url):
                status = "Failed to Load"
                details = "Could not load job page"
                return status, details, screenshot_path
            
            # Check for anti-bot blocks
            is_blocked, block_reason = await self.check_blocked(page)
            if is_blocked:
                screenshot_path = await self.take_screenshot(page, f"blocked_{index}")
                return "Requires Manual Action", block_reason, screenshot_path
            
            # Route to platform handler
            platform_lower = platform.lower()
            
            if platform_lower == "lever":
                # Use Phase 2 JavaScript handler for Lever
                status, details, screenshot_path = await self.handle_lever_with_javascript(
                    page, index, company, job_title
                )
            elif platform_lower == "smartrecruiters":
                status, details = await self._handle_smartrecruiters(page, index)
                screenshot_path = await self.take_screenshot(page, f"application_{index}")
            elif platform_lower == "workable":
                status, details = await self._handle_workable(page, index)
                screenshot_path = await self.take_screenshot(page, f"application_{index}", full_page=True)
            elif platform_lower == "ashby":
                status, details = await self._handle_ashby(page, index)
                screenshot_path = await self.take_screenshot(page, f"application_{index}")
            elif platform_lower == "crelate":
                status, details = await self._handle_crelate(page, index)
                screenshot_path = await self.take_screenshot(page, f"application_{index}")
            elif platform_lower == "rippling":
                status, details = await self._handle_rippling(page, index)
                screenshot_path = await self.take_screenshot(page, f"application_{index}")
            elif platform_lower == "zoho recruit":
                status, details = await self._handle_zoho_recruit(page, index)
                screenshot_path = await self.take_screenshot(page, f"application_{index}")
            else:
                status = "Unsupported Platform"
                details = f"No handler for platform: {platform}"
                screenshot_path = await self.take_screenshot(page, f"application_{index}")
            
        except Exception as e:
            self.logger.error(f"Error in apply_to_job: {str(e)}")
            status = "Error"
            details = str(e)
            try:
                screenshot_path = await self.take_screenshot(page, f"error_{index}")
            except:
                pass
        finally:
            await page.close()
        
        return status, details, screenshot_path
    
    # Platform handlers (from previous implementation)
    async def _handle_smartrecruiters(self, page, index) -> tuple:
        platform_config = self.config.get_platform_config("smartrecruiters")
        selectors = platform_config["selectors"]
        resume_variant = platform_config["resume_variant"]
        resume_path = self.config.get_resume_path(resume_variant)
        
        await self.fill_field(page, selectors["first_name"], self.candidate["first_name"], "first_name")
        await self.fill_field(page, selectors["last_name"], self.candidate["last_name"], "last_name")
        await self.fill_field(page, selectors["email"], self.candidate["email"], "email")
        await self.fill_field(page, selectors["phone"], self.candidate["phone_with_cc"], "phone")
        await self.upload_file(page, selectors["resume"], resume_path, "resume")
        
        return "Form Filled", "SmartRecruiters form filled successfully"
    
    async def _handle_workable(self, page, index) -> tuple:
        platform_config = self.config.get_platform_config("workable")
        selectors = platform_config["selectors"]
        resume_variant = platform_config["resume_variant"]
        resume_path = self.config.get_resume_path(resume_variant)
        
        try:
            await page.evaluate("""() => {
                const c = document.querySelector('[data-ui="cookie-consent"]');
                if (c) c.remove();
                const b = document.querySelector('[data-ui="backdrop"]');
                if (b) b.remove();
            }""")
        except:
            pass
        
        await page.wait_for_timeout(1000)
        
        await self.fill_field(page, selectors["first_name"], self.candidate["first_name"], "first_name")
        await self.fill_field(page, selectors["last_name"], self.candidate["last_name"], "last_name")
        await self.fill_field(page, selectors["email"], self.candidate["email"], "email")
        await self.fill_field(page, selectors["phone"], self.candidate["phone"], "phone")
        await self.fill_field(page, selectors["address"], self.candidate["address"], "address")
        await self.fill_field(page, selectors["city"], self.candidate["city"], "city")
        await self.fill_field(page, selectors["postcode"], self.candidate["postcode"], "postcode")
        await self.fill_field(page, selectors["country"], self.candidate["country"], "country")
        
        await self.upload_file(page, selectors["resume"], resume_path, "resume")
        
        questions = platform_config.get("questions", {})
        for field_name, value in questions.items():
            selector = f"[name='{field_name}']"
            await self.fill_field(page, selector, value, field_name)
        
        essay_selector = "[name='QA_12085438']"
        essay_text = self.config.get_essay_template("ai_experience")
        await self.fill_field(page, essay_selector, essay_text, "ai_experience_essay")
        
        submit_btn = await page.query_selector("button:has-text('Submit application')")
        if submit_btn:
            await self.click_element(page, "button:has-text('Submit application')", "submit_button")
            await page.wait_for_timeout(6000)
            return "Submitted", "Application submitted on Workable"
        else:
            return "Form Filled", "Could not find submit button"
    
    async def _handle_ashby(self, page, index) -> tuple:
        platform_config = self.config.get_platform_config("ashby")
        selectors = platform_config["selectors"]
        resume_variant = platform_config["resume_variant"]
        resume_path = self.config.get_resume_path(resume_variant)
        
        await self.upload_file(page, selectors["resume"], resume_path, "resume")
        await self.fill_field(page, selectors["name"], self.candidate["full_name"], "name")
        await self.fill_field(page, selectors["email"], self.candidate["email"], "email")
        await self.fill_field(page, selectors["phone"], self.candidate["phone_with_cc"], "phone")
        await self.fill_field(page, selectors["location"], self.candidate["location"], "location")
        await self.fill_field(page, selectors["linkedin"], self.candidate["linkedin"], "linkedin")
        await self.fill_field(page, selectors["github"], self.candidate["github"], "github")
        
        if await self.click_element(page, selectors["submit"], "submit_button"):
            await page.wait_for_timeout(6000)
            return "Submitted", "Form submitted on Ashby"
        else:
            return "Form Filled", "Could not locate Ashby submit button"
    
    async def _handle_crelate(self, page, index) -> tuple:
        platform_config = self.config.get_platform_config("crelate")
        selectors = platform_config["selectors"]
        resume_variant = platform_config["resume_variant"]
        resume_path = self.config.get_resume_path(resume_variant)
        
        await self.fill_field(page, selectors["first_name"], self.candidate["first_name"], "first_name")
        await self.fill_field(page, selectors["last_name"], self.candidate["last_name"], "last_name")
        await self.fill_field(page, selectors["email"], self.candidate["email"], "email")
        await self.fill_field(page, selectors["phone"], self.candidate["phone_with_cc"], "phone")
        await self.upload_file(page, selectors["resume"], resume_path, "resume")
        await self.click_element(page, selectors["consent"], "consent_checkbox")
        
        if await self.click_element(page, selectors["submit"], "submit_button"):
            await page.wait_for_timeout(6000)
            return "Submitted", "Form submitted on Crelate"
        else:
            return "Form Filled", "Could not locate Crelate submit button"
    
    async def _handle_rippling(self, page, index) -> tuple:
        platform_config = self.config.get_platform_config("rippling")
        selectors = platform_config["selectors"]
        resume_variant = platform_config["resume_variant"]
        resume_path = self.config.get_resume_path(resume_variant)
        
        await self.fill_field(page, selectors["first_name"], self.candidate["first_name"], "first_name")
        await self.fill_field(page, selectors["last_name"], self.candidate["last_name"], "last_name")
        await self.fill_field(page, selectors["email"], self.candidate["email"], "email")
        await self.fill_field(page, selectors["phone"], self.candidate["phone_with_cc"], "phone")
        await self.fill_field(page, selectors["location"], self.candidate["location"], "location")
        await self.fill_field(page, selectors["company"], self.candidate["company"], "company")
        await self.upload_file(page, selectors["resume"], resume_path, "resume")
        await self.fill_field(page, selectors["salary"], "$42,000 - $54,000 USD", "salary_expectations")
        
        experience_text = f"{self.candidate['years_experience']} years software engineering, {self.candidate['years_ai_experience']} years AI/ML"
        await self.fill_field(page, selectors["experience"], experience_text, "experience")
        
        if await self.click_element(page, selectors["submit"], "submit_button"):
            await page.wait_for_timeout(6000)
            return "Submitted", "Form submitted on Rippling"
        else:
            return "Form Filled", "Could not locate Rippling submit button"
    
    async def _handle_zoho_recruit(self, page, index) -> tuple:
        platform_config = self.config.get_platform_config("zoho_recruit")
        selectors = platform_config["selectors"]
        resume_variant = platform_config["resume_variant"]
        resume_path = self.config.get_resume_path(resume_variant)
        
        try:
            await self.click_element(page, "button:has-text('Accept')", "cookie_accept")
        except:
            pass
        
        try:
            await self.click_element(page, "button:has-text('Apply')", "apply_button")
            await page.wait_for_timeout(4000)
        except:
            pass
        
        await self.fill_field(page, selectors["first_name"], self.candidate["first_name"], "first_name")
        await self.fill_field(page, selectors["last_name"], self.candidate["last_name"], "last_name")
        await self.fill_field(page, selectors["full_name"], self.candidate["full_name"], "full_name")
        await self.fill_field(page, selectors["email"], self.candidate["email"], "email")
        await self.fill_field(page, selectors["phone"], self.candidate["phone"], "phone")
        await self.fill_field(page, selectors["dob"], self.candidate["dob"], "dob")
        
        await self.upload_file(page, selectors["resume_easy"], resume_path, "resume_easy")
        await self.upload_file(page, selectors["resume_eng"], resume_path, "resume_eng")
        
        efset_path = self.config.get_document_path("efset_certificate")
        if efset_path:
            await self.upload_file(page, selectors["efset"], efset_path, "efset_certificate")
        
        specs_path = self.config.get_document_path("specs_screenshot")
        if specs_path:
            await self.upload_file(page, selectors["specs"], specs_path, "specs_screenshot")
        
        prev_desc = self.config.get_essay_template("previous_role")
        await self.fill_field(page, selectors["description"], prev_desc, "previous_role_description")
        
        try:
            await self.click_element(page, selectors["phone_policy"], "phone_policy_checkbox")
        except:
            pass
        
        if await self.click_element(page, selectors["submit"], "submit_button"):
            await page.wait_for_timeout(6000)
            return "Submitted", "Form submitted on Zoho Recruit"
        else:
            return "Form Filled", "Could not locate Zoho Recruit submit button"


async def main():
    """Main entry point with Phase 2 enhancements"""
    config = Config()
    bot = EnhancedMultiPlatformBot(headless=config.get_browser_config()["headless"])
    
    # Load job inventory
    inventory_file = os.path.join(config.get_output_dirs()["status_dir"], "open_applications_inventory.json")
    if not os.path.exists(inventory_file):
        bot.logger.error(f"Inventory file not found: {inventory_file}")
        return
    
    with open(inventory_file, "r") as f:
        inventory = json.load(f)
    
    # Create browser and context
    async with async_playwright() as p:
        browser_cfg = config.get_browser_config()
        browser = await p.chromium.launch(headless=bot.headless)
        context = await browser.new_context(
            user_agent=browser_cfg["user_agent"],
            viewport={
                "width": browser_cfg["viewport_width"],
                "height": browser_cfg["viewport_height"]
            }
        )
        
        # Process each job
        for app in inventory:
            index = app["index"]
            company = app["company"]
            job_title = app["job_title"]
            platform = app["platform"]
            url = app["url"]
            
            status, details, screenshot_path = await bot.apply_to_job(
                index, company, job_title, platform, url, context
            )
            
            # Save status
            bot.save_status(index, company, job_title, platform, url, status, details, screenshot_path)
        
        await browser.close()
    
    bot.logger.info("All applications processed with Phase 2 enhancements")


if __name__ == "__main__":
    asyncio.run(main())
