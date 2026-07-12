import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://workbetternow.zohorecruit.com/jobs/Careers/746650000037462674/AI-Software-Developer-Internal-Tools', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Check if we need to click 'Apply' or if the form is visible
        print("Zoho page title:", await page.title())
        apply_btn = await page.query_selector("button:has-text('Apply'), a:has-text('Apply')")
        if apply_btn:
            print("Found apply button, let's click it to see the form!")
            await apply_btn.click()
            await page.wait_for_timeout(4000)
            
        inputs = await page.query_selector_all('input, textarea, select')
        print("Zoho Inputs:")
        for inp in inputs:
            name = await inp.get_attribute('name')
            typ = await inp.get_attribute('type')
            id_ = await inp.get_attribute('id')
            placeholder = await inp.get_attribute('placeholder')
            print(f"Name: {name}, Type: {typ}, ID: {id_}, Placeholder: {placeholder}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
