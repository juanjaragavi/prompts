import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://apply.workable.com/therapynotes/j/2A691CE916/apply/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        # In Workable, radio options (like Yes/No) are inside fieldsets.
        # Let's inspect the fieldset text or legend for inputs with name QA_...
        inputs = await page.query_selector_all('input[type="radio"]')
        seen_names = set()
        for inp in inputs:
            name = await inp.get_attribute('name')
            if name and name not in seen_names:
                seen_names.add(name)
                # Find parent fieldset and print its text
                fieldset_text = await page.evaluate("""el => {
                    const fs = el.closest('fieldset');
                    return fs ? fs.textContent.strip() : null;
                }""", inp)
                print(f"Name: {name}")
                print(f"Fieldset text:\n{fieldset_text}")
                print("-" * 40)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
