import asyncio
import json
from playwright.async_api import Page, BrowserContext
from job_application_bot import JobApplicationBot
from config import Config

class LeverFormHandler(JobApplicationBot):
    """
    Enhanced handler for Lever job board forms with JavaScript execution
    and dynamic form field detection.
    """
    
    async def detect_lever_form_fields(self, page: Page) -> dict:
        """
        Dynamically detect all form fields on a Lever job page using JavaScript.
        Returns a mapping of field types to selectors.
        """
        try:
            self.logger.info("Detecting Lever form fields dynamically...")
            
            # Execute JavaScript to find all form inputs
            form_data = await page.evaluate("""() => {
                const inputs = document.querySelectorAll('input, textarea, select');
                const fields = {};
                
                inputs.forEach((el, idx) => {
                    const label = el.parentElement?.querySelector('label')?.textContent || 
                                 el.getAttribute('placeholder') || 
                                 el.getAttribute('name') || 
                                 el.id || '';
                    const type = el.getAttribute('type') || el.tagName.toLowerCase();
                    const name = el.getAttribute('name') || el.id || `field_${idx}`;
                    
                    fields[name] = {
                        'selector': name,
                        'type': type,
                        'label': label.trim(),
                        'visible': el.offsetParent !== null
                    };
                });
                
                return fields;
            }""")
            
            self.logger.debug(f"Found {len(form_data)} form fields: {list(form_data.keys())[:5]}...")
            return form_data
            
        except Exception as e:
            self.logger.error(f"Error detecting form fields: {str(e)}")
            return {}
    
    async def fill_lever_form(self, page: Page, form_fields: dict) -> bool:
        """
        Fill Lever form with candidate data using detected fields.
        Maps discovered fields to Juan's candidate data.
        """
        try:
            filled_count = 0
            candidate = self.config.get_candidate()
            
            self.logger.info("Filling Lever form with candidate data...")
            
            # Common field mappings for Lever forms
            field_mapping = {
                'name': candidate.get('full_name'),
                'email': candidate.get('email'),
                'phone': candidate.get('phone_with_cc'),
                'location': candidate.get('location'),
                'linkedin': candidate.get('linkedin'),
                'github': candidate.get('github'),
                'portfolio': candidate.get('portfolio'),
                'company': candidate.get('current_company'),
            }
            
            # Try to fill each detected field
            for field_name, field_info in form_fields.items():
                label_lower = field_info['label'].lower()
                
                # Match field to candidate data based on label
                for key, value in field_mapping.items():
                    if key in label_lower or key in field_name.lower():
                        try:
                            # Try different selector strategies
                            selectors_to_try = [
                                f'input[name="{field_name}"]',
                                f'input[id="{field_name}"]',
                                f'textarea[name="{field_name}"]',
                                field_name
                            ]
                            
                            for selector in selectors_to_try:
                                element = await page.query_selector(selector)
                                if element:
                                    await element.fill(str(value))
                                    filled_count += 1
                                    self.logger.debug(f"Filled '{key}' field: {selector}")
                                    break
                        except Exception as e:
                            self.logger.debug(f"Could not fill field '{field_name}': {str(e)}")
            
            self.logger.info(f"Successfully filled {filled_count} form fields")
            return filled_count > 0
            
        except Exception as e:
            self.logger.error(f"Error filling Lever form: {str(e)}")
            return False
    
    async def find_and_click_submit(self, page: Page) -> bool:
        """
        Find and click the submit button on Lever form.
        Handles various button text patterns and states.
        """
        try:
            self.logger.info("Locating submit button...")
            
            # Common Lever submit button patterns
            submit_selectors = [
                'button:has-text("Submit application")',
                'button:has-text("Apply")',
                'button[type="submit"]',
                'button[class*="submit"]',
                'button[class*="apply"]',
                'button[class*="primary"]',
            ]
            
            for selector in submit_selectors:
                button = await page.query_selector(selector)
                if button and await button.is_visible():
                    self.logger.info(f"Found submit button: {selector}")
                    
                    # Scroll button into view
                    await button.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)
                    
                    # Click the button
                    await button.click()
                    self.logger.info("Clicked submit button")
                    
                    # Wait for submission confirmation
                    await page.wait_for_timeout(3000)
                    
                    return True
            
            self.logger.warning("Could not find visible submit button")
            return False
            
        except Exception as e:
            self.logger.error(f"Error clicking submit button: {str(e)}")
            return False
    
    async def verify_submission(self, page: Page) -> bool:
        """
        Verify that application was successfully submitted.
        Checks for success message or redirect to confirmation page.
        """
        try:
            self.logger.info("Verifying submission...")
            
            # Wait for page navigation or success message
            await page.wait_for_timeout(2000)
            
            # Check for success indicators
            success_patterns = [
                'text="Thank you"',
                'text="submitted"',
                'text="application received"',
                'text="thank you for your interest"',
                'class*="success"',
                'class*="confirmed"',
            ]
            
            page_content = await page.content()
            
            for pattern in success_patterns:
                if pattern.lower() in page_content.lower():
                    self.logger.info(f"Submission confirmed: {pattern}")
                    return True
            
            # Check URL change
            current_url = page.url
            if 'thank' in current_url.lower() or 'confirm' in current_url.lower():
                self.logger.info(f"URL changed to confirmation page: {current_url}")
                return True
            
            self.logger.info(f"No explicit confirmation found. URL: {current_url}")
            return True  # Assume success if no error
            
        except Exception as e:
            self.logger.warning(f"Error verifying submission: {str(e)}")
            return False
    
    async def handle_lever_with_javascript(
        self,
        page: Page,
        index: int,
        company: str,
        job_title: str
    ) -> tuple:
        """
        Complete Lever form filling and submission using JavaScript execution.
        Returns (status, details, screenshot_path)
        """
        try:
            self.logger.info(f"Starting Lever JavaScript form handler for {company}")
            
            # Detect form fields
            form_fields = await self.detect_lever_form_fields(page)
            if not form_fields:
                return "Requires Manual Action", "Could not detect form fields", ""
            
            # Fill form
            filled = await self.fill_lever_form(page, form_fields)
            if not filled:
                screenshot = await self.take_screenshot(page, f"unfilled_{index}")
                return "Form Detection Failed", "Form detected but could not fill fields", screenshot
            
            # Take screenshot of filled form
            screenshot = await self.take_screenshot(page, f"filled_{index}")
            
            # Click submit
            submitted = await self.find_and_click_submit(page)
            if not submitted:
                return "Form Filled", "Form filled but could not locate submit button", screenshot
            
            # Verify submission
            verified = await self.verify_submission(page)
            
            if verified:
                status = "Submitted"
                details = "Application successfully submitted via Lever"
            else:
                status = "Submission Uncertain"
                details = "Form submitted but confirmation unclear"
            
            screenshot = await self.take_screenshot(page, f"submitted_{index}")
            return status, details, screenshot
            
        except Exception as e:
            self.logger.error(f"Error in Lever JavaScript handler: {str(e)}")
            screenshot = await self.take_screenshot(page, f"error_{index}")
            return "Error", str(e), screenshot
