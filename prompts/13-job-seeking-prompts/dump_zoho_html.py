import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://workbetternow.zohorecruit.com/jobs/Careers/746650000037462674/AI-Software-Developer-Internal-Tools', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        apply_btn = await page.query_selector("button:has-text('Apply'), a:has-text('Apply'), [id*='apply']")
        if apply_btn:
            await apply_btn.click()
            await page.wait_for_timeout(5000)
            
            html = await page.content()
            with open('/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/zoho_form.html', 'w') as f:
                f.write(html)
            print("Dumped Zoho form HTML to /Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/zoho_form.html")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
