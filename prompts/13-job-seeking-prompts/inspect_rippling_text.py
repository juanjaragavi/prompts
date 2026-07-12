import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://ats.rippling.com/curve-dental/jobs/ef73da8e-d943-4bd0-9921-415901a748aa/apply?jobBoardSlug=curve-dental&jobId=ef73da8e-d943-4bd0-9921-415901a748aa&step=application', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # Print the text content of divs that contain input fields to match them up
        inputs = await page.query_selector_all('input, textarea, select')
        for idx, inp in enumerate(inputs):
            name = await inp.get_attribute('name')
            id_ = await inp.get_attribute('id')
            
            # Print parent text up to 3 levels
            parent_text = await inp.evaluate("""el => {
                let parent = el;
                for (let i = 0; i < 4; i++) {
                    if (parent.parentElement) parent = parent.parentElement;
                }
                return parent.innerText;
            }""")
            print(f"[{idx}] Name: {name}, ID: {id_}")
            print("  Parent InnerText:")
            print(repr(parent_text.strip().replace('\n', ' | ')[:300]))
            print("-" * 50)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
