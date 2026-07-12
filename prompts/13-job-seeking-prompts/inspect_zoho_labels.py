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
            await page.wait_for_timeout(4000)
            
            # Print outer HTML of parents to identify labels
            inputs = await page.query_selector_all('input, textarea, select')
            for i, inp in enumerate(inputs):
                name = await inp.get_attribute('name')
                id_ = await inp.get_attribute('id')
                typ = await inp.get_attribute('type')
                
                # Get surrounding text or closest label
                surrounding = await inp.evaluate("""el => {
                    const parent = el.closest('.rec-form-row, .form-group, div');
                    return parent ? parent.textContent.trim().replace(/\s+/g, ' ') : '';
                }""")
                print(f"[{i}] Name: {name}, ID: {id_}, Type: {typ}")
                print(f"    Text: {surrounding[:150]}")
                print("-" * 50)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
