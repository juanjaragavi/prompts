import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://ats.rippling.com/curve-dental/jobs/ef73da8e-d943-4bd0-9921-415901a748aa/apply?jobBoardSlug=curve-dental&jobId=ef73da8e-d943-4bd0-9921-415901a748aa&step=application', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        inputs = await page.query_selector_all('input, textarea, select')
        print("Rippling Inputs:")
        for inp in inputs:
            name = await inp.get_attribute('name')
            typ = await inp.get_attribute('type')
            id_ = await inp.get_attribute('id')
            placeholder = await inp.get_attribute('placeholder')
            print(f"Name: {name}, Type: {typ}, ID: {id_}, Placeholder: {placeholder}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
