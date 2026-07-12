import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://workbetternow.zohorecruit.com/jobs/Careers/746650000037462674/AI-Software-Developer-Internal-Tools', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Take pre-click screenshot
        await page.screenshot(path='/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/zoho_pre_click.png')
        
        # Click Apply button
        print("Clicking Apply button...")
        # Let's find button or element with text "Apply"
        apply_btn = await page.query_selector("button:has-text('Apply'), a:has-text('Apply'), [id*='apply']")
        if apply_btn:
            await apply_btn.click()
            print("Clicked!")
            await page.wait_for_timeout(5000)
            await page.screenshot(path='/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/zoho_post_click.png')
            
            # Print all inputs on page now
            inputs = await page.query_selector_all('input, textarea, select, iframe')
            print(f"Found {len(inputs)} inputs/iframes after clicking:")
            for inp in inputs:
                tag = await inp.evaluate("el => el.tagName")
                name = await inp.get_attribute('name')
                typ = await inp.get_attribute('type')
                id_ = await inp.get_attribute('id')
                src = await inp.get_attribute('src')
                print(f"Tag: {tag}, Name: {name}, Type: {typ}, ID: {id_}, Src: {src}")
        else:
            print("Apply button not found!")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
