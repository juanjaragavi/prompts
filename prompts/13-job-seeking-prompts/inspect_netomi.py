import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://jobs.lever.co/netomi/ba379f47-091b-4f2d-82d3-e97a0821227e/apply', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        inputs = await page.query_selector_all('input, textarea, select')
        print("Netomi Inputs:")
        for idx, inp in enumerate(inputs):
            name = await inp.get_attribute('name')
            typ = await inp.get_attribute('type')
            id_ = await inp.get_attribute('id')
            placeholder = await inp.get_attribute('placeholder')
            print(f"[{idx}] Name: {name}, Type: {typ}, ID: {id_}, Placeholder: {placeholder}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
