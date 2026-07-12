import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Let's inspect CA_42077
        element = await page.query_selector('[name="CA_42077"]')
        if element:
            parent = await element.evaluate_handle('el => el.closest("[data-ui*=\'form-field\']")')
            if parent:
                text = await parent.evaluate('el => el.textContent.strip()')
                print("CA_42077 complete text:", repr(text))
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
