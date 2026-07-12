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
            
            # Print outerHTML of parents
            inputs = await page.query_selector_all('input[type="file"]')
            for idx, inp in enumerate(inputs):
                name = await inp.get_attribute('name')
                parent_html = await inp.evaluate("""el => {
                    let parent = el;
                    for (let i = 0; i < 4; i++) {
                        if (parent.parentElement) parent = parent.parentElement;
                    }
                    return parent.outerHTML;
                }""")
                print(f"Index {idx}: name={name}")
                print(parent_html[:1500])
                print("=" * 60)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
