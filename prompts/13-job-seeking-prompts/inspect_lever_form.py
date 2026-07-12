import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Inspect Xsolla
        print("--- Inspecting Xsolla Lever form ---")
        await page.goto('https://jobs.lever.co/xsolla/d1cc3abc-fc26-4732-97ba-49971da226cf/apply', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Dump all text of labels or question headings
        questions = await page.query_selector_all('div.application-label, label, div.application-question')
        for idx, q in enumerate(questions):
            text = await q.text_content()
            print(f"[{idx}] {text.strip()}")
            print("-" * 30)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
