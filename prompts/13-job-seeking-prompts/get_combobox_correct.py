import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        cbs = await page.query_selector_all('[role="combobox"], select, [id*="input_CA"]')
        for i, cb in enumerate(cbs):
            name = await cb.get_attribute("name")
            id_ = await cb.get_attribute("id")
            # Get closest container text
            container_text = await cb.evaluate("""el => {
                let parent = el;
                for (let k = 0; k < 5; k++) {
                    if (parent.parentElement) parent = parent.parentElement;
                }
                return parent.innerText;
            }""")
            print(f"Combobox {i}: name={name}, id={id_}")
            print(f"Container text:\n{container_text}")
            print("=" * 50)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
