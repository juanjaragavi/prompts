import asyncio
import json
import os
import traceback
import logging
from datetime import datetime
from typing import Tuple, Optional
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from config import Config

class JobApplicationBot:
    """Base class for job application automation across multiple platforms"""
    
    def __init__(self, headless: bool = True):
        self.config = Config()
        self.candidate = self.config.get_candidate()
        self.browser_config = self.config.get_browser_config()
        self.output_dirs = self.config.get_output_dirs()
        self.headless = headless
        
        # Setup logging
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logging to file and console"""
        log_dir = self.output_dirs["logs_dir"]
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logger = logging.getLogger("JobApplicationBot")
        logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    async def load_page(
        self, 
        page: Page, 
        url: str, 
        wait_until: str = "domcontentloaded"
    ) -> bool:
        """Load a URL and handle basic errors"""
        try:
            await page.goto(url, wait_until=wait_until, timeout=self.browser_config["timeout_ms"])
            await page.wait_for_timeout(self.browser_config["page_load_wait_ms"])
            self.logger.info(f"Loaded: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load {url}: {str(e)}")
            return False
    
    async def check_blocked(self, page: Page) -> Tuple[bool, str]:
        """Check if page is blocked by anti-bot protection"""
        try:
            content = (await page.content()).lower()
            anti_patterns = self.config.get_anti_patterns()
            
            for keyword in anti_patterns["blocked_keywords"]:
                if keyword in content:
                    return True, f"Blocked by: {keyword}"
            
            return False, ""
        except Exception as e:
            self.logger.warning(f"Error checking block status: {str(e)}")
            return False, ""
    
    async def fill_field(
        self, 
        page: Page, 
        selector: str, 
        value: str,
        field_name: str = "field"
    ) -> bool:
        """Fill a single form field safely"""
        try:
            element = await page.query_selector(selector)
            if element:
                await element.fill(value)
                self.logger.debug(f"Filled {field_name}: {selector}")
                return True
            else:
                self.logger.warning(f"Selector not found for {field_name}: {selector}")
                return False
        except Exception as e:
            self.logger.error(f"Error filling {field_name}: {str(e)}")
            return False
    
    async def upload_file(
        self,
        page: Page,
        selector: str,
        file_path: str,
        file_name: str = "file"
    ) -> bool:
        """Upload a file to an input field"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return False
            
            file_input = await page.query_selector(selector)
            if file_input:
                await file_input.set_input_files(file_path)
                await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                self.logger.debug(f"Uploaded {file_name}: {selector}")
                return True
            else:
                self.logger.warning(f"File upload selector not found: {selector}")
                return False
        except Exception as e:
            self.logger.error(f"Error uploading {file_name}: {str(e)}")
            return False
    
    async def click_element(
        self,
        page: Page,
        selector: str,
        element_name: str = "element"
    ) -> bool:
        """Click an element safely"""
        try:
            element = await page.query_selector(selector)
            if element:
                await element.click()
                await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                self.logger.debug(f"Clicked {element_name}: {selector}")
                return True
            else:
                self.logger.warning(f"Click selector not found: {selector}")
                return False
        except Exception as e:
            self.logger.error(f"Error clicking {element_name}: {str(e)}")
            return False
    
    async def select_option(
        self,
        page: Page,
        selector: str,
        value: str,
        option_name: str = "option"
    ) -> bool:
        """Select an option from a dropdown"""
        try:
            element = await page.query_selector(selector)
            if element:
                await element.select_option(label=value)
                await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                self.logger.debug(f"Selected {option_name}: {value}")
                return True
            else:
                self.logger.warning(f"Select selector not found: {selector}")
                return False
        except Exception as e:
            self.logger.error(f"Error selecting {option_name}: {str(e)}")
            return False
    
    async def take_screenshot(
        self,
        page: Page,
        name: str,
        full_page: bool = False
    ) -> str:
        """Take screenshot and return path"""
        try:
            screenshot_dir = self.output_dirs["screenshots_dir"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
            
            await page.screenshot(path=screenshot_path, full_page=full_page)
            self.logger.debug(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return ""
    
    def save_status(
        self,
        index: int,
        company: str,
        job_title: str,
        platform: str,
        url: str,
        status: str,
        details: str,
        screenshot_path: str = ""
    ) -> str:
        """Save application status to JSON"""
        try:
            status_data = {
                "index": index,
                "company": company,
                "job_title": job_title,
                "platform": platform,
                "url": url,
                "status": status,
                "screenshot_path": screenshot_path,
                "details": details,
                "timestamp": datetime.now().isoformat()
            }
            
            status_file = os.path.join(
                self.output_dirs["status_dir"],
                f"application_status_{index}.json"
            )
            
            with open(status_file, "w") as f:
                json.dump(status_data, f, indent=2)
            
            self.logger.info(f"Status saved: {status_file} - {status}")
            return status_file
        except Exception as e:
            self.logger.error(f"Error saving status: {str(e)}")
            return ""
    
    async def apply_to_job(
        self,
        index: int,
        company: str,
        job_title: str,
        platform: str,
        url: str,
        context: BrowserContext
    ) -> Tuple[str, str, str]:
        """Main application handler - override in subclass for platform-specific logic"""
        page = await context.new_page()
        status = "Pending"
        details = "Default handler - no platform-specific logic implemented"
        screenshot_path = ""
        
        try:
            if not await self.load_page(page, url):
                return "Failed to Load", "Could not load job page", screenshot_path
            
            # Check for anti-bot blocks
            is_blocked, block_reason = await self.check_blocked(page)
            if is_blocked:
                screenshot_path = await self.take_screenshot(page, f"blocked_{index}")
                return "Blocked by Anti-Bot", block_reason, screenshot_path
            
            screenshot_path = await self.take_screenshot(page, f"application_{index}")
            status = "Requires Manual Action"
            details = "Platform-specific automation not implemented"
            
        except Exception as e:
            self.logger.error(f"Error in apply_to_job for {company}: {str(e)}")
            traceback.print_exc()
            status = "Error"
            details = str(e)
            try:
                screenshot_path = await self.take_screenshot(page, f"error_{index}")
            except:
                pass
        finally:
            await page.close()
        
        return status, details, screenshot_path
