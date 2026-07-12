import asyncio
from playwright.async_api import async_playwright

async def inspect_page(url, label):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        print(f"\n--- Buttons on {label} ---")
        buttons = await page.query_selector_all('button, input[type=\"submit\"], [role=\"button\"]')
        for idx, btn in enumerate(buttons):
            tag = await btn.evaluate('el => el.tagName')
            text = await btn.text_content()
            id_ = await btn.get_attribute('id')
            class_ = await btn.get_attribute('class')
            typ = await btn.get_attribute('type')
            print(f"[{idx}] Tag: {tag}, Text: {repr(text.strip())}, ID: {id_}, Class: {class_}, Type: {typ}")
            
        await browser.close()

async def main():
    # Ashby
    await inspect_page('https://jobs.ashbyhq.com/bjakcareer/0ab4a37a-0779-4480-8d3a-bbaf093c2da8/application', 'Bjak (Ashby)')
    # Lever
    await inspect_page('https://jobs.lever.co/xsolla/d1cc3abc-fc26-4732-97ba-49971da226cf/apply', 'Xsolla (Lever)')

if __name__ == '__main__':
    asyncio.run(main())
