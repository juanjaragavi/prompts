import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://jobs.smartrecruiters.com/oneclick-ui/company/Medfar/publication/962a7b51-8f78-4cac-9914-2d045f619464?dcr_ci=Medfar', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        inputs = await page.query_selector_all('input')
        print("Inputs:")
        for inp in inputs:
            name = await inp.get_attribute('name')
            typ = await inp.get_attribute('type')
            id_ = await inp.get_attribute('id')
            placeholder = await inp.get_attribute('placeholder')
            print(f"Name: {name}, Type: {typ}, ID: {id_}, Placeholder: {placeholder}")
            
        textareas = await page.query_selector_all('textarea')
        print("\nTextareas:")
        for ta in textareas:
            name = await ta.get_attribute('name')
            id_ = await ta.get_attribute('id')
            print(f"Name: {name}, ID: {id_}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
