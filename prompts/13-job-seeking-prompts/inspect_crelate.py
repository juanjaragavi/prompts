import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://jobs.crelate.com/portal/teamreddog/job/apply/ny9o6rxqgq7juw8t8z4oo3zp6c', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        inputs = await page.query_selector_all('input, textarea, select')
        print("Crelate Inputs:")
        for inp in inputs:
            name = await inp.get_attribute('name')
            typ = await inp.get_attribute('type')
            id_ = await inp.get_attribute('id')
            placeholder = await inp.get_attribute('placeholder')
            print(f"Name: {name}, Type: {typ}, ID: {id_}, Placeholder: {placeholder}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
