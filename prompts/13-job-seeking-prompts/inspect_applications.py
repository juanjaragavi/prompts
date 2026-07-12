import asyncio
import os
import json
from playwright.async_api import async_playwright

async def main():
    with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/open_applications_inventory.json', 'r') as f:
        inventory = json.load(f)
        
    os.makedirs('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/inspections', exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        for app in inventory:
            index = app['index']
            company = app['company']
            url = app['url']
            print(f"Inspecting {index}: {company} -> {url}")
            
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(5000)
                
                # Take screenshot
                ss_path = f"/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/inspections/{index}_{company}.png"
                await page.screenshot(path=ss_path, full_page=False)
                
                # Dump HTML or interactive text
                title = await page.title()
                print(f"Success. Title: {title}. Screenshot saved to {ss_path}")
            except Exception as e:
                print(f"Failed to inspect {index} {company}: {e}")
            finally:
                await page.close()
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
